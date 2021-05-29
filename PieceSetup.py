"""Class for the Visual representation of the pieces"""

import pygame

from BoardSettings import BoardSetting

import PositionPlacement

##from BoardSetup import BoardSetup

board_settings = BoardSetting()

class PieceSetup():
    
    def __init__(self,screen):
        self.screen =  screen
        
        self.set_of_pieces = ["BlackKing","BlackQueen","BlackBishop",
                              "BlackKnight","BlackPawn","BlackRook",
                              "WhiteKing","WhiteQueen","WhiteBishop",
                              "WhiteKnight","WhitePawn","WhiteRook"]
        
        self.name_dict = {'k':0,'q':1,"b":2,
                              'n':3,'p':4,'r':5,
                              'K':6,'Q':7,'B':8,
                             'N': 9,'P':10,'R':11}
        
        self.image_files = ["C:/Users/Christopher/Documents/Chess pieces"+
                           "/"+name+".bmp" for name in self.set_of_pieces]
       
        
        #self.images =  pygame.image.load(self.image_file + "/BlackKing.bmp")
        #self.image = pygame.transform.scale(self.image, (board_settings.tile_width - 5,
                                                       #  board_settings.tile_width - 5))
        
       # self.rect = self.image.get_rect()
        
        # Start each new piece at the bottom center of the screen.
        #self.rect.center = (90,90)

    def get_images(self, image_files):
        """Get a SET of images of the pieces in the same order as they appear
        in set_of_pieces"""
        images = []
        for image_file in image_files:
            images.append(pygame.image.load(image_file))
        return images
    
    def scale_images(self, images):
        small_images = []
        for image in images:
            small_images.append(pygame.transform.scale(image, (board_settings.tile_width - 15,
                                                  board_settings.tile_width - 15)))
        return small_images    
    
    def blitme(self,FEN):
        """Draw the piece at its described location by the FEN."""
        list_images  = self.get_images(self.image_files)
        images  = self.scale_images(list_images)
        placement  = PositionPlacement.convert_FEN(FEN)
       
        for place in placement:
            current_piece = images[self.name_dict[place[0]]]
            rect = current_piece.get_rect()
            rect.center = (place[1],place[2])
            self.screen.blit(current_piece, rect)   


#Testing methods
#listthing = PositionPlacement.convert_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
#print(listthing)                                        
                                          
                                          
#Array = [ [0] * 8 ] * 8] # with each element value as 0                 
                                          
                                          
                                          
                                          
                                          
                                          
                                          
                                          
                                          
                                          
                                          
                                          
                                          
                                          