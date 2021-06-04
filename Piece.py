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
        
        self.legal_moves = []
        
        #Remmeber that location works with (x,y) and board is a matrix so it works with (y,x)
        #Method screen to board automatically takes care of this and switches the output
        self.board_coord = PositionPlacement.screen_to_board(location[0], location[1])
        self.board =  board
    
       
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
    

    def check_file(self):
        legal_moves = []
        # Check vertically upward in a file
        for i in reversed(range(0,self.board_coord[0])):
            if  self.board.access_tile(i,self.board_coord[1]) == 0:
                legal_moves.append((i,self.board_coord[1]))
                
            elif self.board.access_tile(i,self.board_coord[1]).color != self.color :
                legal_moves.append((i,self.board_coord[1]))
                break
            else:
                break
     
        # Check vertically downward in a file
        for i in range(self.board_coord[0] + 1, 8):
            if  self.board_coord[0] + 1 == 8:#edge of board
                break
            if  self.board.access_tile(i,self.board_coord[1]) == 0:
                legal_moves.append((i,self.board_coord[1]))
                
            elif self.board.access_tile(i,self.board_coord[1]).color != self.color:
                legal_moves.append((i,self.board_coord[1]))
                break
            else:
                break
        return legal_moves   
        
    def check_row(self):
        legal_moves = [] 
        # Check Laterally right in a row
        for j in range(self.board_coord[1]+1,8):
            if self.board_coord[1]+1 == 8: #edge of board
                break
            if  self.board.access_tile(self.board_coord[0],j) == 0:
                legal_moves.append((self.board_coord[0], j))
            elif self.board.access_tile(self.board_coord[0],j).color != self.color:
                legal_moves.append((self.board_coord[0],j))
                break
            else:
                break

        # Check Laterally left in a row
        for j in reversed(range(0,self.board_coord[1])):
            if  self.board.access_tile(self.board_coord[0],j) == 0:
                legal_moves.append((self.board_coord[0], j))
            elif self.board.access_tile(self.board_coord[0],j).color != self.color:
                legal_moves.append((self.board_coord[0],j))
                break
            else:
                break   
        return legal_moves
        
    def check_diagonals(self):
                
        legal_moves = []
        
        # Check the right upward diagonals
        i = self.board_coord[0] - 1
        j = self.board_coord[1] + 1
        
        while i <= 7  and i >= 0 and  j <= 7 and j>=0 :
            
            if self.board.access_tile(i,j) == 0:
                legal_moves.append((i,j))
            elif self.board.access_tile(i,j).color != self.color:
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
            if self.board.access_tile(i,j) == 0:
                legal_moves.append((i,j))
            elif self.board.access_tile(i,j).color != self.color:
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
            if self.board.access_tile(i,j) == 0:
                legal_moves.append((i,j))
            elif self.board.access_tile(i,j).color != self.color:
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
            if self.board.access_tile(i,j) == 0:
                legal_moves.append((i,j))
            elif self.board.access_tile(i,j).color != self.color:
                legal_moves.append((i,j))
                break
            else:
                break
            
            i += 1
            j -= 1
        return legal_moves
    
        
    def check_legal_moves(self):
        """Method overriden in the different piece subclasses 
        which will return a list of the legal moves a given piece has"""
        legal_moves = []  
        for i in range(0,8):
              for j in range(0,8):
                  legal_moves.append((i,j))
        
        self.legal_moves = legal_moves
        
        return legal_moves
    
    def display_legal_moves(self):
        """When a piece is selected to move, display the legal moves 
        in the provided list"""
        for legal_move in self.legal_moves:
            color = boardsettings.move_color
            center = PositionPlacement.matrix_to_screen(*legal_move)
            radius = (boardsettings.tile_width)/boardsettings.radius_coefficient
            
            pygame.draw.circle(self.screen, color , center, radius)
  
    
  
    def check_k(self,y,x): #Enter the position of the king currently or where he will be
                           #check if the king is in danger there
        attack_position = []                    
                           
        #check file for rook or queen
        file_row_piece = ["WhiteRook","WhiteQueen","BlackRook","BlackQueen"]
        
        diag_piece = ["WhiteBishop","BlackBishop","WhiteQueen","BlackQueen"]
        
        diag_pawn_king = ["WhiteKing","BlackKing","BlackPawn","WhitePawn"]
        knight_piece = ["WhiteKnight","BlackKnight"]
        
         # Check vertically upward in a file
        for i in reversed(range(0,y)):
             if  self.board.access_tile(i,x) == 0:
                 pass
                 
             elif self.board.access_tile(i,x).color != self.color :
                 if self.board.access_tile(i,x).name in file_row_piece:
                     attack_position.append(((i,x)))
                     break
                 else: #its a pawn, knight or bishop
                     break
             else:
                 break
          
         # Check vertically downward in a file
        for i in range(y + 1, 8):
             if  y + 1 == 8:#edge of board
                 break
             if  self.board.access_tile(i,x) == 0:
                pass
                 
             elif self.board.access_tile(i,x).color != self.color:
                  if self.board.access_tile(i,x).name in file_row_piece:
                     attack_position.append(((i,x)))
                     break
                  else: 
                     break
             else:
                 break
        
         
         # Check Laterally right in a row
        for j in range(x+1,8):
             if x+1 == 8: #edge of board
                 break
             if  self.board.access_tile(y,j) == 0:
                 pass
             elif self.board.access_tile(y,j).color != self.color:
                 if self.board.access_tile(y,j).name in file_row_piece:
                     attack_position.append(((y,j)))
                     break
                 else:
                     break
             else:
                 break
         
         # Check Laterally left in a row
        for j in reversed(range(0,x)):
             if  self.board.access_tile(y,j) == 0:
                 pass
             elif self.board.access_tile(y,j).color != self.color:
                if self.board.access_tile(y,j).name in file_row_piece:
                     attack_position.append(((y,j)))
                     break
                else:
                     break
             else:
                 break   
         
               
        # Check the right upward diagonals
        i = y - 1
        j = x + 1
        
        while i <= 7  and i >= 0 and  j <= 7 and j>=0 :
            if (self.board.access_tile(i,j) !=0 and 
                self.board.access_tile(i,j).color != self.color and
                i == y-1 and 
                j == x+1 and
                self.board.access_tile(i,j).name in diag_pawn_king):
                attack_position.append(((i,j)))
                break
                
                
            if self.board.access_tile(i,j) == 0:
                pass
            elif self.board.access_tile(i,j).color != self.color:
                if self.board.access_tile(i,j).name in diag_piece:
                    attack_position.append(((i,j)))
                    break
                else: 
                    break
            else:
                break
            i -= 1
            j += 1
        
        # Check the left upward diagonals
        i = y - 1
        j = x - 1
        
        while i <= 7  and i >= 0 and  j <= 7 and j>=0 :
            if (self.board.access_tile(i,j) !=0 and 
                self.board.access_tile(i,j).color != self.color and
                i == y-1 and 
                j == x-1 and
                self.board.access_tile(i,j).name in diag_pawn_king):
                attack_position.append(((i,j)))
                break
            
            if self.board.access_tile(i,j) == 0:
                pass
            elif self.board.access_tile(i,j).color != self.color:
                if self.board.access_tile(i,j).name in diag_piece:
                    attack_position.append(((i,j)))
                    break
                else:
                    break
            else:
                break
            i -= 1
            j -= 1
            
            
        # Check the right downwards diagonals
        i = y + 1
        j = x + 1
        
        while i <= 7  and i >= 0 and  j <= 7 and j>=0 :
            if (self.board.access_tile(i,j) !=0 and 
                self.board.access_tile(i,j).color != self.color and
                i == y+1 and 
                j == x+1 and
                self.board.access_tile(i,j).name in diag_pawn_king):
                attack_position.append(((i,j)))
                break
            
            if self.board.access_tile(i,j) == 0:
                pass
            elif self.board.access_tile(i,j).color != self.color:
                 if self.board.access_tile(i,j).name in diag_piece:
                    attack_position.append(((i,j)))
                    break
                 else:
                    break
            else:
                break
            
            i += 1
            j += 1
            
        # Check the left downwards diagonals
        i = y + 1
        j = x - 1
        
        while i <= 7  and i >= 0 and  j <= 7 and j>=0 :
            if (self.board.access_tile(i,j) !=0 and 
                self.board.access_tile(i,j).color != self.color and
                i == y+1 and 
                j == x-1 and
                self.board.access_tile(i,j).name in diag_pawn_king):
                attack_position.append(((i,j)))
                break
            
            if self.board.access_tile(i,j) == 0:
                pass
            elif self.board.access_tile(i,j).color != self.color:
                 if self.board.access_tile(i,j).name in diag_piece:
                    attack_position.append(((i,j)))
                    break
                 else:
                    break
            else:
                break
            
            i += 1
            j -= 1
        
        #Check Potential Knight moves 
           
            potential_knight = [(y - 2,x + 1),
                            (y - 2,x - 1),
                            (y + 2,x + 1),
                            (y + 2,x - 1),
                            (y + 1,x - 2),
                            (y + 1,x + 2),
                            (y - 1,x + 2),
                            (y - 1,x - 2)]
            
            
            for move in potential_knight:
            
             if (move[1] < 0 or move[1] > 7 
             or move[0] < 0 or move[0] > 7):
                 pass #No knight threat for there because its outside the board
             elif (self.board.access_tile(move[0], move[1]) != 0
                   and self.board.access_tile(move[0], move[1]).color != self.color
                   and self.board.access_tile(move[0], move[1]).name in knight_piece):
                 attack_position.append(move)
             else:
                pass
        
        for attack in attack_position:
            print(self.board.access_tile(*attack).name)
       
        print("safety was checked")
        return attack_position  
   
