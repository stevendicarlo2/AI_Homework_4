TEAM_NAME = "yungAIthugz" #Pick a team name
MEMBERS = ["snd7nb", "yq4du"] #Include a list of your members’ UVA IDs

def get_move(state):
    try:
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
    except:
        move = 0
        team_code = state["team-code"]
    return {
        "team-code": team_code,  # identifying team by the code assigned by game-program
        "move": move  # Can be 0 or 1 only
    }

def get_move_symmetric(info, prospects, opponent):
    past_results = info["past_results"]
    if len(past_results) >= 20:
        trial_range = get_range(past_results, opponent)
        cutoff = trial_range[0] + .75*(trial_range[1]-trial_range[0])
        turns_so_far = len(past_results[opponent])
        dom_strat = dom_strategy(prospects)
        if turns_so_far >= int(cutoff) and dom_strat is not None:
            print("using dom_strat")
            return dom_strat

    if is_normal_cooperation(prospects):
        return tit_2_tats_move(prospects, info, opponent)
    else:
        return no_coop_move(prospects, info, opponent)

def get_range(past_results, opponent):
    game_lengths = []
    for opp, results in past_results.items():
        if opp != opponent:
            game_lengths.append(len(results))
    return min(game_lengths), max(game_lengths)

def dom_strategy(prospects):
    if prospects[0][0] >= prospects[1][0] and prospects[0][1] >= prospects[1][1]:
        return 0
    elif prospects[1][0] >= prospects[0][0] and prospects[1][1] >= prospects[0][1]:
        return 1
    else:
        return None

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

def no_coop_move(prospects, info, opponent):
    opp_history = info["past_results"][opponent]
    optimal_move = 0 if prospects[0][0] > prospects[1][1] else 1
    if len(opp_history) < 1:
        return optimal_move
    last_opp_move = opp_history[-1][1]
    move = 1 if last_opp_move == 0 else 0
    return move

