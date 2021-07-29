import pygame

from Piece import Piece
#from BoardSettings import BoardSetting

class Bishop(Piece):
    #Location is a tuple (x,y) and the board is a 2D array
   def __init__(self, screen, color, name, board_coord):
       
       super(Bishop, self).__init__(screen, color, name, board_coord)
       self.image_file = "Chess pieces"+"/"+name+".bmp"
       self.image = pygame.image.load(self.image_file)
   
    
   def check_legal_moves(self,board):
        """Method overriden in the different piece subclasses which will return a list
        of the legal moves a given piece has"""
                      
        legal_diag = self.check_diagonals(board)
           
        return legal_diag
            
   def check_allowed_moves(self,board, legal_moves):
        return super().check_allowed_moved(board, legal_moves)         
