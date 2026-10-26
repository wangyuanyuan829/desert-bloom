
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Desert Bloom",
    page_icon="🌵",
    layout="centered"
)

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }

html, body {
    margin: 0;
    padding: 0;
    background: #f8efd9;
    color: #39343b;
    font-family: Arial, sans-serif;
}

.game {
    max-width: 650px;
    width: 100%;
    margin: auto;
    padding: 12px 5px 20px;
}

.header {
    position: relative;
    text-align: center;
    margin-bottom: 8px;
}

.title {
    font-size: clamp(27px, 5vw, 38px);
    font-weight: 800;
    margin: 0;
}

.subtitle {
    color: #a08b70;
    font-size: 13px;
    margin-top: 6px;
}

.sound-button {
    position: absolute;
    right: 0;
    top: 0;
    border: 1px solid #dfcba6;
    background: #fff8e9;
    color: #755b3b;
    border-radius: 50%;
    width: 38px;
    height: 38px;
    font-size: 18px;
    cursor: pointer;
}

.board {
    width: 100%;
    display: block;
    margin: 0 auto;
    touch-action: manipulation;
}

.tile {
    cursor: pointer;
    outline: none;
}

.tile polygon {
    transition: fill 0.25s ease;
}

.tile:hover polygon:first-child {
    stroke: #ffffff;
    stroke-width: 4;
}

.tile:focus polygon:first-child {
    stroke: #448eaf;
    stroke-width: 4;
}

.flow-line {
    stroke-dasharray: 5 10;
    animation: flow 1s linear infinite;
    pointer-events: none;
}

@keyframes flow {
    to { stroke-dashoffset: -30; }
}

.hint-ring {
    fill: none;
    stroke: #f3a94e;
    stroke-width: 3;
    stroke-dasharray: 5 4;
    animation: pulse 1.2s ease-in-out infinite;
    pointer-events: none;
}

.hint-hand {
    font-size: 29px;
    animation: tap 0.8s ease-in-out infinite alternate;
    pointer-events: none;
}

@keyframes pulse {
    0%, 100% { opacity: 0.45; r: 23; }
    50% { opacity: 1; r: 28; }
}

@keyframes tap {
    from { transform: translateY(0); }
    to { transform: translateY(6px); }
}

.stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin: 8px 0 12px;
}

.stat {
    background: rgba(255,255,255,0.36);
    border: 1px solid #e7d7b8;
    border-radius: 12px;
    padding: 12px 15px;
}

.stat-label {
    color: #8d765b;
    font-size: 12px;
    margin-bottom: 5px;
}

.stat-value {
    font-size: 26px;
    font-weight: 700;
}

.reset {
    width: 100%;
    border: 1px solid #d5b77e;
    background: #f0dfbd;
    color: #61492e;
    border-radius: 10px;
    padding: 11px;
    font-size: 14px;
    cursor: pointer;
}

.reset:hover, .sound-button:hover {
    background: #e5d0a6;
}

.message {
    text-align: center;
    color: #528047;
    font-size: 14px;
    font-weight: bold;
    min-height: 20px;
    margin-top: 8px;
}

.celebration {
    display: none;
    position: fixed;
    inset: 0;
    z-index: 100;
    background: rgba(48, 48, 42, 0.48);
    align-items: center;
    justify-content: center;
    padding: 18px;
}

.celebration.show {
    display: flex;
}

.win-card {
    position: relative;
    z-index: 2;
    width: 100%;
    max-width: 330px;
    background: #fff7e5;
    border: 2px solid #e6c985;
    border-radius: 22px;
    padding: 28px 20px;
    text-align: center;
    box-shadow: 0 12px 40px #44331f35;
    animation: pop 0.4s ease-out;
}

