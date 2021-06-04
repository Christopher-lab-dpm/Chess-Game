import pygame

import PositionPlacement
from Piece import Piece
#from BoardSettings import BoardSetting

class Pawn(Piece):
    #Location is a tuple (x,y) and the board is a 2D array
   def __init__(self, screen, color, name, board_coord):
       
       super(Pawn, self).__init__(screen, color, name, board_coord)
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
        if self.get_color() == "White" and y != 6:
            self.set_starting(False)
        elif self.get_color() == "Black" and y != 1:
            self.set_starting(False)
        else:
            pass
        
        
               
   def check_legal_moves(self,board): #Note, promotion should happen
                                #when the move is made, not checked again later
        legal_moves = []
        
        y = self.board_coord[0]
        x = self.board_coord[1]
        
        if self.get_color() == "White":
            # Check vertically upward in a file
            if y == 0:
                pass
            
            else:
                # Single move forward
                if board.access_tile(y -1,x) == 0:
                    legal_moves.append((y -1,x))
                #Double move at the start
                if (self.starting and board.access_tile(y -1,x) == 0
                    and board.access_tile(y -2,x) == 0):
                    legal_moves.append((y -2,x))
                    
                #En passant capture left and right
                if self.en_passantL: #en passant is allowed for white only this turn
                    legal_moves.append((y -1,x-1))
                                        
                if self.en_passantR: #en passant is allowed for white only this turn
                    legal_moves.append((y -1,x+1))
                    
                
                #Normal Capture
                #Check up and right
                if x == 7:
                    pass
                else:
                    if (board.access_tile(y -1,x + 1) != 0 and
                        board.access_tile(y -1,x+1).get_color() != self.get_color()):
                         legal_moves.append((y -1,x + 1))
                #Check up and left
                if x == 0 :
                    pass
                else:
                    if (board.access_tile(y -1,x - 1) != 0 and
                        board.access_tile(y -1,x - 1).color != self.get_color()):
                        legal_moves.append((y -1,x - 1))
       
        else:#Color is black
            # Check vertically downward in a file
            if y == 7:
                pass
            
            else:
                #Single move forward
                if board.access_tile(y +1,x) == 0:
                     legal_moves.append((y +1,x))
        
                #Double move at the start
                if (self.starting and 
                board.access_tile(y +1,x) == 0
                and board.access_tile(y +2,x) == 0):
                    legal_moves.append((y +2,x))
                    
                #En passant capture
                #En passant capture left and right
                if self.en_passantL: #en passant is allowed for black only this turn
                    legal_moves.append((y +1,x-1))
                    
                if self.en_passantR: #en passant is allowed for white only this turn
                    legal_moves.append((y +1,x+1))
                    
                
                #Normal Capture
                #Check down and right
                if x == 7:
                    pass
                else:
                    if (board.access_tile(y +1,x + 1) != 0 and
                        board.access_tile(y +1,x+1).get_color() != self.get_color()):
                         legal_moves.append((y +1,x + 1))
                #Check down and left
                if x == 0:
                    pass
                else:
                    if (board.access_tile(y +1,x - 1) != 0 and
                    board.access_tile(y +1,x - 1).get_color() != self.get_color()):
                        legal_moves.append((y +1,x - 1))    
        
         
        return legal_moves  