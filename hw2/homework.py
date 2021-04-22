from itertools import chain
import copy
import time
import math
start_time = time.time()

# read file
input_file = open("input.txt", "r")
lines = input_file.readlines()
game_type = lines[0].replace('\n', '')
play_color = lines[1].replace('\n', '')
remaining_time = lines[2].replace('\n', '')
# convert text to 2d-array matrix
board_txt = lines[3:11]
board_matrix = []
for str_line in board_txt:
    square_line = []
    for str_square in str_line.replace('\n', ''):
        square_line.append(str_square)
    board_matrix.append(square_line)
board = {}

# create board according to file
for row_ind, row in enumerate(board_matrix):
    for col_ind, square in enumerate(row):
        board[(row_ind, col_ind)] = square


def jump(position, piece_type, parent):
    jump_down_left = (position[0] + 2, position[1] - 2)
    jump_down_right = (position[0] + 2, position[1] + 2)
    jump_up_left = (position[0] - 2, position[1] - 2)
    jump_up_right = (position[0] - 2, position[1] + 2)

    adj_down_left = (position[0] + 1, position[1] - 1)
    adj_down_right = (position[0] + 1, position[1] + 1)
    adj_up_left = (position[0] - 1, position[1] - 1)
    adj_up_right = (position[0] - 1, position[1] + 1)

    def down_left(pawn_color, king_color):
        if position[0] <= 5 and position[1] >= 2:
            if board[jump_down_left] == '.' and (board[adj_down_left] == pawn_color or board[adj_down_left] == king_color):
                # King can go forward and go back, so do not jump between two pieces endlessly
                if position not in parent.keys() or parent[position] != [jump_down_left]:
                    if jump_down_left not in parent.keys():
                        parent[jump_down_left] = [position]
                    else:
                        parent[jump_down_left].append(position)
                    jump(jump_down_left, piece_type, parent)

    def down_right(pawn_color, king_color):
        if position[0] <= 5 and position[1] <= 5:
            if board[jump_down_right] == '.' and (board[adj_down_right] == pawn_color or board[adj_down_right] == king_color):
                if position not in parent.keys() or parent[position] != [jump_down_right]:
                    if jump_down_right not in parent.keys():
                        parent[jump_down_right] = [position]
                    else:
                        parent[jump_down_right].append(position)
                    jump(jump_down_right, piece_type, parent)

    def up_left(pawn_color, king_color):
        if position[0] >= 2 and position[1] >= 2:
            if board[jump_up_left] == '.' and (board[adj_up_left] == pawn_color or board[adj_up_left] == king_color):
                if position not in parent.keys() or parent[position] != [jump_up_left]:
                    if jump_up_left not in parent.keys():
                        parent[jump_up_left] = [position]
                    else:
                        parent[jump_up_left].append(position)
                    jump(jump_up_left, piece_type, parent)

    def up_right(pawn_color, king_color):
        if position[0] >= 2 and position[1] <= 5:
            if board[jump_up_right] == '.' and (board[adj_up_right] == pawn_color or board[adj_up_right] == king_color):
                if position not in parent.keys() or parent[position] != [jump_up_right]:
                    if jump_up_right not in parent.keys():
                        parent[jump_up_right] = [position]
                    else:
                        parent[jump_up_right].append(position)
                    jump(jump_up_right, piece_type, parent)

    # black pawn jump
    if piece_type == 'b':
        down_left('w', 'W')
        down_right('w', 'W')
    # black king jump
    if piece_type == 'B':
        down_left('w', 'W')
        down_right('w', 'W')
        up_left('w', 'W')
        up_right('w', 'W')
    # white pawn jump
    if piece_type == 'w':
        up_left('b', 'B')
        up_right('b', 'B')
    # white king jump
    if piece_type == 'W':
        down_left('b', 'B')
        down_right('b', 'B')
        up_left('b', 'B')
        up_right('b', 'B')


