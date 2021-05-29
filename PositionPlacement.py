
from BoardSettings import BoardSetting

board_setting = BoardSetting()

def matrix_to_board(name,x,y):
    """x and y are integers from 1 to 8. Where the chess board is a matrix and
    (1,1) is the a8 square if perspective is white (which is the assumed one)"""
    
    initialX = (board_setting.tile_width + board_setting.tile_width/2)
    initialY = (board_setting.tile_width + board_setting.tile_width/2)
    
    x = initialX + (x - 1)*board_setting.tile_width
    y = initialY + (y - 1)*board_setting.tile_width
    screen_coordinate = (name,x,y)
    return screen_coordinate
   
    

def convert_FEN(FEN):
    """Convert FEN string into proper peice placement on the board"""
    #Lowercase letters describe the black pieces, Uppercase for White. Just like in PGN,
    #"p" stands for pawn, "r" for rook, "n" for knight, "b" for bishop, "q" for queen, 
    #and "k" for king.    
    #Empty squares are denoted by numbers from one to eight, 
    #depending on how many empty squares are between two pieces.
    List_pieces_screen_position = []
    current_matrix_coord = [1,1]
    List_of_symbols = ['k','q','b','n','p','r','K','Q','R','B','N','P']
    
    for char in FEN:
       
        if char in List_of_symbols:
            List_pieces_screen_position.append(
                                                 matrix_to_board(
                                                 char,current_matrix_coord[1],
                                                 current_matrix_coord[0])
                                                 )
            current_matrix_coord[1] = current_matrix_coord[1] + 1 
            
        elif ord(char) == ord("/"):
            current_matrix_coord[0] = current_matrix_coord[0] + 1
            current_matrix_coord[1] = 1
            
         
        else:
            current_matrix_coord[1] += int(char)
        
    return List_pieces_screen_position