using System;
using System.Collections.Generic;
using System.Text;
using TMPro;
using UnityEngine;

namespace NormalGolfArchiProject.Patcher
{

	public enum GolfSurface
	{
		Rough,
		Fairway,
		Green,
		Bunker,
		PuttPuttWall
	}

	public enum PhysicsAttribute
	{
		Friction,
		Bounciness
	}

	public class PhysicsTrap
	{
		public string name;
		public float time;
		public bool IsActive;
		public GolfSurface surface;
		public PhysicsAttribute attribute;
		public float newValue;

		int m_physicsIndex;

		public TextMeshProUGUI ui;

		public PhysicsTrap(string name, GolfSurface surface, PhysicsAttribute attribute, float newValue)
		{
			this.name = name;
			this.surface = surface;
			this.attribute = attribute;
			this.newValue = newValue;

			switch(surface)
			{
				case GolfSurface.Fairway:
					m_physicsIndex = 1;
					break;
				case GolfSurface.Green:
					m_physicsIndex = 2;
					break;
				case GolfSurface.Rough:
					m_physicsIndex = 4;
					break;
				default:
					m_physicsIndex = -1;
					Plugin.BepinLogger.LogError("Invalid surface type for PhysicsTrap");
					break;
			}

			IsActive = false;
		}

		public void ActivateTrap(float duration)
		{
			time += duration;
			IsActive = true;

			if (attribute == PhysicsAttribute.Friction && surface != GolfSurface.PuttPuttWall)
			{
				SavedGameLoader.ball.m_physics[m_physicsIndex].frictionCombine = PhysicsMaterialCombine.Minimum;
				SavedGameLoader.ball.m_physics[m_physicsIndex].staticFriction = newValue;
				SavedGameLoader.ball.m_physics[m_physicsIndex].dynamicFriction = newValue;
			}
			else if (attribute == PhysicsAttribute.Bounciness && surface != GolfSurface.PuttPuttWall)
			{
				SavedGameLoader.ball.m_physics[m_physicsIndex].bounceCombine = PhysicsMaterialCombine.Maximum;
				SavedGameLoader.ball.m_physics[m_physicsIndex].bounciness = newValue;
			}

			if (surface == GolfSurface.Green)
			{
				foreach(var mat in SavedGameLoader.PuttGreenPhysMats)
				{
					if (mat.material == null) continue;
					if (attribute == PhysicsAttribute.Friction)
					{
						mat.material.frictionCombine = PhysicsMaterialCombine.Minimum;
						mat.material.staticFriction = newValue;
						mat.material.dynamicFriction = newValue;
					}
					else if (attribute == PhysicsAttribute.Bounciness)
					{
						mat.material.bounceCombine = PhysicsMaterialCombine.Maximum;
						mat.material.bounciness = newValue;
					}
				}
			}

			ui?.gameObject.SetActive(true);
		}

		public void Update()
		{
			if (MoveAndHitController.instance.m_mode != ControlMode.Golf) return;
			time -= Time.deltaTime;
			if (time <= 0f)
			{
				time = 0f;
				IsActive = false;
				ui.gameObject.SetActive(false);
			}

			if (IsActive)
				ui.SetText(name + ": " + Mathf.RoundToInt(time));
		}
	}

	public static class BallPhysicsTraps
	{
		public static PhysicsTrapUI UI;
		public static List<PhysicsTrap> traps = new List<PhysicsTrap>();

		//original physics values
		public static PhysicsMaterialCombine greenFC = PhysicsMaterialCombine.Maximum;
		public static float greenFriction = 0.2f;
		public static PhysicsMaterialCombine greenBC = PhysicsMaterialCombine.Average;
		public static float greenBounciness = 0.175f;

		public static PhysicsMaterialCombine fairwayFC = PhysicsMaterialCombine.Maximum;
		public static float fairwayFriction = 0.3f;
		public static PhysicsMaterialCombine fairwayBC = PhysicsMaterialCombine.Average;
		public static float fairwayBounciness = 0.3f;


		public static bool IsAcceleratedFairway = false;
		private static float _timeAccelFairway;

		public static bool IsBumperPuttWalls = false;
		private static float _timeBumperPuttWalls;

		public static PhysicsTrap IcyGreen;
		public static PhysicsTrap BouncyGreen;

		public static PhysicsTrap IcyFairway;
		public static PhysicsTrap BouncyFairway;

		public static TextMeshProUGUI AcceleratedFairwayText;
		public static TextMeshProUGUI BumperPuttText;

		public static int CurrentActiveGreenTraps;
		public static int CurrentActiveFairwayTraps;
		public static int CurrentActiveRoughTraps;

		private static bool _greenDirty = false;
		private static bool _fairwayDirty = false;
		private static bool _roughDirty = false;

