import math

from BoardSettings import BoardSetting

board_setting = BoardSetting()

def matrix_to_screen_name(name,x,y):
    """x and y are integers from 0 to 7. Where the chess board is a matrix and
    (0,0) is the a8 square if perspective is white (which is the assumed one)"""
    
    initialX = (board_setting.tile_width + board_setting.tile_width/2)
    initialY = (board_setting.tile_width + board_setting.tile_width/2)
    
    x = initialX + (x)*board_setting.tile_width #Note I thought X starts at 1 when it shouldnt
    y = initialY + (y)*board_setting.tile_width #Note I thought Y starts at 1 when it shouldnt
    screen_coordinate = (name,x,y)
    return screen_coordinate

def matrix_to_screen(y,x):
    """x and y are integers from 0 to 7. Where the chess board is a matrix and
    (0,0) is the a8 square if perspective is white (which is the assumed one)"""
    
    initialX = (board_setting.tile_width + board_setting.tile_width/2)
    initialY = (board_setting.tile_width + board_setting.tile_width/2)
    
    x = initialX + (x)*board_setting.tile_width
    y = initialY + (y)*board_setting.tile_width
    screen_coordinate = (x,y)
    return screen_coordinate


def screen_to_board(x,y): #Necessary for dealing with the double array which is eight by eight
                            # So 0 to 7
    """IMPORTANT give argument as (x,y)!! 
    x and y are integers from 0 to 7. Where the chess board is a matrix and
    (0,0) is the a8 square if perspective is white (which is the assumed one)"""
    
    initialX = (board_setting.tile_width + board_setting.tile_width/2)
    initialY = (board_setting.tile_width + board_setting.tile_width/2)
    
    x = int((x - initialX)/board_setting.tile_width)
    y = int( (y - initialY)/board_setting.tile_width)
    
    
    # Note that you must interchange the x and y position in the return statement
    # This is because screen coordonites work as (x,y) but board/matrix coordinates u will specify
    # the row then the column, ie (y,x)
    
    board_coord = (y,x)
    return board_coord
    
def mouse_to_board(x,y): #Necessary for dealing with the double array which is eight by eight
                            # So 0 to 7
    """IMPORTANT give argument as (x,y)!! 
    x and y are integers from 0 to 7. Where the chess board is a matrix and
    (0,0) is the a8 square if perspective is white (which is the assumed one)"""
  
    #Do modular arithmetic with mod 60  
    boardX = math.floor(x/board_setting.tile_width)
    boardX -= 1
    
    
    boardY = math.floor(y/board_setting.tile_width)
    boardY -= 1
    
    # Note that you must interchange the x and y position in the return statement
    # This is because screen coordonites work as (x,y) but board/matrix coordinates u will specify
    # the row then the column, ie (y,x)
    
    board_coord = (boardY,boardX)
    return board_coord              
              



