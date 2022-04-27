import pygame as pg

class Pane(object):
    def __init__(self, x, y, colour, text=''):
        self.FONT = pg.font.Font(None, 32)
        self.x = x
        self.y = y
        self.color = pg.Color(colour)
        self.txt_surface = self.FONT.render(text, True, self.color)

    def update(self, newText):
        # Update the text
        self.txt_surface = self.FONT.render(newText, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.x+5, self.y+5))