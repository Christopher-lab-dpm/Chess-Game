"""Class for the Visual representation of the pieces"""

import pygame

from BoardSettings import BoardSetting
import PositionPlacement



board_settings = BoardSetting()

class PieceSetup():
    
    def __init__(self,screen):
        self.screen =  screen
     
     
    def create_new_FEN(self, board):
        space_count = 0
        new_FEN=""
        for i in range(0,8):
            space_count = 0     
            for j in range(0,8):
                current_tile = board.access_tile(i,j)
                if current_tile != 0:#There is a piece there
                    if space_count != 0:
                        new_FEN += (str(space_count) + self.reverse_name_dict[current_tile.name])
                    else:
                        new_FEN += self.reverse_name_dict[current_tile.name]
                    space_count = 0
                else:
                    space_count += 1
                    
                if j == 7 and i != 7:
                    if space_count != 0:
                         new_FEN += str(space_count) + '/'
                    else: 
                         new_FEN += '/'
                         
                elif j ==7 and i == 7:
                    if space_count != 0:
                         new_FEN += str(space_count)
                         
        return new_FEN
        
    
 
            
        


#FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
#board = [[0] * 8] * 8                                
#placement  = PositionPlacement.convert_FEN(FEN)   
#for place in placement:
#     board_coord = PositionPlacement.screen_to_board(place[1], place[2])
#     print(place[0] + " " +  str(board_coord))
#    board_coord = PositionPlacement.screen_to_board(place[1], place[2])
#    create_piece_add_to_board(current_piece_name, place, board)
#for i in range(0,7):
#    for j in range(0,7) :
#        print(board[i][j])





                                      
                                          