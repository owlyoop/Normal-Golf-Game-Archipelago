//using App.
using Archipelago.MultiClient.Net.Models;
using BepInEx.Logging;
using HarmonyLib;
using I2.Loc.SimpleJSON;
using NormalGolfArchiProject;
using NormalGolfArchiProject.Archipelago;
using NormalGolfArchiProject.Utils;
using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Text;
using UnityEngine;
using UnityEngine.SceneManagement;
using Utilities;

namespace NormalGolfArchiProject.Patcher
{
	public class IngamePatcher
	{
		[HarmonyPostfix]
		[HarmonyPatch(typeof(MainMenu), "Start")]
		private static void MainMenu_Start_PostFix(MainMenu __instance)
		{
			//var obj = gameobject.find() find the play button to duplicate it
			//GameObject.Instantiate clone

			//change clone button stuff, txt and position
			// button.onClick = new Button.ButtonClickedEvent();
			//interactable = ArchipelagoClient.Authenticated;
		}

		[HarmonyPostfix]
		[HarmonyPatch(typeof(BountyPad), nameof(BountyPad.Complete))]
		private static void BountyPad_Complete_Postfix(BountyPad __instance)
		{
			Plugin.BepinLogger.LogInfo($"Bounty completed: {__instance.name}");
			int value = BountyBalancer.instance.GetDifficultyValue(__instance.m_bountyChallengeSet.difficulty);

			// send your AP check here
			//gets the ID (game_data.py) from the bounty. ID uses the sibling index
			int prefix = 10000;
			int suffix = __instance.gameObject.transform.GetSiblingIndex();

			var parent = __instance.gameObject.transform.GetParent();

			if (parent.name == "Pads") prefix = 10000;
			else if (parent.name == "Special Pads") prefix = 11000;
			else if (parent.name == "ParPads") prefix = 12000;
			else
			{
				Plugin.BepinLogger.LogWarning($"Invalid Parent for: {__instance.name}" + " , parent is " + parent.name);
			}

			var result = Plugin.ArchipelagoClient.SendCheck(prefix + suffix);
			if (result)
			{
				Plugin.BepinLogger.LogInfo("Sending check " + (prefix + suffix));
				//ProgressManager.instance.m_bank.ChangeBalance(-value, halfSound: false, fast: true);
			}

			SavedGameLoader.ChallengeReminder.SetString("test");
		}

		[HarmonyPostfix]
		[HarmonyPatch(typeof(FPSInteractable), nameof(FPSInteractable.GetPrompt))]
		private static void FPSInteractable_GetPrompt_Postfix(FPSInteractable __instance, ref string __result)
		{
			if (__instance.m_interaction >= (InteractionType)50000 && __instance.m_interaction <= (InteractionType)50020)
			{
				var ie = SavedGameLoader.Eye;
				ie.m_usePrompt.SetActive(true);
				var session = Plugin.ArchipelagoClient.session;
				long[] ids = new[] { (long)__instance.m_interaction };
				int id = (int)ids[0];
				if (!SavedGameLoader.FPSInteractableCachedItems.ContainsKey(id))
				{
					Dictionary<long, ScoutedItemInfo> scouts = session.Locations.ScoutLocationsAsync(false, ids).Result;
					SavedGameLoader.FPSInteractableCachedItems[id] = scouts[(long)__instance.m_interaction].ItemName;
				}

				ie.m_useText.text.text = "Buy: " + SavedGameLoader.FPSInteractableCachedItems[(int)__instance.m_interaction];

				ie.m_costAnim.SetText(Loc.GetString("Price") + ": <color=#00FF00><wave>$" + __instance.m_cashValue.ToString("N0") + "</wave></color>");
			}
			else if (__instance.m_interaction >= (InteractionType)60000 && __instance.m_interaction < (InteractionType)69999)
			{
				var ie = SavedGameLoader.Eye;
				ie.m_usePrompt.SetActive(true);
				var session = Plugin.ArchipelagoClient.session;
				long[] ids = new[] { (long)__instance.m_interaction };
				int id = (int)ids[0];
				if (!SavedGameLoader.strayCashFPSInteractables.ContainsKey(id))
				{
					Dictionary<long, ScoutedItemInfo> scouts = session.Locations.ScoutLocationsAsync(false, ids).Result;
					SavedGameLoader.strayCashFPSInteractables[id] = scouts[(long)__instance.m_interaction].ItemName;
				}
				ie.m_useText.text.text = "Collect: " + SavedGameLoader.strayCashFPSInteractables[(int)__instance.m_interaction];
			}
		}

