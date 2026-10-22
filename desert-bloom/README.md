# Desert Bloom 🌵💧

**Desert Bloom** is a small browser-based puzzle made with Python and Streamlit. The player rotates pipe tiles to try to connect a water source to a thirsty tree in a desert.

## Intended user

People who enjoy short, casual logic puzzles. The game is designed to be understandable without a long tutorial.

## Main interaction

- Click a tile to rotate its pipe by one step (60 degrees).
- The program checks which tiles are reachable from the water source through matching pipe openings.
- Connected tiles are labelled `WATER CONNECTED`; other tiles are labelled `DRY TILE`.
- When the water reaches the tree, the game displays a success message.
- Use **Reset puzzle** to restore the starting state.

This creates a simple interaction loop: **input → changed pipe orientation → connection feedback → next decision**.

## Built with

- Python 3.10 or newer
- Streamlit

## Run locally

1. Install Python 3.10+.
2. Open this repository folder in VS Code.
3. Open the VS Code terminal.
4. Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`. Open it in a browser.

## Files

- `app.py` — game interface and puzzle logic
- `requirements.txt` — Python dependency list
- `PROCESS.md` — development process and user-test record template
- `CREDITS.md` — credits and asset notes

## Known limitations

- This is a small prototype with a simplified tile layout and pipe symbols rather than a fully illustrated hexagonal board.
- The game prioritises the interaction loop and clear feedback over complex animation.
- The puzzle layout and tile orientations may be refined during testing. Confirm that the current puzzle has a reachable solution before submitting.
- The app needs Python and Streamlit installed to run locally. An online deployment is optional.

## Screenshot / live link

Add a screenshot after running the app and place it in this repository (for example, `assets/screenshot.png`). If you deploy the app, add the public URL here.

## Credits

See [`CREDITS.md`](CREDITS.md). All development decisions and changes should be reflected in the Git commit history.
