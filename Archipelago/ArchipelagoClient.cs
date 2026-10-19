using Archipelago.MultiClient.Net;
using Archipelago.MultiClient.Net.BounceFeatures.DeathLink;
using Archipelago.MultiClient.Net.Enums;
using Archipelago.MultiClient.Net.Helpers;
using Archipelago.MultiClient.Net.MessageLog.Messages;
using Archipelago.MultiClient.Net.Models;
using Archipelago.MultiClient.Net.Packets;
using BepInEx.Logging;
using NormalGolfArchiProject.Patcher;
using NormalGolfArchiProject.Utils;
using System;
using System.Linq;
using System.Threading;
using TMPro;
using UnityEngine;

namespace NormalGolfArchiProject.Archipelago;

public class ArchipelagoClient
{
    public const string APVersion = "0.6.7";
    private const string Game = "Normal Golf Game";

    public static bool Authenticated;
    private bool attemptingConnection;

    public static ArchipelagoData ServerData = new();
    private DeathLinkHandler DeathLinkHandler;
    public ArchipelagoSession session { get; private set; }

    /// <summary>
    /// call to connect to an Archipelago session. Connection info should already be set up on ServerData
    /// </summary>
    /// <returns></returns>
    public void Connect()
    {
        if (Authenticated || attemptingConnection) return;

        try
        {
            session = ArchipelagoSessionFactory.CreateSession(ServerData.Uri);
            SetupSession();
        }
        catch (Exception e)
        {
            Plugin.BepinLogger.LogError(e);
        }

        TryConnect();
    }

    /// <summary>
    /// add handlers for Archipelago events
    /// </summary>
    private void SetupSession()
    {
        session.MessageLog.OnMessageReceived += message => ArchipelagoConsole.LogMessage(message.ToString());
        session.Items.ItemReceived += OnItemReceived;
        session.Socket.ErrorReceived += OnSessionErrorReceived;
        session.Socket.SocketClosed += OnSessionSocketClosed;
    }

    /// <summary>
    /// attempt to connect to the server with our connection info
    /// </summary>
    private void TryConnect()
    {
        try
        {
            // it's safe to thread this function call but unity notoriously hates threading so do not use excessively
            ThreadPool.QueueUserWorkItem(
                _ => HandleConnectResult(
                    session.TryConnectAndLogin(
                        Game,
                        ServerData.SlotName,
                        ItemsHandlingFlags.AllItems,
                        new Version(APVersion),
                        password: ServerData.Password,
                        requestSlotData: ServerData.NeedSlotData
                    )));
        }
        catch (Exception e)
        {
            Plugin.BepinLogger.LogError(e);
            HandleConnectResult(new LoginFailure(e.ToString()));
            attemptingConnection = false;
        }
    }

    /// <summary>
    /// handle the connection result and do things
    /// </summary>
    /// <param name="result"></param>
    private void HandleConnectResult(LoginResult result)
    {
        string outText;
        if (result.Successful)
        {
            var success = (LoginSuccessful)result;

            ServerData.SetupSession(success.SlotData, session.RoomState.Seed);
            Authenticated = true;

            DeathLinkHandler = new(session.CreateDeathLinkService(), ServerData.SlotName);
            session.Locations.CompleteLocationChecksAsync(ServerData.CheckedLocations.ToArray());
            outText = $"Successfully connected to {ServerData.Uri} as {ServerData.SlotName}!";

            ArchipelagoConsole.LogMessage(outText);

			Plugin.MainMenu();
			
		}
        else
        {
            var failure = (LoginFailure)result;
            outText = $"Failed to connect to {ServerData.Uri} as {ServerData.SlotName}.";
            outText = failure.Errors.Aggregate(outText, (current, error) => current + $"\n    {error}");

            Plugin.BepinLogger.LogError(outText);

            Authenticated = false;
            Disconnect();
        }

        ArchipelagoConsole.LogMessage(outText);
        attemptingConnection = false;
    }

    /// <summary>
    /// something went wrong, or we need to properly disconnect from the server. cleanup and re null our session
    /// </summary>
    private void Disconnect()
    {
        Plugin.BepinLogger.LogDebug("disconnecting from server...");
        session?.Socket.DisconnectAsync();
        session = null;
        Authenticated = false;
    }

    public void SendMessage(string message)
    {
        session.Socket.SendPacketAsync(new SayPacket { Text = message });
    }

    /// <summary>
    /// we received an item so reward it here
    /// </summary>
    /// <param name="helper">item helper which we can grab our item from</param>
    private void OnItemReceived(ReceivedItemsHelper helper)
    {
        var itemInfo = helper.DequeueItem();

        if (helper.Index <= ServerData.Index) return;

        ServerData.Index++;

		int num = (int)itemInfo.ItemId;
		ManualLogSource logger = Plugin.BepinLogger;
		bool flag = default(bool);
		
		logger.LogInfo(itemInfo.ItemName);
		// TODO reward the item here
		// if items can be received while in an invalid state for actually handling them, they can be placed in a local
		// queue/collection to be handled later

		/*if (num >= 2000)	//cash
		{
			Plugin.ReceiveCashItem(num);
		}
		else if (num >= 1000)	//region
		{
			Plugin.ReceiveRegionUnlockItem(num);
		}
		else if (num >= 600)	//difficulty
		{
			Plugin.ReceiveDifficultyUnlockItem(num);
		}
		else
		{
			//misc (clubs, filler, etc)
			Plugin.ReceiveMiscItem(num);
		}*/
		Plugin.ItemQueue.Enqueue(num);
	}

	//https://www.nuget.org/packages/Archipelago.MultiClient.Net/6.0.0
	public bool HasItemReceived(int id)
	{
		foreach(var item in session.Items.AllItemsReceived)
		{
			if (item.ItemId == id)
				return true;
		}
		return false;
	}

	public bool SendCheck(int location)
	{
		foreach(var loc in session.Locations.AllLocationsChecked)
		{
			if ((int)loc == location) return false;
		}
		session.Locations.CompleteLocationChecks(location);
		return true;
	}

    /// <summary>
    /// something went wrong with our socket connection
    /// </summary>
    /// <param name="e">thrown exception from our socket</param>
    /// <param name="message">message received from the server</param>
    private void OnSessionErrorReceived(Exception e, string message)
    {
        Plugin.BepinLogger.LogError(e);
        ArchipelagoConsole.LogMessage(message);
    }

    /// <summary>
    /// something went wrong closing our connection. disconnect and clean up
    /// </summary>
    /// <param name="reason"></param>
    private void OnSessionSocketClosed(string reason)
    {
        Plugin.BepinLogger.LogError($"Connection to Archipelago lost: {reason}");
        Disconnect();
    }
}