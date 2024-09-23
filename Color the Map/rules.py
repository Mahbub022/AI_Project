import math
import random
import pygame
from interface import SHAPES, BOARD_SIZE, PLAYER1_COLOR, PLAYER2_COLOR
#random.seed(42)


def minimax(board, depth, alpha, beta, maximizing_player, player_color):
    
    if depth == 0 or is_game_over(board):
        return evaluate_board(board, player_color)

    if maximizing_player:
        max_eval = float('-inf')
        for move in get_all_possible_moves(board, player_color):
            eval = minimax(make_move(board, move, player_color), depth - 1, alpha, beta, False, toggle_player(player_color))
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_all_possible_moves(board, toggle_player(player_color)):
            eval = minimax(make_move(board, move, toggle_player(player_color)), depth - 1, alpha, beta, True, toggle_player(player_color))
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


# Example of using the Minimax function
def best_move_for_ai(board, player_color, depth=3):
    best_score = float('-inf')
    best_move = None
    for move in get_all_possible_moves(board, player_color):
        new_board = make_move(board.copy(), move, player_color)
        score = minimax(new_board, depth, float('-inf'), float('inf'), False, toggle_player(player_color))
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def show_endgame_popup(screen, winner, player1_points, player2_points):
    """Show the endgame popup with the result of the game."""
    pygame.font.init()
    font = pygame.font.Font(None, 48)

    # Define the message text
    if winner == PLAYER1_COLOR:
        lines = [
            "Player Wins!",
            f"Points: {player1_points}"
        ]
    elif winner == PLAYER2_COLOR:
        lines = [
            "AI Wins!",
            f"Points: {player2_points}"
        ]
    else:
        lines = [
            "It's a Tie!",
            f"Player Points: {player1_points}",
            f"AI Points: {player2_points}"
        ]

    # Render the message text
    screen.fill((255, 255, 255))  # White background

    text_surfaces = [font.render(line, True, (0, 0, 0)) for line in lines]
    total_height = sum(surf.get_height() for surf in text_surfaces)
    start_y = (screen.get_height() // 2) - (total_height // 2)

    for text_surface in text_surfaces:
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, start_y))
        screen.blit(text_surface, text_rect)
        start_y += text_surface.get_height() + 10  # Space between lines

    pygame.display.flip()

    # Wait for a bit to show the message
    pygame.time.wait(2000)  # Wait for 2 seconds

def is_shape_complete(board, row, col, coords, player_color):
    """Check if the shape is complete at the given position on the board for the given player color."""
    return all(
        0 <= row + dr < BOARD_SIZE and
        0 <= col + dc < BOARD_SIZE and
        board[row + dr][col + dc] == player_color
        for dr, dc in coords
    )

def check_shapes(board, row, col, player_color):
    """Check all possible shapes and calculate points for a move at the given position on the board."""
    points = 0

    for shape_name, (coords, base_points) in SHAPES.items():
        # Check if the shape can be formed with the current move
        for dr, dc in coords:
            start_row = row - dr
            start_col = col - dc
            
            if 0 <= start_row < BOARD_SIZE and 0 <= start_col < BOARD_SIZE:
                if is_shape_complete(board, start_row, start_col, coords, player_color):
                    points += base_points * (
                        1 if shape_name == 'L*1:' else
                        2 if shape_name == 'Box*2:' else
                        3
                    )
                    break  # No need to check other positions for the same shape

    return points


def evaluate_move(board, row, col, player_color):
    """Evaluate a move based on the potential points for making a shape and blocking Player 1."""
    opponent_color = PLAYER1_COLOR if player_color == PLAYER2_COLOR else PLAYER2_COLOR
    
    # Evaluate move for AI (shape completion)
    board[row][col] = player_color
    move_points = check_shapes(board, row, col, player_color)
    board[row][col] = None
    
    # Evaluate move for Player 1 (blocking)
    board[row][col] = opponent_color
    block_points = check_shapes(board, row, col, opponent_color)
    board[row][col] = None

    return move_points, block_points

# def best_move_for_ai(board, player_color):
#     """Determine the best move for the AI player based on making a shape and blocking Player 1."""
#     best_move = None
#     best_score = -1  # Start with a very low score
    
#     for row in range(BOARD_SIZE):
#         for col in range(BOARD_SIZE):
#             if board[row][col] is None:
#                 move_points, block_points = evaluate_move(board, row, col, player_color)
                
