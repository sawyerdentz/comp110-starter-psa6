"""
Module: purple_america

Program for visualizing election results in interesting ways.

Authors:
1) Sawyer Dentz - sdentz@sandiego.edu
2) Matt Oderlin - moderlin@sandiego.edu
"""

import turtle

def draw_subregion(my_turtle, polygon_points):
    """
    Draws a polygonal subregion.

    Parameters:
    my_turtle (type: Turtle) - The turtle that will do the drawing.
    polygon_points (type: List) - List of tuples of the coordinates of the
      polygonal region.

    Returns:
    None
    """
    
    my_turtle.penup()
    my_turtle.goto(polygon_points[0])
    my_turtle.pendown()
    for coord in polygon_points[1:]:
        my_turtle.goto(coord)
    my_turtle.goto(polygon_points[0])


def draw_filled_subregion(my_turtle, polygon_points, style, votes):
    """
    Draws a ploygonal subregion filled in with the correct color

    Parameters:
    my_turtle (type: Turtle) - The turtle that will do the drawing.
    polygon_points (type: List) - List of tuples of the coordinates of the
    polygonal region.
    style (type: string) - string of the style the polygon should be filled with
    votes (type: tuple) - tuple containing voting data

    Returns:
    None
    """

    if style == "black-white":
        my_turtle.pencolor("black")
        my_turtle.fillcolor("white")

    elif style == "red-blue":
        my_turtle.pencolor("white")
        if votes[0] > votes[1] and votes[0] > votes[2]:
            my_turtle.fillcolor("red")
        elif votes[1] > votes[0] and votes[1] > votes[2]:
            my_turtle.fillcolor("blue")
        else:
            my_turtle.fillcolor("gray")

    elif style == "purple":
        my_turtle.pencolor("white")
        total_votes = votes[0] + votes[1] + votes[2]
        if total_votes == 0:
            my_turtle.fillcolor("gray")
        else:
            my_turtle.fillcolor((votes[0] / total_votes, votes[2] / total_votes, votes[1] / total_votes))

    my_turtle.begin_fill()
    draw_subregion(my_turtle, polygon_points)
    my_turtle.end_fill()

def read_subregion(geo_file):
    """
    reads file and returns name of subregion and list of coordinates

    Parameters:
    geo_file (type: file object) - the file object to be read

    Return:
    (type: tuple) - tuple containing name of subregion and list of coordinates
    """

    coord_list = []
    subregion = geo_file.readline().rstrip()
    while subregion == "":
        subregion = geo_file.readline().rstrip()
    geo_file.readline()
    geo_file.readline()

    line = geo_file.readline().rstrip()
    while line != "":
        fields = line.split()
        coord_list.append((float(fields[0]), float(fields[1])))
        line = geo_file.readline().rstrip()


    return subregion, coord_list


def draw_map(geo_filename, election_results, style):
    """
    draws election map using map data, election results, and a specified style

    Parameters:
    geo_filename (type: string) - the name of the file containg coordinates to be used to draw the map
    election_results (type: string) - the name of the file containing election data
    style (type: string) - the style the user would like the map to be drawn in

    Return:
    None
    """

    f = open(geo_filename, "r")
    line = f.readline().strip().split()
    min = (float(line[0]), float(line[1]))
    line = f.readline().strip().split()
    max = (float(line[0]), float(line[1]))
    subregions = int(f.readline().strip())

    turt = turtle.Turtle()

    s = turtle.Screen()
    s.setworldcoordinates(min[0], min[1], max[0], max[1])

    turt.speed("fastest")
    s.tracer(0, 0)

    for i in range(subregions):
        subregion, coords = read_subregion(f)
        draw_filled_subregion(turt, coords, style, election_results.get(subregion, (0,0,0)))

    f.close()
    s.update()
    s.exitonclick()


def get_election_results(election_filename):
    """ 
    Reads election results from a file and returns a dictionary containing data

    Parameter:
    election_filename (type: string) - name of the file containing election results

    Return:
    (type: dictionary) - dictionary containing election data
    """

    dict = {}

    f = open(election_filename, "r")

    f.readline().split(",")
   

    for i in f:
        data = i.split(",")
        votes = (int(data[1]), int(data[2]), int(data[3]))

        dict[data[0]] = votes

    return dict  


def main():
    """
    Asks user for input and runs functions to draw map acccordingly

    Returns:
    None
    """

    geo_filename = input("Enter the name of the geography file: ")
    election_filename = input("Enter the name of the election data file: ")

    valid_input = False
    while not valid_input:
        prompt_string = "What style of map would you like?\n"
        prompt_string += "Enter 1 for black & white.\n"
        prompt_string += "Enter 2 for red & blue.\n"
        prompt_string += "Enter 3 for purple.\n"
        style_selection = input(prompt_string)
        if style_selection == "1":
            valid_input = True
            style = "black-white"
        elif style_selection == "2":
            valid_input = True
            style = "red-blue"
        elif style_selection == "3":
            valid_input = True
            style = "purple"
        else:
            print("Invalid selection!")


    results = get_election_results(election_filename)
    draw_map(geo_filename, results, style)


"""
WARNING: Do NOT modify anything below this point.
"""
if __name__ == "__main__":
    main()
