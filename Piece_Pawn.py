import pygame

import PositionPlacement
from Piece import Piece
#from BoardSettings import BoardSetting

class Pawn(Piece):
    #Location is a tuple (x,y) and the board is a 2D array
   def __init__(self, screen, color,name, location, board):
       
       super(Pawn, self).__init__(screen, color, name, location, board)
       self.image_file = "C:/Users/Christopher/Documents/Chess pieces"+"/"+name+".bmp"
       self.image = pygame.image.load(self.image_file)
       
       self.en_passantL = False #Assume starting position, this is for doing en passant left
       self.en_passantR = False #Assume starting position, this is for doing en passant right
       self.action_passant = False
       self.starting = True #Assume starting position
       
   
   def set_en_passant_left(self, boolean):
        self.en_passantL = boolean
       
   def set_en_passant_right(self, boolean):
        self.en_passantR = boolean
        
   def set_action_passant(self, boolean):
       self.action_passant = boolean
        
   def set_starting(self,boolean):
       self.starting = boolean
   
   def update_position(self,y,x): #Uses board coordinates 
        self.board_coord = (y,x)
        self.location = PositionPlacement.matrix_to_screen(y,x)
        
        #Necessary to check weather the double move is allowed
        if self.color == "White" and y != 6:
            self.set_starting(False)
        elif self.color == "Black" and y != 1:
            self.set_starting(False)
        else:
            pass
        
        
                 
                 
                 
   def check_legal_moves(self): #Note, promotion should happen
                                #when the move is made, not checked again later
        legal_moves = []
        
        if self.color == "White":
            # Check vertically upward in a file
            if self.board_coord[0] == 0:
                pass
            
            else:
                # Single move forward
                if self.board.access_tile(self.board_coord[0] -1,
                                           self.board_coord[1]) == 0:
                    legal_moves.append((self.board_coord[0] -1,self.board_coord[1]))
                #Double move at the start
                if (self.starting and 
                self.board.access_tile(self.board_coord[0] -1,self.board_coord[1]) == 0
                and self.board.access_tile(self.board_coord[0] -2,self.board_coord[1]) == 0):
                    legal_moves.append((self.board_coord[0] -2,self.board_coord[1]))
                    
                #En passant capture left and right
                if self.en_passantL: #en passant is allowed for white only this turn
                    legal_moves.append((self.board_coord[0] -1,self.board_coord[1]-1))
                                        
                if self.en_passantR: #en passant is allowed for white only this turn
                    legal_moves.append((self.board_coord[0] -1,self.board_coord[1]+1))
                    
                
                #Normal Capture
                #Check up and right
                if self.board_coord[1] == 7:
                    pass
                else:
                    if (self.board.access_tile(self.board_coord[0] -1,
                                               self.board_coord[1] + 1) != 0 and
                    self.board.access_tile(self.board_coord[0] -1,
                                               self.board_coord[1]+1).color != self.color):
                         legal_moves.append((self.board_coord[0] -1,
                                               self.board_coord[1] + 1))
                #Check up and left
                if self.board_coord[1] == 0 :
                    pass
                else:
                    if (self.board.access_tile(self.board_coord[0] -1,
                                               self.board_coord[1] - 1) != 0 and
                    self.board.access_tile(self.board_coord[0] -1,
                                               self.board_coord[1] - 1).color != self.color):
                        legal_moves.append((self.board_coord[0] -1,
                                               self.board_coord[1] - 1))
        else:#Color is black
            # Check vertically downward in a file
            if self.board_coord[0] == 7:
                pass
            
            else:
                #Single move forward
                if self.board.access_tile(self.board_coord[0] +1,
                                           self.board_coord[1]) == 0:
                     legal_moves.append((self.board_coord[0] +1,self.board_coord[1]))
        
                #Double move at the start
                if (self.starting and 
                self.board.access_tile(self.board_coord[0] +1,self.board_coord[1]) == 0
                and self.board.access_tile(self.board_coord[0] +2,self.board_coord[1]) == 0):
                    legal_moves.append((self.board_coord[0] +2,self.board_coord[1]))
                    
                #En passant capture
                #En passant capture left and right
                if self.en_passantL: #en passant is allowed for black only this turn
                    legal_moves.append((self.board_coord[0] +1,self.board_coord[1]-1))
                    
                if self.en_passantR: #en passant is allowed for white only this turn
                    legal_moves.append((self.board_coord[0] +1,self.board_coord[1]+1))
                    
                
                #Normal Capture
                #Check down and right
                if self.board_coord[1] == 7:
                    pass
                else:
                    if (self.board.access_tile(self.board_coord[0] +1,
                                               self.board_coord[1] + 1) != 0 and
                    self.board.access_tile(self.board_coord[0] +1,
                                               self.board_coord[1]+1).color != self.color):
                         legal_moves.append((self.board_coord[0] +1,
                
                                             self.board_coord[1] + 1))
                #Check down and left
                if self.board_coord[1] == 0:
                    pass
                else:
                    if (self.board.access_tile(self.board_coord[0] +1,
                                               self.board_coord[1] - 1) != 0 and
                    self.board.access_tile(self.board_coord[0] +1,
                                               self.board_coord[1] - 1).color != self.color):
                        legal_moves.append((self.board_coord[0] +1,
                                               self.board_coord[1] - 1))    
        
        self.legal_moves = legal_moves  
        return legal_moves  