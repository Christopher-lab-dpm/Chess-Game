import pygame
import sys
### Test for legal moves                  
import Board
from Piece_Queen import Queen
from Piece_Knight import Knight
from BoardSettings import BoardSetting
import PositionPlacement

#import pdb
#pdb.set_trace()

setting = BoardSetting()
screen = pygame.display.set_mode((setting.screen_width,
                                              setting.screen_height))


gameboard  = Board.Board(screen)

location1 = PositionPlacement.matrix_to_screen(2, 7)
location2 = PositionPlacement.matrix_to_screen(1, 0)

#queen  = Queen(screen, "White", "WhiteQueen", location1, gameboard )
#bqueen  = Queen(screen, "Black", "BlackQueen", location2, gameboard )

knight = Knight(screen, "Black", "BlackKnight", location2, gameboard )
gameboard.set_tile(1, 0, knight)
#gameboard.set_tile(2, 7, queen)
#gameboard.set_tile(2, 4, bqueen)

for i in range(0,8):
            for j in range(0,8):
                if gameboard.access_tile(i,j) != 0:
                    print(gameboard.access_tile(i,j).name + " " + 
                          str(gameboard.access_tile(i,j).board_coord))
                    
                    
"""                
for i in range(0,8):
            for j in range(0,8):
                if queen.board.access_tile(i,j) != 0:
                    print(queen.board.access_tile(i,j).name + " " + 
                          str(queen.board.access_tile(i,j).board_coord))                    
"""
legal_moves = []

legal_moves = knight.check_legal_moves()

print("\n")
print(legal_moves)

pygame.quit() 
sys.exit()