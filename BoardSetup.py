import sys

import pygame

from BoardSettings import BoardSetting
from PieceSetup  import PieceSetup

"""A class for setting up the visuals of the application"""

class BoardSetup():
    """Functions used for the creation of the chess board"""
    
    def __init__(self):
        
        self.setting = BoardSetting()
        self.screen = pygame.display.set_mode((self.setting.screen_width,
                                               self.setting.screen_height))
           
    def make_tiles(self):
            """Creates the tiles of the chess board from the view of given perspective"""
            # Double for loop to create the square on the board
            # i controls the row and j controls the column
            # When i and j are even the square is white
            # Note that tile_width = tile_height
            for i in range(0,8):
                    for j in range(0,8):
                        if (i+j)%2 == 0:
                            pygame.draw.rect(self.screen, 
                                             self.setting.w_tile_color,
                                             pygame.Rect((self.setting.tile_width*(j+1), 
                                                          self.setting.tile_width*(i+1)),
                                                         (self.setting.tile_width, 
                                                         self.setting.tile_height)))
                            
                          
                        else:
                             pygame.draw.rect(self.screen, self.setting.b_tile_color,
                                              pygame.Rect((self.setting.tile_width*(j+1), 
                                                           self.setting.tile_width*(i+1)), 
                                                          (self.setting.tile_width, 
                                                          self.setting.tile_height)))
    
    def run_board_setup(self):
         # Initialize game and create a screen object.
         pygame.init()
         # Give title to opned window
         pygame.display.set_caption("Chess Board")
         FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
         # Add a piece 
         piecesetup  = PieceSetup(self.screen)
         
         # Start the main loop for the game.
         while True:
         # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     pygame.quit() 
                     sys.exit()
            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.setting.backround_color) 
            
            self.make_tiles()
            
            # Add the piece onto the board
            piecesetup.blitme(FEN)
                  
            # Make the most recently drawn screen visible.
            pygame.display.flip()

g = BoardSetup()
g.run_board_setup() 
        
