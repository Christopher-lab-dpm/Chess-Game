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
         board_coord = PositionPlacement.mouse_to_board(mouse_position[0], mouse_position[1])
         
         if board_coord[1] < 0 or board_coord[1] > 7 or board_coord[0] < 0 or board_coord[0] > 7:
           #Cursor was not in the board
           return False #No move was made
           
         else:
           selected_tile = board.access_tile(board_coord[0], board_coord[1])
           #Check if there is a piece at that location and opposite color or 
           #if it a possible move
           if  (selected_tile != 0 and (board.get_turn() == selected_tile.color 
                or board_coord not in legal_moves)):
               print("That is an illegal move")
               board.change_moving_piece(None)
               return False #Move was not made
           
           elif (selected_tile == 0 and board_coord not in legal_moves):
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
    pieces_with_moves = 0
    for i in range(0,8):
        for j in range(0,8):
            current_piece = board.access_tile(i,j)
            if (current_piece != 0
               and current_piece.get_color() == board.get_turn()
               and current_piece.check_legal_moves(board) == [] ):
                    pass
            elif (current_piece != 0
               and current_piece.get_color() == board.get_turn()
               and current_piece.check_legal_moves(board) != []):
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
               
               for piece_loc in def_piece_loc:
                   
                   if board.access_tile(*piece_loc).name != king_type :
                       available_moves = board.access_tile(*piece_loc).check_legal_moves(board)
                       if attack in available_moves:
                           place_holder = board.access_tile(*piece_loc)
                           board.set_tile(*piece_loc, 0)
                           attack_origin2 = Piece_Safety.check_piece_safety(y,x,color,board)
                           if len(attack_origin2) > len(attack_origin):
                               #Not a valid move
                               board.set_tile(*piece_loc, place_holder)
                               continue
                           else:
                               return False
                       else:
                           continue
                   else:
                        continue
               print(message)
               set_game_over(board) 
               return True