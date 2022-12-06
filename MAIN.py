# JANE STREET'S MONTHLY PUZZLE
# DECEMBER 2022: DIE AGONY

########################################################################################################################
# INITIAL PARAMETERS
########################################################################################################################

import time, pickle
start_time = time.time()

success = False
failure = False

die_position_0=[5,0]
destination = (0,5)

board = [[57,33,132,268,492,732],
         [81,123,240,443,353,508],
         [186,42,195,704,452,228],
         [-7,2,357,452,317,395],
         [5,23,-4,592,445,620],
         [0,77,32,403,337,452]]

# The representation of a die can be best understand spatially as a cube-net
# die[1][0] will be used to represent the face up number on the die
die_0 = [[0],
         [0,0,0,0],
         [0]]

move_count_0 = 1
score_0 = 0

history = [] # This stores info about the die's journey thus far: die_position,moves,die,move_count,score
delete_branch_0 = False

current_move_count = 0
current_score = 0



########################################################################################################################
# DICE ROLLING: Geometric representation of orthogonal movements
########################################################################################################################

def show_board(board):
    for row in board:
        print(row)

def left_roll(die):
    temp = die[1][0]
    die[1][0]=die[1][1]
    die[1][1]=die[1][2]
    die[1][2]=die[1][3]
    die[1][3]=temp

    new_die_position = (history[-1][0][0], history[-1][0][1]-1)
    return die, new_die_position

def right_roll(die):
    temp = die[1][3]
    die[1][3] = die[1][2]
    die[1][2] = die[1][1]
    die[1][1] = die[1][0]
    die[1][0] = temp

    new_die_position = (history[-1][0][0], history[-1][0][1]+1)
    return die, new_die_position


def up_roll(die):
    temp = die[1][2]
    die[1][2] = die[0][0]
    die[0][0] = die[1][0]
    die[1][0] = die[2][0]
    die[2][0] = temp
    new_die_position = (history[-1][0][0]-1, history[-1][0][1])
    return die, new_die_position

def down_roll(die):
    temp = die[2][0]
    die[2][0]=die[1][0]
    die[1][0]=die[0][0]
    die[0][0]=die[1][2]
    die[1][2]=temp
    new_die_position = (history[-1][0][0]+1, history[-1][0][1])
    return die, new_die_position



########################################################################################################################
# HELPER FUNCTIONS: condition checking
########################################################################################################################

def calculate_valid_score_right():
    the_die = history[-1][2]
    if the_die[1][3] == 0:
        test_die_position = history[-1][0]

        new_side = board[test_die_position[0]][test_die_position[1] + 1] - history[-1][4]
        new_side = new_side / history[-1][3]
        x = new_side % 1
        if x == 0:

            return True  # we may just need to return the adjusted die object
        else:
            return False
    if len(history) > 0:
        test_score = history[-1][4] + history[-1][3] * the_die[1][3]  # old score + move_count*next die face
        test_die_position = history[-1][0]
    else:
        test_score = the_die[1][3]
        test_die_position = die_position_0
    if test_score == board[test_die_position[0]][test_die_position[1] + 1]:
        return True
    else:
        return False


def calculate_valid_score_left():
    the_die = history[-1][2]
    if the_die[1][1] == 0:
        test_die_position = history[-1][0]

        new_side = board[test_die_position[0]][test_die_position[1] - 1] - history[-1][4]
        new_side = new_side / history[-1][3]
        x = new_side % 1
        if x == 0:
            return True  # we may just need to return the adjusted die object
        else:
            return False

    if len(history) > 0:
        test_score = history[-1][4] + history[-1][3] * the_die[1][1]
        test_die_position = history[-1][0]
    else:
        test_score = the_die[1][1]
        test_die_position = die_position_0
    if test_score == board[test_die_position[0]][test_die_position[1] - 1]:
        return True
    else:
        return False

