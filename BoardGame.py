#Example Flask App for a hexaganal tile game
#Logic is in this python file

from flask import Flask, render_template, jsonify
import  random
import  json
import  os

app = Flask(__name__) # type: ignore

# Keep track of the current player
current_player = 1


# Game state to store player positions and scores
game_state  = {
    "player 1": {"position": 0, "score": 0},
    "player 2": {"position": 0, "score": 0}
}

#   Events on the game board
events = {
    "3": "Hotel",
    "4": "Troll",
    "17": "Hotel",
    "20": "Troll"
}

# File to save game state
SAVE_FILE = "game_state.txt"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_tile')
def add_tile():
    global current_player
    color = 'green' if current_player == 1 else 'blue'  # Alternate between green and blue
    current_player = 2 if current_player == 1 else 1  # Switch to the other player
    return jsonify(color=color)

# Basic dice roll logic
@app.route('/roll_dice')
def roll_dice():
    global current_player
    player = "player " + str(current_player)
    roll = random.randint(1,6)
    game_state[player]["position"] += roll

    # Check for events
    position = str(game_state[player]["position"])
    if position in events:
        if events == "Hotel":
            game_state[player]["score"] += 5
        elif events == "Troll":
            game_state[player]["score"] -= 5
    else:
        event = "No event"

    # Switch player turn
    current_player = 2 if current_player == 1 else 1 

    return jsonify(player=player, roll=roll, event=event, game_state=game_state)

# Save game state to a file
@app.route('/save.game')
def save_game():
    with open(SAVE_FILE, "w") as file:
        file.write(str(current_player) + "\n")
        for player in game_state:
            file.write(player + "," + str(game_state[player]["position"]) + "," + str(game_state[player]["score"]) + "\n")
    return jsonify(message="Game saved!")

# Load game state from a file
@app.route('/load_game')
def load_game():
    global current_player
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            lines = file.readline()
            current_player = int(lines[0].strip())
            for line in lines[1:]:
                parts = line.strip().split(",")
                name = parts[0]
                position = int(parts[1])
                score = int(parts[2])
                game_state[name]["position"] = position
                game_state[name]["score"] = score
        return jsonify(message="Game loaded!", game_state=game_state)
    else:
        return jsonify(message="No save file found!")


if __name__ == "__main__":
    app.run(debug=True)
