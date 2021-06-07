# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 10:35:49 2021

@author: Christopher
"""

def check_piece_safety(y,x,color,board): 
    #Enter the position of the piece currently
    #check if the piece is in danger there, i.e. can be captured
    # color is the color of the piece we are checking danger for
                     
        attack_position = []                    
                           
        #check file for rook or queen
        file_row_piece = ["WhiteRook","WhiteQueen","BlackRook","BlackQueen"]
        
        diag_piece = ["WhiteBishop","BlackBishop","WhiteQueen","BlackQueen"]
        
        diag_pawn_king = ["WhiteKing","BlackKing","BlackPawn","WhitePawn"]
        
        knight_piece = ["WhiteKnight","BlackKnight"]
        
        king_piece = ["WhiteKing" , "BlackKing"]
        
         # Check vertically upward in a file
        for i in reversed(range(0,y)):
             
             if  board.access_tile(i,x) == 0:
                 pass
                 
             elif (board.access_tile(i,x).get_color() != color
                     and board.access_tile(i,x).name in file_row_piece) :
                     attack_position.append(((i,x)))
                     break
             else:
                 break
          
         # Check vertically downward in a file
        for i in range(y + 1, 8):
             if  y + 1 == 8:#edge of board
                 break
             if  board.access_tile(i,x) == 0:
                pass
                 
             elif (board.access_tile(i,x).get_color() != color
                  and board.access_tile(i,x).name in file_row_piece):
                     attack_position.append(((i,x)))
                     break
                  
             else:
                 break
        
         
         # Check Laterally right in a row
        for j in range(x+1,8):
             if x+1 == 8: #edge of board
                 break
             if  board.access_tile(y,j) == 0:
                 pass
             elif ( board.access_tile(y,j).get_color() != color
                   and board.access_tile(y,j).name in file_row_piece ):
                     attack_position.append(((y,j)))
                     break
             else:
                 break
         
         # Check Laterally left in a row
        for j in reversed(range(0,x)):
             if  board.access_tile(y,j) == 0:
                 pass
             elif (board.access_tile(y,j).get_color() != color
                 and board.access_tile(y,j).name in file_row_piece):
                     attack_position.append(((y,j)))
                     break
             
             else:
                 break   
         
               
        # Check the right upward diagonals
        i = y - 1
        j = x + 1
        
        while i <= 7  and i >= 0 and  j <= 7 and j>=0 :
            if board.access_tile(i,j) == 0:
                pass
            
            elif (board.access_tile(i,j).get_color() != color 
                  and i == y-1 and j == x+1 
                  and board.access_tile(i,j).name in diag_pawn_king):
                    
                    if board.access_tile(i,j).name == "WhitePawn":
                        break
                    else:
                        attack_position.append(((i,j)))
                        break
              
            elif (board.access_tile(i,j).get_color() != color
                 and board.access_tile(i,j).name in diag_piece):
                    attack_position.append(((i,j)))
                    break
                
            else:
                break
            
            i -= 1
            j += 1
        
        
        # Check the left upward diagonals
        i = y - 1
        j = x - 1
        
        while i <= 7  and i >= 0 and  j <= 7 and j>=0 :
           if board.access_tile(i,j) == 0:
                pass
            
           elif (board.access_tile(i,j).get_color() != color 
                 and i == y-1 and  j == x-1 
                 and board.access_tile(i,j).name in diag_pawn_king):
                    
                    if board.access_tile(i,j).name == "WhitePawn":
                        break
                    else:
                        attack_position.append(((i,j)))
                        break
            
           elif (board.access_tile(i,j).get_color() != color
                and board.access_tile(i,j).name in diag_piece):
                    attack_position.append(((i,j)))
                    break
            
           else:
                break
           i -= 1
           j -= 1
            
            
        # Check the right downwards diagonals
        i = y + 1
        j = x + 1
        
        while i <= 7  and i >= 0 and  j <= 7 and j>=0 :
            if board.access_tile(i,j) == 0:
                pass
            
            elif (board.access_tile(i,j).get_color() != color 
                  and i == y+1 and j == x+1 
                  and board.access_tile(i,j).name in diag_pawn_king):
                    
                    if board.access_tile(i,j).name == "BlackPawn":
                        break
                    else:
                        attack_position.append(((i,j)))
                        break
            
            
            elif board.access_tile(i,j).get_color() != color:
                 if board.access_tile(i,j).name in diag_piece:
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
            if board.access_tile(i,j) == 0:
                pass
            
            elif (board.access_tile(i,j).get_color() != color 
                  and i == y+1 and j == x-1 
                  and board.access_tile(i,j).name in diag_pawn_king):
                
                    if board.access_tile(i,j).name == "BlackPawn":
                        break
                    else:
                        attack_position.append(((i,j)))
                        break
            
            
            elif (board.access_tile(i,j).get_color() != color
                 and board.access_tile(i,j).name in diag_piece):
                    attack_position.append(((i,j)))
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
         elif (board.access_tile(move[0], move[1]) != 0
               and board.access_tile(move[0], move[1]).get_color() != color
               and board.access_tile(move[0], move[1]).name in knight_piece):
             
             attack_position.append(move)
             
         else:
            pass
   
    
        
        #Check if enemy king is in adjacent, non-diagonal squares
        enemy_king = [(y-1 ,x),
                  (y+1,x),
                  (y,x-1),
                  (y,x+1)]
        
        for enemy in enemy_king:
            
         if (enemy[1] < 0 or enemy[1] > 7 
         or enemy[0] < 0 or enemy[0] > 7):
             pass #outside the board
         elif (board.access_tile(enemy[0], enemy[1]) != 0
               and board.access_tile(enemy[0], enemy[1]).get_color() != color
               and board.access_tile(enemy[0], enemy[1]).name in king_piece):
             attack_position.append(enemy)
         else:
            pass
        
        return attack_position 