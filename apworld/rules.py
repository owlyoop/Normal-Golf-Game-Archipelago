from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule
from .game_data import bounty_data, GolfClubs, shop_data, Difficulty
from worlds.generic.Rules import add_rule, set_rule
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
    set_completion_condition(world)

def set_all_location_rules(world: APNormalGolfWorld) -> None:

    def club_rule(min_club: int):
        allowed = [club.name for club in GolfClubs if club >= min_club]
        return lambda state: state.has_any(allowed, world.player)

    def difficulty_unlock_rule(difficulty: Difficulty):
        return lambda state: state.has("Unlock " + difficulty.name + " bounties", world.player)

    def additional_region_rule(region: str):
        return lambda state: state.can_reach_region(region, world.player)

    def hole2parplus_club_rule():
        allowed = [GolfClubs.Wedge.name, GolfClubs.Iron.name]
        return lambda state: state.has_any(allowed, world.player)

    def crag_gong_club_rule():
        required = [GolfClubs.Driver.name, GolfClubs.Iron.name]
        return lambda state: state.has_all(required, world.player)

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
            add_rule(world.get_location(name), additional_region_rule("Hole 1 Area"))
            add_rule(world.get_location(bounty_complete_event_name(name)), additional_region_rule("Hole 1 Area"))

    def shop_rule(price: int):
        return lambda state: state.has("golf_money", world.player, price)

    for name, item in shop_data.items():
        set_rule(world.get_location(name), shop_rule(item["cost"]))

def set_completion_condition(world: APNormalGolfWorld) -> None:
    amount = world.options.req_bounties_to_win.value
    world.set_completion_rule(Has(BOUNTY_COMPLETE, amount))

