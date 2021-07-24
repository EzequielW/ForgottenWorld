import json
import pygame
import math
from Core.Animation import Animation 

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, collRect, imgID):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.collRect = collRect
        self.imgID = imgID

class Level():
    def __init__(self, level, screenHeight, showCollRect = False):
        levelJson = None
        with open(level, 'r') as f:
            levelJson = json.load(f)

        self.rowSize = levelJson['width']
        self.columnSize = levelJson['height']
        self.tileSize = screenHeight // self.columnSize

        # Load tiles from each tileset
        self.tilesets = {}
        for tileset in levelJson['tilesets']:
            collision = False
            for prop in tileset['properties']:
                if prop['name'] == 'collision':
                    collision = prop['value']

            for tile in tileset['tiles']: 
                image = None
                speed = 1

                if "animation" in tile:
                    tileID = []
                    image = []
                    speed = 0
                    for frame in tile['animation']:
                        speed += frame['duration']
                        # Need to loop for each one to get them in order
                        for t in tileset['tiles']:
                            if t['id'] == frame['tileid']:
                                image.append(pygame.image.load(t['image'][3:]).convert_alpha())
                    # Convert to seconds
                    speed = speed / 1000
                else:
                    image = [pygame.image.load(tile['image'][3:]).convert_alpha()]

                animation = Animation(image, speed)
                rect = ()
                if collision:
                    collRect = tile['objectgroup']['objects'][0]
                    x = (self.tileSize * collRect['x']) // tile['imagewidth']
                    y = (self.tileSize * collRect['y']) // tile['imageheight']
                    width = (self.tileSize * collRect['width']) // tile['imagewidth']
                    height = (self.tileSize * collRect['height']) // tile['imageheight']
                    rect = (x, y, width, height)

                self.tilesets[(tileset['firstgid'] + tile['id'])] = (animation, rect)
        
        #Create tiles for each layers
        self.layers = {}
        for layer in levelJson['layers']:
            reshapedLayer = []
            for i in range(layer['width']):
                for j in range(layer['height']):
                    tile = None
                    tileImg = layer['data'][layer['width']*j + i]

                    if tileImg != 0:
                        x = i*self.tileSize
                        y = j*self.tileSize
                        offsetX = offsetY = offsetWidth = offsetHeight = 0
                        #If it doesnt have collision offset leave to 0
                        if len(self.tilesets[tileImg][1]) != 0:
                            offsetX = self.tilesets[tileImg][1][0]
                            offsetY = self.tilesets[tileImg][1][1]
                            offsetWidth = self.tilesets[tileImg][1][2]
                            offsetHeight = self.tilesets[tileImg][1][3]
                        collRect = pygame.Rect((x + offsetX,y + offsetY), (offsetWidth, offsetHeight))
                        tile = Tile(x, y, collRect, tileImg)
                    reshapedLayer.append(tile)

            self.layers[layer['name']] = reshapedLayer

        self.showCollRect = showCollRect

    def collisionToPlatform(self, entity, velX, velY):
        collX = entity.rect.x + entity.collRect.x
        collY = entity.rect.y + entity.collRect.y
        collRect = pygame.Rect((collX, collY), (entity.collRect.width, entity.collRect.height))
        
        if velX == 0: collRect.height += 1

        for tile in self.layers['Ground']:
            if not tile:
                continue

            if tile.collRect.colliderect(collRect):
                if velX > 0: 
                    entity.rect.x = tile.collRect.left - entity.collRect.right - 1
                elif velX < 0:
                    entity.rect.x = tile.collRect.right - entity.collRect.left + 1

                if velY > 0:
                    entity.rect.y = tile.collRect.top - entity.collRect.bottom
                    entity.velY = 1
                    entity.grounded = True
                elif velY < 0:
                    entity.rect.y = tile.collRect.bottom - entity.collRect.top

    def update(self, deltat):
        for tile in self.tilesets:
            self.tilesets[tile][0].update(deltat)

    def draw(self, screen, cameraX):
        for layerKey in sorted(self.layers.keys()):
            for tile in self.layers[layerKey]:
                if tile:
                    image = self.tilesets[tile.imgID][0].getCurrentFrame()
                    screen.blit(pygame.transform.scale(image, (self.tileSize, self.tileSize)), (tile.x-cameraX, tile.y))
        
        # Show collision rectangle of the level
        if self.showCollRect:
            for tile in self.layers['Ground']:
                if tile:
                    rect = ((tile.collRect.x - cameraX, tile.collRect.y), (tile.collRect.width, tile.collRect.height))
                    pygame.draw.rect(screen, (0, 0, 255), rect, 2)
