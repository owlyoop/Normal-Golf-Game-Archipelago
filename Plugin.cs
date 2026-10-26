using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using NormalGolfArchiProject.Archipelago;
using NormalGolfArchiProject.Patcher;
using NormalGolfArchiProject.Utils;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UIElements;


namespace NormalGolfArchiProject;

[BepInPlugin(PluginGUID, PluginName, PluginVersion)]
public class Plugin : BaseUnityPlugin
{
    public const string PluginGUID = "com.yourName.projectName";
    public const string PluginName = "NormalGolfArchiProject";
    public const string PluginVersion = "0.0.1";

    public const string ModDisplayInfo = $"{PluginName} v{PluginVersion}";
    private const string APDisplayInfo = $"Archipelago v{ArchipelagoClient.APVersion}";
    public static ManualLogSource BepinLogger;
    public static ArchipelagoClient ArchipelagoClient;

	public static string SavePath;
	public static string SavePathBackup;

	Harmony Harmony;

	public static readonly ConcurrentQueue<int> ItemQueue = new ConcurrentQueue<int>();

	private void Awake()
    {
        // Plugin startup logic
        BepinLogger = Logger;
        ArchipelagoClient = new ArchipelagoClient();
        ArchipelagoConsole.Awake();

        ArchipelagoConsole.LogMessage($"{ModDisplayInfo} loaded!");

		Harmony.CreateAndPatchAll(typeof(IngamePatcher));
		Harmony.CreateAndPatchAll(typeof(SaveManager_WriteSave_Prefix));
		Harmony.CreateAndPatchAll(typeof(SaveManager_LoadStoryRun_Prefix));
		Harmony.CreateAndPatchAll(typeof(BallPhysicsPatcher));
		if (ArchipelagoClient.Authenticated && ArchipelagoClient.session != null)
		{
			
		}

		SavePath = Application.persistentDataPath + "/" + "Archipelago/run2.txt";
		SavePathBackup = Application.persistentDataPath + "/" + "Archipelago/run2_temp.txt";
		Directory.CreateDirectory(Application.persistentDataPath + "/" + "Archipelago");
	}

	private void Update()
	{
		while (ItemQueue.TryDequeue(out int num))
		{
			if (num >= 4000)
				ReceiveTrapItem(num);
			else if (num >= 3000)
				ReceiveFillerItem(num);
			else if (num >= 2000)
				ReceiveCashItem(num);
			else if (num >= 1000)
				ReceiveRegionUnlockItem(num);
			else if (num >= 600)
				ReceiveDifficultyUnlockItem(num);
			else
				ReceiveMiscItem(num);
		}
	}



	private void OnDestroy()
	{
		//SceneManager.sceneLoaded -= SavedGameLoader.OnSceneLoaded;
	}
    private void OnGUI()
    {
        // show the mod is currently loaded in the corner
        GUI.Label(new Rect(16, 16, 300, 20), ModDisplayInfo);
        ArchipelagoConsole.OnGUI();

        string statusMessage;
        // show the Archipelago Version and whether we're connected or not
        if (ArchipelagoClient.Authenticated)
        {
            // if your game doesn't usually show the cursor this line may be necessary
            // Cursor.visible = false;

            statusMessage = " Status: Connected";
            GUI.Label(new Rect(16, 50, 300, 20), APDisplayInfo + statusMessage);
        }
        else
        {
            // if your game doesn't usually show the cursor this line may be necessary
            // Cursor.visible = true;

            statusMessage = " Status: Disconnected";
            GUI.Label(new Rect(16, 50, 300, 20), APDisplayInfo + statusMessage);
            GUI.Label(new Rect(16, 70, 150, 20), "Host: ");
            GUI.Label(new Rect(16, 90, 150, 20), "Player Name: ");
            GUI.Label(new Rect(16, 110, 150, 20), "Password: ");

            ArchipelagoClient.ServerData.Uri = GUI.TextField(new Rect(150, 70, 150, 20),
                ArchipelagoClient.ServerData.Uri);
            ArchipelagoClient.ServerData.SlotName = GUI.TextField(new Rect(150, 90, 150, 20),
                ArchipelagoClient.ServerData.SlotName);
            ArchipelagoClient.ServerData.Password = GUI.TextField(new Rect(150, 110, 150, 20),
                ArchipelagoClient.ServerData.Password);

            // requires that the player at least puts *something* in the slot name
            if (GUI.Button(new Rect(16, 130, 100, 20), "Connect") &&
                !ArchipelagoClient.ServerData.SlotName.IsNullOrWhiteSpace())
            {
                ArchipelagoClient.Connect();
            }
        }
		// this is a good place to create and add a bunch of debug buttons
	}

