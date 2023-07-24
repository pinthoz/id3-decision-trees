import random
import time
import math
from copy import deepcopy
import sys
from id3_connect4 import *

NUM_ROWS = 6
NUM_COLS = 7

class State: 
    
    def __init__(self):
        # inicializa o estado do jogo
        self.board = [[0]*NUM_COLS for i in range(NUM_ROWS)] # [[0,0,0,...], [0,0,0,...], ...] estado inicial do tabuleiro (sem pecas)
        self.column_heights = [NUM_ROWS-1] * NUM_COLS # [5, 5, 5, 5, 5, 5, 5] index da proxima linha vazia de cada coluna
        self.available_moves = list(range(7)) # [0, 1, ..., 6] lista das colunas que ainda podem ser jogadas
        self.player = 1
        self.winner = -1 # -1 -> sem vencedor (durante o jogo), 0 -> empate, 1 -> jogador 1 ganhou, 2 -> jogador 2 ganhou
        
    #========================================================================================================================================#
    
    def check_line(self, row, col, dx, dy):
        # verifica se ha 4 pecas do mesmo jogador em linha
        player = self.board[row][col]
        if player == 0:
            return False

        for i in range(1, 4):
            if (row + i * dy >= NUM_ROWS or row + i * dy < 0 or
                col + i * dx >= NUM_COLS or col + i * dx < 0 or
                self.board[row + i * dy][col + i * dx] != player):
                return False
        return True
    
    #========================================================================================================================================#
        
    def move(self, column): 
        # funcao que executa um movimento dado o numero da coluna e retorna o novo estado
        # atualiza a lista de movimentos disponiveis, alturas das colunas, a vez do jogador e verifica se ha vencedores

        state_copy = deepcopy(self)
        
        height = state_copy.column_heights[column]
        state_copy.column_heights[column] = height
        state_copy.board[height][column] = self.player
        
        if height == 0: # se a altura da coluna for 0 (so tem uma posicao disponivel nessa coluna), remove a coluna da lista de movimentos disponiveis
            state_copy.available_moves.remove(column)
        else: # atualiza a altura da coluna
            state_copy.column_heights[column] = height - 1
        
        # verifica se ha vencedor e altera a vez do jogador
        state_copy.update_winner() 
        state_copy.player = 3 - self.player # atualiza a vez do jogador (1 -> (3-1) = 2, 2 -> (3-2) = 1)
        
        return state_copy
        

    #========================================================================================================================================#
 
    def update_winner(self):
        # funcao que verifica se ha vencedor e atualiza o atributo winner
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if (self.check_line(row, col, 1, 0) or
                    self.check_line(row, col, 0, 1) or
                    self.check_line(row, col, 1, 1) or
                    self.check_line(row, col, 1, -1)):
                    self.winner = self.board[row][col]
                    return

        if len(self.available_moves) == 0:
            self.winner = 0

#########################################################################################################################################  

class ConnectFourGame:
    
    def __init__(self, player_1_, player_2_):
        self.state = State() # estado inicial
        self.player_1_ = player_1_ # jogador 1
        self.player_2_ = player_2_ # jogador 2
        
    def start(self):
        self.state = State()
        self.print_state()
        while True:

            if self.state.player == 1:
                print("  It is now 'X' turn.")
                self.player_1_(self)
            else:
                print("   It is now 'O' turn.")
                self.player_2_(self)
            
            self.print_state()
            

            if self.state.winner != -1:
                break
       
        if self.state.winner == 0:
            print("\t End of game! Draw!\n")
        else:
            print(f"\t End of game! Player {self.state.winner} wins!\n")
        
    
#########################################################################################################################################

    # funcao que imprime o estado do jogo
    def print_state(self):   
        for i in range(6):
            print("\t", end="")
            for j in range(7):
                piece = ""
                if (self.state.board[i][j]) == 1:
                    piece = "X"
                elif (self.state.board[i][j]) == 2:
                    piece = "O"
                else:
                    piece = "-"
                print("| " + str(piece), end=" ")
            print("|")
            
        print("\t+---+---+---+---+---+---+---+")
        print("\t  1   2   3   4   5   6   7 ")
        print()
        
#########################################################################################################################################   

def player_move(game):
    # funcao que executa o movimento do jogador humano
    # se o input for invalido, pede novamente um input valido
    
    move = (input("  Make a move by choosing your coordinates to play (1 to 7) : "))
    while (not move.isdigit()) or (int(move) < -1 or int(move) > 7) or ( int(move) - 1 not in game.state.available_moves):
        move = (input("  Make a move by choosing your coordinates to play (1 to 7) : "))
    print("\n")
    game.state = game.state.move(int(move) -1)
    
    
#########################################################################################################################################

# funcao que avalia o estado do jogo
def evaluate_func(state):
    global labels,Root
    prediction_ex = {}
    index = 0
    # comeca no (5,0)
    for col in range(7):
        for row in range(5,-1,-1):
            space = state.board[row][col]
            #print(str(row) + " " + str(col) + " " + str(space))
            if space == 0:
                prediction_ex[labels[index]] = 'b'
            elif space == 1:
                prediction_ex[labels[index]] = 'x'
            elif space == 2:
                prediction_ex[labels[index]] = 'o'
                
            index += 1

    #print(prediction_ex)
    prediction = predict_example(prediction_ex, Root)
    #print(prediction)
    if prediction == 'win':
        return -1
    if prediction == 'loss':
        return 1
    if prediction == 'draw':
        return 0    
 
    
    
