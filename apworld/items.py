from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from enum import IntEnum

from .game_data import bounty_data, shop_data, DIFFICULTY_CASH, Difficulty, ID_OFFSET_ITEM_REGION_UNLOCK, \
    ID_OFFSET_ITEM_CASH, ID_OFFSET_ITEM_DIFFICULTY_UNLOCK, ID_OFFSET_ITEM_FILLER, ID_OFFSET_ITEM_TRAP

if TYPE_CHECKING:
    from .world import APNormalGolfWorld


class APNormalGolfItem(Item):
    game = "Normal Golf Game"

BOUNTY_COMPLETE = "Bounty Complete"

DEFAULT_ITEM_CLASSIFICATIONS = {
    BOUNTY_COMPLETE: ItemClassification.progression,
    "Putter": ItemClassification.progression | ItemClassification.useful,
    "Wedge": ItemClassification.progression | ItemClassification.useful,
    "Iron": ItemClassification.progression | ItemClassification.useful,
    "Hybrid": ItemClassification.progression | ItemClassification.useful,
    "Driver": ItemClassification.progression | ItemClassification.useful,
    "$50": ItemClassification.progression,
    "$75": ItemClassification.progression,
    "$100": ItemClassification.progression,
    "$125": ItemClassification.progression,
    "$150": ItemClassification.progression,
    "$200": ItemClassification.progression,
    "$400": ItemClassification.progression,
    "$600": ItemClassification.progression,
    "$800": ItemClassification.progression,
    "$1000": ItemClassification.progression,
    "Filler $50": ItemClassification.filler
}

ITEM_NAME_TO_ID: dict[str, int] = {
    BOUNTY_COMPLETE: 1,
    "Putter": 2,
    "Wedge": 3,
    "Iron": 4,
    "Hybrid": 5,
    "Driver": 6,
    "Practice Panel": 7,
}

region_unlocks: list[str] = [
    "Unlock Car Park Gate to Front Yard",
    "Unlock Car Park Gate to Holes 2-5",
    "Unlock Pro Shop Door",
    "Unlock Front Yard Gate to Hole 1",
    "Unlock Front Yard Gate to Holes 6-9",
    "Unlock Front Yard Teleporter #2B Shed",
    "Unlock Pro Shop Upstairs",
    "Unlock Pro Shop Bathroom Door",
    "Unlock Hole 1 Gate to Holes 2-5",
    "Unlock Hole 6 Gate",
    "Unlock Driveway Gate to Holes 6-9",
    "Unlock Teleporter #2A Shed",
    "Unlock Teleporter #3 Shed",
    "Unlock Gate to Mountaintop",
    "Unlock Teleporter #1",
    "Unlock Teleporter #2",
    "Unlock Green Screen Building",
    "Unlock Luke's Office Door",
    "Unlock Cash Room Door",
    "Unlock Padlock Room Door",
    "Unlock Simulator Room Door"]

unlock_id = 0
for unlock in region_unlocks:
    ITEM_NAME_TO_ID[unlock] = ID_OFFSET_ITEM_REGION_UNLOCK + unlock_id
    unlock_id += 1

#sums to 3500.
cash_items: dict[str, int] = {
    "$50" : 50,
    "$75" : 75,
    "$100" : 100,
    "$125" : 125,
    "$150" : 150,
    "$200" : 200,
    "$400" : 400,
    "$600" : 600,
    "$800" : 800,
    "$1000" : 1000
}

#id 3000
filler_items: list[str] = [
    "Filler $50",
    "Music Pitch Down",
    "Music Pitch Up"
]

#id 4000
trap_items: list[str] = [
    "Icy Green Trap",
    "Icy Fairway Trap",
    "Bouncy Green Trap",
    "Bouncy Fairway Trap",
    "Accelerated Fairway Trap",
    "Evil Kookaburra"
]

cash_id = 0
for name, cash in cash_items.items():
    ITEM_NAME_TO_ID[name] = cash_id + ID_OFFSET_ITEM_CASH
    cash_id += 1

difficulty_unlock_id = 0
for difficulty in Difficulty:
    ITEM_NAME_TO_ID["Unlock " + difficulty.name + " bounties"] = ID_OFFSET_ITEM_DIFFICULTY_UNLOCK + difficulty_unlock_id
    difficulty_unlock_id += 1

filler_id = 0
for filler in filler_items:
    ITEM_NAME_TO_ID[filler] = filler_id + ID_OFFSET_ITEM_FILLER
    filler_id += 1

trap_id = 0
for trap in trap_items:
    ITEM_NAME_TO_ID[trap] = trap_id + ID_OFFSET_ITEM_TRAP
    trap_id += 1



def create_all_items(world: APNormalGolfWorld) -> None:
    itempool: list[Item] = []

    if world.options.starting_club.value != 0:
        itempool += [world.create_item("Putter")]
    if world.options.starting_club.value != 1:
        itempool += [world.create_item("Wedge")]
    if world.options.starting_club.value != 2:
        itempool += [world.create_item("Iron")]
    if world.options.starting_club.value != 3:
        itempool += [world.create_item("Hybrid")]
    if world.options.starting_club.value != 4:
        itempool += [world.create_item("Driver")]

    for unlock_item in region_unlocks:
        itempool.append(world.create_item(unlock_item))

    #Adds the progression cash items to guarantee that every shop location is obtainable
    #i think cash_items will be more fun than 105 cash items from each bounty, so theres room for filler items
    for i in range(4):
        for cash_item, val in cash_items.items():
            itempool.append(world.create_item(cash_item))

    for diff in Difficulty:
        if diff in world.starting_difficulties:
            continue
        itempool.append(world.create_item("Unlock " + diff.name + " bounties"))


    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    world.multiworld.itempool += itempool

def create_item_with_correct_classification(world: APNormalGolfWorld, name: str) -> APNormalGolfItem:
    if name in DEFAULT_ITEM_CLASSIFICATIONS:
        classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    elif name.startswith("$"):
        classification = ItemClassification.progression
    elif name.startswith("Unlock "):
        classification = ItemClassification.progression | ItemClassification.useful
    else:
        classification = ItemClassification.filler
    return APNormalGolfItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

def get_random_filler_item_name(world: APNormalGolfWorld) -> str:
    # IMPORTANT: Whenever you need to use a random generator, you must use world.random.
    # This ensures that generating with the same generator seed twice yields the same output.
    # DO NOT use a bare random object from Python's built-in random module.
    return world.random.choice(filler_items + trap_items)