	public static void MainMenu()
	{
		
		var playButton = GameObject.Find("Main Menu").GetComponent<MainMenu2>().m_playButton;
		BepinLogger.LogInfo(playButton.name);
		playButton.onClick.RemoveAllListeners();

		BepinLogger.LogInfo(playButton.onClick.GetCallsCount());
		

		playButton.onClick.AddListener(SavedGameLoader.LoadArchipelagoData);
		BepinLogger.LogInfo(playButton.onClick.GetCallsCount());
		GameObject.Find("Main Menu/MainFrame/PlayButton/Menu Button/LABEL").GetComponent<TextMeshProUGUI>().text = "Play Archipelago";

		SceneManager.sceneLoaded += SavedGameLoader.OnSceneLoaded;
	}

	public static void ReceiveCashItem(int id)
	{
		switch (id)
		{
			case 2000:
				ProgressManager.instance.m_bank.ChangeBalance(50, halfSound: true, fast: true);
				break;

			case 2001:
				ProgressManager.instance.m_bank.ChangeBalance(75, halfSound: true, fast: true);
				break;

			case 2002:
				ProgressManager.instance.m_bank.ChangeBalance(100, halfSound: true, fast: true);
				break;

			case 2003:
				ProgressManager.instance.m_bank.ChangeBalance(125, halfSound: true, fast: true);
				break;

			case 2004:
				ProgressManager.instance.m_bank.ChangeBalance(150, halfSound: true, fast: true);
				break;

			case 2005:
				ProgressManager.instance.m_bank.ChangeBalance(200, halfSound: true, fast: true);
				break;

			case 2006:
				ProgressManager.instance.m_bank.ChangeBalance(400, halfSound: true, fast: true);
				break;

			case 2007:
				ProgressManager.instance.m_bank.ChangeBalance(600, halfSound: true, fast: true);
				break;

			case 2008:
				ProgressManager.instance.m_bank.ChangeBalance(800, halfSound: true, fast: true);
				break;

			case 2009:
				ProgressManager.instance.m_bank.ChangeBalance(1000, halfSound: true, fast: true);
				break;
		}
	}

