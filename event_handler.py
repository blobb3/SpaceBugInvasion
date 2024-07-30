import sys
import pygame

class EventHandler:
    def __init__(self, ai_game):
        self.ai_game = ai_game

    def check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._handle_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_events(pygame.mouse.get_pos())

    def _handle_keydown_events(self, event):
        """Handle keydown events separately for clarity and better management."""
        if event.key == pygame.K_RIGHT:
            self.ai_game.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ai_game.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.ai_game.gamemanagement.fire_bullet()
            self.ai_game.shoot_sound.play()
        elif event.key == pygame.K_q:
            sys.exit()

    def _handle_keyup_events(self, event):
        """Handle keyup events separately to manage ship's movement."""
        if event.key == pygame.K_RIGHT:
            self.ai_game.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ai_game.ship.moving_left = False

    def _handle_mouse_events(self, mouse_pos):
        """Handle mouse events, check if the play button was clicked."""
        if self.ai_game.play_button.rect.collidepoint(mouse_pos) and not self.ai_game.game_active:
            self.ai_game._start_game()
