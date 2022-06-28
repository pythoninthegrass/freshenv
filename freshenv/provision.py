import dockerpty
import click
# import os
from decouple import AutoConfig
from docker import APIClient, errors
from freshenv.console import console
from freshenv.util import PythonLiteralOption
from freshenv.view import count_environents
from icecream import ic
from io import BytesIO
from os import getcwd, path
from pathlib import Path
from requests import exceptions, get
from rich import print
from typing import Dict, List

# verbose icecream
# ic.configureOutput(includeContext=True)

client: APIClient = None
current_directory = getcwd()
folder = path.basename(current_directory)
local_mount_binds = [f"{current_directory}:/home/{folder}:delegated"]
google_dns = ["8.8.8.8"]        # TODO: fallback DNS, override with typer

homedir = Path.home()
basedir = f"{homedir}/.freshenv"
config = AutoConfig(search_path=f"{basedir}")
freshenv_config_location = f"{basedir}/settings.ini"

if Path(freshenv_config_location).exists():
    author = config('USERNAME')
    url = config('GIST_URL')
else:
    author = "raiyanyahya"


def get_port_bindings(ports: List[str]) -> Dict:
    port_bindings = {}
    for port in ports:
        port_bindings[port] = port
    return port_bindings


def create_environment(flavour: str, command: str, ports: List[str], name: str, client: APIClient, tty: bool=True, stdin_open: bool=True) -> Dict:
    if name == "index":
        name = str(count_environents() + 1)
    container = client.create_container(
        name=f"freshenv_{name}",
        image=f"{author}/freshenv-flavours/{flavour}",
        stdin_open=stdin_open,
        tty=tty,
        command=command,
        volumes=["/home"],
        ports=ports,
        use_config_proxy=True,
        host_config=client.create_host_config(port_bindings=get_port_bindings(ports),userns_mode="host",privileged=True,dns=google_dns,binds=local_mount_binds))
    return container


def pull_and_try_again(flavour: str, command: str, ports: List[str], name: str, client: APIClient):
    try:
        with console.status("Flavour doesnt exist locally. Fetching flavour...", spinner="dots8Bit"):
            client.pull(f"ghcr.io/raiyanyahya/{flavour}/{flavour}")
        container = create_environment(flavour, command, ports, name, client)
        dockerpty.start(client, container)
    except (errors.ImageNotFound, exceptions.HTTPError):
        print(":x: flavour doesnt exist")

# TODO: set raw github url as default and override with typer
def get_dockerfile_path(flavour: str) -> bytes:
    req = get(f"https://raw.githubusercontent.com/{author}/freshenv-flavours/master/{flavour}")
    return req.text.encode('utf-8')

def build_environment(flavour: str, command: str, ports: List[str], name: str, client: APIClient):
    try:
        with console.status("Flavour doesnt exist locally. Building flavour...", spinner="dots8Bit"):
            [line for line in client.build(fileobj=BytesIO(get_dockerfile_path(flavour=flavour)), tag=f"{author}/freshenv-flavours/{flavour}", rm=True, pull=True, decode=True)] # pylint: disable=expression-not-assigned
        container = create_environment(flavour, command, ports, name, client)
        dockerpty.start(client, container)
    except (errors.APIError, exceptions.HTTPError):
        print(":x: Flavour could not be built or found.")


@click.command("provision")
@click.option("--flavour","-f",default="base", help="The flavour of the environment.",show_default=True)
@click.option("--command","-c", help="The command to execute at startup of environment.")
@click.option("--ports","-p", default='["3000","4000"]', cls=PythonLiteralOption, help="String list of ports to forward.", show_default=True)
@click.option("--name","-n", default="index", help="Name of your environment.", show_default=False)
def provision(flavour: str, command: str, ports: List[str], name: str) -> None:
    """Provision a developer environment."""
    try:
        client = APIClient(base_url="unix://var/run/docker.sock")
        container = create_environment(flavour, command, ports, name, client)
        dockerpty.start(client, container)
    except (errors.ImageNotFound,exceptions.HTTPError, errors.NotFound):
        build_environment(flavour, command, ports, name,client)
        #pull_and_try_again(flavour, command, ports, name,client) to be implemented in the cloud version
    except errors.DockerException:
        print(":cross_mark_button: Docker not installed or running. ")
    except Exception as e:
        print(f"Unknown exception: {e}")


# QA
# if __name__ == "__main__":
#     provision()
