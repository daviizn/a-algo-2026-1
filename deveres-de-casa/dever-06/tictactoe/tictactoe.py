"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Conta o número de X's e O's no tabuleiro
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    # X começa, então se há mesmo número de jogadas, é turno do X
    # Se há um X a mais, é turno do O
    return X if x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    
    # Verifica se a ação é válida
    if board[i][j] != EMPTY:
        raise Exception("Invalid action")
    
    # Cria uma cópia profunda do tabuleiro
    new_board = copy.deepcopy(board)
    
    # Faz a jogada do jogador atual
    player_turn = player(board)
    new_board[i][j] = player_turn
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Verifica linhas
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    
    # Verifica colunas
    for col in range(3):
        if (board[0][col] == board[1][col] == board[2][col] and 
            board[0][col] is not None):
            return board[0][col]
    
    # Verifica diagonais
    if (board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None):
        return board[0][0]
    
    if (board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None):
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Verifica se há vencedor
    if winner(board) is not None:
        return True
    
    # Verifica se o tabuleiro está cheio
    return all(cell != EMPTY for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Se o jogo terminou, retorna None
    if terminal(board):
        return None
    
    # Inicializa com a primeira ação possível
    current_player = player(board)
    best_action = None
    best_value = -math.inf if current_player == X else math.inf
    
    # Avalia todas as ações possíveis
    for action in actions(board):
        new_board = result(board, action)
        value = min_value(new_board) if current_player == X else max_value(new_board)
        
        if current_player == X and value > best_value:
            best_value = value
            best_action = action
        elif current_player == O and value < best_value:
            best_value = value
            best_action = action
    
    return best_action


def max_value(board):
    """
    Função auxiliar para o nó MAX do Minimax (turno do X).
    """
    if terminal(board):
        return utility(board)
    
    value = -math.inf
    for action in actions(board):
        value = max(value, min_value(result(board, action)))
    
    return value


def min_value(board):
    """
    Função auxiliar para o nó MIN do Minimax (turno do O).
    """
    if terminal(board):
        return utility(board)
    
    value = math.inf
    for action in actions(board):
        value = min(value, max_value(result(board, action)))
    
    return value