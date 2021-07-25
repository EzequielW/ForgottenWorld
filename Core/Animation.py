import math
import pygame

class Animation():
    def __init__(self, frames, speed, counter=0.0, looped=True):
        self.frames = frames
        self.speed = speed
        self.looped = looped
        self.counter = counter
        self.finished = False

    def getCurrentFrame(self):
        return self.frames[math.floor(self.counter)]

    def isFinished(self):
        isFinished = False
        if math.floor(self.counter) > len(self.frames) - 1:
            isFinished = True
        return isFinished

    def reset(self):
        self.counter = 0
        self.finished = False

    def update(self, deltat):
        self.counter += deltat * len(self.frames) * (1 / self.speed)

        if self.isFinished():
            if self.looped: 
                self.counter = 0.0
            else: 
                self.counter = len(self.frames) - 1
                self.finished = True