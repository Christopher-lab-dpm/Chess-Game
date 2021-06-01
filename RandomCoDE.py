import sys

import pygame
import PositionPlacement
from BoardSettings import BoardSetting
from PieceSetup  import PieceSetup
from Board import Board

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
         #FEN = "r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1"
         # Add a piece 
         piecesetup  = PieceSetup(self.screen)
         # Create board instance
         #board = [[0]*8 for _ in range(8)] #This creates 2D array where each array is seperate
         
         board = Board(self.screen)
         
         # Start the main loop for the game.
         while True:
         # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     pygame.quit() 
                     sys.exit()
                 elif pygame.mouse.get_pressed()[0]:#Check is the mouse button was pressed down
                     
                         print("Selected!")
                         mouse_pos = pygame.mouse.get_pos() 
                         print (str(mouse_pos))
                         board_coord = PositionPlacement.mouse_to_board(mouse_pos[0], 
                                                        mouse_pos[1])
                         print (str(board_coord))
                         
                 else:
                     pass
                 
            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.setting.backround_color) 
            
            board.make_tiles()
            
      
          
            # Make the most recently drawn screen visible.
            pygame.display.flip()
            
          
g = BoardSetup()
g.run_board_setup()


         
            
                 
