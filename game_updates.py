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
        self.ai_game._check_bullet_alien_collisions()

    def update_aliens(self):
        """Check if the fleet is at an edge, then update positions"""
        self.ai_game.fleet.check_fleet_edges()
        self.ai_game.aliens.update()

        # look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ai_game.ship, self.ai_game.aliens):
            print("Bug Alert! Ship infested!")
            self.ai_game._ship_hit()

        # look for aliens hitting the bottom of the screen
        self.ai_game._check_aliens_bottom()

