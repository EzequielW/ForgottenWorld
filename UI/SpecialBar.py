import pygame
from Core.SpriteSheet import SpriteSheet

class SpecialBar():
    def __init__(self):
        ss = SpriteSheet("Assets/UI/StatusBar/special.png")
        self.emptySpecial = ss.imageAt((0, 0, 206, 28), scaling=(170, 20))
        self.fullSpecial = ss.imageAt((0, 28, 206, 28), scaling=(170, 20))
        self.percentage = 170

    def update(self, player):
        specialPercentage = (player.currentSpecial * 170) // player.maxSpecial
        self.percentage = (0, 0, specialPercentage, 28)

    def draw(self, screen):
        screen.blit(self.emptySpecial, (27, 80))
        screen.blit(self.fullSpecial, (27, 80), self.percentage)