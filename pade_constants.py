
from pade_config import user_settings


class Colors:
    # RED = "E90000"
    # YELLOW = "FFFF00"
    # ORANGE = "FFAD00"
    # GREEN = "6BF40D"
    # GREY = "808080"
    # PURPLE = "800080"
    RED = user_settings["colors"]["red_chance"]
    YELLOW = "FFFF00"
    ORANGE = user_settings["colors"]["orange_chance"]
    GREEN = user_settings["colors"]["green_chance"]
    GREY = "808080"
    PURPLE = user_settings["colors"]["ricochet"]

class ArmorLabel:
    LABEL_FORMAT = user_settings["armor_label"]["label_format"]
    FONT_SIZE = user_settings["armor_label"]["font_size"]
    X_OFFSET = user_settings["armor_label"]["x_offset"]
    Y_OFFSET = user_settings["armor_label"]["y_offset"]

class PenLabel:
    LABEL_FORMAT = user_settings["pen_label"]["label_format"]
    FONT_SIZE = user_settings["pen_label"]["font_size"]
    X_OFFSET = user_settings["pen_label"]["x_offset"]
    Y_OFFSET = user_settings["pen_label"]["y_offset"]

