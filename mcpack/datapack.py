"""Object-oriented abstractions to create and edit Minecraft data packs.

Example usage:

    >>> # for demonstration purposes
    >>> datapacks = getfixture('tmpdir')

    >>> # creating a data pack
    >>> pack = DataPack('My cool pack', 'This is the description.')
    >>> pack['my_cool_pack:hello'] = Function('say hello')
    >>> for i in range(10):
    ...     pack[f'my_cool_pack:function_{i}'] = Function(f'say {i}')
    >>> pack.dump(datapacks)

    >>> # loading back the data pack
    >>> loaded_pack = DataPack.load(datapacks / pack.name)
    >>> pack == loaded_pack
    True
    >>> len(loaded_pack['my_cool_pack'].functions)
    11
    >>> loaded_pack['my_cool_pack'].functions['hello']
    Function(body='say hello')

    >>> # editing the data pack
    >>> loaded_pack['minecraft:load'] = FunctionTag(['my_cool_pack:hello'])
    >>> loaded_pack.dump(datapacks, overwrite=True)

    >>> # loading it again
    >>> DataPack.load(datapacks / loaded_pack.name)['minecraft'].function_tags
    {'load': FunctionTag(values=['my_cool_pack:hello'], replace=False)}
"""


__all__ = ['DataPack', 'Namespace', 'Advancement', 'Function', 'LootTable',
           'Recipe', 'Structure', 'BlockTag', 'ItemTag', 'FluidTag',
           'FunctionTag', 'EntityTypeTag']


import json
import pathlib
import shutil
from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional, Union
from dataclasses import dataclass, field, fields, asdict

from nbtlib import nbt, tag, schema


DATA_VERSION = 1519


def write_json(path, json_data):
    """Write pretty indented json data."""
    path.write_text(json.dumps(json_data, indent=4))


class NamespaceItem:
    """Base class for all namespace items."""

    folder = None
    extension = ''

    def dump(self, path):
        """Write the content of the item to a file."""
        pass

    @classmethod
    def load(cls, path):
        """Load an item from a file."""
        return cls()


class JsonItem(NamespaceItem):
    """Base class for namespace items saved as json files."""

    extension = '.json'

    def dump(self, path):
        write_json(path, {key: value for key, value in asdict(self).items()
                          if value is not None})

    @classmethod
    def load(cls, path):
        return cls.from_json(path.read_text())

    @classmethod
    def from_json(cls, json_string):
        """Create an item from a json string."""
        return cls(**json.loads(json_string))


@dataclass
class Advancement(JsonItem):
    """Minecraft advancement."""

    folder = 'advancements'

    display: Optional[dict] = None
    parent: Optional[str] = None
    criteria: dict = field(default_factory=dict)
    requirements: Optional[list] = None
    rewards: Optional[dict] = None


@dataclass
class Function(NamespaceItem):
    """Minecraft function."""

    folder = 'functions'
    extension = '.mcfunction'

    body: str = ''

    def dump(self, path):
        path.write_text(self.body)

    @classmethod
    def load(cls, path):
        return cls(path.read_text())


@dataclass
class LootTable(JsonItem):
    """Minecraft loot table."""

    folder = 'loot_tables'

    pools: list = field(default_factory=list)
    type: str = 'generic'
    functions: Optional[list] = None


@dataclass
class Recipe(JsonItem):
    """Minecraft recipe."""

    folder = 'recipes'

    type: str = 'crafting_shaped'
    group: Optional[str] = None
    pattern: list = field(default_factory=list)
    key: dict = field(default_factory=dict)
    ingredient: Optional[dict] = None
    ingredients: Optional[list] = None
    result: Union[dict, str] = field(default_factory=dict)
    experience: Optional[float] = None
    cookingtime: Optional[int] = None
    count: Optional[int] = None


StructureSchema = schema('StructureSchema', {
    'DataVersion': tag.Int,
    'author': tag.String,
    'size': tag.List[tag.Int],
    'palette': tag.List[schema('State', {
        'Name': tag.String,
        'Properties': tag.Compound,
    })],
    'palettes': tag.List[tag.List[schema('State', {
        'Name': tag.String,
        'Properties': tag.Compound,
    })]],
    'blocks': tag.List[schema('Block', {
        'state': tag.Int,
        'pos': tag.List[tag.Int],
        'nbt': tag.Compound,
    })],
    'entities': tag.List[schema('Entity', {
        'pos': tag.List[tag.Double],
        'blockPos': tag.List[tag.Int],
        'nbt': tag.Compound,
    })],
}, strict=True)


def item_property(name):
    return property(fget=lambda self: self.__getitem__(name),
                    fset=lambda self, value: self.__setitem__(name, value))


