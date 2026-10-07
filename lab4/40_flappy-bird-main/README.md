# Flappy Bird – Pygame

A small Flappy Bird implementation built with Python and Pygame. The game uses a simple object-oriented structure with separate bird, pipe, game-engine, and audio components.

## Requirements

- Python 3.10 or newer
- Pygame (listed in `requirements.txt`)
- A working graphical environment for Pygame

## Installation

From the project directory:

```bash
python -m pip install -r requirements.txt
```

If your system uses a separate Python 3 command, use `python3` instead.

## Run

```bash
python main.py
```

The game opens in a 500×700 Pygame window.

## Controls

During gameplay:

- `Space` — flap
- Mouse click — flap

Difficulty selection:

- `1` — Easy
- `2` — Medium
- `3` — Hard
- `Enter` or `Space` — start using the current/default difficulty
- `Q` or `Esc` — quit

After Game Over:

- `R` — replay the current difficulty
- `Q` or `Esc` — quit

## Difficulty Modes

Medium is the default difficulty.

| Difficulty | Pipe speed | Spawn interval | Gap | Gravity | Flap strength |
|---|---:|---:|---:|---:|---:|
| Easy | 3 | 105 frames | 190 px | 0.45 | -7.5 |
| Medium | 4 | 90 frames | 150 px | 0.50 | -8.0 |
| Hard | 5 | 75 frames | 125 px | 0.55 | -8.2 |

Higher difficulty increases pipe speed and spawn frequency, reduces the gap, and slightly changes bird physics.

The selected difficulty is shown in the gameplay HUD.

## Collision Detection

Collision detection is performed every gameplay frame. The bird uses its full bounding `pygame.Rect` rather than checking only its center point.

The bird rectangle is tested against the upper and lower pipe rectangles. The previous and current pipe rectangles are combined into a swept rectangle before collision testing, reducing the chance of a fast-moving pipe passing through the bird between frames.

The bird also loses when its bounding rectangle reaches the top or bottom of the game window.

## Game Over

A pipe or boundary collision changes the game state from `playing` to `game_over`. Gameplay updates stop while the Game Over screen is displayed, so pipes and score no longer advance.

The screen displays:

- `GAME OVER`
- Final score
- Current difficulty
- `R = Replay`
- `Q or ESC = Quit`

Keyboard input is handled while in the Game Over state. Quit events are returned to the main application loop so the Pygame window closes cleanly.

## Replay

Pressing `R` after Game Over starts a new run without restarting Python. The selected difficulty is retained and all run-specific state is reset, including:

- Bird position and velocity
- Score
- Pipe positions and scoring flags
- Pipe spawn timer
- Game state

Difficulty can be changed from the difficulty-selection screen before starting a run.

## Audio

The game includes three local WAV effects in `game/assets/`:

- `flap.wav` — played when the bird flaps
- `score.wav` — played when the bird successfully passes a pipe
- `death.wav` — played once when the player dies

Audio is managed by `game/audio_manager.py` using `pygame.mixer`. Mixer initialization and individual sound loading are handled safely. If audio cannot be initialized or an asset is unavailable, the game continues without sound; no external files are downloaded at runtime.

## Project Structure

```text
flappybird-main/
├── main.py
├── requirements.txt
├── README.md
└── game/
    ├── game_engine.py
    ├── bird.py
    ├── pipe.py
    ├── audio_manager.py
    └── assets/
        ├── flap.wav
        ├── score.wav
        └── death.wav
```

## Known Limitations

- The game requires a graphical environment capable of running Pygame.
- Audio is optional; unsupported or unavailable audio hardware disables sound without preventing gameplay.
- The game uses simple geometric graphics and does not include sprite artwork or animation.
