import pygame

from Piece import Piece
#from BoardSettings import BoardSetting

class Knight(Piece):
    #Location is a tuple (x,y) and the board is a 2D array
   def __init__(self, screen, color, name, board_coord):
       
       super(Knight, self).__init__(screen, color, name, board_coord)
       self.image_file = "Chess pieces"+"/"+name+".bmp"
       self.image = pygame.image.load(self.image_file)
   
    
   def check_legal_moves(self, board):
         """Method overriden in the different piece subclasses which will return a list
         of the legal moves a given piece has"""
         legal_moves = []

         legal_moves.append((self.board_coord[0] - 2,self.board_coord[1] + 1))
         legal_moves.append((self.board_coord[0] - 2,self.board_coord[1] - 1))
         legal_moves.append((self.board_coord[0] + 2,self.board_coord[1] + 1))
         legal_moves.append((self.board_coord[0] + 2,self.board_coord[1] - 1))
         legal_moves.append((self.board_coord[0] + 1,self.board_coord[1] - 2))
         legal_moves.append((self.board_coord[0] + 1,self.board_coord[1] + 2))
         legal_moves.append((self.board_coord[0] - 1,self.board_coord[1] + 2))
         legal_moves.append((self.board_coord[0] - 1,self.board_coord[1] - 2))
         
         i = 0 
         while True:
             if i == len(legal_moves) :
                 break
             move = legal_moves[i]
             if (move[1] < 0 or move[1] > 7 
             or move[0] < 0 or move[0] > 7):
                 legal_moves.remove(move)
             elif (board.access_tile(move[0], move[1]) !=0
                   and board.access_tile(move[0], move[1]).color == self.color):
                 legal_moves.remove(move)
             else:
                i += 1
         
        
         return legal_moves
         
   def check_allowed_moves(self,board, legal_moves):
        return super().check_allowed_moved(board, legal_moves)         
      