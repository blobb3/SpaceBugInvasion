import pygame
import cv2
import os
import numpy as np

class Explosion(pygame.sprite.Sprite):
    """A class to manage explosion animations."""

    def __init__(self, ai_game, center):
        """Initialize the explosion sprite."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the explosion frames
        video_path = os.path.join('sounds', 'explosion', 'explosion.gif')
        self.frames = self.extract_video_frames(video_path)

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.frame_index = 0
        self.animation_speed = 0.001  # Updated animation speed for faster playback

        # Load the explosion sound
        self.explosion_sound = pygame.mixer.Sound(os.path.join('sounds', 'explosion', 'explosion.wav'))
        self.explosion_sound.set_volume(0.5)  # Adjust volume as needed

        # Play the explosion sound
        self.explosion_sound.play()

    def extract_video_frames(self, video_path):
        """Extract frames from a video file with transparency."""
        frames = []
        cap = cv2.VideoCapture(video_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB (pygame uses RGB)
            frame = cv2.resize(frame, (64, 64))  # Resize frame to fit in the game

            # Create a mask for white pixels (assuming background is white)
            white_mask = np.all(frame == [255, 255, 255], axis=-1)

            # Create a new frame with an alpha channel
            alpha = np.where(white_mask, 0, 255).astype(np.uint8)
            rgba_frame = np.dstack((frame, alpha))

            # Convert to Pygame Surface
            frame_surface = pygame.image.frombuffer(rgba_frame.flatten(), (64, 64), 'RGBA')

            frames.append(frame_surface)

        cap.release()
        return frames

    def update(self, dt, fleet_direction):
        """Update the explosion animation."""
        self.rect.x += fleet_direction * self.settings.alien_speed * dt
        self.image = self.frames[self.frame_index]
        self.frame_index += 1
        if self.frame_index >= len(self.frames):
            self.kill()
