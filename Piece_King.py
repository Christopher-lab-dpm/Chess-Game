import pygame

from Piece import Piece
#from BoardSettings import BoardSetting

class King(Piece):
    #Location is a tuple (x,y) and the board is a 2D array
   def __init__(self, screen, color,name, location, board):
       
       super(King, self).__init__(screen, color, name, location, board)
       self.image_file = "C:/Users/Christopher/Documents/Chess pieces"+"/"+name+".bmp"
       self.image = pygame.image.load(self.image_file)
       
  
   def check_legal_moves(self):
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
              elif (self.board.access_tile(y,x) != 0 and
                     self.board.access_tile(y,x).color == self.color):
                     pass
              elif (self.board.access_tile(y,x) != 0 and
                     self.board.access_tile(y,x).color != self.color):
                  moves.append((y,x))
              else: 
                  moves.append((y,x))
      
      for move in moves:
               placeholder = self   
               self.board.set_tile(*self.board_coord, 0)
               attack_list =  self.check_k(*move)
               if len(attack_list) == 0: #king is not attacked at the given square
                   legal_moves.append(move)
               
               self.board.set_tile(*placeholder.board_coord, placeholder)    
      self.legal_moves = legal_moves        
      return legal_moves
            
            