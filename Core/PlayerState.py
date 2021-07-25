import pygame
import math

from Core.Constants import Direction, AnimState, DAMAGE_VELX, DAMAGE_VELY

class PlayerBehavior():
    def getState(self, player):
        keys = pygame.key.get_pressed()
        state = None
        entity = player.entity
        shootPrim = keys[pygame.K_j] and entity.projTypes[0].reloadCounter > entity.projTypes[0].reloadTime
        shootSecond = keys[pygame.K_k] and entity.projTypes[1].reloadCounter > entity.projTypes[1].reloadTime and player.currentSpecial >= entity.projTypes[1].cost
        stillShootPrim = entity.projTypes[0].reloadCounter < entity.projTypes[0].reloadTime
        stillShootSecond = entity.projTypes[1].reloadCounter < entity.projTypes[1].reloadTime

        if entity.currentHealth == 0:
            state = DeadState()
        elif entity.directionHit:
            state = HitState()
        elif not player.entity.grounded or (player.triggerUp and player.jumpCount < 1):
            if stillShootPrim or shootPrim or stillShootSecond or shootSecond:
                state = JumpShootState()
            else:
                state = JumpState()
        elif player.triggerSlide or player.sliding:
            state = SlideState()
        elif stillShootPrim or shootPrim:
            if keys[pygame.K_a] or keys[pygame.K_d]:
                state = RunShootState()
            else:
                state = ShootState()
        elif stillShootSecond or shootSecond:
            state = ShootState()
        elif keys[pygame.K_a]:
            state = RunState()
        elif keys[pygame.K_d]:
            state = RunState()
        else:
            state = IdleState()

        return state

class IdleState():
    def changeState(self, player):
        entity = player.entity
        entity.currAnim = entity.animations[AnimState.IDLE]
        entity.currAnim.reset()
        entity.velX = 0

    def handleInput(self, player, GRAVITY):
        pass

class RunState():
    def changeState(self, player):
        entity = player.entity

        counter = 0
        if entity.currAnim == entity.animations[AnimState.RUN_SHOOT]:
            counter = entity.currAnim.counter

        entity.currAnim = entity.animations[AnimState.RUN]
        entity.currAnim.reset()
        entity.currAnim.counter = counter

    def handleInput(self, player, GRAVITY):
        keys = pygame.key.get_pressed()
        entity = player.entity

        if keys[pygame.K_a]:
            entity.setFacing(Direction.LEFT)
            entity.velX = -entity.speed
        elif keys[pygame.K_d]:
            entity.setFacing(Direction.RIGHT)
            entity.velX = entity.speed

class JumpState():
    def changeState(self, player):
        entity = player.entity
        keys = pygame.key.get_pressed()

        counter = 0
        if entity.currAnim == entity.animations[AnimState.JUMP_SHOOT]:
           counter = (len(entity.animations[AnimState.JUMP].frames) - 1) * entity.currAnim.counter / (len(entity.currAnim.frames) - 1)
        else:
            player.sliding = False
            player.jumpCount += 1
            if player.triggerUp:
                player.entity.velY = -player.entity.jumpSpeed
                player.entity.grounded = False

        player.entity.currAnim = player.entity.animations[AnimState.JUMP]
        player.entity.currAnim.reset()
        player.entity.currAnim.counter = counter

    def handleInput(self, player, GRAVITY):
        keys = pygame.key.get_pressed()
        entity = player.entity
        player.triggerUp = False

        if keys[pygame.K_a]:
            entity.setFacing(Direction.LEFT)
        elif keys[pygame.K_d]:
            entity.setFacing(Direction.RIGHT)  
        #Stop velocity if keys are unpressed, allow movement while going up
        if entity.velY < 0:
            if not keys[pygame.K_w]:
                entity.velY = 0

            if keys[pygame.K_a]:
                entity.velX = -entity.speed
            elif keys[pygame.K_d]:
                entity.velX = entity.speed
            
        if not keys[pygame.K_a] and entity.velX < 0:
            entity.velX = 0
        if not keys[pygame.K_d] and entity.velX > 0:
            entity.velX = 0

        entity.velY += GRAVITY