#                 # Combine move points and block points to score the move
#                 score = move_points + block_points  # You can weight these differently if needed
                
#                 if score > best_score:
#                     best_score = score
#                     best_move = (row, col)
    
#     return best_move

def calculate_shape_completion(board, row, col, coords, player_color):
    completed_cells = 0
    total_cells = len(coords)
    
    for dr, dc in coords:
        if 0 <= row + dr < BOARD_SIZE and 0 <= col + dc < BOARD_SIZE and board[row + dr][col + dc] == player_color:
            completed_cells += 1
            
    return (completed_cells / total_cells) * 100


def check_partial_shapes(board, row, col, player_color):
    points = 0

    for shape_name, (coords, base_points) in SHAPES.items():
        # Check if the shape can be formed with the current move
        for dr, dc in coords:
            start_row = row - dr
            start_col = col - dc
            
            if 0 <= start_row < BOARD_SIZE and 0 <= start_col < BOARD_SIZE:
                completion_percentage = calculate_shape_completion(board, start_row, start_col, coords, player_color)
                points += (completion_percentage / 100) * base_points

    return points


def fuzzyLogic(board, player_color, opponent_color, empty, points):
    #membership for board state
    board_state = {}
    if 0<=empty<=30:
        board_state["full"] = 1
        board_state["medium"] = 0
        board_state["empty"] = 0
    elif 30<empty<35:
        board_state["full"] = (35-empty)/5
        board_state["medium"] = (empty-30)/5
        board_state["empty"] = 0
    elif 35<=empty<=70:
        board_state["full"] = 0
        board_state["medium"] = 1
        board_state["empty"] = 0
    elif 70<empty<75:
        board_state["full"] = 0
        board_state["medium"] = (75-empty)/5
        board_state["empty"] = (empty-70)/5
    elif 75<=empty<=100:
        board_state["full"] = 0
        board_state["medium"] = 0
        board_state["empty"] = 1
    
    #membership for point diff
    point_diff = {}
    if 0<=points<=15:
        point_diff["low"] = 1
        point_diff["medium"] = 0
        point_diff["high"] = 0
    elif 15<points<20:
        point_diff["low"] = (20-points)/5
        point_diff["medium"] = (points-15)/5
        point_diff["high"] = 0
    elif 20<=points<=30:
        point_diff["low"] = 0
        point_diff["medium"] = 1
        point_diff["high"] = 0
    elif 30<points<35:
        point_diff["low"] = 0
        point_diff["medium"] = (35-points)/5
        point_diff["high"] = (points-30)/5
    elif 35<=points<=100:
        point_diff["low"] = 0
        point_diff["medium"] = 0
        point_diff["high"] = 1
    
    #rules evaluation
    move = {}
    move["offensive"] = max(min(board_state["empty"],point_diff["low"]),
                            min(board_state["empty"],point_diff["high"]),
                            min(board_state["medium"],point_diff["low"]),
                            min(board_state["medium"],point_diff["high"]),
                            min(board_state["full"],point_diff["low"]),
                            min(board_state["full"],point_diff["high"]))
    
    move["deffensive"] = max(min(board_state["empty"],point_diff["medium"]),
                             min(board_state["medium"],point_diff["medium"]),
                             min(board_state["full"],point_diff["medium"]))
    
    centroid = (0+10+20)*move["offensive"]+(30+40+50)*move["deffensive"]/(3*(move["offensive"]+move["deffensive"]))

    if 0<=centroid<=20:
        place_color = player_color
    elif 20<=centroid<=50:
        place_color = opponent_color
    print(place_color)

    if place_color == player_color:
        opposite_color = opponent_color
    elif place_color == opponent_color:
        opposite_color = player_color

    position = geneticAlgo(board,place_color,opposite_color,empty)
    return position

#genetic algorithm
def convert(cromosome):
    binary_str = ''.join(map(str, cromosome))
    dec = int(binary_str, 2)
    return dec

def population(length):
    cromosome = []
    cr = 0
    while cr<10:
        list = []
        for li in range(7):
            list.append(random.randint(0,1))

        if convert(list)<length:
            cromosome.append(list)
            cr = cr+1
    return cromosome


