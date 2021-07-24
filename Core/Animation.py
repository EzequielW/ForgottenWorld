import math
import pygame

class Animation():
    def __init__(self, frames, speed, counter=0.0, looped=True):
        self.frames = frames
        self.speed = speed
        self.looped = looped
        self.counter = counter
        self.finished = False
        self.color = []

    def getCurrentFrame(self):
        return self.frames[round(self.counter)]

    def isFinished(self):
        isFinished = False
        if self.counter >= len(self.frames) - 1:
            isFinished = True
        return isFinished

    def changeColor(self, color):
        self.color.append(color)
        for image in self.frames:
            # add in new RGB values
            image.fill(color, None, pygame.BLEND_RGBA_ADD)

    def reset(self):
        self.counter = 0
        for image in self.frames:
            for color in self.color:
                image.fill(color, None, pygame.BLEND_RGBA_SUB)
                self.color.remove(color)

    def update(self, deltat):
        self.counter += deltat * len(self.frames) * (1 / self.speed)

        if self.isFinished():
            if self.looped: 
                self.counter = 0.0
            else: 
                self.counter = len(self.frames) - 1
                self.finished = True