from mcpack import DataPack


def test_empty_data_pack(tmpdir):
    pack = DataPack('Some empty pack', 'This is the description of my pack.')
    pack.dump(tmpdir)

    assert DataPack.load(tmpdir / pack.name) == pack
