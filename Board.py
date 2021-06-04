import pygame

from BoardSettings import BoardSetting
import PieceSetup


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
        
        self.moving_piece = None
    
    def change_piece_location(self,new_location):#New location (y,x) aka (i,j)
        old_location =  self.moving_piece.get_position() # Of piece that just moved    
        old_location_capture = None #Used to hold to captured pieces if needed 
                                    #to be put back
        en_passant_capture = False
        #Logic for allowing the capture of pieces
        if self.access_tile(*new_location) != 0: # Not an empty square
                # A capture has just occured!
                #Hold on to captured piece in case move was illegal
                old_location_capture = self.access_tile(*new_location)
                #Remove the piece
                self.board[new_location[0]] [new_location[1]] = 0 #remove the piece
        #The following is the logic which enables en passant catpture to occur        
        elif (self.access_tile(*new_location) == 0 and
        (self.moving_piece.name =="BlackPawn" or self.moving_piece.name == "WhitePawn")
        and (old_location[0] != new_location[0] and old_location[1] != new_location[1])):
            #En passant capture has just occured.
                    #remove the piece
                    print("EN PASSANT")
                    en_passant_capture = True
                    old_location_capture = self.access_tile(old_location[0], 
                                                            new_location[1])
                    
                    self.board[old_location[0]] [new_location[1]] = 0 
            
        
         
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
                    
                setup = PieceSetup.PieceSetup(self.screen)
                piece_name = setup.name_dict[promote]
                #Needs to have the extra 0 for padding because of the way the 
                #function was written
                location = (0,self.moving_piece.location[0],self.moving_piece.location[1])
                
                setup.create_piece_add_to_board(piece_name,location, self)
                self.change_moving_piece(self.access_tile(old_location[0],
                                                          old_location[1]))
        
        #update the board and moving piece position    
        self.board[old_location[0]][old_location[1]] = 0
        self.board[new_location[0]] [new_location[1]] = self.moving_piece
        self.moving_piece.update_position(new_location[0], new_location[1])
        self.moving_piece = None
        
        self.check_king_safety()
                
        if self.Black_in_check and not(self.White_in_check) and self.white_turn:
            return True
        elif (self.White_in_check and self.white_turn) or (self.Black_in_check 
                                                          and self.black_turn):
            #Undo the move
        
            if(old_location_capture == None):
                self.set_tile(old_location[0], old_location[1], 
                              self.access_tile(*new_location))
                self.access_tile(*old_location).update_position(*old_location)
                self.set_tile(*new_location, 0)
                
            elif old_location_capture != None and not(en_passant_capture): 
                #it was a normal capture
                self.set_tile(old_location[0], old_location[1], 
                              self.access_tile(*new_location))
                self.access_tile(*old_location).update_position(*old_location)
                self.set_tile(*new_location, old_location_capture)
                self.access_tile(*new_location).update_position(*new_location)
                
            elif old_location_capture != None and en_passant_capture:    
                #You captured en passant
                self.set_tile(old_location[0], old_location[1], 
                              self.access_tile(*new_location))
                self.access_tile(*old_location).update_position(*old_location)
                self.set_tile(*new_location, 0)
                self.set_tile(old_location[0],new_location[1], old_location_capture)
                self.access_tile(old_location[0],new_location[1]).update_position(
                    old_location[0],new_location[1])    
                    
                
            print("Not a valid move \n")
            return False
        
        elif self.White_in_check and not(self.Black_in_check) and self.black_turn:
            return True

        else:
            return True
        
                   
    def check_king_safety(self):
        print("Checking king safety")
        y = self.black_king.board_coord[0]
        x = self.black_king.board_coord[1]
        black_threat = self.black_king.check_k(y,x) #Check black king safety
        
        print("Threat to black is: ")
        print(black_threat)
        
        y = self.white_king.board_coord[0]
        x = self.white_king.board_coord[1]
        white_threat = self.white_king.check_k(y,x) #Check white king safety
        
        if len(black_threat) != 0:
            self.Black_in_check = True
        else:
             self.Black_in_check = False
            
        if len(white_threat) != 0:
            self.White_in_check = True   
        else:
             self.white_in_check = False    
    
    
    def is_moving_piece(self):
        """Returns a boolean letting us know is a piece is trying to move"""
        if self.moving_piece != None:
            return True
        else:
            return False
        
    def change_moving_piece(self,piece):
        self.moving_piece = piece
    
    def access_tile(self,y,x):
         """Returns what is store at the give position on the board input as (y,x)"""
         return self.board[y][x]
     
    def set_tile(self,y,x,value):
        self.board[y][x] = value
    
    def access_row(self,y):
        return self.board[y]
         
    
    def get_turn(self):
        if self.white_turn:
            return "White"
        elif self.black_turn:
            return "Black"
        else:
            return None
        
            
    def set_game_over(self):
        self.white_turn = False
        self.black_turn = False
        self.game_over = True
        print("The game is finished")
    
    
    def update_turn(self):
        if self.get_turn() == "White":
             self.white_turn = False
             self.black_turn = True
             
        elif self.get_turn() == "Black":
             self.white_turn = True
             self.black_turn = False
        else:
            self.game_over()
            
    def make_tiles(self):
            """Creates the tiles of the chess board from the view of given perspective"""
            # Double for loop to create the square on the board
            # i controls the row and j controls the column
            # When i and j are even the square is white
            # Note that tile_width = tile_height
            for i in range(0,8):
                    for j in range(0,8):
                        if (i+j)%2 == 0:
                            pygame.draw.rect(self.screen, 
                                             self.setting.w_tile_color,
                                             pygame.Rect((self.setting.tile_width*(j+1), 
                                                          self.setting.tile_width*(i+1)),
                                                         (self.setting.tile_width, 
                                                         self.setting.tile_height)))
                            
                          
                        else:
                             pygame.draw.rect(self.screen, self.setting.b_tile_color,
                                              pygame.Rect((self.setting.tile_width*(j+1), 
                                                           self.setting.tile_width*(i+1)), 
                                                          (self.setting.tile_width, 
                                                          self.setting.tile_height)))
    
    
    def update_board_visuals(self):
        """Idea is to use this to update the screen once the game has already started 
        and not to generate new FEN which consequently generates new pieces"""
        self.screen.fill(self.setting.backround_color)
        self.make_tiles()
        
        if self.moving_piece != None:
            self.moving_piece.display_legal_moves()
        for i in range(0,8):
            for j in range(0,8):
                if self.access_tile(i,j) != 0:
                    self.access_tile(i,j).blitme()
                    
    def determine_checkmate(self):
        """True for checkmate, False for no chekcmate"""
        
        if self.white_turn and self.White_in_check:
            if self.white_king.check_legal_moves() == []:
                y = self.white_king.board_coord[0]
                x = self.white_king.board_coord[1]
                attack_origin = self.white_king.check_k(y,x)
                
                if len(attack_origin) >= 2:
                    print("White is checkmated")
                    self.set_game_over() 
                    return True
                else:
                    for attack in attack_origin: #attack origin < 2 by this point aka == 1
                        list_at = self.access_tile(*attack).check_k(*attack)            
                        if (len(list_at) == 1 and 
                            self.access_tile(*list_at[0]).name == "WhiteKing"): 
                            print("White is checkmated")
                            self.set_game_over()  
                            return True
                        else:
                            return False
              
        elif self.black_turn and self.Black_in_check:
             
             if self.black_king.check_legal_moves() == []:
                y = self.black_king.board_coord[0]
                x = self.black_king.board_coord[1]
                attack_origin = self.black_king.check_k(y,x)
               
                if len(attack_origin) >= 2:
                    print("Black is checkmated")
                    self.set_game_over() 
                    return True
                else:
                     for attack in attack_origin: #attack origin < 2 by this point aka == 1
                        list_at = self.access_tile(*attack).check_k(*attack) 
                      
                        print(self.access_tile(*list_at[0]).name) 
                           
                        if (len(list_at) == 1 and 
                            self.access_tile(*list_at[0]).name == "BlackKing"): 
                            print("Black is checkmated")
                            self.set_game_over() 
                            return True
                        else:
                            return False
                     
    def reset_board(self):
        for i in range(0,8):
            for j in range(0,8):
                self.set_tile(i, j, 0)
                
                
                