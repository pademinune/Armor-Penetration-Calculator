
import BigWorld
import math
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from AvatarInputHandler.gun_marker_ctrl import _CrosshairShotResults
from debug_utils import LOG_WARNING



# Helper to find mangled or renamed functions
def get_method_safely(cls, base_name):
    # Try the mangled version first
    mangled = "_%s__%s" % (cls.__name__, base_name)
    if hasattr(cls, mangled):
        return mangled
    # Try the protected version (single underscore)
    protected = "_%s" % base_name
    if hasattr(cls, protected):
        return protected
    # Try the public version
    if hasattr(cls, base_name):
        return base_name
    return None


LOG_WARNING("pademinune ARMOR PEN MOD LOADING STARTED")

# 1. Hook the Crosshair Color Update
# This triggers every time the crosshair moves or a target changes
func_name = get_method_safely(plugins.ShotResultIndicatorPlugin, "updateColor")
# _orig_updateColor = plugins.ShotResultIndicatorPlugin._ShotResultIndicatorPlugin__updateColor
_orig_updateColor = getattr(plugins.ShotResultIndicatorPlugin, func_name)

def _my_updateColor(self, markerType, position, collision, direction):
    # Call original game function first
    _orig_updateColor(self, markerType, position, collision, direction)

    # 2. Safety Check: Are we looking at a valid Vehicle?
    # collision[1] is the target entity (from plugins.py logic)
    if collision is not None and hasattr(collision[1], 'getMatinfo'):
        target = collision[1]
        player = BigWorld.player()
        
        # 3. Get Player's Shell Data
        vDesc = player.vehicleTypeDescriptor
        shell = vDesc.shot.shell
        ppDesc = vDesc.shot.piercingPower
        maxDist = vDesc.shot.maxDistance
        
        # 4. Get Current Average Penetration (Adjusted for distance)
        # hitPoint is collision[0]
        hitPoint = collision[0]
        dist = (hitPoint - player.getOwnVehiclePosition()).length
        
        # We use the game's internal function from gun_marker_ctrl.py
        avg_pen = _CrosshairShotResults._computePiercingPowerAtDist(ppDesc, dist, maxDist, 1.0)

        # 5. Get the Exact Armor Plate under the crosshair
        # We use collideSegmentExt from Vehicle.py line 1201
        # Start at gun position, end 500m away in aiming direction
        details = target.collideSegmentExt(position, position + direction * 500.0)
        
        if details:
            # We look at the first plate hit (details[0])
            first_hit = details[0]
            matInfo = first_hit.matInfo # From Vehicle.py line 1213
            
            if matInfo and matInfo.armor > 0:
                # 6. CALCULATE EFFECTIVE ARMOR (The PMOD Math)
                # We use the game's internal logic for normalization/angles
                # from gun_marker_ctrl.py line 163
                reduced_armor = _CrosshairShotResults._computePenetrationArmor(
                    shell, 
                    first_hit.hitAngleCos, 
                    matInfo
                )
                
                # 7. CALCULATE PROBABILITY (+/- 25% RNG)
                min_pen = avg_pen * 0.75
                max_pen = avg_pen * 1.25
                
                if reduced_armor >= max_pen:
                    prob = 0
                elif reduced_armor <= min_pen:
                    prob = 100
                else:
                    prob = ((max_pen - reduced_armor) / (max_pen - min_pen)) * 100

                # 8. OUTPUT TO LOG
                # This proves the mod is working!
                LOG_WARNING("[pademinune ARMOR PEN] Target: " + str(target.typeDescriptor.type.userString) + " | Reduced: " + str(reduced_armor) + "mm | Prob: " + str(prob) + "%")


# Apply the Hook
# plugins.ShotResultIndicatorPlugin._ShotResultIndicatorPlugin__updateColor = _my_updateColor
setattr(plugins.ShotResultIndicatorPlugin, func_name, _my_updateColor)

LOG_WARNING("pademinune ARMOR PEN MOD LOADING FINISHED")