class Structure(NamespaceItem, StructureSchema):
    """Minecraft structure."""

    folder = 'structures'
    extension = '.nbt'

    data_version = item_property('DataVersion')
    author = item_property('author')
    size = item_property('size')
    palette = item_property('palette')
    palettes = item_property('palettes')
    blocks = item_property('blocks')
    entities = item_property('entities')

    def __init__(self, *args, data_version=DATA_VERSION, **kwargs):
        self.author = ''
        self.size = [0, 0, 0]
        self.palette = []
        self.palettes = []
        self.blocks = []
        self.entities = []

        super().__init__(*args, **kwargs)
        self.data_version = data_version

    def dump(self, path):
        nbt.File({'': self}, gzipped=True).save(path)

    @classmethod
    def load(cls, path):
        return cls(nbt.load(path, gzipped=True).root)


@dataclass
class TagItem(JsonItem):
    """Base class for tag items."""

    values: List[str] = field(default_factory=list)
    replace: bool = False


class BlockTag(TagItem):
    """Minecraft block tag."""

    folder = 'tags/blocks'


class ItemTag(TagItem):
    """Minecraft item tag."""

    folder = 'tags/items'


class FluidTag(TagItem):
    """Minecraft fluid tag."""

    folder = 'tags/fluids'


class FunctionTag(TagItem):
    """Minecraft function tag."""

    folder = 'tags/functions'


class EntityTypeTag(TagItem):
    """Minecraft entity type tag."""

    folder = 'tags/entity_types'


@dataclass
class Namespace:
    """Minecraft namespace."""

    advancements: Dict[str, Advancement] = field(default_factory=dict)
    functions: Dict[str, Function] = field(default_factory=dict)
    loot_tables: Dict[str, LootTable] = field(default_factory=dict)
    recipes: Dict[str, Recipe] = field(default_factory=dict)
    structures: Dict[str, Structure] = field(default_factory=dict)
    block_tags: Dict[str, BlockTag] = field(default_factory=dict)
    item_tags: Dict[str, ItemTag] = field(default_factory=dict)
    fluid_tags: Dict[str, FluidTag] = field(default_factory=dict)
    function_tags: Dict[str, FunctionTag] = field(default_factory=dict)
    entity_type_tags: Dict[str, EntityTypeTag] = field(default_factory=dict)

    def __post_init__(self):
        self._type_items = {field.type.__args__[1]: getattr(self, field.name)
                            for field in fields(self)}

    def __setitem__(self, key, value):
        self._type_items[type(value)][key] = value

    def dump(self, path):
        for item_type, item_dict in self._type_items.items():
            base_path = path / item_type.folder

            for name, item in item_dict.items():
                item_path = base_path / (name + item_type.extension)
                item_path.parent.mkdir(parents=True, exist_ok=True)
                item.dump(item_path)

    @classmethod
    def load(cls, path):
        self = cls()

        for item_type, item_dict in self._type_items.items():
            base_path = path / item_type.folder
            if not base_path.is_dir():
                continue
            depth = len(base_path.parts)

            for item_path in base_path.rglob('*' + item_type.extension):
                name = '/'.join(item_path.parts[depth:-1] + (item_path.stem,))
                item_dict[name] = item_type.load(item_path)

        return self


@dataclass
class DataPack:
    """Minecraft data pack."""

    name: str
    description: str
    namespaces: DefaultDict[str, Namespace] = field(
        default_factory=lambda: defaultdict(Namespace), init=False, repr=False
    )

    pack_format: int = 1

    @property
    def mcmeta(self):
        return {
            'pack': {
                'pack_format': self.pack_format,
                'description': self.description
            }
        }

    def __getitem__(self, key):
        return self.namespaces[key]

    def __setitem__(self, key, value):
        namespace, _, item_path = key.partition(':')
        if item_path:
            self.namespaces[namespace][item_path] = value
        else:
            self.namespaces[namespace] = value

    def dump(self, path='.', overwrite=False):
        output_path = pathlib.Path(path) / self.name

        if output_path.is_dir():
            if overwrite:
                shutil.rmtree(output_path)
            else:
                raise ValueError(f'The directory "{output_path.resolve()}" '
                                 'already exists')

        output_path.mkdir(parents=True)
        write_json(output_path / 'pack.mcmeta', self.mcmeta)
        data_path = output_path / 'data'

        for name, namespace in self.namespaces.items():
            namespace.dump(data_path / name)

    @classmethod
    def load(cls, path):
        pack_path = pathlib.Path(path)
        meta = json.loads((pack_path / 'pack.mcmeta').read_text())['pack']

        self = cls(pack_path.name, meta['description'], meta['pack_format'])
        data_path = pack_path / 'data'

        if data_path.is_dir():
            for namespace_path in data_path.iterdir():
                self[namespace_path.name] = Namespace.load(namespace_path)

        return self
