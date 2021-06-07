   
def check_allowed_moved(self,board,list_of_moves):
        x = None
        y = None
        attack_origin = None
        attack_origin2 = None
        king_type = None
        legal_moves = []

        
        if board.white_turn:
               y = board.get_white_king().board_coord[0]
               x = board.get_white_king().board_coord[1]
               color = "White"
              
               king_type = "WhiteKing" 
               bool_king_moves = (board.get_white_king().
                                  check_legal_moves(board) != [])
               
        elif board.black_turn:
               y = board.get_black_king().board_coord[0]
               x = board.get_black_king().board_coord[1]
               color = "Black"
              
               king_type = "BlackKing"
               bool_king_moves = (board.get_black_king().
                                  check_legal_moves(board) != [])
        else:
            pass
        
        #Check King safety
        attack_origin = Piece_Safety.check_piece_safety(y,x,color,board)     
        
       
        if len(attack_origin) ==  0 : #King has no direct threat
            #Determine if piece can move
             place_holder = board.access_tile(*self.board_coord)
             board.set_tile(*self.board_coord, 0)
             attack_origin2 = Piece_Safety.check_piece_safety(y,x,color,board)
             if len(attack_origin2) > 0:#No moves can be made
                 board.set_tile(*self.board_coord, place_holder)
                 return []
             else:#Piece can move freely
                 board.set_tile(*self.board_coord, place_holder)
                 return list_of_moves
             
        else: #len(attack_origin) >  0 
           
           
           if len(attack_origin) >= 2:
               
               if(board.access_tile(*self.board_coord).name != king_type):
                   return []
               else:
                   return list_of_moves
               
           else:#only 1 attacker
               attack = attack_origin[0] #by now we know len(attack_origin) == 1
              
               attack_color = board.access_tile(*attack).get_color()
                 
               #Check to see if attacker may be block 
               place_holder = board.access_tile(*self.board_coord)
               board.set_tile(*self.board_coord, 0)
               attack_origin2 = Piece_Safety.check_piece_safety(y,x,color,board)
               
               if len(attack_origin2) > len(attack_origin):
                   #It is not allowed to move
                   board.set_tile(*self.board_coord, place_holder)
                   return []
               else:
                    board.set_tile(*self.board_coord, place_holder)
                    #Check to see if attacker may be captured 
                    if attack in list_of_moves:
                        legal_moves.append(attack)
              
                    #Check if the attacker may be blocked
              
                    #Now we know u can make a move
                    #To block, check the intersection between the 
                    #List of  moves that can be made by the attacking piece
                    #The list of moves by the selected piece
                    #Check king safety again, if no attack pieces, then it was a legal move
                    #other wise continue
                    attacking_moves = board.access_tile(*attack).check_legal_moves(board)
                    #The above line call check legal moves, this is a problem
                    #Further code refactoring is need
                    
                    #Remaining idea is to get the location where the 
                    #piece attack and see if we can block that
                    
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
              