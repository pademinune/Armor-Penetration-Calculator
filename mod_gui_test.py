
import math
import GUI
from debug_utils import LOG_WARNING


def log(message):
    LOG_WARNING("pademinune: " + str(message))

log("Mod is loading")

# Create a text component
label = GUI.Text("")
label.font = "system_medium" # Or "default_medium.font"
label.filterType = "LINEAR"
label.horizontalAnchor = "CENTER"
label.verticalAnchor = "CENTER"
label.horizontalPositionMode = "SCREEN_RELATIVE"
label.verticalPositionMode = "SCREEN_RELATIVE"
label.position = (0, -0.1, 0.5) # Center of screen, slightly below crosshair
label.visible = False
GUI.addRoot(label)

label.text = "THIS IS THE LABEL"
label.colour = (255, 0, 0, 255)
label.visible = True

log("Mod has finished loading")

