import sys
import os
import turtle

WIDTH = 600
HEIGHT = 600
AXISCOLOR = "blue"
BACKGROUNDCOLOR = "black"
NAMEDSTARS = "white"
UNNAMEDSTARS = "grey"


# This function initializes the turtle object as well as the window
# INPUT: None
# RETURN: Turtle Object
def setup():
    pointer = turtle.Turtle()
    screen = turtle.getscreen()
    screen.setup(WIDTH, HEIGHT, 0, 0)
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    pointer.hideturtle()
    screen.delay(delay=0)
    turtle.bgcolor(BACKGROUNDCOLOR)
    pointer.up()
    return pointer


# This function draws the blue axes and the tick marks for locating stars
# INPUT: Turtle object
# RETURN: None
def draw_axes(pointer):
    # Draws the lines and ticks for the axes
    for i in range(4):
        pointer.goto(300, 300)
        pointer.down()
        pointer.color(AXISCOLOR)
        for x in range(4):
            pointer.forward(0.25 * 300)
            pointer.left(90)
            pointer.back(5)
            pointer.forward(10)
            pointer.back(5)
            pointer.right(90)
        pointer.right(90)

    # Draws the numbers for the tick positions
    pointer.up()
    pointer.goto(0, 320)
    for i in range(2):
        for x in range(2):
            for j in range(4):
                pointer.down()
                if pointer.ycor() == 320:
                    pointer.write(pointer.pos()[0]/300-1, font=("Arial", 10, "normal"))
                else:
                    pointer.write(pointer.pos()[1]/300-1, font=("Arial", 10, "normal"))
                pointer.up()
                pointer.forward(0.25 * 300)
            pointer.forward(0.25*300)
        pointer.goto(320, 0)
        pointer.left(90)
    pointer.up()
    pointer.home()


# This function takes in a filename given by either the system arguments or through user input...
# ...and returns a list of nested lists containing star x, y coordinates and their magnitudes. It...
# ...also returns a dictionary of all named stars with key=name/value=[x,y,mag]
# INPUT: Star data file
# RETURN: star location information
def read_star_info(filename):
    if not os.path.isfile(filename):
        print('ERROR: The star filename you have given does not exist.')
        sys.exit(1)
    with open(filename) as f:
        data = [lines.strip().split(',') for lines in f]
    for x in range(len(data)):
        if len(data[x]) < 7:
            print('ERROR: Not enough data entries in star file.')
            sys.exit(1)
    star_names = [data[x][-1].split(';') for x in range(len(data))]
    star_info = [data[x][:-1] for x in range(len(data))]
    for x in range(len(star_info)):
        star_info[x] = [star_info[x][0], star_info[x][1], star_info[x][4]]
    star_info_dict = {}
    for x in range(len(star_names)):
        star_info_dict.update({tuple(star_names[x]): tuple(star_info[x])})
    new_star_info_dict = {}
    for k in star_info_dict.keys():
        for x in range(len(k)):
            new_star_info_dict.update({k[x]: star_info_dict[k]})
    for k, v in star_info_dict.items():
        print(k[0], 'is at', v[:-1], 'with magnitude', v[-1])
    return star_info, new_star_info_dict


# This function draws each star from the star_info input data. Named stars are cross-checked with...
# ...the star_info_dict dictionary and are drawn in white. All other unnamed stars are drawn in grey.
# INPUT: Turtle object, star[x,y,mag], star key=name/value=[x,y,mag] dictionary, bit to display names
# RETURN: None
def draw_stars(pointer, star_info, star_info_dict, star_name_bit):
    name = ''
    for star in star_info:
        if tuple(star) in star_info_dict.values():
            pointer.color(NAMEDSTARS)
            if star_name_bit == 1:
                for k, v in star_info_dict.items():
                    if tuple(star) == v:
                        name = k
        else:
            pointer.color(UNNAMEDSTARS)
        pointer.goto(300+(float(star[0])*300), 300+(float(star[1])*300))
        pointer.down()
        pointer.begin_fill()
        pointer.circle((10/(float(star[2])+2))/2)
        pointer.end_fill()
        if star_name_bit == 1 and pointer.pencolor() == NAMEDSTARS:
            pointer.up()
            pointer.goto(pointer.xcor(), pointer.ycor()+10)
            pointer.down()
            pointer.write(name, align='center', font=("Arial", 5, "normal"))
        pointer.up()
    pointer.up()
    pointer.home()


# This function reads constellation file data given from user input
# INPUT: Constellation data file
# RETURN: Constellation star location data, constellation name
def read_constellation_info(filename):
    with open(filename) as f:
        constellation_info = [lines.strip().split(',') for lines in f]
    for x in range(1, len(constellation_info)):
        if len(constellation_info[x]) < 2:
            print('ERROR: Not enough data entries in constellation file.')
            sys.exit(1)
    constellation_name = constellation_info[0][0]
    constellation_info = constellation_info[1:]
    stars = set()
    for s in constellation_info:
        stars.add(s[0])
        stars.add(s[1])
    print(constellation_name, 'constellation contains', stars)
    return constellation_info, constellation_name


