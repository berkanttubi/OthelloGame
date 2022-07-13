
from cmath import inf
from copy import deepcopy
import time
node_count=0 # For counting the number of nodes
actions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1,1)] # For finding the neighboors


def create_board():

    '''
        This function creates the board with its initial position.
        #return : board
    '''
    board = [['-' for x in range(8)] for y in range(8)]
    board[3][3] = 'W'
    board[3][4] = 'B'
    board[4][3] = 'B'
    board[4][4] = 'W'

    return board

def print_board(board):
    
    '''
        This function displays the board.
        #input: board
    '''

    print("  1  2  3  4  5  6  7  8")
    counter1=1
    counter2=1
    for i in range(1,9):
        print(counter1,end=" ")
        counter1+=1
        for j in range(1,9):
            print(board[i-1][j-1],end="  ")
        print(counter2)
        counter2+=1

    print("  1  2  3  4  5  6  7  8")


def play_move(board,move,color):

        '''
            This function plays the move and checks the capturings.
            #input: 
                board : game board
                move: Coordinates of the place (tupple)
                color: 'W' or 'B'
            
            #return: board
        
        '''
    
        board[move[0]][move[1]] = color

        board = horizontal_capture(board,move,color)
        board = diagonal_capture(board,move,color)
        board = vertical_capture(board,move,color)
        return board


def horizontal_capture(board,move,color):
    '''
            This function checks the horizontal captures and flips the pieces.
            #input: 
                board : game board
                move: Coordinates of the place (tupple)
                color: 'W' or 'B'
            
            #return: board
        
        '''
    flip_list=list()

    for i in range(move[1],7):
        state = board[move[0]][i+1]
        if state=="-":
            break
        elif state==color:
            for points in flip_list:
                board[points[0]][points[1]] = color
                        

        else:
            flip_list.append([move[0],i+1])

    for i in range(move[1],0,-1):
        state = board[move[0]][i-1]
        if state=="-":
            break
        elif state==color:
            for points in flip_list:
                board[points[0]][points[1]] = color
                        

        else:
            flip_list.append([move[0],i-1])

    return board
    
def vertical_capture(board,move,color):
    '''
            This function checks the vertical captures and flips the pieces.
            #input: 
                board : game board
                move: Coordinates of the place (tupple)
                color: 'W' or 'B'
            
            #return: board
        
    '''
    flip_list=list()

    for i in range(move[0],7):
        state = board[i+1][move[1]]
        if state=="-":
            break
        elif state==color:
            for points in flip_list:
                board[points[0]][points[1]] = color        

        else:
            flip_list.append([i+1,move[1]])

    for i in range(move[0],0,-1):
        state = board[i-1][move[1]]
        if state=="-":
            break
        elif state==color:
            for points in flip_list:
                board[points[0]][points[1]] = color        

        else:
            flip_list.append([i-1,move[1]])
    
    return board
                
def diagonal_capture(board,move,color):
    '''
            This function checks the diagonal captures and flips the pieces.
            #input: 
                board : game board
                move: Coordinates of the place (tupple)
                color: 'W' or 'B'
            
            #return: board
        
        '''
    flip_list=list()
    j = move[1]
    for i in range(move[0],7):
            if i>=7 or j>=7:
                continue
            state = board[i+1][j+1]
            if state=="-":
                break
            elif state==color:
                for points in flip_list:
                    board[points[0]][points[1]] = color        
            else:
                flip_list.append([i+1,j+1])
            j+=1
    flip_list=list()
    j = move[1]
    for i in range(move[0],7):
            if i>=7:
                continue
            state = board[i+1][j-1]
            if state=="-":
                break
            elif state==color:
                for points in flip_list:
                    board[points[0]][points[1]] = color        
            else:
                flip_list.append([i+1,j-1])
            j-=1
    flip_list=list()
    j = move[1]
    for i in range(move[0],0,-1):
            if j<=0:
                continue
            state = board[i-1][j-1]
            if state=="-":
                break
            elif state==color:
                for points in flip_list:
                    board[points[0]][points[1]] = color        
            else:
                flip_list.append([i-1,j-1])
            j-=1
    flip_list=list()
    j = move[1]
    for i in range(move[0],1,-1):
            if i<=0 or j>=7:
                continue
            state = board[i-1][j+1]
            if state=="-":
                break
            elif state==color:
                for points in flip_list:

                    board[points[0]][points[1]] = color        
            else:
                flip_list.append([i-1,j+1])
            j+=1
    return board