def fitness(cromosome, points):
    fitValue = []
    for cr in cromosome:
        conv = convert(cr)
        #print(f"convert(cr) = {conv}, len(points) = {len(points)}")
        
        if conv<len(points):
            fitValue.append(points[conv])
        else:
            fitValue.append(0)

    sumVal = sum(fitValue)
    probValue = []
    expectValue = []
    expectCount = []
    value = 0
    eval = 0
    fcount = []
    for fvalue in fitValue:
        if sumVal != 0:
            value = fvalue/sumVal
        else:
            value = 0
        probValue.append(value)
        eval = value*10
        expectValue.append(eval)
        count = int(eval)
        fcount.append(eval-count)
        expectCount.append(count)

    while sum(expectCount) != 10:
        expectCount[fcount.index(max(fcount))] +=1

    return expectCount, fitValue

def selection(actualCount,cromosome):
    new_cromosome = []
    count = actualCount[:]
    for indx in range(10):
        while(count[indx] > 0):
            new_cromosome.append(cromosome[indx])
            count[indx] = count[indx]-1

    return new_cromosome

def crossover(new_cromosome,crosspoint):
    cross = new_cromosome.copy()
    id1=0
    while id1<9:
        id2 = id1+1
        for i in range(7):
            if i >= crosspoint:
                tmp = cross[id1][i]
                cross[id1][i] = cross[id2][i]
                cross[id2][i] = tmp
        id1 = id2+1
    return cross

def mutation(crosscr,length):
    mutat = crosscr.copy()
    indx = []
    for i in range(5):
        indx.append(random.randint(0,9))
    id = 0
    while id < len(indx):
        pos = random.randint(0,4)
        mutat[indx[id]][pos] = 1 - crosscr[indx[id]][pos]
        if convert(mutat[indx[id]])<length:
            id = id+1
    return mutat



def validity(cromosome,length):
    for cr in cromosome:
        if length<=convert(cr):
            print("Invalid ",length,convert(cr))        
        # print("Cromosome",cr,convert(cr))


def geneticAlgo(board,player_color,opponent_color,length):
    board_position = []
    points = []
    if  length<2:
        return (row,col) (
            board[row][col] == None
            for row in range(BOARD_SIZE)
            for col in range(BOARD_SIZE)
        )

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == None:
                board[row][col] = player_color
                board_position.append([row,col])
                move = check_partial_shapes(board,row,col,player_color)
                board[row][col] = None
                # board[row][col] = opponent_color
                # block = check_partial_shapes(board,row,col,opponent_color)
                # board[row][col] = None
                # points.append(move+block)
                points.append(move)
    for i in range(len(board_position)):
        print(board_position[i],points[i])
    cromosome = population(len(points)-1)
    # print("out ",length,len(points))
    # print("Cromosme->",len(cromosome),len(points))
 
    # validity(cromosome,len(points))

    actualCount, fitValue = fitness(cromosome,points)
    #print("Count->",len(cromosome),len(actualCount),actualCount)
    best_s = -99
    best_cr = []

    cnt = 1

    while best_s<max(points) and cnt<100:

        new_cromosome = selection(actualCount,cromosome)
        crosspoint = random.randint(2,6)
        crosscr = crossover(new_cromosome,crosspoint)
        #print(len(crosscr))
        mutat = mutation(crosscr,len(points)-1)
        
        cnt += 1
        cromosome = mutat[:]
        # validity(cromosome,len(points))
        # print("in ",length,len(points))
        actualCount, fitValue = fitness(cromosome,points)
        maxfit = max(fitValue)
        if maxfit>best_s:
            best_s = maxfit
            best_cr = cromosome[fitValue.index(maxfit)] 
    print("Best-> ",board_position[convert(best_cr)],points[convert(best_cr)],best_s,convert(best_cr))
    return (board_position[convert(best_cr)])
def evaluate_board(board, player_color):
    
    pass

def is_game_over(board):
    """
    Check if the game is over.
    """
    # Implement your logic to check for game over
    pass

def get_all_possible_moves(board, player_color):
    """
    Generate all possible moves for the given player.
    """
    # Implement logic to generate moves
    pass

def make_move(board, move, player_color):
    """
    Make a move on the board and return the new board state.
    """
    # Implement the move logic
    pass

def toggle_player(player_color):
    """
    Toggle the player from PLAYER1_COLOR to PLAYER2_COLOR or vice versa.
    """
    return PLAYER2_COLOR if player_color == PLAYER1_COLOR else PLAYER1_COLOR
