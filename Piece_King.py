import pygame

import Piece_Safety
from Piece import Piece
#from BoardSettings import BoardSetting

class King(Piece):
    #Location is a tuple (x,y) and the board is a 2D array
   def __init__(self, screen, color, name, board_coord):
       
       super(King, self).__init__(screen, color, name, board_coord)
       self.image_file = "Chess pieces"+"/"+name+".bmp"
       self.image = pygame.image.load(self.image_file)
       self.moved = True
       
   def has_moved(self):
       return self.moved
   
   def set_moved(self, boolean):
       self.moved =  boolean
   
   def check_castling(self, board):
       castling_moves = []
       kings = ["WhiteKing", "BlackKing"]
       rooks = ["WhiteRook", "BlackRook"]
       king_square = None
       rook_squares = None
       in_betweenR = None
       coord_R = None
       
       in_betweenL = None
       coord_L = None
       
       if board.get_turn() == "White":
           king_square = board.access_tile(7,4)
           rook_squares = [board.access_tile(7,0) , board.access_tile(7,7)]
           in_betweenL = [board.access_tile(7,3), board.access_tile(7,2),
                          board.access_tile(7,1)]
           coord_L = [(7,3),(7,2)]
           in_betweenR = [board.access_tile(7,5), board.access_tile(7,6)]
           coord_R = [(7,5),(7,6)] 
       elif board.get_turn() == "Black":
           king_square = board.access_tile(0,4)
           rook_squares = [board.access_tile(0,0) , board.access_tile(0,7)]
           in_betweenL = [board.access_tile(0,3), board.access_tile(0,2),
                          board.access_tile(0,1)]
           coord_L = [(0,3),(0,2)]
           in_betweenR = [board.access_tile(0,5), board.access_tile(0,6)]
           coord_R = [(0,5),(0,6)]
       else:
           return castling_moves
           
       if ( king_square != 0
            and (board.White_in_check or board.Black_in_check) == False
            and king_square.name in kings 
            and king_square.get_color() == board.get_turn()
            and king_square.has_moved() == False):
           
            for rook_square in rook_squares:
                if ( rook_square != 0
                and rook_square.name in rooks
                and rook_square.get_color() == board.get_turn()
                and rook_square.has_moved() == False):
                    #Check left first
                  if rook_square.get_position()[1] == 0:  
                        if(in_betweenL[0] == 0 and
                           in_betweenL[1] == 0 and
                           in_betweenL[2] == 0):
                            
                            threat1 = Piece_Safety.check_piece_safety(
                                *coord_L[0], board.get_turn() , board)
                            threat2  = Piece_Safety.check_piece_safety(
                                *coord_L[1], board.get_turn(), board)
                            if (len(threat1) == 0 and len(threat2) == 0):
                                castling_moves.append(coord_L[1])
                            
                  if rook_square.get_position()[1] == 7:
                    #check right
                        if( in_betweenR[0] == 0 and
                           in_betweenR[1] == 0):
                            
                            threat1 = Piece_Safety.check_piece_safety(
                                *coord_R[0], board.get_turn(), board)
                            threat2  = Piece_Safety.check_piece_safety(
                                *coord_R[1], board.get_turn(), board)
                            if (len(threat1) == 0 and len(threat2) == 0):
                                castling_moves.append(coord_R[1])        
                else:
                    continue
        
       else:
           return []
       
        
       return castling_moves
   
   def check_legal_moves(self, board):
      moves = []
      legal_moves = []
      
      for i in range(-1,2):
          for j in range(-1,2):
              y = self.board_coord[0] + i
              x = self.board_coord[1] + j
                            
              if i == 0 and j == 0:
                  pass
              elif x < 0 or x > 7 or y < 0 or y > 7:
                  pass
              elif (board.access_tile(y,x) != 0 and
                     board.access_tile(y,x).color == self.color):
                     pass
              elif (board.access_tile(y,x) != 0 and
                    board.access_tile(y,x).color != self.color):
                  moves.append((y,x))
              else: 
                  moves.append((y,x))
      
      for move in moves:
               placeholder = self   
               board.set_tile(*self.board_coord, 0)
               attack_list =  Piece_Safety.check_piece_safety(*move,self.color,board)
               if len(attack_list) == 0: #king is not attacked at the given square
                   legal_moves.append(move)
               else:
                   pass
               board.set_tile(*placeholder.get_position(), placeholder)    
      
      #Check for castle-ing
      casting_moves  = self.check_castling(board)         
      
      all_legal_moves = legal_moves + casting_moves
      
      return all_legal_moves
  
 
   def check_allowed_moves(self,board, legal_moves):
       return super().check_allowed_moved(board, legal_moves)           
            