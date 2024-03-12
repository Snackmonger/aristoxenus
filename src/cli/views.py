"""Functions relating to making ``rich`` objects with various formattings."""

import rich
from rich import panel, table, layout, style, theme, console, columns
from data import annotations, data_models
from src import nomenclature, utils

def chord_scale(data: annotations.APIChordScaleResponse) -> console.Group:

    data_ = data_models.ChordScaleRendering(**data)
    scale = f"[title]Parent scale[/title] [emphasis2]{data_.scale}[emphasis2]\n"
    mode = f"[title]Modal rotation[/title] [emphasis2]{data_.mode}[/emphasis2]\n"
    keynote = f"[title]Keynote[/title] [emphasis2]{data_.keynote}[/emphasis2]\n"
    notes = "[title]Number of notes[/title] [emphasis2]" + nomenclature.encode_numeric_keyword(data_.notes, "polyad") + "[/emphasis2]\n"
    step = "[title]Base step[/title] [emphasis2]" + nomenclature.encode_numeric_keyword(data_.step, "basal") + "[/emphasis2]"

    top = panel.Panel(scale + mode + keynote + notes + step)

    def __chord(chord: annotations.HeptatonicChord) -> panel.Panel:
        chord_ = data_models.HeptatonicChordRendering(**chord)
        chord_name = f"\n[title]Chord symbol[/title] {chord_.chord_symbol}\n"
        notes = f"[title]Note names[/title] {chord_.notes}\n"
        intervals = f"[title]Intervals[/title] {chord_.interval_names}"
        panel_ = panel.Panel(chord_name + notes + intervals, title=chord_.roman_degree)
        return panel_

    renderables = [__chord(x) for x in data_.chord_scale]

    bottom = columns.Columns(renderables)

    return console.Group(top, bottom)