def heuristic_one(board,position):
    '''
        This heuristics calculates the difference of scores. Maximum Disk Strategy

        #input:
            board : the game board
            position: dummy value

        #return: heuristic value 
    '''
    w_number = 0
    b_number = 0
    for i in range(8):
        for j in range(8):
            if board[i][j]=='W':
                w_number+=1
            elif board[i][j]=='B':
                b_number+=1
    
    heuristic = w_number-b_number
    return heuristic

def heuristic_two(board,move):
    '''
        This heuristics gives values to each grid. Positional Strategy

        #input:
            board : the game board
            position: coordinates of the move (tupple)
            
        #return: heuristic value 
    '''

    SQUARE_WEIGHTS = [
        4,   -3,   2,   2,   2,   2,   -3,   4,
        -3, -4,   -1,  -1,   -1,   -1,  -4, -3,
        2,  -1,    1,   0,    0,   1,   -1,   2, 
        2,  -1,    0,   1,    1,   0,   -1,   2,
        2,  -1,    0,   1,    1,   0,   -1,   2,
        2,  -1,    1,   0,    0,   1,   -1,   2,
        -3,  -4,   -1,  -1,   -1,   -1,  -4,  -3,
        4,   -3,   2,   2,    2,    2,   -3,   4  
    ]

    xy = move[0]*7+move[1]

    return SQUARE_WEIGHTS[xy]



def find_possible_states(board):
    '''
        This function finds the possible states the can be played in each turn.

        #input: board

        #return: possible states (list)
    
    
    '''
    letter_positions = list()
    states = list()
    for i in range(8):
        for j in range(8):
            if board[i][j]!='-':
                letter_positions.append([i,j])
    
    for x,y in letter_positions:
        validation,places = valid_place(board,x,y)

        if validation:
            for i in places:
                if i not in states:
                    states.append(i)
        
    return states


def valid_place(board,x,y):
    '''
        This function is helping to find_possible_states() function. It checks the states of the board
        whether it is valid or not.

        #input:
            board: the game board
            x: x coordinate
            y: y coordinate
        
        #return: boolean and states

    '''
    validation = 0
    states = list()
    for direction_x,direction_y in actions:
        if helper_validation(board,x,y,direction_x,direction_y):
            states.append([x+direction_x,y+direction_y])
            validation=1

    if validation:
        return True, states
    else:
        return False, states
def helper_validation(board,x,y,direction_x,direction_y):

    '''
        This function checks whether position is valid or not. It is helper for valid_place() function.

        #input: 
            board: the game board
            x: x coordinate
            y: y coordinate
            direction_x : x coordinate of neighboor
            direction_y : y coordinate of neighboor
        
        #return : bool
    '''

    if (x+direction_x <0) or (x+direction_x>7) : # Out of the board
        return False
    if (y+direction_y <0) or (y+direction_y>7) : # Out of the board
        return False
    
    if board[x+direction_x][y+direction_y]!='-':
        return False
    return True


def is_board_full(board):

    '''
        This function checks whether board is full or not.

        #input: board
        #output: bool

    '''
    empty=0
    for i in range(8):
        for j in range(8):
            if board[i][j]=='-':
                empty = 1
                return 0
    
    if empty==0:
        return 1


