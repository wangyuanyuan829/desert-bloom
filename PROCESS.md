# Desert Bloom — Process Documentation

## 1. Starting Idea

My initial idea was to create a small interactive puzzle inspired by hexagonal pipe-rotation games.

Instead of connecting electricity to light bulbs, I changed the central concept to delivering water through desert channels to withered plants. The aim was to keep the original logic-puzzle mechanic while giving the interaction a clearer theme: a small amount of water can bring life back to a dry environment.

I chose a browser-based game because it allows players to interact directly with the puzzle without installing a separate game application.

## 2. Design and Code Changes

The project was developed using Python and Streamlit.

During development, I made the following changes:

- **Direct interaction:** I changed the controls so that clicking a hexagonal tile rotates it directly, removing the need for a separate rotation button.
- **Board layout:** I adjusted the hexagonal tiles so that they form a connected board rather than separate blocks.
- **Visual feedback:** Water-connected channels are visually distinguished from dry channels, helping players understand the current state of the puzzle.
- **Plant revival:** Target plants begin in a withered state and return to life when water reaches them.
- **Progressive difficulty:** I created three levels with increasing difficulty. The final level requires the player to water three plants.
- **Clearer objective:** The player only needs to water the target plants to complete a level. Connecting every channel is not required.
- **Success and progression:** The game provides feedback when a level is completed and allows the player to continue to the next level.
- **Audio:** I added a music control and audio feedback to make the experience more engaging.

These changes were intended to make the interaction easier to understand while preserving the challenge of planning a route through the hexagonal board.

## 3. Feedback and Iteration

One important piece of feedback concerned the original win condition. Requiring the player to connect every channel would make the objective unnecessarily strict and could encourage players to focus on unused tiles instead of the plants.

I therefore changed the objective so that a level is completed when all target plants receive water. This makes the relationship between the player's actions and the goal more direct.

I also noticed during my own playtesting that some surrounding tiles were not being used meaningfully. This motivated me to improve the board layouts and increase the difficulty across the three levels.

### User Trial

The assignment requires another person to try the experience before its rules are explained.

**Complete this section after conducting that test:**

- **Test setup:** I asked one person to try the game without explaining the controls first.
- **What the player attempted:** [Describe the first action the player tried.]
- **Where the player hesitated:** [Describe any confusing tile, symbol, objective, or control.]
- **Feedback or observation:** [Record what the player actually said or did.]
- **Decision:** [Describe one improvement made in response, or explain why the existing design was retained.]

I will use this observation to evaluate whether the game's controls and feedback communicate the puzzle's objective clearly.

## 4. Use of AI Tools

I used ChatGPT as an AI-assisted development tool during the project.

Its main uses were:

- Brainstorming and refining the game concept.
- Assisting with Python and Streamlit code.
- Identifying implementation problems and suggesting debugging steps.
- Refining the interaction design and documentation.

### One Suggestion I Kept

I kept the suggestion to use a small number of progressively more difficult levels, supported by visible feedback. This made the project more substantial than a single puzzle while keeping the scope manageable for an individual assignment.

### One Suggestion I Modified

I modified the approach to puzzle completion. Rather than treating every channel as something that must be connected, I focused the objective on delivering water to the target plants. This decision followed the feedback that connecting every pipe was unnecessary and made the puzzle feel too restrictive.

AI-generated suggestions and code were reviewed and adapted during development. The final project reflects my decisions about the game's theme, controls, difficulty, and success conditions.

## 5. Reflection

This project helped me understand that an interactive experience needs more than a visual design. The user's action must produce a meaningful change, and the resulting feedback must help the user decide what to do next.

In Desert Bloom, rotating a channel changes the water connections, the connected channels show the effect of that action, and the plants provide a clear indication of progress toward the goal.

The project also taught me the importance of testing the experience rather than assuming that the rules are obvious. Feedback about the win condition led me to focus the puzzle on its main purpose: bringing water to the plants.

For future development, I would improve the clarity of the initial interaction, refine the balance of the later levels, and test the game with more players.

