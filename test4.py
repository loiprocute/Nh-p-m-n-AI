from numpy.core.fromnumeric import reshape, trace
from numpy.core.records import array
from  state import *
import copy
import numpy as np

def evaluate_move(curr_state: State,move:UltimateTTT_Move,player):
    score=0
    if move.value==player :
        if curr_state.game_result(curr_state.blocks[move.index_local_board]) != None :
            score-=2
        '''if len(np.where(curr_state.blocks[move.index_local_board]!=0)[0])==0:
            score+=4'''
    if move.value==-player :
        if curr_state.game_result(curr_state.blocks[move.index_local_board]) != None :
            score+=2
        '''if len(np.where(curr_state.blocks[move.index_local_board]!=0)[0])==0:
            score-=4'''
    return score

def Minimax(alpha,beta ,curr_state:State,depth,player,MaximizingPlayer,count_time):
    if depth==0 or curr_state.game_over:
        #print(curr_state.blocks)
        return curr_state.previous_move, evaluate(curr_state,player)
    if time.time() - count_time > 4:
        return curr_state.previous_move,evaluate(curr_state,player)
    if MaximizingPlayer:
        MaxValue = -1000000
        possible_move=curr_state.get_valid_moves
        #best_move=np.random.choice(possible_move)
        best_move=None
        for i in possible_move:
            score_move=evaluate_move(curr_state,i,player)
            tmp=copy.deepcopy(curr_state)
            tmp.act_move(i)
            #print(tmp.blocks)
            value=Minimax(alpha,beta ,tmp,depth-1,player,False,count_time)[1]+score_move
        
            if MaxValue < value:
                MaxValue = value
                best_move=i
            alpha = max(alpha, value)
                    
            if beta <= alpha:
                break

        return best_move, MaxValue
    else:
        MinValue = 1000000
        possible_move=curr_state.get_valid_moves
        #best_move=np.random.choice(possible_move)
        best_move=None
        for i in possible_move:
            score_move=evaluate_move(curr_state,i,player)
            tmp1=copy.deepcopy(curr_state)
            tmp1.act_move(i)
            value=Minimax(alpha,beta ,tmp1,depth-1,player, True,count_time)[1]+score_move

            if MinValue > value:
                MinValue = value
                best_move=i
            beta = min(beta, value)
                    
            if beta <= alpha:
                break

        return best_move, MinValue
      
    
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
        score+=15
    elif curr_state.global_cells[4]==-player:
        score-=15 
    for i in board:#blocks
        if (len(np.where(i==0)[0])==9 ) or (len(np.where(i==0)[0])==0):
            continue
        if curr_state.game_result(i) != None:
            score += curr_state.game_result(i) * player * 15
            continue  
        score += eval_box(list(i),player)
    score+= eval_box(curr_state.global_cells.reshape(3,3),player) * 5
    return score

def eval_box(box,player):
    score = 0
    
    if box[1][1] == player:
        score+=1
    elif box[1][1] == -player:
        score-=1
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
        score += 2
    if  array.count(player) == 1 and  array.count(-player)==2:
        score += 2


    if array.count(-player) == 2 and array.count(player) == 0:
        score -= 2
    if array.count(player) == 2 and  array.count(-player)==1:
        score -= 2

        
    return score

def count_empty(blocks):
    count=0
    for i in range(9):
        block=blocks[i]
        count += len(np.where(block ==0)[0])
    return count

def select_move(cur_state, remain_time):
    empty=count_empty(cur_state.blocks)
    #print('empty: ',empty)
    if empty<=81 and empty>75:
        depth=3
    if empty<=75 and empty>65:
        depth=4
    if empty<=65 and empty> 40:
        depth=5
    elif empty<=40 and empty>30:
        depth=6
    elif empty<=30 and empty>20:
        depth=7
    elif empty<=20 and empty>10:
        depth=8
    else:
        depth=10

    start_time = time.time() 
    if cur_state.previous_move == None:
        return UltimateTTT_Move(4, 1, 1, cur_state.player_to_move)
    valid_moves = cur_state.get_valid_moves
    alpha=-1000000
    beta=1000000
    if len(valid_moves) != 0:
        best_move = Minimax(alpha,beta,cur_state, depth,cur_state.player_to_move, True, start_time)
        end_time=time.time()
        print('time :',round(end_time-start_time,3))
        return best_move[0]
    return None
