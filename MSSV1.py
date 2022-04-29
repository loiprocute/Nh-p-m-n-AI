from numpy.core.fromnumeric import reshape, trace
from numpy.core.records import array
from   state import State
import copy
import numpy as np


  
def Minimax(curr_state:State,depth,player,MaximizingPlayer):
    if depth==0 or curr_state.game_over:
        return curr_state,evaluate(curr_state,player)
    if MaximizingPlayer:
        MaxValue = -10000
        best_move=None
        possible_move=curr_state.get_valid_moves
        for i in possible_move:
            tmp=copy.deepcopy(curr_state)
            tmp.act_move(i)
            #global_cells=[list(s) for s in tmp.global_cells.reshape(3,3)]
            value=Minimax(tmp,depth-1,-player, False)[1]#+eval_box(global_cells,player)
            MaxValue = max(MaxValue,value)
            if MaxValue == value:
                best_move=i
        return best_move, MaxValue
    else:
        MinValue = 10000
        possible_move=curr_state.get_valid_moves
        best_move=None
        for i in possible_move:
            tmp1=copy.deepcopy(curr_state)
            tmp1.act_move(i)
            #global_cells=[list(s) for s in tmp1.global_cells.reshape(3,3)]
            value=Minimax(tmp1,depth-1,-player, True)[1]#+eval_box(global_cells,player)
            MinValue = min(MinValue,value)
            if MinValue == value:
                best_move=i
        return best_move, MinValue

def evaluate(curr_state,player):
    Board=curr_state.blocks
    Score = get_score(Board,player)
    return Score

def get_score(board,player):
    score = 0
    board=[list(s) for s in board]
    for i in board:#blocks
        score += eval_box(i,player)
        
    return score

def eval_box(box,player):
    score = 0
    box=[list(i) for i in box]
    for row in box: #Score for each row
        score += count_score(row,player)

    for col in range(len(box)): #Score for each column
        check = []
        for row in box:
            check.append(box[col])
        score += count_score(box, player)

    #A score for each diagonal
    diags = [box[0][0],box[1][1],box[2][2]]
    score += count_score(diags, player)

    diags_2 = [box[2][0],box[1][1],box[0][2]]
    score += count_score(diags_2, player)

    if len(np.where(np.array(box)==0)[0]) == 0:
        score += 1


    return score

def count_score(array, player):
    score = 0

    if array.count(player) == 3:
        score += 100

    elif array.count(player) == 2:
        score += 50

    elif array.count(player) == 1:
        score += 20

    if array.count(-player) == 3:
        score -= 100

    elif array.count(-player) == 2:
        score -= 50

    if array.count(player) == 1 and array.count(-player) == 2:
        score += 10


    return score

def select_move(cur_state, remain_time):
    valid_moves = cur_state.get_valid_moves
    if cur_state.previous_move==None:
        return np.random.choice(valid_moves)
    if len(valid_moves) != 0:
        move=Minimax(cur_state,3,cur_state.player_to_move,True)
        return move[0]

    return None