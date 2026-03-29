
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from debug_utils import LOG_WARNING

def log(message):
    LOG_WARNING("pademinune: " + str(message))

log("Mod is loading")

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
    try:
        # Only log if we are in Sniper Mode (markerType 2) to keep the log clean
        # markerType 1 = Arcade, 2 = Sniper, 3 = Arty
        if markerType == 2:
            log("In sniper mode")
            # --- DISCOVERY 1: Basic marker info ---
            pos = getattr(gunMarkerState, 'position', 'N/A')
            log("[MOD DEBUG] Pos: %s" % str(pos))

            # --- DISCOVERY 2: Collision Data ---
            # This is the most important part for your mod
            collData = getattr(gunMarkerState, 'collData', None)
            
            if collData is not None:
                # Get the target entity name
                target_name = "None"
                if hasattr(collData, 'entity') and collData.entity:
                    # Some versions use 'typeDescriptor', some use 'publicInfo'
                    if hasattr(collData.entity, 'typeDescriptor'):
                        target_name = collData.entity.typeDescriptor.type.userString

                # Get the raw armor values WG is seeing
                armor = getattr(collData, 'armor', 'N/A')
                angleCos = getattr(collData, 'hitAngleCos', 'N/A')

                log("[MOD DEBUG] TARGET: %s | ARMOR: %s | ANGLE_COS: %s" % (target_name, armor, angleCos))
            else:
                # If this prints while aiming at a tank, your game settings have 
                # "Armor Penetration Indicator" disabled!
                log("[MOD DEBUG] No collision data detected.")

    except Exception as e:
        log("[MOD DEBUG] ERROR in hook: %s" % str(e))


# 4. Apply
setattr(plugins.ShotResultIndicatorPlugin, hook_target, my_onMarkerChanged)

log("Mod has finished loading")
