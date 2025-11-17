import random
import string
from flask import Flask, request
from flask_socketio import SocketIO, emit
import logging
from Player import Player

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.get("/")
def home():
    return {"status": "ok"}

joined_players = set()
gameCode = None

def generateGameCode():
    global gameCode
    gameCode = ''.join(random.choices(string.ascii_uppercase, k=4))

# Called when a client connects
@socketio.on("connect")
def handle_connect():
    logging.info("A client connected")

@socketio.on("user_to_server")
def handle_client_message(data):
    logging.info(f"Received from web client: {data}")
    command = data.get("command")
    payload = data.get("payload")

    # The player has sent a code to the server
    if command == "player_send_code":

        # The code does not match, tell the player to disconnect
        if (payload["code"] != gameCode):
            logging.info(f"Code does not match. Correct code: {gameCode}. Received code: {payload["code"]}")
            logging.info(f"Telling user that they have not been able to connect")
            emit("server_to_user", {"command": "invalid_room_code", "payload": None})

        # The player has connected, send the player to the waiting page and add the user to the unity screen
        else:
            new_player = Player(request.sid, payload["name"])
            joined_players.add(new_player)

            logging.info(f"Client connected: {request.sid} | Total connections: {len(joined_players)}")
            logging.info(f"Telling Unity that player has connected")
            emit("server_to_unity", {"command": "player_join", "payload": payload["name"]}, broadcast=True)

            logging.info(f"Telling user that they have connected")
            emit("server_to_user", {"command": "joined_game", "payload": len(joined_players)}, broadcast=True)
    
    elif command == "start_game":
        logging.info(f"Starting game")

        loot_tiers = [{"loot_tier": 3, "loot_name": "Gold Coins", "loot_value": 10, "max_number": 4},
                      {"loot_tier": 2, "loot_name": "Gold Trinkets", "loot_value": 20, "max_number": 3},
                      {"loot_tier": 1, "loot_name": "Diamond", "loot_value": 50, "max_number": 1}]
        
        logging.info("Sending loot options to players")
        emit("server_to_user", {"command": "send_loot", "payload": loot_tiers}, broadcast=True)

        emit("server_to_unity", {"command": "send_loot", "payload": loot_tiers}, broadcast=True)

    elif command == "sending_loot_choice":

        loot_tiers = [{"loot_tier": 3, "loot_name": "Gold Coins", "loot_value": 10, "max_number": 4},
                      {"loot_tier": 2, "loot_name": "Gold Trinkets", "loot_value": 20, "max_number": 3},
                      {"loot_tier": 1, "loot_name": "Diamond", "loot_value": 50, "max_number": 1}]

        # Update the current player's choice
        for p in joined_players:
            if p.player_id == request.sid:
                p.submittedChoice = payload
                break

        # Check if all players have submitted a choice
        if all(p.submittedChoice is not None for p in joined_players):
            logging.info("All players selected options")
            
            # Count how many chose each loot tier
            chosen_tiers = [0] * len(loot_tiers)
            for p in joined_players:
                for i, tier in enumerate(loot_tiers):
                    if p.submittedChoice == tier:
                        chosen_tiers[i] += 1
                        break

            # Check for dragon attack
            for i, count in enumerate(chosen_tiers):
                if count > loot_tiers[i]["max_number"]:
                    logging.info(f"The dragon breathes fire on tier {i}")
                else:
                    logging.info(f"Tier {i} is safe")
                    for p in joined_players:
                        if p.submittedChoice == loot_tiers[i]:
                            p.add_gold(loot_tiers[i]["loot_value"])
                            logging.info((f"PlayerID: {p.player_id}. Name: {p.name}. I have {p.gold}gp"))



@socketio.on("unity_to_server")
def handle_client_message(data):
    logging.info(f"Received from unity game client: {data}")

    command = data.get("command")
    payload = data.get("payload")

    # The Unity server has opened the room and is requesting the server to provide a Room Code
    if command == "request_room_code":
        logging.info(f"Sending room code")
        generateGameCode()
        emit("server_to_unity", {"command": "room_code_response", "payload": gameCode}, broadcast=True)

    # The Unity server has been disconnected - the player set should be emptied and the
    # players should be disconnected
    elif command == "unity_disconnect":
        logging.info("Unity server disconnected")
        joined_players.clear()

# Called when a client disconnects
@socketio.on("disconnect")
def handle_disconnect():
    logging.info(f"A client: {request.sid} disconnected")
    if (request.sid in joined_players): joined_players.remove(request.sid)

if __name__ == "__main__":
    # Run server on all network interfaces
    socketio.run(app, host="0.0.0.0", port=5000)