def simple_move(position, piece_type):
    adj_down_left = (position[0] + 1, position[1] - 1)
    adj_down_right = (position[0] + 1, position[1] + 1)
    adj_up_left = (position[0] - 1, position[1] - 1)
    adj_up_right = (position[0] - 1, position[1] + 1)

    def down_left():
        if position[0] <= 6 and position[1] >= 1:
            if board[adj_down_left] == '.':
                piece_moves.append([position, adj_down_left])

    def down_right():
        if position[0] <= 6 and position[1] <= 6:
            if board[adj_down_right] == '.':
                piece_moves.append([position, adj_down_right])

    def up_left():
        if position[0] >= 1 and position[1] >= 1:
            if board[adj_up_left] == '.':
                piece_moves.append([position, adj_up_left])

    def up_right():
        if position[0] >= 1 and position[1] <= 6:
            if board[adj_up_right] == '.':
                piece_moves.append([position, adj_up_right])
    # black pawn simple move
    if piece_type == 'b':
        piece_moves = []
        down_left()
        down_right()
        return piece_moves
    # black king simple move
    if piece_type == 'B':
        piece_moves = []
        down_left()
        down_right()
        up_left()
        up_right()
        return piece_moves
    # white pawn simple move
    if piece_type == 'w':
        piece_moves = []
        up_left()
        up_right()
        return piece_moves
    # white king simple move
    if piece_type == 'W':
        piece_moves = []
        down_left()
        down_right()
        up_left()
        up_right()
        return piece_moves


# board-->{(row_ind, col_ind): square, (0, 0): '.', (0, 1): 'W',...}
def get_all_moves(board, pawn, king):
    moves = []
    for position, square in board.items():
        if square == pawn or square == king:
            ends = []
            parent = {}
            # check jump first
            jump(position, square, parent)
            if parent != {}:
                for point in set(parent.keys()):
                    if point not in list(chain.from_iterable(parent.values())):
                        ends.append(point)
                for end in ends:
                    v = end
                    move = [v]
                    while v != position:
                        v = parent[v][0]
                        move.append(v)
                    move.reverse()
                    moves.append(move)
                    if game_type == 'SINGLE':
                        return moves
    # if can not jump, check simple move
    if not moves:
        for position, square in board.items():
            if square == pawn or square == king:
                sim_move = simple_move(position, square)
                moves.extend(sim_move)
                if game_type == 'SINGLE':
                    return moves
    return moves


def update_board(board, move):
    # if jump move
    if abs(move[0][0] - move[1][0]) == 2:
        board[move[-1]] = board[move[0]]
        board[move[0]] = '.'
        for i in range(len(move)-1):
            mid_piece = (int((move[i][0] + move[i + 1][0]) / 2), int((move[i][1] + move[i + 1][1]) / 2))
            board[mid_piece] = '.'
    # if simple move
    else:
        board[move[-1]] = board[move[0]]
        board[move[0]] = '.'
    # crown
    if board[move[-1]] == 'b' and move[-1][0] == 7:
        board[move[-1]] = 'B'
    if board[move[-1]] == 'w' and move[-1][0] == 0:
        board[move[-1]] = 'W'
    return board


def evaluation(pawn, king, king_row_ind, deepest_depth_board):
    # count pieces of the board
    board_ = []
    piece_count = {'b': 0, 'B': 0, 'w': 0, 'W': 0}
    for i in range(8):
        board_.append(list(deepest_depth_board.values())[i * 8:(i * 8 + 8)])
    for row_ind, row in enumerate(board_):
        for col_ind, square in enumerate(row):
            if square == 'b':
                piece_count['b'] += 1
            elif square == 'B':
                piece_count['B'] += 1
            elif square == 'w':
                piece_count['w'] += 1
            elif square == 'W':
                piece_count['W'] += 1
            else:
                continue
    # number of pawn pieces
    num_pawn = piece_count[pawn]
    # number of king pieces
    num_king = piece_count[king]
    # number of pieces in the own king row
    num_king_row = 0
    for square in board_[king_row_ind]:
        if square == pawn or square == king:
            num_king_row += 1
    # number of pieces in the middle(2 row, 4 col) of the board
    num_mid_r_c_pieces = 0
    for square in list(chain(board_[3:5][0][2:6], board_[3:5][1][2:6])):
        if square == pawn or square == king:
            num_mid_r_c_pieces += 1
    # number of pieces in the middle 2 rows of the board
    num_mid_pieces = 0
    for square in list(chain(board_[3:5][0], board_[3:5][1])):
        if square == pawn or square == king:
            num_mid_pieces += 1
    # number of opponent's pawn
    if pawn == 'b':
        num_oppo_pawn = piece_count['w']
    else:
        num_oppo_pawn = piece_count['b']
    # number of opponent's king
    if king == 'B':
        num_oppo_king = piece_count['W']
    else:
        num_oppo_king = piece_count['B']
    # number of pieces on the 4 edges
    num_sides = 0
    for ind, row in enumerate(board_):
        for square in row:
            if (ind == 0 or ind ==7) and (square == pawn or square == king):
                num_sides += 1
            if ind != 0 and ind != 7 and (row[0] == pawn or row[0] == king or row[7] == pawn or row[7] == king):
                num_sides += 1
    eval_value = 5 * (num_pawn - num_oppo_pawn) + 8 * (num_king - num_oppo_king) + 4 * num_king_row + 2.5 * num_mid_r_c_pieces + 0.5 * num_mid_pieces + 2 * num_sides
    return eval_value


