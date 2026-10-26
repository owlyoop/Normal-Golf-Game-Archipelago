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
ID_OFFSET_LOCATION_GOLFHOLE = 70000
ID_OFFSET_LOCATION_BREAKABLE = 71000

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

#region : Club , list of difficulties
#i hope this is helpful in making sure random starting region/club/difficulties wont cause world generation errors
REGIONS_CLUBS_DIFFICULTIES: dict[str, dict[int, list[int]]] = {
    Regions.CarPark : {1 : [],
                       2 : [],
                       3 : [3, 5],
                       4 : [3, 5],
                       5 : [3, 5]},

    Regions.FrontYard : {0 : [1],
                         1: [1, 2, 3, 4, 7],
                         2: [1, 2, 3, 4, 5, 7],
                         3: [1, 2, 3, 4, 5, 7],
                         4: [1, 2, 3, 4, 5, 7],
                         5: [1, 2, 3, 4, 5, 7],},

    Regions.Hole_1_Area : {1 : [3, 4],
                           2 : [3, 4, 5, 8],
                           3 : [3, 4, 5, 8, 9],
                           4 : [3, 4, 5, 8, 9],
                           5 : [3, 4, 5, 8, 9],},


    Regions.Holes_2_to_5 : {1 : [1, 4, 5],
                            2 : [1, 3, 4, 5, 6, 7, 8, 9],
                            3 : [1, 3, 4, 5, 6, 7, 8, 9],
                            4 : [1, 3, 4, 5, 6, 7, 8, 9],
                            5 : [1, 3, 4, 5, 6, 7, 8, 9]},

    Regions.Holes_6_to_9 : {1 : [2, 4, 5],
                            2 : [1, 2, 3, 4, 5, 6, 7, 9],
                            3 : [1, 2, 3, 4, 5, 6, 7, 9],
                            4 : [1, 2, 3, 4, 5, 6, 7, 9],
                            5 : [1, 2, 3, 4, 5, 6, 7, 9]},

    Regions.LakeArea : {1: [6],
                        2: [6, 8],
                        3: [3, 6, 8],
                        4: [3, 6, 8],
                        5: [3, 6, 8]},

    Regions.Mountaintop : { 1: [2],
                            2: [2, 5],
                            3: [2, 5],
                            4: [2, 5, 7],
                            5: [2, 5, 7]},

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

class GolfHole(TypedDict):
    id: int
    region: str

#the dict[int, list[str]] is:
#key: club
#value: list of regions that it is reasonable to hit the breakable with
class Breakable(TypedDict):
    id: int
    region_club_dict: dict[int, list[str]]


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
    "Stray Cash (green screen building)" : {"id": ID_OFFSET_LOCATION_STRAY_CASH + 12, "region": Regions.Green_Screen_Building},
    "Stray Cash (Teleporter Shed #3)" : {"id": ID_OFFSET_LOCATION_STRAY_CASH + 13, "region": "Teleporter #3A Shed"},
    "Lost Golf Ball" : {"id" : ID_OFFSET_LOCATION_STRAY_CASH + 14, "region": Regions.ProShop_Upstairs},
    "Unlock Bunker Button": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 15, "region": Regions.Lukes_Office},
}

