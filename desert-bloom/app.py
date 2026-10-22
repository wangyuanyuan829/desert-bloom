import streamlit as st

st.set_page_config(page_title="Desert Bloom", page_icon="🌱", layout="centered")

# Directions around a hexagon: E, SE, SW, W, NW, NE.
DIR_NAMES = ["E", "SE", "SW", "W", "NW", "NE"]
OPPOSITE = {0: 3, 1: 4, 2: 5, 3: 0, 4: 1, 5: 2}

# The board is a small pointy-top hex grid represented as 3 offset rows.
# Each tile is a two-ended pipe. Rotation changes its two open directions.
# Water starts at the left-middle tile and the tree is at the right-middle tile.
ROWS = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
]
START = (1, 0)
GOAL = (1, 2)

# Fixed puzzle solution (base orientations). Each tile connects two directions.
# Direction pairs are intentionally simple so players can learn by experimenting.
BASE_PAIRS = {
    (0, 0): (0, 3),
    (0, 1): (0, 3),
    (0, 2): (1, 4),
    (1, 0): (0, 3),
    (1, 1): (0, 3),
    (1, 2): (0, 3),
    (2, 0): (1, 4),
    (2, 1): (0, 3),
    (2, 2): (0, 3),
}

# Hex-grid neighbour offsets by direction for an odd-row offset layout.
# E, SE, SW, W, NW, NE
def neighbour(cell, direction):
    r, c = cell
    if direction == 0: return (r, c + 1)
    if direction == 3: return (r, c - 1)
    if r % 2 == 0:
        offsets = {1: (1, 0), 2: (1, -1), 4: (-1, -1), 5: (-1, 0)}
    else:
        offsets = {1: (1, 1), 2: (1, 0), 4: (-1, 0), 5: (-1, 1)}
    dr, dc = offsets[direction]
    return (r + dr, c + dc)

def in_board(cell):
    r, c = cell
    return 0 <= r < 3 and 0 <= c < 3

def rotate_pair(pair, turns):
    return tuple(sorted(((pair[0] + turns) % 6, (pair[1] + turns) % 6)))

def openings(cell, turns):
    return set(rotate_pair(BASE_PAIRS[cell], turns))

def connected_cells(turns):
    """Return all tiles reachable from the source through matching pipe openings."""
    seen = {START}
    stack = [START]
    while stack:
        cell = stack.pop()
        for direction in openings(cell, turns[cell]):
            nxt = neighbour(cell, direction)
            if not in_board(nxt):
                continue
            if OPPOSITE[direction] in openings(nxt, turns[nxt]) and nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return seen

def tile_symbol(cell, turns):
    # Arrows make the current orientation legible even in a simple browser UI.
    pair = openings(cell, turns[cell])
    glyphs = {
        frozenset((0, 3)): "↔",
        frozenset((1, 4)): "↘",
        frozenset((2, 5)): "↙",
        frozenset((0, 1)): "↗",
        frozenset((1, 2)): "↓",
        frozenset((2, 3)): "↙",
        frozenset((3, 4)): "↖",
        frozenset((4, 5)): "↑",
        frozenset((5, 0)): "↗",
    }
    return glyphs.get(frozenset(pair), "⬡")

def initialise():
    st.session_state.turns = {cell: 0 for row in ROWS for cell in row}
    # Start with the centre pipe misaligned so the tree is not watered immediately.
    st.session_state.turns[(1, 1)] = 1
    st.session_state.moves = 0
    st.session_state.won = False

if "turns" not in st.session_state:
    initialise()

st.markdown("""
<style>
.stApp { background: #fbf2df; }
.block-container { max-width: 780px; padding-top: 2rem; }
h1, h2, h3, p, label { color: #5c432b; }
div.stButton > button {
  min-height: 68px; width: 100%; border-radius: 18px;
  border: 2px solid #d6b981; background: #f4dfb5;
  color: #285b85; font-size: 1.6rem; font-weight: 700;
  box-shadow: 0 3px 0 #d2b47e;
}
div.stButton > button:hover { border-color: #4c91c6; color: #17679d; background: #e3f1fc; }
.small-note { color: #826747; font-size: .92rem; }
</style>
""", unsafe_allow_html=True)

st.title("🌵 Desert Bloom")
st.caption("A little water. A new life.")
st.write("Rotate the hexagonal pipe tiles to guide water from the well to the thirsty tree.")

with st.container(border=True):
    st.markdown("**How to play**")
    st.write("1. Click a tile to rotate its pipe by 60°.")
    st.write("2. Connect neighbouring pipe openings from 💧 the well to 🌱 the tree.")
    st.write("3. Use **Reset puzzle** if you want to start over.")

reachable = connected_cells(st.session_state.turns)
is_won = GOAL in reachable
st.session_state.won = is_won

st.markdown("### Your desert")
st.caption("Click any tile to rotate it. Blue tiles are currently connected to the water source.")

# Offset rows slightly to evoke a hexagonal board without complex drawing dependencies.
for r, row in enumerate(ROWS):
    left_pad, center, right_pad = st.columns([0.5, 3, 0.5])
    with center:
        cols = st.columns(3)
        for c, cell in enumerate(row):
            with cols[c]:
                is_connected = cell in reachable
                if cell == START:
                    label = "💧\n" + tile_symbol(cell, st.session_state.turns)
                elif cell == GOAL:
                    label = ("🌳" if is_won else "🥀") + "\n" + tile_symbol(cell, st.session_state.turns)
                else:
                    label = tile_symbol(cell, st.session_state.turns)
                if is_connected:
                    st.markdown('<div style="text-align:center;font-size:12px;color:#267db4;">WATER CONNECTED</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="text-align:center;font-size:12px;color:#9c825f;">DRY TILE</div>', unsafe_allow_html=True)
                if st.button(label, key=f"tile_{r}_{c}", help=f"Rotate tile at row {r+1}, column {c+1}"):
                    st.session_state.turns[cell] = (st.session_state.turns[cell] + 1) % 6
                    st.session_state.moves += 1
                    st.rerun()

st.markdown("---")
left, right = st.columns(2)
with left:
    st.metric("Moves", st.session_state.moves)
with right:
    st.metric("Tiles reached by water", f"{len(reachable)} / 9")

if is_won:
    st.success("🌱 The water reached the tree! The desert is blooming. You solved the puzzle!")
    st.balloons()
else:
    st.info("The tree is still thirsty. Keep rotating tiles until the water reaches it.")

if st.button("↻ Reset puzzle", type="primary", use_container_width=True):
    initialise()
    st.rerun()

st.markdown(
    '<p class="small-note">Prototype note: this version focuses on the interaction loop and path-connection logic. '
    'The board uses a simplified tile layout; later iterations can add custom hexagon artwork and flowing-water animation.</p>',
    unsafe_allow_html=True,
)
