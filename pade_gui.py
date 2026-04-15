
from pade_constants import Colors, ArmorLabel, PenLabel
from gambiter import g_guiFlash # type: ignore
from gambiter.flash import COMPONENT_TYPE, COMPONENT_ALIGN # type: ignore

ARMOR_ALIAS = 'pademinune_ArmorPenLabel'
PROB_ALIAS = 'pademinune_ProbabilityLabel'
TRACK_ALIAS = 'pademinune_TrackLabel'

class GuiState:
    is_visible = False
    track_visible = False

def log(message):
    print("pademinune's Gui: " + str(message))

def update_armor_label(armor_value, color):
    interior_label = ArmorLabel.LABEL_FORMAT.format(armor=armor_value)
    new_text = "<font size='{font_size}' color='#{color}' face='$FieldFont'>{label_format}</font>".format(font_size=ArmorLabel.FONT_SIZE,
                                                                                                          color=color,
                                                                                                          label_format=interior_label)
    
    armor_changes = {'text': new_text, 'visible': True}

    if not GuiState.is_visible:
        GuiState.is_visible = True

    g_guiFlash.updateComponent(ARMOR_ALIAS, armor_changes)

def update_prob_label(prob, color):
    interior_label = PenLabel.LABEL_FORMAT.format(prob=prob)
    new_text = "<font size='{font_size}' color='#{color}' face='$FieldFont'>{label_format}</font>".format(font_size=PenLabel.FONT_SIZE,
                                                                                                          color=color,
                                                                                                          label_format=interior_label)

    prob_changes = {'text': new_text, 'visible': True}

    if not GuiState.is_visible:
        GuiState.is_visible = True
    
    g_guiFlash.updateComponent(PROB_ALIAS, prob_changes)

def show_track_label():
    if not GuiState.track_visible:
        track_changes = {'visible': True}
        g_guiFlash.updateComponent(TRACK_ALIAS, track_changes)
        GuiState.track_visible = True


def hide_track_label():
    if GuiState.track_visible:
        track_changes = {'visible': False}
        g_guiFlash.updateComponent(TRACK_ALIAS, track_changes)
        GuiState.track_visible = False

def hide_labels():
    if GuiState.is_visible:
        armor_changes = {'visible': False}
        prob_changes = {'visible': False}
        g_guiFlash.updateComponent(ARMOR_ALIAS, armor_changes)
        g_guiFlash.updateComponent(PROB_ALIAS, prob_changes)
        GuiState.is_visible = False

    if GuiState.track_visible:
        hide_track_label()

def update_gui(armor_value, prob, ricochet, hit_body, hit_track):

    if hit_track and not GuiState.track_visible:
        show_track_label()
    elif not hit_track and GuiState.track_visible:
        hide_track_label()

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


log('Starting creation of armor and penetration gui components')


armor_label_properties = {
    'isHtml': True,
    'text': '',
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
    'x': ArmorLabel.X_OFFSET,
    'y': ArmorLabel.Y_OFFSET,
    'visible': False,
}

probability_label_properties = {
    'isHtml': True,
    'text': '',
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
    'x': PenLabel.X_OFFSET,
    'y': PenLabel.Y_OFFSET,
    'visible': False,
}

track_label_properties = {
    'image': 'img://gui/pademinune/crosshair-16-green.png',
    'alpha': 1,
    'x': 0,
    'y': 0,
    'alignX': COMPONENT_ALIGN.CENTER,
    'alignY': COMPONENT_ALIGN.CENTER,
    'visible': False,
}

component_type = COMPONENT_TYPE.LABEL

# create the armor value label
g_guiFlash.createComponent(ARMOR_ALIAS, component_type, armor_label_properties)
# create the probability label
g_guiFlash.createComponent(PROB_ALIAS, component_type, probability_label_properties)
# create the track label
g_guiFlash.createComponent(TRACK_ALIAS, COMPONENT_TYPE.IMAGE, track_label_properties)


log('GUI components have been created!')

