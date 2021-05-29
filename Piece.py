import pygame
from BoardSettings import BoardSetting

class Piece():
    """A class to manage bullets fired from the ship"""
    def __init__(self, screen, color, name, location, board):
        """Create a Piece object at the current position."""
       
        self.screen = screen
        self.image = None
        self.name = name
        self.color = color
        self.location = location #Top left of board from white perspective 
        self.board =  board
    
    
    def blitme(self):
        """Draw the piece at its described location by the board"""
        
        self.image  = pygame.transform.scale(self.image, (BoardSetting.tile_width - 15,
                                                  BoardSetting.tile_width - 15))
        
        current_piece = self.image
        rect = current_piece.get_rect()
        rect.center = (self.location[0], self.location[1])
        self.screen.blit(current_piece, rect)
    
        
    
    def check_file(self):
        legal_moves = []
        # Check vertically upward in a file
        for i in range(self.location[0],9):
            if  self.board[i][self.location[1]] == 0:
                legal_moves.append((i,self.location[1]))
                
            elif self.board[i][self.location[1]].color != self.color :
                legal_moves.append((i,self.location[1]))
            else:
                break
       
        # Check vertically downward in a file
        for i in reversed(range(1,self.location[0])):
            if  self.board[i][self.location[1]] == 0:
                legal_moves.append((i,self.location[1]))
                
            elif self.board[i][self.location[1]].color != self.color:
                legal_moves.append((i,self.location[1]))
            else:
                break
        return legal_moves   
        
    def check_row(self):
        legal_moves = [] 
        # Check Laterally right in a row
        for j in range(self.location[1],9):
            if  self.board[self.location[0]][j] == 0:
                legal_moves.append((self.location[0], j))
            elif self.board[self.location[0]][j].color != self.color:
                legal_moves.append((self.location[0],j))
            else:
                break

        # Check Laterally left in a row
        for j in reversed(range(1,self.location[1])):
            if  self.board[self.location[0]][j] == 0:
                legal_moves.append((self.location[0], j))
            elif self.board[self.location[0]][j].color != self.color:
                legal_moves.append((self.location[0],j))
            else:
                break   
        return legal_moves
        
    def check_diagonals(self):
                
        legal_moves = []
        
        # Check the right upward diagonals
        i = self.location[0] + 1
        j = self.location[1] + 1
        
        while i <= 8  and i >= 1 or  j <= 8 and j>=1 :
            if self.board[i][j] == 0:
                legal_moves.append((i,j))
            elif self.board[i][j].color != self.color:
                legal_moves.append((i,j))
            else:
                break
            --i
            ++j
        
        # Check the left upward diagonals
        i = self.location[0] - 1
        j = self.location[1] - 1
        
        while i <= 8  and i >= 1 or  j <= 8 and j>=1 :
            if self.board[i][j] == 0:
                legal_moves.append((i,j))
            elif self.board[i][j].color != self.color:
                legal_moves.append((i,j))
            else:
                break
            --i
            --j
            
            
        # Check the right downwards diagonals
        i = self.location[0] + 1
        j = self.location[1] + 1
        
        while i <= 8  and i >= 1 or  j <= 8 and j>=1 :
            if self.board[i][j] == 0:
                legal_moves.append((i,j))
            elif self.board[i][j].color != self.color:
                legal_moves.append((i,j))
            else:
                break
            
            ++i
            --j
            
        # Check the left downwards diagonals
        i = self.location[0] + 1
        j = self.location[1] + 1
        
        while i <= 8  and i >= 1 or  j <= 8 and j>=1 :
            if self.board[i][j] == 0:
                legal_moves.append((i,j))
            elif self.board[i][j].color != self.color:
                legal_moves.append((i,j))
            else:
                break
            
            ++i
            --j
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
        
   
