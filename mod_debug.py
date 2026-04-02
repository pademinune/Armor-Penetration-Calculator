import BigWorld
import math
import constants
import logging
from debug_utils import LOG_WARNING
from AvatarInputHandler import gun_marker_ctrl
from aih_constants import SHOT_RESULT as _SHOT_RESULT

_logger = logging.getLogger(__name__)

def log(message):
    LOG_WARNING("pademinune: " + str(message))

log("Armor Mod Loading...")

# --- THE FIXED OVERRIDE ---
def my_function(cls, gunMarker, collisionsDetails, fullPiercingPower, shell, minPP, maxPP, entity):
    # Fix 1: Initialize counters
    total_armor_val = 0.0
    
    # Fix 2: Localize references to private class members
    # Since we are outside the class, we must use the "Mangled" names
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
                _logger.error('Unconfigured/default material/armor for material kind %d', matInfo.kind)
                continue
                
            hitAngleCos = cDetails.hitAngleCos if matInfo.useHitAngle else 1.0
            piercingPercent = 1000.0
            
            if not isJet and cls._shouldRicochet(shell, hitAngleCos, matInfo):
                collectDebug(debugPiercingsList, None, hitAngleCos, minPiercingPower, maxPiercingPower, piercingPercent, matInfo, _SHOT_RESULT.NOT_PIERCED)
                break
                
            penetrationArmor = 0
            if piercingPower > 0.0:
                # This is the "Reduced Armor" for the current layer
                penetrationArmor = cls._computePenetrationArmor(shell, hitAngleCos, matInfo)
                
                # Update your counter
                total_armor_val += penetrationArmor
                
                piercingPercent = 100.0 + (penetrationArmor - piercingPower) / fullPiercingPower * 100.0
                piercingPower -= penetrationArmor
                minPiercingPower = round(minPiercingPower - penetrationArmor)
                maxPiercingPower = round(maxPiercingPower - penetrationArmor)

            if matInfo.vehicleDamageFactor:
                if minPP < piercingPercent < maxPP:
                    result = _SHOT_RESULT.LITTLE_PIERCED
                elif piercingPercent <= minPP:
                    result = _SHOT_RESULT.GREAT_PIERCED
                collectDebug(debugPiercingsList, penetrationArmor, hitAngleCos, minPiercingPower, maxPiercingPower, piercingPercent, matInfo, result)
                break
            else:
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

    # --- YOUR CUSTOM PROBABILITY CALC ---
    # WoT RNG is +/- 25% of the fullPiercingPower (which is already distance-adjusted)
    min_possible_pen = fullPiercingPower * 0.75
    max_possible_pen = fullPiercingPower * 1.25
    
    if total_armor_val <= min_possible_pen:
        prob = 100
    elif total_armor_val >= max_possible_pen:
        prob = 0
    else:
        prob = ((max_possible_pen - total_armor_val) / (max_possible_pen - min_possible_pen)) * 100

    log("{}mm | {}%".format(int(total_armor_val), int(prob)))

    return result

# 4. Apply the hook to the private mangled method name
gun_marker_ctrl._CrosshairShotResults._CrosshairShotResults__shotResultDefault = classmethod(my_function)

log("Mod has finished loading")
