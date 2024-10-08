from classes import Item, Machine, Module

PRODUCTIVITY_MODULE_1 = Module('productivity-module', 0.04, -0.05)
PRODUCTIVITY_MODULE_2 = Module('productivity-module-2', 0.06, -0.1)
PRODUCTIVITY_MODULE_3 = Module('productivity-module-3', 0.1, -0.15)

SPEED_MODULE_1 = Module('speed-module', 0.0, 0.2)
SPEED_MODULE_2 = Module('speed-module-2', 0.0, 0.3)
SPEED_MODULE_3 = Module('speed-module-3', 0.0, 0.5)

MODULES = {
    'productivity-module': PRODUCTIVITY_MODULE_1,
    'productivity-module-2': PRODUCTIVITY_MODULE_2,
    'productivity-module-3': PRODUCTIVITY_MODULE_3,
    'speed-module': SPEED_MODULE_1,
    'speed-module-2': SPEED_MODULE_2,
    'speed-module-3': SPEED_MODULE_3,
}

MINING_PROD = 3.3

ASSENBLING_MACHINE_1 = Machine('assembling-machine-1', 0, 0.5, 0, 12, 'assembling-machine')
ASSENBLING_MACHINE_2 = Machine('assembling-machine-2', 2, 0.75, 0, 12, 'assembling-machine')
ASSENBLING_MACHINE_3 = Machine('assembling-machine-3', 4, 1.25, 0, 12, 'assembling-machine')
ELECTRIC_FURNACE = Machine('electric-furnace', 2, 2, 0, 12, 'furnace')
OIL_REFINERY = Machine('oil-refinery', 3, 1, 0, 16, 'oil-refinery')
CHEMICAL_PLANT = Machine('chemical-plant', 3, 1, 0, 12, 'chemical-plant')
CENTRIFUGE = Machine('centrifuge', 2, 2, 0, 12, 'centrifuge')
# LAB = Machine('lab', 2, 1, 0, 12, 'lab')
LAB_MAX_SPEED = Machine('lab', 2, 3.5, 0, 12, 'lab')
ROCKET_SILO = Machine('rocket-silo', 4, 1, 0, 20, 'rocket-silo')
ELECTRIC_MINING_FRILL = Machine('electric-mining-drill', 3, 0.5, MINING_PROD, 12, 'mining-drill')

MACHINES = {
    'assembling-machine-1': ASSENBLING_MACHINE_1,
    'assembling-machine-2': ASSENBLING_MACHINE_2,
    'assembling-machine-3': ASSENBLING_MACHINE_3,
    'electric-furnace': ELECTRIC_FURNACE,
    'oil-refinery': OIL_REFINERY,
    'chemical-plant': CHEMICAL_PLANT,
    'centrifuge': CENTRIFUGE,
    # 'lab': LAB,
    'lab': LAB_MAX_SPEED,
    'rocket-silo': ROCKET_SILO,
    'mining-drill': ELECTRIC_MINING_FRILL,
}

ASSENBLING_MACHINES = {
    'assembling-machine-1': ASSENBLING_MACHINE_1, 
    'assembling-machine-2': ASSENBLING_MACHINE_2, 
    'assembling-machine-3': ASSENBLING_MACHINE_3, 
}

