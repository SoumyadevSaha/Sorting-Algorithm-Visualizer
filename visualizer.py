import pygame as pg
import random
import math

pg.init()

# WE are using a class for all the global variables instead of declaring globally.
class DrawingOnScreen :
    BLACK = (0, 0, 0)
    ANTIQUE_WHITE = (250, 235, 215)
    RED = (255, 0, 0)
    GREEN1 = (0, 255, 0)
    GREEN2 = (0, 170, 0)
    BLUE = (0, 0, 255)
    BACKGROUND_COLOR = ANTIQUE_WHITE

    GRAY_GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]
    FONT = pg.font.SysFont("comicsans", 17)
    LARGE_FONT = pg.font.SysFont("comicsans", 32)

    SIDE_PADDING = 100 # We want padding of 50 px on the right and left of the bars in the pygame window.
    TOP_PADDING = 100 # This is to make sure so that the bars do not collide with the title, info, on the top.

    def __init__(self, width, height, lst):
        # lst is the initial list that we want to worki with.
        self.width = width
        self.height = height

        # Pygame attributes.
        self.window = pg.display
        self.window.set_mode((self.width, self.height))
        self.window.set_caption("Sorting Algo Visualizer") # Name of the window.
        self.setList(lst)

    def setList(self, lst):
        self.lst = lst
        self.min_value = min(self.lst)
        self.max_value = max(self.lst)

        # Calculate the width and height of the bars. (A bar is made up of blocks)
        self.block_width = math.floor((self.width - self.SIDE_PADDING) / len(self.lst)) # rounding as we cannot draw fractional amount.
        self.block_height = math.floor((self.height - self.TOP_PADDING) / (self.max_value - self.min_value)) # max - min value gives us our range.

        self.start_X = self.SIDE_PADDING // 2

# Drawing and Updating the screen.
def draw(screen_info, sorting_algorithm_name) :
    canvas = screen_info.window.get_surface()
    canvas.fill(screen_info.BACKGROUND_COLOR)

    algo = screen_info.LARGE_FONT.render(sorting_algorithm_name, 1, screen_info.BLUE)
    screen_info.window.get_surface().blit(algo, (screen_info.width/2 - algo.get_width()/2, 5))
    controls = screen_info.FONT.render("'R' -> Reset | 'SPACE' -> Begin Sorting | 'A' -> Ascending | 'D' -> Descending", 1, screen_info.BLACK)
    canvas.blit(controls, (screen_info.width/2 - controls.get_width()/2, 50))
    sorting = screen_info.FONT.render("'I' -> Insertion Sort | 'B' -> Bubble Sort | 'M' -> Merge Sort | 'C' -> Cocktail sort", 1, screen_info.RED)
    canvas.blit(sorting, (screen_info.width/2 - sorting.get_width()/2, 80))

    draw_list(screen_info)

    screen_info.window.update()

# Drawing the list(bars) on the screen.
def draw_list(screen_info, color_positions = {}, clear_bg = False) :
    lst = screen_info.lst

    # WE need to clear the portion of the list only and re-draw it every frame.
    if clear_bg :
        clear_rect = (screen_info.SIDE_PADDING // 2, screen_info.TOP_PADDING, 
        screen_info.width - screen_info.SIDE_PADDING, screen_info.height)

        pg.draw.rect(screen_info.window.get_surface(), screen_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst) :
        # Calculate the x and y coordinates of the top left corner of the bar.
        x = screen_info.start_X + i * screen_info.block_width
        y = screen_info.height - val * screen_info.block_height

        color = screen_info.GRAY_GRADIENTS[i % 3]
        if i in color_positions :
            color = color_positions[i]
        pg.draw.rect(screen_info.window.get_surface(), color, (x, y, screen_info.block_width, screen_info.height))
    
    if clear_bg:
        screen_info.window.update(clear_rect)

# generating a list of random numbers.
def generate_starting_list(n, min_val, max_val):
    lst = []
    
    for _ in range(n) :
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

# SORTING ALGORITHMS ->
###########################################################

def bubble_sort(draw_info, ascending = True) :
    lst = draw_info.lst

    for i in range(len(lst) - 1) :
        for j in range(len(lst) - i - 1) :
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending) :
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                # drawing the list with the swapped elements.
                draw_list(draw_info, {j: draw_info.GREEN1, j + 1: draw_info.GREEN2}, True)
                yield True
    return lst

def insertion_sort(draw_info, ascending = True) :
    lst = draw_info.lst

    for i in range(1, len(lst)) :
        key = lst[i]
        j = i-1
        while j >= 0 and ((key < lst[j] and ascending) or (key > lst[j] and not ascending)) :
            lst[j+1] = lst[j]
            j -= 1
            draw_list(draw_info, {j: draw_info.GREEN1, j + 1: draw_info.GREEN2}, True)
            yield True
        lst[j+1] = key
    return lst

