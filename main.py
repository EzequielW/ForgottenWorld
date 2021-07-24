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
from UI.UI import UserInterface

SIZE = MAX_WIDTH, MAX_HEIGHT = 1024, 576 
BACKGROUND_COLOR = pygame.Color('white') 
FPS = 60
GRAVITY = 9

def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)

    pygame.display.set_caption("Test")
    clock = pygame.time.Clock()

    GAME_FONT = pygame.freetype.Font("Gotham.ttf", 24)

    currentLevel = Level('Levels/Level_1.json', MAX_HEIGHT, showCollRect=True)
    background = pygame.image.load('Assets/Terrain/Background/Bright/Background.png').convert_alpha()

    # Init projectiles
    primProj = initFireball(currentLevel.tileSize, 1/3, 225, 0.4, 6, 0)
    secondProj = initFireball(currentLevel.tileSize, 1, 150, 0.5, 12, 70)
    enemyProj = initFireball(currentLevel.tileSize, 1/3, 120, 1.5, 1, 0)

    # Init player
    player = initPlayer(currentLevel.tileSize, 120, 50, [primProj, secondProj])
    playerEntity = player.entity

    # Init enemies
    enemyList = []
    newEnemy = initAndromalius(currentLevel.tileSize, 300, 50, player, [enemyProj])
    enemyList.append(newEnemy)

    # Init user interface
    userInterface = UserInterface(player)

    # Set camera attributes
    cameraX = 0
    cameraThreshold = 100
    cameraMax = currentLevel.tileSize * currentLevel.rowSize - MAX_WIDTH

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
                if event.key == pygame.K_p:
                    playerEntity.rect.x = 150
                    playerEntity.rect.y = 50
                    cameraX = 0

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
        if playerEntity.velX > 0 and cameraX < cameraMax:
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

