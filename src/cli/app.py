# pyright: reportUntypedFunctionDecorator=false, reportFunctionMemberAccess=false
# pylint: disable=invalid-name
"""
Command-line interface application that exposes a 
few of the features of the library.
"""
import rich_click as click
from rich import console

from data import (keywords as keywords,
                  annotations as annotations,
                  constants as constants)
from src import (interface as I,
                 )
from tests import (do_doctests,
                   test_chord_symbol_from_interval_names)

from . import app_data, views

# Configure rich console printing
click.rich_click.USE_RICH_MARKUP = True
console_ = console.Console(theme=app_data.MAIN_THEME)


@click.group()
def aristoxenus() -> None:
    """
    [yellow u]Aristoxenus Command-Line Interface[/yellow u]

    This is a hobby project, so this CLI is mostly just used for debugging
    and testing. If you stumbled on this repository on GitHub, then welcome 
    and enjoy a few of the basic functions of Aristoxenus!
    """

@aristoxenus.command()
@click.option("--scale", "-s", help="The name of the parent scale.",
              type=click.Choice(keywords.HEPTATONIC_SERIES, case_sensitive=False),
              prompt=True)
@click.option("--mode", "-m", help="The name of the modal rotation.",
              type=click.Choice(keywords.MODAL_SERIES, case_sensitive=False),
              prompt=True)
@click.option("--keynote", "-k", prompt=True,
              type=click.Choice(constants.LEGAL_ROOT_NAMES, case_sensitive=False),
              help="The name of the note to use as the tonal centre.")
def heptatonic_form(scale: annotations.HeptatonicScales,
                    mode: annotations.ModalNames,
                    keynote: str
                    ) -> None:
    """Get details about a heptatonic scale form."""
    data = I.render_heptatonic_form(keynote, scale, mode)
    console_.print(data)


@aristoxenus.command()
@click.option("--keynote", "-k", type=str, prompt=True,
              help="The keynote of the chromatic scale. Must be a legal root name.")
@click.option("--binomial", "-b",
              required=False, prompt=False,
              type=bool, show_default=True,
              help="Render the scale with binomial names.")
def chromatic(keynote: str, binomial: bool) -> None:
    """Print a chromatic scale starting on a given keynote."""
    data = I.chromatic(keynote, binomial)
    console_.print(data)


@aristoxenus.command()
@click.option("--symbol", "-s",
              prompt=True,
              help="The chord symbol you want to decipher")
def parse_chord(symbol: str) -> None:
    """Attempt to parse a chord symbol."""
    data = I.parse_chord_symbol(symbol)
    console_.print(data)


@aristoxenus.command()
@click.option("--scale", "-s", help="The name of the parent scale.",
              type=click.Choice(keywords.HEPTATONIC_SERIES, case_sensitive=False),
              prompt=True)
@click.option("--mode", "-m", help="The name of the modal rotation.",
              type=click.Choice(keywords.MODAL_SERIES, case_sensitive=False),
              prompt=True)
@click.option("--keynote", "-k", prompt=True,
              help="The name of the note to use as the tonal centre.",
              type=click.Choice(constants.LEGAL_ROOT_NAMES, case_sensitive=False))
@click.option("--notes", "-n",
              help="The number of notes to include in the structure.",
              required=False, type=int, default=3, show_default=True)
@click.option("--steps", "-st",
              help="How many steps between notes (start at 0, so tertial=2)",
              required=False, type=int, default=2, show_default=True)
def chord_scale(scale: annotations.HeptatonicScales, mode: annotations.ModalNames, keynote: str,
                notes: int, steps: int) -> None:
    """Get details about a heptatonic scale form."""
    data = I.heptatonic_chord_scale(scale, mode, keynote, notes, steps)
    console_.print(views.chord_scale(data))


@aristoxenus.command()
@click.option("--topic", "-t", help="The topic you want information about.",
              prompt=True,
              type=click.Choice(list(app_data.TOPIC_DATA), case_sensitive=False))
def info(topic: str) -> None:
    """Get information about various topics."""
    console_.print(app_data.TOPIC_DATA[topic.lower()])


@aristoxenus.command()
@click.option("--verbose", "-v",
              help="Get a full report of the tests.",
              is_flag=True,
              default=False,
              show_default=True)
def do_tests(verbose: bool) -> None:
    """DEBUG option: Run the tests for the program."""
    do_doctests(verbose)
    test_chord_symbol_from_interval_names(verbose=verbose)
