
import BigWorld # type: ignore
import game # type: ignore
import Keys # type: ignore
from gui.modsSettingsApi import g_modsSettingsApi, templates # type: ignore

from pade_constants import ArmorLabel, PenLabel, Colors
from pade_config import save_flat_config
from pade_gui import update_label_properties

mod_linkage = 'pade_armor_calculator'
modDataVersion = 1

template = {
    'modDisplayName': "pademinune's Armor Calculator",
    'enabled': True,
    'column1': [
        templates.createLabel('<b>— Armor Label —</b>'),
        templates.createSlider('Armor Label Font Size', 'armor_label_font_size',
                               ArmorLabel.FONT_SIZE, 5, 100, 1,
                               format='{{value}}px',
                               tooltip='{HEADER}Armor Label Font Size{/HEADER}{BODY}The size in pixels of the Armor Label.{/BODY}'),
        templates.createNumericStepper('Armor Label Horizontal Offset', 'armor_label_x_offset',
                                       ArmorLabel.X_OFFSET, -2000, 2000, 1,
                                       manual=True,
                                       tooltip="{HEADER}Armor Label Horizontal Offset{/HEADER}{BODY}The armor label's horizontal offset from the center of the screen. Positive values move it to the right.{/BODY}"),
        templates.createNumericStepper('Armor Label Vertical Offset', 'armor_label_y_offset',
                                       ArmorLabel.Y_OFFSET, -2000, 2000, 1,
                                       manual=True,
                                       tooltip="{HEADER}Armor Label Vertical Offset{/HEADER}{BODY}The armor label's vertical offset from the center of the screen. Positive values move it down.{/BODY}"),
        templates.createInput('Armor Label Format', 'armor_label_format',
                              ArmorLabel.LABEL_FORMAT,
                              tooltip="{HEADER}Armor Label Format{/HEADER}{BODY}The display format of the armor label. '{armor}' will be replaced with the armor value.{/BODY}"),
        templates.createEmpty(10),
        templates.createLabel('<b>— Probability Label —</b>'),
        templates.createSlider('Pen Label Font Size', 'pen_label_font_size',
                               PenLabel.FONT_SIZE, 5, 100, 1,
                               format='{{value}}px',
                               tooltip='{HEADER}Pen Label Font Size{/HEADER}{BODY}The size in pixels of the Penetration Label.{/BODY}'),
        templates.createNumericStepper('Pen Label Horizontal Offset', 'pen_label_x_offset',
                                       PenLabel.X_OFFSET, -2000, 2000, 1,
                                       manual=True,
                                       tooltip="{HEADER}Pen Label Horizontal Offset{/HEADER}{BODY}The penetration label's horizontal offset from the center of the screen. Positive values move it to the right.{/BODY}"),
        templates.createNumericStepper('Pen Label Vertical Offset', 'pen_label_y_offset',
                                       PenLabel.Y_OFFSET, -2000, 2000, 1,
                                       manual=True,
                                       tooltip="{HEADER}Pen Label Vertical Offset{/HEADER}{BODY}The penetration label's vertical offset from the center of the screen. Positive values move it down.{/BODY}"),
        templates.createInput('Pen Label Format', 'pen_label_format',
                              PenLabel.LABEL_FORMAT,
                              tooltip="{HEADER}Pen Label Format{/HEADER}{BODY}The display format of the penetration label. '{prob}' will be replaced with the penetration probability.{/BODY}"),
    ],
    'column2': [
        templates.createLabel('<b>— Colors —</b>'),
        templates.createColorChoice('High Pen Chance', 'color_green',
                                    Colors.GREEN,
                                    tooltip='{HEADER}High Pen Chance Color{/HEADER}{BODY}Color shown when penetration probability is high (>93%).{/BODY}'),
        templates.createColorChoice('Medium Pen Chance', 'color_orange',
                                    Colors.ORANGE,
                                    tooltip='{HEADER}Medium Pen Chance Color{/HEADER}{BODY}Color shown when penetration probability is medium.{/BODY}'),
        templates.createColorChoice('Low Pen Chance', 'color_red',
                                    Colors.RED,
                                    tooltip='{HEADER}Low Pen Chance Color{/HEADER}{BODY}Color shown when penetration probability is low (<7%).{/BODY}'),
        templates.createColorChoice('Ricochet', 'color_ricochet',
                                    Colors.PURPLE,
                                    tooltip='{HEADER}Ricochet Color{/HEADER}{BODY}Color shown when the shell will ricochet.{/BODY}'),
    ]
}

def on_settings_save(linkage, new_settings):
    if linkage == mod_linkage:
        ArmorLabel.FONT_SIZE = new_settings['armor_label_font_size']
        ArmorLabel.X_OFFSET = new_settings['armor_label_x_offset']
        ArmorLabel.Y_OFFSET = new_settings['armor_label_y_offset']
        ArmorLabel.LABEL_FORMAT = new_settings['armor_label_format']
        PenLabel.FONT_SIZE = new_settings['pen_label_font_size']
        PenLabel.X_OFFSET = new_settings['pen_label_x_offset']
        PenLabel.Y_OFFSET = new_settings['pen_label_y_offset']
        PenLabel.LABEL_FORMAT = new_settings['pen_label_format']
        Colors.GREEN = new_settings['color_green']
        Colors.ORANGE = new_settings['color_orange']
        Colors.RED = new_settings['color_red']
        Colors.PURPLE = new_settings['color_ricochet']

    save_flat_config(new_settings)
    update_label_properties()


g_modsSettingsApi.setModTemplate(mod_linkage, template, on_settings_save, None)

