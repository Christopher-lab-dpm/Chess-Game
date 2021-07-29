import pygame

from BoardSettings import BoardSetting
import PositionPlacement
import Piece_Safety

from Piece import Piece
from Piece_King import King
from Piece_Queen import Queen
from Piece_Bishop import Bishop
from Piece_Knight import Knight
from Piece_Rook import Rook
from Piece_Pawn import Pawn


class Board():
    def __init__(self, screen):
        
        self.screen =  screen
        
        self.setting = BoardSetting()        
        #This creates 2D array where each array is seperate
        self.board = [[0]*8 for _ in range(8)]
        
        self.white_turn = True
        self.black_turn = False
        self.game_over = False
       
        self.White_in_check = False
        self.white_king  = None
        self.Black_in_check = False
        self.black_king  = None
        
        self.location_capture = None
        self.moving_piece = None
        
        
        
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
        
        
        self.classical_dict = {'a':0,'b':1,"c":2,
                              'd':3,'e':4,'f':5,
                              'g':6,'h':7}
       
        self.reverse_classical_dict = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4:'e', 
                                       5: 'f', 6: 'g', 7: 'h' }
    
    
    
    def change_piece_location(self,new_location):#New location (y,x) aka (i,j)
        old_location =  self.moving_piece.get_position() # Of piece that just moved    
        self.location_capture = None
        en_passant_capture = False
        pawn_promoted = False
        
        #Logic for allowing the capture of pieces 
        en_passant_capture = self.allow_piece_capture(old_location, 
                                                        new_location)
        
        #Check and setup en passant for other pawns if need be
        self.set_up_en_passant(old_location, new_location)
        
        
        pawn_promoted = self.pawn_promotion(old_location, new_location)
        
        self.castle_king(old_location, new_location)
        
        #update the board and moving piece position/value    
        self.board[old_location[0]][old_location[1]] = 0
        self.board[new_location[0]] [new_location[1]] = self.moving_piece
        self.moving_piece.update_position(new_location[0], new_location[1])
        self.moving_piece = None
        
        self.check_king_safety()
                
        if self.Black_in_check and not(self.White_in_check) and self.white_turn:
            self.reset_en_passant()
            return True
        elif (self.White_in_check and self.white_turn) or (self.Black_in_check 
             and self.black_turn):
            
            #self.undo_illegal_move(old_location, new_location,en_passant_capture,
                                   #pawn_promoted)
            
           # print("Not a valid move \n")
            return False
        
        elif self.White_in_check and not(self.Black_in_check) and self.black_turn:
            self.reset_en_passant()
            return True

        else:
            self.reset_en_passant()
            return True
        
    

    def computer_change_piece_location(self,new_location):#New location (y,x) aka (i,j)
        old_location =  self.moving_piece.get_position() # Of piece that just moved    
        self.location_capture = None
        en_passant_capture = False
        pawn_promoted = False
        
        #Logic for allowing the capture of pieces 
        en_passant_capture = self.allow_piece_capture(old_location, 
                                                        new_location)
        
        #Check and setup en passant for other pawns if need be
        self.set_up_en_passant(old_location, new_location)
        
        
        pawn_promoted = self.computer_pawn_promotion(old_location, new_location)
        
        self.castle_king(old_location, new_location)
        
        #update the board and moving piece position/value    
        self.board[old_location[0]][old_location[1]] = 0
        self.board[new_location[0]] [new_location[1]] = self.moving_piece
        self.moving_piece.update_position(new_location[0], new_location[1])
        self.moving_piece = None
        
        self.check_king_safety()
                
        if self.Black_in_check and not(self.White_in_check) and self.white_turn:
            self.reset_en_passant()
            return True
        elif (self.White_in_check and self.white_turn) or (self.Black_in_check 
             and self.black_turn):
            
            #self.undo_illegal_move(old_location, new_location,en_passant_capture,
                                   #pawn_promoted)
            
           # print("Not a valid move \n")
            return False
        
        elif self.White_in_check and not(self.Black_in_check) and self.black_turn:
            self.reset_en_passant()
            return True

        else:
            self.reset_en_passant()
            return True






               
    def check_king_safety(self):
        y = self.black_king.board_coord[0]
        x = self.black_king.board_coord[1]
        black_threat = Piece_Safety.check_piece_safety(y,x,"Black",self) #Check black king safety
        
        if len(black_threat) != 0:
                self.Black_in_check = True
        else:
                self.Black_in_check = False
                 
    
        y = self.white_king.board_coord[0]
        x = self.white_king.board_coord[1]
        white_threat = Piece_Safety.check_piece_safety(y,x,"White",self)#Check white king safety
      
        if len(white_threat) != 0:
            self.White_in_check = True   
        else:
             self.White_in_check = False
                 
      
            
    def castle_king(self,old_location, new_location):#IMPORTANT
        ##Set the moving values for rook and king if need be
        ##ONlY move the rook, logic for moving king is already done
        selected_piece = self.access_tile(*old_location)
        
        position = selected_piece.get_position()
        kings = ["BlackKing", "WhiteKing"]
        rooks =  ["BlackRook", "WhiteRook"]
        if selected_piece.name in rooks:
            rook = self.access_tile(*old_location)#access rook
            rook.set_moved(True)
            return
        
        x_distance = abs(new_location[1] - old_location[1])
        if (selected_piece.name in kings and x_distance == 2):#King is castling
            if (new_location[1] - old_location[1]) < 0: #castled long, aka left
                rook = self.access_tile(old_location[0], 0)#access rook
                rook.set_moved(True)
                selected_piece.set_moved(True)
                self.set_tile(old_location[0], old_location[1] - 1, rook)#move rook
                self.access_tile(old_location[0], #update rook location
                                 old_location[1] - 1).update_position(
                                                    old_location[0], 
                                                    old_location[1] - 1)
                self.set_tile(old_location[0], 0, 0)
            else:#Castled short
                rook = self.access_tile(old_location[0], 7)#access rook
                rook.set_moved(True)
                selected_piece.set_moved(True)
                self.set_tile(old_location[0], old_location[1] + 1, rook)#move rook
                self.access_tile(old_location[0], #update rook location
                                 old_location[1] + 1).update_position(
                                                    old_location[0], 
                                                    old_location[1] + 1)
                self.set_tile(old_location[0], 7, 0)                     
        
        elif (selected_piece.name in kings and x_distance != 2):
            selected_piece.set_moved(True)
        elif selected_piece.name in rooks:
            selected_piece.set_moved(True)
        else:    
            pass
        
    
    
    
    def set_up_en_passant(self,old_location, new_location):
        #Check if en passant needs to be initialized for other pieces
        if (abs(new_location[0] - old_location[0]) == 2  
            and (self.moving_piece.name == "BlackPawn" or 
            self.moving_piece.name =="WhitePawn")):
                 
                #See if en_passant is possible for White
                if self.moving_piece.color == "Black":#Black just moved two squares
                    #Check to left of black piece. Right of white piece
                   if (new_location[1] > 0 and
                     self.board[new_location[0]] [new_location[1]-1] !=0  and 
                      self.board[new_location[0]] [new_location[1]-1].name == "WhitePawn"):  
                          self.board[new_location[0]] [new_location[1]-1].set_en_passant_right(True)
                   
                   #Check to right of black piece. left of white piece 
                   if (new_location[1] < 7 and 
                       self.board[new_location[0]] [new_location[1]+1] !=0  and 
                      self.board[new_location[0]] [new_location[1]+1].name == "WhitePawn"):
                       self.board[new_location[0]] [new_location[1]+1].set_en_passant_left(True)
                
                #Check en passant for black         
                elif  self.moving_piece.color == "White": #White just moved two squares
                    #Check to left of white piece. Right of black piece
                   if (new_location[1] > 0 and
                       self.board[new_location[0]] [new_location[1]-1] !=0  and 
                      self.board[new_location[0]] [new_location[1]-1].name == "BlackPawn"):  
                          self.board[new_location[0]] [new_location[1]-1].set_en_passant_right(True)
                   
                   #Check to right of white piece. left of black piece 
                   if (new_location[1] < 7 and
                       self.board[new_location[0]] [new_location[1]+1] !=0  and 
                      self.board[new_location[0]] [new_location[1]+1].name == "BlackPawn"):
                       self.board[new_location[0]] [new_location[1]+1].set_en_passant_left(True)
                else:
                     pass
    
    def reset_en_passant(self):
        pawn = ["BlackPawn", "WhitePawn" ] 
        for i in range(0,8):
            for j in range(0,8):
                if (self.access_tile(i,j) != 0 and 
                   self.access_tile(i,j).name in pawn and 
                   self.access_tile(i, j).color == self.get_turn()):
                       self.access_tile(i, j).set_en_passant_right(False)
                       self.access_tile(i, j).set_en_passant_left(False)
     
    def allow_piece_capture (self, old_location, new_location):
        if self.access_tile(*new_location) != 0: # Not an empty square
                # A capture has just occured!
                #Hold on to captured piece in case move was illegal
                self.location_capture = self.access_tile(*new_location)
                #Remove the piece
                self.board[new_location[0]] [new_location[1]] = 0 #remove the piece
                return False
            
        #The following is the logic which enables en passant capture to occur        
        elif (self.access_tile(*new_location) == 0 and
        (self.moving_piece.name =="BlackPawn" or self.moving_piece.name == "WhitePawn")
        and (old_location[0] != new_location[0] and old_location[1] != new_location[1])):
            #En passant capture has just occured.
                    #remove the piece
                    print("EN PASSANT")
                    self.location_capture = self.access_tile(old_location[0], 
                                                            new_location[1])
                    
                    self.board[old_location[0]] [new_location[1]] = 0
                   
                    return True
        else:
            return False
    
    def pawn_promotion(self, old_location, new_location):
        #Check if pawn needs to be promoted to: Queen, Knight, Bishop, Rook            
        if ((self.moving_piece.name == "BlackPawn" and new_location[0] == 7) or 
            (self.moving_piece.name =="WhitePawn" and new_location[0] == 0)):
            
                #promote the pawn
                allowed_inputs = ['q','n','b','r']
                message = ("Enter q for Queen \n"+"b for bishop \n"+ 
                           "n for knight \n" +"r for rook \n " + "Entry:")
                promote = ""
                while True:
                    promote = input(message)
                    if promote.lower() in allowed_inputs:
                        break
                if self.moving_piece.color =="White":
                    promote = (promote.strip()).capitalize()
                else:
                    promote = promote.strip()
                    
                
                piece_name = self.name_dict[promote]
                #Needs to have the extra 0 for padding because of the way the 
                #function was written
                position = self.get_moving_piece().get_position()
                
                self.create_piece_add_to_board(piece_name, 
                                               position[0], position[1])
                
                self.change_moving_piece(self.access_tile(old_location[0],
                                                          old_location[1]))
                return True
        else:
                return False
            
    def computer_pawn_promotion(self, old_location, new_location):
        #Check if pawn needs to be promoted to: Queen, Knight, Bishop, Rook            
        if ((self.moving_piece.name == "BlackPawn" and new_location[0] == 7) or 
            (self.moving_piece.name =="WhitePawn" and new_location[0] == 0)):
            
                #promote the pawn
                allowed_inputs = ['q','n','b','r']
               
                promote = "q"
                
                if self.moving_piece.color =="White":
                    promote = (promote.strip()).capitalize()
                else:
                    promote = promote.strip()
                    
                
                piece_name = self.name_dict[promote]
                #Needs to have the extra 0 for padding because of the way the 
                #function was written
                position = self.get_moving_piece().get_position()
                
                self.create_piece_add_to_board(piece_name, 
                                               position[0], position[1])
                
                self.change_moving_piece(self.access_tile(old_location[0],
                                                          old_location[1]))
                return True
        else:
                return False
    
    def undo_illegal_move(self, old_location, new_location,
                          en_passant_capture, pawn_promoted):
                                                    
            #Undo the move
        
            if(self.location_capture == None and
               en_passant_capture == False
               and pawn_promoted == False):#Reset as normal
                                         
                self.set_tile(old_location[0], old_location[1], 
                              self.access_tile(*new_location))
                self.access_tile(*old_location).update_position(*old_location)
                self.set_tile(*new_location, 0)
                
            elif (self.location_capture != None and en_passant_capture == False
                and pawn_promoted == False):
               
                #it was a normal capture
                self.set_tile(old_location[0], old_location[1], 
                              self.access_tile(*new_location))
                self.access_tile(*old_location).update_position(*old_location)
                self.set_tile(*new_location, self.location_capture)
                self.access_tile(*new_location).update_position(*new_location)
                
            elif (self.location_capture != None and en_passant_capture == True
                and pawn_promoted == False):    
                #You captured en passant
                self.set_tile(old_location[0], old_location[1], 
                              self.access_tile(*new_location))
                self.access_tile(*old_location).update_position(*old_location)
                self.set_tile(*new_location, 0)
                
                self.set_tile(old_location[0],new_location[1], self.location_capture)
                self.access_tile(old_location[0],new_location[1]).update_position(
                    old_location[0],new_location[1])
            
            elif pawn_promoted:
                pawntype = 'BlackPawn'
                if  self.access_tile(*new_location).get_color() =="Black":
                    pawntype = 'BlackPawn'
                else:
                     pawntype = 'WhitePawn'
                     
                self.set_tile(*new_location,0)     
                self.create_piece_add_to_board(pawntype,old_location[0], 
                                               old_location[1])
                self.access_tile(*old_location).update_position(*old_location)
                if self.location_capture == None:
                    pass
                else:#A piece was captured and must be put back
                    self.set_tile(*new_location,self.location_capture)
                    self.access_tile(*new_location).update_position(*new_location)
                    
            else:
                pass
                
    
    
    def is_moving_piece(self):
        """Returns a boolean letting us know is a piece is trying to move"""
        if self.moving_piece != None:
            return True
        else:
            return False
        
    def change_moving_piece(self,piece):
        self.moving_piece = piece
    
    def get_moving_piece(self):
        return self.moving_piece
        
    def access_tile(self,y,x):
         """Returns what is store at the give position on the board input as (y,x)"""
         return self.board[y][x]
     
    def set_tile(self,y,x,value):
        self.board[y][x] = value
    
    def access_row(self,y):
        return self.board[y]
         
    def set_turn(self, color):
        if color == 'w' or color == "White":
             self.white_turn = True
             self.black_turn = False
        elif color == "b" or color == "Black":
            self.white_turn = False
            self.black_turn = True
      
        else:
             pass
    
    def get_turn(self):
        if self.white_turn:
            return "White"
        elif self.black_turn:
            return "Black"
        else:
            return None
    
    def get_white_king(self):
        return self.white_king
    
    def get_black_king(self):
        return self.black_king  
    
   
    
    def get_white_turn(self):
         return self.white_turn
     
    def set_white_turn(self, boolean):
          self.white_turn = boolean
   
    def get_black_turn(self):
        return self.black_turn
    
    def set_black_turn(self,boolean):
        self.black_turn = boolean
        
    def get_game_over(self):
         return self._game_over
     
    def set_game_over(self, boolean):
          self.game_over = boolean    
   
    
    def create_piece_add_to_board(self, current_piece_name, y, x):
        """This method creates peices and adds them to the board at the specified Location"""
        
        populate_tile = None
        row = self.access_row(y) 
        
        # Black Pieces checked First
        if current_piece_name == self.set_of_pieces[0]:
            king = King(self.screen, "Black", "BlackKing", (y, x))
            populate_tile = king
            self.black_king = king
        elif current_piece_name == self.set_of_pieces[1]:
            queen = Queen(self.screen, "Black", "BlackQueen", (y, x))
            populate_tile = queen
        elif current_piece_name == self.set_of_pieces[2]:
            bishop = Bishop(self.screen, "Black", "BlackBishop", (y, x))
            populate_tile = bishop
        elif current_piece_name == self.set_of_pieces[3]:
            knight = Knight(self.screen, "Black", "BlackKnight", (y, x))
            populate_tile = knight
        elif current_piece_name == self.set_of_pieces[4]:
            pawn = Pawn(self.screen, "Black", "BlackPawn", (y, x))
            pawn_position = pawn.get_position()
            if pawn_position[0] != 1:
                pawn.set_starting(False)
            populate_tile = pawn    
        elif current_piece_name == self.set_of_pieces[5]:
            rook = Rook(self.screen, "Black", "BlackRook", (y, x))
            populate_tile = rook
            
        # Now the white pieces get checked    
        elif current_piece_name == self.set_of_pieces[6]:
            king = King(self.screen, "White", "WhiteKing", (y, x))
            populate_tile = king
            self.white_king = king
        elif current_piece_name == self.set_of_pieces[7]:
            queen = Queen(self.screen, "White", "WhiteQueen", (y, x))
            populate_tile = queen
        elif current_piece_name == self.set_of_pieces[8]:
            bishop = Bishop(self.screen, "White", "WhiteBishop", (y, x))
            populate_tile = bishop
        elif current_piece_name == self.set_of_pieces[9]:
            knight = Knight(self.screen, "White", "WhiteKnight",(y, x))
            populate_tile = knight
        elif current_piece_name == self.set_of_pieces[10]:
            pawn = Pawn(self.screen, "White", "WhitePawn", (y, x))
            pawn_position = pawn.get_position()
            if pawn_position[0] != 6:
                pawn.set_starting(False)
            populate_tile = pawn  
        elif current_piece_name == self.set_of_pieces[11]:
            rook = Rook(self.screen, "White", "WhiteRook", (y, x))
            populate_tile = rook
        else:
            print("No piece could be made. This is not suppose to happen")
        
        
        row[x] = populate_tile
        
        
    def convert_FEN(self, FEN):
        """Convert FEN string into proper peice placement on the board"""
        #Lowercase letters describe the black pieces, Uppercase for White. Just like in PGN,
        #"p" stands for pawn, "r" for rook, "n" for knight, "b" for bishop, "q" for queen, 
        #and "k" for king.    
        #Empty squares are denoted by numbers from one to eight, 
        #depending on how many empty squares are between two pieces.
        List_pieces_board_position = []
        current_matrix_coord = [0,0]
        List_of_symbols = ['k','q','b','n','p','r','K','Q','R','B','N','P']
        
        for char in FEN:
            if char == " ":
                break
            
            if char in List_of_symbols:
                List_pieces_board_position.append((char,current_matrix_coord[0],
                                                     current_matrix_coord[1]))
                                                     
                current_matrix_coord[1] = current_matrix_coord[1] + 1 
                
            elif ord(char) == ord("/"):
                current_matrix_coord[0] = current_matrix_coord[0] + 1
                current_matrix_coord[1] = 0
                
             
            else:
                current_matrix_coord[1] += int(char)
               
            
        return List_pieces_board_position
    
                
    def intialize_board_position(self, FEN):
        placement  = self.convert_FEN(FEN)
        for place in placement:
           current_piece_name = self.name_dict[place[0]]
           piece_info = (current_piece_name, place[1], place[2])
           self.create_piece_add_to_board(*piece_info)  
           
        turn_index = FEN.index(" ") + 1
        
        self.set_turn(FEN[turn_index])
        
        index = turn_index + 2
        
        white_rook_squares = [self.access_tile(7,0) , self.access_tile(7,7)]
        black_rook_squares = [self.access_tile(0,0) , self.access_tile(0,7)]
           
        while (index < len(FEN) and FEN[index] != " "):
            char = FEN[index]
            if char == "K": #Kingside castle for white
                self.get_white_king().set_moved(False)
                white_rook_squares[1].set_moved(False)
            elif char == "Q": #queenside castle for white
                  self.get_white_king().set_moved(False)
                  white_rook_squares[0].set_moved(False)
            elif char == "k": #Kingside castle for black
                 self.get_black_king().set_moved(False)
                 black_rook_squares[1].set_moved(False) 
            elif char == "q": #queenside castle for black
                self.get_black_king().set_moved(False)
                black_rook_squares[0].set_moved(False) 
           
            index = index + 1
         
        ##Set up en passant    
        index = index + 1 
        if (index < len(FEN) and FEN[index] in self.classical_dict):
            if self.get_turn() == "Black": #White jusrt moved and we are getting white pawn position
                new_location  = ((( 8 - int(FEN[index + 1]))-1), self.classical_dict[FEN[index]])
            else:
                new_location  = ((( 8 - int(FEN[index + 1]))+1), self.classical_dict[FEN[index]])
            
            #See if en_passant is possible for White
            if self.get_turn() == "White":#Black just moved two squares
                #Check to left of black piece. Right of white piece
               if (new_location[1] > 0 and
                 self.board[new_location[0]] [new_location[1]-1] !=0  and 
                  self.board[new_location[0]] [new_location[1]-1].name == "WhitePawn"):  
                      self.board[new_location[0]] [new_location[1]-1].set_en_passant_right(True)
               
               #Check to right of black piece. left of white piece 
               if (new_location[1] < 7 and 
                   self.board[new_location[0]] [new_location[1]+1] !=0  and 
                  self.board[new_location[0]] [new_location[1]+1].name == "WhitePawn"):
                   self.board[new_location[0]] [new_location[1]+1].set_en_passant_left(True)
            
            #Check en passant for black         
            elif  self.get_turn() == "Black": #White just moved two squares
                #Check to left of white piece. Right of black piece
               if (new_location[1] > 0 and
                   self.board[new_location[0]] [new_location[1]-1] !=0  and 
                  self.board[new_location[0]] [new_location[1]-1].name == "BlackPawn"):  
                      self.board[new_location[0]] [new_location[1]-1].set_en_passant_right(True)
               
               #Check to right of white piece. left of black piece 
               if (new_location[1] < 7 and
                   self.board[new_location[0]] [new_location[1]+1] !=0  and 
                  self.board[new_location[0]] [new_location[1]+1].name == "BlackPawn"):
                   self.board[new_location[0]] [new_location[1]+1].set_en_passant_left(True)
            else:
                 pass
    
    def create_new_FEN(self):
        kings = ["BlackKing", "WhiteKing"]
        rooks =  ["BlackRook", "WhiteRook"]
        
        castling = []
        en_passant_square =[]
        space_count = 0
        new_FEN=""
        for i in range(0,8):
            space_count = 0     
            for j in range(0,8):
                current_tile = self.access_tile(i,j)
                if current_tile != 0:#There is a piece there
                    if space_count != 0:
                        new_FEN += (str(space_count) + self.reverse_name_dict[current_tile.name])
                    else:
                        new_FEN += self.reverse_name_dict[current_tile.name]
                    space_count = 0
                    
                    
                    #Logic for tracking castling right
                    if (current_tile.name in rooks and 
                       not(current_tile.has_moved())):
                            if (current_tile.color == "White" and
                                not(self.white_king.has_moved())):
                                    if  current_tile.board_coord[1] == 7:
                                        castling.append('K')
                                    else:
                                        castling.append('Q')
                            elif (current_tile.color == "Black" and
                                not(self.black_king.has_moved())):
                                     if  current_tile.board_coord[1]  == 7:
                                        castling.append('k')
                                     else:
                                        castling.append('q')
                    
                    if (current_tile.name == "WhitePawn" or 
                        current_tile.name == "BlackPawn"):
                        y  = current_tile.board_coord[0]
                        x = current_tile.board_coord[1]
                        
                        if current_tile.en_passantL and current_tile.color == "White":
                           en_passant_square.append(( y - 1 , x-1))
                        elif current_tile.en_passantR and current_tile.color == "White":  
                          en_passant_square.append( ( y -1, x +1))
                        elif current_tile.en_passantL and current_tile.color == "Black":
                            en_passant_square.append((y + 1 , x-1))
                        elif current_tile.en_passantR and current_tile.color == "Black":
                            en_passant_square.append((y +1 , x +1))
                     
                            
                
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
                         
        new_FEN += " "  
        if self.get_turn() == "White":
            new_FEN += "w"
        else:
            new_FEN += "b"
        new_FEN += " "       
        for char in castling:
            new_FEN += char
        new_FEN += " "
        for en_passant in en_passant_square:
             
             new_FEN  = (new_FEN + 
                         str(self.reverse_classical_dict.get(en_passant[1])) +
                         str( (8 - en_passant[0])))
        new_FEN  = new_FEN.strip()          
       # print("\n" + "New FEN is: ")
        #print(new_FEN)                 
        return new_FEN
        
    def reset_board_position(self, FEN):
         for i in range(0,8):
            for j in range(0,8):
                self.set_tile(i, j, 0)
         self.intialize_board_position(FEN)   
         
    
    def reset_board(self):
        for i in range(0,8):
            for j in range(0,8):
                self.set_tile(i, j, 0)
                
                
                