	public static void ReceiveRegionUnlockItem(int id)
	{
		if (SceneManager.GetActiveScene().name != "Main") return;
		//kinda hard-coding this because alot of gates/doors have slightly differing requirements as to how to 'open' them.
		//todo: hide padlocks
		switch (id) 
		{
			case 1000:  //car park <-> front yard
				Plugin.BepinLogger.LogInfo("Opening gates for Car Park <-> Front Yard");
				var cpFyG1 = GameObject.Find("3D Course/Props/GATES/SecurityGates/gate1_LOD0").transform;
				cpFyG1.localRotation = Quaternion.Euler(cpFyG1.eulerAngles.x, 75f, cpFyG1.eulerAngles.z);

				var cpFyG2 = GameObject.Find("3D Course/Props/GATES/SecurityGates/gate2_LOD0").transform;
				cpFyG2.localRotation = Quaternion.Euler(cpFyG2.eulerAngles.x, 285f, cpFyG2.eulerAngles.z);
				break;

			case 1001:  //car park <-> holes 2-5
				Plugin.BepinLogger.LogInfo("Opening gates for Car Park <-> Holes 2-5");
				var cpH2G1 = GameObject.Find("3D Course/Props/GATES/DrivewayGate/gate1_LOD0").transform;
				cpH2G1.localRotation = Quaternion.Euler(cpH2G1.eulerAngles.x, 285f, cpH2G1.eulerAngles.z);
				var cpH2G2 = GameObject.Find("3D Course/Props/GATES/DrivewayGate/gate2_LOD0").transform;
				cpH2G2.localRotation = Quaternion.Euler(cpH2G2.eulerAngles.x, 70f, cpH2G2.eulerAngles.z);
				break;

			case 1002:  //pro shop door
				Plugin.BepinLogger.LogInfo("Opening Pro Shop door");
				var shopdoor = GameObject.Find("3D Course/PRO SHOP/!!!SAVED OBJECTS/ShopDoorOPEN");
				shopdoor.SetActive(true);

				var shopdoorClosed = GameObject.Find("3D Course/PRO SHOP/!!!SAVED OBJECTS/ShopDoorCLOSED");
				shopdoorClosed.SetActive(false);
				break;

			case 1003:  //front yard <-> hole1
				Plugin.BepinLogger.LogInfo("Opening gates for Front Yard <-> Hole 1");
				var fyH1G1 = GameObject.Find("3D Course/Props/GATES/Hole1Gate/gate1_LOD0").transform;
				fyH1G1.localRotation = Quaternion.Euler(fyH1G1.eulerAngles.x, 285f, fyH1G1.eulerAngles.z);

				var fyH1G2 = GameObject.Find("3D Course/Props/GATES/Hole1Gate/gate2_LOD0").transform;
				fyH1G2.localRotation = Quaternion.Euler(fyH1G2.eulerAngles.x, 70f, fyH1G2.eulerAngles.z);
				break;

			case 1004:  //front yard <-> holes6-9
				Plugin.BepinLogger.LogInfo("Opening gates for Front Yard <-> Holes 6-9");
				var fyH9G1 = GameObject.Find("3D Course/Props/GATES/Hole9Gate/gate1_LOD0").transform;
				fyH9G1.localRotation = Quaternion.Euler(fyH9G1.eulerAngles.x, 285f, fyH9G1.eulerAngles.z);

				var fyH9G2 = GameObject.Find("3D Course/Props/GATES/Hole9Gate/gate2_LOD0").transform;
				fyH9G2.localRotation = Quaternion.Euler(fyH9G2.eulerAngles.x, 70f, fyH9G2.eulerAngles.z);
				break;

			case 1005:  //front yard <-> teleport #2B shed door
				Plugin.BepinLogger.LogInfo("Opening Front Yard teleporter shed door");
				var fyTpShed = GameObject.Find("3D Course/Buildings/miniShed/SM_TinShed_Door").transform;
				fyTpShed.localRotation = Quaternion.Euler(fyTpShed.eulerAngles.x, 100f, fyTpShed.eulerAngles.z);
				break;

			case 1006:  //pro shop upstairs access
				Plugin.BepinLogger.LogInfo("Opening pro shop upstairs access");
				var shopCounter = GameObject.Find("3D Course/PRO SHOP/PROPS/Dynamic/BarDoor").transform;
				shopCounter.localRotation = Quaternion.Euler(88.0601f, shopCounter.eulerAngles.y, shopCounter.eulerAngles.z);
				break;

			case 1007:  //pro shop bathroom
				Plugin.BepinLogger.LogInfo("Opening pro shop bathroom door");
				var shopBathroom = GameObject.Find("3D Course/PRO SHOP/PROPS/Dynamic/SM_Door").transform;
				shopBathroom.localRotation = Quaternion.Euler(shopBathroom.eulerAngles.x, 352.344f, shopBathroom.eulerAngles.z);
				break;

			case 1008:  //hole 1 <-> holes 2-5
				Plugin.BepinLogger.LogInfo("Opening gates for Hole 1 <-> Holes 2-5");
				var H1H2G1 = GameObject.Find("3D Course/Props/GATES/Hole2Gate/gate1_LOD0").transform;
				H1H2G1.localRotation = Quaternion.Euler(H1H2G1.eulerAngles.x, 75f, H1H2G1.eulerAngles.z);

				var H1H2G2 = GameObject.Find("3D Course/Props/GATES/Hole2Gate/gate2_LOD0").transform;
				H1H2G2.localRotation = Quaternion.Euler(H1H2G2.eulerAngles.x, 285f, H1H2G2.eulerAngles.z);
				break;

			case 1009:  //holes 2-5 <-> holes 6-9
				Plugin.BepinLogger.LogInfo("Opening Hole 6 Gate");
				var hole6Gate1 = GameObject.Find("3D Course/Props/GATES/Hole6Gate/gate1_LOD0").transform;
				hole6Gate1.localRotation = Quaternion.Euler(hole6Gate1.eulerAngles.x, 75f, hole6Gate1.eulerAngles.z);

				var hole6Gate2 = GameObject.Find("3D Course/Props/GATES/Hole6Gate/gate2_LOD0").transform;
				hole6Gate2.localRotation = Quaternion.Euler(hole6Gate2.eulerAngles.x, 285f, hole6Gate2.eulerAngles.z);
				break;

			case 1010:  //holes 2-5 <-> holes 6-9 (driveway gate)
				Plugin.BepinLogger.LogInfo("Opening Driveway Gates for Holes 2-5 <-> Holes 6-9");
				var drivewayGate1 = GameObject.Find("3D Course/Props/GATES/DrivewayGate/gate1_LOD0 (1)").transform;
				drivewayGate1.localRotation = Quaternion.Euler(drivewayGate1.eulerAngles.x, 285f, drivewayGate1.eulerAngles.z);

				var drivewayGate2 = GameObject.Find("3D Course/Props/GATES/DrivewayGate/gate2_LOD0 (1)").transform;
				drivewayGate2.localRotation = Quaternion.Euler(drivewayGate2.eulerAngles.x, 75f, drivewayGate2.eulerAngles.z);
				break;

			case 1011:  //teleporter #2A shed door
				Plugin.BepinLogger.LogInfo("Opening shed door for Teleport #2A");
				var shed2A = GameObject.Find("3D Course/Buildings/Hole3Shed/SM_TinShed_Door").transform;
				shed2A.localRotation = Quaternion.Euler(shed2A.eulerAngles.x, 179f, shed2A.eulerAngles.z);
				break;

			case 1012:  //teleporter #3 shed door
				Plugin.BepinLogger.LogInfo("Opening shed door for Lake Area");
				var shed3 = GameObject.Find("3D Course/Buildings/miniShed (1)/SM_TinShed_Door").transform;
				shed3.localRotation = Quaternion.Euler(shed3.eulerAngles.x, 134f, shed3.eulerAngles.z);
				break;

			case 1013:  //mountaintop gate
				Plugin.BepinLogger.LogInfo("Opening gate for MountainTop <-> holes 6-9");
				var mtGate1 = GameObject.Find("3D Course/Props/GATES/MountaintopGate/gate1_LOD0").transform;
				mtGate1.localRotation = Quaternion.Euler(270f, 75f, 0f);
				var mtGate2 = GameObject.Find("3D Course/Props/GATES/MountaintopGate/gate2_LOD0").transform;
				mtGate2.localRotation = Quaternion.Euler(90f, 285f, 0f);
				break;

			case 1014:  //unlock teleporter 1
				Plugin.BepinLogger.LogWarning("Unlocking Teleporter #1 panel (UNIMPLEMENTED)");
				break;

			case 1015:  //unlock teleporter 2
				Plugin.BepinLogger.LogWarning("Unlocking Teleporter #2 panel (UNIMPLEMENTED)");
				break;

			case 1016: //green screen building
				var greenDoor = GameObject.Find("3D Course/Buildings/marketingdpt2/SM_SlidingDoor");
				greenDoor.SetActive(false);
				break;

			case 1017: //luke's office
				var office = GameObject.Find("3D Course/PRO SHOP/PROPS/Dynamic/LockRoom").transform;
				office.localRotation = Quaternion.Euler(270f, 194f, 0f);
				break;

			case 1018: //cash room
				var cashDoor = GameObject.Find("3D Course/PRO SHOP/PROPS/Dynamic/CashRoom").transform;
				cashDoor.localRotation = Quaternion.Euler(270f, 300f, 0f);
				break;

			case 1019: //padlock room
				var lockDoor = GameObject.Find("3D Course/PRO SHOP/PROPS/Dynamic/MysteryRoom").transform;
				lockDoor.localRotation = Quaternion.Euler(270f, 190f, 0f);
				break;

			case 1020: //simulator room
				var simDoor = GameObject.Find("3D Course/PRO SHOP/PROPS/Dynamic/OfficeDoorPADLOCKED").transform;
				simDoor.localRotation = Quaternion.Euler(270f, 120f, 0f);
				break;

			default:
				Plugin.BepinLogger.LogWarning("Received invalid ID in ReceiveRegionUnlockItem: " + id);
				break;
		}
	}

