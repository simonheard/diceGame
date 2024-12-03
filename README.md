# Dice Game 🎲

Welcome to the **Dice Game** – a strategic and fun dice-based game where you compete against an AI opponent. Roll dice, score points, and strategically use power-ups to win! This project is a personal development challenge and showcases custom-built game mechanics, an interactive GUI, and a shop system.

## Table of Contents

- [Dice Game 🎲](#dice-game-)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Game Rules](#game-rules)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
  - [How to Play](#how-to-play)
  - [Credits](#credits)
  - [License](#license)

---

## Features

- 🎲 **Dice Rolling:** Roll dice to score points, with AI opponents adding competition.
- ⚡ **Power-Ups:** Purchase and use power-ups like "Reroll Single Dice" or "Set Dice to 1".
- 🛒 **Shop System:** Earn tokens by winning games and spend them on power-ups.
- 🎵 **Background Music:** Immersive BGM created with **Suno AI**.
- 🖼️ **Custom Graphics:** Dice face images and an intuitive GUI.
- 🧠 **AI Opponents:** Different difficulty levels with unique behaviors.
- 🔄 **Game Levels:** Choose from multiple levels and multipliers for higher risks and rewards.

---

## Game Rules

1. Players roll five dice each turn to score points.
2. Power-ups can be used to modify dice rolls and enhance strategies.
3. Players (you and AI) can choose to reroll if not satisfied or stop to keep the current score.
4. When one player choose to stop, the other player has one last chance to reroll or stop.
5. The player with the highest score at the end of the game wins.
6. **Scoring combinations:**
   - 🎯 1-2-3-4-5: 130 points
   - 🎯 2-3-4-5-6: 110 points
   - if not in a straight, 1 can be used as a wild card but with deduced score.
   - 🎯 Five of a kind: 100 points + sum of dice faces
   - 🎯 Full House (3+2 same): 70 points + sum of dice faces
   - 🎯 Four of a kind: 70 points + sum of dice faces
   - 🎯 Three of a kind or Two Pairs: 40 + sum of dice faces
   - 🎯 One Pair: 10 points + sum of dice faces

---

## Installation

### Prerequisites

- Python 3.8 or higher
- `pygame` library installed

### Steps

1. Clone this repository:

   ```bash
   git clone https://github.com/simonheard/diceGame.git
   cd dice-game
   ```

2. Install dependencies:

   ```bash
   pip install pygame
   ```

3. Run the game:

   ```bash
   python main.py
   ```

---

## How to Play

1. **Start the Game:**
   Launch the game with `python main.py` and navigate the main menu.

2. **Main Menu:**
   - Play the game.
   - Open the shop to buy power-ups.
   - View game rules and credits.
   - Quit the game.

3. **Gameplay:**
   - Choose an opponent level and multiplier.
   - Roll dice to maximize your score.
   - Use power-ups strategically to gain an edge over the AI.

4. **Earn Rewards:**
   Win games to earn tokens, then spend them in the shop.

---

## Credits

- **Development:** Hede Wang
- **Background Music:** Created with [Suno AI](https://suno.ai)
- **Sound Effects:** Free online resources and custom assets
- **Special Thanks:** Python's `pygame` library and the open-source community

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to modify and use it for your projects.

---

Enjoy the game! 🎲 If you encounter any issues or have suggestions, feel free to open an issue or contact me. 😊