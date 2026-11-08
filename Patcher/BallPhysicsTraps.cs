using System;
using System.Collections.Generic;
using System.Text;
using UnityEngine;

namespace NormalGolfArchiProject.Patcher
{

	public enum GolfSurface
	{
		Rough,
		Fairway,
		Green,
		Bunker
	}

	public enum PhysicsAttribute
	{
		Friction,
		Bounciness
	}

	public class PhysicsTrap
	{
		public float time;
		public bool IsActive;
		public GolfSurface surface;
		public PhysicsAttribute attribute;
		public float newValue;

		int m_physicsIndex;
		public PhysicsTrap(GolfSurface surface, PhysicsAttribute attribute, float newValue)
		{
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

			if (attribute == PhysicsAttribute.Friction)
			{
				SavedGameLoader.ball.m_physics[m_physicsIndex].frictionCombine = PhysicsMaterialCombine.Minimum;
				SavedGameLoader.ball.m_physics[m_physicsIndex].staticFriction = newValue;
				SavedGameLoader.ball.m_physics[m_physicsIndex].dynamicFriction = newValue;
			}
			else if (attribute == PhysicsAttribute.Bounciness)
			{
				SavedGameLoader.ball.m_physics[m_physicsIndex].bounceCombine = PhysicsMaterialCombine.Maximum;
				SavedGameLoader.ball.m_physics[m_physicsIndex].bounciness = newValue;
			}
		}

		public void Update()
		{
			time -= Time.deltaTime;
			if (time <= 0f)
			{
				time = 0f;
				IsActive = false;
			}
		}
	}

	public static class BallPhysicsTraps
	{

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

		public static PhysicsTrap IcyGreen;
		public static PhysicsTrap BouncyGreen;

		public static PhysicsTrap IcyFairway;
		public static PhysicsTrap BouncyFairway;

		public static int CurrentActiveGreenTraps;
		public static int CurrentActiveFairwayTraps;
		public static int CurrentActiveRoughTraps;

		private static bool _greenDirty;
		private static bool _fairwayDirty;
		private static bool _roughDirty;

		public static void InitializeTraps()
		{
			IcyGreen = new PhysicsTrap(GolfSurface.Green, PhysicsAttribute.Friction, 0.032f);
			traps.Add(IcyGreen);
			BouncyGreen = new PhysicsTrap(GolfSurface.Green, PhysicsAttribute.Bounciness, 0.85f);
			traps.Add(BouncyGreen);

			IcyFairway = new PhysicsTrap(GolfSurface.Fairway, PhysicsAttribute.Friction, 0.064f);
			traps.Add(IcyFairway);
			BouncyFairway = new PhysicsTrap(GolfSurface.Fairway, PhysicsAttribute.Bounciness, 0.95f);
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
			if (CurrentActiveRoughTraps == 0 && _roughDirty)
			{

			}

			_timeAccelFairway -= Time.deltaTime;

			//physics traps that arent simple attribute changes
			if (_timeAccelFairway <= 0f)
			{
				_timeAccelFairway = 0f;
				IsAcceleratedFairway = false;
			}
		}

		public static void ActivateAcceleratedFairwayTrap(float duration)
		{
			_timeAccelFairway = duration;
			IsAcceleratedFairway = true;
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
