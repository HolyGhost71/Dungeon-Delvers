import React from "react";

const LootScreen = ({ lootTiers, sendLootChoice }) => {
  return (
    <div>
      <h1>Make your choice...</h1>
      <p>
        Higher valued loot is hidden closer to the dragon. The more people that
        attempt to steal it, the more likely the dragon is to attack...
      </p>
      <div className="loot-container">
        {lootTiers.map((loot, index) => (
          <div
            key={index}
            className="loot-box"
            onClick={() => sendLootChoice(loot)}
          >
            <h2>{loot.loot_name}</h2>
            <p>Value: {loot.loot_value}</p>
            <p>Max players before dragon awakens: {loot.max_number}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LootScreen;
