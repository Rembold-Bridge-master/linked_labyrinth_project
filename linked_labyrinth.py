from MazeUtils import normal_maze_for, twisty_maze_for

NAME = "YourNameHere"


def is_path_to_freedom(start, path_out):
    """Checks to see if a path to freedom is valid

    Args:
        start (MazeCell): The cell the player starts in
        path_out (str): The sequence of N,S,E,W directions the player follows
    Returns:
        (bool): Whether the directions successfully escape the maze
    """
    # Fill this in with your code!





def gridded(path_out):
    """Generates a gridded maze unique to the NAME and checks the provided path
    to see if it successfully escapes the maze.

    Args:
        path_out (str): The sequence of N,S,E, and W directions to follow
    """

    start = normal_maze_for(NAME)

    if is_path_to_freedom(start, path_out): # place breakpoint on this line
        print("Congratulations! You've found your way out of your gridded labyrinth.")
    else:
        print("Sorry, but you're still stuck in your gridded labyrinth.")

def twisty(path_out):
    """Generates a twisty maze unique to the NAME and checks the provided path
    to see if it successfully escapes the maze.

    Args:
        path_out (str): The sequence of N,S,E, and W directions to follow
    """
    start = twisty_maze_for(NAME)

    if is_path_to_freedom(start, path_out): # place breakpoint on this line
        print("Congratulations! You've found your way out of your twisty labyrinth.")
    else:
        print("Sorry, but you're still stuck in your twisty labyrinth.")


if __name__ == '__main__':
    gridded("N")
    twisty("N")
