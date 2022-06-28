import click
import git
import re
# from icecream import ic
from pathlib import Path
from rich import pretty, print
from urllib.request import urlopen
from json import loads
from sys import exit

# verbose icecream
# ic.configureOutput(includeContext=True)

# if .git exists, use git to populate maintainer username
if Path('../.git').exists():
    r = git.Repo('../.git').config_reader()
    author = r.get_value('user', 'name')
    url = f"https://raw.githubusercontent.com/{author}/freshenv/master/fr-flavours.json"
    gist_reponse = urlopen(url)
else:
    url = "https://api.github.com/gists/c4709c540a7c29616c771ab642ed2b8b"
    gist_reponse = urlopen(url)

@click.command("flavours")
def flavours() -> None:
    """Show all available flavours for provisioning."""
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


if __name__ == "__main__":
    flavours()
