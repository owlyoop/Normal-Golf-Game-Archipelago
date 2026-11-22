from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle, DefaultOnToggle


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

    default = option_iron

class StartingRegion(Choice):
    """The region the player has access to at the start of the game"""
    display_name = "Starting Region"

    option_front_yard = 1
    option_hole_1 = 4
    option_holes_2_to_5 = 5
    option_holes_6_to_9 = 6
    option_car_park = 0

    default = "random"

class NumberOfStartingDifficulties(Range):
    """How many class of bounty difficulties are unlocked at the start of the game."""
    display_name = "Number of Starting Difficulties"
    range_start = 1
    range_end = 8
    default = 4

class MarkImportantShopLocationsAsPriority(Toggle):
    """Flag the 5 clubs and the LMUGC ticket locations as priority locations so filler/trap items don't appear there"""
    display_name = "Flag important shop locations as priority locations"

class PuttingDrillBountiesRequirePutter(DefaultOnToggle):
    """Whether the 'Putting Drill' and the 'Pressure Drill' bounties should require the putter in logic"""
    display_name = "Require the putter for the 'Putting Drill' and 'Pressure Drill' bounties logic"

class GreatExplorerAllowPutterInLogic(Toggle):
    """Whether the 'Great Explorer' bounty should be considered in logic if the player's only club is a putter (Hole 2 fairway to Hole 5 MultiHit bounty). Easy but very tedious"""
    display_name = "Allow putter in logic for 'Great Explorer' bounty"

class PhysicsTrapDuration(Range):
    """How long in seconds physics traps last for"""
    range_start = 1
    range_end = 300
    default = 60
    display_name = "Physics traps duration (seconds)"

class GolfHoleChecks(DefaultOnToggle):
    """Enables getting the ball into golf holes as locations"""
    display_name = "Enable golf hole checks"

class GolfHoleChecksEnableMiniIslands(Toggle):
    """Enables the three mini islands golf holes. Does nothing if golf hole checks are disabled"""
    display_name = "Enable the mini island golf hole checks"

class GolfHoleChecksEnableSecretGreens(Toggle):
    """Enables the two secret green golf holes. Does nothing if golf hole checks are disabled. Warning: these are very hard to get"""
    display_name = "Enable the secret green golf hole checks"


class BreakableChecks(DefaultOnToggle):
    """Enable breaking destructible objects as locations"""
    display_name = "Enable breakable objects as checks"

class BreakableChecksEnableStatue(DefaultOnToggle):
    """Adds each breakable statue piece in the holes 2-5 area as a location for breakable checks.
    Does nothing if breakable checks re disabled"""
    display_name = "Breakable statue pieces are checks"

class BreakableStatuesFrontYardInLogic(Toggle):
    """Some of the statue block pieces can be hit from the front yard with a Driver, enabling this option adds that possibility in logic.
    Does nothing if breakable checks are disabled"""
    display_name = "Logic considers breaking statue blocks from front yard"


class AchievementChecks(DefaultOnToggle):
    """Enable some achievements as checks"""
    display_name = "Enable achievement checks"

class AchievementChecksEnableHoleInOne(Toggle):
    """Enable the hole-in-one achievement for achievement checks. Does nothing if achievement checks are disabled"""
    display_name = "Enable the hole-in-one achievement checks"

class AchievementChecksEnableHoleSixAlbatross(Toggle):
    """Enable the hole 6 albatross achievement for achievement checks. Does nothing if achievement checks is disabled"""
    display_name = "Enable the hole 6 albatross achievement check"


# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class APNormalGolfGameOptions(PerGameCommonOptions):
    req_bounties_to_win: RequiredBountiesToWin
    starting_club: StartingClub
    starting_region: StartingRegion
    num_starting_difficulties: NumberOfStartingDifficulties
    shop_locations_never_filler: MarkImportantShopLocationsAsPriority
    putting_drills_req_putter: PuttingDrillBountiesRequirePutter
    great_explorer_allow_putter_logic: GreatExplorerAllowPutterInLogic
    physics_traps_duration: PhysicsTrapDuration
    hole_checks_enabled: GolfHoleChecks
    hole_checks_enable_mini_island_holes: GolfHoleChecksEnableMiniIslands
    hole_checks_enable_secret_greens: GolfHoleChecksEnableSecretGreens
    breakable_checks_enabled: BreakableChecks
    breakable_checks_statues_enabled: BreakableChecksEnableStatue
    breakable_checks_statues_frontyard: BreakableStatuesFrontYardInLogic
    achievement_checks_enabled: AchievementChecks
    achievement_checks_hole_in_one_enabled: AchievementChecksEnableHoleInOne
    achievement_checks_albatross_hole6_enabled: AchievementChecksEnableHoleSixAlbatross


# Group logic/trick options together, especially for the local WebHost.
normalgolfgame_options_groups = [
    OptionGroup(
        "Game Progression",
        [
            RequiredBountiesToWin,
            StartingClub,
            StartingRegion,
            NumberOfStartingDifficulties,
            PuttingDrillBountiesRequirePutter,
            GreatExplorerAllowPutterInLogic,
            MarkImportantShopLocationsAsPriority
        ]
    ),
    OptionGroup(
        "Golf Hole Options",
        [
            GolfHoleChecks,
            GolfHoleChecksEnableMiniIslands,
            GolfHoleChecksEnableSecretGreens
        ]
    ),
    OptionGroup(
        "Breakable Options",
        [
            BreakableChecks,
            BreakableChecksEnableStatue,
            BreakableStatuesFrontYardInLogic
        ]
    ),
    OptionGroup(
        "Achievement Options",
        [
            AchievementChecks,
            AchievementChecksEnableHoleInOne,
            AchievementChecksEnableHoleSixAlbatross
        ]
    ),
]