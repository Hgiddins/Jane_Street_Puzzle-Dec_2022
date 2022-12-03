# die[1][0] will be used to represent the face up number on the die

# brd = [[57,33,132,268,492,732],
#          [81,123,240,443,353,508],
#          [186,42,195,704,452,228],
#          [-7,2,357,452,317,395],
#          [5,23,-4,592,445,620],
#          [0,77,32,403,337,452]]

import time,pickle
import time

start_time = time.time()



def show_board(board):
    for row in board:
        print(row)

def show_die():
    for row in die:
        print(row)

def left_roll():
#     middle row numbers all shift 1 left
    temp = die[1][0]
    die[1][0]=die[1][1]
    die[1][1]=die[1][2]
    die[1][2]=die[1][3]
    die[1][3]=temp

    new_die_position = (possible_moves[-1][0][0],possible_moves[-1][0][1]-1)
    return die, new_die_position

def right_roll():
#     middle row numbers all shift 1 right
    temp = die[1][3]
    die[1][3] = die[1][2]
    die[1][2] = die[1][1]
    die[1][1] = die[1][0]
    die[1][0] = temp

    new_die_position = (possible_moves[-1][0][0],possible_moves[-1][0][1]+1)
    return die, new_die_position


def up_roll():
#     on an up roll, items move between arrays. items at index 1 and 3 in the middle array are unchanged as they
#     are on the left and right sides of the die while the die is moved up
    temp = die[1][2]
    die[1][2] = die[0][0]
    die[0][0] = die[1][0]
    die[1][0] = die[2][0]
    die[2][0] = temp
    new_die_position = (possible_moves[-1][0][0]-1,possible_moves[-1][0][1])
    return die, new_die_position

def down_roll():
#     on an up roll, items move between arrays. items at index 1 and 3 in the middle array are unchanged as they
#     are on the left and right sides of the die while the die is moved up
    temp = die[2][0]
    die[2][0]=die[1][0]
    die[1][0]=die[0][0]
    die[0][0]=die[1][2]
    die[1][2]=temp
    new_die_position = (possible_moves[-1][0][0]+1,possible_moves[-1][0][1])
    return die, new_die_position

def calculate_valid_score_right():
    if len(possible_moves)>0:
        test_score = possible_moves[-1][4] + possible_moves[-1][3]*die[1][3] #old score + move_coint*next die face
        test_die_position = possible_moves[-1][0]
    else:
        test_score = die[1][3]
        test_die_position = die_position_0
    if test_score == board[test_die_position[0]][test_die_position[1] + 1]:
        return True
    else:
        return False

def calculate_valid_score_left():
    if len(possible_moves) > 0:
        test_score = possible_moves[-1][4] + possible_moves[-1][3]*die[1][1]
        test_die_position = possible_moves[-1][0]
    else:
        test_score = die[1][1]
        test_die_position = die_position_0
    if test_score == board[test_die_position[0]][test_die_position[1] - 1]:
        return True
    else:
        return False

def calculate_valid_score_up():
    if len(possible_moves) > 0:
        test_score = possible_moves[-1][4] + possible_moves[-1][3]*die[2][0] #old score + move_count*next die face
        test_die_position = possible_moves[-1][0]
    else:
        test_score = die[2][0]
        test_die_position = die_position_0

    if test_score == board[test_die_position[0] - 1][test_die_position[1]]:
        return True
    else:
        return False

def calculate_valid_score_down():
    if len(possible_moves) > 0:
        test_score = possible_moves[-1][4] + possible_moves[-1][3]*die[0][0]
        test_die_position = possible_moves[-1][0]
    else:
        test_score = die[0][0]
        test_die_position = die_position_0
    if test_score == board[test_die_position[0] + 1][test_die_position[1]]:
        return True
    else:
        return False


########################################################################################################################
# algorithm

success = False
failure = False

destination = (0,4)

# board = [[0,2],
#          [3,5]]
# board = [[0,0,0,0,130],
#          [0,0,0,84,98],
#          [0,0,33,48,0],
#          [0,10,13,0,0],
#          [0,2,0,0,0],]
board = [[0,0,0,0,130],
         [0,0,0,84,98],
         [0,0,33,48,0],
         [0,10,13,0,0],
         [0,2,0,0,0],]

