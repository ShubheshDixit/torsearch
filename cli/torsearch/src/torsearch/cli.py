import os
from typing import Optional

import typer

from torsearch import (__app_name__, __version__)

from torsearch import torSearch

from torsearch.constants import SOURCES

from torsearch.utils.config import create_config_file, load_config

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


def get_handler() -> torSearch.Handler:
    return torSearch.Handler()


def search(query: typer.Context, src=1, page=1):
    print(query.to_info_dict())
    if query:
        typer.echo(
            f"Searching for {query} from {SOURCES[src]} in {page} {'pages' if page > 1 else 'page'} ...")
        handler = get_handler()
        handler.search(query, src, page)
        typer.echo(f"Done!")

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command(help="Search for a torrent")
def search(query: str = typer.Argument(None), src: int = typer.Option(
        1, "--source", "-s", help="The Source to search query from."), page: int = typer.Option(
            1, "--page", "-p", help="Number of pages to search for.")) -> None:
    typer.echo(
        f"Searching for '{query}' from {SOURCES[src]} in {page} {'pages' if page > 1 else 'page'} ...")
    handler = get_handler()
    handler.search(query, src, page)
    typer.echo(f"Done!")


@app.command(name="downloads", help="List all the downloads")
def downloads() -> None:
    typer.echo(f"Showing Downloads ...")
    handler = get_handler()
    handler.show_downloads()
    typer.echo(f"Done!")


@app.command(name="current", help="List current downloads")
def current() -> None:
    typer.echo(f"Showing Current Downloads ...")
    handler = get_handler()
    handler.show_current()
    typer.echo(f"Done!")


@app.command(name="last", help="List last search")
def list_last() -> None:
    typer.echo(f"Listing last search results...")
    handler = get_handler()
    handler.list_last()
    typer.echo(f"Done!")


@app.command(name="config", help="Change config for default download path")
def list_downloads(path=typer.Option(None, "--path", help="the new default download path")) -> None:
    if path is not None:
        if os.path.isdir(path):
            create_config_file(path)
            typer.echo(f"Changed default download path to {path}")
        else:
            typer.echo(f"Given Path [{path}] is not a valid directory")
    else:
        config = load_config()
        typer.echo(f"Current config: {config}")