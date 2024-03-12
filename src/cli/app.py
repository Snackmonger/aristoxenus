# pyright: reportUntypedFunctionDecorator=false, reportFunctionMemberAccess=false
# pylint: disable=invalid-name
"""
Command-line interface application that exposes a 
few of the features of the library.
"""

from typing import Optional
import rich_click as click
import rich
from rich import theme, console

from src import interface as I
from data import (keywords as K,
                  annotations as A,
                  constants as C)
from src.gui.fretboard_diagram.app import FretboardDiagramApp
from . import app_data, views

# Toggle rich markup in docs and help strings.
click.rich_click.USE_RICH_MARKUP = True


aristoxenus_theme = theme.Theme({
    "title": "orange1 u",
    "emphasis1": "cyan",
    "emphasis2": "light_green",
    "warning": "black on yellow"
})
console_ = console.Console(theme=aristoxenus_theme)

class CLI_State:
    """
    Persistent values used by the CLI.
    """
    start: str = "fuck"
    scale: A.APIScaleFormResponse


_state = CLI_State()


@click.group()
@click.pass_context
def aristoxenus(context: click.Context) -> None:
    """
    [yellow u]Aristoxenus Command-Line Interface[/yellow u]

    This is a hobby project, so this CLI is mostly just used for debugging
    and testing. If you stumbled on this repository on GitHub, then welcome 
    and enjoy a few of the basic functions of Aristoxenus.
    """
    context.obj = _state


@aristoxenus.command()
def fretboard_diagram() -> None:
    """
    Attempt to launch the tkinter [red]Fretboard Diagram Tool[/red].
    """
    FretboardDiagramApp().mainloop()


@aristoxenus.command()
@click.option("--scale", "-s", help="The name of the parent scale.",
              type=click.Choice(K.HEPTATONIC_ORDER, case_sensitive=False),
              prompt=True)
@click.option("--mode", "-m", help="The name of the modal rotation.",
              type=click.Choice(K.MODAL_NAME_SERIES, case_sensitive=False),
              prompt=True)
@click.option("--keynote", "-k", prompt=True,
              type=click.Choice(C.LEGAL_ROOT_NAMES, case_sensitive=False),
              help="The name of the note to use as the tonal centre.")
def heptatonic_form(scale: A.HeptatonicScales, 
                    mode: A.ModalNames, 
                    keynote: str
                    ) -> None:
    """Get details about a heptatonic scale form."""
    data = I.render_heptatonic_form(scale, mode, keynote)
    console_.print(data)


@aristoxenus.command()
@click.option("--keynote", "-k", type=str, prompt=True,
              help="The keynote of the chromatic scale. Must be a legal root name.")
@click.option("--accidental_type", "-a", required=False, prompt=False,
              type=click.Choice(["sharps", "flats", "binomials"], case_sensitive=False),
              help="The type of accidental used in the chromatic scale.")
def chromatic(keynote: str, accidental_type: Optional[str] = None) -> None:
    """Print a chromatic scale starting on a given keynote."""
    data = I.chromatic(keynote, accidental_type)
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
              type=click.Choice(K.HEPTATONIC_ORDER, case_sensitive=False),
              prompt=True)
@click.option("--mode", "-m", help="The name of the modal rotation.",
              type=click.Choice(K.MODAL_NAME_SERIES, case_sensitive=False),
              prompt=True)
@click.option("--keynote", "-k", prompt=True,
              help="The name of the note to use as the tonal centre.",
              type=click.Choice(C.LEGAL_ROOT_NAMES, case_sensitive=False))
@click.option("--notes", "-n",
              help="The number of notes to include in the structure.",
              required=False, type=int, default=3, show_default=True)
@click.option("--steps", "-st",
              help="How many steps between notes (start at 0, so tertial=2)",
              required=False, type=int, default=2, show_default=True)
def chord_scale(scale: A.HeptatonicScales, mode: A.ModalNames, keynote: str,
                notes: int, steps: int) -> None:
    """Get details about a heptatonic scale form."""
    data = I.heptatonic_chord_scale(scale, mode, keynote, notes, steps)
    console_.print(views.chord_scale(data))





@aristoxenus.command()
@click.option("--topic", "-t", help="The topic you want information about.",
              prompt=True,
              type=click.Choice(list(app_data.TOPIC_DATA), case_sensitive=False))
def info(topic: str) -> None:
    console_.print(app_data.TOPIC_DATA[topic.lower()])