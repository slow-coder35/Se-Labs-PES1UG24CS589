"""Small, optional sound-effect manager for the game."""

from pathlib import Path
import pygame


class AudioManager:
    """Load and play local effects without making audio a gameplay dependency."""

    VOLUME = 0.35

    def __init__(self, asset_dir=None):
        self.enabled = False
        self.sounds = {}

        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()

            self.enabled = pygame.mixer.get_init() is not None
            if not self.enabled:
                return

            asset_dir = Path(asset_dir) if asset_dir else Path(__file__).with_name("assets")
            for name in ("flap", "score", "death"):
                path = asset_dir / f"{name}.wav"
                try:
                    sound = pygame.mixer.Sound(str(path))
                    sound.set_volume(self.VOLUME)
                    self.sounds[name] = sound
                except (pygame.error, OSError):
                    # A missing/corrupt effect should never prevent the game starting.
                    pass
        except pygame.error:
            # Audio hardware/driver problems are non-fatal to the game.
            self.enabled = False

    def play(self, name):
        """Play one named effect; silently do nothing when audio is unavailable."""
        if not self.enabled:
            return

        sound = self.sounds.get(name)
        if sound is not None:
            try:
                sound.play()
            except pygame.error:
                # Keep gameplay functional if the audio device fails at runtime.
                pass

    def flap(self):
        self.play("flap")

    def score(self):
        self.play("score")

    def death(self):
        self.play("death")
