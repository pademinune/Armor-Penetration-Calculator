from pade_config import user_settings, DEFAULT_CONFIG


def safe_get_color(color):
    default = DEFAULT_CONFIG.get("colors", "808080").get(color, "808080")
    return user_settings.get("colors", default).get(color, default)


def safe_get_setting(label, attribute):
    default = DEFAULT_CONFIG[label][attribute]
    return user_settings.get(label, default).get(attribute, default)


class Colors:
    RED = safe_get_color("red_chance")
    YELLOW = "FFFF00"
    ORANGE = safe_get_color("orange_chance")
    GREEN = safe_get_color("green_chance")
    GREY = "808080"
    PURPLE = safe_get_color("ricochet")


class ArmorLabel:
    LABEL_FORMAT = safe_get_setting("armor_label", "label_format")
    FONT_SIZE = safe_get_setting("armor_label", "font_size")
    X_OFFSET = safe_get_setting("armor_label", "x_offset")
    Y_OFFSET = safe_get_setting("armor_label", "y_offset")


class PenLabel:
    LABEL_FORMAT = safe_get_setting("pen_label", "label_format")
    FONT_SIZE = safe_get_setting("pen_label", "font_size")
    X_OFFSET = safe_get_setting("pen_label", "x_offset")
    Y_OFFSET = safe_get_setting("pen_label", "y_offset")
