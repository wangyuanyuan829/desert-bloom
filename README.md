# Desert Bloom 🌵💧

**A little water. A new life.**

**Live Demo:** [Play Desert Bloom] (https://desert-bloom.onrender.com/))

![![Desert Bloom gameplay screenshot](d400ad7074f8306cbfb3334097b78543.png)

## About the Project

Desert Bloom is a small browser-based hexagonal puzzle game built with Python and Streamlit.

The player rotates connected hexagonal channel tiles to guide water from a water source to withered plants in a desert. When a plant receives water, it comes back to life.

The goal is not to connect every channel on the board. Players only need to deliver water to the target plants to complete each level.

## Intended Users

The game is designed for people who enjoy short, casual logic puzzles. It aims to provide a simple but satisfying experience through experimentation, visual feedback, and progressively more challenging levels.

## Main Interaction

- **Rotate a tile:** Click a hexagonal tile to rotate its channel.
- **Guide the water:** Connect channel openings so water can flow from the source to the target plants.
- **Revive the plants:** A plant changes from a withered state to a living state when water reaches it.
- **Progress through levels:** Complete three levels with increasing difficulty. The final level requires the player to water three plants.
- **Receive feedback:** The game shows water connections, the number of moves, plant progress, and a success message when the level is completed.
- **Continue or reset:** Continue to the next level after winning, or reset the current puzzle if needed.
- **Audio controls:** Use the music control to turn the background music on or off.

## How to Run Locally

### Requirements

- Python
- `uv`
- The dependencies listed in `requirements.txt`

### Windows (PowerShell)

Run these commands from the project directory:

1. Create a virtual environment:

   ```powershell
   uv venv
   ```

2. Install the dependencies:

   ```powershell
   uv pip install --python .venv\Scripts\python.exe -r requirements.txt
   ```

3. Start the game:

   ```powershell
   uv run --python .venv\Scripts\python.exe streamlit run app.py
   ```

4. Open the local URL shown in the terminal, usually `http://localhost:8501`.

### Online Version

The game is deployed on Render. Open the Live Demo link at the top of this document to play it in a browser.

The free hosting service may temporarily sleep after a period of inactivity, so the first visit may take some time to load.

## Design and Iteration

The project began as a simple pipe-connection puzzle inspired by hexagonal rotation games. It was adapted into a desert irrigation experience in which water helps restore life.

The main design decisions were to make each tile directly clickable, connect the hexagonal board visually, use plant revival as the main goal, and increase difficulty across three levels.

Feedback about the original objective led to a more focused win condition: players need to water the target plants rather than connect every channel.

## Known Limitations

- The game uses a predefined set of levels rather than an unlimited procedural puzzle generator.
- The puzzle is designed around a small number of target plants and a fixed board layout for each level.
- Online availability depends on the hosting service.

## Credits

See [CREDITS.md](CREDITS.md) for information about code, tools, and media used in the project.

## Development Process

See [PROCESS.md](PROCESS.md) for the design changes, user testing, and use of AI tools.
