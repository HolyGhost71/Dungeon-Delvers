import React, { useEffect, useState, useRef } from "react";
import Banner from "./components/Banner";
import { io } from "socket.io-client";
import ConnectionBox from "./components/ConnectionBox";
import WaitingBox from "./components/WaitingBox";
import InfoBox from "./components/InfoBox";

function App() {
  // Game state
  const GameScreen = {
    LOGIN: "login",
    WAITING: "waiting",
    INFO: "info",
  };

  const [currentScreen, setCurrentScreen] = useState(GameScreen.LOGIN);
  const [isFirstUser, setIsFirstUser] = useState(false);
  const [infoScreenText, setInfoScreenText] = useState("");

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
          setCurrentScreen(GameScreen.WAITING);
        }

        if (data.command === "invalid_room_code") {
          console.log("Disconneceted from server");
          alert("Invalid room code, please try again.");
          socket.current.disconnect();
          socket.current = null;
        }

        if (data.command === "display_answer") {
          setCurrentScreen(GameScreen.INFO);
          setInfoScreenText(data.payload);
        }
      });
    }
  };

  const startGame = () => {
    console.log("Starting game");
    sendMessage("user_to_server", { command: "start_game", payload: null });
  };

  const sendMessage = (emitTo, message) => {
    if (socket.current) socket.current.emit(emitTo, message);
    else console.warn("Socket not connected yet!");
  };

  return (
    <div>
      <Banner />
      {currentScreen === GameScreen.LOGIN && (
        <ConnectionBox
          sendMessage={sendMessage}
          connectToServer={connectToServer}
        />
      )}
      {currentScreen === GameScreen.WAITING && (
        <WaitingBox isFirstUser={isFirstUser} startGame={startGame} />
      )}
      {currentScreen === GameScreen.INFO && (
        <InfoBox infoScreenText={infoScreenText} />
      )}
    </div>
  );
}

export default App;
