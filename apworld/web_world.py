from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld


# For our game to display correctly on the website, we need to define a WebWorld subclass.
class APNormalGolfGameWebWorld(WebWorld):
    game = "Normal Golf Game"

    theme = "grassFlowers"

    '''setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Normal Golf Game for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["owlyoop"],
    )'''

    # We add these tutorials to our WebWorld by overriding the "tutorials" field.
    #tutorials = [setup_en]

    # If we have option groups and/or option presets, we need to specify these here as well.
    #option_groups = option_groups
    #options_presets = option_presets
