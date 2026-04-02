
import math
import GUI
from debug_utils import LOG_WARNING


def log(message):
    LOG_WARNING("pademinune: " + str(message))

log("Mod is loading")

# Create a text component
label = GUI.Text("")
label.position = (0, -0.1, 0.5) # Center of screen, slightly below crosshair
label.visible = False
GUI.addRoot(label)

label.text = "THIS IS THE LABEL"
label.colour = (255, 0, 0, 255)
label.visible = True

log("Mod has finished loading")