	public static void ReceiveDifficultyUnlockItem(int id)
	{
		if (SceneManager.GetActiveScene().name != "Main") return;
		Difficulty difficulty = Difficulty.SuperEasy;
		switch (id)
		{
			case 600:
				difficulty = Difficulty.SuperEasy;
				break;
			case 601:
				difficulty = Difficulty.Easy;
				break;
			case 602:
				difficulty = Difficulty.Medium;
				break;
			case 603:
				difficulty = Difficulty.KindaHard;
				break;
			case 604:
				difficulty = Difficulty.Hard;
				break;
			case 605:
				difficulty = Difficulty.VeryHard;
				break;
			case 606:
				difficulty = Difficulty.Nightmare;
				break;
			case 607:
				difficulty = Difficulty.SuperNightmare;
				break;
			case 608:
				difficulty = Difficulty.ActuallyImpossible;
				break;

			default:
				Plugin.BepinLogger.LogError("Received invalid ID for ReceiveDifficultyUnlockItem: " + id);
				break;
		}

		UnlockAllBountiesByDifficulty(difficulty);

	}

	public static void ReceiveMiscItem(int id)
	{
		//todo: make queue thing for items received outside of game ahhhh
		if (SceneManager.GetActiveScene().name != "Main") return;
		switch (id)
		{
			case 2: //putter
				var putter = GameObject.Find("PANEL_ClubsAndMore/Canvas/FRAME/Content/Clubs/Unlocked/List/Content/Putter").GetComponent<SelectableClub>();
				putter.SetLockedState(true);
				break;

			case 3: //wedge
				var wedge = GameObject.Find("PANEL_ClubsAndMore/Canvas/FRAME/Content/Clubs/Unlocked/List/Content/Wedge").GetComponent<SelectableClub>();
				wedge.SetLockedState(true);
				break;

			case 4: //iron
				var iron = GameObject.Find("PANEL_ClubsAndMore/Canvas/FRAME/Content/Clubs/Unlocked/List/Content/7 Iron").GetComponent<SelectableClub>();
				iron.SetLockedState(true);
				break;

			case 5: //hybrid
				var hybrid = GameObject.Find("PANEL_ClubsAndMore/Canvas/FRAME/Content/Clubs/Unlocked/List/Content/Hybrid").GetComponent<SelectableClub>();
				hybrid.SetLockedState(true);
				break;

			case 6: //driver
				var driver = GameObject.Find("PANEL_ClubsAndMore/Canvas/FRAME/Content/Clubs/Unlocked/List/Content/Driver").GetComponent<SelectableClub>();
				driver.SetLockedState(true);
				break;

			case 7: //todo: practice panel
				break;
		}
	}

