from mazegenerator import MazeGenerator
from blob import Blob


def main():

    # Create a simple 20x20 maze
    maze_gen = MazeGenerator()

    # Get the maze structure
    maze_grid = maze_gen.maze
    shortest_path = maze_gen.shortest_path

    print(f"Maze dimensions: {len(maze_grid[0])}x{len(maze_grid)}")
    print(f"Entry: {maze_gen.maze_entry}, Exit: {maze_gen.maze_exit}")
    print(f"Shortest path length: {len(shortest_path)}")


if __name__ == "__main__":
    main()
