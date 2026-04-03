
import math
from debug_utils import LOG_WARNING # type: ignore
from AvatarInputHandler import gun_marker_ctrl # type: ignore
from aih_constants import SHOT_RESULT as _SHOT_RESULT # type: ignore
from gui import update_gui, hide_labels, GuiState

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

def call_update_gui(avg_pen, min_pen, max_pen, armor_val, ricochet, hit_body):
    
    prob = 0
    if not ricochet and hit_body:
        prob = get_gaussian_probability(avg_pen, armor_val)

    update_gui(armor_val, prob, ricochet, hit_body)


log("Mod is loading")

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
    call_update_gui(fullPiercingPower, min_possible_pen, max_possible_pen, total_armor_val, ricochet, hit_body)

    return result

original_getShotResult = gun_marker_ctrl._CrosshairShotResults.getShotResult.__func__

def my_get_shot_result(cls, gunMarker, excludeTeam=0, piercingMultiplier=1):
    result = original_getShotResult(cls, gunMarker, excludeTeam, piercingMultiplier)
    if result == _SHOT_RESULT.UNDEFINED and GuiState.is_visible:
        # only call hide if the gui is still visible
        hide_labels()
    return result


# overriding source code functions
gun_marker_ctrl._CrosshairShotResults.getShotResult = classmethod(my_get_shot_result)

gun_marker_ctrl._CrosshairShotResults._CrosshairShotResults__shotResultDefault = classmethod(my_shot_result_default)

log("Mod has finished loading")
