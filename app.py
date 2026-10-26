
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Desert Bloom",
    page_icon="🌱",
    layout="centered"
)

# --------------------------------------------------
# 1. GAME SETTINGS
# Directions: E, SE, SW, W, NW, NE
# --------------------------------------------------

OPPOSITE = {0: 3, 1: 4, 2: 5, 3: 0, 4: 1, 5: 2}

CELLS = [(r, c) for r in range(3) for c in range(3)]
START = (1, 0)
GOAL = (1, 2)

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

# --------------------------------------------------
# 2. HEXAGON NEIGHBOURS
# Odd-row offset layout
# --------------------------------------------------

def neighbour(cell, direction):
    r, c = cell

    if direction == 0:
        return (r, c + 1)
    if direction == 3:
        return (r, c - 1)

    if r % 2 == 0:
        offsets = {
            1: (1, 0), 2: (1, -1),
            4: (-1, -1), 5: (-1, 0)
        }
    else:
        offsets = {
            1: (1, 1), 2: (1, 0),
            4: (-1, 0), 5: (-1, 1)
        }

    dr, dc = offsets[direction]
    return (r + dr, c + dc)


def openings(cell):
    pair = BASE_PAIRS[cell]
    turn = st.session_state.turns[cell]
    return {
        (pair[0] + turn) % 6,
        (pair[1] + turn) % 6
    }


def connected_cells():
    seen = {START}
    stack = [START]

    while stack:
        cell = stack.pop()

        for direction in openings(cell):
            nxt = neighbour(cell, direction)

            if nxt not in CELLS or nxt in seen:
                continue

            if OPPOSITE[direction] in openings(nxt):
                seen.add(nxt)
                stack.append(nxt)

    return seen


def initialise():
    st.session_state.turns = {
        cell: 0 for cell in CELLS
    }
    # The starting puzzle is not solved immediately.
    st.session_state.turns[(1, 1)] = 1
    st.session_state.moves = 0


if "turns" not in st.session_state:
    initialise()


# --------------------------------------------------
# 3. DRAW A HEXAGON WITH AN IRRIGATION CHANNEL
# Render SVG inside a component iframe so it is
# displayed as artwork, not as source code.
# --------------------------------------------------

def tile_svg(cell, wet, won):
    pair = openings(cell)

    # Six points around the centre of the hexagon.
    points = [
        (166, 100),  # E
        (133, 157),  # SE
        (67, 157),   # SW
        (34, 100),   # W
        (67, 43),    # NW
        (133, 43),   # NE
    ]

    x1, y1 = points[pair.pop()] if False else (0, 0)
    # Sort the two openings for consistent drawing.
    a, b = sorted(openings(cell))
    x1, y1 = points[a]
    x2, y2 = points[b]

    path = f"M {x1} {y1} L 100 100 L {x2} {y2}"

    ground = "#b9dce4" if wet else "#e8d3a5"
    border = "#fff7e7"
    pipe_outer = "#377fa6" if wet else "#b49a6d"
    pipe_inner = "#72d9f5" if wet else "#d4bc8e"

    if cell == START:
        plant_or_well = """
        <circle cx="100" cy="100" r="21"
                fill="#e8f8ff" stroke="#368fbd" stroke-width="3"/>
        <path d="M100 82 C91 96 88 101 88 107
                 A12 12 0 0 0 112 107
                 C112 101 109 96 100 82Z"
              fill="#36a9e8"/>
        """
    elif cell == GOAL and won:
        plant_or_well = """
        <path d="M100 137 L100 98 M100 119 L78 99 M100 111 L121 91"
              fill="none" stroke="#397f39" stroke-width="7"
              stroke-linecap="round"/>
        <ellipse cx="77" cy="97" rx="16" ry="8"
                 transform="rotate(35 77 97)" fill="#65ad4c"/>
        <ellipse cx="122" cy="89" rx="16" ry="8"
                 transform="rotate(-35 122 89)" fill="#65ad4c"/>
        <ellipse cx="100" cy="91" rx="9" ry="15" fill="#7dc75b"/>
        """
    elif cell == GOAL:
        plant_or_well = """
        <path d="M100 137 L100 111 M100 126 L82 116 M100 129 L118 119"
              fill="none" stroke="#92985a" stroke-width="7"
              stroke-linecap="round"/>
        <ellipse cx="81" cy="114" rx="14" ry="7"
                 transform="rotate(25 81 114)" fill="#aab36d"/>
        <ellipse cx="119" cy="117" rx="14" ry="7"
                 transform="rotate(-25 119 117)" fill="#b3b96f"/>
        """
    else:
        plant_or_well = ""

    animation = ""
    if wet:
        animation = f"""
        <path d="{path}" fill="none" stroke="#e9fbff"
              stroke-width="3" stroke-dasharray="6 12"
              stroke-linecap="round">
          <animate attributeName="stroke-dashoffset"
                   from="0" to="-36" dur="1.2s"
                   repeatCount="indefinite"/>
        </path>
        """

    status = "WATER" if wet else "DRY"
    status_color = "#286f96" if wet else "#9a7c51"

    return f"""
    <html>
    <head>
    <style>
      html, body {{
        margin: 0;
        padding: 0;
        background: transparent;
        overflow: hidden;
      }}
      svg {{
        display: block;
        width: 100%;
        height: auto;
      }}
    </style>
    </head>
    <body>
    <svg viewBox="0 0 200 200"
         xmlns="http://www.w3.org/2000/svg">
      <polygon points="100,8 180,54 180,146
                       100,192 20,146 20,54"
               fill="{ground}" stroke="{border}"
               stroke-width="5" stroke-linejoin="round"/>
      <polygon points="100,18 170,59 170,141
                       100,182 30,141 30,59"
               fill="none" stroke="#d8bf8e" stroke-width="1.5"/>

      <path d="{path}" fill="none" stroke="{pipe_outer}"
            stroke-width="22" stroke-linecap="round"
            stroke-linejoin="round"/>
      <path d="{path}" fill="none" stroke="{pipe_inner}"
            stroke-width="12" stroke-linecap="round"
            stroke-linejoin="round"/>
      {animation}
      <circle cx="100" cy="100" r="6" fill="{pipe_outer}"/>

      {plant_or_well}

      <text x="100" y="174" text-anchor="middle"
            font-family="Arial,sans-serif" font-size="11"
            font-weight="bold" fill="{status_color}">
        {status}
      </text>
    </svg>
    </body>
    </html>
    """


