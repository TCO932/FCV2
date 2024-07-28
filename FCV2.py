from typing import Literal
from FCV2_Classes import Module, Effect, EffectedMachine, ASSENBLING_MACHINE_3, PRODUCTIVITY_MODULE_3, SPEED_MODULE_3, Machine
from utility import *
from paths import PATHS

MISCELLANEOUS = read(PATHS.MISCELLANEOUS)
RECIPES = read(PATHS.RECIPES)

def calcEffect(effects: dict[int: Module]) -> Effect:
    resEffect = Effect()
    for amount, module in effects.items():
        resEffect.productivity += module.productivity * amount
        resEffect.speed += module.speed * amount
    return resEffect
    
def placeholder(): pass

def setEffects(machine: Machine, effects: dict[Module: int], mode: Literal['FULL', 'ONLY_PROD', 'CUSTOM'] = 'CUSTOM') -> EffectedMachine:
    """
    FULL (max amount beacons with 2 tier 3 speed modules, max amount tier 3 prod modules); 

    ONLY_PROD (max amount tier 3 prod modules);

    CUSTOM (default value, custom beacons and speed modules amount, custom speed module tiers)
    """

    def FullMode():
        machine = ASSENBLING_MACHINE_3
        effects: dict[int: Module] = {
            machine.slots: PRODUCTIVITY_MODULE_3, 12: SPEED_MODULE_3 #TODO: fix 12 in future
        }
        effectedMachine = EffectedMachine(machine)
        effect = calcEffect(effects)
        effectedMachine.productivity = effect.productivity
        effectedMachine.speedInGame = machine.speed * (1 + effect.speed)
        effectedMachine.speed = machine.speed * (1 + effect.speed) * (1 + effect.productivity) #TODO: check this in game

        return effectedMachine

    def customMode():

        return 

    switcher = {}
    switcher['FULL'] = FullMode
    switcher['ONLY_PROD'] = placeholder
    switcher['CUSTOM'] = customMode

    def switch_case(case):
        return switcher.get(case, lambda: customMode)()

    return switch_case(mode)
    

# update({}, PATHS.MISCELLANEOUS)
# test(PATHS.MISCELLANEOUS)

effectedMachine = setEffects(None, None, 'FULL')
print(effectedMachine)