class ShootState():
    def changeState(self, player):
        keys = pygame.key.get_pressed()
        entity = player.entity
        entity.velX = 0
        
        projType = None
        if keys[pygame.K_j] and entity.projTypes[0].reloadCounter > entity.projTypes[0].reloadTime:
            projType = entity.projTypes[0]
        else:
            projType = entity.projTypes[1]

        entity.currAnim = entity.animations[AnimState.SHOOT]
        entity.currAnim.reset()
        entity.currAnim.speed = projType.reloadTime

    def handleInput(self, player, GRAVITY):
        keys = pygame.key.get_pressed()
        entity = player.entity
        projNumber = -1

        if keys[pygame.K_j] and entity.projTypes[0].reloadCounter > entity.projTypes[0].reloadTime and entity.projTypes[0].cost <= player.currentSpecial:
            projNumber = 0
        elif keys[pygame.K_k] and entity.projTypes[1].reloadCounter > entity.projTypes[1].reloadTime and entity.projTypes[1].cost <= player.currentSpecial:
            projNumber = 1

        if projNumber != -1:
            player.currentSpecial -= entity.projTypes[projNumber].cost
            entity.currAnim.speed = entity.projTypes[projNumber].reloadTime
            entity.addProjectile(entity.projTypes[projNumber])

class RunShootState(RunState):
    def changeState(self, player):
        entity = player.entity

        counter = 0
        if entity.currAnim == entity.animations[AnimState.RUN] or entity.currAnim == entity.animations[AnimState.RUN_SHOOT]:
            counter = entity.currAnim.counter

        entity.currAnim = entity.animations[AnimState.RUN_SHOOT]
        entity.currAnim.reset()
        entity.currAnim.counter = counter

    def handleInput(self, player, GRAVITY):
        keys = pygame.key.get_pressed()
        entity = player.entity

        super().handleInput(player, GRAVITY)
        
        if keys[pygame.K_j] and entity.projTypes[0].reloadCounter > entity.projTypes[0].reloadTime:
            player.currentSpecial -= entity.projTypes[0].cost
            entity.addProjectile(entity.projTypes[0])

class JumpShootState(JumpState):
    def changeState(self, player):
        entity = player.entity

        counter = 0
        if entity.currAnim == entity.animations[AnimState.JUMP]:
            counter = (len(entity.animations[AnimState.JUMP_SHOOT].frames) - 1) * entity.currAnim.counter / (len(entity.currAnim.frames) - 1)
        else:
            player.sliding = False
            player.jumpCount += 1
            if player.triggerUp:
                player.entity.velY = -player.entity.jumpSpeed
                player.entity.grounded = False

        entity.currAnim = entity.animations[AnimState.JUMP_SHOOT]
        entity.currAnim.reset()
        entity.currAnim.counter = counter

    def handleInput(self, player, GRAVITY):
        keys = pygame.key.get_pressed()
        entity = player.entity

        super().handleInput(player, GRAVITY)

        if keys[pygame.K_j] and player.canShoot(entity.projTypes[0]):
            player.currentSpecial -= entity.projTypes[0].cost
            entity.addProjectile(entity.projTypes[0])
        elif keys[pygame.K_k] and player.canShoot(entity.projTypes[1]):
            player.currentSpecial -= entity.projTypes[1].cost
            entity.addProjectile(entity.projTypes[1])

class HitState():
    def changeState(self, player):
        entity = player.entity
        entity.immuneCounter = 0
        entity.grounded = False

        entity.velY = -DAMAGE_VELY
        if entity.directionHit == Direction.RIGHT:
            entity.velX = DAMAGE_VELX
        else:
            entity.velX = -DAMAGE_VELX
            
        entity.effectsSprite = entity.currAnim.getCurrentFrame().copy()
        entity.effectsSprite.fill((255, 0, 0, 0), None, pygame.BLEND_RGBA_ADD)

    def handleInput(self, player, GRAVITY):
        entity = player.entity

        entity.velY += GRAVITY
        if entity.grounded:
            entity.directionHit = None
            entity.effectsSprite = None

class DeadState():
    def changeState(self, player):
        entity = player.entity
        entity.currAnim.reset()
        entity.currAnim = entity.animations[AnimState.DEAD]
        entity.velX = 0
        entity.velY = 0

    def handleInput(self, player, GRAVITY):
        pass

class SlideState():
    def changeState(self, player):
        entity = player.entity
        self.direction = entity.facing

        player.triggerSlide = False
        player.sliding = True
        entity.currAnim = entity.animations[AnimState.SLIDE]
        entity.currAnim.reset()
    
    def handleInput(self, player, GRAVITY):
        entity = player.entity

        if entity.currAnim.finished:
            player.sliding = False
        else:
            player.triggerSlide = False
            if self.direction == Direction.RIGHT:
                entity.velX = entity.speed * 2
            else:
                entity.velX = -entity.speed * 2
        
        