upstairs_cash_data: dict[str, StrayCashItem] = {
    "Stray Cash (Cash Room #1)" : {"id" : ID_OFFSET_LOCATION_STRAY_CASH + 1000,
                                   "region": Regions.ProShop_Upstairs_CashRoom},
    "Stray Cash (Cash Room #2)": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 1001,
                                  "region": Regions.ProShop_Upstairs_CashRoom},
    "Stray Cash (Cash Room #3)": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 1002,
                                  "region": Regions.ProShop_Upstairs_CashRoom},
    "Stray Cash (Cash Room #4)": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 1003,
                                  "region": Regions.ProShop_Upstairs_CashRoom},
    "Stray Cash (Cash Room #5)": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 1004,
                                  "region": Regions.ProShop_Upstairs_CashRoom},
    "Stray Cash (Cash Room #6)": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 1005,
                                  "region": Regions.ProShop_Upstairs_CashRoom},
    "Stray Cash (Cash Room #7)": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 1006,
                                  "region": Regions.ProShop_Upstairs_CashRoom},
    "Stray Cash (Cash Room #8)": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 1007,
                                  "region": Regions.ProShop_Upstairs_CashRoom},
    "Stray Cash (Cash Room #9)": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 1008,
                                  "region": Regions.ProShop_Upstairs_CashRoom},
    "Stray Cash (Cash Room #10)": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 1009,
                                  "region": Regions.ProShop_Upstairs_CashRoom},
    "Stray Cash (Cash Room #11)": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 1010,
                                  "region": Regions.ProShop_Upstairs_CashRoom},
    "Stray Cash (Cash Room #12)": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 1011,
                                  "region": Regions.ProShop_Upstairs_CashRoom},
    "Stray Cash (Cash Room #13)": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 1012,
                                  "region": Regions.ProShop_Upstairs_CashRoom},
    "Stray Cash (Cash Room #14)": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 1013,
                                  "region": Regions.ProShop_Upstairs_CashRoom},
    "Stray Cash (Cash Room #15)": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 1014,
                                  "region": Regions.ProShop_Upstairs_CashRoom},
    "Stray Cash (Cash Room #16)": {"id": ID_OFFSET_LOCATION_STRAY_CASH + 1015,
                                   "region": Regions.ProShop_Upstairs_CashRoom},

}

#for holesanity where every golfhole is a location
golfhole_data: dict[str, GolfHole] = {
    "Hole #1 hole" : {"id" : ID_OFFSET_LOCATION_GOLFHOLE, "region":Regions.Hole_1_Area},
    "Hole #2 hole" : {"id" : ID_OFFSET_LOCATION_GOLFHOLE + 1, "region":Regions.Holes_2_to_5},
    "Hole #3 hole": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 2, "region": Regions.Holes_2_to_5},
    "Hole #4 hole": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 3, "region": Regions.Holes_2_to_5},
    "Hole #5 hole": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 4, "region": Regions.Holes_2_to_5},
    "Hole #6 hole": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 5, "region": Regions.Holes_6_to_9},
    "Hole #7 hole": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 6, "region": Regions.Holes_6_to_9},
    "Hole #8 hole": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 7, "region": Regions.Holes_6_to_9},
    "Hole #9 hole": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 8, "region": Regions.Holes_6_to_9},
    #todo: equally difficult to do miniIsland1 from hole1 or holes 2-5, but the bounty is in frontyard
    "Mini Island Hole #1": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 9, "region": Regions.FrontYard},
    "Mini Island Hole #2": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 10, "region": Regions.Holes_2_to_5},
    "Mini Island Hole #3": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 11, "region": Regions.Holes_6_to_9},
    "Big Bunker Hole": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 12, "region": Regions.Holes_2_to_5},
    "Practice Green Hole #1": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 13, "region": Regions.Hole_1_Area},
    "Practice Green Hole #2": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 14, "region": Regions.Hole_1_Area},
    "Practice Green Hole #3": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 15, "region": Regions.Hole_1_Area},
    "Practice Green Hole #4": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 16, "region": Regions.Hole_1_Area},
    "Practice Green Hole #5": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 17, "region": Regions.Hole_1_Area},
    "Practice Green Hole #6": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 18, "region": Regions.Hole_1_Area},
    "Hole 4 PuttPutt": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 19, "region": Regions.Holes_2_to_5},
    "Hole 5 PuttPutt Ramp": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 20, "region": Regions.Holes_2_to_5},
    "Hole 7 PuttPutt": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 21, "region": Regions.Holes_6_to_9},
    "Hole PuttPutt Dish" : {"id": ID_OFFSET_LOCATION_GOLFHOLE + 22, "region" : Regions.Holes_2_to_5},
    "Hole PuttPutt Pool #1" : {"id": ID_OFFSET_LOCATION_GOLFHOLE + 23, "region" : Regions.Holes_2_to_5},
    "Hole PuttPutt Pool #2": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 24, "region": Regions.Holes_2_to_5},
    "Hole PuttPutt Pool #3": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 25, "region": Regions.Holes_2_to_5},
    "Hole PuttPutt Pool #4": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 26, "region": Regions.Holes_2_to_5},
    "Hole PuttPutt Pool #5": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 27, "region": Regions.Holes_2_to_5},
    "Hole PuttPutt Pool #6": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 28, "region": Regions.Holes_2_to_5},
    "No Cheese Chip Short Hole": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 29, "region": Regions.Holes_6_to_9},
    "No Cheese Chip Middle Hole": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 30, "region": Regions.Holes_6_to_9},
    "No Cheese Chip Tall Hole": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 31, "region": Regions.Holes_6_to_9},
    "Hole PuttPutt Tilted": {"id": ID_OFFSET_LOCATION_GOLFHOLE + 32, "region": Regions.Holes_6_to_9},
}