		[HarmonyPostfix]
		[HarmonyPatch(typeof(InteractChecker), nameof(InteractChecker.CheckForInteractions))]
		private static void InteractChecker_CheckForInteractions_Postfix(InteractChecker __instance)
		{
			//code copied from CheckForInteractions. Sorry if this is illegal
			//couldn't figure out how to keep m_costPrompt active without doing this
			Collider[] array = Physics.OverlapSphere(__instance.transform.position, 0.09f, __instance._layerMask);
			foreach (Collider item in array)
			{
				__instance.m_frameCols.Add(item);
			}
			if (Physics.Raycast(__instance.transform.position, __instance.transform.forward, out var hitInfo, __instance.m_maxDistance, __instance._layerMask))
			{
				__instance.m_frameCols.Add(hitInfo.collider);
			}
			if (__instance.m_frameCols.Count > 0)
			{
				float num = __instance.m_maxAngle + 1f;
				Collider collider = null;
				foreach (Collider frameCol in __instance.m_frameCols)
				{
					if (!(frameCol == null))
					{
						if (frameCol.gameObject.name == "InteractableBall")
						{
							collider = frameCol;
							break;
						}
						Vector3 to = frameCol.transform.position - __instance.transform.position;
						float num2 = Vector3.Angle(__instance.transform.forward, to);
						if (num2 < __instance.m_maxAngle && num2 < num && (frameCol.gameObject.name.Contains("Ignore")
							|| !Physics.Raycast(__instance.transform.position, frameCol.transform.position - __instance.transform.position,
							out var hitInfo2, Vector3.Distance(frameCol.transform.position, __instance.transform.position) - 0.1f,
							~__instance._layerMask) || (!(hitInfo2.transform == null) && !(frameCol.transform == null) && (!(Vector3.Distance(hitInfo2.transform.position, frameCol.transform.position) > 0.05f) || hitInfo2.collider.gameObject.CompareTag("Player")))))
						{
							num = num2;
							collider = frameCol;
						}
					}
				}
				if (collider != null && !MoveAndHitController.instance.m_moveLocked)
				{
					FPSInteractable component = collider.gameObject.GetComponent<FPSInteractable>();
					if (component != null)
					{
						if (component.m_interaction >= (InteractionType)50000 && component.m_interaction <= (InteractionType)50020)
						{
							__instance.m_costPrompt.SetActive(true);
						}
					}
				}
			}
		}

		[HarmonyPostfix]
		[HarmonyPatch(typeof(FPSInteractable), nameof(FPSInteractable.Interact))]
		private static void FPSInteractable_Interact_Postfix(FPSInteractable __instance)
		{
			bool boughtCheck = false;
			//shop locations ID start at 50000
			if (__instance.m_interaction >= (InteractionType)50000 && __instance.m_interaction <= (InteractionType)50020)
			{
				//ProgressManager.instance.m_bank.m_balance
				//__instance.m_cashValue

				if (__instance.m_cashValue > ProgressManager.instance.m_bank.m_balance)
				{
					ProgressManager.instance.m_bank.ChangeBalance(0, halfSound: true, fast: true);
				}
				else
				{
					ProgressManager.instance.m_bank.ChangeBalance(-__instance.m_cashValue, halfSound: true, fast: true);
					boughtCheck = true;
				}
			}

			//stray cash
			if (__instance.m_interaction >= (InteractionType)60000 && __instance.m_interaction <= (InteractionType)69999)
			{
				Plugin.BepinLogger.LogInfo("Interacted with item: " + __instance.m_interaction.ToString());
				Plugin.ArchipelagoClient.SendCheck((int)__instance.m_interaction);
				__instance.gameObject.SetActive(false);
				__instance.transform.parent.gameObject.SetActive(false);
			}

			if (!boughtCheck) return;


			Plugin.ArchipelagoClient.SendCheck((int)__instance.m_interaction);
			__instance.gameObject.SetActive(false);

		}

