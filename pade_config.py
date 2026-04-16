
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
        "y_offset": 55,
        "font_size": 18,
        "label_format": "{prob}%",
    },
    "colors": {
        "green_chance": "B6FF00",
        "orange_chance": "FFAD00",
        "red_chance": "FF2717",
        "ricochet": "800080",
    },
    'track_label': {
        'enabled': True,
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


if not os.path.isfile(CONFIG_PATH):
    create_config()

try:
    user_settings = read_config()
except:
    # if the config is invalid, reset it
    create_config()
    user_settings = read_config()