	public static void ReceiveFillerItem(int id)
	{
		if (SceneManager.GetActiveScene().name != "Main") return;
		switch (id)
		{
			case 3000:	//filler $50
				ProgressManager.instance.m_bank.ChangeBalance(50, halfSound: true, fast: true);
				break;

			case 3001:  //music pitch down
				SavedGameLoader.SetMusicPitchLow();
				break;

			case 3002:  //music pitch up
				SavedGameLoader.SetMusicPitchHigh();
				break;
		}
	}

	private void ReceiveTrapItem(int id)
	{
		if (SceneManager.GetActiveScene().name != "Main") return;
		switch (id)
		{
			case 4000: //icy green
				BallPhysicsTraps.ActivateIcyGreen(60f);
				break;

			case 4001: //icy fairway
				BallPhysicsTraps.ActivateIcyFairway(60f);
				break;

			case 4002: //bouncy fairway
				BallPhysicsTraps.ActivateBouncyGreen(60f);
				break;

			case 4003: //bouncy fairway
				BallPhysicsTraps.ActivateBouncyFairway(60f);
				break;

			case 4004: //accelerated fairway
				BallPhysicsTraps.ActivateAcceleratedFairwayTrap(60f);
				break;

			case 4005: //evil kookaburra
				SavedGameLoader.MakeKookaburraEvil();
				break;
		}
	}

