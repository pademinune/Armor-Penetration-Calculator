
import BigWorld
from debug_utils import LOG_WARNING
from AvatarInputHandler import gun_marker_ctrl

def log(message):
    LOG_WARNING("pademinune: " + str(message))

log("Mod is loading")

# 1. Use the MANGLED name
hook_target = "_ShotResultIndicatorPlugin__onGunMarkerStateChanged"
# _computePenetrationArmor

# 2. Save the original
orginal_function = gun_marker_ctrl._CrosshairShotResults._computePenetrationArmor

# 3. Your Wrapper
def my_function(cls, shell, hitAngleCos, matInfo):
    armor_value = orginal_function(shell, hitAngleCos, matInfo)
    # log("Armor is " + str(armor_value) + "mm")
    
    # --- GET SHELL PENETRATION ---
    player = BigWorld.player()
    v_desc = player.getVehicleDescriptor()
    
    # This is the average penetration of your currently selected shell (garage value)
    avg_pen = v_desc.shot.piercingPower[0]
    
    # --- CALCULATE PROBABILITY ---
    # WoT RNG is +/- 25% (0.75 to 1.25)
    min_pen = avg_pen * 0.75
    max_pen = avg_pen * 1.25
    
    if armor_value <= min_pen:
        prob = 100
    elif armor_value >= max_pen:
        prob = 0
    else:
        prob = ((max_pen - armor_value) / (max_pen - min_pen)) * 100
    
    log("Armor: %dmm | Pen: %dmm | Prob: %d%%" % (int(armor_value), int(avg_pen), int(prob)))

    return armor_value

# 4. Apply
gun_marker_ctrl._CrosshairShotResults._computePenetrationArmor = classmethod(my_function)

log("Mod has finished loading")
