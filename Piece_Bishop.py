import pygame

from Piece import Piece
#from BoardSettings import BoardSetting

class Bishop(Piece):
    #Location is a tuple (x,y) and the board is a 2D array
   def __init__(self, screen, color, name, board_coord):
       
       super(Bishop, self).__init__(screen, color, name, board_coord)
       self.image_file = "C:/Users/Christopher/Documents/Chess pieces"+"/"+name+".bmp"
       self.image = pygame.image.load(self.image_file)
   
    
   def check_legal_moves(self,board):
        """Method overriden in the different piece subclasses which will return a list
        of the legal moves a given piece has"""
                      
        legal_diag = self.check_diagonals(board)
        
        
        return legal_diag
            
            
