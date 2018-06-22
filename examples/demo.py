from pathlib import Path

from mcpack import (DataPack, Advancement, Function, LootTable, Recipe,
                    FunctionTag)


pack = DataPack('Demo', 'This is a simple demo data pack.')

pack['demo:hello'] = Function('say Hello, world!')
pack['minecraft:load'] = FunctionTag(['demo:hello'])

pack['demo:test'] = Advancement(
    criteria={
        'impossible': {
            'trigger': 'minecraft:impossible'
        }
    },
    rewards={
        'recipes': ['demo:test_rewards/recipe'],
        'loot': ['demo:test_rewards/loot'],
        'function': 'demo:test_rewards/function'
    }
)

pack['demo:test_rewards/recipe'] = Recipe(
    type='crafting_shapeless',
    ingredients=[{'item': 'minecraft:dead_bush'}],
    result={'item': 'minecraft:command_block'}
)

pack['demo:test_rewards/loot'] = LootTable([{
    'rolls': 1,
    'entries': [{
        'type': 'item',
        'weight': 1,
        'name': 'minecraft:dead_bush'
    }]
}])

pack['demo:test_rewards/function'] = Function(
    'tellraw @s {"text":"Try crafting your dead bush!","color":"yellow"}'
)

pack.dump(
    Path.home() / 'AppData/Roaming/.minecraft/saves/mcpack/datapacks',
    overwrite=True
)
