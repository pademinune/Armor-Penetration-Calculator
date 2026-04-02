
import math
import GUI
import constants
import logging
import BigWorld
from debug_utils import LOG_WARNING
from AvatarInputHandler import gun_marker_ctrl
from aih_constants import SHOT_RESULT as _SHOT_RESULT

def log(message):
    LOG_WARNING("pademinune: " + str(message))

def get_gaussian_probability(avg_pen, armor_val):
    min_pen = avg_pen * 0.75
    max_pen = avg_pen * 1.25

    if armor_val <= min_pen: 
        return 100.0
    if armor_val >= max_pen: 
        return 0.0
    
    # 12 * (armor_val - avg_pen) / (avg_pen)
    # If 25% is the 3-sigma point:
    # avg_pen * 0.25 = 3 SD.
    standard_deviation = avg_pen / 12
    
    # z-score
    z = (armor_val - avg_pen) / standard_deviation
    
    # Cumulative Distribution Function (CDF)
    # P(pen < armor)
    phi = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
    
    # get area to the right P(pen > armor)
    prob = (1.0 - phi) * 100
    
    return prob

# or try:
# red: E90000
# yellow: FFAD00
# green: 6BF40D

RED = (255, 0, 0, 255)
YELLOW = (255, 255, 0, 255)
ORANGE = (255, 173, 0, 255)
GREEN = (0, 255, 0, 255)
GREY = (128, 128, 128, 255)
PURPLE = (128, 0, 128, 255)

log("Mod is loading")

# Create a text component
label = GUI.Text("")

label.position = (0, -0.1, 0.5) # Center of screen, slightly below crosshair
label.visible = False
GUI.addRoot(label)

label.text = "ARMOR PEN LABEL"
label.colour = GREY
label.visible = True

def update_ui(text, color_vec4 = GREY):
    label.text = text
    label.colour = color_vec4 # (R, G, B, A) from 0-255
    label.visible = True

def update_ui_with_stats(avg_pen, min_pen, max_pen, armor_val, ricochet, hit_body):

    if ricochet:
        # shell ricochet
        color = PURPLE
        update_ui("- | 0%", color)
        return
    
    if not hit_body:
        # shell only hits spaced armor or tracks
        color = RED
        update_ui("- | 0%", color)
        return


    prob = get_gaussian_probability(avg_pen, armor_val)

    color = GREY
    if prob <= 7:
        # armor_val is right of z = 1.5
        color = RED
    elif prob >= 93:
        # armor_val is left of z = -1.5
        color = GREEN
    else:
        color = ORANGE

    update_ui("{}mm | {}%".format(int(armor_val), int(prob)), color)


