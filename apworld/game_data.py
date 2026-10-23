from __future__ import annotations

from enum import IntEnum
from typing import TypedDict

from .regions import Regions

ID_OFFSET_ITEM_DIFFICULTY_UNLOCK = 600
ID_OFFSET_ITEM_REGION_UNLOCK = 1000
ID_OFFSET_ITEM_CASH = 2000
ID_OFFSET_ITEM_FILLER = 3000
ID_OFFSET_ITEM_TRAP = 4000
ID_OFFSET_LOCATION_SHOP = 50000
ID_OFFSET_LOCATION_STRAY_CASH = 60000

class GolfClubs(IntEnum):
    Putter = 1
    Wedge = 2
    Iron = 3
    Hybrid = 4
    Driver = 5


class Difficulty(IntEnum):
    SUPER_EASY = 1
    EASY = 2
    MANAGEABLE = 3
    INTERMEDIATE = 4
    DIFFICULT = 5
    VERY_HARD = 6
    NIGHTMARE = 7
    DIABOLICAL = 8
    IMPOSSIBLE = 9


DIFFICULTY_CASH: dict[Difficulty, int] = {
    Difficulty.SUPER_EASY: 75,
    Difficulty.EASY: 100,
    Difficulty.MANAGEABLE: 125,
    Difficulty.INTERMEDIATE: 150,
    Difficulty.DIFFICULT: 200,
    Difficulty.VERY_HARD: 250,
    Difficulty.NIGHTMARE: 400,
    Difficulty.DIABOLICAL: 600,
    Difficulty.IMPOSSIBLE: 800,
}


# smallest_club_req is the smallest club this bounty is possible with.
#   ex. hole 1 par is not possible with only a putter, but it is with only an iron
#   this assumes that if a bounty is possible with just a wedge, it is with just an iron, a hybrid, etc.
# game_id is the gameobject name. usually PadV3_ + the bounty name w/out spaces
class GolfBounty(TypedDict):
    id: int  # unique location ID
    difficulty: Difficulty
    region: str
    smallest_club_req: GolfClubs
    game_id: str

class ShopItem(TypedDict):
    id: int
    cost: int
    region: str

class StrayCashItem(TypedDict):
    id: int
    region: str


TOTAL_COST_OF_ALL_SHOP = 12100
TOTAL_COST_OF_SHOP_CLUBS = 3450

#todo: put all the id offsets in one place. very sloppy
# 500XX for shop items
#todo: make the 4 clubs and the ticket guranteed to be non-cash progression items? idk
shop_data: dict[str, ShopItem] = {
    "Pro Shop Buy Putter" : {"id": ID_OFFSET_LOCATION_SHOP, "cost": 200, "region": Regions.ProShop},
    "Pro Shop Buy Wedge" : {"id": ID_OFFSET_LOCATION_SHOP + 1, "cost":1500, "region": Regions.ProShop},
    "Pro Shop Buy Hybrid" : {"id": ID_OFFSET_LOCATION_SHOP + 2, "cost":1500, "region": Regions.ProShop},
    "Pro Shop Buy Driver" : {"id": ID_OFFSET_LOCATION_SHOP + 3, "cost":250, "region": Regions.ProShop},
    "Pro Shop Buy LMUGC Ticket" : {"id": ID_OFFSET_LOCATION_SHOP + 4, "cost":1750, "region": Regions.ProShop},
    "Pro Shop Crowbar" : {"id": ID_OFFSET_LOCATION_SHOP + 5, "cost":0, "region": Regions.ProShop_Upstairs},
    "Pro Shop Buy Mulligan #1" : {"id": ID_OFFSET_LOCATION_SHOP + 6, "cost":400, "region": Regions.ProShop_Upstairs},
    "Pro Shop Buy Mulligan #2" : {"id": ID_OFFSET_LOCATION_SHOP + 7, "cost":400, "region": Regions.ProShop_Upstairs},
    "Pro Shop Buy Mulligan #3" : {"id": ID_OFFSET_LOCATION_SHOP + 8, "cost":400, "region": Regions.ProShop_Upstairs},
    "Pro Shop Buy Mulligan #4" : {"id": ID_OFFSET_LOCATION_SHOP + 9, "cost":400, "region": Regions.ProShop_Upstairs},
    "Pro Shop Buy Mulligan #5" : {"id": ID_OFFSET_LOCATION_SHOP + 10, "cost":400, "region": Regions.ProShop_Upstairs},
    "Pro Shop Buy Mulligan #6" : {"id": ID_OFFSET_LOCATION_SHOP + 11, "cost":400, "region": Regions.ProShop_Upstairs},
    "Pro Shop Buy No Wind #1" : {"id": ID_OFFSET_LOCATION_SHOP + 12, "cost":250, "region": Regions.ProShop_Upstairs},
    "Pro Shop Buy No Wind #2" : {"id": ID_OFFSET_LOCATION_SHOP + 13, "cost":250, "region": Regions.ProShop_Upstairs},
    "Pro Shop Buy No Wind #3" : {"id": ID_OFFSET_LOCATION_SHOP + 14, "cost":250, "region": Regions.ProShop_Upstairs},
    "Pro Shop Buy No Wind #4" : {"id": ID_OFFSET_LOCATION_SHOP + 15, "cost":250, "region": Regions.ProShop_Upstairs},
    "Pro Shop Buy Hole Skip #1" : {"id": ID_OFFSET_LOCATION_SHOP + 16, "cost":700, "region": Regions.ProShop},
    "Pro Shop Buy Hole Skip #2" : {"id": ID_OFFSET_LOCATION_SHOP + 17, "cost":700, "region": Regions.ProShop},
    "Pro Shop Buy Hole Skip #3" : {"id": ID_OFFSET_LOCATION_SHOP + 18, "cost":700, "region": Regions.ProShop},
    "Pro Shop Buy Hole Skip #4" : {"id": ID_OFFSET_LOCATION_SHOP + 19, "cost":700, "region": Regions.ProShop},
    "Pro Shop Buy Hole Skip #5" : {"id": ID_OFFSET_LOCATION_SHOP + 20, "cost":700, "region": Regions.ProShop}
}

