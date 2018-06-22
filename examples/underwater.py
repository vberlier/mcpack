from pathlib import Path

from mcpack import DataPack, Advancement


pack = DataPack('Under the sea', 'Improve the underwater experience.')

pack['under_the_sea:underwater/root'] = Advancement(
    display={
        'title': 'Swimming',
        'description': 'Dipping your toes in the water',
        'icon': {
            'item': 'minecraft:tube_coral'
        },
        'background': 'minecraft:textures/gui/advancements/backgrounds/stone.png'
    },
    criteria={
        'swim': {
            'trigger': 'minecraft:enter_block',
            'conditions': {
                'block': 'minecraft:water'
            }
        }
    },
    rewards={
        'experience': 10
    }
)

for fish in ('cod', 'salmon', 'pufferfish'):
    pack[f'under_the_sea:underwater/kill_{fish}'] = Advancement(
        display={
            'title': f'{fish.capitalize()} for dinner',
            'description': f'Kill a {fish}',
            'icon': {
                'item': f'minecraft:{fish}'
            },
        },
        parent='under_the_sea:underwater/root',
        criteria={
            'kill_fish': {
                'trigger': 'minecraft:player_killed_entity',
                'conditions': {
                    'entity': {
                        'type': fish
                    }
                }
            }
        },
        rewards={
            'experience': 10
        }
    )

pack.dump(
    Path.home() / 'AppData/Roaming/.minecraft/saves/mcpack/datapacks',
    overwrite=True
)
