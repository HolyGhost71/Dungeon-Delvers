import React, { useState } from "react";

const LoginScreen = ({ sendMessage, connectToServer }) => {
  let [roomCode, setRoomCode] = useState("");
  let [name, setName] = useState("");

  let submit = () => {
    console.log("Button Pressed");

    connectToServer();

    let message = {
      command: "player_send_code",
      payload: { code: roomCode, name: name },
    };
    sendMessage("user_to_server", message);
    console.log("Sending message:", message);
  };

  return (
    <div className="content">
      <h4 className="heading">ROOM CODE</h4>
      <input
        className="inputBox"
        type="text"
        placeholder="ENTER 4-LETTER CODE"
        value={roomCode}
        onChange={(e) => setRoomCode(e.target.value.toUpperCase())}
        maxLength={4}
      />
      <h4 className="heading">NAME</h4>
      <input
        className="inputBox"
        type="text"
        placeholder="ENTER YOUR NAME"
        value={name}
        onChange={(e) => setName(e.target.value.toUpperCase())}
        maxLength={12}
      />
      <button className="enterButton" onClick={submit}>
        PLAY
      </button>
    </div>
  );
};

export default LoginScreen;