#########################
#                       #
# IMPLEMENTACAO DO MTCS #
#                       #
#########################

#executa o movimento do mcts
def execute_mcts_move(lim):
    def execute_mcts_move_aux(game):
        print("   Thinking...\n")
        start_time = time.time()
        move_choice = MCTSPlayer(lim).select_move(game.state,game.state.player)
        move= move_choice[0]
        n_rollouts = move_choice[1]       
        game.state = game.state.move(move)
        end_time = time.time()
        print(f"   MCTS Move: Column {move + 1} selected in {(end_time - start_time):.4}s")
        print(f'\t     Number of Rollouts: {n_rollouts}\n')
        
    return execute_mcts_move_aux

#========================================================================================================================================#

# no do MCTS
class MCTSNode:
    global LIM
    # state -> estado do jogo
    # parent -> no pai
    # children -> dicionario com os filhos: chave -> movimento, valor -> no filho
    # wins -> numero de vitorias
    # visits -> numero de visitas
    # untried_moves -> lista com os movimentos nao testados
    def __init__(self, state, parent=None): 
        self.state = state
        self.parent = parent
        self.children = {}
        self.wins = 0
        self.visits = 0
        self.untried_moves = state.available_moves.copy()

    def UCT_select_child(self, c=3):
        # usa a formula UCT para selecionar o filho
        # c -> constante de exploracao
        # devolve o no filho com maior pontuacao UCT
        if LIM > 4:
            c = 4
        
        best_child = None
        best_score = -1
        for move, child_node in self.children.items():
            UCT_score = child_node.wins / child_node.visits + c * math.sqrt(math.log(self.visits) / child_node.visits)
            if UCT_score > best_score:
                best_child = child_node
                best_score = UCT_score
        return best_child

    def expand(self):
        # Escolhe um movimento que ainda nao foi tentado e cria o filho
        move = random.choice(self.untried_moves)
        new_state = self.state.move(move)
        new_node = MCTSNode(new_state, self)
        self.children[move] = new_node
        self.untried_moves.remove(move)
        return new_node

    def back_prop(self, result):
        # faz backpropagation do resultado
        self.wins += result
        self.visits += 1
        if self.parent is not None:
            self.parent.back_prop(result)


    def is_fully_expanded(self):
        # devolve se todos os movimentos foram testados para este no
        return len(self.untried_moves) == 0
    
    def rollout(self):
        # Escolhe um movimento que ainda nao foi tentado e cria o filho
        # usa a arvore de decisao para avaliar o estado
        best_choices = []
        best = -1
        unt_mov = self.untried_moves.copy()
        for i in range(len(unt_mov)):
            tree_result = evaluate_func(self.state)
        
            if tree_result > best:
                best_choices = [unt_mov[i]]
                best = tree_result
            elif tree_result == best:
                best_choices.append(unt_mov[i])
        
        move = random.choice(best_choices)    
        new_state = self.state.move(move)
        new_node = MCTSNode(new_state, self)
        self.children[move] = new_node
        self.untried_moves.remove(move)
        return new_node
    

#========================================================================================================================================#

class MCTSPlayer:
    
    def __init__(self, time_limit=1.0):
        self.time_limit = time_limit

    def select_move(self, state,player):
        # seleciona o movimento a partir do estado atual
        root = MCTSNode(state)
        num_rollouts = 0
        start_time = time.time()
        while time.time() - start_time < self.time_limit:
            node = root
            # Select
            while node.is_fully_expanded() and len(node.children) > 0: # enquanto o no nao for folha
                node = node.UCT_select_child()
            # Expand
            if not node.is_fully_expanded():
                node = node.expand()
            # Rollout
            while node.state.winner == -1:
                node = node.rollout()
                num_rollouts +=1
              
            
            if node.state.winner == 0 or node.state.winner != player:
                result = 0
            else:
                result = 1
            #print(result)
            # Backpropagate
            node.back_prop(result)
            
            
        # escolhe o melhor no
        best_move = None
        best_visits = -1
        for move, child_node in root.children.items():
            if child_node.visits > best_visits:
                best_visits = child_node.visits
                best_move = move
            
        return best_move,num_rollouts

#########################################################################################################################################
LIM = 0
labels =['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6']
Root = {}


def build_tree():
    global Root
    Connect4 = read_csv('connect4.csv')
    TargetAttribute = 'Class'
    Attributes = {'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6'}
    Root = id3(Connect4, TargetAttribute, Attributes)

if __name__ == "__main__":
    
    LIM = int(sys.argv[1]) # profundidade a usar (minimax e alpha-beta) ou limite de tempo (MCTS)
    print("   Building Tree...\n")
    build_tree()
    game = ConnectFourGame(player_move, execute_mcts_move(LIM))
    game.start()