		[HarmonyPostfix]
		[HarmonyPatch(typeof(Breakable), nameof(Breakable.OnCollisionEnter))]
		private static void Breakable_OnCollisionEnter_Postfix(Breakable __instance, UnityEngine.Collision __0)
		{
			if (__0.gameObject.layer == LayerMask.NameToLayer("Ball"))
			{
				//programming is my passion
				if (__instance.transform.parent.name == "plyboard")
					Plugin.ArchipelagoClient.SendCheck(71000);
				else if (__instance.transform.parent.name == "plyboard (2)")
					Plugin.ArchipelagoClient.SendCheck(71001);
				else if (__instance.transform.parent.name == "plyboard (5)")
					Plugin.ArchipelagoClient.SendCheck(71002);
				else if (__instance.name == "MU1a")
					Plugin.ArchipelagoClient.SendCheck(71003);
				else if (__instance.name == "MU1b")
					Plugin.ArchipelagoClient.SendCheck(71004);
				else if (__instance.name == "MU2a")
					Plugin.ArchipelagoClient.SendCheck(71005);
				else if (__instance.name == "MU2b")
					Plugin.ArchipelagoClient.SendCheck(71006);
				else if (__instance.name == "1")
					Plugin.ArchipelagoClient.SendCheck(71007);
				else if (__instance.name == "2")
					Plugin.ArchipelagoClient.SendCheck(71008);
				else if (__instance.transform.parent.name == "plyboard_cashroom")
					Plugin.ArchipelagoClient.SendCheck(71009);

			}
		}

		[HarmonyPostfix]
		[HarmonyPatch(typeof(BallTarget), nameof(BallTarget.OnTriggerEnter))]
		private static void BallTarget_OnTriggerEnter_Postfix(BallTarget __instance, Collider __0)
		{
			if (__0.gameObject.layer == LayerMask.NameToLayer("Ball"))
			{
				Plugin.BepinLogger.LogInfo("golfball in " + __instance.id);
				var id = GameData.BallTargetIDs[__instance.id];
				Plugin.ArchipelagoClient.SendCheck(id);
			}
		}

		[HarmonyPostfix]
		[HarmonyPatch(typeof(MainManager), nameof(MainManager.Start))]
		private static void MainManager_Start_Postfix(MainManager __instance)
		{
			Plugin.BepinLogger.LogInfo("MainManager start()");
			if (Plugin.ArchipelagoClient.session != null)
			{
				Plugin.BepinLogger.LogInfo("Calling SavedGameLoader.InitializeWorld(); from MainManager start()");
				SavedGameLoader.InitializeWorld();
			}

		}

		[HarmonyPostfix]
		[HarmonyPatch(typeof(ChallengeReminder), nameof(ChallengeReminder.SetString))]
		private static void ChallengeReminder_SetString_Postfix(ChallengeReminder __instance)
		{
			int count = SaveManager.instance.m_run.m_completedBounties.Count;
			__instance.m_text.text = "Completed " + count + "/" + SavedGameLoader.BountyGoal + " Bounties";
			__instance.ShowBalanceReminder(true);
			__instance.UpdateBalanceReminder();
		}

