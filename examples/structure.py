from pathlib import Path

from mcpack import DataPack, Structure
from nbtlib import tag


pack = DataPack('Structure example', 'This pack contains a custom structure.')

pack['structure_example:command_block'] = Structure(
    size=[1, 2, 1],
    palette=[
        {'Name': 'minecraft:command_block'},
        {'Name': 'minecraft:stone_button', 'Properties': {
             'face': tag.String('floor')
        }}
    ],
    blocks=[
        {'pos': [0, 0, 0], 'state': 0, 'nbt': {
            'Command': tag.String("say I'm a command block!")
        }},
        {'pos': [0, 1, 0], 'state': 1}
    ]
)

pack.dump(
    Path.home() / 'AppData/Roaming/.minecraft/saves/mcpack/datapacks',
    overwrite=True
)
