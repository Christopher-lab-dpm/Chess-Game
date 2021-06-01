import pygame

from Piece import Piece
#from BoardSettings import BoardSetting

class King(Piece):
    #Location is a tuple (x,y) and the board is a 2D array
   def __init__(self, screen, color,name, location, board):
       
       super(King, self).__init__(screen, color, name, location, board)
       self.image_file = "C:/Users/Christopher/Documents/Chess pieces"+"/"+name+".bmp"
       self.image = pygame.image.load(self.image_file)
   
    
   def check_legal_moves(self):
        """Method overriden in the different piece subclasses which will return a list
        of the legal moves a given piece has"""
              
        #return legal_moves
            
            