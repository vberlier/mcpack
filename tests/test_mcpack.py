import pytest

from mcpack import (DataPack, Advancement, Function, LootTable, Recipe,
                    Structure, BlockTag, ItemTag, FluidTag, FunctionTag)


ALL_ITEM_TYPES = [Advancement, Function, LootTable, Recipe, Structure,
                  BlockTag, ItemTag, FluidTag, FunctionTag]


@pytest.fixture
def pack():
    return DataPack('My data pack', 'This is the description of my pack.')


def test_empty_data_pack(pack, tmpdir):
    pack.dump(tmpdir)
    assert DataPack.load(tmpdir / pack.name) == pack


@pytest.mark.parametrize('item_type', ALL_ITEM_TYPES)
def test_default_items(pack, tmpdir, item_type):
    pack['test:thing'] = item_type()
    pack.dump(tmpdir)
    assert DataPack.load(tmpdir / pack.name) == pack


def test_overlapping_names(pack, tmpdir):
    for item_type in ALL_ITEM_TYPES:
        pack['test:thing/subfolder'] = item_type()

    for item_type, items in pack['test']._type_items.items():
        assert items == {'thing/subfolder': item_type()}

    pack.dump(tmpdir)
    assert DataPack.load(tmpdir / pack.name) == pack
