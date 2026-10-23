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
	public class BallPhysicsPatcher
	{
		[HarmonyPostfix]
		[HarmonyPatch(typeof(MainManager), nameof(MainManager.Update))]
		private static void MainManager_Update_PostFix(MainManager __instance)
		{
			if (SceneManager.GetActiveScene().name != "Main") return;
			BallPhysicsTraps.Update();
		}

		[HarmonyPostfix]
		[HarmonyPatch(typeof(Ball), nameof(Ball.OnCollisionStay))]
		private static void Ball_OnCollisionStay_PostFix(Ball __instance)
		{
			if (!BallPhysicsTraps.IsAcceleratedFairway) return;

			if (__instance.m_currentShotData.m_lastTouchedSurface.Substring(0, 4) == "Fair")
			{
				__instance.m_rb.linearVelocity += (__instance.m_rb.linearVelocity.normalized * 0.32f);
			}
		}
	}
}
