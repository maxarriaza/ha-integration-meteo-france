### Script to build distribution for Home Assistant usage ###
from argparse import ArgumentParser
from logging import getLogger
from shutil import copytree, make_archive
from pathlib import Path
from tomllib import loads
from json import dumps as json_dumps

_LOGGER = getLogger("Build")

_SRC_DIR = "src"
_CUSTOM_COMPONENTS_DIR = "custom_components"
_DIST_DIR = "dist"
_PYPROJECT_TOML = "pyproject.toml"

def _load_domain() -> str:
    """ Function to load domain for Home Assistant integration """
    _LOGGER.info("-> Loading Home Assistant integration domain")
    pyproject_path = Path(_PYPROJECT_TOML).absolute()
    pyproject_content = loads(pyproject_path.read_text())
    pyproject_homeassistant = pyproject_content.get("home-assistant")
    return pyproject_homeassistant["domain"]

def _init_custom_components(domain: str):
    """ Function to init dist directory """
    _LOGGER.info("-> Init custom_components folder")
    custom_components_path = Path(_CUSTOM_COMPONENTS_DIR).joinpath(domain).absolute()
    custom_components_path.mkdir(parents=True, exist_ok=True)

def _copy_src(domain: str):
    """ Function to copy source code into distribution folder """
    _LOGGER.info("-> Copying source code")
    source_path = Path(_SRC_DIR).absolute()
    custom_components_path = Path(_CUSTOM_COMPONENTS_DIR).joinpath(domain).absolute()
    copytree(source_path, custom_components_path, dirs_exist_ok=True)

def _generate_manifest(domain: str):
    """ Function to generate Home assistant integration manifest file """
    _LOGGER.info("-> Generating Home Assistant manifest")
    pyproject_path = Path(_PYPROJECT_TOML).absolute()
    pyproject_content = loads(pyproject_path.read_text())
    pyproject_project = pyproject_content.get("project")
    pyproject_homeassistant = pyproject_content.get("home-assistant")
    homeassistant_manifest = {
        "domain": domain,
        "version": pyproject_project["version"],
        "name": pyproject_homeassistant["name"],
        "requirements": pyproject_project["dependencies"] if not None else [],
        "config_flow": pyproject_homeassistant["config-flow"],
        "iot_class": pyproject_homeassistant["iot-class"],
        "integration_type": pyproject_homeassistant["integration-type"],
    }
    homeassistant_manifest_content = json_dumps(homeassistant_manifest, indent=4)
    homeassistant_manifest_path = Path(_CUSTOM_COMPONENTS_DIR).joinpath(homeassistant_manifest['domain']).joinpath("manifest.json")
    homeassistant_manifest_path.touch()
    homeassistant_manifest_path.write_text(homeassistant_manifest_content, encoding="utf-8")

def _generate_artifacts(artifact: str):
    """ Function to generate Home Assistant integration artifacts """
    _LOGGER.info("-> Generating Home Assistant integration artifacts")
    artifact_path = Path(_DIST_DIR).joinpath(artifact)
    make_archive(str(artifact_path), "zip", root_dir=".", base_dir=_CUSTOM_COMPONENTS_DIR)

def main():
    parser = ArgumentParser(description="Build project")
    parser.add_argument('--artifact', help="New version of the project")

    arguments = parser.parse_args()
    artifact = arguments.artifact

    _LOGGER.info(f"⚙️ Building project distribution")
    _domain = _load_domain()
    _init_custom_components(_domain)
    _copy_src(_domain)
    _generate_manifest(_domain)
    if artifact:
        _generate_artifacts(artifact)
    _LOGGER.info(f"✅ Project built successfully")

if __name__ == '__main__':
    main()