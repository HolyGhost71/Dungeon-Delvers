import React from "react";
import { Button } from "@mui/material";

const WaitingBox = ({ startGame, isFirstUser }) => {
  const submit = () => {
    console.log("Starting game...");
    startGame();
  };

  return (
    <div>
      <h1>Waiting for players...</h1>
      {isFirstUser && <Button onClick={submit}>Start Game</Button>}
    </div>
  );
};

export default WaitingBox;
