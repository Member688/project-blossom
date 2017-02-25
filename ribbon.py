import pygame


class Ribbon(object):
    left = 0
    top = 0
    rect_width = 0
    rect_height = 0
    full_scale = 0
    font_name = ''
    font_size = 0

    rect_stroke_width = 2
    current_value = 0

    segment_scale_real= 0
    number_of_major_segments = 8        #TODO: Set method.
    colour = (153, 255, 153)            #TODO: Set method.
    segment_large_x = 0
    segment_small_x = 0
    min_value = 0
    max_value = 0
    rectangle = []
    lines = []
    labels = []
    lables_pos = []
    font = None

    def __init__(self, left, top, width, height, scale, font_name, font_size):
        self.left = left
        self.top = top

        self.rect_width = width
        self.rect_height = height

        self.full_scale = scale

        self.segment_start_left = self.left + self.rect_width
        self.segment_large_end_left = self.segment_start_left - self.rect_width // 4
        self.segment_small_end_left = self.segment_start_left - self.rect_width // 8

        self.segment_scale_real = self.full_scale / self.number_of_major_segments
        self.segment_scale_pixel = self.rect_height // self.number_of_major_segments

        self.font_name = font_name
        self.font_size = font_size

        self.font = pygame.font.SysFont(self.font_name, self.font_size)

    def update_current_value(self, current_value):
        self.current_value = current_value
        self.min_value = self.current_value - self.full_scale / 2
        self.max_value = self.current_value + self.full_scale / 2

    def calculate_slider(self):
        # Create Rectangle
        self.rectangle = [self.left, self.top, self.rect_width, self.rect_height]

        # Create 2*2*n array of lines. self.lines[ Line Index, Start/End Pos, x/y Value ]
        self.lines = [[[0 for _ in range(2)] for _ in range(2)] for _ in range(self.number_of_major_segments * 2)]

        # Create arrays for label text and position of each label
        self.labels = [0 for _ in range(self.number_of_major_segments)]
        self.lables_pos = [[0 for _ in range(2)] for _ in range(self.number_of_major_segments)]

        # Calculate size of gap between the minimum value on the ribbon and the bottom segment
        btm_seg_above_min_real = self.segment_scale_real - (self.min_value % self.segment_scale_real)

        # Calculate the value of the bottom segment
        btm_seg_value_real = (self.min_value // self.segment_scale_real + 1) * self.segment_scale_real

        # Calculate the distance between minimum value and the bottom segment in pixels
        btm_seg_above_min_pixel = int(float(btm_seg_above_min_real) / float(self.full_scale) * float(self.rect_height))
        btm_seg_above_min_pixel += self.rect_stroke_width

        # All segments start at the same point.
        left_start = self.segment_start_left

        for i in range(self.number_of_major_segments):

            top_start = self.top + self.rect_height - btm_seg_above_min_pixel - self.segment_scale_pixel * i
            top_end = top_start

            left_end = self.segment_large_end_left

            self.lines[2*i][0] = [left_start, top_start]
            self.lines[2*i][1] = [left_end, top_end]

            self.labels[i] = str(int(btm_seg_value_real + i * self.segment_scale_real))
            self.lables_pos[i] = [self.left + self.font_size / 2, top_end - self.font_size // 2]

            # Draw Midpoint lines either above or below the segment lines. This decision depends on the distance from
            # the minimum value to the first segment.
            if btm_seg_above_min_real >= (self.segment_scale_real/ 2):
                top_start += self.segment_scale_pixel / 2
            else:
                top_start -= self.segment_scale_pixel / 2

            top_end = top_start
            left_end = self.segment_small_end_left
            self.lines[2*i + 1][0] = [left_start, top_start]
            self.lines[2*i + 1][1] = [left_end, top_end]

    def draw(self, screen):

        self.calculate_slider()

        # Draw Rectangle
        pygame.draw.rect(screen, self.colour, self.rectangle, self.rect_stroke_width)

        temp_colour = self.colour

        for line in self.lines:
            pygame.draw.line(screen, temp_colour, line[0], line[1], self.rect_stroke_width)

        for i, label_text in enumerate(self.labels):
            # Draw Segment Label
            label = self.font.render(label_text, 1, temp_colour)
            screen.blit(label, (self.lables_pos[i][0], self.lables_pos[i][1]))

        # Show current value in Red. TODO: Make this configurable.
        temp_colour = (255, 0, 0)

        label = self.font.render('{:06.2f}'.format(self.current_value), 1, temp_colour)
        screen.blit(label, (self.left + self.rect_width + self.font_size, self.top + self.rect_height // 2 - self.font_size // 2))

        left_start = self.segment_start_left + self.rect_stroke_width // 2
        top_start = self.top + self.rect_height // 2
        left_end = self.left + self.rect_width * 9 // 8
        top_end = top_start

        line_start = [left_start, top_start]
        line_end = [left_end, top_end]
        pygame.draw.line(screen, temp_colour, line_start, line_end, self.rect_stroke_width)

#        label = FONT.render('{:06.2f}'.format(self.min_value), 1, temp_colour)
#        screen.blit(label, (self.pos_x+self.rect_width + FONT_SIZE, self.top + self.rect_height - FONT_SIZE // 2))

#        label = FONT.render('{:06.2f}'.format(self.max_value), 1, temp_colour)
#        screen.blit(label, (self.pos_x+self.rect_width + FONT_SIZE, self.top - FONT_SIZE // 2))
