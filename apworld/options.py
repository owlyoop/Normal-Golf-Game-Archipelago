from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md

class RequiredBountiesToWin(Range):
    """Number of bounty items needed to complete the game"""
    display_name = "Required Bounties to Win"
    range_start = 1
    range_end = 105
    default = 50

class StartingClub(Choice):
    """The club the player starts with"""
    display_name = "Starting Club"

    option_putter = 0
    option_wedge = 1
    option_iron = 2
    option_hybrid = 3
    option_driver = 4

    default = option_hybrid

class StartingRegion(Choice):
    """The region the player has access to at the start of the game"""
    display_name = "Starting Region"

    option_front_yard = 1
    option_hole_1 = 4
    option_holes_2_to_5 = 5
    option_holes_6_to_9 = 6
    option_car_park = 0

    default = "random"

'''class StartingDifficulty(Choice):
    """The class of bounty difficulty that will be available at the start of the game"""
    display_name = "Starting Bounty Difficulty"

    option_super_easy = 0
    option_easy = 1
    option_manageable = 2
    option_intermediate = 3
    option_difficult = 4
    option_very_hard = 5
    option_nightmare = 6
    option_diabolical = 7
    option_impossible = 8

    default = option_manageable'''

class NumberOfStartingDifficulties(Range):
    """How many class of bounty difficulties are unlocked at the start of the game."""
    display_name = "Number of Starting Difficulties"
    range_start = 1
    range_end = 8
    default = 4



# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class APNormalGolfGameOptions(PerGameCommonOptions):
    req_bounties_to_win: RequiredBountiesToWin
    starting_club: StartingClub
    starting_region: StartingRegion
    num_starting_difficulties: NumberOfStartingDifficulties