#todo: driveway picket fence cash can be collected from either holes6-9 or holes2-5
stray_cash_data: dict[str, StrayCashItem] = {
    "Stray Cash (pro shop shelf)" : {"id" : ID_OFFSET_LOCATION_STRAY_CASH, "region": Regions.ProShop},
    "Stray Cash (cash register)": {"id" : ID_OFFSET_LOCATION_STRAY_CASH + 1, "region":Regions.ProShop},
    "Stray Cash (boxes behind register)": {"id" : ID_OFFSET_LOCATION_STRAY_CASH + 2, "region": Regions.ProShop_Upstairs},
    "Stray Cash (practice putt)": {"id" : ID_OFFSET_LOCATION_STRAY_CASH + 3, "region":Regions.Hole_1_Area},
    "Stray Cash (hole 3 picnic table)": {"id" : ID_OFFSET_LOCATION_STRAY_CASH + 4, "region": Regions.Holes_2_to_5},
    "Stray Cash (hole 4 no swimming sign)": {"id" : ID_OFFSET_LOCATION_STRAY_CASH + 5, "region": Regions.Holes_2_to_5},
    "Stray Cash (tunnel rocks #1)": {"id" : ID_OFFSET_LOCATION_STRAY_CASH + 6, "region": Regions.Holes_2_to_5} ,
    "Stray Cash (tunnel rocks #2)": {"id" : ID_OFFSET_LOCATION_STRAY_CASH + 7, "region": Regions.Holes_2_to_5},
    "Stray Cash (driveway picket fence)": {"id" : ID_OFFSET_LOCATION_STRAY_CASH + 8, "region":Regions.Holes_6_to_9 },
    "Stray Cash (mountainside bunker door)": {"id" : ID_OFFSET_LOCATION_STRAY_CASH + 9, "region":Regions.Mountaintop},
    "Stray Cash (Hole 6 rocks #1)": {"id" : ID_OFFSET_LOCATION_STRAY_CASH + 10, "region":Regions.Holes_6_to_9},
    "Stray Cash (Hole 6 rocks #2)": {"id" : ID_OFFSET_LOCATION_STRAY_CASH + 11, "region":Regions.Holes_6_to_9},
}

#ID is XXYYY, where XX is the parent ID and YYY is the index among its siblings
#10 if child of "Pads"
#11 if child of "Special Pads" (only My First Multi Hit and Great Explorer)
#12 if child of ParPads (index 0 is ParConfetti, so it will start at 1

#i dont think things will ever get added that messes up the sibling index (barring a game update).
#todo: i probably should have a safer way to get the id.
#   since in Harmony i was just gonna call "__instance.gameObject.transform.GetSiblingIndex();"
#   hope this doesnt cause problems later!

#   Hole 1 is possible to complete while only having access to FrontYard with Hole-In-Ones
#   in that case, smallest club req is Iron

#   My First Multi-Hit requires front yard + hole1

