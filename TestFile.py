import sys
import pygame

from BoardSettings import BoardSetting
from Display  import Display
from Board import Board
import GameLogic

"""A class for setting up the visuals of the application"""

class BoardSetup():
    """Functions used for the creation of the chess board"""
    
    def __init__(self):
        
        self.setting = BoardSetting()
        self.screen = pygame.display.set_mode((self.setting.screen_width,
                                               self.setting.screen_height))
           
   
    
    def run_board_setup(self):
         # Initialize game and create a screen object.
         pygame.init()
         # Give title to opned window
         pygame.display.set_caption("Chess Board")
         
         FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
         # Add a piece 
         display  = Display(self.screen)
         # Create board instance
         #board = [[0]*8 for _ in range(8)] #This creates 2D array where each array is seperate
         
         board = Board(self.screen)
         board.intialize_board_position(FEN)  
         
         for i in range(0,8):
             for j in range (0,8):
                if  board.access_tile(i, j) != 0 : 
                     print("At Position (" + str(i) + "," + str(j) + 
                           ") we have a " + board.access_tile(i, j).name)
         
            
         
         pygame.quit() 
         sys.exit()
            
g = BoardSetup()
g.run_board_setup()


         
            
                 