breakable_signs_data: dict[str, Breakable] = {
    #todo: record what club is needed for each sign from each region.
    #facing holes2-5. doable with wedge from carpark, frontyard, holes2-5, holes6-9, mountaintop.
    #might be possible with a wedge from hole1, very hard. definately iron tho.
    "Car Park Plywood #1": {
        "id": ID_OFFSET_LOCATION_BREAKABLE,
        "region_club_dict": {
            GolfClubs.Wedge: [Regions.CarPark,
                              Regions.FrontYard,
                              Regions.Holes_2_to_5,
                              Regions.Holes_6_to_9,
                              Regions.Mountaintop],
            GolfClubs.Iron: [Regions.Hole_1_Area]}
    },
    #facing house inside holes6-9. doable with wedge from carpark, holes6-9, holes2-5, frontyard. iron hole1.
    "Car Park Plywood #2": {
        "id": ID_OFFSET_LOCATION_BREAKABLE + 1,
        "region_club_dict": {
            GolfClubs.Wedge: [Regions.CarPark,
                              Regions.FrontYard,
                              Regions.Holes_2_to_5,
                              Regions.Holes_6_to_9,
                              Regions.Mountaintop],
            GolfClubs.Iron: [Regions.Hole_1_Area]}
    },
    #facing house inside holes2-5. doable with wedge from carpark, holes2-5, holes6-9, frontyard. iron hole1.
    "Car Park Plywood #3": {
        "id": ID_OFFSET_LOCATION_BREAKABLE + 2,
        "region_club_dict": {
            GolfClubs.Wedge: [Regions.CarPark,
                              Regions.FrontYard,
                              Regions.Holes_2_to_5,
                              Regions.Holes_6_to_9],
            GolfClubs.Iron: [Regions.Hole_1_Area]}
    },
    #front yard, 2-5, 6-9, hole1, mountaintop
    "Meetup Sign Rooftop #1": {
        "id": ID_OFFSET_LOCATION_BREAKABLE + 3,
        "region_club_dict": {
            GolfClubs.Wedge: [Regions.CarPark,
                              Regions.FrontYard,
                              Regions.Hole_1_Area,
                              Regions.Holes_2_to_5,
                              Regions.Holes_6_to_9,
                              Regions.Mountaintop]}
    },
    "Meetup Sign Rooftop #2": {
        "id": ID_OFFSET_LOCATION_BREAKABLE + 4,
        "region_club_dict": {
            GolfClubs.Wedge: [Regions.CarPark,
                              Regions.FrontYard,
                              Regions.Hole_1_Area,
                              Regions.Holes_2_to_5,
                              Regions.Holes_6_to_9,
                              Regions.Mountaintop]}
    },
    #putter mountaintop. wedge carpark, holes2-5, holes6-9. iron frontyard, hole1
    "Meetup Sign Mountaintop #1": {
        "id": ID_OFFSET_LOCATION_BREAKABLE + 5,
        "region_club_dict": {
            GolfClubs.Putter: [Regions.Mountaintop],
            GolfClubs.Wedge: [Regions.CarPark,
                              Regions.Holes_2_to_5,
                              Regions.Holes_6_to_9],
            GolfClubs.Iron: [Regions.FrontYard,
                             Regions.Hole_1_Area]}
    },
    "Meetup Sign Mountaintop #2": {
        "id": ID_OFFSET_LOCATION_BREAKABLE + 6,
        "region_club_dict": {
            GolfClubs.Putter: [Regions.Mountaintop],
            GolfClubs.Wedge: [Regions.CarPark,
                              Regions.Holes_2_to_5,
                              Regions.Holes_6_to_9],
            GolfClubs.Iron: [Regions.FrontYard,
                             Regions.Hole_1_Area]}
    },
    #putter hole1. wedge holes6-9. too many trees for the other regions.
    "Under Construction Sign #1": {
        "id": ID_OFFSET_LOCATION_BREAKABLE + 7,
        "region_club_dict": {
            GolfClubs.Putter: [Regions.Hole_1_Area],
            GolfClubs.Wedge: [Regions.Holes_6_to_9]}
    },
    "Under Construction Sign #2": {
        "id": ID_OFFSET_LOCATION_BREAKABLE + 8,
        "region_club_dict": {
            GolfClubs.Putter: [Regions.Hole_1_Area],
            GolfClubs.Wedge: [Regions.Holes_6_to_9]}
    },

    "Cash Room Plywood": {
        "id": ID_OFFSET_LOCATION_BREAKABLE + 9,
        "region_club_dict": {
            GolfClubs.Wedge: [Regions.ProShop_Upstairs_CashRoom]}
    },
}


