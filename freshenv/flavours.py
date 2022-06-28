import click
import re
from decouple import AutoConfig
from icecream import ic
from pathlib import Path
from rich import pretty, print
from urllib.request import urlopen
from json import loads
from sys import exit

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
    url = "https://api.github.com/gists/c4709c540a7c29616c771ab642ed2b8b"


@click.command("flavours")
def flavours() -> None:
    """Show all available flavours for provisioning."""
    gist_reponse = urlopen(url)
    if gist_reponse.getcode() == 200:
        gist_data = loads(gist_reponse.read().decode("utf-8"))
        if re.match(r"^https://raw.githubusercontent.com", url):
            flavour_list = gist_data['fr-flavours']
            print(f":mag: Found {len(flavour_list)} flavours:")
            for flavour in flavour_list:
                pretty.pprint(flavour)
        else:
            flavour_dict = loads(gist_data["files"]["fr-flavours.json"]["content"])
            print(f":mag: Found {len(flavour_dict['fr-flavours'])} flavours:")
            pretty.pprint(flavour_dict["fr-flavours"])
    else:
        print(":heavy_exclamation_mark: Could not fetch flavours.")
        exit(1)


# QA
# if __name__ == "__main__":
#     flavours()
