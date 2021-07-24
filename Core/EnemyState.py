import pygame
from Core.Constants import Direction, AnimState, DAMAGE_VELX, DAMAGE_VELY

class EnemyBehavior():
    def getState(self, enemy, player):
        entity = enemy.entity
        state = None

        if entity.currentHealth == 0:
            state = DeadState()
        elif entity.directionHit:
            state = HitState()
        elif not entity.grounded:
            state = JumpState()
        elif enemy.playerInSight(player):
            state = ShootState()
        else:
            state = RunState()

        return state
            

class JumpState():
    def changeState(self, enemy):
        enemy.entity.currAnim = enemy.entity.animations[AnimState.JUMP]
        enemy.entity.currAnim.reset()
    
    def updateState(self, enemy, GRAVITY):
        enemy.entity.velY += GRAVITY

class RunState():
    def changeState(self, enemy):
        entity = enemy.entity

        entity.currAnim = entity.animations[AnimState.RUN]
        entity.currAnim.reset()

        if entity.facing == Direction.RIGHT:
            entity.velX = entity.speed
        else:
            entity.velX = -entity.speed

    def updateState(self, enemy, GRAVITY):
        entity = enemy.entity

        if entity.rect.x + entity.collRect.width >= enemy.pointEnd:
            entity.setFacing(Direction.LEFT)
            entity.velX = -entity.speed
        elif entity.rect.x < enemy.pointStart:
            entity.setFacing(Direction.RIGHT) 
            entity.velX = entity.speed

class ShootState():
    def changeState(self, enemy):
        entity = enemy.entity

        entity.currAnim = entity.animations[AnimState.RUN]
        entity.currAnim.reset()

        if entity.facing == Direction.RIGHT:
            entity.velX = entity.speed
        else:
            entity.velX = -entity.speed
    
    def updateState(self, enemy, GRAVITY):
        entity = enemy.entity

        if entity.facing == Direction.LEFT:
            if entity.rect.x > enemy.pointStart:
                entity.velX = -entity.speed
            else:
                entity.velX = 0
        else:
            if entity.rect.x + entity.collRect.width < enemy.pointEnd:
                entity.velX = entity.speed
            else:
                entity.velX = 0

        if entity.projTypes[0].reloadCounter >= entity.projTypes[0].reloadTime:
            entity.addProjectile(entity.projTypes[0])

class HitState():
    def changeState(self, enemy):
        entity = enemy.entity
        entity.grounded = False

        entity.velY = -DAMAGE_VELY
        if entity.directionHit == Direction.RIGHT:
            entity.velX = DAMAGE_VELX
        else:
            entity.velX = -DAMAGE_VELX

        entity.effectsSprite = entity.currAnim.getCurrentFrame().copy()
        entity.effectsSprite.fill((255, 0, 0, 0), None, pygame.BLEND_RGBA_ADD)

    def updateState(self, enemy, GRAVITY):
        entity = enemy.entity

        entity.velY += GRAVITY
        if entity.grounded:
            entity.directionHit = None
            entity.effectsSprite = None
            
class DeadState():
    def changeState(self, enemy):
        entity = enemy.entity
        
        entity.velX = 0
        entity.velY = 0
        entity.currAnim.reset()
        entity.currAnim = entity.animations[AnimState.DEAD]

        entity.effectsSprite = entity.currAnim.getCurrentFrame().copy()
        entity.effectsSprite.fill((255, 0, 0, 0), None, pygame.BLEND_RGBA_ADD)
    
    def updateState(self, enemy, GRAVITY):
        entity = enemy.entity
        fadeCounter = 255 - 255 * (entity.currAnim.counter / (len(entity.currAnim.frames) - 1))
        entity.effectsSprite.fill((255, 255, 255, fadeCounter), None, pygame.BLEND_RGBA_MULT)