def calculate_valid_score_up():
    the_die = history[-1][2]
    if the_die[2][0] == 0:
        test_die_position = history[-1][0]

        new_side = board[test_die_position[0] - 1][test_die_position[1]] - history[-1][4]
        new_side = new_side / history[-1][3]
        x = new_side % 1
        if x == 0:
            return True  # we may just need to return the adjusted die object
        else:
            return False

    if len(history) > 0:
        test_score = history[-1][4] + history[-1][3] * the_die[2][0]  # old score + move_count*next die face
        test_die_position = history[-1][0]
    else:
        test_score = the_die[2][0]
        test_die_position = die_position_0

    if test_score == board[test_die_position[0] - 1][test_die_position[1]]:
        return True
    else:
        return False

def calculate_valid_score_down():
    the_die = history[-1][2]
    if the_die[0][0] == 0:
        test_die_position = history[-1][0]
        new_side = board[test_die_position[0] + 1][test_die_position[1]] - history[-1][4]
        new_side = new_side / history[-1][3]
        x = new_side % 1
        if x == 0:
            return True  # we may just need to return the adjusted die object
        else:
            return False

    if len(history) > 0:
        test_score = history[-1][4] + history[-1][3] * the_die[0][0]
        test_die_position = history[-1][0]
    else:
        test_score = the_die[0][0]
        test_die_position = die_position_0
    if test_score == board[test_die_position[0] + 1][test_die_position[1]]:
        return True
    else:
        return False

def check_conditions(die_position,move_count,score,delete_branch, test_die):
    global history
    global tests
    if delete_branch:
        history = history[:-1]
        print('MOVED BACK!')
        return history
    moves = []
    current_die = pickle.loads(pickle.dumps(test_die))
    history.append([die_position, moves, current_die, move_count, score])
    checks_clear = True
    return checks_clear



########################################################################################################################
# THE ALGORITHM
#
#    - This algorithm procedurally generates the values on each side of the die whilst adapting Trémaux's maze-solving
#      algorithm to ensure the correct path is eventually found:

#       1. Checks what valid moves are open to the die.
#       2. If the value on the upright face of the die is currently empty then it will assign it the required value to
#          make an attempted move valid. Thus, it procedurally works out the sides of the die.
#       3. Makes a move. This involves, adding the new position and orientation of the die (and score and moves) to the
#          history. It also involves deleting the option of making that move from the history so that if the node is
#          revisited it will not try the same move twice.
#       4. If a dead-end is reached then the last visited node (square on the board) is deleted from the history until
#          a node is reached where there is an available move to make. Then the process repeats.

########################################################################################################################

def check_surround_spaces(die_position,move_count,score,delete_branch, test_die):
    global history

    check = check_conditions(die_position, move_count, score, delete_branch, test_die)

    if check ==True:
        pass
    else:
        return check

    moves = []
    # RIGHT (fails when out of index (len(row)=pos index)
    if die_position[1] + 1 < len(board[0]):
        # print('passes length check')
        if calculate_valid_score_right():
            # print('passes score check')
            moves.append('right')

    # LEFT (ok when current position is > 0)
    if die_position[1] > 0:
        # print('passes length check')
        if calculate_valid_score_left():
            # print('passes score check')
            moves.append('left')

    # UP (ok when current position is > 0)
    if die_position[0] > 0:
        # print('passes length check')
        if calculate_valid_score_up():
            # print('passes score check')
            moves.append('up')

    # DOWN (fails when out of rows index (len(all rows)=pos index
    if die_position[0] + 1 < len(board):
        # print('passes length check')
        if calculate_valid_score_down():
            # print('passes score check')
            moves.append('down')
    history[-1][1] = moves



