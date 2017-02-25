import pygame
import time
import math
import ribbon

from pygame.locals import *

WINSIZE = [640, 480]
MAXFPS = 60.0
TARGETCYCLETIME_US = 1.0 / MAXFPS * 1000000.0
lime_green = (153, 255, 153)
red = (255, 0, 0)
COUNTER = 0.0

FONT_SIZE = 14


def main():
    black = 0, 0, 0
    cycle_time_us_last_update = 0.0

    # initialize and prepare screen
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('First Project')
    screen.fill(black)

    font_name = "monospace"

    speed_ribbon = ribbon.Ribbon(100, 30, 50, 300, 160, font_name, FONT_SIZE)
    another_ribbon = ribbon.Ribbon(400, 60, 75, 150, 160, font_name, FONT_SIZE - 4)

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

            # Update Ribbon Current Value
            speed_ribbon.update_current_value(100 * math.sin(COUNTER / 1000000.0 / 5.0))
            another_ribbon.update_current_value(80 + 40 * math.sin(COUNTER / 1000000.0 / 2.0))

            # Start Drawing
            # Clear Screen
            screen.fill(black)
            # Draw Components
            speed_ribbon.draw(screen)
            another_ribbon.draw(screen)

            # Call Screen Update
            pygame.display.update()
        else:
            wait_time_us = TARGETCYCLETIME_US - delta_time_us
            wait_time_s = wait_time_us / 1000000.0
            time.sleep(wait_time_s)
    pygame.quit()

if __name__ == '__main__':
    main()
