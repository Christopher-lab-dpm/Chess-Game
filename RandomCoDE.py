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
         FEN = "k7/2N5/8/N7/8/8/8/K7"
         #FEN = "r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1"
         #FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
         # Add a piece 
         piecesetup  = PieceSetup(self.screen)
         # Create board instance
         #board = [[0]*8 for _ in range(8)] #This creates 2D array where each array is seperate
         
         board = Board(self.screen)
         game_beginning = True
         load_new_FEN = False
         piecesetup.blitme(FEN,board)
         
         # Start the main loop for the game.
         while True:
         # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     pygame.quit() 
                     sys.exit()
                 elif pygame.mouse.get_pressed()[0]:#Check is the mouse button was pressed down
                     if board.is_moving_piece():
                         
                         print("Moving piece!")
                         mouse_pos = pygame.mouse.get_pos() 
                         FEN = piecesetup.create_new_FEN(board)
                         #load_new_FEN = not(piecesetup.move_select_piece(mouse_pos,board))
                         piecesetup.move_select_piece(mouse_pos,board)
                         #print(FEN)
                     else:
                         game_beginning  = False
                         # Piece was not selected to move  
                         print("Selected!")
                         mouse_pos = pygame.mouse.get_pos() 
                         piecesetup.select_piece(mouse_pos,board)
                         
                         
                 else:
                     pass
                 
            if board.White_in_check or board.Black_in_check:
                load_new_FEN = board.determine_checkmate()
                FEN = piecesetup.create_new_FEN(board)
                
                    
            if game_beginning:
                self.screen.fill(self.setting.backround_color) 
                board.make_tiles()
                # Add the piece onto the board
                piecesetup.blitme(FEN,board)
            elif load_new_FEN:
                print("Loading previous FEN")
                self.screen.fill(self.setting.backround_color) 
                board.make_tiles()
                board.reset_board()
                # Add the piece onto the board
                piecesetup.blitme(FEN,board)
                load_new_FEN = False
            else:
                 board.update_board_visuals()
                                  
        
            # Make the most recently drawn screen visible.
            pygame.display.flip()
            
          
g = BoardSetup()
g.run_board_setup()


         
            
                 
