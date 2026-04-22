
import json
import os


DEFAULT_CONFIG = {
    "armor_label": {
        "x_offset": 0,
        "y_offset": 30,
        "font_size": 20,
        "label_format": "{armor}",
    },
    "pen_label": {
        "x_offset": 0,
        "y_offset": 50,
        "font_size": 16,
        "label_format": "{prob}%",
    },
    "colors": {
        "green_chance": "B6FF00",
        "orange_chance": "FFAD00",
        "red_chance": "FF2717",
        "ricochet": "800080",
    },
}

CONFIG_FOLDER = os.path.join('mods', 'configs', 'pademinune')
CONFIG_PATH = os.path.join(CONFIG_FOLDER, 'armor-calculator.json')


def create_config():
    if not os.path.exists(CONFIG_FOLDER):
        os.makedirs(CONFIG_FOLDER)

    with open(CONFIG_PATH, 'w') as file:
        json.dump(DEFAULT_CONFIG, file, indent=4)

def read_config():
    with open(CONFIG_PATH) as file:
        user_config = json.load(file)
    
    return user_config

def save_flat_config(settings):
    config = {
        "armor_label": {
            "x_offset": settings['armor_label_x_offset'],
            "y_offset": settings['armor_label_y_offset'],
            "font_size": settings['armor_label_font_size'],
            "label_format": settings['armor_label_format'],
        },
        "pen_label": {
            "x_offset": settings['pen_label_x_offset'],
            "y_offset": settings['pen_label_y_offset'],
            "font_size": settings['pen_label_font_size'],
            "label_format": settings['pen_label_format'],
        },
        "colors": {
            "green_chance": settings['color_green'],
            "orange_chance": settings['color_orange'],
            "red_chance": settings['color_red'],
            "ricochet": settings['color_ricochet'],
        },
    }

    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)


if not os.path.isfile(CONFIG_PATH):
    create_config()

try:
    user_settings = read_config()
except:
    # if the config is invalid, reset it
    create_config()
    user_settings = read_config()

