import pygame
import time
import math

from pygame.locals import *

WINSIZE = [640, 480]
MAXFPS = 60.0
TARGETCYCLETIME_US = 1.0 / MAXFPS * 1000000.0
lime_green = (153, 255, 153 )
red = (255, 0, 0)
COUNTER = 0.0


class Ribbon(object):
    pos_x = 0
    pos_y = 0
    rect_width = 0
    rect_height = 0
    rect_stroke_width = 2
    current_value = 0
    full_scale = 0
    major_segment_scale = 0
    number_of_major_segments = 8
    colour = lime_green
    segment_large_x = 0
    segment_small_x = 0
    bottom_value = 0
    top_value = 0
    lines = []

    def __init__(self, pos_x, pos_y, width, height, scale):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect_width = width
        self.rect_height = height
        self.full_scale = scale
        self.colour = lime_green

        self.segment_x_start = self.pos_x + self.rect_width
        self.segment_large_x_end = self.segment_x_start - self.rect_width/2
        self.segment_small_x_end = self.segment_x_start - self.rect_width/4

        self.major_segment_scale = self.full_scale / self.number_of_major_segments
        self.major_segment_pixel = self.rect_height / self.number_of_major_segments

    def update_current_value(self, current_value):
        self.current_value = current_value
        self.bottom_value = self.current_value - self.full_scale / 2
        self.top_value = self.current_value + self.full_scale / 2

    def calculate_slider(self):
        return 0

    def draw(self, screen):
        rectangle = [self.pos_x, self.pos_y, self.rect_width, self.rect_height]
        pygame.draw.rect(screen, lime_green, rectangle, self.rect_stroke_width)

        offset = self.current_value % self.major_segment_scale
        above_center = int(float(offset) / float(self.full_scale) * float(self.rect_height))
        startpos_x = self.segment_x_start

        for x in range(self.number_of_major_segments):

            factor = 2 * (x % 2) - 1
            distance_index = math.floor(( x + 1) / 2)

            startpos_y = self.pos_y + self.rect_height / 2 - above_center - self.major_segment_pixel * factor * distance_index
            endpos_y = startpos_y

            if math.ceil((float(x) + 1)/2) % 2 == 0:
                endpos_x = self.segment_large_x_end
            else:
                endpos_x = self.segment_small_x_end

            line_start = [startpos_x, startpos_y]
            line_end = [endpos_x, endpos_y]
            tempcolor = lime_green
            if x == 0:
                tempcolor = red
            pygame.draw.line(screen, tempcolor, line_start, line_end, self.rect_stroke_width)


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

    global COUNTER

    done = 0
    while not done:
        cycle_time_us = time.time() * 1000000.0
        delta_time_us = (cycle_time_us - cycle_time_us_last_update)

        if delta_time_us >= TARGETCYCLETIME_US:
            COUNTER += float(TARGETCYCLETIME_US)
            for e in pygame.event.get():
                if e.type == QUIT:
                    done = 1
                    break
            cycle_time_us_last_update = cycle_time_us
            print(1000000.0 / delta_time_us)
            screen.fill(black)

            speed_ribbon.update_current_value(50 + 50 * math.sin(COUNTER / 1000000.0 / 5.0))
            speed_ribbon.draw(screen)
            pygame.display.update()
        else:
            wait_time_us = TARGETCYCLETIME_US - delta_time_us
            wait_time_s = wait_time_us / 1000000.0
#            print('Sleeping: %12f s' % wait_time_s)
            time.sleep(wait_time_s)
    pygame.quit()


if __name__ == '__main__':
    main()