die = [[3],
       [6,5,1,2],
       [4]]

die_position_0=[4,0]

move_count_0 = 1
score_0 = 0
delete_branch_0 = False

possible_moves = [] #die_position,moves,die,move_count,score

current_move_count = 0
current_score = 0



def check_conditions(die_position,move_count,score,delete_branch):
    global possible_moves

    if delete_branch:
        possible_moves = possible_moves[:-1]
        return possible_moves
    moves = []
    current_die = pickle.loads(pickle.dumps(die))
    possible_moves.append([die_position, moves, current_die, move_count, score])
    checks_clear = True
    return checks_clear

def check_surround_spaces(die_position,move_count,score,delete_branch):
    global possible_moves

    check = check_conditions(die_position, move_count, score, delete_branch)

    if check ==True:
        pass
    else:
        return check

    moves = []
    # RIGHT (fails when out of index (len(row)=pos index)
    if die_position[1] + 1 < len(board[0]):
        print('passes length check')
        if calculate_valid_score_right():
            print('passes score check')
            moves.append('right')

    # LEFT (ok when current position is > 0)
    if die_position[1] > 0:
        print('passes length check')
        if calculate_valid_score_left():
            print('passes score check')
            moves.append('left')

    # UP (ok when current position is > 0)
    if die_position[0] > 0:
        print('passes length check')
        if calculate_valid_score_up():
            print('passes score check')
            moves.append('up')

    # DOWN (fails when out of rows index (len(all rows)=pos index
    if die_position[0] + 1 < len(board):
        print('passes length check')
        if calculate_valid_score_down():
            print('passes score check')
            moves.append('down')
    possible_moves[-1][1] = moves



def make_move(possible_moves):
    if len(possible_moves) > 0:
        die = possible_moves[-1][2]
        die_position = possible_moves[-1][0]
        move_count = possible_moves[-1][3]
        score = possible_moves[-1][4]
        print(die_position)
        if len(possible_moves[-1][1])>0:
            if 'right' in possible_moves[-1][1]:
                possible_moves[-1][1].remove('right')
                roll_result = right_roll()
                die = roll_result[0]
                die_position = roll_result[1]
                score = score + move_count * die[1][0]
                move_count += 1
                print('MOVED RIGHT!')
                return die_position, move_count, score, False

            elif 'left' in possible_moves[-1][1]:
                possible_moves[-1][1].remove('left')
                roll_result = left_roll()
                die = roll_result[0]
                die_position = roll_result[1]
                score = score + move_count * die[1][0]
                move_count += 1
                die_position
                print('MOVED LEFT!')
                return die_position, move_count, score, False

            elif 'down' in possible_moves[-1][1]:
                possible_moves[-1][1].remove('down')
                roll_result = down_roll()
                die = roll_result[0]
                die_position = roll_result[1]
                score = score + move_count * die[1][0]
                move_count += 1
                die_position
                print('MOVED DOWN!')
                return die_position, move_count, score, False

            elif 'up' in possible_moves[-1][1]:
                possible_moves[-1][1].remove('up')
                roll_result = up_roll()
                die = roll_result[0]
                die_position = roll_result[1]
                score = score + move_count * die[1][0]
                move_count += 1
                die_position
                print('MOVED UP!')
                return die_position, move_count, score, False

        else:
            #there are no possible moves in last branch so we must delete it and try cycle again
            return die_position, move_count, score, True
    # there are no more moves for this die. we need to return input for the check_surround_spaces function that will
    # trigger it to realise there are no more moves. for this purpose we will set moves =0
    die_position = die_position_0
    return die_position, 0, 0, False


def ending():
    global failure
    global success

    if len(possible_moves) == 0:
        print('this die has no solution')
        failure = True
        return

    test_position = possible_moves[-1][0]
    if test_position == destination:
        print('this die is solved!')
        success = True
        return


print(possible_moves)
check_surround_spaces(die_position_0, move_count_0, score_0, delete_branch_0)

while success == False and failure == False:
    output = make_move(possible_moves)
    check_surround_spaces(output[0], output[1], output[2], output[3])
    print(possible_moves)
    ending()


print('-------------------------------------')
print("--- %s seconds ---" % (time.time() - start_time))





# while len(possible_moves[0][1])>0:
#     check_surround_spaces(make_move(possible_moves))




