# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 14:47:38 2021

@author: Christopher
"""

import sys
import pygame

from BoardSettings import BoardSetting

from Display  import Display
from Board import Board
import GameLogic


class Engine():
    def __init__(self, FEN, color, depth):
        
        self.max_Positions = 0
        self.depth = depth
        self.color = color
        
        self.original_FEN = FEN
        
        self.piece_value = {"BlackKing": -100,"BlackQueen":-10,"BlackBishop":-3,
                               "BlackKnight":-3,"BlackPawn":-1,"BlackRook":-5,
                              "WhiteKing":100,"WhiteQueen":10,"WhiteBishop":3,
                             "WhiteKnight":3,"WhitePawn":1,"WhiteRook":5
            }
        
        self.piece_utility = {"BlackKing": 0,"BlackQueen":-10,"BlackBishop":-6,
                               "BlackKnight":-5,"BlackPawn":-1,"BlackRook":-4,
                              "WhiteKing":0,"WhiteQueen":10,"WhiteBishop":6,
                             "WhiteKnight":5,"WhitePawn":1,"WhiteRook":4
            }
    
    
    def evaluation(self, board):
         evaluation = 0
         for i in range(0,8):
                for j in range(0,8):
                    piece  = board.access_tile(i,j)
                    if piece != 0:
                        evaluation += self.piece_value[piece.name]
         return evaluation               
    
    def get_moves(self, board, player):
          all_moves = {}  
          for i in range(0,8):
              for j in range(0,8):
                    piece  = board.access_tile(i,j)
                    
                    if piece != 0 and piece.color == player:
                        list_of_moves = piece.check_legal_moves(board)
                        all_moves[piece] = piece.check_allowed_moves(board,list_of_moves)  
          return all_moves


    def sort_pieces(self, list_of_pieces):#THIS IS USED ONLY TO SORT PIECES OF THE SAME COLOR
        sorted_pieces = [list_of_pieces[0]]
        
        for piece in list_of_pieces:
            value = abs(self.piece_utility[piece.name])
           
            for i in range (0 , len(sorted_pieces)):
                
                if piece == sorted_pieces[0] :
                    break
                elif  i  == (len(sorted_pieces) -1 ):
                    sorted_pieces.append(piece)
                
                elif value < abs(self.piece_utility[sorted_pieces[i].name]):
                    pass
                elif value >= abs(self.piece_utility[sorted_pieces[i].name]):
                       sorted_pieces.insert(i,piece)
                       break
                   
                else:
                    pass
               
        return sorted_pieces                
           

    def mini_max(self, board, depth, player,FEN, alpha = -10000 , beta = 10000, max_Positions=1000): #Depth is number of half move(rg. 6 mean black does 3 and white does 3)
        self.max_Positions += 1
      
        opp_color = None
        move_eval = []
        best_eval = 0 
        if depth == 0 : 
           return self.evaluation(board)
       
        if player == "White":
            opp_color = "Black"
        else:
            opp_color = "White"
   
        all_moves = self.get_moves(board, player)
        keys =  list(all_moves.keys())
        sorted_keys = self.sort_pieces(keys)
        for piece in sorted_keys:
            original_position = piece.get_position()
            for move in all_moves[piece]:
              board.change_moving_piece(board.access_tile(*original_position))
              board.computer_change_piece_location(move)
              new_FEN = board.create_new_FEN()
              
              
              if self.max_Positions == max_Positions and depth == self.depth:
                  x= 0
                  if player == "Black":
                      x = 10000
                  else:
                      x = -10000
                  best_eval =  (piece, move, x  ) 
                  return best_eval
              elif self.max_Positions == max_Positions and depth != self.depth:
                  x= 0
                  if player == "Black":
                      x = 10000
                  else:
                      x = -10000
                  return x
              else:
                  pass 
              
              
              
              move_eval.append( (piece, move , self.mini_max(board, (depth-1), opp_color, new_FEN))) 
             
              if len(move_eval) == 1 : 
                  best_eval = move_eval[0]
              elif len(move_eval) == 0:
                  pass
              else:
                 if move_eval[len(move_eval) -1][2] < best_eval[2] and player == "Black":
                     best_eval = move_eval[len(move_eval) -1]
                     beta = best_eval[2]
                 elif move_eval[len(move_eval) -1][2] > best_eval[2] and player == "White":   
                      best_eval = move_eval[len(move_eval) -1]
                      alpha = best_eval[2]
                 else:
                     pass
    
              board.reset_board_position(FEN)
              piece.update_position(*original_position)
              
              if self.max_Positions == max_Positions and depth == self.depth:
                  return best_eval
              elif self.max_Positions == max_Positions and depth != self.depth:
                   return best_eval[2]
              else:
                  pass 
                 
              if beta <= alpha and depth == self.depth:
                  return best_eval
              elif beta <= alpha and depth != self.depth:
                  return best_eval[2]
              else:
                  pass
        
        if depth == self.depth:
            return best_eval   
         
        return best_eval[2]
            
    def make_move(self, board):
        FEN =  board.create_new_FEN()
        best_move = self.mini_max(board, self.depth, self.color, FEN)
        #print(best_move)
        #print(best_move[0].get_position())
        board.change_moving_piece(board.access_tile(*best_move[0].get_position())) 
        
        board.computer_change_piece_location(best_move[1])
        self.max_Positions = 0
        print("The position is now " + str(best_move[2]) + " after my move.\n")


"""
BoardSettings = BoardSetting()        
screen = pygame.display.set_mode((BoardSettings.screen_width,BoardSettings.screen_height))      

FEN = "rnbqkb1r/ppp1pppp/5n2/3P4/8/8/PPPPQPPP/RNB1KBNR b qkQK"                                                    
board = Board(screen)
engine = Engine(FEN, "Black",1)

board.intialize_board_position(FEN)  

all_moves = engine.get_moves(board, "Black")
keys =  list(all_moves.keys())

sorted_keys = engine.sort_pieces(keys)

for piece in sorted_keys:
    
    print(piece.name)
           
pygame.quit() 
sys.exit()
  
   """        
            
            