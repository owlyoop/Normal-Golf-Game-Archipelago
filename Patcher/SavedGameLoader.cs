using BepInEx.Logging;
using HarmonyLib;
using Mono.Cecil.Cil;
using NormalGolfArchiProject;
using NormalGolfArchiProject.Archipelago;
using NormalGolfArchiProject.Utils;
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace NormalGolfArchiProject.Patcher
{
	//the long string annoys me so its in a seperate class
	public static class SavedGameLoader
	{
		public static int StartingClub;
		public static int StartingRegion;

		private static bool startsDriver = StartingClub == 4;
		private static bool startsHybrid = StartingClub == 3;
		private static bool startsIron = StartingClub == 2;
		private static bool startsWedge = StartingClub == 1;
		private static bool startsPutter = StartingClub == 0;

		private static int shopInteractEnum = 50000; //Archipelago ID offset for shop locations
		private static int strayCashInteractEnum = 60000; //Archipelago ID offset for stray cash locations
		private static int upstairsCashInteractEnum = 61000;
		public static bool hasOpenedClubPanel = false;

		public static int BountyGoal = 105;


		#region References
		static List<FPSInteractable> shopItems = new List<FPSInteractable>(); //im not using this afaik
		public static Dictionary<int, string> FPSInteractableCachedItems = new Dictionary<int, string>(); //Stores
		public static Dictionary<int, string> strayCashFPSInteractables = new Dictionary<int, string>();
		public static InteractChecker Eye;
		public static ChallengeReminder ChallengeReminder;
		public static SaveManager SaveManager;
		public static Ball ball;
		public static WindPanel wind;

		public static PhysicsMaterial physGreenBase;
		public static PhysicsMaterial physFairwayBase;
		

		static AmbienceManager ambience;
		static AudioSource radio;
		static AudioSource kookaburra;
		static AudioSource shopMusic;
		static float evilKookaburraPitch = 0.4f;
		static float evilkookaburraVolume = 0.32f;
		#endregion

		public static void LoadArchipelagoData()
		{
			var data = ArchipelagoClient.ServerData.SlotData;
			StartingClub = int.Parse(data["starting_club"].ToString());
			BountyGoal = int.Parse(data["req_bounties_to_win"].ToString());
			
			//todo, set new runsavepath
			bool putter = StartingClub == 0;
			bool wedge = StartingClub == 1;
			bool iron = StartingClub == 2;
			bool hybrid = StartingClub == 3;
			bool driver = StartingClub == 4;
			iron = true;	//i cant figure out how to get the clubs panel working if i load the save without the iron. ill just disable the iron later if needed
			Plugin.BepinLogger.LogInfo("Starting club is " + StartingClub);



			//TODO: I am never actually loading the save.
			//I think I got it working to where it saves it in an Archipelago folder so it doesn't overwrite the players saves. i still need to test that more
			//This was copied from the DebugLoadSave func from ILSpy. There's probably a more elegant way to handle saves.
			#region savefile
			string rawSave = "{\"m_playerPosition\":{\"x\":103.63618469238281,\"y\":2.8397185802459719,\"z\":-184.50772094726563}," +
				"\"m_playerRotation\":{\"x\":0.0,\"y\":-0.5088202953338623,\"z\":0.0,\"w\":0.8608728051185608}," +
				"\"m_challengeSetLoaded\":\"ML_Ending\",\"m_currentChallenge\":0,\"bountyAccessLevel\":3," +
				"\"m_completedBounties\":[]," +
				"\"m_savedObjects\":[{\"m_id\":\"bbf1615d-ff17-462b-b829-323d5f2e7371\",\"m_active\":true,\"m_rotation\":{\"x\":0.5608886480331421,\"y\":-0.43053364753723147,\"z\":-0.430385023355484,\"w\":-0.5610823631286621}},{\"m_id\":\"e7cd1c3a-0c07-4dfe-b1d5-c842987f5e15\",\"m_active\":true,\"m_rotation\":{\"x\":0.0,\"y\":0.7072302103042603,\"z\":0.7069833874702454,\"w\":0.0}},{\"m_id\":\"ecc7f5b8-a68a-47c5-9d89-a5429bedfcbb\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"2d4ff2cb-2a4f-49a6-8b95-5da8f942c2cf\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"1a435d4a-4a40-4b31-8be4-72675b46e7d7\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"86f908ab-9443-4e0e-bb14-53c551124f40\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"b0a92a0d-a9ba-4663-99ca-8fe44e4536a6\",\"m_active\":true,\"m_rotation\":{\"x\":-0.4999127686023712,\"y\":0.500087320804596,\"z\":0.4999127686023712,\"w\":0.500087320804596}},{\"m_id\":\"1e1ce95a-af64-4fe7-8c20-2b9b433e5a33\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"c71e6c9b-69c5-450e-b638-7e35b7442df5\",\"m_active\":true,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"731481d5-1293-4a6e-852b-f60b877ee0e0\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"dbf52ef4-46e8-40dd-8cc1-3d555a7e3a12\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"a097f48f-7d2f-41ae-830e-50332b3c490c\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"2ea98dbe-093f-4520-9d4e-f785f1c9b603\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"8fa76193-93b9-4873-8212-4c1f37a63869\",\"m_active\":true,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"3f8d6fb0-eea7-495e-b6a9-2dd71a99781e\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"0fcab7cf-36f7-47c2-a5cb-10c0570d49c5\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"d406fbbd-d5ff-4f43-9ef8-4ce6ba60b76b\",\"m_active\":true,\"m_rotation\":{\"x\":0.3912038207054138,\"y\":0.5890896320343018,\"z\":-0.5888861417770386,\"w\":0.39133885502815249}},{\"m_id\":\"bc623920-c10e-432b-853c-f6ffb8ce35d3\",\"m_active\":true,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"2285e26a-e1ea-4915-b5fb-15d30a550ff1\",\"m_active\":true,\"m_rotation\":{\"x\":-0.4676501452922821,\"y\":-0.530380368232727,\"z\":-0.530380368232727,\"w\":0.4676501452922821}},{\"m_id\":\"86a4ee13-2af1-426b-9c91-f5cda46458c3\",\"m_active\":true,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"d0919af4-d683-484c-8986-ceb79fd9da85\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"93eed31a-74fe-4ca1-8405-4b0a59f2ee0f\",\"m_active\":true,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"324a04dd-2b70-496e-88f0-0a05089f4255\",\"m_active\":true,\"m_rotation\":{\"x\":0.5000000596046448,\"y\":0.4999999701976776,\"z\":-0.5000000596046448,\"w\":0.4999999701976776}},{\"m_id\":\"e9d62ed8-1933-48b8-895a-41ea18ef4ae6\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"c6544730-9924-4e59-b7ff-cab6cdc49995\",\"m_active\":true,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"ee4fe86a-0b64-4017-a40d-c385dc5f0511\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"b1600d52-dd29-424a-8a0e-c4529db10dab\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"de52cdbb-ec41-47aa-a6be-d630fd557da9\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"531dfbc0-7bad-4fd0-9c90-bd0f4d6cd930\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"03458e96-9313-4e68-bf4f-bc0fbe3874b2\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"619ce524-015b-4662-a234-10da79cfaa4f\",\"m_active\":true,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"ca37522b-e4ab-42cd-a035-4c5aacf78415\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"3fc82e96-8c8a-435c-8d1e-7706022cdf2b\",\"m_active\":true,\"m_rotation\":{\"x\":0.0,\"y\":0.7071067094802856,\"z\":-0.7071068286895752,\"w\":0.0}},{\"m_id\":\"01a8023b-a62f-4582-bdf9-9c7029c9a75f\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"1528363c-760f-4a07-ba5f-695e41e95bdd\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"fa6f4baa-9384-4560-8a38-2c0f8776f82b\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"731481d5-1293-4a6e-852b-f60b877ee0e0\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"f5a0374d-699d-402b-8341-9655a50e1e69\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"2fe8ea42-d82d-47ae-8949-14faf1b521b6\",\"m_active\":true,\"m_rotation\":{\"x\":0.560848593711853,\"y\":-0.43056437373161318,\"z\":0.4303542971611023,\"w\":0.5611224174499512}},{\"m_id\":\"d5dd6c85-1cbd-4f6c-8c35-7142b3081cef\",\"m_active\":true,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"4c1bb595-b752-4bea-91ab-eda99425ebfe\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"cdb63e1a-920f-4233-8bd0-1356d7484fda\",\"m_active\":true,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"f02c67cd-22d1-42fc-af3d-cad5015cea99\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"7f3b4ca9-b80c-4dac-8108-9467c49a09bc\",\"m_active\":true,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"03fe7e41-3781-4867-a9f2-865fb7411a02\",\"m_active\":true,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"71cfc2bb-a743-4ccb-be39-68b391f2de05\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}},{\"m_id\":\"c776a3cb-5d94-4c60-8ef9-ce2951991ec8\",\"m_active\":false,\"m_rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0,\"w\":0.0}}]," +
				"\"m_preHitTargets\":[],\"m_canGolf\":true,\"m_golfUnlocked\":true,\"m_spinUnlocked\":true,\"m_aimUnlocked\":true,\"m_stancePanelUnlocked\":true,\"m_windUnlocked\":true," +
				"\"m_ironUnlocked\":false,\"m_putterUnlocked\":false,\"m_driverUnlocked\":false,\"m_wedgeUnlocked\":false,\"m_hybridUnlocked\":false,\"m_foundFirstCash\":false,\"m_bankBalance\":0,\"m_shots\":0,\"m_time\":0,\"seenBulletproof\":false,\"finishedDemo\":false}";
			#endregion

			//set clubs
			rawSave = rawSave
				.Replace("\"m_ironUnlocked\":false", $"\"m_ironUnlocked\":{iron.ToString().ToLower()}")
				.Replace("\"m_putterUnlocked\":false", $"\"m_putterUnlocked\":{putter.ToString().ToLower()}")
				.Replace("\"m_driverUnlocked\":false", $"\"m_driverUnlocked\":{driver.ToString().ToLower()}")
				.Replace("\"m_wedgeUnlocked\":false", $"\"m_wedgeUnlocked\":{wedge.ToString().ToLower()}")
				.Replace("\"m_hybridUnlocked\":false", $"\"m_hybridUnlocked\":{hybrid.ToString().ToLower()}");

			//set player coords based on starting region
			Vector3 startingPos = new Vector3(-134.9768f, 9.9882f, 39.1788f);
			Vector3 startingViewPos = Vector3.zero;

			StartingRegion = int.Parse(data["starting_region"].ToString());
			Plugin.BepinLogger.LogInfo("Starting Region is: " + StartingRegion);
			switch (StartingRegion)
			{
				case 0:
					startingPos = new Vector3(69.551f, 5.2834f, -367.2121f);
					break;
				case 1:
					startingPos = new Vector3(48.1098f, 4.7228f, -318.9951f);
					break;
				case 4:
					startingPos = new Vector3(23.85f, 8.0577f, -221.059f);
					break;
				case 5:
					startingPos = new Vector3(322.9053f, 44.9822f, -343.5749f);
					break;
				case 6:
					startingPos = new Vector3(-221.8353f, 8.9257f, -574.2776f);
					break;
				case 666:
					startingPos = new Vector3(-134.9768f, 9.9882f, 39.1788f);
					break;
			}

			rawSave = rawSave.Replace(	"\"m_playerPosition\":{\"x\":103.63618469238281,\"y\":2.8397185802459719,\"z\":-184.50772094726563}",
										$"\"m_playerPosition\":{{\"x\":{startingPos.x},\"y\":{startingPos.y},\"z\":{startingPos.z}}}");
			
			//SavePath = SaveManager.instance.m_backupSavePath + "Archipelago/run2.txt";
			Plugin.BepinLogger.LogInfo("Writing save data");
			Directory.CreateDirectory(SaveManager.instance.m_backupSavePath + "Archipelago");

			File.WriteAllText(Plugin.SavePath, rawSave);
			//File.WriteAllText(SaveManager.instance.m_runSavePath, rawSave);

			Plugin.BepinLogger.LogInfo("Loading scene");


			SceneManager.LoadScene("Main");
			
		}

		public static void OnSceneLoaded(Scene scene, LoadSceneMode mode)
		{
			if (scene.name == "Main")
			{
				Plugin.BepinLogger.LogInfo("OnSceneLoaded called");
				//InitializeWorld();
			}
		}

		public static void InitializeWorld()
		{
			Plugin.BepinLogger.LogInfo("InitializeWorld called");
			LockAllBounties();
			CloseAllGates();
			CloseAllProShopDoors();
			CloseAllShedDoors();
			SetClubs();
			SetupProShop();
			SetupAllStrayCash();
			SetupBreakables();
			RemoveCashRewards();
			PreparePhysicsMaterials();
			PrepareAudioReferences();

			foreach (var item in Plugin.ArchipelagoClient.session.Items.AllItemsReceived)
			{
				int id = (int)item.ItemId;
				if (id >= 1000 && id < 2000) Plugin.ReceiveRegionUnlockItem(id);
				else if (id >= 600 && id <= 608) Plugin.ReceiveDifficultyUnlockItem(id);
				else if (id >= 2 && id <= 8) Plugin.ReceiveMiscItem(id);
				else if (id >= 2000 && id <= 2009) Plugin.ReceiveCashItem(id);
			}

			//UnlockStartingDifficulties();

			Eye = GameObject.Find("___PLAYER/First Person Character/Eye").GetComponent<InteractChecker>();
			ChallengeReminder = GameObject.Find("___PLAYER/First Person Character/Eye/Camera/Canvas/CHALLENGEREMINDER").GetComponent<ChallengeReminder>();
			SaveManager = GameObject.Find("__Managers House/SaveManager").GetComponent<SaveManager>();

			wind = GameObject.Find("PANEL_Wind").GetComponent<WindPanel>();

			CreateMountaintopGate();
		}

		public static void LockAllBounties()
		{
			//!!!Bountys/Pads/
			GameObject bountyParent = GameObject.Find("!!!Bountys/Pads/");
			GameObject parPadsParent = GameObject.Find("!!!Bountys/ParPads/");
			GameObject specialPadsParent = GameObject.Find("!!!Bountys/Special Pads/");

			var bounties = bountyParent.GetComponentsInChildren<BountyPad>(true);
			foreach(var b in bounties)
			{
				if (b == null) continue;
				b.gameObject.SetActive(true);
				b.m_padThatIsUnlocked = null;
				b.SetLock(false, b);
			}

			var parBounties = parPadsParent.GetComponentsInChildren<BountyPad>(true);
			foreach (var b in parBounties)
			{
				if (b == null) continue;
				b.gameObject.SetActive(true);
				b.m_padThatIsUnlocked = null;
				b.SetLock(false, b);
			}
			var specialBounties = specialPadsParent.GetComponentsInChildren<BountyPad>(true);
			foreach (var b in specialBounties)
			{
				if (b == null) continue;
				b.gameObject.SetActive(true);
				b.m_padThatIsUnlocked = null;
				b.SetLock(false, b);
			}

			Plugin.BepinLogger.LogInfo("Locked all bounties");
		}

		public static void UnlockStartingDifficulties()
		{
			if (Plugin.ArchipelagoClient.HasItemReceived(600))
				Plugin.UnlockAllBountiesByDifficulty(Difficulty.SuperEasy);

			if (Plugin.ArchipelagoClient.HasItemReceived(601))
				Plugin.UnlockAllBountiesByDifficulty(Difficulty.Easy);

			if (Plugin.ArchipelagoClient.HasItemReceived(602))
				Plugin.UnlockAllBountiesByDifficulty(Difficulty.Medium);

			if (Plugin.ArchipelagoClient.HasItemReceived(603))
				Plugin.UnlockAllBountiesByDifficulty(Difficulty.KindaHard);

			if (Plugin.ArchipelagoClient.HasItemReceived(604))
				Plugin.UnlockAllBountiesByDifficulty(Difficulty.Hard);

			if (Plugin.ArchipelagoClient.HasItemReceived(605))
				Plugin.UnlockAllBountiesByDifficulty(Difficulty.VeryHard);

			if (Plugin.ArchipelagoClient.HasItemReceived(606))
				Plugin.UnlockAllBountiesByDifficulty(Difficulty.Nightmare);

			if (Plugin.ArchipelagoClient.HasItemReceived(607))
				Plugin.UnlockAllBountiesByDifficulty(Difficulty.SuperNightmare);

			if (Plugin.ArchipelagoClient.HasItemReceived(608))
				Plugin.UnlockAllBountiesByDifficulty(Difficulty.ActuallyImpossible);

			var items = Plugin.ArchipelagoClient.session.Items.AllItemsReceived;

			foreach(var i in items)
			{
				Plugin.BepinLogger.LogInfo(i.ItemName);
			}
		}

		/// <summary>
		/// Manually closes all the gates inbetween regions. Does not include teleporter sheds or pro shop doors
		/// </summary>
		public static void CloseAllGates()
		{
			GameObject gatesParent = GameObject.Find("3D Course/Props/GATES/");

			for (int i = 0; i < gatesParent.transform.childCount; i++)
			{
				var child = gatesParent.transform.GetChild(i);
				Plugin.BepinLogger.LogInfo(child.name);

				if (child.name == "Hole6Gate")
				{
					var g1 = child.Find("gate1_LOD0 (2)").transform;
					g1.localRotation = Quaternion.Euler(g1.eulerAngles.x, 0, g1.eulerAngles.z);
					//Plugin.BepinLogger.LogInfo(g1.parent.name + " " + g1.name);

					var g2 = child.Find("gate2_LOD0 (2)").transform;
					g2.localRotation = Quaternion.Euler(g2.eulerAngles.x, 0, g2.eulerAngles.z);
					//Plugin.BepinLogger.LogInfo(g2.parent.name + " " + g2.name);
				}
				else if (child.name == "DrivewayGate")
				{
					var g1 = child.Find("gate1_LOD0").transform;
					g1.localRotation = Quaternion.Euler(g1.eulerAngles.x, 0, g1.eulerAngles.z);
					//Plugin.BepinLogger.LogInfo(g1.parent.name + " " + g1.name);

					var g11 = child.Find("gate1_LOD0 (1)").transform;
					g11.localRotation = Quaternion.Euler(g11.eulerAngles.x, 0, g11.eulerAngles.z);
					//Plugin.BepinLogger.LogInfo(g11.parent.name + " " + g11.name);

					var g2 = child.Find("gate2_LOD0").transform;
					g2.localRotation = Quaternion.Euler(g2.eulerAngles.x, 0, g2.eulerAngles.z);
					//Plugin.BepinLogger.LogInfo(g2.parent.name + " " + g2.name);

					var g21 = child.Find("gate2_LOD0 (1)").transform;
					g21.localRotation = Quaternion.Euler(g21.eulerAngles.x, 0, g21.eulerAngles.z);
					//Plugin.BepinLogger.LogInfo(g21.parent.name + " " + g21.name);
				}
				else
				{
					var g1 = child.Find("gate1_LOD0").transform;
					g1.localRotation = Quaternion.Euler(g1.eulerAngles.x, 0, g1.eulerAngles.z);
					//Plugin.BepinLogger.LogInfo(g1.parent.name + " " + g1.name);

					var g2 = child.Find("gate2_LOD0").transform;
					g2.localRotation = Quaternion.Euler(g2.eulerAngles.x, 0, g2.eulerAngles.z);
					//Plugin.BepinLogger.LogInfo(g2.parent.name + " " + g2.name);
				}
			}
		}

		public static void CloseAllShedDoors()
		{
			//hole3 shed door
			var shed3door = GameObject.Find("3D Course/Buildings/Hole3Shed/SM_TinShed_Door").transform;
			shed3door.localRotation = Quaternion.Euler(shed3door.eulerAngles.x, 0, shed3door.eulerAngles.z);

			//hole5 shed door
			var shed5door = GameObject.Find("3D Course/Buildings/Hole5Shed/SM_TinShed_Door").transform;
			shed5door.localRotation = Quaternion.Euler(shed5door.eulerAngles.x, 0, shed5door.eulerAngles.z);

			//frontyard shed door
			var fyShedDoor = GameObject.Find("3D Course/Buildings/miniShed/SM_TinShed_Door").transform;
			fyShedDoor.localRotation = Quaternion.Euler(fyShedDoor.eulerAngles.x, 0, fyShedDoor.eulerAngles.z);

			//hole9 shed
			var shed9door = GameObject.Find("3D Course/Buildings/miniShed (1)/SM_TinShed_Door").transform;
			shed9door.localRotation = Quaternion.Euler(shed9door.eulerAngles.x, 0, shed9door.eulerAngles.z);

			GameObject.Find("3D Course/PRO SHOP/PROPS/Teleporter").SetActive(false);
			GameObject.Find("3D Course/Buildings/Hole5Shed/Teleporter (1)").SetActive(false);

			GameObject.Find("3D Course/Buildings/miniShed/Hole1ShedATeleporter").SetActive(false);
			GameObject.Find("3D Course/Buildings/Hole3Shed/TeleporterHole3").SetActive(false);
		}

		public static void CloseAllProShopDoors()
		{
			var shopOpen = GameObject.Find("3D Course/PRO SHOP/!!!SAVED OBJECTS/ShopDoorOPEN");
			shopOpen.SetActive(false);

			var shopClosed = GameObject.Find("3D Course/PRO SHOP/!!!SAVED OBJECTS/ShopDoorCLOSED");
			shopClosed.SetActive(true);


			//bathroom teleporter door
			var bathroom = GameObject.Find("3D Course/PRO SHOP/PROPS/Dynamic/SM_Door").transform;
			bathroom.localRotation = Quaternion.Euler(bathroom.eulerAngles.x, 90f, bathroom.eulerAngles.z);

			//shop counter
			var counter = GameObject.Find("3D Course/PRO SHOP/PROPS/Dynamic/BarDoor").transform;
			counter.localRotation = Quaternion.Euler(-90f, counter.eulerAngles.y, counter.eulerAngles.z);

			//lukes office
			var office = GameObject.Find("3D Course/PRO SHOP/PROPS/Dynamic/LockRoom").transform;
			office.localRotation = Quaternion.Euler(270f, 0f, 0f);

			//greenscreen building
			var greenDoor = GameObject.Find("3D Course/Buildings/marketingdpt2/SM_SlidingDoor");
			greenDoor.SetActive(true);
			GameObject.Find("3D Course/Buildings/marketingdpt2/PROPS").SetActive(true);
			//3D Course/Buildings/marketingdpt2/PROPS/server/Interact (1)

			//cash room
			var cashDoor = GameObject.Find("3D Course/PRO SHOP/PROPS/Dynamic/CashRoom").transform;
			cashDoor.localRotation = Quaternion.Euler(270f, 180f, 0f);

			//padlock room
			var lockDoor = GameObject.Find("3D Course/PRO SHOP/PROPS/Dynamic/MysteryRoom").transform;
			lockDoor.localRotation = Quaternion.Euler(270f, 90f, 0f);

			//simulator room
			var simDoor = GameObject.Find("3D Course/PRO SHOP/PROPS/Dynamic/OfficeDoorPADLOCKED").transform;
			simDoor.localRotation = Quaternion.Euler(270f, 0f, 0f);


		}

		public static void SetClubs()
		{
			var panel = GameObject.Find("PANEL_ClubsAndMore").GetComponent<ClubsPanelNavigation>();
			Plugin.BepinLogger.LogInfo("Set Clubs Ahhh " + panel.name);
			panel.Unlock(true);

			//disable club buttons except the starting ones
			SelectableClub driver = GameObject.Find("PANEL_ClubsAndMore/Canvas/FRAME/Content/Clubs/Unlocked/List/Content/Driver").GetComponent<SelectableClub>();
			Plugin.BepinLogger.LogInfo("Set Clubs driver ahhh " + driver.name);
			driver.SetLockedState(StartingClub == 4);
			driver.Unselect();

			SelectableClub hybrid = GameObject.Find("PANEL_ClubsAndMore/Canvas/FRAME/Content/Clubs/Unlocked/List/Content/Hybrid").GetComponent<SelectableClub>();
			Plugin.BepinLogger.LogInfo("Set Clubs hybrid ahhh " + hybrid.name);
			hybrid.SetLockedState(StartingClub == 3);
			hybrid.Unselect();

			SelectableClub iron = GameObject.Find("PANEL_ClubsAndMore/Canvas/FRAME/Content/Clubs/Unlocked/List/Content/7 Iron").GetComponent<SelectableClub>();
			Plugin.BepinLogger.LogInfo("Set Clubs iron ahhh " + iron.name);
			iron.SetLockedState(StartingClub == 2);
			iron.Unselect();

			SelectableClub wedge = GameObject.Find("PANEL_ClubsAndMore/Canvas/FRAME/Content/Clubs/Unlocked/List/Content/Wedge").GetComponent<SelectableClub>();
			Plugin.BepinLogger.LogInfo("Set Clubs wedge ahhh " + wedge.name);
			wedge.SetLockedState(StartingClub == 1);
			wedge.Unselect();

			SelectableClub putter = GameObject.Find("PANEL_ClubsAndMore/Canvas/FRAME/Content/Clubs/Unlocked/List/Content/Putter").GetComponent<SelectableClub>();
			Plugin.BepinLogger.LogInfo("Set Clubs putter ahhh " + putter.name);
			putter.SetLockedState(StartingClub == 0);
			putter.Unselect();


			var selectClub = GameObject.Find("PANEL_ClubsAndMore/Canvas/FRAME/Content/Clubs").GetComponent<SelectClub>();
			Plugin.BepinLogger.LogInfo("select club " + selectClub.name);
			selectClub.Start();
			selectClub.SelectNextClub(true);
			//selectClub.SelectAClub(Clubs.Driver);
		}

		/// <summary>
		/// Handles all of the shop item triggers
		/// </summary>
		public static void SetupProShop()
		{
			//todo: disable 'out of stock' sign things
			string clubsParent = "3D Course/PRO SHOP/PROPS/CLUBS/";

			//dunno if ill need to store the shop items later 
			var putter = SetupShopItem(clubsParent, "SM_Putter", "/Interact");
			var wedge = SetupShopItem(clubsParent, "SM_Wedge", "/Interact (2)");
			var hybrid = SetupShopItem(clubsParent, "SM_Hybrid", "/Interact (2)");
			var driver = SetupShopItem(clubsParent, "SM_Driver", "/Interact (1)");
			var lmugcTicket = SetupShopItem(clubsParent, "lmugcTicket", "/Interact (1)");
			var crowbar = SetupShopItem(clubsParent, "crowbar", "/Interact (1)");

			string ticketsParent = "3D Course/PRO SHOP/PROPS/SHELF/";
			var shelf = GameObject.Find(ticketsParent);
			shelf.SetActive(true);

			//there are two tickets with the same name 'mulliganTicket'
			var holeDupe = GameObject.Find(ticketsParent + "holeSkipT");
			holeDupe.SetName("holeSkipT_dupe");


			string ticketSuffix = "/Trigger";
			
			var ticketMull = SetupShopItem(ticketsParent, "mulliganTicket", ticketSuffix);
			var ticketMull1 = SetupShopItem(ticketsParent, "mulliganTicket (1)", ticketSuffix);
			var ticketMull2 = SetupShopItem(ticketsParent, "mulliganTicket (2)", ticketSuffix);
			var ticketMull3 = SetupShopItem(ticketsParent, "mulliganTicket (3)", ticketSuffix);
			var ticketMull4 = SetupShopItem(ticketsParent, "mulliganTicket (4)", ticketSuffix);
			var ticketMull5 = SetupShopItem(ticketsParent, "mulliganTicket (5)", ticketSuffix);

			var ticketHole = SetupShopItem(ticketsParent, "holeSkipT", ticketSuffix);
			var ticketHole1 = SetupShopItem(ticketsParent, "holeSkipT (1)", ticketSuffix);
			var ticketHole2 = SetupShopItem(ticketsParent, "holeSkipT (2)", ticketSuffix);
			var ticketHole3 = SetupShopItem(ticketsParent, "holeSkipT (3)", ticketSuffix);
			var ticketHoleDupe = SetupShopItem(ticketsParent, "holeSkipT_dupe", ticketSuffix);

			var ticketWind = SetupShopItem(ticketsParent, "nowindTicket", ticketSuffix);
			var ticketWind1 = SetupShopItem(ticketsParent, "nowindTicket (1)", ticketSuffix);
			var ticketWind2 = SetupShopItem(ticketsParent, "nowindTicket (2)", ticketSuffix);
			var ticketWind3 = SetupShopItem(ticketsParent, "nowindTicket (3)", ticketSuffix);
		}

		/// <summary>
		/// Helper function for SetupProShop
		/// </summary>
		/// <param name="goParent"></param>
		/// <param name="goItem"></param>
		/// <param name="goTrigger"></param>
		/// <returns></returns>
		static FPSInteractable SetupShopItem(string goParent, string goItem, string goTrigger)
		{
			var item = GameObject.Find(goParent + goItem + goTrigger).GetComponent<FPSInteractable>();
			item.gameObject.SetActive(true);
			item.transform.parent.gameObject.SetActive(true);
			item.m_interaction = (InteractionType)shopInteractEnum;
			shopInteractEnum++;
			shopItems.Add(item);
			return item;
		}

		public static void SetupAllStrayCash()
		{
			//3D Course / CASH / NAME / Mesh / Trigger name.FpsInteractable



			/*
			 * all paths are like: 3D Course / CASH / 100(1) / Mesh / Trigger
			 * 
			 * except for 50 which is: 3D Course/CASH/50/Mesh/TriggerIgnoreWalls
			 * and 100 (7) which is: 3D Course/CASH/100 (7)/Mesh/IgnoreWalls
			 * 
			//name	sibling index	location
			50			0			pro shop shelf
			full path: 3D Course/CASH/50/Mesh/TriggerIgnoreWalls

			100			1			pro shop cash register
			100			2			pro shop boxes (behind counter)
			100 (1)		3			practice putt (hole1)
			100 (2)		4			hole 3 picnic table
			100 (3)		5			hole 4 no swimming sign
			100 (4)		6			tunnel rocks 1
			100 (5)		7			tunnel rocks 2
			100 (6)		8			inside greenscreen building

			100 (7)		9			driveway picket fence (can be collected from holes 6-9 and holes 2-5)
			3D Course/CASH/100 (7)/Mesh/IgnoreWalls

			100 (8)		10			mountainside bunker door
			100 (9)		11			hole 6 rocks 1
			100 (10)	12			hole 6 rocks 2
			upstairs???

			lake teleporter shed cash in completely different location
			3D Course/Buildings/miniShed (1)/100 (5)/Mesh/IgnoreWalls

			todo: if i ever add that greenscreen building as a location, thats what cash 100 (6) is.
			*/


			string cashParent = "3D Course/CASH/";
			string suffix = "/Mesh/Trigger"; //the suffix of the path for all cash except 50, 100 (7), and the teleport shed cash

			var dupeCash = GameObject.Find(cashParent + "100"); //two of the cash items have the same exact name and im using Gameobject.Find like a criminal
			dupeCash.SetName("100_dupe");


			var cash0 = SetupFPSInteractable(cashParent, "50", "/Mesh/TriggerIgnoreWalls");
			var cash1 = SetupFPSInteractable(cashParent, "100", suffix);
			var cash2 = SetupFPSInteractable(cashParent, "100_dupe", suffix);
			var cash3 = SetupFPSInteractable(cashParent, "100 (1)", suffix);
			var cash4 = SetupFPSInteractable(cashParent, "100 (2)", suffix);
			var cash5 = SetupFPSInteractable(cashParent, "100 (3)", suffix);
			var cash6 = SetupFPSInteractable(cashParent, "100 (4)", suffix);
			var cash7 = SetupFPSInteractable(cashParent, "100 (5)", suffix);
			var cash8 = SetupFPSInteractable(cashParent, "100 (7)", "/Mesh/IgnoreWalls");
			var cash9 = SetupFPSInteractable(cashParent, "100 (8)", suffix);
			var cash10 = SetupFPSInteractable(cashParent, "100 (9)", suffix);
			var cash11 = SetupFPSInteractable(cashParent, "100 (10)", suffix);
			var cash12 = SetupFPSInteractable(cashParent, "100 (6)", suffix);
			var cash13 = SetupFPSInteractable("3D Course/Buildings/miniShed (1)/", "100 (5)", "/Mesh/IgnoreWalls");

			var ball = SetupFPSInteractable("3D Course/PRO SHOP/PROPS/Static/", "missingBall", "/Trigger");
			var button = SetupFPSInteractable("3D Course/PRO SHOP/Upstairs/Office/", "bunkerTerminalButtonOnly", "/Interact (1)");

			//upstairs cash
			string upCashParent = "3D Course/CASH/upstairs/";
			string upCashSuffix = "/IgnroeWalls"; //ingame is a typo
			string upCashSuffix2 = "/Mesh/Trigger";
			var ucash0 = SetupUpstairsCash(upCashParent, "moneyStack", upCashSuffix);
			var ucash1 = SetupUpstairsCash(upCashParent, "moneyStack (1)", upCashSuffix);
			var ucash2 = SetupUpstairsCash(upCashParent, "moneyStack (2)", upCashSuffix);
			var ucash3 = SetupUpstairsCash(upCashParent, "moneyStack (3)", upCashSuffix);
			var ucash4 = SetupUpstairsCash(upCashParent, "moneyStack (4)", upCashSuffix);
			var ucash5 = SetupUpstairsCash(upCashParent, "moneyStack (5)", upCashSuffix);
			var ucash6 = SetupUpstairsCash(upCashParent, "moneyStack (6)", upCashSuffix);

			var ucash_4 = SetupUpstairsCash(upCashParent, "CASH (4)", upCashSuffix2);
			var ucash_5 = SetupUpstairsCash(upCashParent, "CASH (5)", upCashSuffix2);
			var ucash_6 = SetupUpstairsCash(upCashParent, "CASH (6)", upCashSuffix2);
			var ucash_7 = SetupUpstairsCash(upCashParent, "CASH (7)", upCashSuffix2);
			var ucash_8 = SetupUpstairsCash(upCashParent, "CASH (8)", upCashSuffix2);
			var ucash_9 = SetupUpstairsCash(upCashParent, "CASH (9)", upCashSuffix2);
			var ucash_10 = SetupUpstairsCash(upCashParent, "CASH (10)", upCashSuffix2);
			var ucash_11 = SetupUpstairsCash(upCashParent, "CASH (11)", upCashSuffix2);
			var ucash_12 = SetupUpstairsCash(upCashParent, "CASH (12)", upCashSuffix2);

		}

		/// <summary>
		/// Edits the m_interaction enum of the FPSInteractable to align with the archipelago location ID
		/// </summary>
		/// <param name="goParent">String of the path that precedes the item name. Should end in a slash / </param>
		/// <param name="goCash"></param>
		/// <param name="goFPS">String of the path after the item name, should begin with a slash / </param>
		/// <returns></returns>
		static FPSInteractable SetupFPSInteractable(string goParent, string goCash, string goFPS)
		{
			var cash = GameObject.Find(goParent + goCash + goFPS).GetComponent<FPSInteractable>();
			//Plugin.BepinLogger.LogInfo(cash.name);
			cash.gameObject.SetActive(true);
			cash.m_interaction = (InteractionType)strayCashInteractEnum;
			strayCashInteractEnum++;
			return cash;
		}

		static FPSInteractable SetupUpstairsCash(string goParent, string goCash, string goFPS)
		{
			var cash = GameObject.Find(goParent + goCash + goFPS).GetComponent<FPSInteractable>();
			//Plugin.BepinLogger.LogInfo(cash.name);
			cash.gameObject.SetActive(true);
			cash.m_interaction = (InteractionType)upstairsCashInteractEnum;
			upstairsCashInteractEnum++;
			return cash;
		}


		static void SetupBreakables()
		{
			string plyboardParent = "3D Course/Props/Car Park/";
			string suffix = "/Board";

			var board1 = GameObject.Find(plyboardParent + "plyboard" + suffix);
			Plugin.BepinLogger.LogInfo(board1.name);
			board1.SetActive(true);

			var board2 = GameObject.Find(plyboardParent + "plyboard (2)" + suffix);
			Plugin.BepinLogger.LogInfo(board2.name);
			board2.SetActive(true);

			var board3 = GameObject.Find(plyboardParent + "plyboard (5)" + suffix);
			Plugin.BepinLogger.LogInfo(board3.name);
			board3.SetActive(true);

			string signsParent = "3D Course/Props/Car Park/Signs/";

			var mu1a = GameObject.Find(signsParent + "MeetUp1/MU1a");
			Plugin.BepinLogger.LogInfo(mu1a.name);
			mu1a.SetActive(true);

			var mu1b = GameObject.Find(signsParent + "MeetUp1/MU1b");
			Plugin.BepinLogger.LogInfo(mu1b.name);
			mu1b.SetActive(true);

			var mu2a = GameObject.Find(signsParent + "MeetUp2/MU2a");
			Plugin.BepinLogger.LogInfo(mu2a.name);
			mu2a.SetActive(true);

			var mu2b = GameObject.Find(signsParent + "MeetUp2/MU2b");
			Plugin.BepinLogger.LogInfo(mu2b.name);
			mu2b.SetActive(true);

			var con1 = GameObject.Find(signsParent + "Construction/1");
			Plugin.BepinLogger.LogInfo(con1.name);
			con1.SetActive(true);

			var con2 = GameObject.Find(signsParent + "Construction/2");
			Plugin.BepinLogger.LogInfo(con2.name);
			con2.SetActive(true);

			var board4 = GameObject.Find("3D Course/PRO SHOP/PROPS/Dynamic/plyboard/Board");
			board4.transform.parent.SetName("plyboard_cashroom");
			Plugin.BepinLogger.LogInfo(board4.name);
			board4.SetActive(true);
		}

		/// <summary>
		/// Remove the cash rewards completing a bounty gives you
		/// </summary>
		static void RemoveCashRewards()
		{
			var manager = GameObject.Find("!!!Bountys").GetComponent<BountyBalancer>();
			foreach(var difficulty in manager.m_difficultyMats)
			{
				difficulty.reward = 0;
			}
			//todo: remove cash reward text from bountypads?
		}

		static void CreateMountaintopGate()
		{
			var gate = GameObject.Find("3D Course/Props/GATES/Hole1Gate");
			var mtGate = GameObject.Instantiate(gate);
			mtGate.SetName("MountaintopGate");
			mtGate.transform.SetParent(GameObject.Find("3D Course/Props/GATES").transform);

			mtGate.transform.position = new Vector3(29.3348f, 18.2192f, -464.4035f);
			mtGate.transform.localRotation = Quaternion.Euler(0, 60f, 0);
			mtGate.transform.localScale = new Vector3(1.5f, 1.5f, 1.5f);
			
			var p6 = GameObject.Find("3D Course/Props/GATES/MountaintopGate/picketPost (6)");
			var p7 = GameObject.Find("3D Course/Props/GATES/MountaintopGate/picketPost (7)");

			var g1 = GameObject.Find("3D Course/Props/GATES/MountaintopGate/gate1_LOD0");
			var g2 = GameObject.Find("3D Course/Props/GATES/MountaintopGate/gate2_LOD0");

			var padlock1 = GameObject.Find("3D Course/Props/GATES/MountaintopGate/padlock2 (1)");
			var padlock2 = GameObject.Find("3D Course/Props/GATES/MountaintopGate/padlock2");
			GameObject.Destroy(padlock1);
			GameObject.Destroy(padlock2);

			p6.transform.position = new Vector3(34.0603f, 18.2868f, -472.2803f);
			p6.transform.localPosition = new Vector3(6.1228f, 0.0451f, 0.1027f);

			p7.transform.position = new Vector3(29.3127f, 15.4686f, -464.1548f);
			p7.transform.localPosition = new Vector3(-0.151f, -1.8337f, 0.0701f);
			p7.transform.localScale = new Vector3(100f, 100f, 200f);

			g1.transform.position = new Vector3(33.8288f, 18.2192f, -472.1873f);
			g1.transform.localPosition = new Vector3(5.992f, 0f, 0f);
			g1.transform.localRotation = Quaternion.Euler(270f, 0f, 0f); //y rot 75f open

			g2.transform.position = new Vector3(29.3348f, 18.2192f, -464.4035f);
			g2.transform.localPosition = new Vector3(0f, 0f, 0f);
			g2.transform.localRotation = Quaternion.Euler(90f, 0f, 0f); //y rot 285f open
			g2.transform.localScale = new Vector3(-100f, -100f, -100f);
		}

		static void PreparePhysicsMaterials()
		{
			ball = GameObject.Find("/Ball").GetComponent<Ball>();
			Plugin.BepinLogger.LogInfo(ball.name);
			physGreenBase = new PhysicsMaterial();
			physGreenBase = ball.m_physics[2];
			physFairwayBase = new PhysicsMaterial();
			physFairwayBase = ball.m_physics[1];
			BallPhysicsTraps.InitializePhysicsMaterials();
		}

		static void PrepareBreakables()
		{
			string plyboardParent = "3D Course/PROPS/Car Park";
			var plyboard1 = GameObject.Find(plyboardParent + "/plyboard/Board");
			plyboard1.SetActive(true);

			var plyboard2 = GameObject.Find(plyboardParent + "/plyboard (2)/Board");
			plyboard2.SetActive(true);

			var plyboard3 = GameObject.Find(plyboardParent + "/plyboard (5)/Board");
			plyboard3.SetActive(true);

			string signsParent = "3D Course/Props/Car Park/Signs";
			var meetup1a = GameObject.Find(signsParent + "/MeetUp1/MU1a");
			var meetup1b = GameObject.Find(signsParent + "/MeetUp1/MU1b");
			meetup1a.SetActive(true);
			meetup1b.SetActive(true);

			var meetup2a = GameObject.Find(signsParent + "/MeetUp2/MU2a");
			var meetup2b = GameObject.Find(signsParent + "/MeetUp2/MU2b");
			meetup2a.SetActive(true);
			meetup2b.SetActive(true);

			var construction1 = GameObject.Find(signsParent + "/Construction/1");
			var construction2 = GameObject.Find(signsParent + "/Construction/2");
			construction1.SetActive(true);
			construction2.SetActive(true);
		}

		static void PrepareAudioReferences()
		{
			ambience = GameObject.Find("__Managers House/Audio Manager/AmbienceManager").GetComponent<AmbienceManager>();
			var sounds = ambience.gameObject.GetComponents<AudioSource>();

			foreach(var sound in sounds)
			{
				if(sound.clip.name == "kooky")
				{
					kookaburra = sound;
				}
			}

			radio = GameObject.Find("__Managers House/Audio Manager/RadioController").GetComponent<AudioSource>();
			shopMusic = GameObject.Find("__Managers House/Audio Manager/MUSICAREA").GetComponent<MusicArea>().m_music;
		}

		public static void SetMusicPitchLow()
		{
			radio.pitch = 0.64f;
			shopMusic.pitch = 0.6f;
		}

		public static void SetMusicPitchHigh()
		{
			radio.pitch = 1.64f;
			shopMusic.pitch = 2f;
		}

		public static void MakeKookaburraEvil()
		{
			kookaburra.pitch = 0.4f;
			kookaburra.volume = 0.28f;
		}

		

	}
}
