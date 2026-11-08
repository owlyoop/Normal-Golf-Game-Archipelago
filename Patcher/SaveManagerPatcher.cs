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
	[HarmonyPatch(typeof(SaveManager), "WriteSave")]
	public class SaveManager_WriteSave_Prefix
	{
		[HarmonyPrefix]
		static bool Prefix(SaveManager __instance, ref IEnumerator __result, string json)
		{
			__result = Archipelago_WriteSave(__instance, json);
			return false;
		}

		//I received permission from Luke Muscat to use this function taken from the original game's code & minorly edited.
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

		//I received permission from Luke Muscat to use this function taken from the original game's code & minorly edited.
		static RunSave Archipelago_LoadStoryRun(SaveManager __instance)
		{
			if (!File.Exists(Plugin.SavePath) && !File.Exists(Plugin.SavePathBackup))
			{
				Plugin.BepinLogger.LogInfo("Archipelago_LoadStoryRun: File does not exist");

				if (ArchipelagoClient.Authenticated && Plugin.ArchipelagoClient.session != null)
				{
					SavedGameLoader.CreateSaveData();
				}
				else
				{
					__instance.ApplyStoryModeDefaults();
				}
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
						SavedGameLoader.CreateSaveData();
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
