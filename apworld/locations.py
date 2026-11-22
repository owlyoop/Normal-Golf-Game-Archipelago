from __future__ import annotations
from typing import Dict, TypedDict, List
from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location
from . import world
from .items import BOUNTY_COMPLETE

if TYPE_CHECKING:
    from .world import APNormalGolfWorld

from .game_data import bounty_data, shop_data, stray_cash_data, ID_OFFSET_LOCATION_STRAY_CASH, golfhole_data, \
    breakable_signs_data, upstairs_cash_data, GolfClubs, golfholes_secret_green, achievement_data, \
    golfholes_mini_islands, breakable_statue_data


# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.

# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class APNormalGolfLocation(Location):
    game = "Normal Golf Game"

LOCATION_NAME_TO_ID = {}
for table in (bounty_data, shop_data, stray_cash_data, breakable_signs_data, breakable_statue_data, upstairs_cash_data,
              golfhole_data, golfholes_mini_islands, golfholes_secret_green,
              achievement_data):
   for location_id, data in table.items():
       LOCATION_NAME_TO_ID[location_id] = data["id"]

def create_all_locations(world: APNormalGolfWorld) -> None:
    create_bounty_locations(world)
    create_shop_locations(world)
    create_stray_cash_locations(world)
    create_upstairs_cash_locations(world)

    if world.options.breakable_checks_enabled:
        create_breakable_sign_locations(world)

    if world.options.hole_checks_enabled:
        create_golfhole_locations(world)

    if world.options.achievement_checks_enabled:
        create_achievement_locations(world)

def bounty_complete_event_name(bounty_name: str) -> str:
    return f"{bounty_name} (Complete)"

def create_bounty_locations(world: APNormalGolfWorld) -> None:
    for name, bounty in bounty_data.items():

        if world.options.great_explorer_allow_putter_logic:
            if name == "Great Explorer":
                bounty["smallest_club_req"] = GolfClubs.Putter

        region_obj = world.get_region(bounty["region"])
        location = APNormalGolfLocation(world.player, name, bounty["id"], region_obj)
        region_obj.locations.append(location)

        bountycomplete_event = APNormalGolfLocation(world.player, bounty_complete_event_name(name), None, region_obj)
        bountycomplete_event.place_locked_item(world.create_item(BOUNTY_COMPLETE))
        #todo: add cash event item here if im not scrambling/randomizing the cash items
        region_obj.locations.append(bountycomplete_event);

def create_shop_locations(world: APNormalGolfWorld) -> None:
    for name, shop in shop_data.items():
        region = world.get_region(shop["region"])
        location = APNormalGolfLocation(world.player, name, shop["id"], region)
        region.locations.append(location)

def create_stray_cash_locations(world: APNormalGolfWorld) -> None:
    for name, cash in stray_cash_data.items():
        region = world.get_region(cash["region"])
        location = APNormalGolfLocation(world.player, name, cash["id"], region)
        region.locations.append(location)

def create_upstairs_cash_locations(world: APNormalGolfWorld) -> None:
    for name, ucash in upstairs_cash_data.items():
        region = world.get_region(ucash["region"])
        location = APNormalGolfLocation(world.player, name, ucash["id"], region)
        region.locations.append(location)

def create_breakable_sign_locations(world: APNormalGolfWorld) -> None:
    for name, sign in breakable_signs_data.items():
        region = world.get_region(world.origin_region_name)
        location = APNormalGolfLocation(world.player, name, sign["id"], region)
        region.locations.append(location)

    if world.options.breakable_checks_statues_enabled:
        for name, statue in breakable_statue_data.items():
            region = world.get_region(world.origin_region_name)
            location = APNormalGolfLocation(world.player, name, statue["id"], region)
            region.locations.append(location)

def create_golfhole_locations(world: APNormalGolfWorld) -> None:
    for name, golfhole in golfhole_data.items():
        region = world.get_region(golfhole["region"])
        location = APNormalGolfLocation(world.player, name, golfhole["id"], region)
        region.locations.append(location)

    if world.options.hole_checks_enable_secret_greens:
        for name, golfhole in golfholes_secret_green.items():
            region = world.get_region(golfhole["region"])
            location = APNormalGolfLocation(world.player, name, golfhole["id"], region)
            region.locations.append(location)

    if world.options.hole_checks_enable_mini_island_holes:
        for name, golfhole in golfholes_mini_islands.items():
            region = world.get_region(golfhole["region"])
            location = APNormalGolfLocation(world.player, name, golfhole["id"], region)
            region.locations.append(location)

def create_achievement_locations(world: APNormalGolfWorld) -> None:
    for name, achv in achievement_data.items():
        if achv["region"] == "":
            if name == "Achievement: Ace":
                if world.options.achievement_checks_hole_in_one_enabled:
                    region = world.get_region("Car Park")
                    location = APNormalGolfLocation(world.player, name, achv["id"], region)
                    region.locations.append(location)
            elif name == "Achievement: Albatross":
                if world.options.achievement_checks_albatross_hole6_enabled:
                    region = world.get_region("Holes 6-9")
                    location = APNormalGolfLocation(world.player, name, achv["id"], region)
                    region.locations.append(location)
            else:
                region = world.get_region("Car Park") #these achievements dont have a specific location but the rules should handle this
                location = APNormalGolfLocation(world.player, name, achv["id"], region)
                region.locations.append(location)
        else:
            region = world.get_region(achv["region"])
            location = APNormalGolfLocation(world.player, name, achv["id"], region)
            region.locations.append(location)
