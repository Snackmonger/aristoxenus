"""Functions relating to making ``rich`` objects with various formattings."""

import rich
from rich import panel, table, layout, style, theme, console, columns
from data import annotations, data_models
from src import nomenclature, utils

def chord_scale(data: annotations.APIChordScaleResponse) -> console.Group:

    data_ = data_models.ChordScaleRendering(**data)
    side1 = """[title]Parent scale\nModal rotation\nKeynote\nNumber of notes\nBase step[/title]"""
    polyad = nomenclature.encode_numeric_keyword(data_.notes, "polyad")
    basal = nomenclature.encode_numeric_keyword(data_.step, "basal")
    side2 = f"""[emphasis2]{data_.scale}\n{data_.mode}\n{data_.keynote}\n{polyad}\n{basal}[/emphasis2]"""

    def __chord(chord: annotations.HeptatonicChord) -> panel.Panel:
        chord_ = data_models.HeptatonicChordRendering(**chord)
        chord_name = f"\n[title]Chord symbol[/title] {chord_.chord_symbol}\n"
        notes = f"[title]Note names[/title] {chord_.notes}\n"
        intervals = f"[title]Intervals[/title] {chord_.interval_names}"
        panel_ = panel.Panel(chord_name + notes + intervals, title=f"[emphasis2]{chord_.roman_degree}[/emphasis2]")
        return panel_

    renderables = [__chord(x) for x in data_.chord_scale]

    top = table.Table(show_header=False)
    top.add_row(side1, side2)
    bottom = columns.Columns(renderables)

    return console.Group(top, bottom)
