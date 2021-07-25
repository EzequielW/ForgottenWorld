import pygame
from Core.SpriteSheet import SpriteSheet
from Core.Projectile import ProjectileType
from Core.Constants import Direction, AnimState
from Core.Animation import Animation
from Core.Entity import Entity
from Core.Enemy import Enemy
from Core.Player import Player

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

def initShadow(tileSize, scale, speed, reloadTime, damage, cost):
    # Initialize projectile attributes
    ssProj = SpriteSheet("Assets/Enemies/shadow-80x70.png")
    ssProjWidth = 80
    ssProjHeight = 70

    shadowRight = ssProj.imagesAt(((0 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                (1 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                (2 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                (3 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                (0 * ssProjWidth, ssProjHeight, ssProjWidth, ssProjHeight),
                                (1 * ssProjWidth, ssProjHeight, ssProjWidth, ssProjHeight), 
                                (2 * ssProjWidth, ssProjHeight, ssProjWidth, ssProjHeight), 
                                (3 * ssProjWidth, ssProjHeight, ssProjWidth, ssProjHeight),
                                (0 * ssProjWidth, 2 * ssProjHeight, ssProjWidth, ssProjHeight),
                                (1 * ssProjWidth, 2 * ssProjHeight, ssProjWidth, ssProjHeight), 
                                (2 * ssProjWidth, 2 * ssProjHeight, ssProjWidth, ssProjHeight), 
                                (3 * ssProjWidth, 2 * ssProjHeight, ssProjWidth, ssProjHeight),
                                (0 * ssProjWidth, 3 * ssProjHeight, ssProjWidth, ssProjHeight),
                                (1 * ssProjWidth, 3 * ssProjHeight, ssProjWidth, ssProjHeight), 
                                (0 * ssProjWidth, 4 * ssProjHeight, ssProjWidth, ssProjHeight),
                                (1 * ssProjWidth, 4 * ssProjHeight, ssProjWidth, ssProjHeight), 
                                (2 * ssProjWidth, 4 * ssProjHeight, ssProjWidth, ssProjHeight), 
                                (3 * ssProjWidth, 4 * ssProjHeight, ssProjWidth, ssProjHeight)))
    
    shadowRight = [pygame.transform.flip(image, True, False) for image in shadowRight]

    shadowLeft = ssProj.imagesAt(((0 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                (1 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                (2 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                (3 * ssProjWidth, 0, ssProjWidth, ssProjHeight), 
                                (0 * ssProjWidth, ssProjHeight, ssProjWidth, ssProjHeight),
                                (1 * ssProjWidth, ssProjHeight, ssProjWidth, ssProjHeight), 
                                (2 * ssProjWidth, ssProjHeight, ssProjWidth, ssProjHeight), 
                                (3 * ssProjWidth, ssProjHeight, ssProjWidth, ssProjHeight),
                                (0 * ssProjWidth, 2 * ssProjHeight, ssProjWidth, ssProjHeight),
                                (1 * ssProjWidth, 2 * ssProjHeight, ssProjWidth, ssProjHeight), 
                                (2 * ssProjWidth, 2 * ssProjHeight, ssProjWidth, ssProjHeight), 
                                (3 * ssProjWidth, 2 * ssProjHeight, ssProjWidth, ssProjHeight),
                                (0 * ssProjWidth, 3 * ssProjHeight, ssProjWidth, ssProjHeight),
                                (1 * ssProjWidth, 3 * ssProjHeight, ssProjWidth, ssProjHeight), 
                                (0 * ssProjWidth, 4 * ssProjHeight, ssProjWidth, ssProjHeight),
                                (1 * ssProjWidth, 4 * ssProjHeight, ssProjWidth, ssProjHeight), 
                                (2 * ssProjWidth, 4 * ssProjHeight, ssProjWidth, ssProjHeight), 
                                (3 * ssProjWidth, 4 * ssProjHeight, ssProjWidth, ssProjHeight)))

    hitAnim = [ssProj.imageAt((3 * ssProjWidth, 4 * ssProjHeight, ssProjWidth, ssProjHeight))]

    projWidth = round(tileSize * 1.142857 * scale)
    projHeight = round(tileSize * scale)

    projAnim = { Direction.RIGHT: [pygame.transform.scale(image, (projWidth, projHeight)) for image in shadowRight], 
                    Direction.LEFT: [pygame.transform.scale(image, (projWidth, projHeight)) for image in shadowLeft] }
    
    hitAnim = [pygame.transform.scale(image, (ssProjWidth, projHeight)) for image in hitAnim]
    # Primary projectile
    projRect = pygame.Rect((25, 10), (projWidth / 3, projHeight - 10))
    proj = ProjectileType(projRect.width, projRect.height, projRect, speed, reloadTime, projAnim, hitAnim, damage, cost)

    return proj

def initAndromalius(tileSize, x, y, startPoint, endPoint, player, projList):
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
    newEnemy = Enemy(enemyEntity, startPoint, endPoint, player)

    return newEnemy

def initDarkMage(tileSize, x, y, startPoint, endPoint, player, projList):
    rect = pygame.Rect((x, y), (85, 94))
    collRect = pygame.Rect((25, 15), (tileSize, tileSize * 2))
    speed = 30
    jumpSpeed = 250

    ss = SpriteSheet("Assets/Enemies/mage-1-85x94.png")
    ssWidth = 85
    ssHeight = 94

    jump = ss.imagesAt(((0 * ssWidth, 0, ssWidth, ssHeight),
        (0 * ssWidth, 0, ssWidth, ssHeight)), 
        scaling=(rect.width, rect.height))

    run = ss.imagesAt(((0 * ssWidth, 0, ssWidth, ssHeight),
        (1 * ssWidth, 0, ssWidth, ssHeight),
        (2 * ssWidth, 0, ssWidth, ssHeight),
        (3 * ssWidth, 0, ssWidth, ssHeight),
        (0 * ssWidth, ssHeight, ssWidth, ssHeight),
        (1 * ssWidth, ssHeight, ssWidth, ssHeight),
        (2 * ssWidth, ssHeight, ssWidth, ssHeight),
        (3 * ssWidth, ssHeight, ssWidth, ssHeight)),
        scaling=(rect.width, rect.height))

    shoot = ss.imagesAt(((0 * ssWidth, 0, ssWidth, ssHeight),
        (1 * ssWidth, 0, ssWidth, ssHeight),
        (2 * ssWidth, 0, ssWidth, ssHeight),
        (3 * ssWidth, 0, ssWidth, ssHeight),
        (0 * ssWidth, ssHeight, ssWidth, ssHeight),
        (1 * ssWidth, ssHeight, ssWidth, ssHeight),
        (2 * ssWidth, ssHeight, ssWidth, ssHeight),
        (3 * ssWidth, ssHeight, ssWidth, ssHeight)),
        scaling=(rect.width, rect.height))

    dead = ss.imagesAt(((0 * ssWidth, 0, ssWidth, ssHeight),
        (0 * ssWidth, 0, ssWidth, ssHeight)),
        scaling=(rect.width, rect.height))

    animations = {AnimState.JUMP: Animation(jump, 1), AnimState.RUN: Animation(run, 1), 
        AnimState.SHOOT: Animation(shoot, 1), AnimState.DEAD: Animation(dead, 2, looped=False)}
    
    immuneTime = 0
    hp = 35

    enemyEntity = Entity(rect, collRect, speed, jumpSpeed, animations, animations[AnimState.JUMP], hp, immuneTime, projList, showCollRect=True)
    newEnemy = Enemy(enemyEntity, startPoint, endPoint, player)

    return newEnemy

def initPlayer(tileSize, x, y, projList):
    # Initialize player attributes
    rect = pygame.Rect((x, y), (90, 90))
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

    slide = ss.imagesAt(((0 * ssWidth, 8 * ssHeight, ssWidth, ssHeight), 
                        (1 * ssWidth, 8 * ssHeight, ssWidth, ssHeight), 
                        (2 * ssWidth, 8 * ssHeight, ssWidth, ssHeight), 
                        (3 * ssWidth, 8 * ssHeight, ssWidth, ssHeight), 
                        (4 * ssWidth, 8 * ssHeight, ssWidth, ssHeight), 
                        (5 * ssWidth, 8 * ssHeight, ssWidth, ssHeight), 
                        (6 * ssWidth, 8 * ssHeight, ssWidth, ssHeight), 
                        (7 * ssWidth, 8 * ssHeight, ssWidth, ssHeight)),
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
        AnimState.MELEE: Animation(melee, 1, looped=False), AnimState.SLIDE: Animation(slide, 0.4, looped=False),
        AnimState.DEAD: Animation(dead, 1.5, looped=False)
    }

    immuneTime = 3
    lifes = 3

    playerEntity = Entity(rect, collRect, speed, jumpSpeed, animations, animations[AnimState.JUMP], lifes, immuneTime, projList, showCollRect = True)
    player = Player(playerEntity, 100)

    return player