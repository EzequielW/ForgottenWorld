import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" 
import math
import pygame
import pygame.freetype
from Core.Player import Player
from Core.Constants import Direction, AnimState
from Core.Animation import Animation
from Core.Level import Level
from Core.SpriteSheet import SpriteSheet
from Core.Entity import Entity
from Core.Enemy import Enemy
from Core.Projectile import ProjectileType
from Core.Load import initFireball, initAndromalius, initDarkMage, initLavaHybrid, initShadow, initMageBullet, initFireballoga, initPlayer
from UI.UI import UserInterface

SIZE = MAX_WIDTH, MAX_HEIGHT = 1024, 576 
BACKGROUND_COLOR = pygame.Color('white') 
FPS = 60
GRAVITY = 9

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(SIZE)

    pygame.display.set_caption("Forgotten World")
    clock = pygame.time.Clock()

    GAME_FONT = pygame.freetype.Font("Gotham.ttf", 24)

    currentLevel = Level('Levels/Level_1.json', MAX_HEIGHT, showCollRect=False)
    levelMusic = pygame.mixer.music.load("Assets/Sounds/high tech lab.wav")
    pygame.mixer.music.play(loops=-1)
    background = pygame.image.load('Assets/Terrain/Background/Bright/Background.png').convert_alpha()

    # Init projectiles
    primProj = initFireball(currentLevel.tileSize, 1/3, 225, 0.5, 6, 0)
    secondProj = initFireball(currentLevel.tileSize, 1, 150, 0.5, 12, 70)

    # Init player
    player = initPlayer(currentLevel.tileSize, 120, 50, [primProj, secondProj])
    playerEntity = player.entity

    # Init enemies
    enemyList = initEnemies(currentLevel.tileSize, player)

    # Init user interface
    userInterface = UserInterface(player, screen)

    # Set camera attributes
    cameraX = 0
    cameraVel = 50
    cameraThreshold = 100
    cameraMax = currentLevel.tileSize * currentLevel.rowSize - MAX_WIDTH
    bossFightTrigger = 2500
    cameraLock = False

    gameRestart = False
    gameRun = True
    # Main game loop
    while(gameRun):
        deltat = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRun = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.triggerUp = True
                if event.key == pygame.K_i and not player.sliding and playerEntity.grounded:
                    player.triggerSlide = True
                if event.key == pygame.K_p:
                    playerEntity.rect.x = 150
                    playerEntity.rect.y = 50
                    cameraX = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if userInterface.restartButton.collidepoint(event.pos):
                        gameRestart = True

        # Restart game variables
        if gameRestart:
            cameraX = 0
            cameraVel = 50
            cameraLock = False
            player = initPlayer(currentLevel.tileSize, 120, 50, [primProj, secondProj])
            playerEntity = player.entity
            enemyList = initEnemies(currentLevel.tileSize, player)
            gameRestart = False

        #Game logic
        currentLevel.update(deltat)
        deadEnemy = []
        for enemy in enemyList:
            enemy.update(deltat, GRAVITY, currentLevel, player)
            if enemy.entity.currentHealth == 0 and enemy.entity.currAnim.finished:
                deadEnemy.append(enemy)
        for deadE in deadEnemy:
            enemyList.remove(deadE)
        player.update(deltat, GRAVITY, currentLevel, enemyList)
        userInterface.update(player)

        #Camera movement
        if cameraLock:
            if cameraX < cameraMax:
                cameraX += cameraVel * deltat
                cameraVel += cameraVel * deltat
            else:
                cameraX = cameraMax
        elif player.entity.rect.x >= bossFightTrigger:
            cameraLock = True
        elif playerEntity.velX > 0 and cameraX < cameraMax:
            if playerEntity.rect.x + playerEntity.rect.width - cameraX > MAX_WIDTH/2 + cameraThreshold:
                cameraX = playerEntity.rect.x + playerEntity.rect.width - (MAX_WIDTH/2 + cameraThreshold)
            if cameraX > cameraMax: cameraX = cameraMax
        elif playerEntity.velX < 0 and cameraX > 0:
            if playerEntity.rect.x - cameraX < MAX_WIDTH/2 - cameraThreshold:
                cameraX = playerEntity.rect.x - (MAX_WIDTH/2 - cameraThreshold)
            if cameraX < 0: cameraX = 0

        #Draw everything
        screen.blit(pygame.transform.scale(background, SIZE), (0, 0))
        currentLevel.draw(screen, cameraX)
        for enemy in enemyList:
            enemy.draw(screen, deltat, cameraX)
        player.draw(screen, deltat, cameraX)
        userInterface.draw(screen)

        # Show fps
        fpsText, rect = GAME_FONT.render("FPS:" + str(round(clock.get_fps())), (255, 255, 255))
        screen.blit(fpsText,(MAX_WIDTH - 100, 20))

        pygame.display.update()

    pygame.quit()

def initEnemies(tileSize, player):
    enemyList = []

    # Init projectiles
    andromaliusProj = initMageBullet(tileSize, 1/2, 120, 1, 1, 0)
    darkMageProj = initShadow(tileSize, 2, 120, 2, 1, 0)
    lavaHybridProj = initFireball(tileSize, 1, 175, 1.5, 1, 0)
    lavaHybridCeilProj = initFireballoga(tileSize, 5/6, 175, 1, 1, 0)

    newEnemy = initAndromalius(tileSize, 300, 50, 260, 380, player, [andromaliusProj])
    darkMage = initDarkMage(tileSize, 1500, 50, 1300, 1600, player, [darkMageProj])
    lavaHybrid = initLavaHybrid(tileSize, 3250, 50, 3100, 3300, player, [lavaHybridProj, lavaHybridCeilProj])
    enemyList.append(newEnemy)
    enemyList.append(darkMage)
    enemyList.append(lavaHybrid)

    return enemyList

if __name__ == '__main__':
    main()