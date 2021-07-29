import pygame
from BoardSettings import BoardSetting
import PositionPlacement
import Piece_Safety

boardsettings = BoardSetting()

class Piece():
    """A class to manage bullets fired from the ship"""
    def __init__(self, screen, color, name, board_coord):
        """Create a Piece object at the current position."""
       
        self.screen = screen
        self.image = None
        self.name = name
        self.color = color
        self.board_coord = board_coord
        
        #Top left of board from white perspective using screen coordinates
        self.location =  PositionPlacement.matrix_to_screen(board_coord[0], 
                                                            board_coord[1])
        
    def get_color(self):
        return self.color
    
    def get_position(self):
        return self.board_coord
    
    def update_position(self,y,x): #Uses board coordinates 
        self.board_coord = (y,x)
        self.location = PositionPlacement.matrix_to_screen(y,x)
    
    def blitme(self):
        """Draw the piece at its described location by the board"""
        
        self.image  = pygame.transform.scale(self.image, (boardsettings.tile_width - 15,
                                                  boardsettings.tile_width - 15))
        
        current_piece = self.image
        rect = current_piece.get_rect()
        rect.center = (self.location[0], self.location[1])
        self.screen.blit(current_piece, rect)
    

    def check_file(self, board):
        legal_moves = []
        y = self.board_coord[0]
        x = self.board_coord[1]
        # Check vertically upward in a file
        for i in reversed(range(0,y)):
            if  board.access_tile(i,x) == 0:
                legal_moves.append((i,x))
                
            elif board.access_tile(i,x).color != self.color :
                legal_moves.append((i,x))
                break
            else:
                break
     
        # Check vertically downward in a file
        for i in range(y + 1, 8):
            if  y + 1 == 8:#edge of board
                break
            if  board.access_tile(i,x) == 0:
                legal_moves.append((i,x))
                
            elif board.access_tile(i,x).color != self.color:
                legal_moves.append((i,x))
                break
            else:
                break
        return legal_moves   
        
    def check_row(self, board):
        legal_moves = [] 
        y = self.board_coord[0]
        x = self.board_coord[1]
        # Check Laterally right in a row
        for j in range(x+1,8):
            if x+1 == 8: #edge of board
                break
            if  board.access_tile(y,j) == 0:
                legal_moves.append((y, j))
            elif board.access_tile(y,j).color != self.color:
                legal_moves.append((y,j))
                break
            else:
                break

        # Check Laterally left in a row
        for j in reversed(range(0,x)):
            if  board.access_tile(y,j) == 0:
                legal_moves.append((y, j))
            elif board.access_tile(y,j).color != self.color:
                legal_moves.append((y,j))
                break
            else:
                break   
        return legal_moves
        
    
    def check_diagonals(self,board):
        legal_moves = []
        
        # Check the right upward diagonals
        i = self.board_coord[0] - 1
        j = self.board_coord[1] + 1
        
        while i <= 7  and i >= 0 and  j <= 7 and j>=0 :
            
            if board.access_tile(i,j) == 0:
                legal_moves.append((i,j))
            elif board.access_tile(i,j).color != self.color:
                legal_moves.append((i,j))
                break
            else:
                break
            i -= 1
            j += 1
        
        # Check the left upward diagonals
        i = self.board_coord[0] - 1
        j = self.board_coord[1] - 1
        
        while i <= 7  and i >= 0 and  j <= 7 and j>=0 :
            if board.access_tile(i,j) == 0:
                legal_moves.append((i,j))
            elif board.access_tile(i,j).color != self.color:
                legal_moves.append((i,j))
                break
            else:
                break
            i -= 1
            j -= 1
            
            
        # Check the right downwards diagonals
        i = self.board_coord[0] + 1
        j = self.board_coord[1] + 1
        
        while i <= 7  and i >= 0 and  j <= 7 and j>=0 :
            if board.access_tile(i,j) == 0:
                legal_moves.append((i,j))
            elif board.access_tile(i,j).color != self.color:
                legal_moves.append((i,j))
                break
            else:
                break
            
            i += 1
            j += 1
            
        # Check the left downwards diagonals
        i = self.board_coord[0] + 1
        j = self.board_coord[1] - 1
        
        while i <= 7  and i >= 0 and  j <= 7 and j>=0 :
            if board.access_tile(i,j) == 0:
                legal_moves.append((i,j))
            elif board.access_tile(i,j).color != self.color:
                legal_moves.append((i,j))
                break
            else:
                break
            
            i += 1
            j -= 1
            
        return legal_moves
    
    


    
    def check_legal_moves(self):
         pass
    
    
     
    def check_allowed_moved(self,board,list_of_moves):
        
        if self.name == "BlackKing" or self.name == "WhiteKing":
            
            return list_of_moves
        
        
        placeholder = None
        allowed_moves = []
        color = None
        initial_threat_level = None
        second_threat_level = None
        if self.color == "White":
            king  = board.white_king
            king_position = king.get_position()
            color = "White"
        else:#Black
             king  = board.black_king
             king_position = king.get_position()
             color = "Black"
    
        initial_threat_level = Piece_Safety.check_piece_safety(*king_position,
                                                                   color, board)
   
        placeholder = board.access_tile(*self.board_coord)
        board.set_tile(*self.board_coord, 0)
        
        second_threat_level = Piece_Safety.check_piece_safety(*king_position,
                                                                   color, board)
        if len(second_threat_level) == 0:
            board.set_tile(*self.board_coord, placeholder)
            return list_of_moves 
        elif len(second_threat_level) > 1 : #removing piece from board exposes king to more danger
                                            #piece has no more moves
            #Moving piece exposes king to danger when king already in check
            if self.name != "BlackKing" or self.name != "WhiteKing":
                allowed_moves = []
                board.set_tile(*self.board_coord, placeholder)
                return allowed_moves
            else:
                board.set_tile(*self.board_coord, placeholder)
                return list_of_moves
        else: #len(second_threat_level) == 1
            board.set_tile(*self.board_coord, placeholder)
           
            attacking_moves = board.access_tile(*second_threat_level[0]).check_legal_moves(board)
                                                
            
            for move in list_of_moves:
               #Check if attacking piece may be captured
                             
               if move in second_threat_level:
                   allowed_moves.append(move)
               else: # check if it can block the attacking piece    
                   if move in attacking_moves:
                        
                        board.set_tile(*move, placeholder)
                        board.set_tile(*self.board_coord, 0)
                        second_threat_level2 = Piece_Safety.check_piece_safety(*king_position,
                                                                   color, board)
                        board.set_tile(*self.board_coord, placeholder)
                        
                        
                        if len(second_threat_level2) == 0:
                             allowed_moves.append(move)
                        
                        board.set_tile(*move, 0)    
                       
                         
                   
            
        return allowed_moves 
     
   
