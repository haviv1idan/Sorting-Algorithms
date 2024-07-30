import ascendingAlgorithms
import descendingAlgorithms
import pygame
import random


pygame.init()


class DrawInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BLUE = 0, 0, 255
    GRAYS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192),
    ]

    FONT = pygame.font.SysFont("comicsans", 30)
    LARGE_FONT = pygame.font.SysFont("comicsans", 40)
    TOP_PAD = 200
    SIDE_PAD = 50

    block_width = 0
    block_height = 0
    lst = []

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.sorting_name = ""
        self.ascending = True

        self.window = pygame.display.set_mode((self.width, self.height))
        self.window.fill(self.WHITE)

        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.block_width = (self.width - self.SIDE_PAD) / len(lst)
        self.block_height = round((self.height - self.TOP_PAD) // (max(lst) - min(lst)))
        print("block width: ", self.block_width)
        print("block height: ", self.block_height)


# Complete
def draw(draw_info: DrawInfo):
    # Clear screen
    draw_info.window.fill(draw_info.WHITE)

    # Draw control options
    controls = draw_info.FONT.render("R - Reset | A - Ascending | D - Descending", True, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 5))

    # Draw sorting options
    sorting = draw_info.FONT.render("B - Bubble | H - Heap | I - Insertion | M - Merge | S - Selection", True, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 35))

    # Draw sort and ascending
    if draw_info.ascending:
        str_ascending = "Ascending"
    else:
        str_ascending = "Descending"

    current = draw_info.FONT.render("current sort: {} Ascending: {} ".format(draw_info.sorting_name, str_ascending), True, draw_info.RED)
    draw_info.window.blit(current, (draw_info.width / 2 - current.get_width() / 2, 65))

    # Draw list
    draw_list(draw_info)

    # Update screen
    pygame.display.update()


def draw_list(draw_info: DrawInfo, color_positions={}):

    # Clear background of list
    clear_list_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD,
                       draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
    pygame.draw.rect(draw_info.window, draw_info.WHITE, clear_list_rect)

    # Start x and y of list rect
    start_x = draw_info.SIDE_PAD // 2
    start_y = draw_info.height - max(draw_info.lst)

    for i, val in enumerate(draw_info.lst):

        start_block_x = start_x + draw_info.block_width * i
        start_block_y = start_y + (max(draw_info.lst) - val * draw_info.block_height)

        color = draw_info.GRAYS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        # screen width = 800
        # screen height = 600
        # pygame.display.rect(window, color, (start_x, start_y, width_of_rect, height_of_rect))
        pygame.draw.rect(draw_info.window, color,
                         (start_block_x, start_block_y, draw_info.block_width, val * draw_info.block_height))

    pygame.display.update()


def generate_new_list(n, min_val, max_val):
    arr = []
    for _ in range(0, n):
        num = random.randint(min_val, max_val)
        arr.append(num)
    return arr


def main():

    clock = pygame.time.Clock()
    run = True
    sorting = False

    n = 50
    min_val = 10
    max_val = 200
    screen_width = 1400
    screen_height = 900

    lst = generate_new_list(n, min_val, max_val)
    draw_info = DrawInfo(screen_width, screen_height, lst)
    draw(draw_info)

    sorting_algorithm = None

    while run:

        clock.tick(60)
        ascending = draw_info.ascending

        # Draw list after sorting
        if draw_info.lst == sorted(draw_info.lst) or draw_info.lst == list(reversed(sorted(draw_info.lst))):
            draw(draw_info)

        if sorting:
            try:
                next(sorting_algorithm)
            except StopIteration:
                print(draw_info.lst)
                sorting = False
                draw_info.sorting_name = ""

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:

                # Reset
                if event.key == pygame.K_r:
                    sorting = False
                    print("r")
                    lst = generate_new_list(n, min_val, max_val)
                    draw_info.set_list(lst)
                    draw(draw_info)

                # Ascending
                elif event.key == pygame.K_a:
                    draw_info.ascending = True
                    draw(draw_info)

                # Descending
                elif event.key == pygame.K_d:
                    draw_info.ascending = False
                    draw(draw_info)

                # Bubble
                elif event.key == pygame.K_b and not sorting:
                    sorting = True
                    draw_info.sorting_name = "bubble sort"
                    if ascending:
                        sorting_algorithm = ascendingAlgorithms.ascending_bubble_sort(draw_info)
                    else:
                        sorting_algorithm = descendingAlgorithms.descending_bubble_sort(draw_info)

                # Heap
                elif event.key == pygame.K_h and not sorting:
                    sorting = True
                    draw_info.sorting_name = "Heap sort"
                    if ascending:
                        sorting_algorithm = ascendingAlgorithms.ascending_heap_sort(draw_info)
                    else:
                        sorting_algorithm = descendingAlgorithms.descending_heap_sort(draw_info)

                # Insertion
                elif event.key == pygame.K_i and not sorting:
                    sorting = True
                    draw_info.sorting_name = "insertion sort"
                    if ascending:
                        sorting_algorithm = ascendingAlgorithms.ascending_insertion_sort(draw_info)
                    else:
                        sorting_algorithm = descendingAlgorithms.descending_insertion_sort(draw_info)

                # Merge
                elif event.key == pygame.K_m and not sorting:
                    sorting = True
                    draw_info.sorting_name = "merge sort"
                    if ascending:
                        sorting_algorithm = ascendingAlgorithms.ascending_mergesort(draw_info, draw_info.lst, len(draw_info.lst) // 2)
                    else:
                        sorting_algorithm = descendingAlgorithms.descending_mergesort(draw_info, draw_info.lst, len(draw_info.lst) // 2)

                # Selection
                elif event.key == pygame.K_s and not sorting:
                    sorting = True
                    draw_info.sorting_name = "selection sort"
                    if ascending:
                        sorting_algorithm = ascendingAlgorithms.ascending_selection_sort(draw_info)
                    else:
                        sorting_algorithm = descendingAlgorithms.descending_selection_sort(draw_info)

                draw(draw_info)

    pygame.quit()


if __name__ == '__main__':
    main()
