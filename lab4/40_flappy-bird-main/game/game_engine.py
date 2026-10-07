import pygame
from .bird import Bird
from .pipe import Pipe

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 150, 0)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.pipe_speed = 4
        self.pipe_interval = 90  # frames between pipe spawns
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.action_font = pygame.font.SysFont("Arial", 28)

        self._reset_game()

    def _reset_game(self):
        """Reset all gameplay state for a new run."""
        self.bird = Bird(self.width // 4, self.height // 2)
        self._spawn_timer = 0
        self.pipes = [Pipe(self.width + 100, self.height, speed=self.pipe_speed)]
        self.score = 0
        self.game_over = False

    def handle_event(self, event):
        """Handle input and return 'quit' when the application should exit."""
        if self.game_over:
            # Game-over input is handled separately so normal gameplay input
            # cannot flap the bird or otherwise advance the game.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._reset_game()
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return "quit"
            return None

        # Flap is edge-triggered (KEYDOWN / MOUSEBUTTONDOWN), not held.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.bird.flap()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.bird.flap()
        return None

    def handle_input(self):
        # Reserved for continuously-held-key input; flapping is handled
        # in handle_event instead, so there's nothing to poll here.
        pass

    def update(self):
        # Gameplay is completely frozen after death. The Game Over screen
        # remains interactive through handle_event(), but nothing moves here.
        if self.game_over:
            return

        self.bird.update()

        # Check the bird's full bounding rectangle against the screen bounds.
        bird_rect = self.bird.rect()
        if bird_rect.top <= 0 or bird_rect.bottom >= self.height:
            self.game_over = True
            return

        self._spawn_timer += 1
        if self._spawn_timer >= self.pipe_interval:
            self._spawn_timer = 0
            self.pipes.append(Pipe(self.width, self.height, speed=self.pipe_speed))

        for pipe in self.pipes:
            # Keep the previous rectangles so a fast-moving pipe cannot
            # skip over the bird between two frames.
            previous_top = pipe.top_rect()
            previous_bottom = pipe.bottom_rect()
            pipe.move()
            current_top = pipe.top_rect()
            current_bottom = pipe.bottom_rect()

            # Check the bird's full hitbox against the pipe rectangles and
            # their swept areas from the previous frame to the current one.
            top_sweep = previous_top.union(current_top)
            bottom_sweep = previous_bottom.union(current_bottom)
            if bird_rect.colliderect(top_sweep) or bird_rect.colliderect(bottom_sweep):
                self.game_over = True
                return

            if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                pipe.scored = True
                self.score += 1

        self.pipes = [p for p in self.pipes if not p.off_screen()]

    def render(self, screen):
        for pipe in self.pipes:
            pygame.draw.rect(screen, GREEN, pipe.top_rect())
            pygame.draw.rect(screen, GREEN, pipe.bottom_rect())

        pygame.draw.circle(screen, WHITE, (int(self.bird.x), int(self.bird.y)), self.bird.radius)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            self._render_game_over(screen)

    def _render_game_over(self, screen):
        """Draw the final-score overlay without advancing gameplay state."""
        # Keep the existing sky-blue background and white text style while
        # adding a subtle dark overlay to separate the menu from gameplay.
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        title = self.game_over_font.render("GAME OVER", True, WHITE)
        final_score = self.font.render(f"Final Score: {self.score}", True, WHITE)
        replay = self.action_font.render("R = Replay", True, WHITE)
        quit_text = self.action_font.render("Q or ESC = Quit", True, WHITE)

        center_x = self.width // 2
        title_y = self.height // 2 - 100
        score_y = title_y + title.get_height() + 20
        replay_y = score_y + final_score.get_height() + 35
        quit_y = replay_y + replay.get_height() + 10

        screen.blit(title, title.get_rect(center=(center_x, title_y)))
        screen.blit(final_score, final_score.get_rect(center=(center_x, score_y)))
        screen.blit(replay, replay.get_rect(center=(center_x, replay_y)))
        screen.blit(quit_text, quit_text.get_rect(center=(center_x, quit_y)))
