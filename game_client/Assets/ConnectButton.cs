using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using UnityEngine;

public class ConnectButton : MonoBehaviour
{
    public async void OnPressConnect()
    {
        await NetworkClient.Instance.ConnectToServer();

        await NetworkClient.Instance.socket.EmitAsync("unity_to_server", new
        {
            command = "request_room_code",
            payload = (object)null
        });

        
    }
}
