"""
This file stores all the necessary code for generating linked labyrinths
thate are unique to a given name.

No edits should be made to this file.
"""

from enum import Enum
import random
import math

HASH_SEED = 5381
HASH_MULTIPLIER = 33
HASH_MASK = 0x7FFFFFFF

class Item(Enum):
    """Represents one of the items that can be placed in a cell."""
    WAND = "Wand"
    POTION = "Potion"
    SPELL = "Spellbook"

class MazeCell:
    """Represents a single node of the linked list maze."""
    def __init__(self):
        self.contents: Item | None = None
        self.north: MazeCell | None = None
        self.south: MazeCell | None = None
        self.east: MazeCell | None = None
        self.west: MazeCell | None = None

def hashmasked(value: int) -> int:
    return value & HASH_MASK

def hashcode(s: str) -> int:
    hash = HASH_SEED
    for ch in s:
        hash = HASH_MULTIPLIER * hash + ord(ch)
    return hashmasked(hash)

def hashcodes(s: str, values: list[int]) -> int:
    result = hashcode(s)
    for v in values:
        result = result * HASH_MULTIPLIER + v
    return hashmasked(result)

def normal_maze_for(name: str, num_rows = 4, num_cols = 4):
    randgen = random.Random(hashcodes(name, [num_rows, num_cols]))
    maze: list[list[MazeCell]] = make_maze(num_rows, num_cols, randgen)
    linear_maze = []
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            linear_maze.append(maze[row][col])

    distances = all_pairs_shortest_paths(linear_maze)
    locations = remote_locations_in(distances)

    linear_maze[locations[1]].contents = Item.SPELL
    linear_maze[locations[2]].contents = Item.POTION
    linear_maze[locations[3]].contents = Item.WAND

    return linear_maze[locations[0]]



def twisty_maze_for(name: str, size = 12):
    randgen = random.Random(hashcodes(name,[size]))
    maze: list[MazeCell] = make_twisty_maze(size, randgen)
    distances = all_pairs_shortest_paths(maze)
    locations = remote_locations_in(distances)

    maze[locations[1]].contents = Item.SPELL
    maze[locations[2]].contents = Item.POTION
    maze[locations[3]].contents = Item.WAND

    return maze[locations[0]]

def are_adjacent(first: MazeCell, second: MazeCell) -> bool:
    return (first.east == second or
           first.west == second or
           first.north == second or
           first.south == second)

def all_pairs_shortest_paths( maze: list[MazeCell] ) -> list[list[int]]:
    result = [[len(maze) + 1 for _ in range(len(maze))] for _ in range(len(maze))]
    
    for i in range(len(maze)):
        result[i][i] = 0

    for i in range(len(maze)):
        for j in range(len(maze)):
            if are_adjacent(maze[i], maze[j]):
                result[i][j] = 1

    for i in range(len(maze)):
        next = [[0 for _ in range(len(maze))] for _ in range(len(maze))]
        for j in range(len(maze)):
            for k in range(len(maze)):
                next[j][k] = min(result[j][k], result[j][i] + result[i][k])
        result = next

    return result

def score_of(nodes: list[int], distances: list[list[int]]):
    result = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            result.append(distances[nodes[i]][nodes[j]])

    result.sort()
    return result

def lexicographically_follows(lhs: list[int], rhs: list[int]) -> bool:
    for i in range(len(lhs)):
        if lhs[i] != rhs[i]:
            return lhs[i] > rhs[i]
    return False

def remote_locations_in(distances: list[list[int]]) -> list[int]:
    result = list(range(4))
    ld = len(distances)
    
    for i in range(ld):
        for j in range(i+1, ld):
            for k in range(j + 1, ld):
                for l in range(k+1, ld):
                    curr = [i, j, k, l]
                    if lexicographically_follows(score_of(curr, distances), score_of(result, distances)):
                        result = curr

    return result

def clear_graph(nodes: list[MazeCell]) -> None:
    for node in nodes:
        node.contents = None
        node.north = None
        node.south = None
        node.east = None
        node.west = None