def merge_sort(draw_info, ascending = True, left = 0, right = -1) :
    if right == -1 :
        right = len(draw_info.lst) - 1
    
    if left < right :
        mid = left + (right - left) // 2 # To prevent overflow for large lists.
        yield from merge_sort(draw_info, ascending, left, mid)
        yield from merge_sort(draw_info, ascending, mid + 1, right)
        n1 = mid - left + 1
        n2 = right - mid

        L = [0] * (n1)
        R = [0] * (n2)
        for i in range (0, n1) :
            L[i] = draw_info.lst[left + i]
        for j in range (0, n2) :
            R[j] = draw_info.lst[mid + 1 + j]
        i = 0
        j = 0
        k = left
        while i < n1 and j < n2 :
            if (L[i] < R[j] and ascending) or (L[i] > R[j] and not ascending) :
                draw_info.lst[k] = L[i]
                i += 1
            else :
                draw_info.lst[k] = R[j]
                j += 1
            k += 1
            draw_list(draw_info, {k - 1: draw_info.GREEN1}, True)
            yield True
        while i < n1 :
            draw_info.lst[k] = L[i]
            i += 1
            k += 1
        while j < n2 :
            draw_info.lst[k] = R[j]
            j += 1
            k += 1

def cocktail_sort(draw_info, ascending = True) :
    a = draw_info.lst
    n = len(a)
    swapped = True
    start = 0
    end = n-1
    while (swapped==True):
  
        # reset the swapped flag on entering the loop,
        # because it might be true from a previous
        # iteration.
        swapped = False
  
        # loop from left to right same as the bubble
        # sort
        for i in range (start, end):
            if (a[i] > a[i+1] and ascending) or (a[i] < a[i+1] and not ascending) :
                a[i], a[i+1]= a[i+1], a[i]
                swapped=True
                draw_list(draw_info, {i: draw_info.GREEN1, i + 1: draw_info.GREEN2}, True)
                yield True
  
        # if nothing moved, then array is sorted.
        if (swapped==False):
            break
  
        # otherwise, reset the swapped flag so that it
        # can be used in the next stage
        swapped = False
  
        # move the end point back by one, because
        # item at the end is in its rightful spot
        end = end-1
  
        # from right to left, doing the same
        # comparison as in the previous stage
        for i in range(end-1, start-1,-1):
            if (a[i] > a[i+1] and ascending) or (a[i] < a[i+1] and not ascending) :
                a[i], a[i+1] = a[i+1], a[i]
                swapped = True
                draw_list(draw_info, {i: draw_info.GREEN1, i + 1: draw_info.GREEN2}, True)
                yield True
  
        # increase the starting point, because
        # the last stage would have moved the next
        # smallest number to its rightful spot.
        start = start+1

# BROKEN !!!! ❌❌❌
def pigeonhole_sort(a):
	# size of range of values in the list
	# (ie, number of pigeonholes we need)
	my_min = min(a)
	my_max = max(a)
	size = my_max - my_min + 1

	# our list of pigeonholes
	holes = [0] * size

	# Populate the pigeonholes.
	for x in a:
		assert type(x) is int, "integers only please"
		holes[x - my_min] += 1

	# Put the elements back into the array in order.
	i = 0
	for count in range(size):
		while holes[count] > 0:
			holes[count] -= 1
			a[i] = count + my_min
			i += 1
			

a = [8, 3, 2, 7, 4, 6, 8]
print("Sorted order is : ", end = ' ')

pigeonhole_sort(a)
		
for i in range(0, len(a)):
	print(a[i], end = ' ')
	
###########################################################

def main():
    running = True
    clock = pg.time.Clock()
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    n = 57
    min_val = 5
    max_val = 150
    lst = generate_starting_list(n, min_val, max_val)
    # Initialize the drawing on screen object.
    screen = DrawingOnScreen(800, 600, lst)
    sorting = False
    ascending = True

    while running :
        clock.tick(69) # 69 is our fps, i.e, maxm number of times the while loop runs in a second is 69.
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else :
            draw(screen, sorting_algo_name)
            screen.window.update()

        for event in pg.event.get() :
            if event.type == pg.QUIT :
                running = False
            if event.type == pg.KEYDOWN :
                if event.key == pg.K_r and not sorting : # Resetting the list on pressing 'R' key.
                    lst = generate_starting_list(n, min_val, max_val)
                    screen.setList(lst)
                elif event.key == pg.K_SPACE and not sorting : # Sorting the list on pressing 'SPACE' key.
                    sorting = True
                    sorting_algorithm_generator = sorting_algorithm(screen, ascending) # It stores the generator object returned by the yield keyword.

                elif event.key == pg.K_a and not ascending and not sorting : # Press 'A' key to sort in ascending order.
                    ascending = True
                elif event.key == pg.K_d and ascending and not sorting : # Press 'D' key to sort in descending order.
                    ascending = False
                elif event.key == pg.K_b and not sorting : # For bubble sort.
                    sorting_algorithm = bubble_sort
                    sorting_algo_name = "Bubble Sort"
                elif event.key == pg.K_i and not sorting : # For insertion sort.
                    sorting_algorithm = insertion_sort
                    sorting_algo_name = "Insertion Sort"
                elif event.key == pg.K_m and not sorting : # For merge sort.
                    sorting_algorithm = merge_sort
                    sorting_algo_name = "Merge Sort"
                elif event.key == pg.K_c and not sorting : # For cocktail sort.
                    sorting_algorithm = cocktail_sort
                    sorting_algo_name = "Cocktail Sort"

    pg.quit()

if __name__ == "__main__":
    main()