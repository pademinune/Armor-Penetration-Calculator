
from colors import Colors
from gambiter import g_guiFlash
from gambiter.flash import COMPONENT_TYPE, COMPONENT_ALIGN


ARMOR_ALIAS = "pademinune_ArmorPenLabel"
PROB_ALIAS = "pademinune_ProbabilityLabel"

def log(message):
    print("pademinune's GuiTest mod: " + str(message))

def update_armor_label(armor_value, color):
    armor_changes = {
        'text': "<font size='25' color='#{}' face='$FieldFont'>{}mm</font>".format(color, armor_value),
        "visible": True,
    }
    g_guiFlash.updateComponent(ARMOR_ALIAS, armor_changes)

def update_prob_label(prob, color):
    prob_changes = {
        'text': "<font size='25' color='#{}' face='$FieldFont'>{}%</font>".format(color, prob),
        "visible": True,
    }
    g_guiFlash.updateComponent(PROB_ALIAS, prob_changes)

def hide_labels():
    armor_changes = {"visible": False}
    prob_changes = {"visible": False}
    g_guiFlash.updateComponent(ARMOR_ALIAS, armor_changes)
    g_guiFlash.updateComponent(PROB_ALIAS, prob_changes)

def update_gui(armor_value, prob, ricochet, hit_body):

    if ricochet:
        # shell ricochet
        color = Colors.PURPLE
        update_armor_label("-", color)
        update_prob_label(0, color)
        return
    
    if not hit_body:
        # shell only hits spaced armor or tracks
        color = Colors.RED
        update_armor_label("-", color)
        update_prob_label(0, color)
        return
    
    color = Colors.GREY
    if prob <= 7:
        # armor_val is right of z = 1.5
        color = Colors.RED
    elif prob >= 93:
        # armor_val is left of z = -1.5
        color = Colors.GREEN
    else:
        color = Colors.ORANGE
    
    update_armor_label(int(armor_value), color)
    update_prob_label(int(prob), color)


log("Starting creation of armor and penetration gui components")


armor_label_properties = {
    'isHtml': True,
    'text': "<font size='25' color='#6BF40D' face='$FieldFont'>150mm</font>",
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
    "visible": False,
}

probability_label_properties = {
    'isHtml': True,
    'text': "<font size='25' color='#6BF40D' face='$FieldFont'>100%</font>",
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
    "visible": False,
}


component_type = COMPONENT_TYPE.LABEL

# create the armor value label
g_guiFlash.createComponent(ARMOR_ALIAS, component_type, armor_label_properties)
# create the probability label
g_guiFlash.createComponent(PROB_ALIAS, component_type, probability_label_properties)

log("GUI components have been created!")

