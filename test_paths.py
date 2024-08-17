"""
This file serves to test the is_path_to_freedom function written by students.

If using PyTest, it should be automatically picked up and each of the methods
run. I am also provided code at the bottom so that this can be run manually if 
PyTest is not installed.

The generated demo maze is the gridded maze shown in the guide.
"""

from MazeUtils import generate_demo_maze
from linked_labyrinth import is_path_to_freedom

class TestPathToFreedom:

    maze = generate_demo_maze()

    def test_valid_paths(self):
        assert is_path_to_freedom(self.maze, "ESNWWNNEWSSESWWN")
        assert is_path_to_freedom(self.maze, "SWWNSEENWNNEWSSEES")
        assert is_path_to_freedom(self.maze, "WNNEWSSESWWNSEENES")
        assert is_path_to_freedom(self.maze, "WNNEWSSESWWNSEENESNNN")

    def test_valid_then_wall(self):
        assert not is_path_to_freedom(self.maze, "ESNWWNNEWSSESWWNN")
        assert not is_path_to_freedom(self.maze, "SWWNSEENWNNEWSSEESNNNN")
        assert not is_path_to_freedom(self.maze, "WNNEWSSESWWNSEENESS")

    def test_invalid_wall_hits(self):
        assert not is_path_to_freedom(self.maze, "EE")
        assert not is_path_to_freedom(self.maze, "NN")
        assert not is_path_to_freedom(self.maze, "WW")
        assert not is_path_to_freedom(self.maze, "SS")

    def test_invalid_no_items(self):
        assert not is_path_to_freedom(self.maze, "ENNSSWSWW")
        assert not is_path_to_freedom(self.maze, "WNWNSENSSEN")

    def test_invalid_single_item(self):
        assert not is_path_to_freedom(self.maze, "ESNNNSSWWNWN")
        assert not is_path_to_freedom(self.maze, "WNNEWSSEN")
        assert not is_path_to_freedom(self.maze, "SWWNSEENN")

    def test_invalid_double_item(self):
        assert not is_path_to_freedom(self.maze, "SWWNSEENWNNEW")
        assert not is_path_to_freedom(self.maze, "ESNWSWWN")
        assert not is_path_to_freedom(self.maze, "WNWNSENEWSSEES")

    def test_duplicate_items(self):
        assert not is_path_to_freedom(self.maze, "ESNSNS")
        assert not is_path_to_freedom(self.maze, "SWWNSEENWNNEWE")
        assert is_path_to_freedom(self.maze, "ESNWWNNEWSSESWWNSN")
        assert is_path_to_freedom(self.maze, "SWWNSEENWNNEWSSEESNS")
        assert is_path_to_freedom(self.maze, "WNNEWSSESWWNSEENESNWWNNE")


if __name__ == '__main__':
    testrun = TestPathToFreedom()
    testrun.test_valid_paths()
    testrun.test_valid_then_wall()
    testrun.test_invalid_wall_hits()
    testrun.test_invalid_no_items()
    testrun.test_invalid_single_item()
    testrun.test_invalid_double_item()
    testrun.test_duplicate_items()

