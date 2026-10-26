from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState, ItemClassification
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule
from .game_data import bounty_data, GolfClubs, shop_data, Difficulty, Breakable, breakable_signs_data, golfhole_data
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
    set_breakable_rules(world)
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

    def no_filler_rule():
        return lambda item: item.classification != ItemClassification.filler

    def no_trap_rule():
        return lambda item: item.classification != ItemClassification.trap

    for name, item in shop_data.items():
        set_rule(world.get_location(name), shop_rule(item["cost"]))
        # todo: if i enable both of these rules, tests fail due running out of locations to place items
        '''if (name == "Pro Shop Buy Putter" or
                name == "Pro Shop Buy Wedge" or
                name == "Pro Shop Buy Iron" or
                name == "Pro Shop Buy Hybrid" or
                name == "Pro Shop Buy Driver" or
                name == "Pro Shop Buy LMUGC Ticket"):
            add_item_rule(world.get_location(name), no_trap_rule())
            #add_item_rule(world.get_location(name), no_filler_rule())'''

    for name, golfhole in golfhole_data.items():
        if (name == "No Cheese Chip Short Hole"
            or name == "No Cheese Chip Middle Hole"
            or name == "No Cheese Chip Tall Hole"
            or name == "Mini Island Hole #1"
            or name == "Mini Island Hole #2"
            or name == "Mini Island Hole #3"):
            add_rule(world.get_location(name), club_rule(2))


def breakable_rule(world: APNormalGolfWorld, region_club_dict):
    pairs = []  # club-region pairs
    for min_club, regions in region_club_dict.items():
        club_names = [club.name for club in GolfClubs if club >= min_club]
        pairs.append((club_names, list(regions)))

    #rule should return true if the player has any of the club-region combos
    def rule(state) -> bool:
        for club_names, regions in pairs:
            if not state.has_any(club_names, world.player):
                return False
            for region in regions:
                if state.can_reach_region(region, world.player):
                    return True
        return False
    return rule


def set_breakable_rules(world: APNormalGolfWorld) -> None:
    for name, sign in breakable_signs_data.items():
        set_rule(world.get_location(name), breakable_rule(world, sign["region_club_dict"]))




def set_completion_condition(world: APNormalGolfWorld) -> None:
    amount = world.options.req_bounties_to_win.value
    world.set_completion_rule(Has(BOUNTY_COMPLETE, amount))

