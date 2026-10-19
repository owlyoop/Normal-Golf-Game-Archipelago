# **There is a risk of your save files being overwritten. Backup your saves before using this mod!**
> C:\Users\[YOUR USERNAME]\AppData\LocalLow\Luke Muscat\Normal Golf Game

I tried to make it so it loads & saves the files in Normal Golf Game\Archipelago, but there are no guarantees it works.  

## **This is a very early version of an Archipelago randomizer mod for Normal Golf Game**

There will be many problems. Do not use this expecting to complete the game without running into issues.

Currently the only objective is to complete X amount of bounties. There are plans to include LMUGC as a goal in the future. There are barely any features as my goal was to release a functional version before overwhelming myself with numerous options.

### The current yaml options:  
- Starting region  
* Starting club  
* Number of starting bounty difficulties  
* Number of bounties required to win

### Currently implemented locations:  
- All 105 bounties
* Purchasing shop items

### Currently implemented items:  
- Any of the 5 clubs  
* Unlocking all bounties of a specific difficulty  
* Unlocking gates/teleporter shed doors/pro shop door  
* Cash items, including a filler 50$ item  

### Known issues:  
- World generation can fail, I suspect it is caused when all of the bounties in the starting region are locked due to none of the starting bounty difficulties lining up.  
* Mountaintop region unimplemented.  
* Bounties don't get locked if they are impossible to complete with the player's currently unlocked clubs.   
* Bounties are accessed by the sibling index in the !!!Bounties gameobject, this will certainly break if the game gets updated or if other mods mess with the bounty ordering.
* Starting region numbers in options.py are weird since I was using them for indexing purposes.  
* The apworld py files are messy and unorganized.  

### Special thanks to:  
- Luke Muscat for creating a wonderful game.  
* The Archipelago team for having great resources on learning how to create apworlds, the APQuest documentation was especially useful https://github.com/ItsSeafoamy/Once-Upon-an-Archipelago  
* alwaysintreble for creating the Unity plugin client template https://github.com/alwaysintreble/ArchipelagoBepInExPluginTemplate  
* ItsSeafoamy for their Archipelago mod for Once Upon a Katamari, and KitLemonfoot and thearst3rd for their Archipelago mod for Marble it up Ultra.  
I used these mods for reference on implementing the unity side of things. https://github.com/ItsSeafoamy/Once-Upon-an-Archipelago https://github.com/KitLemonfoot/ArchipelagoMIUU  
* Uroogla for their Spyro 3 Archipelago mod, which was a useful reference for creating the apworld https://github.com/Uroogla/S3AP  

