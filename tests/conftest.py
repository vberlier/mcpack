import io
import zipfile
import pytest
import requests


def pytest_addoption(parser):
    parser.addoption('--vanilla', action='store_true', dest='vanilla',
                     default=False, help='test against the vanilla datapack')


MINECRAFT_VERSIONS = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'


DATAPACK_CACHE = {}


def download_version_datapack(url, directory):
    if url in DATAPACK_CACHE:
        return DATAPACK_CACHE[url]
    else:
        DATAPACK_CACHE[url] = directory

    client_url = requests.get(url).json()['downloads']['client']['url']
    jar = zipfile.ZipFile(io.BytesIO(requests.get(client_url).content))

    for filename in jar.namelist():
        if filename.startswith('data/'):
            jar.extract(filename, directory)

    mcmeta = directory / 'pack.mcmeta'
    mcmeta.write_text('{"pack": {"pack_format": 1, "description": ""}}')

    return directory


@pytest.fixture(scope='session', params=['release', 'snapshot'])
def vanilla(request, tmp_path_factory):
    if not request.config.getoption('--vanilla'):
        pytest.skip()

    manifest = requests.get(MINECRAFT_VERSIONS).json()
    latest = manifest['latest']

    version_url = next(v['url'] for v in manifest['versions']
                       if v['id'] == latest[request.param])

    directory = tmp_path_factory.mktemp('vanilla')
    return download_version_datapack(version_url, directory / 'release')