def make_move(history):
    test_die = pickle.loads(pickle.dumps(history[-1][2]))
    die_position = history[-1][0]
    move_count = history[-1][3]
    score = history[-1][4]

    if len(history) > 0:
        if len(history[-1][1])>0:
            if 'right' in history[-1][1]:

                if test_die[1][3] == 0:
                    test_die_position = history[-1][0]
                    new_side = board[test_die_position[0]][test_die_position[1] + 1] - history[-1][4]
                    new_side = new_side / history[-1][3]
                    x = new_side % 1
                    if x == 0 and int(new_side) != 0:
                        test_die[1][3] = int(new_side)

                if test_die[1][3] != 0:
                    history[-1][1].remove('right')
                    roll_result = right_roll(test_die)
                    test_die = roll_result[0]
                    die_position = roll_result[1]
                    score = score + move_count * test_die[1][0]
                    move_count += 1

                    print('MOVED RIGHT!')

                    return die_position, move_count, score, False, test_die


            elif 'left' in history[-1][1]:

                if test_die[1][1] == 0:
                    test_die_position = history[-1][0]

                    new_side = board[test_die_position[0]][test_die_position[1] - 1] - history[-1][4]
                    new_side = new_side / history[-1][3]
                    x = new_side % 1

                    if x == 0 and int(new_side) != 0:
                        test_die[1][1] = int(new_side)

                if test_die[1][1] != 0:
                    history[-1][1].remove('left')
                    roll_result = left_roll(test_die)
                    test_die = roll_result[0]
                    die_position = roll_result[1]
                    score = score + move_count * test_die[1][0]
                    move_count += 1

                    print('MOVED LEFT!')
                    return die_position, move_count, score, False, test_die

            elif 'down' in history[-1][1]:

                if test_die[0][0] == 0:
                    test_die_position = history[-1][0]

                    new_side = board[test_die_position[0] + 1][test_die_position[1]] - history[-1][4]
                    new_side = new_side / history[-1][3]
                    x = new_side % 1
                    if x == 0 and int(new_side)!=0:
                        test_die[0][0] = int(new_side)

                if test_die[0][0] != 0:
                    history[-1][1].remove('down')
                    roll_result = down_roll(test_die)
                    test_die = roll_result[0]
                    die_position = roll_result[1]
                    score = score + move_count * test_die[1][0]
                    move_count += 1

                    print('MOVED DOWN!')
                    return die_position, move_count, score, False, test_die

            elif 'up' in history[-1][1]:

                if test_die[2][0] == 0:
                    test_die_position = history[-1][0]

                    new_side = board[test_die_position[0] - 1][test_die_position[1]] - history[-1][4]
                    new_side = new_side / history[-1][3]
                    x = new_side % 1
                    if x == 0 and int(new_side)!=0:
                        test_die[2][0] = int(new_side)

                if test_die[2][0] != 0:
                    history[-1][1].remove('up')
                    roll_result = up_roll(test_die)
                    test_die = roll_result[0]
                    die_position = roll_result[1]
                    score = score + move_count * test_die[1][0]
                    move_count += 1

                    print('MOVED UP!')
                    return die_position, move_count, score, False, test_die

        else:
            #there are no possible moves in last branch, so we must delete it and try cycle again
            return die_position, move_count, score, True, test_die

    # there are no possible moves in last branch, so we must delete it and try cycle again
    return die_position, move_count, score, True, test_die



########################################################################################################################
# ENDING FEATURES
########################################################################################################################

def amend_board():
    last_move = [0, 0]
    for move in history:
        position = move[0]
        board[position[0]][position[1]] = 'x'
        last_move = position



def ending():
    global failure
    global success

    if len(history) == 0:
        print('***NO SOLUTION EXISTS***')
        failure = True
        return

    test_position = history[-1][0]
    if test_position == destination:
        print('***DESTINATION REACHED***')
        success = True
        return

def show_path(history):
    path = []
    for i in history:
        path.append(i[0])
    return path



########################################################################################################################
# RUN
########################################################################################################################

# Initialise history for first square with initial inputs
check_surround_spaces(die_position_0, move_count_0, score_0, delete_branch_0,die_0)
print('Path:', show_path(history))

# Run the algorithm until the path is found
while success == False and failure == False:
    output = make_move(history)
    check_surround_spaces(output[0], output[1], output[2], output[3],output[4])
    print('Path:', show_path(history))
    print(' ')
    ending()



########################################################################################################################
# PATH & TIME
########################################################################################################################

amend_board()
print('-------------------------------------')
print('Squares visited: x')

show_board(board)
print('-------------------------------------')
print("--- %s seconds ---" % (time.time() - start_time))