# This function draws the constellation when given the constellation data read from a file
# INPUT: Turtle object, constellation star location data, star key=name/value=[x,y,mag], color bit
# RETURN: None
def draw_constellation(pointer, constellation_info, constellation_name, star_info_dict, color):
    min_x, max_x, min_y, max_y = 1.0, -1.0, 1.0, -1.0
    if color == 0:
        pointer.color('red')
    elif color == 1:
        pointer.color('green')
    else:
        pointer.color('yellow')
    for x in range(len(constellation_info)):
        for k in range(len(constellation_info[x])):
            x_cor = float(star_info_dict[constellation_info[x][k]][0])
            if min_x > x_cor:
                min_x = x_cor
            if max_x < x_cor:
                max_x = x_cor
            y_cor = float(star_info_dict[constellation_info[x][k]][1])
            if min_y > y_cor:
                min_y = y_cor
            if max_y < y_cor:
                max_y = y_cor
            pointer.goto(300+(x_cor*300), 300+(y_cor*300))
            pointer.down()
        pointer.up()
    with open('boxes/'+constellation_name+'_box.dat', 'w') as f:
        f.write('{}\n{}\n{}\n{}'.format(str(min_x), str(max_x), str(min_y), str(max_y)))
    pointer.up()
    pointer.home()

# This function draws a named box around the constellation to better highlight it.
# INPUT: Turtle object, name of the constellation to draw a box around
# RETURN: None
def draw_constellation_border_box(pointer, constellation_name):
    pointer.color('orange')
    with open('boxes/'+constellation_name+'_box.dat') as f:
        points = [lines.strip() for lines in f]

    min_x = float(points[0])
    max_x = float(points[1])
    min_y = float(points[2])
    max_y = float(points[3])

    # Top left corner
    pointer.goto(300 + (min_x * 300) - 10, 300 + (max_y * 300) + 10)
    pointer.down()
    # Top right corner
    pointer.goto(300 + (max_x * 300) + 10, 300 + (max_y * 300) + 10)
    # Bottom right corner
    pointer.goto(300 + (max_x * 300) + 10, 300 + (min_y * 300) - 10)
    # Bottom left corner
    pointer.goto(300 + (min_x * 300) - 10, 300 + (min_y * 300) - 10)
    # Top left corner
    pointer.goto(300 + (min_x * 300) - 10, 300 + (max_y * 300) + 10)
    pointer.up()

    # Top middle for drawing name
    pointer.goto(((300 + (max_x * 300))+(300 + (min_x * 300)))/2, 300 + (max_y * 300) + 15)
    pointer.down()
    pointer.write(constellation_name, align='center', font=("Arial", 5, "normal"))
    pointer.up()


def main():
    pointer = setup()
    star_name_bit = 0

    # Checking number of arguments, whether the user entered system arguments, and whether the -names flag was given
    if len(sys.argv) > 3:
        print('ERROR: Too many arguments given (2 expected)')
        sys.exit(1)
    elif len(sys.argv) == 3 and '-names' not in sys.argv:
        print('ERROR: If two arguments are given one must be -names')
        sys.exit(1)
    elif len(sys.argv) == 3:
        star_name_bit = 1
        if sys.argv[1] != '-names':
            star_info, star_info_dict = read_star_info(sys.argv[1])
        else:
            star_info, star_info_dict = read_star_info(sys.argv[2])
    elif len(sys.argv) == 2 and '-names' not in sys.argv:
        star_info, star_info_dict = read_star_info(sys.argv[1])
    elif len(sys.argv) == 2 and '-names' in sys.argv:
        star_name_bit = 1
        stars_location_file = input('Enter a star location filename:')
        star_info, star_info_dict = read_star_info(stars_location_file)
    else:
        stars_location_file = input('Enter a star location filename:')
        star_info, star_info_dict = read_star_info(stars_location_file)

    # Calling drawing functions for the axes and stars
    draw_axes(pointer)
    draw_stars(pointer, star_info, star_info_dict, star_name_bit)

    # Continuously asking for user input of constellation files until nothing is entered
    color = 0
    while True:
        constellation_filename = input('Enter a constellation filename:')
        if constellation_filename == '':
            break
        elif os.path.isfile(constellation_filename):
            constellation_info, constellation_name = read_constellation_info(constellation_filename)
            draw_constellation(pointer, constellation_info, constellation_name, star_info_dict, color)
            draw_constellation_border_box(pointer, constellation_name)
            color = (color + 1) % 3


main()
