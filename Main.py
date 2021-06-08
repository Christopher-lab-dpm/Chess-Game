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
         
         FEN = "r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1"
         # Add a piece 
         display  = Display(self.screen)
         # Create board instance
         #board = [[0]*8 for _ in range(8)] #This creates 2D array where each array is seperate
         
         board = Board(self.screen)
         board.intialize_board_position(FEN)  
         
         
         # Start the main loop for the game.
         while True:
         # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     board.create_new_FEN()
                     pygame.quit() 
                     sys.exit()
                 elif pygame.mouse.get_pressed()[0]:#Check is the mouse button was pressed down    
                     if  not(board.is_moving_piece()):#No piece selected yet
                         mouse_pos = pygame.mouse.get_pos() 
                         GameLogic.select_piece(mouse_pos,board)
                         
                     elif board.is_moving_piece():
                         mouse_pos = pygame.mouse.get_pos()
                         moved = GameLogic.move_piece(mouse_pos,board)
                         if moved:
                             GameLogic.update_turn(board)
                             GameLogic.determine_stalemate(board)
                             GameLogic.determine_checkmate(board)
                         else:
                             pass
                 else:
                     pass
            #Update the screen
            display.update_board_visuals(board)        
            # Make the most recently drawn screen visible.
            pygame.display.flip()
            
          
g = BoardSetup()
g.run_board_setup()


         
            
                 
