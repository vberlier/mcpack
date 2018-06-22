# mcpack

[![Build Status](https://travis-ci.com/vberlier/mcpack.svg?branch=master)](https://travis-ci.com/vberlier/mcpack)
[![PyPI](https://img.shields.io/pypi/v/mcpack.svg)](https://pypi.org/project/mcpack/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mcpack.svg)](https://pypi.org/project/mcpack/)

> A python library for programmatically creating and editing [Minecraft data packs](https://minecraft.gamepedia.com/Data_pack). Requires python 3.7.

```py
from mcpack import DataPack, Function

pack = DataPack('My cool pack', 'This is the description of my pack.')

pack['my_cool_pack:hello'] = Function(
    'say Hello, world!\n'
    'give @s minecraft:dead_bush\n'
)

pack.dump('.minecraft/saves/New World/datapacks')
```

## Installation

Make sure that you're using python 3.7 or above. The package can be installed with `pip`.

```sh
$ pip install mcpack
```

## Using mcpack

> Check out the [examples](https://github.com/vberlier/mcpack/tree/master/examples) for a quick overview.

### Creating a data pack

The `DataPack` class represents a minecraft data pack.

```py
from mcpack import DataPack

pack = DataPack('Test', 'Test description.')

print(pack.name)  # 'Test'
print(pack.description)  # 'Test description.'
print(pack.pack_format)  # 1
print(pack.namespaces)  # defaultdict(<class 'mcpack.Namespace'>, {})
```

You can load already existing data packs using the `load` class method.

```py
from mcpack import DataPack

pack = DataPack.load('.minecraft/save/New World/datapacks/Test')
```

The `dump` method allows you to generate the actual Minecraft data pack. The method will raise a `ValueError` if the data pack already exists. You can explicitly overwrite the existing data pack by setting the `overwrite` argument to `True`.

```py
from mcpack import DataPack

pack = DataPack('Test', 'Test description.')

pack.dump('.minecraft/save/New World/datapacks')
pack.dump('.minecraft/save/New World/datapacks', overwrite=True)
```

### Namespaces

`Namespace` objects hold references to data pack items using a separate dictionary for each type of item.

```py
from mcpack import Namespace

namespace = Namespace()

print(namespace.advancements)  # {}
print(namespace.functions)  # {}
print(namespace.loot_tables)  # {}
print(namespace.recipes)  # {}
print(namespace.structures)  # {}
print(namespace.block_tags)  # {}
print(namespace.item_tags)  # {}
print(namespace.fluid_tags)  # {}
print(namespace.function_tags)  # {}
```

You can add namespaces to `DataPack` objects using the `namespaces` attribute. Note that you won't usually need to create namespaces yourself. If you want to edit a namespace, you just need to retrieve it and the `defaultdict` will create an empty namespace for you if it doesn't already exist.

```py
from mcpack import DataPack

pack = DataPack('Test', 'Test description.')

print(pack.namespaces['test'])  # Namespace(...)
```

To make things even more convenient, the `__getitem__` and `__setitem__` methods of `DataPack` objects are mapped to the `namespaces` attribute. It means that you can access namespaces directly from the `DataPack` object.

```py
print(pack['test'])  # Namespace(...)
```

Adding items to namespaces is pretty straight-forward. Simply add them to their respective dictionaries.

```py
from mcpack import (DataPack, Advancement, Function, LootTable, Recipe,
                    Structure, BlockTag, ItemTag, FluidTag, FunctionTag)

pack = DataPack('Test', 'Test description.')

pack['test'].advancements['foo'] = Advancement(...)
pack['test'].functions['foo/spam'] = Function(...)
pack['test'].loot_tables['foo/egg'] = LootTable(...)
pack['test'].recipes['bar'] = Recipe(...)
pack['test'].structures['bar/spam'] = Structure(...)
pack['test'].block_tags['bar/egg'] = BlockTag(...)
pack['test'].item_tags['baz'] = ItemTag(...)
pack['test'].fluid_tags['baz/spam'] = FluidTag(...)
pack['test'].function_tags['baz/egg'] = FunctionTag(...)
```

You can also use the `DataPack` object directly. The `__setitem__` method actually checks if the key looks like `namespace:path` and dispatches the item automatically. We can now simplify the previous piece of code quite a bit.

```py
from mcpack import (DataPack, Advancement, Function, LootTable, Recipe,
                    Structure, BlockTag, ItemTag, FluidTag, FunctionTag)

pack = DataPack('Test', 'Test description.')

pack['test:foo'] = Advancement(...)
pack['test:foo/spam'] = Function(...)
pack['test:foo/egg'] = LootTable(...)
pack['test:bar'] = Recipe(...)
pack['test:bar/spam'] = Structure(...)
pack['test:bar/egg'] = BlockTag(...)
pack['test:baz'] = ItemTag(...)
pack['test:baz/spam'] = FluidTag(...)
pack['test:baz/egg'] = FunctionTag(...)
```

### Advancements

`Advancement` objects represent Minecraft advancements.

```py
from mcpack import DataPack, Advancement

pack = DataPack('Test', 'Test description.')
pack['test:foo'] = Advancement()

advancement = pack['test'].advancements['foo']

print(advancement.display)  # None
print(advancement.parent)  # None
print(advancement.criteria)  # {}
print(advancement.requirements)  # None
print(advancement.rewards)  # None
```

All the attributes can be set in the constructor. They mirror the root properties of the advancement JSON file format.

> Check out the [wiki](https://minecraft.gamepedia.com/Advancements) for further details.

### Functions

`Function` objects represent Minecraft functions.

```py
from mcpack import DataPack, Function

pack = DataPack('Test', 'Test description.')
pack['test:foo'] = Function()

function = pack['test'].functions['foo']

print(function.body)  # ''
```

The `body` attribute can be set in the constructor. The body of the function corresponds to the content of the actual `.mcfunction` file.

> Check out the [wiki](https://minecraft.gamepedia.com/Function) for further details.

### Loot tables

`LootTable` objects represent Minecraft loot tables.

```py
from mcpack import DataPack, LootTable

pack = DataPack('Test', 'Test description.')
pack['test:foo'] = LootTable()

loot_table = pack['test'].loot_tables['foo']

print(loot_table.pools)  # []
```

The `pools` attribute can be set in the constructor. It mirrors the `pools` property of the loot table JSON file format.

> Check out the [wiki](https://minecraft.gamepedia.com/Loot_table) for further details.

### Recipes

`Recipe` objects represent Minecraft recipes.

```py
from mcpack import DataPack, Recipe

pack = DataPack('Test', 'Test description.')
pack['test:foo'] = Recipe()

recipe = pack['test'].recipes['foo']

print(recipe.type)  # 'crafting_shaped'
print(recipe.group)  # None
print(recipe.pattern)  # []
print(recipe.key)  # {}
print(recipe.ingredient)  # None
print(recipe.ingredients)  # None
print(recipe.result)  # {}
print(recipe.experience)  # None
print(recipe.cookingtime)  # None
```

All the attributes can be set in the constructor. They mirror the root properties of the recipe JSON file format.

> Check out the [wiki](https://minecraft.gamepedia.com/Recipe) for further details.

### Structures

`Structure` objects represent Minecraft structures.

```py
from mcpack import DataPack, Structure

pack = DataPack('Test', 'Test description.')
pack['test:foo'] = Structure()

structure = pack['test'].structures['foo']

print(structure.data_version)  # Int(1503)
print(structure.author)  # String('')
print(structure.size)  # List[Int]([0, 0, 0])
print(structure.palette)  # List[State]([])
print(structure.blocks)  # List[Block]([])
print(structure.entities)  # List[Entity]([])
```

All the attributes can be set in the constructor. They mirror the root properties of the structure NBT file format. `mcpack` uses [`nbtlib`](https://github.com/vberlier/nbtlib) to manipulate nbt data. The `Structure` class inherits from an `nbtlib` schema that takes care of wrapping python values with the appropriate nbt tags.

> Check out the [wiki](https://minecraft.gamepedia.com/Structure_block_file_format) for further details.

### Tags

`BlockTag`, `ItemTag`, `FluidTag` and `FunctionTag` objects represent Minecraft block, item, fluid and function tags respectively. They are all identical in structure, the only difference between them is the namespace directory they get written to.

```py
from mcpack import DataPack, BlockTag

pack = DataPack('Test', 'Test description.')
pack['test:foo'] = BlockTag()

block_tag = pack['test'].block_tags['foo']

print(block_tag.values)  # []
print(block_tag.replace)  # False
```

The `values` and `replace` attributes can be set in the constructor. They mirror the root properties of the tag JSON file format.

> Check out the [wiki](https://minecraft.gamepedia.com/Tag) for further details.

## Contributing

Contributions are welcome. This project uses [`poetry`](https://poetry.eustace.io/) so you'll need to install it first if you want to be able to work with the project locally.

```sh
$ curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

You should now be able to install the required dependencies.

```sh
$ poetry install
```

You can run the tests using `pytest`.

```sh
$ poetry run pytest
```

---

License - [MIT](https://github.com/vberlier/mcpack/blob/master/LICENSE)
