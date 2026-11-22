from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState, ItemClassification
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule
from .game_data import bounty_data, GolfClubs, shop_data, Difficulty, Breakable, breakable_signs_data, golfhole_data, \
    achievement_data, HoleRequirement, ParFeedback, golfholes_mini_islands, golfholes_secret_green, \
    breakable_statue_data
from worlds.generic.Rules import add_rule, set_rule, add_item_rule
from .items import BOUNTY_COMPLETE
from .locations import bounty_complete_event_name
from .regions import Regions

if TYPE_CHECKING:
    from .world import APNormalGolfWorld

def set_all_rules(world: APNormalGolfWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_location_rules(world)
    if world.options.breakable_checks_enabled:
        set_breakable_rules(world)
    if world.options.achievement_checks_enabled:
        set_achievement_rules(world)
    set_completion_condition(world)

def set_all_location_rules(world: APNormalGolfWorld) -> None:

    def club_rule(min_club: int):
        allowed = [club.name for club in GolfClubs if club >= min_club]
        return lambda state: state.has_any(allowed, world.player)

    def difficulty_unlock_rule(difficulty: Difficulty):
        return lambda state: state.has("Unlock " + difficulty.name + " bounties", world.player)

    def hole2parplus_club_rule():
        allowed = [GolfClubs.Wedge.name, GolfClubs.Iron.name]
        return lambda state: state.has_any(allowed, world.player)

    def crag_gong_club_rule():
        required = [GolfClubs.Driver.name, GolfClubs.Iron.name]
        return lambda state: state.has_all(required, world.player)

    def putter_rule():
        return lambda state: state.has("Putter", world.player)

    #Hole 1 bountys & My First Multihit start in FrontYard but end in Hole 1 Area
    def additional_region_rule_both(region: str):
        return lambda state: state.can_reach_region(region, world.player)

    def additional_region_rule_either(region1: str, region2: str):
        return lambda state: state.can_reach_region(region1, world.player) or state.can_reach_region(region2, world.player)

    #Bounty rules
    for name, bounty in bounty_data.items():

        #Club rule exceptions
        if name == "Hole 2 - Par Plus":
            add_rule(world.get_location(name), hole2parplus_club_rule())
            add_rule(world.get_location(bounty_complete_event_name(name)), hole2parplus_club_rule())
        elif name == "Crag Gong":
            add_rule(world.get_location(name), crag_gong_club_rule())
            add_rule(world.get_location(bounty_complete_event_name(name)), crag_gong_club_rule())
        elif name == "Putting Drill" or name == "Pressure Drill":
            if world.options.putting_drills_req_putter:
                add_rule(world.get_location(name), putter_rule())
                add_rule(world.get_location(bounty_complete_event_name(name)), putter_rule())
            add_rule(world.get_location(name), club_rule(bounty["smallest_club_req"]))
            add_rule(world.get_location(bounty_complete_event_name(name)), club_rule(bounty["smallest_club_req"]))
        else:
            add_rule(world.get_location(name), club_rule(bounty["smallest_club_req"]))
            add_rule(world.get_location(bounty_complete_event_name(name)), club_rule(bounty["smallest_club_req"]))



        add_rule(world.get_location(name), difficulty_unlock_rule(bounty["difficulty"]))
        add_rule(world.get_location(bounty_complete_event_name(name)), difficulty_unlock_rule(bounty["difficulty"]))

        #Location rule exceptions
        if name == "My First Multi Hit" or name == "Hole 1 - Par" or name == "Hole 1 - Birdie" or name == "Hole 1 - Par Plus":
            add_rule(world.get_location(name), additional_region_rule_both("Hole 1 Area"))
            add_rule(world.get_location(bounty_complete_event_name(name)), additional_region_rule_both("Hole 1 Area"))

    #This stray cash can be collected from either side of the picket fence
    add_rule(world.get_location("Stray Cash (driveway picket fence)"), additional_region_rule_either(Regions.Holes_6_to_9, Regions.Holes_2_to_5))

    def shop_rule(price: int):
        return lambda state: state.has("golf_money", world.player, price)

    for name, item in shop_data.items():
        set_rule(world.get_location(name), shop_rule(item["cost"]))
        if world.options.shop_locations_never_filler:
            if (name == "Pro Shop Buy Putter" or
                    name == "Pro Shop Buy Wedge" or
                    name == "Pro Shop Buy Iron" or
                    name == "Pro Shop Buy Hybrid" or
                    name == "Pro Shop Buy Driver" or
                    name == "Pro Shop Buy LMUGC Ticket"):
                world.options.priority_locations.value.add(name)

    if world.options.hole_checks_enabled:
        for name, golfhole in golfhole_data.items():
            if (name == "No Cheese Chip Short Hole"
                or name == "No Cheese Chip Middle Hole"
                or name == "No Cheese Chip Tall Hole"):
                add_rule(world.get_location(name), club_rule(2))

    if world.options.hole_checks_enable_mini_island_holes:
        for name, golfhole in golfholes_mini_islands.items():
            add_rule(world.get_location(name), club_rule(2))

    if world.options.hole_checks_enable_secret_greens:
        for name, golfhole in golfholes_secret_green.items():
            if name == "Secret green hole #1":
                add_rule(world.get_location(name), club_rule(2))
                add_rule(world.get_location(name), additional_region_rule_either(Regions.Holes_6_to_9, Regions.Holes_2_to_5))
            elif name == "Secret green hole #2":
                add_rule(world.get_location(name), club_rule(3))

def set_breakable_rules(world: APNormalGolfWorld) -> None:
    def breakable_rule(region_club_dict):
        pairs = []  # club-region pairs
        for min_club, regions in region_club_dict.items():
            club_names = [club.name for club in GolfClubs if club >= min_club]
            pairs.append((club_names, list(regions)))

        # rule should return true if the player has any of the club-region combos
        def rule(state) -> bool:
            for club_names, regions in pairs:
                if not state.has_any(club_names, world.player):
                    return False
                for region in regions:
                    if state.can_reach_region(region, world.player):
                        return True
            return False
        return rule

    for name, sign in breakable_signs_data.items():
        set_rule(world.get_location(name), breakable_rule(sign["region_club_dict"]))

    if world.options.breakable_checks_statues_enabled:
        if world.options.breakable_checks_statues_frontyard:
            for name, statue in breakable_statue_data.items():
                statue["region_club_dict"][GolfClubs.Driver].append(Regions.FrontYard)
        for name, statue in breakable_statue_data.items():
            set_rule(world.get_location(name), breakable_rule(statue["region_club_dict"]))

def set_achievement_rules(world: APNormalGolfWorld) -> None:

    def hole_in_one_rule(state) -> bool:
        if (state.can_reach_region(Regions.FrontYard, world.player) and state.has("Iron", world.player) and
                (state.has("Unlock INTERMEDIATE bounties", world.player)
                 or state.has("Unlock DIFFICULT bounties", world.player)
                 or state.has("Unlock VERY HARD bounties", world.player))): return True

        if (state.can_reach_region(Regions.Holes_2_to_5, world.player) and state.has("Wedge", world.player) and
                (state.has("Unlock INTERMEDIATE bounties", world.player)
                 or state.has("Unlock VERY_HARD bounties", world.player))): return True

        if (state.can_reach_region(Regions.Holes_2_to_5, world.player) and state.has("Iron", world.player) and
                (state.has("Unlock INTERMEDIATE bounties", world.player)
                 or state.has("Unlock VERY_HARD bounties", world.player)
                 or state.has("Unlock DIFFICULT bounties", world.player))): return True

        if (state.can_reach_region(Regions.Holes_2_to_5, world.player) and state.has("Iron", world.player) and
                (state.has("Unlock INTERMEDIATE bounties", world.player)
                 or state.has("Unlock VERY_HARD bounties", world.player)
                 or state.has("Unlock DIFFICULT bounties", world.player)
                 or state.has("Unlock MANAGEABLE bounties", world.player))): return True

        if (state.can_reach_region(Regions.Holes_6_to_9, world.player)
                and ( state.has("Iron", world.player) or state.has("Hybrid", world.player) or state.has("Driver", world.player) )
                and (state.has("Unlock INTERMEDIATE bounties", world.player)
                     or state.has("Unlock VERY_HARD bounties", world.player)
                     or state.has("Unlock DIFFICULT bounties", world.player))): return True
        return False

    def eagle_rule(state) -> bool:
        if (state.can_reach_region(Regions.Holes_2_to_5, world.player) and state.has("Iron", world.player) and
                (state.has("Unlock INTERMEDIATE bounties", world.player)
                 or state.has("Unlock DIFFICULT bounties", world.player))): return True

        if ( (state.can_reach_region(Regions.Holes_2_to_5, world.player) or state.can_reach_region(Regions.Holes_6_to_9, world.player) )
                and state.has("Driver", world.player) and
                (state.has("Unlock INTERMEDIATE bounties", world.player)
                 or state.has("Unlock DIFFICULT bounties", world.player)
                 or state.has("Unlock VERY_HARD bounties", world.player))): return True

        if (state.can_reach_region(Regions.Holes_6_to_9, world.player)
                and ( state.has("Iron", world.player) or state.has("Hybrid", world.player) ) and
                (state.has("Unlock INTERMEDIATE bounties", world.player)
                 or state.has("Unlock DIFFICULT bounties", world.player) )): return True
        return False

    def birdie_rule(state) -> bool:
        if world.get_location("Hole 1 - Par").can_reach(state) and state.can_reach_region(Regions.Hole_1_Area, world.player): return True
        if world.get_location("Hole 1 - Birdie").can_reach(state) and state.can_reach_region(Regions.Hole_1_Area, world.player): return True
        if world.get_location("Hole 1 - Par Plus").can_reach(state) and state.can_reach_region(Regions.Hole_1_Area, world.player): return True

        if world.get_location("Hole 2 - Par").can_reach(state): return True
        if world.get_location("Hole 2 - Birdie").can_reach(state): return True
        if world.get_location("Hole 2 - Par Plus").can_reach(state): return True

        if world.get_location("Hole 3 - Par").can_reach(state): return True
        if world.get_location("Hole 3 - Birdie").can_reach(state): return True
        if world.get_location("Hole 3 - Par Plus").can_reach(state): return True

        if world.get_location("Hole 4 - Par").can_reach(state): return True
        if world.get_location("Hole 4 - Birdie").can_reach(state): return True
        if world.get_location("Hole 4 - Par Plus").can_reach(state): return True

        if world.get_location("Hole 5 - Par").can_reach(state): return True
        if world.get_location("Hole 5 - Birdie").can_reach(state): return True

        if world.get_location("Hole 6 - Par").can_reach(state): return True
        if world.get_location("Hole 6 - Birdie").can_reach(state): return True
        if world.get_location("Hole 6 - Par Plus").can_reach(state): return True

        if world.get_location("Hole 7 - Par").can_reach(state): return True
        if world.get_location("Hole 7 - Birdie").can_reach(state): return True
        if world.get_location("Hole 7 - Par Plus").can_reach(state): return True

        if world.get_location("Hole 8 - Par").can_reach(state): return True
        if world.get_location("Hole 8 - Birdie").can_reach(state): return True

        if world.get_location("Hole 9 - Par").can_reach(state): return True
        if world.get_location("Hole 9 - Birdie").can_reach(state): return True
        return False

    def par_rule(state) -> bool:
        if birdie_rule(state): return True
        if world.get_location("Hole 5 - Par Plus").can_reach(state): return True
        if world.get_location("Hole 8 - Par Plus").can_reach(state): return True
        if world.get_location("Hole 9 - Par Plus").can_reach(state): return True
        return False

    def to_the_moon_rule(state) -> bool:
        if state.can_reach_region(Regions.Holes_2_to_5, world.player) and state.has("Driver", world.player): return True
        else: return False

    def skipper_rule(state) -> bool:
        if ((state.has("Driver", world.player) or state.has("Hybrid", world.player)) and
                (state.can_reach_region(Regions.FrontYard, world.player)
                 or state.can_reach_region(Regions.Hole_1_Area, world.player)
                 or state.can_reach_region(Regions.Holes_2_to_5, world.player)
                 or state.can_reach_region(Regions.Holes_6_to_9, world.player)
                 or state.can_reach_region(Regions.LakeArea, world.player))): return True
        else: return False

    def lavatory_linksman_rule(state) -> bool:
        if (state.can_reach_region(Regions.ProShop_Bathroom, world.player) and
                ( state.has("Driver", world.player)
                  or state.has("Hybrid", world.player)
                  or state.has("Iron", world.player)
                  or state.has("Wedge", world.player))): return True
        else: return False

    def all_clubs_rule(state) -> bool:
        if (state.has("Driver", world.player)
                and state.has("Hybrid", world.player)
                and state.has("Iron", world.player)
                and state.has("Wedge", world.player)
                and state.has("Putter", world.player)): return True
        else: return False

    def putt_putt_rule(state) -> bool:
        if state.has("Putter", world.player): return True
        else: return False

    def mystery_bounty_rule(state) -> bool:
        if world.get_location("Mystery Bounty").can_reach(state): return True
        else: return False

    def albatross_rule(state) -> bool:
        if world.get_location("Hole 6 - Par").can_reach(state): return True
        if world.get_location("Hole 6 - Birdie").can_reach(state): return True
        return False

    def region_rule(region: str):
        def rule(state) -> bool:
            if state.can_reach_region(region, world.player): return True
            else: return False
        return rule

    for name, achv in achievement_data.items():
        if achv["region"] == "":
            if name == "Achievement: To The Moon":
                add_rule(world.get_location(name), to_the_moon_rule)
            elif name == "Achievement: Skipper":
                add_rule(world.get_location(name), skipper_rule)
            elif name == "Achievement: Lavatory Linksman":
                add_rule(world.get_location(name), lavatory_linksman_rule)
            elif name == "Achievement: What an Achievement":
                add_rule(world.get_location(name), all_clubs_rule)
            elif name == "Achievement: Putt Putt":
                set_rule(world.get_location(name), putt_putt_rule)
            elif name == "Achievement: ????":
                add_rule(world.get_location(name), mystery_bounty_rule)
            elif name == "Achievement: Ace":
                if world.options.achievement_checks_hole_in_one_enabled:
                    add_rule(world.get_location(name), hole_in_one_rule)
            elif name == "Achievement: Eagle":
                add_rule(world.get_location(name), eagle_rule)
            elif name == "Achievement: Birdie":
                add_rule(world.get_location(name), birdie_rule)
            elif name == "Achievement: Par":
                add_rule(world.get_location(name), par_rule)
            elif name == "Achievement: Albatross":
                if world.options.achievement_checks_albatross_hole6_enabled:
                    add_rule(world.get_location(name), albatross_rule)
        else:
            add_rule(world.get_location(name), region_rule(achv["region"]))

def set_completion_condition(world: APNormalGolfWorld) -> None:
    amount = world.options.req_bounties_to_win.value
    world.set_completion_rule(Has(BOUNTY_COMPLETE, amount))

