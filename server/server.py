import random
import string
from flask import Flask, request
from flask_socketio import SocketIO, emit
import logging
import chameleon_game

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
            joined_players.add(request.sid)

            logging.info(f"Client connected: {request.sid} | Total connections: {len(joined_players)}")
            logging.info(f"Telling Unity that player has connected")
            emit("server_to_unity", {"command": "player_join", "payload": payload["name"]}, broadcast=True)

            logging.info(f"Telling user that they have connected")
            emit("server_to_user", {"command": "joined_game", "payload": len(joined_players)}, broadcast=True)
    
    elif command == "start_game":
        logging.info(f"Starting game")

        gameInfo = chameleon_game.getGameCard()
        heading = gameInfo["heading"]
        options = gameInfo["options"]
        chosenAnswer = gameInfo["chosenAnswer"]
        logging.info(heading)
        logging.info(options)
        logging.info(chosenAnswer)

        chameleon_player = random.choice(list(joined_players))
        logging.info("The chameleon is: " + chameleon_player)

        for player in joined_players:
            if player == chameleon_player:
                emit("server_to_user", {"command": "display_answer", "payload": "You are the Chameleon"}, to=player)
            else:
                emit("server_to_user", {"command": "display_answer", "payload": chosenAnswer}, to=player)

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