	public static void UnlockAllBountiesByDifficulty(Difficulty difficulty)
	{
		if (SceneManager.GetActiveScene().name != "Main") return;


		Plugin.BepinLogger.LogInfo("Unlocking All Bounties: " + difficulty.ToString());

		GameObject bountyParent = GameObject.Find("!!!Bountys/Pads");
		var bounties = bountyParent.GetComponentsInChildren<BountyPad>(true);
		GameObject parPadsParent = GameObject.Find("!!!Bountys/ParPads");
		var parPads = parPadsParent.GetComponentsInChildren<BountyPad>(true);
		GameObject specialPadsParent = GameObject.Find("!!!Bountys/Special Pads");
		var specialPads = specialPadsParent.GetComponentsInChildren<BountyPad>(true);
		foreach (var b in bounties)
		{
			//Plugin.BepinLogger.LogInfo("bounties " + b.name);
			if (b.m_bountyChallengeSet.difficulty == difficulty)
			{
				//Plugin.BepinLogger.LogInfo("Setlock " + b.name);
				b.SetLock(true, b);
				/*foreach (var u in b.m_unlocked)
					u.SetActive(true);
				foreach (var l in b.m_locked)
					l.SetActive(false);*/
			}
		}
		foreach (var b in parPads)
		{
			//Plugin.BepinLogger.LogInfo("parpads " + b.name);
			if (b.m_bountyChallengeSet.difficulty == difficulty)
			{
				//Plugin.BepinLogger.LogInfo("Setlock " + b.name);
				b.SetLock(true, b);
				/*foreach (var u in b.m_unlocked)
					u.SetActive(true);
				foreach (var l in b.m_locked)
					l.SetActive(false);*/
			}
		}
		foreach (var b in specialPads)
		{
			//Plugin.BepinLogger.LogInfo("specialpads " + b.name);
			if (b.m_bountyChallengeSet.difficulty == difficulty)
			{
				//Plugin.BepinLogger.LogInfo("Setlock " + b.name);
				b.SetLock(true, b);
				/*foreach (var u in b.m_unlocked)
					u.SetActive(true);
				foreach (var l in b.m_locked)
					l.SetActive(false);*/
			}
		}
	}
}