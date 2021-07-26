import pygame
import math
from Core import EnemyState
from Core.EnemyState import DeadState, JumpState
from Core.Constants import AnimState

class BossBehavior():
    def getState(self, boss, player):
        entity = boss.entity
        state = None

        if entity.currentHealth == 0:
            state = DeadState()
        elif entity.directionHit:
            state = HitState()
        elif not entity.grounded:
            state = JumpState()
        elif boss.playerInSight(player):
            state = ShootState()
        elif boss.stomp:
            state = StompState()
        else:
            state = IdleState()

        return state

class IdleState():
    def changeState(self, boss):
        boss.entity.velX = 0
        boss.entity.currAnim = boss.entity.animations[AnimState.IDLE]
        if not isinstance(boss.state, HitState) and not isinstance(boss.state, JumpState):
            boss.entity.currAnim.reset()

    def updateState(self, boss, GRAVITY):
        if boss.idleCounter >= boss.idleTime:
            boss.stomp = True
            boss.idleCounter = 0

class ShootState(EnemyState.ShootState):
    def changeState(self, boss):
        super().changeState(boss)

    def updateState(self, boss, GRAVITY):
        entity = boss.entity

        if entity.projTypes[0].reloadCounter >= entity.projTypes[0].reloadTime and math.floor(entity.currAnim.counter) == (len(entity.currAnim.frames) - 1):
            entity.addProjectile(entity.projTypes[0])
        
class HitState(EnemyState.HitState):
    def changeState(self, boss):
        super().changeState(boss)
        boss.entity.velY = 0
        boss.entity.velX = 0
    
    def updateState(self, boss, GRAVITY):
        super().updateState(boss, GRAVITY)

class StompState():
    def changeState(self, boss):
        boss.entity.currAnim = boss.entity.animations[AnimState.STOMP]
    
    def updateState(self, boss, GRAVITY):
        if boss.entity.currAnim.finished:
            boss.idleCounter = 0
            boss.stomp = False
            boss.entity.currAnim.reset()