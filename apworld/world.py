import random
from collections.abc import Mapping
from typing import Any

from BaseClasses import ItemClassification, CollectionState, Item

# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, regions, rules
from . import options as normalgolfgame_options
from .game_data import GolfClubs, Difficulty
from .locations import LOCATION_NAME_TO_ID
from .items import ITEM_NAME_TO_ID
from .regions import Regions

# This implementation in particular has the following additional files, each covering one topic:
# regions.py, locations.py, rules.py, items.py, options.py and web_world.py.
# It is recommended that you read these in that specific order, then come back to the world class.
class APNormalGolfWorld(World):
    game = "Normal Golf Game"

    location_name_to_id = LOCATION_NAME_TO_ID
    item_name_to_id = ITEM_NAME_TO_ID

    options_dataclass = normalgolfgame_options.APNormalGolfGameOptions
    options: normalgolfgame_options.APNormalGolfGameOptions

    number_of_bounties = 0

    unique_nums: list[int] = []

    def generate_early(self) -> None:
        clubs = ["Putter", "Wedge", "Iron", "Hybrid", "Driver"]
        starting_regions = {
            0: "Car Park",
            1: "Front Yard",
            4: "Hole 1 Area",
            5: "Holes 2-5",
            6: "Holes 6-9",
        }
        starting_club = clubs[self.options.starting_club.value]
        self.multiworld.push_precollected(self.create_item(starting_club))
        self.origin_region_name = starting_regions[self.options.starting_region.value]

        difficulty_list = list(Difficulty)

        unique_nums: list[int] = []
        for i in range(self.options.num_starting_difficulties.value):
            added = False
            while not added:
                num = self.random.randint(0, 8)
                if num not in unique_nums:
                    unique_nums.append(num)
                    added = True
                    self.multiworld.push_precollected(self.create_item("Unlock " + difficulty_list[num].name + " bounties"))


    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.APNormalGolfItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def collect(self, state: CollectionState, item: items.APNormalGolfItem) -> bool:
        change = super().collect(state, item)
        if change:
            if item.name.startswith("$"):
                state.prog_items[self.player]["golf_money"] += items.cash_items[item.name]
            elif item.name == "Filler 50$":
                state.prog_items[self.player]["golf_money"] += 50
        return change

    def remove(self, state: CollectionState, item: items.APNormalGolfItem) -> bool:
        change = super().remove(state, item)
        if change:
            if item.name.startswith("$"):
                state.prog_items[self.player]["golf_money"] -= items.cash_items[item.name]
            elif item.name == "Filler 50$":
                state.prog_items[self.player]["golf_money"] -= 50
        return change

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data =  self.options.as_dict(
            "req_bounties_to_win", "starting_club", "starting_region", "num_starting_difficulties")
        slot_data["starting_difficulties_ids"] = self.unique_nums
        return slot_data

