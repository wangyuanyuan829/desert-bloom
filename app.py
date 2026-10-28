
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

.level-label {
    display: inline-block;
    margin-top: 12px;
    padding: 5px 13px;
    border: 1px solid #e5d1a9;
    border-radius: 20px;
    color: #8c7049;
    background: #fff8e9;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 1px;
}

.sound-button {
    position: absolute;
    right: 0;
    top: 0;
    width: 38px;
    height: 38px;
    border: 1px solid #dfcba6;
    border-radius: 50%;
    background: #fff8e9;
    color: #755b3b;
    font-size: 18px;
    cursor: pointer;
}

.board {
    display: block;
    width: 100%;
    margin: 0 auto;
    touch-action: manipulation;
}

.tile {
    cursor: pointer;
    outline: none;
}

.tile:focus polygon:first-child {
    stroke: #438eaf;
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
    animation: tap .8s ease-in-out infinite alternate;
    pointer-events: none;
}

@keyframes pulse {
    0%, 100% { opacity: .45; }
    50% { opacity: 1; }
}

@keyframes tap {
    from { transform: translateY(0); }
    to { transform: translateY(6px); }
}

.stats {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 8px;
    margin: 8px 0 12px;
}

.stat {
    min-width: 0;
    padding: 10px;
    border: 1px solid #e7d7b8;
    border-radius: 12px;
    background: rgba(255,255,255,.36);
}

.stat-label {
    margin-bottom: 5px;
    color: #8d765b;
    font-size: 12px;
}

.stat-value {
    font-size: clamp(19px, 3.5vw, 26px);
    font-weight: 700;
}

.reset, .next-button, .replay-button {
    width: 100%;
    padding: 12px;
    border-radius: 10px;
    font-size: 14px;
    cursor: pointer;
}

.reset {
    border: 1px solid #d5b77e;
    background: #f0dfbd;
    color: #61492e;
}