@keyframes pop {
    from { transform: scale(.7); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

.win-plant {
    font-size: 54px;
    margin-bottom: 8px;
}

.win-title {
    font-size: 25px;
    font-weight: 800;
    color: #427b3c;
    margin-bottom: 10px;
}

.win-description {
    color: #806b4e;
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 20px;
}

.play-again {
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    background: #77a957;
    color: white;
    font-size: 15px;
    font-weight: bold;
    cursor: pointer;
}

.confetti {
    position: fixed;
    z-index: 1;
    top: -15px;
    width: 9px;
    height: 13px;
    animation: fall 2.8s linear forwards;
    pointer-events: none;
}

@keyframes fall {
    to { transform: translateY(110vh) rotate(720deg); opacity: 0; }
}

@media (max-width: 420px) {
    .game { padding-left: 0; padding-right: 0; }
    .stat { padding: 10px; }
}
</style>
</head>

<body>
<div class="game">
    <div class="header">
        <h1 class="title">🌵 Desert Bloom</h1>
        <div class="subtitle">A little water. A new life.</div>
        <button id="soundButton" class="sound-button"
                aria-label="Toggle music and sound"
                title="Toggle music and sound">♫</button>
    </div>

    <svg id="board" class="board"
         viewBox="0 0 500 470"
         xmlns="http://www.w3.org/2000/svg"
         aria-label="Desert water channel puzzle"></svg>

    <div class="stats">
        <div class="stat">
            <div class="stat-label">Moves</div>
            <div class="stat-value" id="moves">0</div>
        </div>
        <div class="stat">
            <div class="stat-label">Plants watered</div>
            <div class="stat-value" id="plantCount">0 / 2</div>
        </div>
    </div>

    <button class="reset" id="reset">↻ Reset</button>
    <div class="message" id="message"></div>
</div>

<div id="celebration" class="celebration">
    <div class="win-card">
        <div class="win-plant">🌱 🌿</div>
        <div class="win-title">Desert Bloom!</div>
        <div class="win-description">
            Both little plants are alive again.<br>
            Your water has brought life to the desert!
        </div>
        <button class="play-again" id="playAgain">
            Play again
        </button>
    </div>
</div>

<script>
"use strict";

// --------------------------------------------------
// 1. HEXAGON MAP: 19 tiles in a honeycomb.
// Axial coordinates form a hexagonal cluster.
// --------------------------------------------------

const R = 46;
const SQRT3 = Math.sqrt(3);

const START = "-2,0";
const GOALS = ["2,-1", "2,0"];

const DIRECTIONS = [
    [1, 0],
    [0, 1],
    [-1, 1],
    [-1, 0],
    [0, -1],
    [1, -1]
];

const cells = [];

for (let q = -2; q <= 2; q++) {
    for (let r = -2; r <= 2; r++) {
        if (Math.abs(q + r) <= 2) {
            cells.push({q, r, key: `${q},${r}`});
        }
    }
}

const cellKeys = new Set(cells.map(c => c.key));

function neighbour(key, direction) {
    const [q, r] = key.split(",").map(Number);
    const [dq, dr] = DIRECTIONS[direction];
    return `${q + dq},${r + dr}`;
}

function opposite(direction) {
    return (direction + 3) % 6;
}

// --------------------------------------------------
// 2. CREATE A SOLVABLE WATER NETWORK.
// The solved network connects the source to both plants.
// --------------------------------------------------

function createSolutionMasks() {
    const masks = {};

    for (const cell of cells) {
        masks[cell.key] = [];
    }

    const visited = new Set([START]);
    const queue = [START];

    while (queue.length > 0) {
        const key = queue.shift();

        for (let d = 0; d < 6; d++) {
            const next = neighbour(key, d);

            if (!cellKeys.has(next) || visited.has(next)) {
                continue;
            }

            visited.add(next);
            queue.push(next);

            masks[key].push(d);
            masks[next].push(opposite(d));
        }
    }

    return masks;
}

const SOLUTION_MASKS = createSolutionMasks();

// Each tile starts rotated away from the solution.
// A click rotates it by 60 degrees.
let turns = {};
let moves = 0;
let soundOn = true;
let audioContext = null;
let musicTimer = null;
let musicIndex = 0;
let previousGoals = null;
let victoryShown = false;

// --------------------------------------------------
// 3. SOUND: generated with Web Audio, no audio files.
// Browsers require a user gesture before playing audio.
// --------------------------------------------------

function ensureAudio() {
    try {
        if (!audioContext) {
            const AudioClass =
                window.AudioContext || window.webkitAudioContext;

            if (!AudioClass) return false;
            audioContext = new AudioClass();
        }

        if (audioContext.state === "suspended") {
            audioContext.resume();
        }

        return true;
    } catch (error) {
        return false;
    }
}

function tone(frequency, duration, volume, type = "sine", delay = 0) {
    if (!soundOn || !audioContext) return;

    try {
        const start = audioContext.currentTime + delay;
        const oscillator = audioContext.createOscillator();
        const gain = audioContext.createGain();

        oscillator.type = type;
        oscillator.frequency.setValueAtTime(frequency, start);

        gain.gain.setValueAtTime(0.0001, start);
        gain.gain.linearRampToValueAtTime(
            volume, start + 0.025
        );
        gain.gain.exponentialRampToValueAtTime(
            0.0001, start + duration
        );

        oscillator.connect(gain);
        gain.connect(audioContext.destination);

        oscillator.start(start);
        oscillator.stop(start + duration + 0.02);
    } catch (error) {
        // Sound is optional; the puzzle still works without it.
    }
}

function startMusic() {
    if (!soundOn || musicTimer !== null) return;
    if (!ensureAudio()) return;

    const melody = [
        261.63, 329.63, 392.00, 329.63,
        293.66, 349.23, 440.00, 349.23,
        261.63, 329.63, 392.00, 523.25,
        440.00, 392.00, 329.63, 293.66
    ];

    musicTimer = setInterval(() => {
        if (!soundOn || !audioContext) return;

        const note = melody[musicIndex % melody.length];
        tone(note, 0.34, 0.012, "sine");
        musicIndex++;

    }, 440);
}

function stopMusic() {
    if (musicTimer !== null) {
        clearInterval(musicTimer);
        musicTimer = null;
    }
}

function clickSound() {
    tone(480, 0.09, 0.035, "triangle");
}

function waterSound() {
    tone(660, 0.16, 0.045, "sine");
    tone(880, 0.22, 0.035, "sine", 0.10);
}

function winSound() {
    [523.25, 659.25, 783.99, 1046.5].forEach(
        (note, i) => tone(note, 0.42, 0.045, "sine", i * 0.13)
    );
}

const soundButton = document.getElementById("soundButton");

function updateSoundButton() {
    soundButton.textContent = soundOn ? "♫" : "♪̸";
    soundButton.style.opacity = soundOn ? "1" : "0.55";
}

soundButton.addEventListener("click", () => {
    soundOn = !soundOn;

    if (soundOn) {
        ensureAudio();
        startMusic();
        clickSound();
    } else {
        stopMusic();
    }

    updateSoundButton();
});

// --------------------------------------------------
// 4. ROTATION AND WATER CONNECTION.
// Turns = 0 is the correct orientation.
// --------------------------------------------------

function openings(key) {
    return SOLUTION_MASKS[key].map(
        direction => (direction + turns[key]) % 6
    );
}

function findWater() {
    const reached = new Set([START]);
    const stack = [START];

    while (stack.length > 0) {
        const key = stack.pop();

        for (const direction of openings(key)) {
            const next = neighbour(key, direction);

            if (!cellKeys.has(next) || reached.has(next)) {
                continue;
            }

            if (openings(next).includes(opposite(direction))) {
                reached.add(next);
                stack.push(next);
            }
        }
    }

    return reached;
}

// --------------------------------------------------
// 5. SVG DRAWING HELPERS.
// Neighbouring hexagons touch edge-to-edge.
// --------------------------------------------------

const board = document.getElementById("board");

function svgElement(name, attributes = {}) {
    const el = document.createElementNS(
        "http://www.w3.org/2000/svg", name
    );

    for (const [key, value] of Object.entries(attributes)) {
        el.setAttribute(key, value);
    }

    return el;
}

function center(key) {
    const [q, r] = key.split(",").map(Number);

    return {
        x: 250 + R * 1.5 * q,
        y: 235 + R * SQRT3 * (r + q / 2)
    };
}

function vertices(cx, cy) {
    const result = [];

    for (let i = 0; i < 6; i++) {
        const angle = i * Math.PI / 3;

        result.push([
            cx + R * Math.cos(angle),
            cy + R * Math.sin(angle)
        ]);
    }

    return result;
}

function edgePoint(cx, cy, direction) {
    const angle = (30 + direction * 60) * Math.PI / 180;
    const distance = SQRT3 * R / 2;

    return {
        x: cx + distance * Math.cos(angle),
        y: cy + distance * Math.sin(angle)
    };
}

function addPlant(group, cx, cy, alive) {
    const leafColor = alive ? "#65b34b" : "#b4ad70";
    const stemColor = alive ? "#367c37" : "#9b925c";

    group.appendChild(svgElement("path", {
        d: `M ${cx} ${cy+22} L ${cx} ${cy-8}
            M ${cx} ${cy+8} L ${cx-16} ${cy-2}
            M ${cx} ${cy} L ${cx+17} ${cy-12}`,
        fill: "none",
        stroke: stemColor,
        "stroke-width": 5.5,
        "stroke-linecap": "round",
        "pointer-events": "none"
    }));

    group.appendChild(svgElement("ellipse", {
        cx: cx - 16,
        cy: cy - 3,
        rx: alive ? 12 : 10,
        ry: 6,
        transform: `rotate(30 ${cx-16} ${cy-3})`,
        fill: leafColor,
        "pointer-events": "none"
    }));

    group.appendChild(svgElement("ellipse", {
        cx: cx + 17,
        cy: cy - 13,
        rx: alive ? 12 : 10,
        ry: 6,
        transform: `rotate(-30 ${cx+17} ${cy-13})`,
        fill: leafColor,
        "pointer-events": "none"
    }));

    if (alive) {
        group.appendChild(svgElement("ellipse", {
            cx: cx,
            cy: cy - 16,
            rx: 7,
            ry: 11,
            fill: "#83c957",
            "pointer-events": "none"
        }));
    }
}

function addSource(group, cx, cy) {
    group.appendChild(svgElement("circle", {
        cx, cy, r: 17,
        fill: "#f1fbff",
        stroke: "#358eb8",
        "stroke-width": 3,
        "pointer-events": "none"
    }));

    group.appendChild(svgElement("path", {
        d: `M ${cx} ${cy-13}
            C ${cx-6} ${cy-3}, ${cx-11} ${cy+3}, ${cx-11} ${cy+7}
            A 11 11 0 0 0 ${cx+11} ${cy+7}
            C ${cx+11} ${cy+3}, ${cx+6} ${cy-3}, ${cx} ${cy-13} Z`,
        fill: "#38aee8",
        "pointer-events": "none"
    }));
}

function drawTile(cell, reached) {
    const {key} = cell;
    const {x: cx, y: cy} = center(key);
    const isWet = reached.has(key);

    const isPlant = GOALS.includes(key);
    const isSource = key === START;
    const alive = isPlant && isWet;

    const group = svgElement("g", {
        class: "tile",
        tabindex: "0",
        role: "button",
        "aria-label": `Rotate channel ${key}`,
        "data-key": key
    });

    const pointString = vertices(cx, cy)
        .map(p => `${p[0]},${p[1]}`)
        .join(" ");

    group.appendChild(svgElement("polygon", {
        points: pointString,
        fill: isWet ? "#b8dce5" : "#e8d3a5",
        stroke: "#fff8e9",
        "stroke-width": 3,
        "stroke-linejoin": "round"
    }));

    const innerString = vertices(cx, cy)
        .map(p => {
            const ix = cx + (p[0] - cx) * 0.86;
            const iy = cy + (p[1] - cy) * 0.86;
            return `${ix},${iy}`;
        })
        .join(" ");

    group.appendChild(svgElement("polygon", {
        points: innerString,
        fill: "none",
        stroke: isWet ? "#80bdcb" : "#d4bc8a",
        "stroke-width": 1.3,
        "pointer-events": "none"
    }));

    // A tile may contain a straight pipe, a bend, or a junction.
    // Each opening connects to the centre.
    let pathData = "";

    for (const direction of openings(key)) {
        const p = edgePoint(cx, cy, direction);
        pathData += `M ${p.x} ${p.y} L ${cx} ${cy} `;
    }

    group.appendChild(svgElement("path", {
        d: pathData,
        fill: "none",
        stroke: isWet ? "#3586a9" : "#b49a6b",
        "stroke-width": 17,
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "pointer-events": "none"
    }));

    group.appendChild(svgElement("path", {
        d: pathData,
        fill: "none",
        stroke: isWet ? "#6acde9" : "#d6bf90",
        "stroke-width": 9,
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "pointer-events": "none"
    }));

    if (isWet) {
        group.appendChild(svgElement("path", {
            d: pathData,
            class: "flow-line",
            fill: "none",
            stroke: "#effcff",
            "stroke-width": 2.3,
            "stroke-linecap": "round",
            "pointer-events": "none"
        }));
    }

    if (isSource) {
        addSource(group, cx, cy);
    }

    if (isPlant) {
        addPlant(group, cx, cy, alive);
    }

    return group;
}

// --------------------------------------------------
// 6. FINGER HINT AND SUCCESS CELEBRATION
// --------------------------------------------------

function addFingerHint() {
    const cell = cells.find(c => c.key === "0,0");
    const {x, y} = center(cell.key);

    const hint = svgElement("g", {
        "pointer-events": "none",
        id: "fingerHint"
    });

    hint.appendChild(svgElement("circle", {
        cx: x, cy: y, r: 24,
        class: "hint-ring"
    }));

    const hand = svgElement("text", {
        x: x + 20,
        y: y - 18,
        class: "hint-hand",
        "font-family": "Arial, sans-serif"
    });

    hand.textContent = "👆";
    hint.appendChild(hand);
    board.appendChild(hint);
}

function makeConfetti() {
    const colors = [
        "#79ad55", "#e8b75f", "#5cb6d4",
        "#e68d5c", "#c5a5d9"
    ];

    for (let i = 0; i < 45; i++) {
        const piece = document.createElement("div");
        piece.className = "confetti";
        piece.style.left = Math.random() * 100 + "%";
        piece.style.background =
            colors[Math.floor(Math.random() * colors.length)];
        piece.style.animationDelay = Math.random() * 0.8 + "s";
        piece.style.transform =
            `rotate(${Math.random() * 360}deg)`;

        document.body.appendChild(piece);

        setTimeout(() => piece.remove(), 4000);
    }
}

function showVictory() {
    if (victoryShown) return;

    victoryShown = true;

    document.getElementById("celebration").classList.add("show");
    makeConfetti();

    if (soundOn) {
        ensureAudio();
        winSound();
    }
}

// --------------------------------------------------
// 7. UPDATE GAME
// --------------------------------------------------

const movesText = document.getElementById("moves");
const plantCountText = document.getElementById("plantCount");
const message = document.getElementById("message");

function render() {
    const reached = findWater();
    const watered = GOALS.filter(key => reached.has(key)).length;

    board.replaceChildren();

    for (const cell of cells) {
        board.appendChild(drawTile(cell, reached));
    }

    if (moves === 0) {
        addFingerHint();
    }

    movesText.textContent = moves;
    plantCountText.textContent = `${watered} / 2`;

    message.textContent = watered === 1
        ? "One little plant is blooming!"
        : "";

    const currentGoals = GOALS.map(key => reached.has(key));

    if (previousGoals !== null && moves > 0) {
        const newlyWatered = currentGoals.some(
            (value, i) => value && !previousGoals[i]
        );

        if (newlyWatered && soundOn) {
            waterSound();
        }
    }

    previousGoals = currentGoals;

    if (watered === 2 && moves > 0) {
        message.textContent = "Both plants are alive again!";
        showVictory();
    }
}

// --------------------------------------------------
// 8. CLICK A HEXAGON TO ROTATE IT
// No separate rotate buttons.
// --------------------------------------------------

function activateAudio() {
    if (soundOn) {
        ensureAudio();
        startMusic();
    }
}

board.addEventListener("click", event => {
    const tile = event.target.closest(".tile");

    if (!tile) return;

    activateAudio();

    const key = tile.getAttribute("data-key");

    turns[key] = (turns[key] + 1) % 6;
    moves++;

    if (soundOn) {
        clickSound();
    }

    render();
});

board.addEventListener("keydown", event => {
    if (event.key !== "Enter" && event.key !== " ") return;

    const tile = event.target.closest(".tile");

    if (!tile) return;

    event.preventDefault();
    activateAudio();

    const key = tile.getAttribute("data-key");

    turns[key] = (turns[key] + 1) % 6;
    moves++;

    if (soundOn) {
        clickSound();
    }

    render();
});

// --------------------------------------------------
// 9. RESET
// --------------------------------------------------

function resetGame() {
    turns = {};

    for (const cell of cells) {
        const {q, r, key} = cell;

        // Deterministic scrambled starting orientation.
        turns[key] = ((q + 2) * 7 + (r + 2) * 3) % 5 + 1;
    }

    moves = 0;
    victoryShown = false;
    previousGoals = null;

    document.getElementById("celebration").classList.remove("show");

    document.querySelectorAll(".confetti").forEach(
        el => el.remove()
    );

    // Ensure both plants are not already watered at the start.
    for (let i = 0; i < 6; i++) {
        const reached = findWater();

        if (!GOALS.every(key => reached.has(key))) {
            break;
        }

        turns[GOALS[0]] = (turns[GOALS[0]] + 1) % 6;
    }

    render();
}

document.getElementById("reset").addEventListener("click", () => {
    activateAudio();
    resetGame();
});

document.getElementById("playAgain").addEventListener("click", () => {
    resetGame();
    activateAudio();
});

// Start with a scrambled board.
updateSoundButton();
resetGame();

</script>
</body>
</html>
"""

components.html(
    GAME_HTML,
    height=820,
    scrolling=False
)
