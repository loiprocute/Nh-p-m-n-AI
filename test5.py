from state import State, UltimateTTT_Move
import numpy as np
import time
from copy import deepcopy
from agent import *

def isEmpty(cur_state: State, index_local_board):
    board = cur_state.blocks[index_local_board]
    indices = np.where(board == 0)
    if (len(indices[0]) == 9):
        return True
    return False

def isFull(cur_state: State, index_local_board):
    board = cur_state.blocks[index_local_board]
    indices = np.where(board == 0)
    if (len(indices[0]) != 0):
        return False
    return True


def evaluateBoard(board, player_init): 
    # good for 'O' => minus
    # good for 'X' => add
    #vertical
    sum = 0
    for i in range(3):
        if (board[0,i] == 1 and board[1, i] == 1) or (board[0,i] == 1 and board[2, i] == 1) or (board[2,i] == 1 and board[1, i] == 1):
            # if (board[0,i] == 1 and board[1, i] == 1 and board[2,i] == 1):
            #     sum += 5
            if(board[0,i] == -1 or board[1, i] == -1 or board[2,i] == -1):
                sum -= 2
            if(board[0,i] == 0 or board[1, i] == 0 or board[2,i] == 0):
                sum += 2
    
    for i in range(3):
        if (board[0,i] == -1 and board[1, i] == -1) or (board[0,i] == -1 and board[2, i] == -1) or (board[2,i] == -1 and board[1, i] == -1):
            # if (board[0,i] == -1 and board[1, i] == -1 and board[2,i] == -1):
            #     sum -= 5
            if(board[0,i] == 1 or board[1, i] == 1 or board[2,i] == 1):
                sum += 2
            if(board[0,i] == 0 or board[1, i] == 0 or board[2,i] == 0):
                sum -= 2

    #horizontal
    for i in range(3):
        if (board[i,0] == 1 and board[i,1] == 1) or (board[i,0] == 1 and board[i,2] == 1) or (board[i,2] == 1 and board[i,1] == 1):
            # if (board[i,0] == 1 and board[i,1] == 1 and board[i,2] == 1):
            #     sum += 5
            if(board[i,0] == -1 or board[i,1] == -1 or board[i,2] == -1):
                sum -= 2
            if(board[i,0] == 0 or board[i,1] == 0 or board[i,2] == 0):
                sum += 2

    for i in range(3):
        if (board[i,0] == -1 and board[i,1] == -1) or (board[i,0] == -1 and board[i,2] == -1) or (board[i,2] == -1 and board[i,1] == -1):
            # if (board[i,0] == -1 and board[i,1] == -1 and board[i,2] == -1):
            #     sum -= 5
            if(board[i,0] == 1 or board[i,1] == 1 or board[i,2] == 1):
                sum += 2
            if(board[i,0] == 0 or board[i,1] == 0 or board[i,2] == 0):
                sum -= 2
    
    #diagnosed right
    if (board[0,0] == 1 and board[1,1] == 1) or (board[0,0] == 1 and board[2,2] == 1) or (board[2,2] == 1 and board[1,1] == 1):
        # if (board[0,0] == 1 and board[1,1] == 1 and board[2,2] == 1):
        #     sum += 5
        if(board[0,0] == -1 or board[1,1] == -1 or board[2,2] == -1):
            sum -= 2
        if(board[0,0] == 0 or board[1,1] == 0 or board[2,2] == 0):
            sum += 2

    if (board[0,0] == -1 and board[1,1] == -1) or (board[0,0] == -1 and board[2,2] == -1) or (board[2,2] == -1 and board[1,1] == -1):
        # if (board[0,0] == -1 and board[1,1] == -1 and board[2,2] == -1):
        #     sum -= 5
        if(board[0,0] == 1 or board[1,1] == 1 or board[2,2] == 1):
            sum += 2
        if(board[0,0] == 0 or board[1,1] == 0 or board[2,2] == 0):
            sum -= 2
            
    #diagnosed left
    if(board[0,2] == 1 and board [1,1] == 1) or (board[0,2] == 1 and board[2,0] == 1) or (board[2,0] == 1 and board[1,1] == 1):
        # if (board[0,2] == 1 and board[1,1] == 1 and board [2,0] == 1):
        #     sum += 5
        if(board[0,2] == -1 or board[1,1] == -1 or board [2,0] == -1):
            sum -= 2
        if(board[0,2] == 0 or board[1,1] == 0 or board [2,0] == 0):
            sum += 2


    if(board[0,2] == -1 and board [1,1] == -1) or (board[0,2] == -1 and board[2,0] == -1) or (board[2,0] == -1 and board[1,1] == -1):
        # if (board[0,2] == -1 and board[1,1] == -1 and board [2,0] == -1):
        #     sum -= 5
        if(board[0,2] == 1 or board[1,1] == 1 or board [2,0] == 1):
            sum += 2
        if(board[0,2] == 0 or board[1,1] == 0 or board [2,0] == 0):
            sum -= 2
    
    if board[1,1] == 1:
        sum += 1
    elif board[1,1] == -1:
        sum -= 1
    return sum * player_init


def evaluate(cur_state: State, player_init):            #evaluate each board + winning small board + winning big board
    if cur_state.game_over:
        return cur_state.game_result(cur_state.global_cells.reshape(3,3)) * player_init * 99999
    sum = 0
    # player = cur_state.player_to_move
    for i in range(9):
        if isFull(cur_state, i) or isEmpty(cur_state, i):
            continue

        board = cur_state.blocks[i]
        if cur_state.game_result(board) != None:
            sum += cur_state.game_result(board) * player_init * 15
            continue                # need to check back, could be a bonus

        sum += evaluateBoard(board, player_init)

    sum += evaluateBoard(cur_state.global_cells.reshape(3,3), player_init) * 5 
    return sum

def alpha_beta(cur_state: State,player_init, s_time, alpha, beta, max_or_min, depth, limit):
    #alpha is min, beta is max
    #max_or_min, 1 if max, -1 if min
    if depth > limit or cur_state.game_over:
        return evaluate(cur_state, player_init) # evaluate function
    if time.time() - s_time > 5:
        return evaluate(cur_state,player_init)

    if max_or_min == 1:
        maxScore = -99999
        valid_moves = cur_state.get_valid_moves
        for move in valid_moves:
            clone = deepcopy(cur_state)
            clone.act_move(move)
            score = alpha_beta(clone, player_init,s_time,alpha, beta,  max_or_min * -1, depth + 1, limit)
            maxScore = max(maxScore, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return maxScore
    else:
        minScore = 99999
        valid_moves = cur_state.get_valid_moves
        for move in valid_moves:
            clone = deepcopy(cur_state)
            clone.act_move(move)
            score = alpha_beta(clone, player_init, s_time, alpha, beta, max_or_min * -1, depth + 1, limit)
            minScore = min(minScore, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return minScore


def bestMove(cur_state: State):
    bestScore = -99999
    valid_moves = cur_state.get_valid_moves
    best_move = np.random.choice(valid_moves)
    player_init = cur_state.player_to_move
    s_time = time.time()
    alpha = -99999
    beta = 99999
    for move in valid_moves:
        clone = deepcopy(cur_state)
        clone.act_move(move)
        score = alpha_beta(clone, player_init,s_time, alpha, beta,max_or_min = -1, depth = 1, limit=4)
        if (score > bestScore):
            bestScore = score
            best_move = move
        if beta <= alpha:
            break
    return best_move    



def select_move(cur_state: State, remain_time):
    if cur_state.previous_move == None:
        return UltimateTTT_Move(4,1,1,cur_state.player_to_move)
    return bestMove(cur_state)