# functin override
def my_shot_result_default(cls, gunMarker, collisionsDetails, fullPiercingPower, shell, minPP, maxPP, entity):
    # pademinune armor mod variables
    total_armor_val = 0.0
    ricochet = False
    hit_body = False
    
    # Since we are outside the class, we must use the mangled names
    isDestructible = cls._CrosshairShotResults__isDestructibleComponent
    collectDebug = cls._CrosshairShotResults__collectDebugPiercingData
    sendDebug = cls._CrosshairShotResults__sendDebugInfo
    
    result = _SHOT_RESULT.NOT_PIERCED
    isJet = False
    jetStartDist = None
    piercingPower = fullPiercingPower
    dispersion = round(piercingPower) * shell.piercingPowerRandomization
    minPiercingPower = round(round(piercingPower) - dispersion)
    maxPiercingPower = round(round(piercingPower) + dispersion)
    ignoredMaterials = set()
    debugPiercingsList = []

    for cDetails in collisionsDetails:
        if not isDestructible(entity, cDetails.compName):
            break
        if isJet:
            jetDist = cDetails.dist - jetStartDist
            if jetDist > 0.0:
                lossByDist = 1.0 - jetDist * cls._SHELL_EXTRA_DATA[shell.kind].jetLossPPByDist
                
                # add dissipation amount onto total armor
                lost_pen = max(0, piercingPower * (1 - lossByDist)) # max ensures no negative penetration dropoffs (when models overlap)
                total_armor_val += lost_pen
                # log("heat dropoff: {}mm".format(lost_pen))

                piercingPower *= lossByDist
                minPiercingPower = round(minPiercingPower * lossByDist)
                maxPiercingPower = round(maxPiercingPower * lossByDist)
        
        if cDetails.matInfo is None:
            result = cls._CRIT_ONLY_SHOT_RESULT
        else:
            matInfo = cDetails.matInfo
            if (cDetails.compName, matInfo.kind) in ignoredMaterials:
                continue
            if matInfo.armor is None:
                result = _SHOT_RESULT.UNDEFINED
                continue
                
            hitAngleCos = cDetails.hitAngleCos if matInfo.useHitAngle else 1.0
            piercingPercent = 1000.0
            
            if not isJet and cls._shouldRicochet(shell, hitAngleCos, matInfo):
                # shell ricochet
                ricochet = True
                collectDebug(debugPiercingsList, None, hitAngleCos, minPiercingPower, maxPiercingPower, piercingPercent, matInfo, _SHOT_RESULT.NOT_PIERCED)
                break
                
            penetrationArmor = 0
            if piercingPower > 0.0:
                penetrationArmor = cls._computePenetrationArmor(shell, hitAngleCos, matInfo)
                
                # add to total armor counter
                total_armor_val += penetrationArmor
                
                piercingPercent = 100.0 + (penetrationArmor - piercingPower) / fullPiercingPower * 100.0
                piercingPower -= penetrationArmor
                minPiercingPower = round(minPiercingPower - penetrationArmor)
                maxPiercingPower = round(maxPiercingPower - penetrationArmor)

            if matInfo.vehicleDamageFactor:
                # main armor plate
                hit_body = True
                if minPP < piercingPercent < maxPP:
                    result = _SHOT_RESULT.LITTLE_PIERCED
                elif piercingPercent <= minPP:
                    result = _SHOT_RESULT.GREAT_PIERCED
                collectDebug(debugPiercingsList, penetrationArmor, hitAngleCos, minPiercingPower, maxPiercingPower, piercingPercent, matInfo, result)
                break
            else:
                # spaced armor
                debugResut = _SHOT_RESULT.NOT_PIERCED
                if minPP < piercingPercent < maxPP:
                    debugResut = _SHOT_RESULT.LITTLE_PIERCED
                elif piercingPercent <= minPP:
                    debugResut = _SHOT_RESULT.GREAT_PIERCED
                if matInfo.extra:
                    if piercingPercent <= maxPP:
                        result = cls._CRIT_ONLY_SHOT_RESULT
                collectDebug(debugPiercingsList, penetrationArmor, hitAngleCos, minPiercingPower, maxPiercingPower, piercingPercent, matInfo, debugResut)
            
            if matInfo.collideOnceOnly:
                ignoredMaterials.add((cDetails.compName, matInfo.kind))
        
        if piercingPower <= 0.0:
            break
            
        if cls._SHELL_EXTRA_DATA[shell.kind].jetLossPPByDist > 0.0:
            isJet = True
            mInfo = cDetails.matInfo
            armor = mInfo.armor if mInfo is not None else 0.0
            jetStartDist = cDetails.dist + armor * 0.001

    sendDebug(gunMarker, debugPiercingsList, minPP, maxPP, fullPiercingPower)

    # pademinune armor mod calc
    min_possible_pen = fullPiercingPower * 0.75
    max_possible_pen = fullPiercingPower * 1.25
    update_ui_with_stats(fullPiercingPower, min_possible_pen, max_possible_pen, total_armor_val, ricochet, hit_body)

    return result

# override source code function
gun_marker_ctrl._CrosshairShotResults._CrosshairShotResults__shotResultDefault = classmethod(my_shot_result_default)

log("Mod has finished loading")
