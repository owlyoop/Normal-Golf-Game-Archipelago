using System;
using System.Collections.Generic;
using System.Text;

//using App.
using BepInEx.Logging;
using HarmonyLib;
using NormalGolfArchiProject;
using TMPro;
using UnityEngine;

namespace NormalGolfArchiProject.Patcher
{
	public class PhysicsTrapUI : MonoBehaviour
	{
		GameObject status;

		TextMeshProUGUI textPrefab;
		Color yellow;
		Color blue;
		Color pink;


		public TextMeshProUGUI IcyGreen;
		public TextMeshProUGUI BouncyGreen;
		public TextMeshProUGUI IcyFairway;
		public TextMeshProUGUI BouncyFairway;
		public TextMeshProUGUI AcceleratedFairway;
		public TextMeshProUGUI PuttPuttWallBumpers;

		List<TextMeshProUGUI> TrapsText = new List<TextMeshProUGUI>();
		public void Initialize()
		{
			yellow = new Color(0.9843f, 0.9137f, 0.6863f, 1f);
			blue = new Color(0.8353f, 0.9922f, 0.9686f, 1f);
			pink = new Color(0.9324f, 0.6863f, 0.9843f, 1f);

			var go = GameObject.Find("PANEL_Main Controls/Canvas/STATS");
			status = Instantiate(go, go.transform.parent);
			status.SetName("PhysicsTrapUI");
			status.SetActive(true);
			var rect = status.GetComponent<RectTransform>();
			rect.anchoredPosition = new Vector2(-625f, 200f);

			var a = status.transform.Find("ANGLE");
			var b = status.transform.Find("Backspin");
			Destroy(a.gameObject);
			Destroy(b.gameObject);

			var text = status.transform.Find("LOFT").GetComponent<TextMeshProUGUI>().GetComponent<TextMeshProUGUI>();
			text.SetName("Physics Trap Text");

			for (int i = text.transform.childCount - 1; i >= 0; i--)
			{
				Destroy(text.transform.GetChild(i).gameObject);
			}

			text.alignment = TextAlignmentOptions.Left;
			text.color = yellow;
			text.GetComponent<RectTransform>().offsetMax = new Vector2(300f, text.GetComponent<RectTransform>().offsetMax.y);
			text.SetText("Physics Trap Name");
			textPrefab = text;
			text.gameObject.SetActive(false);

			BallPhysicsTraps.UI = this;
			CreateTextPerTrap();
		}

		public void CreateTextPerTrap()
		{
			IcyGreen = Instantiate(textPrefab, textPrefab.transform.parent);
			IcyGreen.SetText("Icy Green: 60");
			BallPhysicsTraps.IcyGreen.ui = IcyGreen;

			BouncyGreen = Instantiate(textPrefab, textPrefab.transform.parent);
			BouncyGreen.SetText("Bouncy Green: 60");
			BallPhysicsTraps.BouncyGreen.ui = BouncyGreen;

			IcyFairway = Instantiate(textPrefab, textPrefab.transform.parent);
			IcyFairway.SetText("Icy Fairway: 60");
			BallPhysicsTraps.IcyFairway.ui = IcyFairway;

			BouncyFairway = Instantiate(textPrefab, textPrefab.transform.parent);
			BouncyFairway.SetText("Bouncy Fairway: 60");
			BallPhysicsTraps.BouncyFairway.ui = BouncyFairway;

			AcceleratedFairway = Instantiate(textPrefab, textPrefab.transform.parent);
			AcceleratedFairway.SetText("Accelerated Fairway: 60");
			BallPhysicsTraps.AcceleratedFairwayText = AcceleratedFairway;

			PuttPuttWallBumpers = Instantiate(textPrefab, textPrefab.transform.parent);
			PuttPuttWallBumpers.SetText("PuttPutt Bumpers: 60");
			BallPhysicsTraps.BumperPuttText = PuttPuttWallBumpers;



			TrapsText = new List<TextMeshProUGUI>()
			{
				IcyGreen,
				BouncyGreen,
				IcyFairway,
				BouncyFairway,
				AcceleratedFairway,
				PuttPuttWallBumpers
			};

			foreach(var text in TrapsText)
			{
				text.gameObject.SetActive(false);
			}
		}
	}
}
