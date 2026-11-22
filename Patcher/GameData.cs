using System;
using System.Collections.Generic;
using System.Text;

namespace NormalGolfArchiProject.Patcher
{
	public static class GameData
	{
		public static readonly Dictionary<string, int> BallTargetIDs =
			new Dictionary<string, int>()
			{
				["hole1"] = 70000,
				["hole2"] = 70001,
				["hole3"] = 70002,
				["hole4"] = 70003,
				["hole5"] = 70004,
				["hole6"] = 70005,
				["hole7"] = 70006,
				["hole8"] = 70007,
				["hole9"] = 70008,
	
				["bigBunkerHole"] = 70012,
				["puttputt1"] = 70013,
				["puttputt2"] = 70014,
				["puttputt3"] = 70015,
				["puttputt4"] = 70016,
				["puttputt5"] = 70017,
				["puttputt6"] = 70018,
				["puttputtHole4"] = 70019,
				["puttJump"] = 70020,
				["puttHole7"] = 70021,
				["puttputtDish"] = 70022,
				["puttPool1"] = 70023,
				["puttPool2"] = 70024,
				["puttPool3"] = 70025,
				["puttPool4"] = 70026,
				["puttPool5"] = 70027,
				["puttPool6"] = 70028,
				["tallBoy1"] = 70029,
				["tallBoy2"] = 70030,
				["tallBoy3"] = 70031,
				["puttTilt"] = 70032,

				["miniIsland"] = 70033,
				["miniIsland2"] = 70034,
				["miniIsland3"] = 70035,

				["secretGreen"] = 70036,
				["secretGreen2"] = 70037,
			};

		public static readonly Dictionary<string, int> BreakableParentNameIDs =
			new Dictionary<string, int>()
			{
				["plyboard"] = 71000,
				["plyboard (2)"] = 71001,
				["plyboard (5)"] = 71002,
				["MU1a"] = 71003,
				["MU1b"] = 71004,
				["MU2a"] = 71005,
				["MU2b"] = 71006,
				["1"] = 71007,
				["2"] = 71008,
				["plyboard_cashroom"] = 71009,

				["Cube"] = 72000,
				["Cube.001"] = 72001,
				["Cube.002"] = 72002,
				["Cube.003"] = 72003,
				["Cube.004"] = 72004,
				["Cube.005"] = 72005,
				["Cube.006"] = 72006,
				["Cube.007"] = 72007,
			};
	}
}
