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
			SavedGameLoader.Update();
		}

		[HarmonyPostfix]
		[HarmonyPatch(typeof(Ball), nameof(Ball.OnCollisionStay))]
		private static void Ball_OnCollisionStay_PostFix(Ball __instance, Collision __0)
		{
			if (__instance == null || __0 == null) return;
			if (BallPhysicsTraps.IsAcceleratedFairway == true)
			{
				if (__0.collider.material.name.Contains("Fairway"))
				{
					__instance.m_rb.linearVelocity += (__instance.m_rb.linearVelocity.normalized * 0.32f);
				}
			}
			if (BallPhysicsTraps.IsBumperPuttWalls == true)
			{
				if (__0.collider.material.name.Contains("Wood"))
				{
					__instance.m_rb.linearVelocity += ((__instance.m_rb.linearVelocity.normalized * 2.5f) + (Vector3.up * 0.64f));
				}
			}
		}
	}
}
