import pygame

from Piece import Piece
from BoardSettings import BoardSetting

class Board():
    def __init__(self, screen):
        
        self.screen =  screen
        
        self.setting = BoardSetting()        
        #This creates 2D array where each array is seperate
        self.board = [[0]*8 for _ in range(8)]
        
        self.white_turn = True
        self.black_turn = False
        self.game_over = False
       
        self.moving_piece = None
    
    def change_piece_location(self,new_location):#New location (y,x) aka (i,j)
        if self.access_tile(*new_location) != 0: # Not an empty square
                # A capture has just occured!
                #Remove the piece
                self.board[new_location[0]] [new_location[1]].update_position(8000,8000)
                self.board[new_location[0]] [new_location[1]].blitme()
                self.board[new_location[0]] [new_location[1]] = 0 #remove the piece
        
        
        old_location =  self.moving_piece.get_position()
        self.board[old_location[0]][old_location[1]] = 0
        self.board[new_location[0]] [new_location[1]] = self.moving_piece
        self.moving_piece.update_position(new_location[0], new_location[1])
        self.moving_piece.blitme()
        self.moving_piece = None
        
        self.update_turn()
                   
    
    def is_moving_piece(self):
        """Returns a boolean letting us know is a piece is trying to move"""
        if self.moving_piece != None:
            return True
        else:
            return False
        
    def change_moving_piece(self,piece):
        self.moving_piece = piece
    
    def access_tile(self,y,x):
         """Returns what is store at the give position on the board input as (y,x)"""
         return self.board[y][x]
     
    def set_tile(self,y,x,value):
        self.board[y][x] = value
    
    def access_row(self,y):
        return self.board[y]
    
    
    def get_turn(self):
        if self.white_turn:
            return "White"
        elif self.black_turn:
            return "Black"
        else:
            print("The game is over")
            
    def game_over(self):
        self.white_turn = False
        self.black_turn = False
        self.game_over = True
        print("The game is finished")
    
    
    def update_turn(self):
        if self.get_turn() == "White":
             self.white_turn = False
             self.black_turn = True
             
        elif self.get_turn() == "Black":
             self.white_turn = True
             self.black_turn = False
        else:
            self.game_over()
            
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
    
    
    def update_board_visuals(self):
        """Idea is to use this to update the screen once the game has started 
        and not to generate new FEN which consequently generates new pieces"""
        self.make_tiles()
        for i in range(0,7):
            for j in range(0,7):
    