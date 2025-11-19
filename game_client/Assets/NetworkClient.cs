using System;
using System.Collections.Generic;
using UnityEngine;
using SocketIOClient.Newtonsoft.Json;
using SocketIOClient;
using static SocketIOUnity;
using System.Threading.Tasks;
using UnityEngine.UI;
using TMPro;
using Unity.VisualScripting;

public class NetworkClient : MonoBehaviour
{
    public static NetworkClient Instance;     // <--- Global access!

    public SocketIOUnity socket;
    [SerializeField] private GameObject playButton;
    [SerializeField] private TextMeshProUGUI roomCodeText;
    [SerializeField] private PlayerManager playerManager;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
            return;
        }
    }

    async void Start()
    {
        // Replace with your PC LAN IP
        Uri serverUri = new Uri("http://127.0.0.1:5000");

        // Initialize Socket.IO client
        socket = new SocketIOUnity(serverUri, new SocketIOOptions
        {
            Query = new Dictionary<string, string> { { "token", "UNITY" } },
            Transport = SocketIOClient.Transport.TransportProtocol.WebSocket
        });

        socket.JsonSerializer = new NewtonsoftJsonSerializer();
        socket.unityThreadScope = UnityThreadScope.Update;

        // Event: on connect
        socket.On("connect", (response) =>
        {
            Debug.Log("Connected to server!");
        });

        // Handle messages from server
        socket.OnUnityThread("server_to_unity", (message) =>
        {
            try
            {
                // Parse the response as JObject
                var json = message.GetValue<Newtonsoft.Json.Linq.JObject>();

                // Extract command and payload
                string command = json["command"]?.ToString();
                var p = json["payload"];
                var payload = p?.ToString();

                Debug.Log("Command received: " + command);
                Debug.Log("Payload received: " + payload);

                if (command == "room_code_response")
                {
                    roomCodeText.text = ("The room code is " + payload);
                    roomCodeText.gameObject.SetActive(true);
                    playButton.gameObject.SetActive(false);
                }

                if (command == "player_join")
                {
                    // Parse payload from string → JObject
                    var payloadObj = Newtonsoft.Json.Linq.JObject.Parse(payload);

                    string playerName = payloadObj["name"].ToString();
                    int gold = payloadObj["gold"].ToObject<int>();

                    Debug.Log(playerName + " joined the game with " + gold.ToString() + "gp");

                    playerManager.AddPlayer(playerName, gold);
                }

                if (command == "player_disconnected")
                {
                    Debug.Log(payload + " disconnected");
                    playerManager.RemovePlayer(payload);
                }
            }
            catch (Exception ex)
            {
                Debug.LogError("Failed to parse server_to_unity: " + ex);
            }
        });
    }

    public async Task ConnectToServer()
    {
        // Connect to the server and send a test ping/pong reply
        try
        {
            await socket.ConnectAsync();
        }
        catch (Exception ex)
        {
            Debug.LogError("Socket.IO connection error: " + ex);
        }
    }

    private async void OnApplicationQuit()
    {
        if (socket != null)
        {
            await socket.EmitAsync("unity_to_server", new
            {
                command = "unity_disconnect",
                payload = (object)null
            });
            await socket.DisconnectAsync();
            Debug.Log("Disconnected from server");
        }
    }
}