import pygame

class GameUpdates:
    def __init__(self, ai_game):
        self.ai_game = ai_game

    def update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.ai_game.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.ai_game.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.ai_game.bullets.remove(bullet)
        self.ai_game.gamemanagement.check_bullet_alien_collisions()

    def update_aliens(self):
        """Check if the fleet is at an edge, then update positions"""
        self.ai_game.fleet.check_fleet_edges()
        self.ai_game.aliens.update()

        # look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ai_game.ship, self.ai_game.aliens):
            print("Bug Alert! Ship infested!")
            self.ai_game.gamemanagement.ship_hit()

        # look for aliens hitting the bottom of the screen
        self.ai_game.gamemanagement.check_aliens_bottom()

    def update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.ai_game.screen.fill(self.ai_game.settings.bg_color)  # Redraw the screen during each pass through the loop 
        for bullet in self.ai_game.bullets.sprites():
            bullet.draw_bullet()
        for alien in self.ai_game.aliens.sprites():
            alien.draw() 
        self.ai_game.ship.blitme()  # Draw the ship on the screen on top of the background
        self.ai_game.aliens.draw(self.ai_game.screen)  # Make aliens appear
        self.ai_game.explosions.draw(self.ai_game.screen)  # Draw explosions

        # Draw the score information
        self.ai_game.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.ai_game.game_active:
            self.ai_game.play_button.draw_button()

        pygame.display.flip()  # Make the most recently drawn screen visible
