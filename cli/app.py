# pyright: reportUntypedFunctionDecorator=false, reportFunctionMemberAccess=false
# pylint: disable=invalid-name
"""
Command-line interface application that exposes a 
few of the features of the library.
"""

import rich_click as click
import rich

from src import interface as I
from data import (keywords as K,
                  annotations as T,
                  constants as C)
from gui.fretboard_diagram.app import FretboardDiagramApp

# Toggle rich markup in docs and help strings.
click.rich_click.USE_RICH_MARKUP = True


class CLI_State:
    """
    Persistent values used by the CLI.
    """
    start: str = "fuck"
    scale: T.APIScaleFormResponse


_state = CLI_State()


@click.group()
@click.pass_context
def aristoxenus(context: click.Context) -> None:
    """
    [yellow u]Aristoxenus Library Command-Line Interface[/yellow u]

    The Aristoxenus library is a suite of musical functions and tools, and
    some of these can be accessed without much difficulty from the
    command-line. 
    """
    context.obj = _state


@aristoxenus.command()
def fretboard_diagram() -> None:
    """
    Attempt to launch the tkinter [red]Fretboard Diagram Tool[/red].
    """
    FretboardDiagramApp().mainloop()


@aristoxenus.command()
@click.option("--scale", "-s",
              type=click.Choice(K.HEPTATONIC_ORDER, case_sensitive=False),
              prompt=True,
              help="The name of the parent scale.")
@click.option("--mode", "-m",
              type=click.Choice(K.MODAL_NAME_SERIES, case_sensitive=False),
              prompt=True,
              help="The name of the modal rotation.")
@click.option("--keynote", "-k",
              type=click.Choice(C.LEGAL_ROOT_NAMES, case_sensitive=False),
              prompt=True,
              help="The name of the note to use as the tonal centre.")
def heptatonic_form(scale: T.HeptatonicScales,
                    mode: T.ModalNames,
                    keynote: str
                    ) -> None:
    """Get details about a heptatonic scale form."""
    data_ = I.render_heptatonic_form(scale, mode, keynote)

    rich.print(data_)