		[HarmonyPostfix]
		[HarmonyPatch(typeof(Bank), nameof(Bank.ChangeBalance))]
		private static void Bank_ChangeBalance_Postfix(Bank __instance)
		{
			SavedGameLoader.ChallengeReminder.SetString("test"); //challengereminder postfix will set it correctly
		}

		[HarmonyPostfix]
		[HarmonyPatch(typeof(SelectClub), nameof(SelectClub.Start))]
		private static void SelectClub_Start_Postfix(SelectClub __instance)
		{
			foreach (var item in Plugin.ArchipelagoClient.session.Items.AllItemsReceived)
			{
				int id = (int)item.ItemId;
				if (id >= 2 && id <= 7) Plugin.ReceiveMiscItem(id);
			}
		}
	}


	[HarmonyPatch(typeof(SaveManager), "WriteSave")]
	public class SaveManager_WriteSave_Prefix
	{
		[HarmonyPrefix]
		static bool Prefix(SaveManager __instance, ref IEnumerator __result, string json)
		{
			__result = Archipelago_WriteSave(__instance, json);
			return false;
		}

		//Taken from the game's original WriteSave function. Identical except it should save in an archipelago folder
		static IEnumerator Archipelago_WriteSave(SaveManager __instance, string json)
		{
			while (MoveAndHitController.instance.m_moveLocked)
			{
				yield return null;
			}
			if (__instance.m_debugNoSave)
			{
				Debug.Log("Did not save, debugNoSave is on!");
				yield break;
			}
			if (__instance.m_gamemodeState.mode == GameMode.Story)
			{
				__instance.SafeWrite(Plugin.SavePath, __instance.m_runSavePath_writeBackUp, json);
			}
			if (__instance.m_gamemodeState.mode == GameMode.JustGolf)
			{
				File.WriteAllText(__instance.m_normalGolfSavePath, json);
			}
			Debug.Log("Saved!");

			Plugin.BepinLogger.LogInfo("Harmony WriteSave Prefix Saved!");
		}
	}


	[HarmonyPatch(typeof(SaveManager), "LoadStoryRun")]
	public class SaveManager_LoadStoryRun_Prefix
	{
		[HarmonyPrefix]
		static bool Prefix(SaveManager __instance, ref RunSave __result)
		{
			__result = Archipelago_LoadStoryRun(__instance);
			return false;
		}

		static RunSave Archipelago_LoadStoryRun(SaveManager __instance)
		{
			if (!File.Exists(Plugin.SavePath) && !File.Exists(Plugin.SavePathBackup))
			{
				Plugin.BepinLogger.LogInfo("Calling SavedGameLoader.LoadArchipelagoData");
				__instance.ApplyStoryModeDefaults();
				//SavedGameLoader.LoadArchipelagoData();
			}
			else
			{
				try
				{
					RunSave run = JsonUtility.FromJson<RunSave>(File.ReadAllText(Plugin.SavePath));
					__instance.m_run = run;
				}
				catch (Exception e)
				{
					Plugin.BepinLogger.LogInfo(e.Message);
					Debug.Log("Failed to load primary save, trying temp");
					try
					{
						RunSave run2 = JsonUtility.FromJson<RunSave>(File.ReadAllText(Plugin.SavePathBackup));
						__instance.m_run = run2;
					}
					catch (Exception)
					{
						Debug.Log("Failed to load backup save, reverting to default");
						//__instance.ApplyStoryModeDefaults();
						SavedGameLoader.LoadArchipelagoData();
					}
				}
				if (__instance.m_run.finishedDemo && !__instance.m_isDemo && SceneManager.GetActiveScene().name == "Main")
				{
					__instance.UpgradeDemoSave();
				}
				if (__instance.m_run.m_bankBalance == -7)
				{
					__instance.m_run.m_bankBalance = -10;
				}
				if (SceneManager.GetActiveScene().name == "Main")
				{
					__instance.SetUpScene();
				}
			}
			Plugin.BepinLogger.LogInfo("Harmony LoadStoryRun Prefix Loaded!");
			return __instance.m_run;
		}

	}
}
