from enum import Enum

AnimState = Enum('AnimState', 'IDLE RUN JUMP DOUBLE_JUMP SHOOT RUN_SHOOT JUMP_SHOOT MELEE JUMP_MELEE SLIDE DEAD')
Direction = Enum('Direction', 'RIGHT LEFT')
ProjType = Enum('ProjType', 'PRIMARY SECONDARY')
DAMAGE_VELX = 45
DAMAGE_VELY = 120