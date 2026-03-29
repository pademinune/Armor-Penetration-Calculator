
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from debug_utils import LOG_WARNING

LOG_WARNING("pademinune: mod is loading")

# 1. Use the MANGLED name
hook_target = "_ShotResultIndicatorPlugin__onGunMarkerStateChanged"

# 2. Save the original
orig_onMarkerChanged = getattr(plugins.ShotResultIndicatorPlugin, hook_target)

# 3. Your Wrapper
def my_onMarkerChanged(self, markerType, gunMarkerState, supportMarkersInfo):
    # Let the game update the crosshair color first
    orig_onMarkerChanged(self, markerType, gunMarkerState, supportMarkersInfo)
    
    # NOW perform your armor math here using 'gunMarkerState.collData'
    # ... your math logic ...
    # ... update ArmorModData.display_text ...
    LOG_WARNING("pademinune: GAME IS NOW LOOKING AT SOMETHING")

# 4. Apply
setattr(plugins.ShotResultIndicatorPlugin, hook_target, my_onMarkerChanged)

LOG_WARNING("pademinune: mod has finished loading")
