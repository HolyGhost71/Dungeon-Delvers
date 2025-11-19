using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;



public class PlayerManager : MonoBehaviour
{
    [SerializeField] private Transform playerRowParent;
    [SerializeField] private GameObject playerCardPrefab;

    // Stores: playerName → PlayerData
    private Dictionary<string, PlayerData> activePlayers = new Dictionary<string, PlayerData>();

    public void AddPlayer(string playerName, int startingGold)
    {
        if (activePlayers.ContainsKey(playerName))
            return;

        GameObject card = Instantiate(playerCardPrefab, playerRowParent, false);

        // Set UI text
        TextMeshProUGUI nameText = card.transform.Find("NameText").GetComponent<TextMeshProUGUI>();
        nameText.text = playerName;

        // Optional: also show gold if your prefab has a "GoldText"
        TextMeshProUGUI goldText = card.transform.Find("GoldText").GetComponent<TextMeshProUGUI>();
        if (goldText != null)
            goldText.text = startingGold.ToString();

        // Store player data
        activePlayers[playerName] = new PlayerData
        {
            uiCard = card,
            gold = startingGold
        };
    }

    public void UpdateGold(string playerName, int newGold)
    {
        if (!activePlayers.ContainsKey(playerName))
            return;

        PlayerData p = activePlayers[playerName];
        p.gold = newGold;

        TextMeshProUGUI goldText = p.uiCard.transform.Find("GoldText").GetComponent<TextMeshProUGUI>();
        if (goldText != null)
            goldText.text = newGold.ToString();
    }

    public void RemovePlayer(string playerName)
    {
        if (!activePlayers.ContainsKey(playerName))
            return;

        Debug.Log("Removing player: " + playerName);

        GameObject card = activePlayers[playerName].uiCard;
        Destroy(card);
        activePlayers.Remove(playerName);
    }

}

public class PlayerData
{
    public GameObject uiCard;
    public int gold;
}
