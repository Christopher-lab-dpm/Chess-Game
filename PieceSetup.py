"""Class for the Visual representation of the pieces"""

import pygame

from BoardSettings import BoardSetting
import PositionPlacement

from Piece import Piece
from Piece_King import King
from Piece_Queen import Queen
from Piece_Bishop import Bishop
from Piece_Knight import Knight
from Piece_Rook import Rook
from Piece_Pawn import Pawn

board_settings = BoardSetting()

class PieceSetup():
    
    def __init__(self,screen):
        self.screen =  screen
        
        self.name_dict ={'k':"BlackKing",'q':"BlackQueen","b":"BlackBishop",
                              'n': "BlackKnight",'p':"BlackPawn",'r':"BlackRook",
                              'K':"WhiteKing",'Q':"WhiteQueen",'B':"WhiteBishop",
                             'N': "WhiteKnight",'P':"WhitePawn",'R':"WhiteRook"}
        
        self.reverse_name_dict = {"BlackKing": 'k',"BlackQueen":'q',"BlackBishop":'b',
                               "BlackKnight":'n',"BlackPawn":'p',"BlackRook":'r',
                              "WhiteKing":'K',"WhiteQueen":'Q',"WhiteBishop":'B',
                             "WhiteKnight":'N',"WhitePawn":'P',"WhiteRook":'R'
            }
        
        self.place_dict = {'k':0,'q':1,"b":2,
                              'n':3,'p':4,'r':5,
                              'K':6,'Q':7,'B':8,
                             'N': 9,'P':10,'R':11}
        
        self.set_of_pieces = ["BlackKing","BlackQueen","BlackBishop",
                              "BlackKnight","BlackPawn","BlackRook",
                              "WhiteKing","WhiteQueen","WhiteBishop",
                              "WhiteKnight","WhitePawn","WhiteRook"]
    
        
    def select_piece(self, mouse_position, board):
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
                legal_moves = board.moving_piece.check_legal_moves()
            else: #The piece was the wrong color
                print("wrong color")
                pass
    
    def move_select_piece(self, mouse_position, board):
         """return false indicating that a new FEN must be loaded because internal board was altered
         Note that this was of doing it loses certain information such as en passant 
         priveleges"""
         legal_moves = board.moving_piece.check_legal_moves()
         board_coord = PositionPlacement.mouse_to_board(mouse_position[0], mouse_position[1])
         print (str(board_coord))
         if board_coord[1] < 0 or board_coord[1] > 7 or board_coord[0] < 0 or board_coord[0] > 7:
           #Cursor was not in the board
           return True #The move did not alter the board, no need to return false
           
         else:
           selected_tile = board.access_tile(board_coord[0], board_coord[1])
           #Check if there is a piece at that location and opposite color or 
           #if it a possible move
           if  (selected_tile != 0 and board.get_turn() == selected_tile.color 
                or board_coord not in legal_moves):
               print("That is an illegal move")
               board.change_moving_piece(None)
               return True #The move did not alter the board, no need to return false
           else: #The piece is of opposite color or empty square
           
           #Boolean legal_move helpls determine if the move did or didnt violate some other rules
           #Example exposing the king to check
           #If it did then we return false indicating that a new FEN must be loaded
               legal_move = board.change_piece_location(board_coord)
               if legal_move:
                   board.update_turn()
                   return True
               else:
                   checkmated = board.determine_checkmate()
                   print(checkmated)
                   return not(checkmated)
              
               
    def create_piece_add_to_board(self, current_piece_name, place, board):
        """This method creates peices and adds them to the board at the specified Location"""
        board_coord = PositionPlacement.screen_to_board(place[1], place[2])
        populate_tile = None
        row = board.access_row(board_coord[0]) 
        
        # Black Pieces checked First
        if current_piece_name == self.set_of_pieces[0]:
            king = King(self.screen, "Black", "BlackKing", (place[1],place[2]), board)
            populate_tile = king
            board.black_king = king
        elif current_piece_name == self.set_of_pieces[1]:
            queen = Queen(self.screen, "Black", "BlackQueen", (place[1],place[2]), board)
            populate_tile = queen
        elif current_piece_name == self.set_of_pieces[2]:
            bishop = Bishop(self.screen, "Black", "BlackBishop", (place[1],place[2]), board)
            populate_tile = bishop
        elif current_piece_name == self.set_of_pieces[3]:
            knight = Knight(self.screen, "Black", "BlackKnight", (place[1],place[2]), board)
            populate_tile = knight
        elif current_piece_name == self.set_of_pieces[4]:
            pawn = Pawn(self.screen, "Black", "BlackPawn", (place[1],place[2]), board)
            pawn_position = pawn.get_position()
            if pawn_position[0] != 1:
                pawn.set_starting(False)
            populate_tile = pawn    
        elif current_piece_name == self.set_of_pieces[5]:
            rook = Rook(self.screen, "Black", "BlackRook", (place[1],place[2]), board)
            populate_tile = rook
            
        # Now the white pieces get checked    
        elif current_piece_name == self.set_of_pieces[6]:
            king = King(self.screen, "White", "WhiteKing", (place[1],place[2]), board)
            populate_tile = king
            board.white_king = king
        elif current_piece_name == self.set_of_pieces[7]:
            queen = Queen(self.screen, "White", "WhiteQueen", (place[1],place[2]), board)
            populate_tile = queen
        elif current_piece_name == self.set_of_pieces[8]:
            bishop = Bishop(self.screen, "White", "WhiteBishop", (place[1],place[2]), board)
            populate_tile = bishop
        elif current_piece_name == self.set_of_pieces[9]:
            knight = Knight(self.screen, "White", "WhiteKnight", (place[1],place[2]), board)
            populate_tile = knight
        elif current_piece_name == self.set_of_pieces[10]:
            pawn = Pawn(self.screen, "White", "WhitePawn", (place[1],place[2]), board)
            pawn_position = pawn.get_position()
            if pawn_position[0] != 6:
                pawn.set_starting(False)
            populate_tile = pawn  
        elif current_piece_name == self.set_of_pieces[11]:
            rook = Rook(self.screen, "White", "WhiteRook", (place[1],place[2]), board)
            populate_tile = rook
        else:
            print("No piece could be made. This is not suppose to happen")
        
        row[board_coord[1]] = populate_tile
     
        
     
    def create_new_FEN(self, board):
        space_count = 0
        new_FEN=""
        for i in range(0,8):
            space_count = 0     
            for j in range(0,8):
                current_tile = board.access_tile(i,j)
                if current_tile != 0:#There is a piece there
                    if space_count != 0:
                        new_FEN += (str(space_count) + self.reverse_name_dict[current_tile.name])
                    else:
                        new_FEN += self.reverse_name_dict[current_tile.name]
                    space_count = 0
                else:
                    space_count += 1
                    
                if j == 7 and i != 7:
                    if space_count != 0:
                         new_FEN += str(space_count) + '/'
                    else: 
                         new_FEN += '/'
                         
                elif j ==7 and i == 7:
                    if space_count != 0:
                         new_FEN += str(space_count)
                         
        return new_FEN
        
    
    def blitme(self,FEN,board):
        """Draw the piece at its described location by the FEN."""
        placement  = PositionPlacement.convert_FEN(FEN)
       
        for place in placement:
            current_piece_name = self.name_dict[place[0]]
            self.create_piece_add_to_board(current_piece_name, place, board)
            board_coord = PositionPlacement.screen_to_board(place[1], place[2])
            board.access_tile(board_coord[0],board_coord[1]).blitme()
            
        


#FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
#board = [[0] * 8] * 8                                
#placement  = PositionPlacement.convert_FEN(FEN)   
#for place in placement:
#     board_coord = PositionPlacement.screen_to_board(place[1], place[2])
#     print(place[0] + " " +  str(board_coord))
#    board_coord = PositionPlacement.screen_to_board(place[1], place[2])
#    create_piece_add_to_board(current_piece_name, place, board)
#for i in range(0,7):
#    for j in range(0,7) :
#        print(board[i][j])





                                      
                                          