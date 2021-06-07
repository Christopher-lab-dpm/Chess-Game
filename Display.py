# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 08:58:24 2021

@author: Christopher
"""
import pygame

from BoardSettings import BoardSetting
import PositionPlacement


class Display():
    def __init__(self, screen):
        self.screen = screen
        self.setting = BoardSetting()
        
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
    

    def display_legal_moves(self, board):
        """When a piece is selected to move, display the legal moves 
        in the provided list"""
        if  board.is_moving_piece():
            legal_moves = board.get_moving_piece().check_legal_moves(board)
                      
            for legal_move in legal_moves:
                color = self.setting.move_color
                center = PositionPlacement.matrix_to_screen(*legal_move)
                radius = (self.setting.tile_width)/self.setting.radius_coefficient
                
                pygame.draw.circle(self.screen, color , center, radius)
        
        
    
    def update_board_visuals(self, board):
            """Idea is to use this to update the screen once the game has already started 
            and not to generate new FEN which consequently generates new pieces"""
            self.screen.fill(self.setting.backround_color)
            self.make_tiles()
            
            self.display_legal_moves(board)
            for i in range(0,8):
                for j in range(0,8):
                    if board.access_tile(i,j) != 0:
                        board.access_tile(i,j).blitme()
                        
                                       