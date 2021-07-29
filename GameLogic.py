# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 08:58:52 2021

@author: Christopher
"""
import PositionPlacement
import Piece_Safety

def set_game_over(board):
    board.set_white_turn(False)
    board.set_black_turn (False)
    board.change_moving_piece(None)
    board.set_game_over(True)
    print("The game is finished")
    
    
def update_turn(board):
    if board.get_turn() == "White":
         board.set_white_turn(False)
         board.set_black_turn (True)
         
    elif board.get_turn() == "Black":
         board.set_white_turn(True)
         board.set_black_turn (False)
    else:
        set_game_over(board)
        

def select_piece(mouse_position, board):
        """Select the piece that the user intends to move"""
        # note that mouse positon is a tuple (x,y) in screen coordonintes
        board_coord = PositionPlacement.mouse_to_board(mouse_position[0], mouse_position[1])
        # We are now working in (y,x)
        #Because of the way the conversion of coordinates was mplemented, it 
        #already returns the correct point on the board iff the cursor is in the board
       
        if board_coord[1] < 0 or board_coord[1] > 7 or board_coord[0] < 0 or board_coord[0] > 7:
           #Cursor was not in the board
           pass
        else:
           maybe_piece = board.access_tile(board_coord[0], board_coord[1])
           #Check if there is a piece at that location
           if maybe_piece == 0:
               pass
           elif board.get_turn() == maybe_piece.color:
               board.change_moving_piece(maybe_piece)
              
           else: #The piece was the wrong color
               print("Wrong color")
               pass

def move_piece(mouse_position, board):
         """return false indicating that a new FEN must be loaded because internal board was altered
         Note that this was of doing it loses certain information such as en passant 
         priveleges"""
         legal_moves = board.get_moving_piece().check_legal_moves(board)
         allowed_moves = board.get_moving_piece().check_allowed_moves(board, legal_moves)
         
         board_coord = PositionPlacement.mouse_to_board(mouse_position[0], mouse_position[1])
         
         if board_coord[1] < 0 or board_coord[1] > 7 or board_coord[0] < 0 or board_coord[0] > 7:
           #Cursor was not in the board
           return False #No move was made
           
         else:
           selected_tile = board.access_tile(board_coord[0], board_coord[1])
           #Check if there is a piece at that location and opposite color or 
           #if it a possible move
           if  (selected_tile != 0 and (board.get_turn() == selected_tile.color 
                or board_coord not in allowed_moves)):
               print("That is an illegal move")
               board.change_moving_piece(None)
               return False #Move was not made
           
           elif (selected_tile == 0 and board_coord not in allowed_moves):
               print("That is an illegal move")
               board.change_moving_piece(None)
               return False
            
           else: #The piece is making a legal move (not counting checks and stuff)
           
           #Boolean legal_move helps determine if the move did or didnt violate some other rules
           #Example exposing the king to check
          
               legal_move = board.change_piece_location(board_coord)
               if legal_move:
                   return True
               else:
                  return False
              
                
def determine_stalemate(board):
    if board.White_in_check or board.Black_in_check:
        return
    pieces_with_moves = 0
    for i in range(0,8):
        for j in range(0,8):
            current_piece = board.access_tile(i,j)
            if current_piece != 0:
              legal_moves = current_piece.check_legal_moves(board)
              
            if (current_piece != 0
               and current_piece.get_color() == board.get_turn()
               and current_piece.check_allowed_moves(board,legal_moves) == [] ):
                    pass
            elif (current_piece != 0
               and current_piece.get_color() == board.get_turn()
               and current_piece.check_allowed_moves(board,legal_moves) != []):
                    pieces_with_moves += 1
            else: 
                pass
    
    if pieces_with_moves == 0:#stalemate
         print("Stalemate")
         set_game_over(board)
    else:#Opponent still has moves to be played
        pass


def determine_checkmate(board):
        x = None
        y = None
        attack_origin = None
        attack_origin2 = None
        king_type = None    

        """True for checkmate, False for no chekcmate"""
        if board.white_turn and board.White_in_check:
               y = board.get_white_king().board_coord[0]
               x = board.get_white_king().board_coord[1]
               color = "White"
               message = "White is checkmated"
               king_type = "WhiteKing" 
               bool_king_moves = (board.get_white_king().
                                  check_legal_moves(board) != [])
               
        elif board.black_turn and board.Black_in_check:
               y = board.get_black_king().board_coord[0]
               x = board.get_black_king().board_coord[1]
               color = "Black"
               message = "Black is checkmated"
               king_type = "BlackKing"
               bool_king_moves = (board.get_black_king().
                                  check_legal_moves(board) != [])
        else:
            return False
        
             
        if bool_king_moves:
            return False
        else:
           attack_origin = Piece_Safety.check_piece_safety(y,x,color,board)
           
           if len(attack_origin) >= 2:
               print(message)
               set_game_over(board) 
               return True
           else:
               attack = attack_origin[0] #by now we know len(attack_origin) == 1
              
               attack_color = board.access_tile(*attack).get_color()
               def_piece_loc = Piece_Safety.check_piece_safety(*attack,attack_color,board)
               
               #Check to see if attacking piece may be captured
               for piece_loc in def_piece_loc:
                   
                   if board.access_tile(*piece_loc).name != king_type :
                       
                           place_holder = board.access_tile(*piece_loc)
                           board.set_tile(*piece_loc, 0)
                           attack_origin2 = Piece_Safety.check_piece_safety(y,x,color,board)
                           if len(attack_origin2) > len(attack_origin):
                               #Not a valid move, it put the king in danger
                               board.set_tile(*piece_loc, place_holder)
                               continue
                           else:
                               #But this is only if a peice can attack the piece 
                               #giving check, it doesn't account for blocking
                               board.set_tile(*piece_loc, place_holder)
                                   
                               return False
                      
               #By this point, attacking may not be captured
               #Check for blocks, only bishops, rooks and queens may be blocked
               for i in range(0,8):
                   for j in range (0,8):
                       if (board.access_tile(i,j) != 0
                           and board.access_tile(i,j).get_color() == color):
                           def_piece_moves = board.access_tile(i,j).check_legal_moves(board)
                           
                           place_holder = board.access_tile(i,j)
                           board.set_tile(i,j, 0)
                           attack_origin2 = Piece_Safety.check_piece_safety(y,x,color,board)
                           if place_holder.name == king_type:
                               board.set_tile(i,j, place_holder)
                               continue
                           elif def_piece_moves == []:
                               board.set_tile(i,j, place_holder)
                               continue
                           elif len(attack_origin2) > len(attack_origin):
                               #No a valid moves, it put the king in danger
                               board.set_tile(i,j, place_holder)
                               continue
                           else:
                               board.set_tile(i,j, place_holder)
                               #Now we know u can make a move
                               #To block, check the intersection between the 
                               #List of  moves that can be made by the attacking piece
                               #The list of moves by the defending piece
                               #Check king safety again, if no attack pieces, then no check mate
                               #else checkmate once loop is finished
                               attacking_moves = board.access_tile(*attack).check_legal_moves(board)
                               intersection = set(def_piece_moves).intersection(attacking_moves)
                               #Note the intersection can ony be empty squares
                               for move in  intersection:
                                   board.set_tile(*move,  board.access_tile(i,j) )
                                   attack_origin2 = Piece_Safety.check_piece_safety(y,x,color,board)
                                   if len(attack_origin2) < len(attack_origin):
                                       #The attack is successfully blocked!
                                       board.set_tile(*move, 0)
                                       return False
                                   else:
                                       board.set_tile(*move, 0)
                                       continue
               #Attack could not be stopped by taking piece or blocking
               #Enemy was checkmated    
               print(message)
               set_game_over(board) 
               return True