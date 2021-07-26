import pygame
import math
from Core.Constants import Direction

class ProjectileType(object):
    def __init__(self, width, height, collRect, speed, reloadTime, frames, framesHit, damage, cost, ceil=False, projRange=-1, looped=True):
        self.width = width
        self.height = height
        self.collRect = collRect
        self.speed = speed
        self.reloadTime = reloadTime
        self.reloadCounter = 0
        self.frames = frames
        self.framesHit = framesHit
        self.damage = damage
        self.cost = cost
        self.looped = looped
        self.ceil = ceil
        self.projRange = projRange
    
    def update(self, deltat):
        if self.reloadCounter <= self.reloadTime:
            self.reloadCounter += deltat

class Projectile(object):
    def __init__(self, rect, collRect, speed, animation, animationHit, facing, damage, cost, ceil=False, looped=True, showCollRect = False):
        self.rect = rect
        self.collRect = collRect
        self.speed = speed
        self.animation = animation
        self.animationHit = animationHit
        self.animCounter = 0
        self.facing = facing
        if self.facing == Direction.LEFT:
            self.speed = -speed
        self.damage = damage
        self.cost = cost
        self.looped = looped
        self.ceil = ceil

        self.hit = False    
        self.showCollRect = showCollRect

    # If the projectile is outside the screen returns true
    def outsideScreen(self, cameraX, maxWidth):
        projX = self.rect.x + self.collRect.x
        projWidth = projX + self.collRect.width

        outside = False
        if projX - cameraX > maxWidth or projWidth - cameraX < 0:
            outside = True

        return outside

    def update(self, deltat):
        if self.ceil:
            self.rect.y -= round(self.speed * deltat)
        else:
            self.rect.x += round(self.speed * deltat)

        if not self.looped and math.floor(self.animation.counter) == len(self.animation.frames) - 1:
            self.hit = True

        if self.hit and self.animation != self.animationHit:
            self.animation = self.animationHit
            self.speed = 0

            width = self.animationHit.getCurrentFrame().get_rect().width
            if self.facing == Direction.RIGHT:
                self.rect.x = self.rect.x + self.rect.width - width
    
    def draw(self, screen, deltat, cameraX):
        self.animation.update(deltat)
        currFrame = self.animation.getCurrentFrame()
        screen.blit(currFrame, (self.rect.x - cameraX, self.rect.y))

        if self.showCollRect:
            collRect = (self.rect.x - cameraX + self.collRect.x , self.rect.y + self.collRect.y, self.collRect.width, self.collRect.height)
            pygame.draw.rect(screen, (255, 255, 0), collRect, 2)