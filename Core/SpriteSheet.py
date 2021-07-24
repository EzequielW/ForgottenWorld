import pygame

class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
            self.colors = []
        except pygame.error as message:
            print ('Unable to load spritesheet image:', filename)
            raise message

    # Load a specific image from a specific rectangle
    def imageAt(self, rectangle, scaling = None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()
        image.fill((0, 0, 0, 0))
        image.blit(self.sheet, (0, 0), rect)
        
        if scaling is not None:
            image = pygame.transform.scale(image, scaling)

        return image

    # Load a whole bunch of images and return them as a list
    def imagesAt(self, rects, scaling = None):
        return [self.imageAt(rect, scaling) for rect in rects]