class Port(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

def random_free_port_of(cell: MazeCell, generator: random.Random):
    ports = []
    if cell.east is None:
        ports.append(Port.EAST)
    if cell.west is None:
        ports.append(Port.WEST)
    if cell.north is None:
        ports.append(Port.NORTH)
    if cell.south is None:
        ports.append(Port.SOUTH)
    if len(ports) == 0:
        return None

    port = generator.randrange(0, len(ports))
    return ports[port]

def link(_from: MazeCell, _to: MazeCell, link: Port) -> None:
    if link == Port.EAST:
        _from.east = _to
    elif link == Port.WEST:
        _from.west = _to
    elif link == Port.NORTH:
        _from.north = _to
    elif link == Port.SOUTH:
        _from.south = _to
    else:
        raise RuntimeError("Unknown port.")

def erdos_renyi_link(nodes: list[MazeCell], generator: random.Random) -> bool:
    threshold = math.log(len(nodes)) / len(nodes)

    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if generator.random() <= threshold:
                ilink = random_free_port_of(nodes[i], generator)
                jlink = random_free_port_of(nodes[j], generator)

                if ilink is None or jlink is None:
                    return False

                link(nodes[i], nodes[j], ilink)
                link(nodes[j], nodes[i], jlink)
    return True

def is_connected(maze: list[MazeCell]) -> bool:
    visited = set()
    frontier = []

    frontier.append(maze[0])
    while len(frontier) > 0:
        curr = frontier.pop(0)

        if not curr in visited:
            visited.add(curr)

            if curr.east is not None:
                # print(f"East of {curr.id} is {curr.east.id}")
                frontier.append(curr.east)
            if curr.west is not None:
                # print(f"West of {curr.id} is {curr.west.id}")
                frontier.append(curr.west)
            if curr.north is not None:
                # print(f"North of {curr.id} is {curr.north.id}")
                frontier.append(curr.north)
            if curr.south is not None:
                # print(f"South of {curr.id} is {curr.south.id}")
                frontier.append(curr.south)

    # print(f"Is connected: {len(visited) == len(maze)}")
    return len(visited) == len(maze)

def make_twisty_maze(num_nodes: int, generator: random.Random):
    result = []
    for _ in range(num_nodes):
        result.append(MazeCell())

    while not (erdos_renyi_link(result, generator) and is_connected(result)):
        clear_graph(result)

    return result


class Edge:
    def __init__(self, _from: MazeCell, _to: MazeCell, from_port: Port, to_port: Port):
        self._from = _from
        self._to = _to
        self.from_port = from_port
        self.to_port = to_port

def all_possible_edges_for(maze: list[list[MazeCell]]) -> list[Edge]:
    result = []
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if row + 1 < len(maze):
                result.append(Edge(maze[row][col], maze[row+1][col], Port.SOUTH, Port.NORTH))
            if col + 1 < len(maze[row]):
                result.append(Edge(maze[row][col], maze[row][col + 1], Port.EAST, Port.WEST))

    return result

def rep_for(reps: dict[MazeCell, MazeCell], cell: MazeCell) -> MazeCell:
    # TODO: I'm not sure if this function makes any sense to me
    while reps.get(cell) != cell:
        cell = reps.get(cell, cell)
    return cell

def shuffle_edges(edges: list[Edge], generator: random.Random) -> None:
    for i in range(len(edges)):
        j = generator.randint(0, len(edges) - i - 1) + i

        edges[i], edges[j] = edges[j], edges[i]


def make_maze(num_rows: int, num_cols: int, generator: random.Random) -> list[list[MazeCell]]:
    maze = [[ MazeCell() for _ in range(num_cols)] for _ in range(num_rows)]
    edges = all_possible_edges_for(maze)
    shuffle_edges(edges, generator)

    representatives = {maze[row][col]: maze[row][col] for row in range(num_rows) for col in range(num_cols)}

    edges_left = num_rows * num_cols - 1
    for i in range(1, len(edges)):
        edge = edges[i]

        rep1 = rep_for(representatives, edge._from)
        rep2 = rep_for(representatives, edge._to)

        if (rep1 != rep2):
            representatives[rep1] = rep2

            link(edge._from, edge._to, edge.from_port)
            link(edge._to, edge._from, edge.to_port)

            edges_left -= 1
    if edges_left != 0:
        raise RuntimeError("Edges remain?")

    return maze


def generate_demo_maze():
    def nice_connection(_from: MazeCell, _to: MazeCell, side: Port):
        link(_from, _to, side)
        if side == Port.NORTH:
            link(_to, _from, Port.SOUTH)
        elif side == Port.SOUTH:
            link(_to, _from, Port.NORTH)
        elif side == Port.EAST:
            link(_to, _from, Port.WEST)
        elif side == Port.WEST:
            link(_to, _from, Port.EAST)

    maze = [[ MazeCell() for _ in range(4)] for _ in range(4)]
    nice_connection(maze[0][0], maze[1][0], Port.SOUTH)
    nice_connection(maze[0][1], maze[1][1], Port.SOUTH)
    nice_connection(maze[0][3], maze[1][3], Port.SOUTH)
    nice_connection(maze[1][1], maze[2][1], Port.SOUTH)
    nice_connection(maze[1][2], maze[2][2], Port.SOUTH)
    nice_connection(maze[1][3], maze[2][3], Port.SOUTH)
    nice_connection(maze[2][0], maze[3][0], Port.SOUTH)
    nice_connection(maze[2][2], maze[3][2], Port.SOUTH)
    nice_connection(maze[2][3], maze[3][3], Port.SOUTH)

    nice_connection(maze[0][1], maze[0][2], Port.EAST)
    nice_connection(maze[1][0], maze[1][1], Port.EAST)
    nice_connection(maze[2][1], maze[2][2], Port.EAST)
    nice_connection(maze[2][2], maze[2][3], Port.EAST)
    nice_connection(maze[3][0], maze[3][1], Port.EAST)
    nice_connection(maze[3][1], maze[3][2], Port.EAST)

    maze[0][2].contents = Item.WAND
    maze[2][0].contents = Item.SPELL
    maze[3][3].contents = Item.POTION

    return maze[2][2]

