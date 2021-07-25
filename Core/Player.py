import pygame
import math

from Core import PlayerState

class Player(pygame.sprite.Sprite):
    def __init__(self, entity, maxSpecial):
        self.entity = entity
        self.triggerUp = False
        self.jumpCount = 0
        self.maxSpecial = maxSpecial
        self.currentSpecial = maxSpecial
        self.triggerSlide = False
        self.sliding = False

        self.behavior = PlayerState.PlayerBehavior()
        self.state = self.behavior.getState(self)

    def canShoot(self, projType):
        canShoot = False
        if projType.reloadCounter > projType.reloadTime and projType.cost <= self.currentSpecial:
            canShoot = True
        return canShoot

    # Update player logic
    def update(self, deltat, GRAVITY, level, enemies):
        if self.entity.grounded:
            self.jumpCount = 0

        # Get new state, change only if its of different type
        newState = self.behavior.getState(self)
        if type(newState) != type(self.state):
            self.state = newState
            self.state.changeState(self)
        self.state.handleInput(self, GRAVITY)
        self.entity.update(deltat, GRAVITY, level, enemies)

        if self.entity.immuneCounter < self.entity.immuneTime and self.entity.directionHit is None:
            self.entity.effectsSprite = self.entity.currAnim.getCurrentFrame().copy()
            self.entity.effectsSprite.fill((255, 255, 255, 150), None, pygame.BLEND_RGBA_MULT)
        elif self.entity.effectsSprite and self.entity.immuneCounter >= self.entity.immuneTime:
            self.entity.effectsSprite = None

    # Draw player sprite
    def draw(self, screen, deltat, cameraX):
        self.entity.draw(screen, deltat, cameraX)
