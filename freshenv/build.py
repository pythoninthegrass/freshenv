import click
from configparser import ConfigParser, SectionProxy
from decouple import AutoConfig
from docker import APIClient, errors
from freshenv.console import console
from freshenv.provision import get_dockerfile_path
from io import BytesIO
from jinja2 import Environment
from os import makedirs, path
from pathlib import Path
from requests import exceptions
from rich import print

# verbose icecream
# ic.configureOutput(includeContext=True)

homedir = Path.home()
basedir = f"{homedir}/.freshenv"
config = AutoConfig(search_path=f"{basedir}")
freshenv_config_location = f"{basedir}/settings.ini"

# TODO: validate config file
if Path(freshenv_config_location).exists():
    author = config('USERNAME')
    url = config('GIST_URL')
else:
    author = "raiyanyahya"


def create_dockerfile(base: str, install: str, cmd: str) -> str:
    contents = get_dockerfile_path("simple")
    template = Environment(autoescape=True).from_string(str(contents.decode("utf-8")))
    build_template = template.render(base=base, install=install, cmd=cmd)
    return build_template


def config_exists() -> bool:
    if not path.isfile(freshenv_config_location):
        return False
    return True


def get_key_values_from_config(flavour: str) -> SectionProxy:
    config = ConfigParser()
    config.read(freshenv_config_location)
    return config[flavour]


def env_exists(flavour: str) -> bool:
    config = ConfigParser()
    config.read(freshenv_config_location)
    if flavour not in config.sections():
        return False
    return True


def mandatory_keys_exists(flavour: str) -> bool:
    config = ConfigParser()
    config.read(freshenv_config_location)
    if "base" not in config[flavour]:
        return False
    if "install" not in config[flavour]:
        return False
    if "cmd" not in config[flavour]:
        return False
    return True


def create_file(location: str) -> None:
    makedirs(path.dirname(location), exist_ok=True)
    open(location, "w", encoding="utf8").close()


def run_checks(flavour: str) -> bool:
    if not config_exists():
        print(f":card_index: No config file found. Creating an empty config at {freshenv_config_location}.")
        create_file(freshenv_config_location)
        return False
    if not env_exists(flavour):
        print(f":exclamation_mark:configuration for custom flavour {flavour} does not exist.")
        return False
    if not mandatory_keys_exists(flavour):
        print(":exclamation_mark: missing mandatory keys in configuration for custom environment {flavour}.")
        return False
    return True

@click.command("build")
@click.argument("flavour")
@click.option('--logs', '-l', is_flag=True, help="Show build logs")
def build(flavour: str, logs: bool) -> None:
    """Build a custom freshenv flavour."""
    if not run_checks(flavour):
        return

    flavour_config = get_key_values_from_config(flavour)
    flavour_dockerfile = create_dockerfile(flavour_config["base"], flavour_config["install"], flavour_config["cmd"])
    try:
        client = APIClient(base_url="unix://var/run/docker.sock")
        with console.status("Building custom flavour...", spinner="point"):
            for line in client.build(fileobj=BytesIO(flavour_dockerfile.encode("utf-8")), tag=f"{author}/freshenv-flavours/{flavour}", rm=True, pull=True, decode=True):
                if "errorDetail" in line:
                    raise Exception(line["errorDetail"]["message"])
                if logs:
                    print(line)
        print(f":party_popper: Successfully built custom flavour {flavour}. You can provision it by running [bold]freshenv provision -f {flavour}[/bold].")
    except (errors.APIError, exceptions.HTTPError):
        print(":x: Custom flavour could not be built. Try again after cleaning up with [bold]fr clean --force [/bold]")
    except Exception as e:
        print(f":x: Custom flavour could not be built due to the error: {e}.")
