import pygame
from Core.SpriteSheet import SpriteSheet

class HealthBar():
    def __init__(self, maxHealth):
        self.maxHealth = maxHealth
        self.currentHealth = maxHealth
        ss = SpriteSheet("Assets/UI/StatusBar/health.png")
        self.fullHeart = ss.imageAt((0, 0, 674, 603), scaling=(60, 50))
        self.emptyHeart = ss.imageAt((674, 0, 674, 603), scaling=(60, 50))

    def update(self, player):
        self.currentHealth = player.entity.currentHealth

    def draw(self, screen):
        for life in range(self.maxHealth):
            if life + 1 <= self.currentHealth:
                screen.blit(self.fullHeart, (20 + life * self.fullHeart.get_rect().width, 20))
            else:
                screen.blit(self.emptyHeart, (20 + life * self.fullHeart.get_rect().width, 20))
