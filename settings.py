class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the games settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (15, 15, 70)

        # Ship settings
        self.ship_speed = 1.5 # position is adjusted by 1.5 pixels

        # Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 respresents right; -1 represents left
        self.fleet_direction = 1
