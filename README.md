# Sequence Memory Game

A memory game where you need to remember and recreate a sequence of numbers.

## Game Description

The game shows you a sequence of numbers, then shows them again in a different order. Your task is to remember and recreate the original sequence.

## Requirements

- Python 3.x
- Pygame

## Installation

1. Install Python (if you don't have it already):

   - Download Python[https://www.python.org/downloads/]
   - During installation, make sure to check "Add Python to PATH"
   - Verify installation by opening a terminal and typing `python --version`

2. Clone this repository:

```bash
git clone https://github.com/Linneaeas/game_assignment
```

3. Install the required dependencies:

```bash
pip install pygame
```

## How to Play

1. Run the game:

```bash
python main.py
```

2. Game Flow:
   - The game will show you a sequence of numbers, visually represented as cards starting face down.
   - The cards are flipped up one by one revealing the numbers of the sequense.
     -The cards are flipped back, and will open again one by one with the same numbers, but in a different order.
     -The cards are flipped back again and you can now make your guess.
   - Type the numbers on your keyboard in the order they appeared in the first sequence.
   - If you're correct, you win! The cards are flipped open to display the winning sequence.
   - If you're wrong, you can try again
   - Click the "Restart Game" button to start a new game

## Project Structure

- `main.py` - Main game loop and initialization
- `game.py` - Game logic and state management
- `constants.py` - Game settings and constants
- `card_image.jpg` - Card back image