node_count=0
def miniMax_with_pruning(position,board,alpha,beta,maximizePlayer,heuristic,color,depth=4):
    '''
        This function applies the minimax algorithm with alpha-beta pruning.

        #input:
            position: Played position
            board: The game board
            alpha-beta: Parameter for pruning
            maximizePlayer: boolean for algorithm
            heuristic: The heuristic function
            color: 'W' or 'B'
            depth: depth of tree

        #output: maximum heuristic value and position
        
    '''

    global node_count
    node_count+=1
    if depth==0 or is_board_full(board):
        return heuristic(board,position),position
    
    states = find_possible_states(board)
    best_move = states[0]

    if maximizePlayer:
        maximumEvaluation = -inf
        for state in states:
            board_copy = deepcopy(board)
            board_copy = play_move(board_copy,[state[0],state[1]],color)
            eval,_ = miniMax_with_pruning(state,board_copy,alpha,beta,False,heuristic,'W',depth-1)
            if eval> maximumEvaluation:
                maximumEvaluation = eval
                best_move = state
            alpha = max(alpha,eval)
            if beta<=alpha:
                break
        return maximumEvaluation,best_move
    else:
        minimumEvaluation = inf
        for state in states:
            board_copy = deepcopy(board)
            board_copy = play_move(board_copy,[state[0],state[1]],color)
            eval,_= miniMax_with_pruning(state,board_copy,alpha,beta,True,heuristic,'B',depth-1)
            if eval< minimumEvaluation:
                minimumEvaluation = eval
                best_move = state
            beta = min(beta,eval)
            if beta<=alpha:
                break

        return minimumEvaluation,best_move
        

def play_computer(board,color,heuristic):
    '''
        This function plays the computer turn.

        #input:
            board: The game board
            color: 'W' or 'B'
            heuristic: The heuristic function

        #return: board

    '''
    global node_count
    node_count = 0
    if color=="W":
        _,move = miniMax_with_pruning([2,2],board,-inf,inf,True,heuristic,color)
    else:
        _,move = miniMax_with_pruning([2,2],board,-inf,inf,False,heuristic,color)
    board = play_move(board,move,color)
    print("NODE: ",node_count)
    return board


    
def game_over(board):
    '''
        This function checks whether game is over or not.

        #param: board
        #retrun: bool
    '''
    for i in range(8):
        for j in range(8):
            if board[i][j]=='-':
                return 0
    return 1

def winner(board):

    '''
        This function determines the winner.

        #param: board
    
    '''

    w_number = 0
    b_number = 0
    for i in range(8):
        for j in range(8):
            if board[i][j]=='W':
                w_number+=1
            elif board[i][j]=='B':
                b_number+=1
    if w_number>b_number:
        print("W WINS")
    else:
        print("B WINS")

if __name__ == '__main__':
    board= create_board()


    print("Welcome to the Othello Game!")
    ans = input("Please choose the mode: Computer vs Computer (1) | Computer vs Human (2): ")
    heuristic_input = input("Please choose the mode heuristic:   Maximum Disks Strategy(1) |  Positional Strategy(2): ")
    if heuristic_input=="1":
        heuristic = heuristic_one
    else:
        heuristic = heuristic_two
        
    while(True):

        if ans=='2':
            print_board(board)
            if game_over(board):
                winner(board)
                break
            print("Hmm nice move... Let me think about it!")
            board=play_computer(board,'W',heuristic)
            if game_over(board):
                winner(board)
                break
            print_board(board)
            x=int(input("Enter row: "))
            y=int(input("Enter column:"))
            board=play_move(board,[x-1,y-1],'B')
            
        else:
            time.sleep(0.5)
            print_board(board)
            if game_over(board):
                winner(board)
                break
            board=play_computer(board,'W',heuristic)
            if game_over(board):
                winner(board)
                break
            time.sleep(0.5)
            print_board(board)
            board=play_computer(board,'B',heuristic)
        
        