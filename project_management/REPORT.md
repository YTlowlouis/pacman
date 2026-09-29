# Project Management Report - Pac-Man

## 1. Team Organization
**Team Members:** [ ] and [ ]

**Task Distribution:**
- **[ ]**: Core game loop architecture, collision detection logic, Ghost AI algorithms, and Pygame input handling.
- **[ ]**: A-Maze-ing (`mazegen`) package integration, asset rendering, UI (menus/score), highscore persistence, and Pygbag (Web) adaptation.

**Workflow and Decision Making:**
Decisions were made collaboratively during bi-weekly sync meetings (via Discord/Slack). Code was shared and version-controlled via GitHub. Conflicts in technical choices (e.g., how to handle ghost movement) were resolved by prototyping both ideas quickly and keeping the most performant one. Issue tracking was handled directly through GitHub Issues.

---

## 2. Project Timeline & Progress Tracking
We utilized a Kanban board (GitHub Projects) to track our progress. The project was divided into 4 main sprints:

- **Sprint 1 (Days 1-3): Architecture & Setup**
  - Repository initialization, Makefile setup, and Pygame basic window loop.
  - *Status:* Completed on time.
- **Sprint 2 (Days 4-7): Maze Integration & Core Mechanics**
  - Parsing the `mazegen` output, rendering walls, and implementing basic Pac-Man movement with collision.
  - *Status:* Completed on time.
- **Sprint 3 (Days 8-11): Entities & AI**
  - Adding dots, scoring system, and Ghost autonomous movement.
  - *Status:* Delayed by 1 day due to complex sub-pixel collision bugs when ghosts turned at intersections.
- **Sprint 4 (Days 12-14): Polish & Web Deployment**
  - Highscore system via JSON, configuration file parsing, UI polish, and Pygbag implementation for itch.io.
  - *Status:* Completed on time.

Overall, the actual progress closely matched the initial timeline, with only a minor delay during the AI implementation phase, which was absorbed by the buffer time in Sprint 4.

---

## 3. Project Analysis and Associated Choices
- **Object-Oriented Programming (OOP):** We chose a strict OOP model (`Game`, `Entity`, `Pacman`, `Ghost`, `Level`). This made it incredibly easy to manage multiple ghosts by simply instantiating the `Ghost` class four times with different start parameters.
- **Configuration & Highscore files:** We opted for `.json` files instead of `.env` or databases (like SQLite). JSON is natively supported by Python, highly readable, and lightweight enough for a local arcade game, ensuring smooth compilation for the WebAssembly version.
- **Movement Logic:** Instead of locking entities strictly to a grid step-by-step, we allowed smooth pixel movement and implemented "input buffering" for Pac-Man, allowing the player to queue a turn slightly before reaching an intersection for a better game feel.

---

## 4. Risk Analysis and Mitigation
| Identified Risk | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **Pygame Performance Drops** | High (stuttering loop) | Instead of checking collisions against every wall in the maze every frame, we only check collisions against walls immediately adjacent to the entity's current grid position. |
| **A-Maze-ing Integration Failure** | Critical (no map) | Tested the `mazegen` package independently in a dummy script before plugging it into the Pygame engine. Built a fallback hardcoded map just in case (unused). |
| **Web Deployment (Pygbag) Freezes** | High (unplayable on browser) | Standard Pygame loops block the browser thread. We migrated the main loop to an `asyncio` structure early in development to ensure compatibility. |

---

## 5. Acceptance Test Plan
We established a manual testing protocol before merging major branches into `main`.

**Features Tested:**
1. *Wall Collisions:* Moving Pac-Man into every wall direction to ensure no clipping.
2. *A-Maze-ing Generator:* Generating 20 random seeds to ensure the maze is always perfect and fully reachable.
3. *Ghost Collisions:* Letting a ghost touch Pac-Man to verify life deduction and respawn logic.
4. *Score Tracking:* Eating dots and finishing the level to check if the highscore saves correctly to the JSON file.

**Bugs Found & Fixed:**
- *Bug:* Pac-Man getting stuck on corners when turning too early.
  *Fix:* Implemented a bounding-box tolerance and input buffering.
- *Bug:* Highscore file wiping completely if the game crashed.
  *Fix:* Added a try-except block to safely load and write to the JSON file, ensuring data persistence.

---

## 6. Summary of Blocking Points and Conflicts
**Blocking Points:**
The most significant blocking point was adapting the game loop for Web browser play via `Pygbag`. Our initial `while True` loop worked perfectly on desktop but crashed the browser tab. We had to pause feature development for one day to research and refactor the entire loop using `asyncio` and `await asyncio.sleep(0)`.

**Conflicts:**
There were no interpersonal conflicts. Technically, we had a debate regarding the Ghost AI: whether to use a strict pathfinding algorithm (A*) or a semi-random intersection logic. We chose the semi-random intersection logic as it was less CPU-intensive and felt closer to the chaotic, arcade nature of the original game within the scope of our randomly generated mazes.