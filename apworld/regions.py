from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import APNormalGolfWorld

class Regions:

    CarPark = "Car Park"
    FrontYard = "Front Yard"
    ProShop = "Pro Shop"
    ProShop_Upstairs = "Pro Shop Upstairs"
    Hole_1_Area = "Hole 1 Area"
    Holes_2_to_5 = "Holes 2-5"
    Holes_6_to_9 = "Holes 6-9"
    LakeArea = "Lake Area"
    Mountaintop = "Mountaintop"


# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


def create_and_connect_regions(world: APNormalGolfWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: APNormalGolfWorld) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    car_park = Region("Car Park", world.player, world.multiworld)
    front_yard = Region("Front Yard", world.player, world.multiworld)
    pro_shop = Region("Pro Shop", world.player, world.multiworld)
    pro_shop_upstairs = Region("Pro Shop Upstairs", world.player, world.multiworld)
    hole_1_area = Region("Hole 1 Area", world.player, world.multiworld)
    holes_2_to_5 = Region("Holes 2-5", world.player, world.multiworld)
    holes_6_to_9 = Region("Holes 6-9", world.player, world.multiworld)

    lake_area = Region("Lake Area", world.player, world.multiworld)

    mountaintop = Region("Mountaintop", world.player, world.multiworld)

    teleporter_1a_shed = Region("Teleporter #1A Shed", world.player, world.multiworld)
    teleporter_1b_bathroom = Region("Teleporter #1B Bathroom", world.player, world.multiworld)

    teleporter_2b_shed = Region("Teleporter #2B Shed", world.player, world.multiworld)
    teleporter_2a_shed = Region("Teleporter #2A Shed", world.player, world.multiworld)

    teleporter_3a_shed = Region("Teleporter #3A Shed", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [car_park, front_yard, pro_shop, pro_shop_upstairs, hole_1_area, holes_2_to_5, holes_6_to_9,
               teleporter_1b_bathroom, teleporter_1a_shed,
               teleporter_2b_shed, teleporter_2a_shed,
               teleporter_3a_shed, lake_area,
               mountaintop]

    # Some regions may only exist if the player enables certain options.


    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: APNormalGolfWorld) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    car_park = world.get_region("Car Park")
    front_yard = world.get_region("Front Yard")
    pro_shop = world.get_region("Pro Shop")
    pro_shop_upstairs = world.get_region("Pro Shop Upstairs")
    hole_1_area = world.get_region("Hole 1 Area")
    holes_2_to_5 = world.get_region("Holes 2-5")
    holes_6_to_9 = world.get_region("Holes 6-9")

    teleporter_1b_bathroom = world.get_region("Teleporter #1B Bathroom")
    teleporter_1a_shed = world.get_region("Teleporter #1A Shed")

    teleporter_2a_shed = world.get_region("Teleporter #2A Shed")
    teleporter_2b_shed = world.get_region("Teleporter #2B Shed")

    teleporter_3a_shed = world.get_region("Teleporter #3A Shed")
    lake_area = world.get_region("Lake Area")

    mountaintop = world.get_region("Mountaintop")

    #car park connections
    car_park.connect(front_yard, "Car Park to Front Yard",
                     lambda state: state.has("Unlock Car Park Gate to Front Yard", world.player))
    front_yard.connect(car_park, "Front Yard to Car Park",
                     lambda state: state.has("Unlock Car Park Gate to Front Yard", world.player))

    car_park.connect(holes_2_to_5, "Holes 2-5 Area Gate to Car Park",
                     lambda state: state.has("Unlock Car Park Gate to Holes 2-5", world.player))
    holes_2_to_5.connect(car_park, "Car Park Gate to Holes 2-5 Area",
                     lambda state: state.has("Unlock Car Park Gate to Holes 2-5", world.player))

    #front yard connections
    front_yard.connect(pro_shop, "Door to Pro Shop",
                       lambda state: state.has("Unlock Pro Shop Door", world.player))
    pro_shop.connect(front_yard, "Door out of Pro Shop",
                       lambda state: state.has("Unlock Pro Shop Door", world.player))

    front_yard.connect(hole_1_area, "Front Yard Gate to Hole 1 Area",
                       lambda state: state.has("Unlock Front Yard Gate to Hole 1", world.player))
    hole_1_area.connect(front_yard, "Hole 1 Area Gate to Front Yard",
                       lambda state: state.has("Unlock Front Yard Gate to Hole 1", world.player))

    front_yard.connect(holes_6_to_9, "Front Yard Gate to Holes 6-9 Area",
                       lambda state: state.has("Unlock Front Yard Gate to Holes 6-9", world.player))
    holes_6_to_9.connect(front_yard, "Holes 6-9 Area to Front Yard",
                       lambda state: state.has("Unlock Front Yard Gate to Holes 6-9", world.player))

    front_yard.connect(teleporter_2b_shed, "Front Yard to Teleporter #2B Shed",
                       lambda state: state.has("Unlock Front Yard Teleporter #2B Shed", world.player))
    teleporter_2b_shed.connect(front_yard, "Teleporter #2B Shed to Front Yard",
                       lambda state: state.has("Unlock Front Yard Teleporter #2B Shed", world.player))


    #Pro Shop connections
    pro_shop.connect(pro_shop_upstairs, "Pro Shop Upstairs",
                     lambda state: state.has("Unlock Pro Shop Upstairs", world.player))
    pro_shop_upstairs.connect(pro_shop, "Pro Shop Downstairs",
                     lambda state: state.has("Unlock Pro Shop Upstairs", world.player))

    pro_shop.connect(teleporter_1b_bathroom, "Teleporter #1B Bathroom",
                     lambda state: state.has("Unlock Pro Shop Bathroom Door", world.player))
    teleporter_1b_bathroom.connect(pro_shop, "Teleporter #1B Bathroom Exit",
                     lambda state: state.has("Unlock Pro Shop Bathroom Door", world.player))

    teleporter_1b_bathroom.connect(teleporter_1a_shed, "Teleporter #1 Bathroom to Shed",
                                   lambda state: state.has("Unlock Teleporter #1", world.player))
    teleporter_1a_shed.connect(teleporter_1b_bathroom, "Teleporter #1 Shed to Bathroom",
                                   lambda state: state.has("Unlock Teleporter #1", world.player))


    #Hole 1 connections
    hole_1_area.connect(holes_2_to_5, "Hole 1 Gate to Holes 2-5 Area",
                        lambda state: state.has("Unlock Hole 1 Gate to Holes 2-5", world.player))
    holes_2_to_5.connect(hole_1_area, "Holes 2-5 Area Gate to Hole 1",
                        lambda state: state.has("Unlock Hole 1 Gate to Holes 2-5", world.player))


    #Holes 2-5 connections
    holes_2_to_5.connect(holes_6_to_9, "Hole 5 Gate to Hole 6",
                         lambda state: state.has("Unlock Hole 6 Gate", world.player))
    holes_6_to_9.connect(holes_2_to_5, "Holes 6 Gate to Hole 5",
                         lambda state: state.has("Unlock Hole 6 Gate", world.player))

    holes_2_to_5.connect(holes_6_to_9, "Driveway Gate to Holes 6-9 Area",
                         lambda state: state.has("Unlock Driveway Gate to Holes 6-9", world.player))
    holes_6_to_9.connect(holes_2_to_5, "Driveway Gate to Holes 2-5 Area",
                         lambda state: state.has("Unlock Driveway Gate to Holes 6-9", world.player))

    holes_2_to_5.connect(teleporter_2a_shed, "Holes 2-5 to Teleporter #2A Shed",
                         lambda state: state.has("Unlock Teleporter #2A Shed", world.player))
    teleporter_2a_shed.connect(holes_2_to_5, "Teleporter #2A Shed to Holes 2-5",
                         lambda state: state.has("Unlock Teleporter #2A Shed", world.player))

    teleporter_2a_shed.connect(teleporter_2b_shed, "Teleporter #2 2A-2B",
                               lambda state: state.has("Unlock Teleporter #2", world.player))
    teleporter_2b_shed.connect(teleporter_2a_shed, "Teleporter #2 2B-2A",
                               lambda state: state.has("Unlock Teleporter #2", world.player))


    #Holes 6-9 connections
    holes_6_to_9.connect(teleporter_3a_shed, "Holes 6-9 to Teleporter #3 Shed",
                         lambda state: state.has("Unlock Teleporter #3 Shed", world.player))
    teleporter_3a_shed.connect(holes_6_to_9, "Teleporter #3 Shed to Holes 6-9",
                         lambda state: state.has("Unlock Teleporter #3 Shed", world.player))

    holes_6_to_9.connect(mountaintop, "Holes 6-9 Mountaintop path",
                         lambda state: state.has("Unlock Gate to Mountaintop", world.player))
    mountaintop.connect(holes_6_to_9, "Mountaintop path to Holes 6-9",
                         lambda state: state.has("Unlock Gate to Mountaintop", world.player))

    teleporter_3a_shed.connect(lake_area, "Teleporter #3 Shed to Lake Area",
                               lambda state: state.has("Unlock Teleporter #3 Shed", world.player))
    lake_area.connect(teleporter_3a_shed, "Lake Area to Teleporter #3 Shed",
                               lambda state: state.has("Unlock Teleporter #3 Shed", world.player))

    # todo: look into how one-way connections are made. player can fall from mountaintop to holes 2-5 or 6-9
    mountaintop_oneway_holes_2_5 = Entrance(world.player, "Mountaintop drop-down to Holes 2-5", parent=mountaintop)
    mountaintop.exits.append(mountaintop_oneway_holes_2_5)
    mountaintop_oneway_holes_2_5.connect(holes_2_to_5)

    mountaintop_oneway_holes_6_9 = Entrance(world.player, "Mountaintop drop-down to Holes 6-9", parent=mountaintop)
    mountaintop.exits.append(mountaintop_oneway_holes_6_9)
    mountaintop_oneway_holes_6_9.connect(holes_6_to_9)

    pro_shop_oneway_front_yard = Entrance(world.player, "Upstairs Pro Shop drop-down to Front Yard", parent=pro_shop_upstairs)
    pro_shop_upstairs.exits.append(pro_shop_oneway_front_yard)
    pro_shop_oneway_front_yard.connect(front_yard)
