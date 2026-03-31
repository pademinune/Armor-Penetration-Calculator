
import BigWorld
from debug_utils import LOG_WARNING
from AvatarInputHandler import gun_marker_ctrl
import math
import GUI


def log(message):
    LOG_WARNING("pademinune: " + str(message))


RED = (255, 0, 0, 255)
YELLOW = (255, 255, 0, 255)
GREEN = (0, 255, 0, 255)
GREY = (128, 128, 128, 255)

log("Mod is loading")

# Create a text component
label = GUI.Text("")
# label.font = "default_medium.font" # Or "default_medium.font"
# label.filterType = "LINEAR"
# label.horizontalAnchor = "CENTER"
# label.verticalAnchor = "CENTER"
# label.horizontalPositionMode = "SCREEN_RELATIVE"
# label.verticalPositionMode = "SCREEN_RELATIVE"


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
    
    text = "{}mm | {}%".format(int(armor_value), int(prob))
    color = GREY # catch all
    if prob == 100:
        color = GREEN
    elif 0 < prob < 100:
        color = YELLOW
    elif prob == 0:
        color = RED
    
    update_ui(text, color)

    return armor_value

# 4. Apply
gun_marker_ctrl._CrosshairShotResults._computePenetrationArmor = classmethod(my_function)

log("Mod has finished loading")
