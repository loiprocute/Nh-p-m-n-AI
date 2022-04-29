from numpy.core.fromnumeric import reshape, trace
from numpy.core.records import array
from  state import *
import copy
import numpy as np

def Minimax(alpha,beta ,curr_state:State,depth,player,MaximizingPlayer,count_time):
    if depth==0 or curr_state.game_over:
        return evaluate(curr_state,player)
    if time.time() - count_time > 5:
        return evaluate(curr_state,player)
    if MaximizingPlayer:
        MaxValue = -1000000
        possible_move=curr_state.get_valid_moves
        for i in possible_move:
            tmp=copy.deepcopy(curr_state)
            tmp.act_move(i)
        
            value=Minimax(alpha,beta ,tmp,depth-1,player, True,count_time)
           
            if MaxValue < value:
                MaxValue = value
            alpha = max(alpha, value)
                    
            if beta <= alpha:
                break
        return  MaxValue
    else:
        MinValue = 1000000
        possible_move=curr_state.get_valid_moves
        for i in possible_move:
            tmp1=copy.deepcopy(curr_state)
            tmp1.act_move(i)
            value=Minimax(alpha,beta ,tmp1,depth-1,player, False,count_time)

            if MinValue > value:
                MinValue = value
            beta = min(beta, value)
                    
            if beta <= alpha:
                break
        return  MinValue
    
def find_best_move(cur_state: State):
    bestvalue = -1000000
    valid_moves = cur_state.get_valid_moves
    best_move = np.random.choice(valid_moves)
    depth=4
    count_time=time.time()
    alpha = -1000000
    beta = 1000000
    player_init = cur_state.player_to_move
    for move in valid_moves:
        temp = copy.deepcopy(cur_state)
        temp.act_move(move)
        value =Minimax(alpha,beta ,temp,depth-1,player_init, False,count_time)
        if (value > bestvalue):
            bestvalue = value
            best_move = move
        if beta <= alpha:
            break
    return best_move    


    
def evaluate(curr_state: State,player):
    if curr_state.game_over:
        return curr_state.game_result(curr_state.global_cells.reshape(3,3)) * player * 100000
    score = get_score(curr_state,player)
    return score

def get_score(curr_state: State,player):
    score = 0
    board=curr_state.blocks
    #board=[list(s) for s in board]
    if curr_state.global_cells[4]==player:
        score+=20
    elif curr_state.global_cells[4]==-player:
        score-=20
    for i in board:#blocks
        if (len(np.where(i==0)[0])==9 ) or (len(np.where(i==0)[0])==0):
            continue
        if curr_state.game_result(i) != None:
            score += curr_state.game_result(i) * player * 20
            continue  
        score += eval_box(list(i),player)
    score+= eval_box(curr_state.global_cells.reshape(3,3),player) * 7
    return score

def eval_box(box,player):
    score = 0
    
    if box[1][1] == player:
        score+=2
    elif box[1][1] == -player:
        score-=2
    '''if box[0][0]==player:
        score +=0.5
    elif  box[0][0]== -player: 
        score -=0.5
    
    if box[0][2]==player:
        score +=0.5
    elif  box[0][2]== -player: 
        score -=0.5
        
    if box[2][2]==player:
        score +=0.5
    elif  box[2][2]== -player: 
        score -=0.5
        
    if box[2][0]==player:
        score +=0.5
    elif  box[2][0]== -player: 
        score -=0.5
     '''   
    box=[list(i) for i in box]
    for row in box: #Score for each row
        score += count_score(row,player)
    for col in range(len(box)): #Score for each column
        check = []
        for row in box:
            check.append(row[col])
        score += count_score(check, player)
    #A score for each diagonal
    diags = [box[0][0],box[1][1],box[2][2]]
    score += count_score(diags, player)
    diags_2 = [box[2][0],box[1][1],box[0][2]]
    score += count_score(diags_2, player)

    return score

def count_score(array, player):

    score = 0

    if array.count(player) == 2 and  array.count(-player)==0:
        score += 4
    if  array.count(player) == 1 and  array.count(-player)==2:
        score += 4


    if array.count(-player) == 2 and array.count(player) == 0:
        score -= 4
    if array.count(player) == 2 and  array.count(-player)==1:
        score -= 4

        
    return score


def select_move(cur_state: State, remain_time):
    if cur_state.previous_move == None:
        return UltimateTTT_Move(4,1,1,cur_state.player_to_move)
    if len(cur_state.get_valid_moves) !=0:
        return find_best_move(cur_state)
    return None

