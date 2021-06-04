import pygame

from Piece import Piece
#from BoardSettings import BoardSetting

class Bishop(Piece):
    #Location is a tuple (x,y) and the board is a 2D array
   def __init__(self, screen, color,name, location, board):
       
       super(Bishop, self).__init__(screen, color, name, location, board)
       self.image_file = "C:/Users/Christopher/Documents/Chess pieces"+"/"+name+".bmp"
       self.image = pygame.image.load(self.image_file)
   
    
   def check_legal_moves(self):
        """Method overriden in the different piece subclasses which will return a list
        of the legal moves a given piece has"""
                      
        legal_diag = self.check_diagonals()
        
        self.legal_moves = legal_diag      
        return legal_diag
            
            
