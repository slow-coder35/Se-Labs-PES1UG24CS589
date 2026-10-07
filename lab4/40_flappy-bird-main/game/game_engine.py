import pygame
from .bird import Bird
from .pipe import Pipe
from .audio_manager import AudioManager

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 150, 0)


class GameEngine:
    DIFFICULTIES = {
        "Easy": {
            "pipe_speed": 3,
            "pipe_interval": 105,
            "gap": 190,
            "gravity": 0.45,
            "flap_strength": -7.5,
        },
        "Medium": {
            "pipe_speed": 4,
            "pipe_interval": 90,
            "gap": 150,
            "gravity": 0.5,
            "flap_strength": -8,
        },
        "Hard": {
            "pipe_speed": 5,
            "pipe_interval": 75,
            "gap": 125,
            "gravity": 0.55,
            "flap_strength": -8.2,
        },
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Medium is the default difficulty.
        self.difficulty = "Medium"
        self.settings = self.DIFFICULTIES[self.difficulty]

        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.action_font = pygame.font.SysFont("Arial", 28)
        self.menu_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 24)
        self.audio = AudioManager()

        self.game_state = "difficulty_select"
        self._reset_game()

    def _reset_game(self):
        """Reset every run-specific value using the selected difficulty."""
        self.bird = Bird(
            self.width // 4,
            self.height // 2,
            gravity=self.settings["gravity"],
            flap_strength=self.settings["flap_strength"],
        )
        self._spawn_timer = 0
        self.pipes = [
            Pipe(
                self.width + 100,
                self.height,
                gap=self.settings["gap"],
                speed=self.settings["pipe_speed"],
            )
        ]
        self.score = 0
        self.game_state = "playing"

    def _select_difficulty(self, difficulty):
        """Apply a difficulty and start a completely fresh run."""
        self.difficulty = difficulty
        self.settings = self.DIFFICULTIES[difficulty]
        self._reset_game()

    def handle_event(self, event):
        """Handle input and return 'quit' when the application should exit."""
        if event.type == pygame.KEYDOWN:
            if self.game_state == "difficulty_select":
                if event.key == pygame.K_1:
                    self._select_difficulty("Easy")
                elif event.key == pygame.K_2:
                    self._select_difficulty("Medium")
                elif event.key == pygame.K_3:
                    self._select_difficulty("Hard")
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    # Start with the default/current selection (Medium initially).
                    self._reset_game()
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return "quit"
                return None

            if self.game_state == "game_over":
                # R returns to difficulty selection so the next run can use
                # a different difficulty without restarting Python.
                if event.key == pygame.K_r:
                    self.game_state = "difficulty_select"
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return "quit"
                return None

            if self.game_state == "playing" and event.key == pygame.K_SPACE:
                self.bird.flap()
                self.audio.flap()

        if self.game_state == "playing" and event.type == pygame.MOUSEBUTTONDOWN:
            self.bird.flap()
            self.audio.flap()

        return None

    def handle_input(self):
        # Reserved for continuously-held-key input.
        pass

    def update(self):
        # Difficulty selection and Game Over are both paused states.
        if self.game_state != "playing":
            return

        self.bird.update()

        # Check the bird's full bounding rectangle against the screen bounds.
        bird_rect = self.bird.rect()
        if bird_rect.top <= 0 or bird_rect.bottom >= self.height:
            self.game_state = "game_over"
            self.audio.death()
            return

        self._spawn_timer += 1
        if self._spawn_timer >= self.settings["pipe_interval"]:
            self._spawn_timer = 0
            self.pipes.append(
                Pipe(
                    self.width,
                    self.height,
                    gap=self.settings["gap"],
                    speed=self.settings["pipe_speed"],
                )
            )

        for pipe in self.pipes:
            # Keep previous rectangles so a fast-moving pipe cannot skip over
            # the bird between two frames.
            previous_top = pipe.top_rect()
            previous_bottom = pipe.bottom_rect()
            pipe.move()
            current_top = pipe.top_rect()
            current_bottom = pipe.bottom_rect()

            top_sweep = previous_top.union(current_top)
            bottom_sweep = previous_bottom.union(current_bottom)
            if bird_rect.colliderect(top_sweep) or bird_rect.colliderect(bottom_sweep):
                self.game_state = "game_over"
                self.audio.death()
                return

            if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                pipe.scored = True
                self.score += 1
                self.audio.score()

        self.pipes = [p for p in self.pipes if not p.off_screen()]

    def render(self, screen):
        for pipe in self.pipes:
            pygame.draw.rect(screen, GREEN, pipe.top_rect())
            pygame.draw.rect(screen, GREEN, pipe.bottom_rect())

        pygame.draw.circle(screen, WHITE, (int(self.bird.x), int(self.bird.y)), self.bird.radius)

        if self.game_state == "playing":
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            difficulty_text = self.small_font.render(f"Difficulty: {self.difficulty}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(difficulty_text, (10, 45))
        elif self.game_state == "game_over":
            # Keep the final score visible behind the overlay.
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            self._render_game_over(screen)
        else:
            self._render_difficulty_select(screen)

    def _render_difficulty_select(self, screen):
        """Draw the menu used before a run and after pressing R."""
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 90))
        screen.blit(overlay, (0, 0))

        title = self.menu_font.render("SELECT DIFFICULTY", True, WHITE)
        default = self.small_font.render("Medium is the default", True, WHITE)
        easy = self.action_font.render("1 = Easy", True, WHITE)
        medium = self.action_font.render("2 = Medium", True, WHITE)
        hard = self.action_font.render("3 = Hard", True, WHITE)
        start = self.small_font.render("ENTER / SPACE = Start", True, WHITE)
        quit_text = self.small_font.render("Q or ESC = Quit", True, WHITE)

        center_x = self.width // 2
        screen.blit(title, title.get_rect(center=(center_x, 170)))
        screen.blit(default, default.get_rect(center=(center_x, 225)))
        screen.blit(easy, easy.get_rect(center=(center_x, 300)))
        screen.blit(medium, medium.get_rect(center=(center_x, 350)))
        screen.blit(hard, hard.get_rect(center=(center_x, 400)))
        screen.blit(start, start.get_rect(center=(center_x, 480)))
        screen.blit(quit_text, quit_text.get_rect(center=(center_x, 520)))

    def _render_game_over(self, screen):
        """Draw the final-score overlay without advancing gameplay state."""
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        title = self.game_over_font.render("GAME OVER", True, WHITE)
        final_score = self.font.render(f"Final Score: {self.score}", True, WHITE)
        difficulty = self.small_font.render(f"Difficulty: {self.difficulty}", True, WHITE)
        replay = self.action_font.render("R = Replay / Change Difficulty", True, WHITE)
        quit_text = self.action_font.render("Q or ESC = Quit", True, WHITE)

        center_x = self.width // 2
        title_y = self.height // 2 - 120
        score_y = title_y + title.get_height() + 15
        difficulty_y = score_y + final_score.get_height() + 10
        replay_y = difficulty_y + difficulty.get_height() + 30
        quit_y = replay_y + replay.get_height() + 10

        screen.blit(title, title.get_rect(center=(center_x, title_y)))
        screen.blit(final_score, final_score.get_rect(center=(center_x, score_y)))
        screen.blit(difficulty, difficulty.get_rect(center=(center_x, difficulty_y)))
        screen.blit(replay, replay.get_rect(center=(center_x, replay_y)))
        screen.blit(quit_text, quit_text.get_rect(center=(center_x, quit_y)))