# --------------------------------------------------
# 4. PAGE DESIGN
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background: #f8efd9;
}
.block-container {
    max-width: 850px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
h1, h2, h3, p, label {
    color: #4c3928;
}
.hero {
    font-size: clamp(2.2rem, 6vw, 3.8rem);
    font-weight: 850;
    letter-spacing: -1px;
}
.subtitle {
    color: #9a8266;
    font-size: 1.1rem;
    margin-bottom: 1.2rem;
}
div.stButton > button {
    min-height: 38px;
    border-radius: 10px;
    border: 1px solid #c8aa78;
    background: #f1dfba;
    color: #60472e;
    font-weight: 700;
}
div.stButton > button:hover {
    background: #d7edf8;
    border-color: #3989bd;
    color: #17679d;
}
div[data-testid="stMetric"] {
    background: rgba(255,255,255,.3);
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #eadbc0;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="hero">🌵 Desert Bloom</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">A little water. A new life.</div>',
    unsafe_allow_html=True
)
st.write(
    "Rotate the hexagonal channels to guide water "
    "from the well to the thirsty seedling."
)

with st.container(border=True):
    st.markdown("**How to play**")
    st.write("1. Press ↻ to rotate a channel by 60°.")
    st.write("2. Connect neighbouring channels from 💧 the well to 🥀 the seedling.")
    st.write("3. When water reaches the seedling, the desert blooms.")


# --------------------------------------------------
# 5. HONEYCOMB BOARD
# The middle row is shifted to create a honeycomb.
# --------------------------------------------------

reachable = connected_cells()
is_won = GOAL in reachable

st.markdown("## Your desert")
st.caption("Blue channels are connected to the water source.")

for r in range(3):
    if r == 1:
        left_space, tile_area, right_space = st.columns(
            [0.5, 4, 0.5]
        )
    else:
        left_space, tile_area, right_space = st.columns(
            [0.1, 4, 0.1]
        )

    with tile_area:
        cols = st.columns(3, gap="small")

        for c in range(3):
            cell = (r, c)

            # Shift the middle row slightly right.
            if r == 1:
                # Keep a little extra space before the first tile.
                pass

            with cols[c]:
                components.html(
                    tile_svg(cell, cell in reachable, is_won),
                    height=155,
                    scrolling=False
                )

                if st.button(
                    "↻ Rotate",
                    key=f"rotate_{r}_{c}",
                    use_container_width=True
                ):
                    st.session_state.turns[cell] = (
                        st.session_state.turns[cell] + 1
                    ) % 6
                    st.session_state.moves += 1
                    st.rerun()


# --------------------------------------------------
# 6. PROGRESS AND RESET
# --------------------------------------------------

st.divider()

left, right = st.columns(2)

with left:
    st.metric("Moves", st.session_state.moves)

with right:
    st.metric(
        "Tiles reached by water",
        f"{len(reachable)} / 9"
    )

if is_won:
    st.success(
        "🌱 The water reached the seedling! "
        "The desert is blooming!"
    )
    st.balloons()
else:
    st.info(
        "The seedling is still thirsty. "
        "Keep rotating the channels to guide the water."
    )

if st.button(
    "↻ Reset puzzle",
    type="primary",
    use_container_width=True
):
    initialise()
    st.rerun()

st.caption(
    "Desert Bloom · Connect the channels, deliver the water, restore life."
)
