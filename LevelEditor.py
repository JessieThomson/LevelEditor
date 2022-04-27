import pygame, sys, time, random
from pygame.locals import *
import numpy as np


if __name__ == '__main__':
    pygame.init()
    windowSurface = pygame.display.set_mode((500, 400), 0, 32)
    pygame.display.set_caption("Paint")
    # get screen size
    info = pygame.display.Info()
    sw = info.current_w
    sh = info.current_h
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (239, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    box_colour = BLACK
    while True:
        joystick = joysticks[0]
        joystick.init()
        # buttons = joystick.get_numbuttons()
        # print "Number of buttons: {}".format(buttons)
        # for i in range(buttons):
        #     button = joystick.get_button(i)
        #     print "Button {:>2} value: {}".format(i, button)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.JOYBUTTONDOWN:
                if joystick.get_button(0) > 0:
                    print("A Button")
                    box_colour = GREEN
                if joystick.get_button(1) > 0:
                    print("B Button")
                    box_colour = RED
                if joystick.get_button(2) > 0:
                    print("X Button")
                    box_colour = BLUE
                if joystick.get_button(3) > 0:
                    print("Y Button")
                    box_colour = YELLOW

        windowSurface.fill(BLACK)
        pygame.draw.rect(windowSurface, box_colour, [150, 150, 25, 25], 0)
        pygame.time.Clock().tick(20)

        pygame.display.update()
