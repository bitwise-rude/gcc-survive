# GCC - Survive the Balls

A simple survival game created with Python and Pygame. The goal is to dodge a series of incoming balls for as long as possible, earning a high score.

***

## How to Play 🎮

The game's objective is to survive as long as you can while a "monster" character shoots projectiles at you.

### Controls 🕹️

-   **Movement:** Use the **Arrow keys** or **WASD** to move your character around the container.
-   **Speed Boost:** Hold **`LSHIFT`** to temporarily increase your movement speed.
-   **Shield:** Press **`SPACE`** to activate a temporary shield that protects you from a single hit.
-   **Restart:** After you die, press any key to return to the main menu and play again.

***

## Gameplay Mechanics 🧠

-   **Objective:** Survive as long as you can. Each projectile that goes off-screen without hitting you increases your score by one.
-   **Projectiles:** A "monster" character in the middle of the screen periodically fires projectiles at you.
-   **Lives:** You start with a set number of lives. Each time a projectile hits you and you don't have a shield active, you lose a life.
-   **Shield:** Your shield provides a single-use protection. Once a projectile hits you while your shield is active, the shield is gone.
-   **High Score:** The game keeps track of your highest score. If you beat it, a "New High Score" message will appear on the game over screen.

***

## Game Over 💀

The game ends when your character runs out of lives. The game over screen will display your final score and, if applicable, announce that you've set a new high score.

***

## Project Structure 📁

The code is structured into several files:

-   `main_game.py`: Contains the `MainGame` class, which handles the main game loop, rendering, user input, and game state.
-   `characters.py`: (Assumed, based on the `from characters import *` import) This file likely contains the classes for the game entities: `Player`, `Monster`, `Container`, and `Projectile`.
-   `menu.py`: (Assumed, based on the `from menu import *` import) This file manages the game's main menu, allowing you to start or quit the game and display the high score.
-   `Assets/`: This directory contains all the game assets, including background images, sounds, and the game icon.

***

## Technical Details ⚙️

-   **Language:** Python
-   **Library:** Pygame
-   **Dependencies:** Pygame
-   **Audio:** The game includes background music and a countdown sound effect before new waves of projectiles.

To run the game, you'll need to have Pygame installed. You can install it using pip: `pip install pygame`