def initFireball(tileSize, scale, speed, reloadTime, damage, cost):
    # Initialize projectile attributes
    ssProj = SpriteSheet("Assets/Player/projectile.png")
    ssProjWidth = 172
    ssProjHeight = 139

    fireballRight = ssProj.imagesAt(((0 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                            (1 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                            (2 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                            (3 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                            (4 * ssProjWidth, 0, ssProjWidth, ssProjHeight)))
    
    fireballLeft = ssProj.imagesAt(((0 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                        (1 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                        (2 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                        (3 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                        (4 * ssProjWidth, 0, ssProjWidth, ssProjHeight)))

    fireballLeft = [pygame.transform.flip(image, True, False) for image in fireballLeft]

    ssProjHit = SpriteSheet("Assets/Player/muzzle.png")
    ssProjHitWidth = 19
    ssProjHitHeight = 241

    hitAnim = ssProjHit.imagesAt(((0 * ssProjHitWidth, 0, ssProjHitWidth, ssProjHitHeight),
    (1 * ssProjHitWidth, 0, ssProjHitWidth, ssProjHitHeight),
    (2 * ssProjHitWidth, 0, ssProjHitWidth, ssProjHitHeight),
    (3 * ssProjHitWidth, 0, ssProjHitWidth, ssProjHitHeight),
    (4 * ssProjHitWidth, 0, ssProjHitWidth, ssProjHitHeight)))

    projWidth = round(tileSize * 1.2374 * scale)
    projHeight = round(tileSize * scale)

    projAnim = { Direction.RIGHT: [pygame.transform.scale(image, (projWidth, projHeight)) for image in fireballRight], 
                    Direction.LEFT: [pygame.transform.scale(image, (projWidth, projHeight)) for image in fireballLeft] }
    
    hitAnim = [pygame.transform.scale(image, (ssProjHitWidth, projHeight)) for image in hitAnim]
    # Primary projectile
    projRect = pygame.Rect((0, 0), (projWidth, projHeight))
    proj = ProjectileType(projRect.width, projRect.height, projRect, speed, reloadTime, projAnim, hitAnim, damage, cost)

    return proj

def initAndromalius(tileSize, x, y, player, projList):
    rect = pygame.Rect((x, y), (57, 88))
    collRect = pygame.Rect((0, 0), (tileSize, tileSize * 2))
    speed = 30
    jumpSpeed = 250

    ss = SpriteSheet("Assets/Enemies/andromalius-57x88.png")
    ssWidth = 57
    ssHeight = 88

    jump = ss.imagesAt(((0 * ssWidth, 0, ssWidth, ssHeight),
        (0 * ssWidth, 0, ssWidth, ssHeight)), 
        scaling=(rect.width, rect.height))

    run = ss.imagesAt(((0 * ssWidth, 0, ssWidth, ssHeight),
        (1 * ssWidth, 0, ssWidth, ssHeight),
        (2 * ssWidth, 0, ssWidth, ssHeight),
        (3 * ssWidth, 0, ssWidth, ssHeight),
        (4 * ssWidth, 0, ssWidth, ssHeight),
        (5 * ssWidth, 0, ssWidth, ssHeight),
        (6 * ssWidth, 0, ssWidth, ssHeight),
        (7 * ssWidth, 0, ssWidth, ssHeight)),
        scaling=(rect.width, rect.height))

    shoot = ss.imagesAt(((0 * ssWidth, ssHeight, ssWidth, ssHeight),
        (1 * ssWidth, ssHeight, ssWidth, ssHeight),
        (2 * ssWidth, ssHeight, ssWidth, ssHeight),
        (3 * ssWidth, ssHeight, ssWidth, ssHeight),
        (4 * ssWidth, ssHeight, ssWidth, ssHeight),
        (5 * ssWidth, ssHeight, ssWidth, ssHeight),
        (6 * ssWidth, ssHeight, ssWidth, ssHeight),
        (7 * ssWidth, ssHeight, ssWidth, ssHeight)),
        scaling=(rect.width, rect.height))

    dead = ss.imagesAt(((0 * ssWidth, 0, ssWidth, ssHeight),
        (0 * ssWidth, 0, ssWidth, ssHeight)),
        scaling=(rect.width, rect.height))

    animations = {AnimState.JUMP: Animation(jump, 1), AnimState.RUN: Animation(run, 1), 
        AnimState.SHOOT: Animation(shoot, 1), AnimState.DEAD: Animation(dead, 2, looped=False)}
    
    immuneTime = 0
    hp = 20

    enemyEntity = Entity(rect, collRect, speed, jumpSpeed, animations, animations[AnimState.JUMP], hp, immuneTime, projList, showCollRect=True)
    newEnemy = Enemy(enemyEntity, 260, 380, player)

    return newEnemy

def initPlayer(tileSize, x, y, projList):
    # Initialize player attributes
    rect = pygame.Rect((120, 50), (90, 90))
    # Player rectangle of collision
    collRect = pygame.Rect((20, 10), (tileSize, tileSize * 2))

    speed = 130
    jumpSpeed = 300

    ss = SpriteSheet("Assets/Player/player.png")
    ssWidth = 567
    ssHeight = 556

    idle = ss.imagesAt(((0 * ssWidth, 0, ssWidth, ssHeight), 
                        (1 * ssWidth, 0, ssWidth, ssHeight), 
                        (2 * ssWidth, 0, ssWidth, ssHeight), 
                        (3 * ssWidth, 0, ssWidth, ssHeight), 
                        (4 * ssWidth, 0, ssWidth, ssHeight), 
                        (5 * ssWidth, 0, ssWidth, ssHeight), 
                        (6 * ssWidth, 0, ssWidth, ssHeight), 
                        (7 * ssWidth, 0, ssWidth, ssHeight)), 
                        scaling = (rect.width, rect.height))

    run = ss.imagesAt(((0 * ssWidth, 1 * ssHeight, ssWidth, ssHeight), 
                            (1 * ssWidth, 1 * ssHeight, ssWidth, ssHeight), 
                            (2 * ssWidth, 1 * ssHeight, ssWidth, ssHeight), 
                            (3 * ssWidth, 1 * ssHeight, ssWidth, ssHeight), 
                            (4 * ssWidth, 1 * ssHeight, ssWidth, ssHeight), 
                            (5 * ssWidth, 1 * ssHeight, ssWidth, ssHeight), 
                            (6 * ssWidth, 1 * ssHeight, ssWidth, ssHeight), 
                            (7 * ssWidth, 1 * ssHeight, ssWidth, ssHeight)),
                            scaling = (rect.width, rect.height))

    jump = ss.imagesAt(((0 * ssWidth, 2 * ssHeight, ssWidth, ssHeight), 
                            (1 * ssWidth, 2 * ssHeight, ssWidth, ssHeight), 
                            (2 * ssWidth, 2 * ssHeight, ssWidth, ssHeight), 
                            (3 * ssWidth, 2 * ssHeight, ssWidth, ssHeight), 
                            (4 * ssWidth, 2 * ssHeight, ssWidth, ssHeight), 
                            (5 * ssWidth, 2 * ssHeight, ssWidth, ssHeight), 
                            (6 * ssWidth, 2 * ssHeight, ssWidth, ssHeight), 
                            (7 * ssWidth, 2 * ssHeight, ssWidth, ssHeight),
                            (8 * ssWidth, 2 * ssHeight, ssWidth, ssHeight),
                            (9 * ssWidth, 2 * ssHeight, ssWidth, ssHeight)),
                            scaling = (rect.width, rect.height))

    shoot = ss.imagesAt(((0 * ssWidth, 3 * ssHeight, ssWidth, ssHeight), 
                            (1 * ssWidth, 3 * ssHeight, ssWidth, ssHeight), 
                            (2 * ssWidth, 3 * ssHeight, ssWidth, ssHeight), 
                            (3 * ssWidth, 3 * ssHeight, ssWidth, ssHeight)),
                            scaling = (rect.width, rect.height))

    runShoot = ss.imagesAt(((0 * ssWidth, 4 * ssHeight, ssWidth, ssHeight), 
                                (1 * ssWidth, 4 * ssHeight, ssWidth, ssHeight), 
                                (2 * ssWidth, 4 * ssHeight, ssWidth, ssHeight), 
                                (3 * ssWidth, 4 * ssHeight, ssWidth, ssHeight),
                                (4 * ssWidth, 4 * ssHeight, ssWidth, ssHeight),
                                (5 * ssWidth, 4 * ssHeight, ssWidth, ssHeight),
                                (6 * ssWidth, 4 * ssHeight, ssWidth, ssHeight),
                                (7 * ssWidth, 4 * ssHeight, ssWidth, ssHeight)),
                                scaling = (rect.width, rect.height))

    jumpShoot = ss.imagesAt(((0 * ssWidth, 5 * ssHeight, ssWidth, ssHeight), 
                            (1 * ssWidth, 5 * ssHeight, ssWidth, ssHeight), 
                            (2 * ssWidth, 5 * ssHeight, ssWidth, ssHeight), 
                            (3 * ssWidth, 5 * ssHeight, ssWidth, ssHeight),
                            (4 * ssWidth, 5 * ssHeight, ssWidth, ssHeight)),
                            scaling = (rect.width, rect.height))

    melee = ss.imagesAt(((0 * ssWidth, 6 * ssHeight, ssWidth, ssHeight), 
                        (1 * ssWidth, 6 * ssHeight, ssWidth, ssHeight), 
                        (2 * ssWidth, 6 * ssHeight, ssWidth, ssHeight), 
                        (3 * ssWidth, 6 * ssHeight, ssWidth, ssHeight), 
                        (4 * ssWidth, 6 * ssHeight, ssWidth, ssHeight), 
                        (5 * ssWidth, 6 * ssHeight, ssWidth, ssHeight), 
                        (6 * ssWidth, 6 * ssHeight, ssWidth, ssHeight), 
                        (7 * ssWidth, 6 * ssHeight, ssWidth, ssHeight)),
                        scaling = (rect.width, rect.height))

    dead = ss.imagesAt(((0 * ssWidth, 9 * ssHeight, ssWidth, ssHeight), 
                        (1 * ssWidth, 9 * ssHeight, ssWidth, ssHeight), 
                        (2 * ssWidth, 9 * ssHeight, ssWidth, ssHeight), 
                        (3 * ssWidth, 9 * ssHeight, ssWidth, ssHeight), 
                        (4 * ssWidth, 9 * ssHeight, ssWidth, ssHeight), 
                        (5 * ssWidth, 9 * ssHeight, ssWidth, ssHeight), 
                        (6 * ssWidth, 9 * ssHeight, ssWidth, ssHeight), 
                        (7 * ssWidth, 9 * ssHeight, ssWidth, ssHeight)),
                        scaling = (rect.width, rect.height))

    # Dictionary with each animation
    animations = {
        AnimState.IDLE: Animation(idle, 1), AnimState.RUN: Animation(run, 1),
        AnimState.JUMP: Animation(jump, 1.2, looped=False), AnimState.SHOOT: Animation(shoot, 1),
        AnimState.RUN_SHOOT: Animation(runShoot, 1), AnimState.JUMP_SHOOT: Animation(jumpShoot, 1, looped=False), 
        AnimState.MELEE: Animation(melee, 1, looped=False), AnimState.DEAD: Animation(dead, 1.5, looped=False)
    }

    immuneTime = 3
    lifes = 3

    playerEntity = Entity(rect, collRect, speed, jumpSpeed, animations, animations[AnimState.JUMP], lifes, immuneTime, projList, showCollRect = True)
    player = Player(playerEntity, 100)

    return player

if __name__ == '__main__':
    main()