		public static void InitializeTraps()
		{
			IcyGreen = new PhysicsTrap("Icy Green", GolfSurface.Green, PhysicsAttribute.Friction, 0.032f);
			traps.Add(IcyGreen);
			BouncyGreen = new PhysicsTrap("Bouncy Green", GolfSurface.Green, PhysicsAttribute.Bounciness, 0.85f);
			traps.Add(BouncyGreen);

			IcyFairway = new PhysicsTrap("Icy Fairway", GolfSurface.Fairway, PhysicsAttribute.Friction, 0.064f);
			traps.Add(IcyFairway);
			BouncyFairway = new PhysicsTrap("Bouncy Fairway", GolfSurface.Fairway, PhysicsAttribute.Bounciness, 0.95f);
			traps.Add(BouncyFairway);

		}

		public static void Update()
		{
			CurrentActiveGreenTraps = 0;
			CurrentActiveFairwayTraps = 0;
			CurrentActiveRoughTraps = 0;
			foreach (var trap in traps)
			{
				if (!trap.IsActive) continue;
				
				trap.Update();
				
				switch (trap.surface)
				{
					case GolfSurface.Green:
						CurrentActiveGreenTraps++;
						_greenDirty = true;
						break;
					case GolfSurface.Fairway:
						CurrentActiveFairwayTraps++;
						_fairwayDirty = true;
						break;
					case GolfSurface.Rough:
						CurrentActiveRoughTraps++;
						_roughDirty = true;
						break;
				}
			}

			//Reset all the physics materials values to their vanilla values
			if (CurrentActiveGreenTraps == 0 && _greenDirty)
			{
				SavedGameLoader.ball.m_physics[2].frictionCombine = greenFC;
				SavedGameLoader.ball.m_physics[2].staticFriction = greenFriction;
				SavedGameLoader.ball.m_physics[2].dynamicFriction = greenFriction;
				SavedGameLoader.ball.m_physics[2].bounceCombine = greenBC;
				SavedGameLoader.ball.m_physics[2].bounciness = greenBounciness;

				foreach(var mat in SavedGameLoader.PuttGreenPhysMats)
				{
					if (mat.material != null)
					{
						mat.material.frictionCombine = greenFC;
						mat.material.staticFriction = greenFriction;
						mat.material.dynamicFriction = greenFriction;
						mat.material.bounceCombine = greenBC;
						mat.material.bounciness = greenBounciness;
					}
				}

				_greenDirty = false;
			}
			if (CurrentActiveFairwayTraps == 0 && _fairwayDirty)
			{
				SavedGameLoader.ball.m_physics[1].frictionCombine = fairwayFC;
				SavedGameLoader.ball.m_physics[1].staticFriction = fairwayFriction;
				SavedGameLoader.ball.m_physics[1].dynamicFriction = fairwayFriction;
				SavedGameLoader.ball.m_physics[1].bounceCombine = fairwayBC;
				SavedGameLoader.ball.m_physics[1].bounciness = fairwayBounciness;

				_fairwayDirty = false;
			}

			if (MoveAndHitController.instance.m_mode == ControlMode.Golf)
			{
				_timeAccelFairway -= Time.deltaTime;
				_timeBumperPuttWalls -= Time.deltaTime;
			}

			//physics traps that arent simple attribute changes
			if (_timeAccelFairway <= 0f)
			{
				_timeAccelFairway = 0f;
				IsAcceleratedFairway = false;
				AcceleratedFairwayText.gameObject.SetActive(false);
			}
			if (_timeBumperPuttWalls <= 0f)
			{
				_timeBumperPuttWalls = 0f;
				IsBumperPuttWalls = false;
				BumperPuttText.gameObject.SetActive(false);
			}

			if (IsAcceleratedFairway)
			{
				AcceleratedFairwayText.SetText("Accelerated Fairway: " + Mathf.RoundToInt(_timeAccelFairway));
			}
			if (IsBumperPuttWalls)
			{
				BumperPuttText.SetText("PuttPutt Bumpers: " + Mathf.RoundToInt(_timeBumperPuttWalls));
			}
		}

		public static void ActivateAcceleratedFairwayTrap(float duration)
		{
			_timeAccelFairway = duration;
			IsAcceleratedFairway = true;
			AcceleratedFairwayText.gameObject.SetActive(true);
		}

		public static void ActivatePuttPuttBumpersTrap(float duration)
		{
			_timeBumperPuttWalls = duration;
			IsBumperPuttWalls = true;
			BumperPuttText.gameObject.SetActive(true);
		}

		public static void ActivateIcyGreen(float duration)
		{
			IcyGreen.ActivateTrap(duration);
		}

		public static void ActivateIcyFairway(float duration)
		{
			IcyFairway.ActivateTrap(duration);
		}

		public static void ActivateBouncyGreen(float duration)
		{
			BouncyGreen.ActivateTrap(duration);
		}

		public static void ActivateBouncyFairway(float duration)
		{
			BouncyFairway.ActivateTrap(duration);
		}
	}
}