bounty_data: dict[str, GolfBounty] = {
    "Space Captain": {
        "id": 10014,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.CarPark,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "PadV3_SpaceCaptain"
    },
    "Pinball": {
        "id": 10018,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.CarPark,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "PadV3_Pinball"
    },
    "Quitter": {
        "id": 10008,
        "difficulty": Difficulty.SUPER_EASY,
        "region": Regions.FrontYard,
        "smallest_club_req": GolfClubs.Putter,
        "game_id": "PadV3_Quitter"
    },
    "The Big Flush": {
        "id": 10007,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.FrontYard,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_Toilet"
    },
    "Tiny Island 1": {
        "id": 10009,
        "difficulty": Difficulty.NIGHTMARE,
        "region": Regions.FrontYard,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_MiniHole"
    },
    "No Clip": {
        "id": 10017,
        "difficulty": Difficulty.EASY,
        "region": Regions.FrontYard,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_HiddenGong"
    },
    "Consistency": {
        "id": 10003,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.FrontYard,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_3Fairways"
    },
    "Crosswind": {
        "id": 10006,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.FrontYard,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "PadV3_GreenWind"
    },
    "My First Multi Hit": {
        "id": 11000,
        "difficulty": Difficulty.EASY,
        "region": Regions.FrontYard,    #Requires FrontYard AND Hole 1 Area
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "MULTIHITPad_Tutorial"
    },
    "Putt Putt Ace": {
        "id": 10013,
        "difficulty": Difficulty.DIABOLICAL,
        "region": Regions.Hole_1_Area,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_PuttPuttAce"
    },
    "Watermelon Ninja": {
        "id": 10021,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.Hole_1_Area,
        "smallest_club_req": GolfClubs.Putter,
        "game_id": "PadV3_FN"
    },
    "Putting Drill": {
        "id": 10020,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Hole_1_Area,
        "smallest_club_req": GolfClubs.Putter,
        "game_id": "PadV3_PuttingDrill2"
    },
    "Top Shelf": {
        "id": 10019,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.Hole_1_Area,
        "smallest_club_req": GolfClubs.Putter,
        "game_id": "PadV3_TopShelf"
    },
    "Nice On": {
        "id": 10016,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Hole_1_Area,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_Close"
    },
    "Thread the Needle": {
        "id": 10015,
        "difficulty": Difficulty.DIABOLICAL,
        "region": Regions.Hole_1_Area,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_Pole"
    },
    "Gone Home": {
        "id": 10026,
        "difficulty": Difficulty.NIGHTMARE,
        "region": Regions.Hole_1_Area,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "PadV3_GoneHome"
    },
    "Wrong Green 1": {
        "id": 10005,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_WrongGreen2"  #Not a mistake, Wrong Green is WrongGreen2
    },
    "Wrong Green 2": {
        "id": 10004,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Driver,
        "game_id": "PadV3_WrongGreen"   #Not a mistake, Wrong Green 2 is WrongGreen
    },
    "Good Dog": {
        "id": 10052,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_Trivia1"
    },
    "Great Explorer": {
        "id": 11001,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "MULTIHITPad_CrossCountry"
    },
    "Tiny Island 3": {
        "id": 10012,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_TinyIsland3"
    },
    "Bunker Bypass": {
        "id": 10043,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "PadV3_BB3"
    },
    "Bunker Behavior": {
        "id": 10041,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_BB1"
    },
    "Bunker Dunker": {
        "id": 10042,
        "difficulty": Difficulty.IMPOSSIBLE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_BB2"
    },
    "Bunker Buster": {
        "id": 10044,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_BB4"
    },
    "Splishy Splashy": {
        "id": 10063,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Hybrid,
        "game_id": "PadV3_Skip3"
    },
    "Apple Ninja": {
        "id": 10025,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_FNApple"
    },
    "To The Moon": {
        "id": 10040,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Driver,
        "game_id": "PadV3_ToTheMoon"
    },
    "You Can't Miss": {
        "id": 10039,
        "difficulty": Difficulty.SUPER_EASY,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Putter,
        "game_id": "PadV3_PuttDish"
    },
    "You Might Miss": {
        "id": 10045,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_PuttDish (1)"
    },
    "You Will Miss": {
        "id": 10046,
        "difficulty": Difficulty.NIGHTMARE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_PuttDish (2)"
    },
    "You Have Missed": {
        "id": 10047,
        "difficulty": Difficulty.IMPOSSIBLE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Hybrid,
        "game_id": "PadV3_PuttDish (3)"
    },
    "Hazy Memory": {
        "id": 10053,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_Trivia4"
    },
    "Putt Putt Putt Putt": {
        "id": 10028,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Putter,
        "game_id": "PadV3_PuttHole4a"
    },
    "Chipper": {
        "id": 10048,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_PuttHole4b"
    },
    "Curlew 1": {
        "id": 10069,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "CC_Hole5Birdy"
    },
    "Skipper": {
        "id": 10060,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Hybrid,
        "game_id": "PadV3_Skip1"
    },
    "Central Tee 1": {
        "id": 10032,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "PadV3_CentralTee 1"
    },
    "Central Tee 2": {
        "id": 10034,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "PadV3_CentralTee 2"
    },
    "Central Tee 3": {
        "id": 10033,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Hybrid,
        "game_id": "PadV3_CentralTee 3"
    },
    "Pressure Drill": {
        "id": 10037,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Putter,
        "game_id": "PadV3_PuttPool2"
    },
    "8 Ball Scratch": {
        "id": 10031,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Putter,
        "game_id": "PadV3_PuttPool"
    },
    "Bender": {
        "id": 10027,
        "difficulty": Difficulty.DIABOLICAL,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_Bender"
    },
    "Cliffside Pool 1": {
        "id": 10035,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "PadV3_CliffsidePool"
    },
    "Trickster": {
        "id": 10030,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Putter,
        "game_id": "PadV3_PuttJump"
    },
    "Cliffside Pool 2": {
        "id": 10036,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Driver,
        "game_id": "PadV3_CliffsidePool2"
    },
    "Viral Challenge 1": {
        "id": 10056,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_Pint1"
    },
    "Hall Monitor": {
        "id": 10049,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "PadV3_HallMonitor"
    },
    "Crag Gong": {
        "id": 10072,
        "difficulty": Difficulty.EASY,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Iron,  #TODO: This requires the Iron AND the Driver
        "game_id": "NEW_CliffGong"
    },
    "Secret Green": {
        "id": 10011,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_SecretGreen"
    },
    "Hidden Pin": {
        "id": 10074,
        "difficulty": Difficulty.EASY,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "NEW_HiddenPin"
    },
    "Smarty Pants": {
        "id": 10054,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_Trivia2"
    },
    "Tiny Island 2": {
        "id": 10010,
        "difficulty": Difficulty.NIGHTMARE,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_TinyIsland2"
    },
    "Head High": {
        "id": 10050,
        "difficulty": Difficulty.EASY,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_Headwind"
    },
    "Drawn In": {
        "id": 10051,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_Headwind2"
    },
    "Fish Out of Water": {
        "id": 10061,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Hybrid,
        "game_id": "PadV3_Skip2"
    },
    "Sea Legs": {
        "id": 10062,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Driver,
        "game_id": "PadV3_Skip4"
    },
    "Sisyphus Flat": {
        "id": 10064,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "PadV3_Megaball1"
    },
    "Find the Angle": {
        "id": 10029,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Putter,
        "game_id": "PadV3_PuttHole7"
    },
    "Misclick": {
        "id": 10075,
        "difficulty": Difficulty.SUPER_EASY,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "NEW_SecretBunker"
    },
    "Sisyphus Tilt": {
        "id": 10065,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "PadV3_Megaball2"
    },
    "Sisyphus With a S": {
        "id": 10066,
        "difficulty": Difficulty.NIGHTMARE,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "PadV3_Megaball3"
    },
    "Curlew 2": {
        "id": 10070,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "CC_Hole5Birdy2"
    },
    "Volcano": {
        "id": 10073,
        "difficulty": Difficulty.EASY,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "NEW_Volcano"
    },
    "Viral Challenge 2": {
        "id": 10057,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_Pint2"
    },
    "Viral Challenge 3": {
        "id": 10058,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_Pint3"
    },
    "Math Is Hard": {
        "id": 10055,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_Trivia3"
    },
    "Tilted": {
        "id": 10038,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Putter,
        "game_id": "PadV3_PuttTilted"
    },
    "No Cheese Chip 1": {
        "id": 10067,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_ChipUp"
    },
    "No Cheese Chip 2": {
        "id": 10068,
        "difficulty": Difficulty.IMPOSSIBLE,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_ChipUpImpossible"
    },
    "???": {
        "id": 10059,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_Code"
    },
    "Big Bunker": {
        "id": 10071,
        "difficulty": Difficulty.EASY,
        "region": Regions.Mountaintop,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "NEW_BigBunker"
    },
    "Long Drop": {
        "id": 10001,
        "difficulty": Difficulty.EASY,
        "region": Regions.Mountaintop,
        "smallest_club_req": GolfClubs.Putter,
        "game_id": "PadV3_LongDrop"
    },
    "Far Far Away": {
        "id": 10002,
        "difficulty": Difficulty.NIGHTMARE,
        "region": Regions.Mountaintop,
        "smallest_club_req": GolfClubs.Hybrid,
        "game_id": "PadV3_FarFarAway"
    },
    "The Windy Apple": {
        "id": 10000,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Mountaintop,
        "smallest_club_req": GolfClubs.Hybrid,
        "game_id": "PadV3_LongDrive"
    },
    "Streak Ninja": {
        "id": 10022,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.LakeArea,
        "smallest_club_req": GolfClubs.Putter,
        "game_id": "PadV3_FN (1)"
    },
    "Sideways": {
        "id": 10024,
        "difficulty": Difficulty.DIABOLICAL,
        "region": Regions.LakeArea,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "PadV3_Sideways"
    },
    "Gong Bomb": {
        "id": 10023,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.LakeArea,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "PadV3_GongBomb"
    },
    "Hole 1 - Par": {
        "id": 12001,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Hole_1_Area,
        "smallest_club_req": GolfClubs.Wedge,   #TODO Different based on if player has hole1 area unlocked
        "game_id": "Hole1Par"
    },
    "Hole 1 - Birdie": {
        "id": 12003,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.Hole_1_Area,
        "smallest_club_req": GolfClubs.Iron,  #TODO Different based on if player has hole1 area unlocked
        "game_id": "Hole1Birdy"
    },
    "Hole 1 - Par Plus": {
        "id": 12002,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Hole_1_Area,
        "smallest_club_req": GolfClubs.Wedge,  #TODO Different based on if player has hole1 area unlocked
        "game_id": "Hole1ParPlus"
    },
    "Hole 2 - Par": {
        "id": 12004,
        "difficulty": Difficulty.MANAGEABLE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "Hole2Par"
    },
    "Hole 2 - Birdie": {
        "id": 12006,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "Hole2Birdy"
    },
    "Hole 2 - Par Plus": {
        "id": 12005,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Iron,  #TODO: Restricts Driver and Hybrid
        "game_id": "Hole2ParPlus"
    },
    "Hole 3 - Par": {
        "id": 12007,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "Hole3Par"
    },
    "Hole 3 - Birdie": {
        "id": 12009,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,  #TODO:
        "game_id": "Hole3Birdy"
    },
    "Hole 3 - Par Plus": {
        "id": 12008,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "HoleParPlus"
    },
    "Hole 4 - Par": {
        "id": 12010,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "Hole4Par"
    },
    "Hole 4 - Birdie": {
        "id": 12012,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "Hole4Birdy"
    },
    "Hole 4 - Par Plus": {
        "id": 12011,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "Hole4ParPlus"
    },
    "Hole 5 - Par": {
        "id": 12013,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "Hole5Par"
    },
    "Hole 5 - Birdie": {
        "id": 12015,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "Hole5Birdy"
    },
    "Hole 5 - Par Plus": {
        "id": 12014,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.Holes_2_to_5,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "Hole5ParPlus"
    },
    "Hole 6 - Par": {
        "id": 12016,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "Hole6Par"
    },
    "Hole 6 - Birdie": {
        "id": 12018,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "Hole6Birdy"
    },
    "Hole 6 - Par Plus": {
        "id": 12017,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "Hole6ParPlus"
    },
    "Hole 7 - Par": {
        "id": 12019,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "Hole7Par"
    },
    "Hole 7 - Birdie": {
        "id": 12021,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "Hole7Birdy"
    },
    "Hole 7 - Par Plus": {
        "id": 12020,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "Hole7ParPlus"
    },
    "Hole 8 - Par": {
        "id": 12022,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "Hole8Par"
    },
    "Hole 8 - Birdie": {
        "id": 12024,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "Hole8Birdy"
    },
    "Hole 8 - Par Plus": {
        "id": 12023,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "Hole8ParPlus"
    },
    "Hole 9 - Par": {
        "id": 12025,
        "difficulty": Difficulty.INTERMEDIATE,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Wedge,
        "game_id": "Hole9Par"
    },
    "Hole 9 - Birdie": {
        "id": 12027,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Iron,
        "game_id": "Hole9Birdy"
    },
    "Hole 9 - Par Plus": {
        "id": 12026,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.Holes_6_to_9,
        "smallest_club_req": GolfClubs.Hybrid,
        "game_id": "Hole9ParPlus"
    }
}