def max_value(state, alpha, beta):
    if state in point_value.keys():
        return point_value[state]
    v = -math.inf
    for successor in minimax_successors[state]:
        min_v = min_value(successor, alpha, beta)
        v = max(v, min_v)
        temp[successor] = min_v
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def min_value(state, alpha, beta):
    if state in point_value.keys():
        return point_value[state]
    v = math.inf
    for successor in minimax_successors[state]:
        v = min(v, max_value(successor, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


def alpha_beta_search(state):
    v = max_value(state, -math.inf, math.inf)
    for succesor in minimax_successors[(0, 0)]:
        if temp[succesor] == v:
            return succesor

# build minimax tree of moves and boards, minimax successors, and boards in different depths
depth = 0
depth_limit = 10
minimax_tree = {(0, 0): [board]}
minimax_successors = {}
boards = {depth: [board]}
if game_type == 'SINGLE':
    depth_limit = 2
for depth in range(depth_limit-1):
    depth += 1
    depth_boards = []
    for parent_board_ind_in_depth, _board in enumerate(boards[depth - 1]):
        if play_color == 'BLACK':
            if depth % 2 == 1:
                all_moves = get_all_moves(_board, 'b', 'B')
            else:
                all_moves = get_all_moves(_board, 'w', 'W')
        else:
            if depth % 2 == 1:
                all_moves = get_all_moves(_board, 'w', 'W')
            else:
                all_moves = get_all_moves(_board, 'b', 'B')
        parent_board = copy.deepcopy(_board)
        for move in all_moves:
            new_board = update_board(copy.deepcopy(parent_board), move)
            minimax_tree[(depth, len(depth_boards))] = (move, new_board)
            if (depth - 1, parent_board_ind_in_depth) not in minimax_successors.keys():
                minimax_successors[(depth - 1, parent_board_ind_in_depth)] = [(depth, len(depth_boards))]
            else:
                minimax_successors[(depth - 1, parent_board_ind_in_depth)].append((depth, len(depth_boards)))
            depth_boards.append(new_board)
        boards[depth] = depth_boards
point_value = {}
# get evaluation for leaves of the minimax tree
# minimax_tree[(depth, len(depth_boards))] = (move, new_board)
for board_ind in range(len(boards[depth_limit - 1])):
    if play_color == 'BLACK':
        evalu = evaluation('b', 'B', 0, minimax_tree[(depth_limit - 1, board_ind)][1])
    else:
        evalu = evaluation('w', 'W', -1, minimax_tree[(depth_limit - 1, board_ind)][1])
    point_value[(depth_limit - 1, board_ind)] = evalu
temp = {}
# choose a move to output
if game_type == 'GAME':
    successor = alpha_beta_search((0, 0))
    chosen_move = minimax_tree[successor][0]
else:
    chosen_move = all_moves[0]
# simple move to empty square or jump
if abs(chosen_move[0][0] - chosen_move[1][0]) == 1:
    move_type = 'E'
else:
    move_type = 'J'
# convert indice into position marks
pos = []
for i in ['8', '7', '6', '5', '4', '3', '2', '1']:
    for s in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
        pos.append(s + i)
index_pos = {}
for i in range(8):
    for j in range(8):
        index_pos[i, j] = pos[i * 8:(i * 8 + 8)][j]
# write file
f = open('output.txt', 'w')
for i in range(len(chosen_move) - 1):
    f.write(move_type + ' ' + index_pos[chosen_move[i]] + ' ' + index_pos[chosen_move[i + 1]] + '\n')
print("--- %s seconds ---" % (time.time() - start_time))


