This project has been created as part of the 42 curriculum by [ ], [ ], [ ].

Pac-Man Web / Python
Description
This project is a modern Python-based implementation of the classic arcade game Pac-Man, adapted for both local desktop play and Web browsers. The objective of the game is to guide Pac-Man through a randomly generated maze, consuming all the dots while evading four distinct ghosts: Blinky, Pinky, Inky, and Clyde.

The project combines dynamic maze generation, game loop state management, custom asset rendering, and highscore tracking. It is fully exportable to HTML5 and WebAssembly via Pygbag for browser-based deployment on platforms like itch.io.

Instructions
Prerequisites
Python 3.10 or higher

Pygame package installed via pip (pip install pygame)

Running Locally
To launch the game on your desktop, execute the main entry point from the project root directory:

python pacman.py

Controls
Up Arrow: Move Up

Down Arrow: Move Down

Left Arrow: Move Left

Right Arrow: Move Right

Building for Web (itch.io)
Ensure index.html and pacman.py are positioned at the root level of the project directory.

Zip all root directory contents including src/, configuration files, and assets.

Upload the archive to itch.io as an HTML project with a viewport resolution configured to 380x500 pixels (or matching canvas dimensions).

Configuration
The project uses a JSON configuration file named config.json located at the root directory to define core game parameters and board settings without requiring source code modification.

Structure & Default Values
{
"cell_size": 20,
"maze_width": 19,
"maze_height": 22,
"fps": 60,
"pacman_speed": 1,
"ghost_speed": 1,
"initial_lives": 3
}

cell_size: Size in pixels of each square grid cell (default: 20).

maze_width: Grid width dimension used for maze generation (default: 19).

maze_height: Grid height dimension used for maze generation (default: 22).

fps: Target frame rate for the game loop (default: 60).

pacman_speed: Movement speed multiplier for Pac-Man (default: 1).

ghost_speed: Movement speed multiplier for ghosts (default: 1).

initial_lives: Total number of lives Pac-Man starts with (default: 3).

Highscore System
How It Works
The highscore system reads and updates a persistent record stored in highscore.json. When a session ends or a level is completed, the current player score is compared against the top recorded score. If the new score is higher, the file is updated immediately with the new high score and displayed on the interface.

Rationale
A lightweight JSON-based persistent storage approach was chosen over a full database to keep the project portable, self-contained, and easily deployable across local environments and WebAssembly sandboxes without introducing external database dependencies.

Maze Generation
The maze layout is generated programmatically using the dedicated MazeGenerator class inside src/maze_generator.py.

A-Maze-ing Integration
The generator constructs a grid-based labyrinth ensuring all reachable paths are fully open and connected.

Outer boundaries are completely closed off to restrict entity movement within the board limits.

Playable cells (value 0) are populated with collectible dots, while wall cells (value 1) are rendered as solid obstacles.

Empty cells are selected dynamically at startup to define valid spawn points for Pac-Man and the ghosts, preventing immediate instant collisions.

Implementation
Asynchronous Game Loop: Uses asyncio and await asyncio.sleep(0) within the main loop to maintain execution compatibility with browser single-threaded event loops when compiled via Pygbag / WebAssembly.

Collision Detection: Implements pixel-and-grid bounding box collision checks between entities and maze walls using directional sub-pixel precision.

Ghost AI Logic: Ghosts implement direction choices at grid intersections based on valid paths while restricting immediate 180-degree turnbacks to guarantee continuous fluid movement.

Asset Rendering: Performs dynamic scaling and blitting of sprite images (.png) loaded directly into memory during game initialization.

General Software Architecture
The software follows an Object-Oriented Programming (OOP) model separating game entities, world generation, and loop controllers.

pacman/
├── index.html               # WebAssembly HTML entry point
├── pacman.py                # Main application & Async Game Loop
├── config.json              # Game configuration settings
├── highscore.json           # Highscore persistence store
├── project_management/      # Project tracking and task logs
└── src/
├── init.py
├── maze_generator.py    # Maze generation logic
└── assets/              # Sprite textures and images

Module / Class Relationships
Game: Central controller managing loop events, updates, drawing routines, score counters, and asset loads.

Pacman: Manages player position, vector movement, inputs, lives, and scoring.

Ghost: Manages ghost instances, direction choices, and movement constraints.

MazeGenerator: Independent helper module generating grid layouts passed directly into the Game context.

Project Management
The project was managed iteratively using milestone-based development tracking, with tasks divided into core mechanics, maze generation, graphics rendering, and web deployment.

All project management resources, task boards, and meeting notes can be found in the dedicated directory:
./project_management/

Resources
References
Pygame Documentation: https://www.pygame.org/docs/

Pygbag / Pygame-Web Documentation: https://pygame-web.github.io/

The Pac-Man Dossier (Game Mechanics): https://www.pacman-dossier.com/

AI Usage
AI tools (ChatGPT / Claude / Gemini) were utilized during the development of this project for:

Refactoring Async Loop: Converting standard Pygame blocking loops into asyncio routines required for Pygbag browser rendering.

Documentation & Formatting: Structuring and drafting project technical specifications and the README.md file.