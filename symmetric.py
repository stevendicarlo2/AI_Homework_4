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

    move = get_move_symmetric(info, prospects, opponent)
    info["last_opponent"] = opponent
    info["last_move"] = move
    save_data(info)

    return {
        "team-code": team_code,  # identifying team by the code assigned by game-program
        "move": move  # Can be 0 or 1 only
    }

def get_move_symmetric(info, prospects, opponent):
    if is_normal_cooperation(prospects):
        return tit_2_tats_move(prospects, info, opponent)
    else:
        return None

def save_data(data):
    return

def is_normal_cooperation(prospects):
    coop_value = max(prospects[0][0], prospects[1][1])
    min_other_move_value = min(prospects[0][1], prospects[1][0])
    return coop_value > min_other_move_value

def coop_move(prospects):
    move = 0 if prospects[0][0] > prospects[1][1] else 1
    return move

def tit_2_tats_move(prospects, info, opponent):
    coop = coop_move(prospects)
    bad = 1 if coop == 0 else 0
    opp_history = info["past_results"][opponent]
    if len(opp_history) < 2:
        return coop
    prev_turn = opp_history[-1]
    prev_turn_2 = opp_history[-2]
    if prev_turn[1] == bad and prev_turn_2[1] == bad:
        return bad
    else:
        return coop

def load_data():
    saved_info = {
        "past_results": {
            "opp1": [(0, 1, 5), (1, 1, 2), (1, 0, 3)],
            "opp2": []
        },
        "last_opponent": "opp2",
        "last_move": 0
    }
    return saved_info

sample_state = {
   "team-code": "eef8976e",
   "game": "sym",
   "opponent-name": "opp1",
   "prev-repetitions": 10, #Might be None if first game ever, or other number
   "last-opponent-play": 1, #0 or 1 depending on strategy played
   "last-outcome": 4, #Might be None if first game, or whatever outcome of play is
   "prospects": [
        [2,6],
        [3,2]
    ]
}
print(get_move(sample_state))



