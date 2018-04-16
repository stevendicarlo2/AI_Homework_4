TEAM_NAME = "mighty_ducks" #Pick a team name
MEMBERS = ["snd7nb", "yq4du"] #Include a list of your members’ UVA IDs

def get_move(state):
    team_code = state["team-code"]
    opponent = state["opponent-name"]
    last_opp_play = state["last-opponent-play"]
    last_outcome = state["last-outcome"]
    prospects = state["prospects"]

    info = load_data()
    if info == {}:
        info = {"past_results": {}}
    else:
        last_opp = info["last_opponent"]
        last_move = info["last_move"]
        info["past_results"][last_opp].append((last_move, last_opp_play, last_outcome))

    if opponent not in info["past_results"]:
        info["past_results"][opponent] = []

    move = get_move_symmetric(info, prospects)
    info["last_opponent"] = opponent
    info["last_move"] = move
    save_data(info)

    return {
        "team-code": team_code,  # identifying team by the code assigned by game-program
        "move": move  # Can be 0 or 1 only
    }

def get_move_symmetric(info, prospects):
    return 1

def save_data(data):
    return

def load_data():
    saved_info = {
        "past_results": {
            "opp1": [(0, 1, 5), (1, 1, 2)],
            "opp2": []
        },
        "last_opponent": "opp2",
        "last_move": 0
    }
    return saved_info

sample_state = {
   "team-code": "eef8976e",
   "game": "sym",
   "opponent-name": "mighty-ducks",
   "prev-repetitions": 10, #Might be None if first game ever, or other number
   "last-opponent-play": 1, #0 or 1 depending on strategy played
   "last-outcome": 4, #Might be None if first game, or whatever outcome of play is
   "prospects": [
        [4,5],
        [3,2]
    ]
}