ITEMS = {
    'research': Item(
        name='lab',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/lab.png',
        production_time=60,
        quantity=1,
        recipe={'automation-science-pack': 1, 'logistic-science-pack': 1, 'chemical-science-pack': 1, 'production-science-pack': 1, 'utility-science-pack': 1, 'space-science-pack': 1},
        machineType='lab',
    ),
    'radar': Item(
        name='radar',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/radar.png',
        production_time=0.5,
        quantity=1,
        recipe={'iron-plate': 10, 'iron-gear-wheel': 5, 'electronic-circuit': 5},
        machineType='assembling-machine',
        no_prod=True
    ),
    'solar-panel': Item(
        name='solar-panel',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/solar-panel.png',
        production_time=10,
        quantity=1,
        recipe={'copper-plate': 5, 'steel-plate': 5, 'electronic-circuit': 15},
        machineType='assembling-machine',
        no_prod=True
    ),
    'accumulator': Item(
        name='accumulator',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/accumulator.png',
        production_time=10,
        quantity=1,
        recipe={'iron-plate': 2, 'battery': 5},
        machineType='assembling-machine',
        no_prod=True
    ),
    'satellite': Item(
        name='satellite',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/satellite.png',
        production_time=5,
        quantity=1,
        recipe={'processing-unit': 100, 'low-density-structure': 100, 'rocket-fuel': 50, 'solar-panel': 100, 'accumulator': 100, 'radar': 5},
        machineType='assembling-machine',
        no_prod=True
    ),
    'space-science-pack': Item(
        name='space-science-pack',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/space-science-pack.png',
        production_time=40.33,
        quantity=1000,
        recipe={'rocket-part': 100, 'satellite': 1},
        machineType='rocket-silo'
    ),
    'advanced-circuit': Item(
        name='advanced-circuit',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/advanced-circuit.png',
        production_time=6,
        quantity=1,
        recipe={'copper-cable': 4, 'electronic-circuit': 2, 'plastic-bar': 2},
        machineType='assembling-machine'
    ),
    'automation-science-pack': Item(
        name='automation-science-pack',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/automation-science-pack.png',
        production_time=5,
        quantity=1,
        recipe={'copper-plate': 1, 'iron-gear-wheel': 1},
        machineType='assembling-machine'
    ),
    'battery': Item(
        name='battery',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/battery.png',
        production_time=4,
        quantity=1,
        recipe={'copper-plate': 1, 'iron-plate': 1, 'sulfuric-acid': 20},
        machineType='chemical-plant'
    ),
    'chemical-science-pack': Item(
        name='chemical-science-pack',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/chemical-science-pack.png',
        production_time=24,
        quantity=2,
        recipe={'advanced-circuit': 3, 'engine-unit': 2, 'sulfur': 1},
        machineType='assembling-machine'
    ),
    'coal': Item(
        name='coal',
        elementary=True,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/coal.png',
        production_time=0,
        quantity=0,
        recipe={},
        machineType='mining-drill'
    ),
    'copper-cable': Item(
        name='copper-cable',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/copper-cable.png',
        production_time=0.5,
        quantity=2,
        recipe={'copper-plate': 1},
        machineType='assembling-machine'
    ),
    'copper-ore': Item(
        name='copper-ore',
        elementary=True,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/copper-ore.png',
        production_time=0,
        quantity=0,
        recipe={},
        machineType='mining-drill'
    ),
    'copper-plate': Item(
        name='copper-plate',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/copper-plate.png',
        production_time=3.2,
        quantity=1,
        recipe={'copper-ore': 1},
        machineType='furnace'
    ),
    'effectivity-module': Item(
        name='effectivity-module',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/effectivity-module.png',
        production_time=15,
        quantity=1,
        recipe={'advanced-circuit': 5, 'electronic-circuit': 5},
        machineType='assembling-machine',
        no_prod=True
    ),
    'electric-engine-unit': Item(
        name='electric-engine-unit',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/electric-engine-unit.png',
        production_time=10,
        quantity=1,
        recipe={'electronic-circuit': 2, 'engine-unit': 1, 'lubricant': 15},
        machineType='assembling-machine'
    ),
    'electric-furnace': Item(
        name='electric-furnace',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/electric-furnace.png',
        production_time=5,
        quantity=1,
        recipe={'advanced-circuit': 5, 'steel-plate': 10, 'stone-brick': 10},
        machineType='assembling-machine',
        no_prod=True
    ),
    'electronic-circuit': Item(
        name='electronic-circuit',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/electronic-circuit.png',
        production_time=0.5,
        quantity=1,
        recipe={'copper-cable': 3, 'iron-plate': 1},
        machineType='assembling-machine'
    ),
    'engine-unit': Item(
        name='engine-unit',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/engine-unit.png',
        production_time=10,
        quantity=1,
        recipe={'iron-gear-wheel': 1, 'pipe': 2, 'steel-plate': 1},
        machineType='assembling-machine'
    ),
    'firearm-magazine': Item(
        name='firearm-magazine',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/firearm-magazine.png',
        production_time=1,
        quantity=1,
        recipe={'iron-plate': 4},
        machineType='assembling-machine'
    ),
    'flying-robot-frame': Item(
        name='flying-robot-frame',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/flying-robot-frame.png',
        production_time=20,
        quantity=1,
        recipe={'battery': 2, 'electric-engine-unit': 1,
                'electronic-circuit': 3, 'steel-plate': 1},
        machineType='assembling-machine'
    ),
    'grenade': Item(
        name='grenade',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/grenade.png',
        production_time=8,
        quantity=1,
        recipe={'coal': 10, 'iron-plate': 5},
        machineType='assembling-machine',
        no_prod=True
    ),
    'inserter': Item(
        name='inserter',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/inserter.png',
        production_time=0.5,
        quantity=1,
        recipe={'electronic-circuit': 1, 'iron-gear-wheel': 1, 'iron-plate': 1},
        machineType='assembling-machine',
        no_prod=True
    ),
    'iron-gear-wheel': Item(
        name='iron-gear-wheel',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/iron-gear-wheel.png',
        production_time=0.5,
        quantity=1,
        recipe={'iron-plate': 2},
        machineType='assembling-machine'
    ),
    'iron-ore': Item(
        name='iron-ore',
        elementary=True,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/iron-ore.png',
        production_time=1,
        quantity=1,
        recipe={},
        machineType='mining-drill'
    ),
    'iron-plate': Item(
        name='iron-plate',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/iron-plate.png',
        production_time=3.2,
        quantity=1,
        recipe={'iron-ore': 1},
        machineType='furnace'
    ),
    'iron-stick': Item(
        name='iron-stick',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/iron-stick.png',
        production_time=0.5,
        quantity=2,
        recipe={'iron-plate': 1},
        machineType='assembling-machine'
    ),
    'logistic-science-pack': Item(
        name='logistic-science-pack',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/logistic-science-pack.png',
        production_time=6,
        quantity=1,
        recipe={'inserter': 1, 'transport-belt': 1},
        machineType='assembling-machine'
    ),
    'low-density-structure': Item(
        name='low-density-structure',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/low-density-structure.png',
        production_time=20,
        quantity=1,
        recipe={'copper-plate': 20, 'plastic-bar': 5, 'steel-plate': 2},
        machineType='assembling-machine'
    ),
    'lubricant': Item(
        name='lubricant',
        elementary=True,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/lubricant.png',
        production_time=0,
        quantity=0,
        recipe={},
        machineType='chemical-plant'
    ),
    'military-science-pack': Item(
        name='military-science-pack',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/military-science-pack.png',
        production_time=10,
        quantity=2,
        recipe={'grenade': 1, 'piercing-rounds-magazine': 1, 'stone-brick': 2},
        machineType='assembling-machine'
    ),
    'piercing-rounds-magazine': Item(
        name='piercing-rounds-magazine',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/piercing-rounds-magazine.png',
        production_time=3,
        quantity=1,
        recipe={'copper-plate': 5, 'firearm-magazine': 1, 'steel-plate': 1},
        machineType='assembling-machine',
        no_prod=True
    ),
    'pipe': Item(
        name='pipe',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/pipe.png',
        production_time=0.5,
        quantity=1,
        recipe={'iron-plate': 1},
        machineType='assembling-machine'
    ),
    'plastic-bar': Item(
        name='plastic-bar',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/plastic-bar.png',
        production_time=1,
        quantity=2,
        recipe={'coal': 1, 'petroleum-gas': 20},
        machineType='chemical-plant'
    ),
    'processing-unit': Item(
        name='processing-unit',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/processing-unit.png',
        production_time=10,
        quantity=1,
        recipe={'advanced-circuit': 2,
                'electronic-circuit': 20, 'sulfuric-acid': 5},
        machineType='assembling-machine'
    ),
    'production-science-pack': Item(
        name='production-science-pack',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/production-science-pack.png',
        production_time=21,
        quantity=3,
        recipe={'electric-furnace': 1, 'productivity-module': 1, 'rail': 30},
        machineType='assembling-machine'
    ),
    'productivity-module': Item(
        name='productivity-module',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/productivity-module.png',
        production_time=15,
        quantity=1,
        recipe={'advanced-circuit': 5, 'electronic-circuit': 5},
        machineType='assembling-machine',
        no_prod=True
    ),
    'rail': Item(
        name='rail',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/rail.png',
        production_time=0.5,
        quantity=2,
        recipe={'iron-stick': 1, 'steel-plate': 1, 'stone': 1},
        machineType='assembling-machine',
        no_prod=True
    ),
    'speed-module': Item(
        name='speed-module',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/speed-module.png',
        production_time=15,
        quantity=1,
        recipe={'advanced-circuit': 5, 'electronic-circuit': 5},
        machineType='assembling-machine',
        no_prod=True
    ),
    'steel-plate': Item(
        name='steel-plate',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/steel-plate.png',
        production_time=16,
        quantity=1,
        recipe={'iron-plate': 5},
        machineType='furnace'
    ),
    'stone': Item(
        name='stone',
        elementary=True,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/stone.png',
        production_time=0,
        quantity=0,
        recipe={},
        machineType='mining-drill'
    ),
    'stone-brick': Item(
        name='stone-brick',
        elementary=True,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/stone-brick.png',
        production_time=0,
        quantity=0,
        recipe={},
        machineType='furnace'
    ),
    'sulfur': Item(
        name='sulfur',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/sulfur.png',
        production_time=1,
        quantity=2,
        recipe={'water': 30, 'petroleum-gas': 30},
        machineType='chemical-plant'
    ),
    'water': Item(
        name='water',
        elementary=True,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/water.png',
        production_time=0,
        quantity=0,
        recipe={},
        machineType='chemical-plant'
    ),
    'sulfuric-acid': Item(
        name='sulfuric-acid',
        elementary=True,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/sulfuric-acid.png',
        production_time=0,
        quantity=0,
        recipe={},
        machineType='chemical-plant'
    ),
    'petroleum-gas': Item(
        name='petroleum-gas',
        elementary=True,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/petroleum-gas.png',
        production_time=0,
        quantity=0,
        recipe={},
        machineType='chemical-plant'
    ),
    'rocket-part': Item(
        name='rocket-part',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/rocket-part.png',
        production_time=3,
        quantity=1,
        recipe={'rocket-control-unit': 10,
                'low-density-structure': 10, 'rocket-fuel': 10},
        machineType='rocket-silo'
    ),
    'rocket-fuel': Item(
        name='rocket-fuel',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/rocket-fuel.png',
        production_time=3,
        quantity=1,
        recipe={'solid-fuel': 10, 'light-oil': 10},
        machineType='assembling-machine'
    ),
    'solid-fuel': Item(
        name='solid-fuel',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/solid-fuel.png',
        production_time=2,
        quantity=1,
        recipe={'light-oil': 10},
        machineType='chemical-plant'
    ),
    'light-oil': Item(
        name='light-oil',
        elementary=True,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/light-oil.png',
        production_time=0,
        quantity=0,
        recipe={},
        machineType='chemical-plant'
    ),
    'rocket-control-unit': Item(
        name='rocket-control-unit',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/rocket-control-unit.png',
        production_time=30,
        quantity=1,
        recipe={'processing-unit': 1, 'speed-module': 1},
        machineType='assembling-machine'
    ),
    'transport-belt': Item(
        name='transport-belt',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/transport-belt.png',
        production_time=0.5,
        quantity=2,
        recipe={'iron-gear-wheel': 1, 'iron-plate': 1},
        machineType='assembling-machine',
        no_prod=True
    ),
    'uranium-ore': Item(
        name='uranium-ore',
        elementary=True,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/uranium-ore.png',
        production_time=0,
        quantity=0,
        recipe={},
        machineType='mining-drill'
    ),
    'utility-science-pack': Item(
        name='utility-science-pack',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/utility-science-pack.png',
        production_time=21,
        quantity=3,
        recipe={'flying-robot-frame': 1,
                'low-density-structure': 3, 'processing-unit': 2},
        machineType='assembling-machine'
    ),
    'wall': Item(
        name='wall',
        elementary=False,
        image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/wall.png',
        production_time=0.5,
        quantity=1,
        recipe={'stone-brick': 5},
        machineType='assembling-machine',
        no_prod=True
    ),
}