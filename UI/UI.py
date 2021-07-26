import pygame
from UI.HealthBar import HealthBar
from UI.SpecialBar import SpecialBar

class UserInterface():
    def __init__(self, player, screen):
        self.healthBar = HealthBar(player.entity.maxHealth)
        self.specialBar = SpecialBar()
        font = pygame.font.Font(None, 30)
        self.restartText = font.render('RESTART GAME', True, pygame.Color('white'))
        width = self.restartText.get_rect().width
        height = self.restartText.get_rect().height
        screenWidth = screen.get_rect().width
        screenHeight = screen.get_rect().height
        self.restartButton = pygame.Rect((screenWidth/2 - width/2, screenHeight/2 - height/2), (width, height))
    
    def update(self, player):
        self.healthBar.update(player)
        self.specialBar.update(player)

    def draw(self, screen):
        self.healthBar.draw(screen)
        self.specialBar.draw(screen)
        if self.healthBar.currentHealth <= 0:
            screen.blit(self.restartText, self.restartButton)