'''breakable_statue_data: dict[str, Breakable] = {
    "Statue Block #1" : {"id": ID_OFFSET_LOCATION_BREAKABLE + 9, "region": Regions.Holes_2_to_5},
    "Statue Block #2": {"id": ID_OFFSET_LOCATION_BREAKABLE + 10, "region": Regions.Holes_2_to_5},
    "Statue Block #3": {"id": ID_OFFSET_LOCATION_BREAKABLE + 11, "region": Regions.Holes_2_to_5},
    "Statue Block #4": {"id": ID_OFFSET_LOCATION_BREAKABLE + 12, "region": Regions.Holes_2_to_5},
    "Statue Block #5": {"id": ID_OFFSET_LOCATION_BREAKABLE + 13, "region": Regions.Holes_2_to_5},
    "Statue Block #6": {"id": ID_OFFSET_LOCATION_BREAKABLE + 14, "region": Regions.Holes_2_to_5},
    "Statue Block #7": {"id": ID_OFFSET_LOCATION_BREAKABLE + 15, "region": Regions.Holes_2_to_5},
    "Statue Block #8": {"id": ID_OFFSET_LOCATION_BREAKABLE + 16, "region": Regions.Holes_2_to_5},
}'''

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
        "region": Regions.FrontYard,
        "smallest_club_req": GolfClubs.Wedge,   #TODO Different based on if player has hole1 area unlocked
        "game_id": "Hole1Par"
    },
    "Hole 1 - Birdie": {
        "id": 12003,
        "difficulty": Difficulty.VERY_HARD,
        "region": Regions.FrontYard,
        "smallest_club_req": GolfClubs.Iron,  #TODO Different based on if player has hole1 area unlocked
        "game_id": "Hole1Birdy"
    },
    "Hole 1 - Par Plus": {
        "id": 12002,
        "difficulty": Difficulty.DIFFICULT,
        "region": Regions.FrontYard,
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

