import pygame
from BoardSettings import BoardSetting
import PositionPlacement

boardsettings = BoardSetting()

class Piece():
    """A class to manage bullets fired from the ship"""
    def __init__(self, screen, color, name, location, board):
        """Create a Piece object at the current position."""
       
        self.screen = screen
        self.image = None
        self.name = name
        self.color = color
        self.location = location #Top left of board from white perspective using screen coordinates
        
        #Remmeber that location works with (x,y) and board is a matrix so it works with (y,x)
        #Method screen to board automatically takes care of this and switches the output
        self.board_coord = PositionPlacement.screen_to_board(location[0], location[1])
        self.board =  board
    
   
    def get_position(self):
        return self.board_coord
    
    def update_position(self,y,x): #Uses board coordinates 
        self.board_coord = (y,x)
        self.location = PositionPlacement.matrix_to_screen(x,y)
    
    def blitme(self):
        """Draw the piece at its described location by the board"""
        
        self.image  = pygame.transform.scale(self.image, (boardsettings.tile_width - 15,
                                                  boardsettings.tile_width - 15))
        
        current_piece = self.image
        rect = current_piece.get_rect()
        rect.center = (self.location[0], self.location[1])
        self.screen.blit(current_piece, rect)
    

    def check_file(self):
        legal_moves = []
        # Check vertically upward in a file
        for i in range(self.board_coord[0],8):
            if  self.board.access_tile(i,self.board_coord[1]) == 0:
                legal_moves.append((i,self.board_coord[1]))
                
            elif self.board.access_tile(i,self.board_coord[1]).color != self.color :
                legal_moves.append((i,self.board_coord[1]))
            else:
                break
       
        # Check vertically downward in a file
        for i in reversed(range(0,self.board_coord[0])):
            if  self.board.access_tile(i,self.board_coord[1]) == 0:
                legal_moves.append((i,self.board_coord[1]))
                
            elif self.board.access_tile(i,self.board_coord[1]).color != self.color:
                legal_moves.append((i,self.board_coord[1]))
            else:
                break
        return legal_moves   
        
    def check_row(self):
        legal_moves = [] 
        # Check Laterally right in a row
        for j in range(self.board_coord[1],8):
            if  self.board.access_tile(self.board_coord[0],j) == 0:
                legal_moves.append((self.board_coord[0], j))
            elif self.board.access_tile(self.board_coord[0],j).color != self.color:
                legal_moves.append((self.board_coord[0],j))
            else:
                break

        # Check Laterally left in a row
        for j in reversed(range(0,self.board_coord[1])):
            if  self.board.access_tile(self.board_coord[0],j) == 0:
                legal_moves.append((self.board_coord[0], j))
            elif self.board.access_tile(self.board_coord[0],j).color != self.color:
                legal_moves.append((self.board_coord[0],j))
            else:
                break   
        return legal_moves
        
    def check_diagonals(self):
                
        legal_moves = []
        
        # Check the right upward diagonals
        i = self.board_coord[0] + 1
        j = self.board_coord[1] + 1
        
        while i <= 7  and i >= 0 or  j <= 7 and j>=0 :
            if self.board.access_tile(i,j) == 0:
                legal_moves.append((i,j))
            elif self.board.access_tile(i,j).color != self.color:
                legal_moves.append((i,j))
            else:
                break
            i -= 1
            j += 1
        
        # Check the left upward diagonals
        i = self.board_coord[0] - 1
        j = self.board_coord[1] - 1
        
        while i <= 7  and i >= 0 or  j <= 7 and j>=0 :
            if self.board.access_tile(i,j) == 0:
                legal_moves.append((i,j))
            elif self.board.access_tile(i,j).color != self.color:
                legal_moves.append((i,j))
            else:
                break
            i -= 1
            j -= 1
            
            
        # Check the right downwards diagonals
        i = self.board_coord[0] + 1
        j = self.board_coord[1] + 1
        
        while i <= 7  and i >= 0 or  j <= 7 and j>=0 :
            if self.board.access_tile(i,j) == 0:
                legal_moves.append((i,j))
            elif self.board.access_tile(i,j).color != self.color:
                legal_moves.append((i,j))
            else:
                break
            
            i += 1
            j -= 1
            
        # Check the left downwards diagonals
        i = self.board_coord[0] + 1
        j = self.board_coord[1] + 1
        
        while i <= 7  and i >= 0 or  j <= 7 and j>=0 :
            if self.board.access_tile(i,j) == 0:
                legal_moves.append((i,j))
            elif self.board.access_tile(i,j).color != self.color:
                legal_moves.append((i,j))
            else:
                break
            
            i += 1
            j -= 1
        return legal_moves
    
        
    def check_legal_moves(self):
        """Method overriden in the diferent piece subclasses which will return a list
        of the legal moves a given piece has"""
        
    def move(self, move):
        """ Moves Piece the postion specified if the argument if legal move """
        legal_moves = self.check_legal_moves()
        
        if move in legal_moves:
            #update the piece postion on the screen
            pass
        return None
        
   
