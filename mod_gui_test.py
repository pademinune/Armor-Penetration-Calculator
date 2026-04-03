
from gambiter import g_guiFlash
from gambiter.flash import COMPONENT_TYPE, COMPONENT_ALIGN

def log(message):
    print("pademinune's GuiTest mod: " + str(message))

log("GUIFlash Test Mod is loading")


armor_value_properties = {
    'text': "<font size='25' color='#6BF40D' face='$FieldFont'>150mm</font>",
    'multiline': True,
    'glowfilter': {
        'color': 0x000000,   # Black
        'alpha': 1,          # Solid
        'blurX': 3,          # Glow width
        'blurY': 3,          # Glow height
        'strength': 10,      # Higher = sharper outline
        'quality': 2
    },
    'alignX': COMPONENT_ALIGN.CENTER,
    'alignY': COMPONENT_ALIGN.CENTER,
    'x': 0,
    'y': 30,
}

probability_properties = {
    'text': "<font size='25' color='#6BF40D' face='$FieldFont'>100%</font>",
    'multiline': True,
    'glowfilter': {
        'color': 0x000000,   # Black
        'alpha': 1,          # Solid
        'blurX': 3,          # Glow width
        'blurY': 3,          # Glow height
        'strength': 10,      # Higher = sharper outline
        'quality': 2
    },
    'alignX': COMPONENT_ALIGN.CENTER,
    'alignY': COMPONENT_ALIGN.CENTER,
    'x': 0,
    'y': 60,
}


alias = "pademinune_ArmorPenLabel"
component_type = COMPONENT_TYPE.LABEL

# create the armor value label
g_guiFlash.createComponent(alias, component_type, armor_value_properties)
# create the probability label
g_guiFlash.createComponent("pademinune_probabilityLabel", component_type, probability_properties)

log("GUIFlash Test Mod has finished loading")

