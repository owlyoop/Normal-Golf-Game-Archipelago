using System;
using System.Collections.Generic;
using System.Text;
using UnityEngine;

namespace NormalGolfArchiProject.Patcher
{

	/*public class PhysicsTrap
	{
		public float time;
		public bool IsActive;

		public void ActivateTrap(float duration)
		{
			time = duration;
			IsActive = true;
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
	}*/

	public static class BallPhysicsTraps
	{
		//todo make less repetitive
		public static PhysicsMaterialCombine greenFC = PhysicsMaterialCombine.Maximum;
		public static float greenFriction = 0.2f;
		public static PhysicsMaterialCombine greenBC = PhysicsMaterialCombine.Average;
		public static float greenBounciness = 0.175f;

		public static PhysicsMaterialCombine fairwayFC = PhysicsMaterialCombine.Maximum;
		public static float fairwayFriction = 0.3f;
		public static PhysicsMaterialCombine fairwayBC = PhysicsMaterialCombine.Average;
		public static float fairwayBounciness = 0.3f;

		public static PhysicsMaterial icyGreen;
		public static PhysicsMaterial icyFairway;
		public static PhysicsMaterial bouncyGreen;
		public static PhysicsMaterial bouncyFairway;

		public static float icyGreenFriction = 0.032f;
		public static float icyFairwayFriction = 0.064f;
		public static float bouncyFairwayBounciness = 0.95f;
		public static float bouncyGreenBounciness = 0.85f;

		public static bool IsIcyGreen = false;
		public static bool IsIcyFairway = false;
		public static bool IsBouncyGreen = false;
		public static bool IsBouncyFairway = false;
		public static bool IsAcceleratedFairway = false;

		private static float timeAccelFairway;

		private static float timeIcyGreen;
		private static float timeIcyFairway;
		private static float timeBouncyGreen;
		private static float timeBouncyFairway;
		public static void Update()
		{
			//todo make this better
			if (IsIcyGreen)
				timeIcyGreen -= Time.deltaTime;
			if (IsIcyFairway)
				timeIcyFairway -= Time.deltaTime;
			if (IsBouncyGreen)
				timeBouncyGreen -= Time.deltaTime;
			if (IsBouncyFairway)
				timeBouncyFairway -= Time.deltaTime;
			if (IsAcceleratedFairway)
				timeAccelFairway -= Time.deltaTime;

			if (timeIcyGreen <= 0f)
			{
				timeIcyGreen = 0f;
				IsIcyGreen = false;

				SavedGameLoader.ball.m_physics[2].frictionCombine = greenFC;
				SavedGameLoader.ball.m_physics[2].staticFriction = greenFriction;
				SavedGameLoader.ball.m_physics[2].dynamicFriction = greenFriction;
			}

			if (timeIcyFairway <= 0f)
			{
				timeIcyFairway = 0f;
				IsIcyFairway = false;

				SavedGameLoader.ball.m_physics[1].frictionCombine = fairwayFC;
				SavedGameLoader.ball.m_physics[1].staticFriction = fairwayFriction;
				SavedGameLoader.ball.m_physics[1].dynamicFriction = fairwayFriction;
			}

			if (timeBouncyGreen <= 0f)
			{
				timeBouncyGreen = 0f;
				IsBouncyGreen = false;

				SavedGameLoader.ball.m_physics[2].bounceCombine = greenBC;
				SavedGameLoader.ball.m_physics[2].bounciness = greenBounciness;
			}

			if (timeBouncyFairway <= 0f)
			{
				timeBouncyFairway = 0f;
				IsBouncyFairway = false;

				SavedGameLoader.ball.m_physics[1].bounceCombine = fairwayBC;
				SavedGameLoader.ball.m_physics[1].bounciness = fairwayBounciness;
			}

			if (timeAccelFairway <= 0f)
			{
				timeAccelFairway = 0f;
				IsAcceleratedFairway = false;
			}
		}

		public static void InitializePhysicsMaterials()
		{
			icyGreen = UnityEngine.Object.Instantiate(SavedGameLoader.physGreenBase);
			icyGreen.frictionCombine = PhysicsMaterialCombine.Minimum;
			icyGreen.staticFriction = icyGreenFriction;
			icyGreen.dynamicFriction = icyGreenFriction;

			icyFairway = UnityEngine.Object.Instantiate(SavedGameLoader.physFairwayBase);
			icyFairway.frictionCombine = PhysicsMaterialCombine.Minimum;
			icyFairway.staticFriction = icyFairwayFriction;
			icyFairway.dynamicFriction = icyFairwayFriction;

			bouncyGreen = UnityEngine.Object.Instantiate(SavedGameLoader.physGreenBase);
			bouncyGreen.bounceCombine = PhysicsMaterialCombine.Maximum;
			bouncyGreen.bounciness = bouncyGreenBounciness;

			bouncyFairway = UnityEngine.Object.Instantiate(SavedGameLoader.physFairwayBase);
			bouncyFairway.bounceCombine = PhysicsMaterialCombine.Maximum;
			bouncyFairway.bounciness = bouncyFairwayBounciness;
		}

		public static void ActivateAcceleratedFairwayTrap(float duration)
		{
			timeAccelFairway = duration;
			IsAcceleratedFairway = true;
		}

		public static void ActivateIcyGreen(float duration)
		{
			timeIcyGreen = duration;
			IsIcyGreen = true;
			SavedGameLoader.ball.m_physics[2].frictionCombine = icyGreen.frictionCombine;
			SavedGameLoader.ball.m_physics[2].staticFriction = icyGreen.staticFriction;
			SavedGameLoader.ball.m_physics[2].dynamicFriction = icyGreen.dynamicFriction;
		}

		public static void ActivateIcyFairway(float duration)
		{
			timeIcyFairway = duration;
			IsIcyFairway = true;
			SavedGameLoader.ball.m_physics[1].frictionCombine = icyFairway.frictionCombine;
			SavedGameLoader.ball.m_physics[1].staticFriction = icyFairway.staticFriction;
			SavedGameLoader.ball.m_physics[1].dynamicFriction = icyFairway.dynamicFriction;
		}

		public static void ActivateBouncyGreen(float duration)
		{
			timeBouncyGreen = duration;
			IsBouncyGreen = true;

			SavedGameLoader.ball.m_physics[2].bounceCombine = bouncyGreen.bounceCombine;
			SavedGameLoader.ball.m_physics[2].bounciness = bouncyGreen.bounciness;
		}

		public static void ActivateBouncyFairway(float duration)
		{
			timeBouncyFairway = duration;
			IsBouncyFairway = true;

			SavedGameLoader.ball.m_physics[1].bounceCombine = bouncyFairway.bounceCombine;
			SavedGameLoader.ball.m_physics[1].bounciness = bouncyFairway.bounciness;
		}
	}
}
