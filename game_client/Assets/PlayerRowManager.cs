using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;


public class PlayerRowManager : MonoBehaviour
{
    [SerializeField] private Transform playerRowParent;   // The Horizontal Layout Group
    [SerializeField] private GameObject playerCardPrefab; // UI prefab

    private Dictionary<string, GameObject> activePlayers = new Dictionary<string, GameObject>();

    public void AddPlayer(string playerName)
    {
        if (activePlayers.ContainsKey(playerName))
            return; // Already exists

        GameObject card = Instantiate(playerCardPrefab, playerRowParent, false);

        // Update card text
        TextMeshProUGUI nameText = card.GetComponentInChildren<TextMeshProUGUI>();
        nameText.text = playerName;

        activePlayers[playerName] = card;
    }

    public void RemovePlayer(string playerName)
    {
        if (!activePlayers.ContainsKey(playerName))
            return;

        GameObject card = activePlayers[playerName];
        Destroy(card);
        activePlayers.Remove(playerName);
    }

    public void Start()
    {
    }
}
