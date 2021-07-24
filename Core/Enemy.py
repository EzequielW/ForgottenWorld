import pygame
import math
from Core.Constants import Direction
from Core.EnemyState import EnemyBehavior

class Enemy(pygame.sprite.Sprite):
    def __init__(self, entity, pointStart, pointEnd, player):
        pygame.sprite.Sprite.__init__(self)
        self.entity = entity
        self.pointStart = pointStart
        self.pointEnd = pointEnd
        self.behavior = EnemyBehavior()
        self.state = self.behavior.getState(self, player)

    def playerInSight(self, player):
        playerSighted = False
        entityP = player.entity
        entityE = self.entity

        # Check if enemy is looking at player direction
        isPlayerRight = entityE.facing == Direction.RIGHT and entityE.rect.x < entityP.rect.x
        isPlayerLeft = entityE.facing == Direction.LEFT and entityE.rect.x > entityP.rect.x

        # If it is, check if the player is vertically in sight
        if isPlayerRight or isPlayerLeft:
            playerY = entityP.rect.y + entityP.collRect.y
            playerBottom = playerY + entityP.collRect.height
            enemyY = entityE.rect.y + entityE.collRect.y
            enemyBottom = enemyY + entityE.collRect.height
            
            if playerY < enemyBottom and playerBottom > enemyY:
                playerSighted = True
        
        return playerSighted

    def update(self, deltat, GRAVITY, level, player):
        newState = self.behavior.getState(self, player)
        if type(newState) != type(self.state):
            self.state = newState
            self.state.changeState(self)
        self.state.updateState(self, GRAVITY)

        self.entity.update(deltat, GRAVITY, level, [player])

    def draw(self, screen, deltat, cameraX):
        self.entity.draw(screen, deltat, cameraX)
