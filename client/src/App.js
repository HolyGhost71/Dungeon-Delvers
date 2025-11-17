import React, { useEffect, useState, useRef } from "react";
import Banner from "./components/Banner";
import { io } from "socket.io-client";
import LoginScreen from "./components/LoginScreen";
import WaitingScreen from "./components/WaitingScreen";
import LootScreen from "./components/LootScreen";

function App() {
  // Game state
  const GameScreen = {
    LOGIN: "login",
    WAITING_FOR_PLAYERS: "waiting",
    IDLE: "idle", // Can be displayed while the unity game runs animations or waiting for other players
    LOOT: "loot",
    SHOP: "shop",
  };

  const [currentScreen, setCurrentScreen] = useState(GameScreen.LOGIN);
  const [isFirstUser, setIsFirstUser] = useState(false);
  const [lootTiers, setLootTiers] = useState([]);

  const socket = useRef(null);

  const connectToServer = () => {
    if (!socket.current) {
      socket.current = io("http://127.0.0.1:5000");

      socket.current.on("connect", () => console.log("Connected to server!"));

      socket.current.on("server_to_user", (data) => {
        console.log("Server message:", data);

        if (data.command === "joined_game") {
          if (data.payload == 1) {
            console.log("Number of users " + data.payload);
            setIsFirstUser(true);
          }
          setCurrentScreen(GameScreen.WAITING_FOR_PLAYERS);
        }

        if (data.command === "invalid_room_code") {
          console.log("Disconneceted from server");
          alert("Invalid room code, please try again.");
          socket.current.disconnect();
          socket.current = null;
        }

        if (data.command === "send_loot") {
          setLootTiers(data.payload);
          setCurrentScreen(GameScreen.LOOT);
        }
      });
    }
  };

  const startGame = () => {
    console.log("Starting game");
    sendMessage("user_to_server", { command: "start_game", payload: null });
  };

  const sendLootChoice = (loot) => {
    console.log("Sending loot choice");
    sendMessage("user_to_server", {
      command: "sending_loot_choice",
      payload: loot,
    });
    setCurrentScreen(GameScreen.IDLE);
  };

  const sendMessage = (emitTo, message) => {
    if (socket.current) socket.current.emit(emitTo, message);
    else console.warn("Socket not connected yet!");
  };

  return (
    <div>
      <Banner />
      {currentScreen === GameScreen.LOGIN && (
        <LoginScreen
          sendMessage={sendMessage}
          connectToServer={connectToServer}
        />
      )}
      {currentScreen === GameScreen.WAITING_FOR_PLAYERS && (
        <WaitingScreen isFirstUser={isFirstUser} startGame={startGame} />
      )}
      {currentScreen === GameScreen.LOOT && (
        <LootScreen lootTiers={lootTiers} sendLootChoice={sendLootChoice} />
      )}
    </div>
  );
}

export default App;
