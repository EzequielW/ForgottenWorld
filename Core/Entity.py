import pygame
import math
import random

from Core.Projectile import Projectile
from Core.Animation import Animation
from Core.Constants import Direction

class Entity():
    def __init__(self, rect, collRect, speed, jumpSpeed, animations, currAnim, maxHealth, immuneTime, projTypes=[], showCollRect=False):
        self.rect = rect
        self.collRect = collRect
        self.speed = speed
        self.jumpSpeed = jumpSpeed
        self.animations = animations
        self.currAnim = currAnim
        self.maxHealth = maxHealth
        self.currentHealth = maxHealth
        self.immuneTime = immuneTime
        self.projTypes = projTypes
        self.showCollRect = showCollRect

        self.velX = 0
        self.velY = 0
        self.facing = Direction.RIGHT
        self.grounded = False
        self.projList = []
        self.directionHit = None
        self.immuneCounter = immuneTime
        self.effectsSprite = None

    # Set direction, if its a new direction change x and collision x
    def setFacing(self, direction):
        if self.facing != direction:
            self.facing = direction
            prevX = self.collRect.x
            self.collRect.x = self.rect.width - self.collRect.width - self.collRect.x
            self.rect.x += prevX - self.collRect.x

    # Add projectile of a given type
    def addProjectile(self, projType):
        projType.reloadCounter = 0

        projX = self.rect.x + self.collRect.x - projType.width
        if self.facing == Direction.RIGHT:
            projX = self.rect.x + self.collRect.x + self.collRect.width
        projY = (self.rect.y + self.rect.height / 2 - projType.height / 2)
        
        if projType.ceil:
            projY = 0
            if self.facing == Direction.RIGHT:
                projX = random.randint(projX, projX + projType.projRange)
            else:
                projX = random.randint(projX-projType.projRange, projX)

        rect = pygame.Rect(projX, projY, projType.width, projType.height)
        animation = Animation(projType.frames[self.facing], projType.reloadTime, looped=projType.looped)
        animationHit = Animation(projType.framesHit, 0.8, looped=False)
        newProj = Projectile(rect, projType.collRect, projType.speed, animation, 
            animationHit, self.facing, projType.damage, projType.cost, ceil=projType.ceil, 
            looped=projType.looped, showCollRect=False)

        self.projList.append(newProj)

    def isHit(self, enemies):
        entityX = self.rect.x + self.collRect.x
        entityY = self.rect.y + self.collRect.y
        collRect = pygame.Rect((entityX, entityY, self.collRect.width, self.collRect.height))

        for enemy in enemies:
            for proj in enemy.entity.projList:
                projX = proj.rect.x + proj.collRect.x
                projY = proj.rect.y + proj.collRect.y
                projCollRect = pygame.Rect((projX, projY, proj.collRect.width, proj.collRect.height))

                # Only hits if the projectile didnt already hit, and the entity isnt immune at this time
                if collRect.colliderect(projCollRect) and proj.hit == False and self.immuneCounter >= self.immuneTime and self.currentHealth != 0:
                    proj.hit = True
                    self.currentHealth -= proj.damage
                    self.directionHit = proj.facing
                    if self.currentHealth < 0:
                        self.currentHealth = 0
                

    def update(self, deltat, GRAVITY, level, enemies):
        self.rect.x += round(self.velX * deltat)
        level.collisionToPlatform(self, self.velX, 0)

        self.rect.y += round(self.velY * deltat)
        self.grounded = False
        level.collisionToPlatform(self, 0, self.velY)

        self.isHit(enemies)
        # Update projectiles types, each has a cooldown
        for projT in self.projTypes:
            projT.update(deltat)
        
        # Update every projectile
        for proj in self.projList:
            proj.update(deltat)

        if self.immuneCounter < self.immuneTime:
            self.immuneCounter += deltat

    def draw(self, screen, deltat, cameraX):
        self.currAnim.update(deltat)
        animFrame = self.currAnim.getCurrentFrame()
        if self.facing == Direction.LEFT:
            if self.effectsSprite:
                screen.blit(pygame.transform.flip(self.effectsSprite, True, False), (self.rect.x - cameraX, self.rect.y))
            else:
                screen.blit(pygame.transform.flip(animFrame, True, False), (self.rect.x - cameraX, self.rect.y)) 
        else:
            if self.effectsSprite:
                screen.blit(self.effectsSprite, (self.rect.x - cameraX, self.rect.y))
            else:
                screen.blit(animFrame, (self.rect.x - cameraX, self.rect.y))

        # Draw all projectiles for this entity
        projDelete = []
        for proj in self.projList:
            if proj.outsideScreen(cameraX, screen.get_width()) or (proj.hit and proj.animation.finished): 
                projDelete.append(proj)
            else: 
                proj.draw(screen, deltat, cameraX)

        for proj in projDelete:
            self.projList.remove(proj)

        # Shot collision rectangle in test mode
        if self.showCollRect:
            collRect = (self.rect.x - cameraX + self.collRect.x , self.rect.y + self.collRect.y, self.collRect.width, self.collRect.height)
            pygame.draw.rect(screen, (255, 0, 0), collRect, 2)
        


