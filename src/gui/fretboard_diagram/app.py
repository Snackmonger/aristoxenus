"""Main controller class for the fretboard diagram app."""

import tkinter as tk
from tkinter import ttk

from src import (interface)
from src.models import diagrams
from data import (
    data_models as DM,
    annotations as A,
    keywords as K
)

from .widgets import (
    ScaleSelector,
    PositionSelector,
    RenderingModeSelector,
    InterfaceModeToggle,
    FingerboardGrid,
    StringFingeringSelector,
    IntervalDisplaySelector,
    ArpeggioModeControlPanel
)

from . import functions

class FretboardDiagramApp(ttk.Frame):
    """Main widget for the fretboard diagram."""

    def __init__(self):
        master_ = tk.Tk()
        master_.title("Aristoxenus Fretboard Diagram Tool")
        ttk.Frame.__init__(self, master_)

        # The abstract diagrams model the layout of the grid and its nodes.
        self.scale_diagram = diagrams.GuitarFingeringDiagram(
            5, diagrams.standard_fretboard(), 5)
        self.arpeggio_diagram = diagrams.GuitarFingeringDiagram(
            5, diagrams.standard_fretboard(), 5)
        self.current_diagram = self.scale_diagram

        # Set default scale data for the initial view.
        cmaj = DM.HeptatonicRendering(
            **interface.render_heptatonic_form(K.DIATONIC,
                                               K.IONIAN,
                                               "C"))
        self.current_diagram.define_scale(cmaj.optimal_rendering)
        self.current_diagram.define_intervals(cmaj.interval_map)
        self.current_diagram.turn_on_names(cmaj.optimal_rendering)

        # Define the top control bar (scale, position, rendering, interface)
        self.scale_selector = ScaleSelector(self, self.on_scale_change)
        self.position_selector = PositionSelector(self, self.current_diagram.positions(
            cmaj.optimal_rendering), self.on_position_change)
        self.rendering_mode_selector = RenderingModeSelector(
            self, self.on_rendering_mode_change)
        self.interface_mode_toggle = InterfaceModeToggle(
            self, self.on_interface_mode_change)

        # TODO: top bar also needs a toggle button to decide whether the
        # doubled note in a scale should fall on the g or b string
        # (but this is only a concern in some tunings... can we train the
        # machine to respect the logic of a tuning on its own??)

        # Main window, left: grid drawing of the abstract diagram.
        self.fingerboard_grid = FingerboardGrid(
            self, self.current_diagram)

        # Main window, centre: controls for the fingering of each string.
        self.fingering_panel = StringFingeringSelector(
            self, self.on_fingering_change, self.current_diagram.number_of_strings)

        # Main window, right: controls for the representation of forms
        # within the diagram display; depends on the interface mode to
        # decide which set of controls to show.
        self.current_main_panel: ttk.Frame

        # Frame 4a: Scale Mode Panel (RIGHT, STATE)
        intervals = [v for k, v in self.current_diagram.interval_map.items()
                     if k in self.current_diagram.active_names]
        self.scale_node_selector: IntervalDisplaySelector = IntervalDisplaySelector(
            self, self.on_node_option_change, intervals)

        self.arpeggio_node_selector: ArpeggioModeControlPanel

        # Finish orienting widgets
        self.scale_selector.grid(column=0, row=0, sticky=tk.W)
        self.position_selector.grid(column=1, row=0, sticky=tk.W)
        self.rendering_mode_selector.grid(column=2, row=0, sticky=tk.W)
        self.interface_mode_toggle.grid(column=3, row=0, sticky=tk.W)

        self.fingerboard_grid.grid(column=0, row=1, columnspan=2)
        self.fingering_panel.grid(column=2, row=1, sticky=tk.EW)
        self.scale_node_selector.grid(column=3, row=1, sticky=tk.EW)

        self.grid()

        # Display initial default values
        self.scale_selector.change_state()
        for report in self.fingering_panel.summarize():
            self.current_diagram.apply_fingering(**report)

    def on_fingering_change(self, report: A.FingeringReport) -> None:
        """Receive a report about the change in fingering and modify the 
        diagram to reflect it.
        """
        self.current_diagram.apply_fingering(**report)
        self.fingerboard_grid.draw_diagram(self.current_diagram)

    def on_node_option_change(self, report: A.NodeDisplayReport) -> None:
        """Receive a report about the change to an interval node's
        display options and modify the diagram to reflect it.

        This method is only available when the app is in the "Scale" 
        interface mode.
        """
        self.current_diagram.apply_node_display_options(report)
        self.fingerboard_grid.draw_diagram(self.current_diagram)

    def on_scale_change(self, report: A.ScaleformReport) -> None:
        """Receive a report about the change to the main scale paradigm
        and modify the diagram to reflect it.

        This method is only available when the app is in the "Scale" 
        interface mode.
        """
        # Whenever the scale, mode, or keynote changes, we have to reassign
        # the active nodes to reflect the new notes and intervals.
        current_names: list[str] = list(set(self.current_diagram.active_names))
        positions: list[int] = self.current_diagram.positions(current_names)
        i: int = positions.index(self.current_diagram.position)
        data = DM.HeptatonicRendering(
            **interface.render_heptatonic_form(**report))

        # Set the diagram to the new scale.
        self.current_diagram.define_scale(data.chromatic_rendering)
        self.current_diagram.define_intervals(data.interval_map)
        self.current_diagram.turn_on_names(data.chromatic_rendering)

        # Set the new position to the value at the old position's index,
        # in case the old position's value is no longer valid.
        positions = self.current_diagram.positions(data.chromatic_rendering)
        self.on_position_change(positions[i])
        self.position_selector.set_position(
            self.current_diagram.position, positions)

        # Configure nodes to display correct scale nomenclature
        self.current_diagram.clear_overrides()
        self.current_diagram.override_names({k: v for k, v in
                                             dict(zip(data.chromatic_rendering,
                                                      data.optimal_rendering)).items()
                                             if not k == v})

        # The node selector will restore the same settings for each of the 7
        # intervals, but the intervals' names will be updated for the new
        # scale configuration.
        self.scale_node_selector.rename_intervals(
            [v for k, v in data.interval_map.items()
             if k in data.chromatic_rendering])
        for report_ in self.scale_node_selector.summarize():
            self.current_diagram.apply_node_display_options(report_)
        self.scale_node_selector.set_subwidget("1")

        self.fingerboard_grid.draw_diagram(self.current_diagram)

    def on_rendering_mode_change(self, report: str) -> None:
        """Receive a report about the change to the display mode
        and modify the diagram to reflect it.
        """
        self.current_diagram.apply_rendering_mode(report)
        self.fingerboard_grid.draw_diagram(self.current_diagram)

    def on_position_change(self, report: int) -> None:
        """Receive a report about the change to the position
        and modify the diagram to reflect it.

        This method is only available when the app is in the "Scale" 
        interface mode.
        """
        self.current_diagram.change_position(report,
                                             self.fingering_panel.summarize(),
                                             self.scale_node_selector.summarize(),
                                             self.rendering_mode_selector.report())
        self.fingerboard_grid.draw_diagram(self.current_diagram)

    def on_interface_mode_change(self) -> None:
        """Change the state of the main panel, and perform any necessary 
        changes to the UI to accommodate the change."""
        if self.interface_mode_toggle.current_interface_mode == K.ARPEGGIO:
            functions.enable_widget(self.scale_selector, False)
            functions.enable_widget(self.scale_node_selector, False)
            functions.enable_widget(self.position_selector, False)

            # rewrite the main app so that we keep two references to diagrams for the
            # two different modes, then switch between them depending on the user's
            # interface selection.

            # Basically, we ALLOW the fingering selector and rendering type selector to
            # make changes to the main diagram, being ignorant of what interface mode
            # is active, but we DISALLOW the scale selector, position selector, or
            # scale node controls to make any changes to the arpeggio diagram.

            # THEREFORE: Whenever we switch modes, we clone the last settings for
            # FINGERING and RENDERING to the the current diagram.

            # current_scale = interface.render_heptatonic_form(**self.scale_selector.report())
            # self.current_diagram = self.arpeggio_diagram

        elif self.interface_mode_toggle.current_interface_mode == K.SCALE:
            functions.enable_widget(self.scale_selector)
            functions.enable_widget(self.scale_node_selector)
            functions.enable_widget(self.position_selector)

            # self.diagram = self.scale_diagram

    def on_arpeggio_change(self, report: A.ArpeggioFormReport) -> None:
        """This method is only available when the app is in the "Arpeggio" 
        interface mode."""
