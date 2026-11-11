using Archipelago.MultiClient.Net.Models;
using BepInEx.Logging;
using HarmonyLib;
using I2.Loc.SimpleJSON;
using Newtonsoft.Json;
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
	[HarmonyPatch(typeof(SaveManager), nameof(SaveManager.m_runSavePath), MethodType.Getter)]
	public class SaveManager_RunSavePath_Postfix
	{
		static void Postfix(ref string __result)
		{
			if (!string.IsNullOrEmpty(Plugin.SavePath))
				__result = Plugin.SavePath;
		}
	}

	[HarmonyPatch(typeof(SaveManager), nameof(SaveManager.m_runSavePath_writeBackUp), MethodType.Getter)]
	public class SaveManager_RunSavePathBackup_Postfix
	{
		static void Postfix(ref string __result)
		{
			if (!string.IsNullOrEmpty(Plugin.SavePath))
				__result = Plugin.SavePathBackup;
		}
	}

	[HarmonyPatch(typeof(SaveManager), "LoadStoryRun")]
	public class SaveManager_LoadStoryRun_Prefix
	{
		[HarmonyPrefix]
		static bool Prefix(SaveManager __instance, ref RunSave __result)
		{
			if (Plugin.ArchipelagoClient.session != null && Plugin.ArchipelagoClient.session.Socket.Connected)
			{
				if (!File.Exists(Plugin.SavePath) && !File.Exists(Plugin.SavePathBackup))
					__instance.m_run = SavedGameLoader.CreateSaveData();
				else
				{
					try
					{
						RunSave run = JsonConvert.DeserializeObject<RunSave>(File.ReadAllText(Plugin.SavePath));
						__instance.m_run = run;
					}
					catch (Exception e)
					{
						Plugin.BepinLogger.LogInfo(e.Message);
						try
						{
							RunSave run2 = JsonConvert.DeserializeObject<RunSave>(File.ReadAllText(Plugin.SavePathBackup));
							__instance.m_run = run2;
						}
						catch (Exception e2)
						{
							Plugin.BepinLogger.LogInfo(e2.Message);
						}
					}
					
				}

				if (__instance.m_run.m_bankBalance == -10)
					__instance.m_run.m_bankBalance = 0;

				if (SceneManager.GetActiveScene().name == "Main")
					__instance.SetUpScene();

				__result = __instance.m_run;
				return false;
			}
			
			return true;
		}
	}

	//bypass the difficulty select screen if connected to archi
	[HarmonyPatch(typeof(MainMenu), nameof(MainMenu.PlayGame))]
	public class MainMenu_PlayGame_Prefix
	{
		[HarmonyPrefix]
		static bool Prefix(MainMenu __instance)
		{
			if (Plugin.ArchipelagoClient.session != null && Plugin.ArchipelagoClient.session.Socket.Connected)
			{
				SaveManager.instance.SaveGameSettings();
				SceneManager.LoadScene("Main");
				return false;
			}
			return true;
		}
	}
}
