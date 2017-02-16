import pygame
import time
import math

from pygame.locals import *

WINSIZE = [640, 480]
MAXFPS = 60.0
TARGETCYCLETIME_US = 1.0 / MAXFPS * 1000000.0
lime_green = (153, 255, 153 )


class Ribbon(object):
    pos_y = 0
    pos_y = 0
    rect_width = 0
    rect_height = 0
    rect_stroke_width = 2
    current_value = 0
    full_scale = 0
    major_segment_scale = 0
    number_of_major_segments = 6
    colour = lime_green


    def __init__(self, pos_x, pos_y, width, height, scale):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect_width = width
        self.rect_height = height
        self.full_scale = scale
        self.colour = lime_green

        major_segment_scale = self.full_scale / self.number_of_major_segments


    def update_current_value(self, current_value):
        self.current_value = current_value


    def calculate_slider(self):
        return 0


    def draw(self,screen):
        rectangle = [self.pos_x, self.pos_y, self.rect_width, self.rect_height]
        pygame.draw.rect(screen, lime_green, rectangle, self.rect_stroke_width)

        currentvalue_ratio = int(float(self.current_value) / float(self.full_scale) * float(self.rect_height))

        startpos_x = self.pos_x + self.rect_width
        startpos_y = self.pos_y + self.rect_height - currentvalue_ratio

        endpos_x = startpos_x - self.rect_width/2
        endpos_y = startpos_y

        startpos = [startpos_x, startpos_y]
        endpos = [endpos_x, endpos_y]
        pygame.draw.line(screen, lime_green, startpos, endpos, self.rect_stroke_width)


def main():
    white = 255, 255, 255
    black = 0, 0, 0
    cycle_time_us_last_update = 0.0

    # initialize and prepare screen
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('First Project')
    screen.fill(black)

    speed_ribbon = Ribbon(200, 30, 50, 300, 150)

    done = 0
    while not done:
        cycle_time_us = time.time() * 1000000.0
        delta_time_us = (cycle_time_us - cycle_time_us_last_update)

        if delta_time_us >= TARGETCYCLETIME_US:
            for e in pygame.event.get():
                if e.type == QUIT:
                    done = 1
                    break
            cycle_time_us_last_update = cycle_time_us
            print(1000000.0 / delta_time_us)
            x = 300 + 50.0 * math.cos(cycle_time_us / 1000000.0 / 5.0) + 20 * math.cos(cycle_time_us / 1000000.0 / 0.5)
            y = 300 + 50.0 * math.sin(cycle_time_us / 1000000.0 / 5.0) + 20 * math.sin(cycle_time_us / 1000000.0 / 0.5)
            pos = [int(x), int(y)]
            screen.fill(black)
            screen.set_at(pos, white)

            speed_ribbon.update_current_value(50 + 50 * math.sin(cycle_time_us / 1000000.0 / 5.0))
            speed_ribbon.draw(screen)
            pygame.display.update()
        else:
            wait_time_us = TARGETCYCLETIME_US - delta_time_us
            wait_time_s = wait_time_us / 1000000.0
            print('Sleeping: %12f s' % wait_time_s)
            time.sleep(wait_time_s)
    pygame.quit()


if __name__ == '__main__':
    main()