.reset:hover { background: #e5d0a6; }

.message {
    min-height: 22px;
    margin-top: 8px;
    text-align: center;
    color: #528047;
    font-size: 14px;
    font-weight: bold;
}

.celebration {
    display: none;
    position: fixed;
    inset: 0;
    z-index: 100;
    align-items: center;
    justify-content: center;
    padding: 18px;
    background: rgba(48,48,42,.48);
}

.celebration.show { display: flex; }

.win-card {
    width: 100%;
    max-width: 340px;
    padding: 27px 22px;
    border: 2px solid #e6c985;
    border-radius: 22px;
    background: #fff7e5;
    box-shadow: 0 12px 40px #44331f35;
    text-align: center;
    animation: pop .4s ease-out;
}

@keyframes pop {
    from { transform: scale(.7); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

.win-plant {
    margin-bottom: 8px;
    font-size: 48px;
}

.win-title {
    margin-bottom: 10px;
    color: #427b3c;
    font-size: 25px;
    font-weight: 800;
}

.win-description {
    margin-bottom: 20px;
    color: #806b4e;
    font-size: 14px;
    line-height: 1.7;
}

.next-button {
    margin-bottom: 9px;
    border: none;
    background: #77a957;
    color: white;
    font-weight: bold;
}

.replay-button {
    border: 1px solid #decba6;
    background: transparent;
    color: #735b3d;
}

.confetti {
    position: fixed;
    z-index: 101;
    top: -15px;
    width: 9px;
    height: 13px;
    pointer-events: none;
    animation: fall 2.8s linear forwards;
}

@keyframes fall {
    to {
        transform: translateY(110vh) rotate(720deg);
        opacity: 0;
    }
}

@media (max-width: 480px) {
    .stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
</style>
</head>

<body>
<div class="game">
    <div class="header">
        <h1 class="title">🌵 Desert Bloom</h1>
        <div class="subtitle">A little water. A new life.</div>
        <div class="level-label" id="levelLabel">LEVEL 1 / 3</div>
        <button id="soundButton" class="sound-button"
                aria-label="Toggle music">♫</button>
    </div>

    <svg id="board" class="board"
         viewBox="0 0 500 470"
         xmlns="http://www.w3.org/2000/svg"
         aria-label="Desert irrigation puzzle"></svg>

    <div class="stats">
        <div class="stat">
            <div class="stat-label">Moves</div>
            <div class="stat-value" id="moves">0</div>
        </div>
        <div class="stat">
            <div class="stat-label">Plants watered</div>
            <div class="stat-value" id="plantCount">0 / 2</div>
        </div>
        <div class="stat">
            <div class="stat-label">Network connected</div>
            <div class="stat-value" id="networkCount">0 / 19</div>
        </div>
    </div>

    <button class="reset" id="reset">↻ Restart level</button>
    <div class="message" id="message"></div>
</div>

<div id="celebration" class="celebration">
    <div class="win-card">
        <div class="win-plant" id="winPlant">🌱 🌿</div>
        <div class="win-title" id="winTitle">Desert Bloom!</div>
        <div class="win-description" id="winDescription"></div>
        <button class="next-button" id="nextLevelButton">
            Continue to Level 2 →
        </button>
        <button class="replay-button" id="replayLevelButton">
            Replay this level
        </button>
    </div>
</div>

<script>
"use strict";

// ------------------------------------------
// THREE DIFFERENT LEVELS
// ------------------------------------------

const levels = [
    {
        name: "First Sprout",
        start: "-2,0",
        goals: ["2,-1", "2,0"],
        order: [0,1,2,3,4,5]
    },
    {
        name: "Desert Crossing",
        start: "-2,0",
        goals: ["2,0", "1,1"],
        order: [2,1,0,5,4,3]
    },
    {
        name: "Hidden Oasis",
        start: "0,-2",
        goals: ["2,0", "2,-1"],
        order: [1,3,5,0,2,4]
    }
];

let levelIndex = 0;
let START;
let GOALS;
let SOLUTION_MASKS = {};

const R = 46;
const SQRT3 = Math.sqrt(3);

const DIRECTIONS = [
    [1,0],
    [0,1],
    [-1,1],
    [-1,0],
    [0,-1],
    [1,-1]
];

// 19 connected hexagonal tiles.
const cells = [];

for (let q=-2; q<=2; q++) {
    for (let r=-2; r<=2; r++) {
        if (Math.abs(q+r)<=2) {
            cells.push({q,r,key:`${q},${r}`});
        }
    }
}

const cellKeys = new Set(cells.map(c=>c.key));

function neighbour(key,direction) {
    const [q,r] = key.split(",").map(Number);
    const [dq,dr] = DIRECTIONS[direction];
    return `${q+dq},${r+dr}`;
}

function opposite(direction) {
    return (direction+3)%6;
}

// Build a spanning network that uses every tile.
// Every tile has a correct orientation when turns[key] = 0.
function createSolutionMasks(start,order) {
    const masks = {};

    for (const cell of cells) {
        masks[cell.key] = [];
    }

    const visited = new Set([start]);
    const queue = [start];

    while (queue.length>0) {
        const key = queue.shift();

        for (const d of order) {
            const next = neighbour(key,d);

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

function setupLevel() {
    const config = levels[levelIndex];

    START = config.start;
    GOALS = config.goals;

    SOLUTION_MASKS = createSolutionMasks(
        START,
        config.order
    );

    document.getElementById("levelLabel").textContent =
        `LEVEL ${levelIndex+1} / ${levels.length} · ${config.name}`;
}

// ------------------------------------------
// SOUND: GENERATED LOCALLY IN THE BROWSER
// ------------------------------------------

let soundOn = true;
let audioContext = null;
let musicTimer = null;
let musicIndex = 0;

function ensureAudio() {
    try {
        if (!audioContext) {
            const AudioClass =
                window.AudioContext || window.webkitAudioContext;

            if (!AudioClass) return false;
            audioContext = new AudioClass();
        }

        if (audioContext.state==="suspended") {
            audioContext.resume();
        }

        return true;
    } catch (error) {
        return false;
    }
}

function tone(frequency,duration,volume,type="sine",delay=0) {
    if (!soundOn || !audioContext) return;

    try {
        const start = audioContext.currentTime+delay;
        const oscillator = audioContext.createOscillator();
        const gain = audioContext.createGain();

        oscillator.type = type;
        oscillator.frequency.setValueAtTime(frequency,start);

        gain.gain.setValueAtTime(0.0001,start);
        gain.gain.linearRampToValueAtTime(volume,start+0.025);
        gain.gain.exponentialRampToValueAtTime(
            0.0001,start+duration
        );

        oscillator.connect(gain);
        gain.connect(audioContext.destination);

        oscillator.start(start);
        oscillator.stop(start+duration+0.02);
    } catch (error) {
        // Sound is optional.
    }
}

function startMusic() {
    if (!soundOn || musicTimer!==null) return;
    if (!ensureAudio()) return;

    const melody = [
        261.63,329.63,392.00,329.63,
        293.66,349.23,440.00,349.23,
        261.63,329.63,392.00,523.25,
        440.00,392.00,329.63,293.66
    ];

    musicTimer = setInterval(()=>{
        if (!soundOn || !audioContext) return;

        tone(melody[musicIndex%melody.length],
             0.34,0.012,"sine");

        musicIndex++;
    },440);
}

function stopMusic() {
    if (musicTimer!==null) {
        clearInterval(musicTimer);
        musicTimer = null;
    }
}

function activateAudio() {
    if (soundOn) {
        ensureAudio();
        startMusic();
    }
}

function clickSound() {
    tone(480,0.09,0.035,"triangle");
}

function waterSound() {
    tone(660,0.16,0.045,"sine");
    tone(880,0.22,0.035,"sine",0.10);
}

function winSound() {
    [523.25,659.25,783.99,1046.5].forEach(
        (note,i)=>tone(note,0.42,0.045,"sine",i*0.13)
    );
}

const soundButton = document.getElementById("soundButton");

function updateSoundButton() {
    soundButton.textContent = soundOn ? "♫" : "♪̸";
    soundButton.style.opacity = soundOn ? "1" : "0.55";
}

soundButton.addEventListener("click",()=>{
    soundOn = !soundOn;

    if (soundOn) {
        activateAudio();
        clickSound();
    } else {
        stopMusic();
    }

    updateSoundButton();
});

// ------------------------------------------
// WATER CONNECTION LOGIC
// ------------------------------------------

let turns = {};
let moves = 0;
let victoryShown = false;
let previousGoals = null;

function openings(key) {
    return SOLUTION_MASKS[key].map(
        d=>(d+turns[key])%6
    );
}

function findWater() {
    const reached = new Set([START]);
    const stack = [START];

    while (stack.length>0) {
        const key = stack.pop();

        for (const d of openings(key)) {
            const next = neighbour(key,d);

            if (!cellKeys.has(next) || reached.has(next)) {
                continue;
            }

            if (openings(next).includes(opposite(d))) {
                reached.add(next);
                stack.push(next);
            }
        }
    }

    return reached;
}

// ------------------------------------------
// DRAW HEXAGON ARTWORK
// ------------------------------------------

const board = document.getElementById("board");

function svgElement(name,attributes={}) {
    const el = document.createElementNS(
        "http://www.w3.org/2000/svg",name
    );

    for (const [key,value] of Object.entries(attributes)) {
        el.setAttribute(key,value);
    }

    return el;
}

function center(key) {
    const [q,r] = key.split(",").map(Number);

    return {
        x:250+R*1.5*q,
        y:235+R*SQRT3*(r+q/2)
    };
}

function vertices(cx,cy) {
    const result = [];

    for (let i=0;i<6;i++) {
        const angle = i*Math.PI/3;

        result.push([
            cx+R*Math.cos(angle),
            cy+R*Math.sin(angle)
        ]);
    }

    return result;
}

function edgePoint(cx,cy,direction) {
    const angle = (30+direction*60)*Math.PI/180;
    const distance = SQRT3*R/2;

    return {
        x:cx+distance*Math.cos(angle),
        y:cy+distance*Math.sin(angle)
    };
}

function addSource(group,cx,cy) {
    group.appendChild(svgElement("circle",{
        cx,cy,r:17,
        fill:"#f1fbff",
        stroke:"#358eb8",
        "stroke-width":3,
        "pointer-events":"none"
    }));

    group.appendChild(svgElement("path",{
        d:`M ${cx} ${cy-13}
           C ${cx-6} ${cy-3}, ${cx-11} ${cy+3},
             ${cx-11} ${cy+7}
           A 11 11 0 0 0 ${cx+11} ${cy+7}
           C ${cx+11} ${cy+3}, ${cx+6} ${cy-3},
             ${cx} ${cy-13} Z`,
        fill:"#38aee8",
        "pointer-events":"none"
    }));
}

function addPlant(group,cx,cy,alive) {
    const leaf = alive ? "#65b34b" : "#b4ad70";
    const stem = alive ? "#367c37" : "#9b925c";

    group.appendChild(svgElement("path",{
        d:`M ${cx} ${cy+22} L ${cx} ${cy-8}
           M ${cx} ${cy+8} L ${cx-16} ${cy-2}
           M ${cx} ${cy} L ${cx+17} ${cy-12}`,
        fill:"none",
        stroke:stem,
        "stroke-width":5.5,
        "stroke-linecap":"round",
        "pointer-events":"none"
    }));

    group.appendChild(svgElement("ellipse",{
        cx:cx-16,cy:cy-3,rx:10,ry:6,
        transform:`rotate(30 ${cx-16} ${cy-3})`,
        fill:leaf,
        "pointer-events":"none"
    }));

    group.appendChild(svgElement("ellipse",{
        cx:cx+17,cy:cy-13,rx:10,ry:6,
        transform:`rotate(-30 ${cx+17} ${cy-13})`,
        fill:leaf,
        "pointer-events":"none"
    }));

    if (alive) {
        group.appendChild(svgElement("ellipse",{
            cx,cy:cy-16,rx:7,ry:11,
            fill:"#83c957",
            "pointer-events":"none"
        }));
    }
}

function drawTile(cell,reached) {
    const key = cell.key;
    const {x:cx,y:cy} = center(key);

    const wet = reached.has(key);
    const isPlant = GOALS.includes(key);
    const isSource = key===START;
    const alive = isPlant && wet;

    const group = svgElement("g",{
        class:"tile",
        tabindex:"0",
        role:"button",
        "aria-label":`Rotate channel ${key}`,
        "data-key":key
    });

    const points = vertices(cx,cy)
        .map(p=>`${p[0]},${p[1]}`).join(" ");

    group.appendChild(svgElement("polygon",{
        points,
        fill:wet ? "#b8dce5" : "#e8d3a5",
        stroke:"#fff8e9",
        "stroke-width":3,
        "stroke-linejoin":"round"
    }));

    const inner = vertices(cx,cy)
        .map(p=>{
            const ix=cx+(p[0]-cx)*0.86;
            const iy=cy+(p[1]-cy)*0.86;
            return `${ix},${iy}`;
        }).join(" ");

    group.appendChild(svgElement("polygon",{
        points:inner,
        fill:"none",
        stroke:wet ? "#80bdcb" : "#d4bc8a",
        "stroke-width":1.3,
        "pointer-events":"none"
    }));

    let path = "";

    for (const d of openings(key)) {
        const p = edgePoint(cx,cy,d);
        path += `M ${p.x} ${p.y} L ${cx} ${cy} `;
    }

    group.appendChild(svgElement("path",{
        d:path,
        fill:"none",
        stroke:wet ? "#3586a9" : "#b49a6b",
        "stroke-width":17,
        "stroke-linecap":"round",
        "stroke-linejoin":"round",
        "pointer-events":"none"
    }));

    group.appendChild(svgElement("path",{
        d:path,
        fill:"none",
        stroke:wet ? "#6acde9" : "#d6bf90",
        "stroke-width":9,
        "stroke-linecap":"round",
        "stroke-linejoin":"round",
        "pointer-events":"none"
    }));

    if (wet) {
        group.appendChild(svgElement("path",{
            d:path,
            class:"flow-line",
            fill:"none",
            stroke:"#effcff",
            "stroke-width":2.3,
            "stroke-linecap":"round",
            "pointer-events":"none"
        }));
    }

    if (isSource) addSource(group,cx,cy);
    if (isPlant) addPlant(group,cx,cy,alive);

    return group;
}

// ------------------------------------------
// FIRST-CLICK HAND HINT
// ------------------------------------------

function addFingerHint() {
    const cell = cells.find(c=>c.key==="0,0");
    const {x,y} = center(cell.key);

    const hint = svgElement("g",{
        "pointer-events":"none",
        id:"fingerHint"
    });

    hint.appendChild(svgElement("circle",{
        cx:x,cy:y,r:24,
        class:"hint-ring"
    }));

    const hand = svgElement("text",{
        x:x+20,y:y-18,
        class:"hint-hand",
        "font-family":"Arial, sans-serif"
    });

    hand.textContent="👆";
    hint.appendChild(hand);
    board.appendChild(hint);
}

function makeConfetti() {
    const colors=[
        "#79ad55","#e8b75f","#5cb6d4",
        "#e68d5c","#c5a5d9"
    ];

    for (let i=0;i<45;i++) {
        const piece=document.createElement("div");

        piece.className="confetti";
        piece.style.left=Math.random()*100+"%";
        piece.style.background=
            colors[Math.floor(Math.random()*colors.length)];
        piece.style.animationDelay=Math.random()*0.8+"s";

        document.body.appendChild(piece);

        setTimeout(()=>piece.remove(),4000);
    }
}

// ------------------------------------------
// VICTORY AND LEVEL PROGRESSION
// ------------------------------------------

function showVictory() {
    if (victoryShown) return;

    victoryShown=true;

    const finalLevel=levelIndex===levels.length-1;

    document.getElementById("winPlant").textContent=
        finalLevel ? "🌵 🌸 🌿" : "🌱 🌿";

    document.getElementById("winTitle").textContent=
        finalLevel ? "All Levels Complete!" : "Desert Bloom!";

    document.getElementById("winDescription").textContent=
        finalLevel
        ? "You restored every channel and brought life back to the entire desert!"
        : `Level ${levelIndex+1} complete! Every channel is connected and both plants are alive!`;

    document.getElementById("nextLevelButton").textContent=
        finalLevel ? "Play from Level 1 ↻" :
        `Continue to Level ${levelIndex+2} →`;

    document.getElementById("celebration")
        .classList.add("show");

    makeConfetti();

    if (soundOn) {
        ensureAudio();
        winSound();
    }
}

function goToNextLevel() {
    activateAudio();

    if (levelIndex<levels.length-1) {
        levelIndex++;
    } else {
        levelIndex=0;
    }

    setupLevel();
    resetGame();
}

document.getElementById("nextLevelButton")
    .addEventListener("click",goToNextLevel);

document.getElementById("replayLevelButton")
    .addEventListener("click",()=>{
        activateAudio();
        resetGame();
    });

// ------------------------------------------
// MAIN RENDER AND VICTORY CONDITION
// ------------------------------------------

const movesText=document.getElementById("moves");
const plantCountText=document.getElementById("plantCount");
const networkCountText=document.getElementById("networkCount");
const message=document.getElementById("message");

function render() {
    const reached=findWater();

    const watered=GOALS.filter(
        key=>reached.has(key)
    ).length;

    board.replaceChildren();

    for (const cell of cells) {
        board.appendChild(drawTile(cell,reached));
    }

    if (moves===0) addFingerHint();

    movesText.textContent=moves;
    plantCountText.textContent=`${watered} / 2`;
    networkCountText.textContent=`${reached.size} / ${cells.length}`;

    if (watered===1) {
        message.textContent="One little plant is blooming!";
    } else {
        message.textContent="";
    }

    const currentGoals=GOALS.map(
        key=>reached.has(key)
    );

    if (previousGoals!==null && moves>0) {
        const newlyWatered=currentGoals.some(
            (value,i)=>value && !previousGoals[i]
        );

        if (newlyWatered && soundOn) waterSound();
    }

    previousGoals=currentGoals;

    // ALL 19 tiles must be connected, and both plants watered.
    if (
        watered===2 &&
        reached.size===cells.length &&
        moves>0
    ) {
        message.textContent="The entire desert is blooming!";
        showVictory();
    } else if (watered===2) {
        message.textContent=
            "Both plants are alive! Connect the remaining channels.";
    } else if (reached.size===cells.length) {
        message.textContent=
            "The network is connected. Water both plants!";
    } else {
        message.textContent=
            "Keep connecting the irrigation channels.";
    }
}

// ------------------------------------------
// CLICK A HEXAGON TO ROTATE IT
// ------------------------------------------

function rotateTile(key) {
    if (victoryShown) return;

    activateAudio();

    turns[key]=(turns[key]+1)%6;
    moves++;

    if (soundOn) clickSound();

    render();
}

board.addEventListener("click",event=>{
    const tile=event.target.closest(".tile");
    if (!tile) return;

    rotateTile(tile.getAttribute("data-key"));
});

board.addEventListener("keydown",event=>{
    if (event.key!=="Enter" && event.key!==" ") return;

    const tile=event.target.closest(".tile");
    if (!tile) return;

    event.preventDefault();
    rotateTile(tile.getAttribute("data-key"));
});

// ------------------------------------------
// RESET CURRENT LEVEL
// ------------------------------------------

function resetGame() {
    turns={};

    // Start with randomly rotated channels.
    for (const cell of cells) {
        const {q,r,key}=cell;

        turns[key]=
            ((q+2)*7+(r+2)*3+(levelIndex+1)*5)%5+1;
    }

    moves=0;
    victoryShown=false;
    previousGoals=null;

    document.getElementById("celebration")
        .classList.remove("show");

    document.querySelectorAll(".confetti").forEach(
        el=>el.remove()
    );

    // Ensure the initial board is not already a completed puzzle.
    for (let attempt=0;attempt<cells.length;attempt++) {
        const reached=findWater();

        const bothWatered=GOALS.every(
            key=>reached.has(key)
        );

        const allConnected=reached.size===cells.length;

        if (!(bothWatered && allConnected)) break;

        const key=cells[attempt].key;
        turns[key]=(turns[key]+1)%6;
    }

    render();
}

document.getElementById("reset").addEventListener("click",()=>{
    activateAudio();
    resetGame();
});

// Start the game.
updateSoundButton();
setupLevel();
resetGame();

</script>
</body>
</html>
"""

components.html(
    GAME_HTML,
    height=980,
    scrolling=True
)
