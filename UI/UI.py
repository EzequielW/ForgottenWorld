from UI.HealthBar import HealthBar
from UI.SpecialBar import SpecialBar

class UserInterface():
    def __init__(self, player):
        self.healthBar = HealthBar(player.entity.maxHealth)
        self.specialBar = SpecialBar()
    
    def update(self, player):
        self.healthBar.update(player)
        self.specialBar.update(player)

    def draw(self, screen):
        self.healthBar.draw(screen)
        self.specialBar.draw(screen)