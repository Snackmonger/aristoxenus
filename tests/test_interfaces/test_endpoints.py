# pylint: disable=missing-function-docstring,line-too-long,missing-module-docstring,invalid-name,redefined-outer-name
from typing import Iterable, Optional
import pytest

from aristoxenus import api
from aristoxenus.core.annotations import ChordStyle
from aristoxenus.core.constants import INTERVAL_NAMES, CHORD_SYMBOL, CONFIGURATION, MAJ_SYMBOL, MIN_SYMBOL, DIM_SYMBOL

params = pytest.mark.parametrize


@params(
    'intervals, config, expected', [
        (('1', '3', '#5', 'b7'), None, {INTERVAL_NAMES: ('1', '3', '#5', 'b7'), CHORD_SYMBOL: '7#5', CONFIGURATION: {MAJ_SYMBOL: 'maj', MIN_SYMBOL: 'min', DIM_SYMBOL: 'dim'}}),
        (('1', '3', '5', '7'), None, {INTERVAL_NAMES: ('1', '3', '5', '7'), CHORD_SYMBOL: 'maj7', CONFIGURATION: {MAJ_SYMBOL: 'maj', MIN_SYMBOL: 'min', DIM_SYMBOL: 'dim'}}),
        (('1', '3', '5', '7'), {MAJ_SYMBOL: 'M'}, {INTERVAL_NAMES: ('1', '3', '5', '7'), CHORD_SYMBOL: 'M7', CONFIGURATION: {MAJ_SYMBOL: 'M', MIN_SYMBOL: 'min', DIM_SYMBOL: 'dim'}}),
        (('1', 'b3', 'b5', 'bb7', '9'), None, {INTERVAL_NAMES: ('1', 'b3', 'b5', 'bb7', '9'), CHORD_SYMBOL: 'dim9', CONFIGURATION: {MAJ_SYMBOL: 'maj', MIN_SYMBOL: 'min', DIM_SYMBOL: 'dim'}}),
        (('1', 'b3', 'b5', 'bb7', '9'), {DIM_SYMBOL: 'o'}, {INTERVAL_NAMES: ('1', 'b3', 'b5', 'bb7', '9'),CHORD_SYMBOL: 'o9', CONFIGURATION: {MAJ_SYMBOL: 'maj', MIN_SYMBOL: 'min', DIM_SYMBOL: 'o'}}),
        (('1', 'b3', 'b5', 'bb7', '11'), None, {INTERVAL_NAMES: ('1', 'b3', 'b5', 'bb7', '11'), CHORD_SYMBOL: 'dim7add11', CONFIGURATION: {MAJ_SYMBOL: 'maj', MIN_SYMBOL: 'min', DIM_SYMBOL: 'dim'}}),
        (('1', 'bb3', 'b5', 'bb7'), None, {INTERVAL_NAMES: ('1', 'bb3', 'b5', 'bb7'), CHORD_SYMBOL: 'susbb3b5bb7', CONFIGURATION: {MAJ_SYMBOL: 'maj', MIN_SYMBOL: 'min', DIM_SYMBOL: 'dim'}}),
        (('1', '4', '5', 'b7'), None, {INTERVAL_NAMES: ('1', '4', '5', 'b7'), CHORD_SYMBOL: '7sus4', CONFIGURATION: {MAJ_SYMBOL: 'maj', MIN_SYMBOL: 'min', DIM_SYMBOL: 'dim'}}),
        (('1', '2', '5', '7', '9'), None, {INTERVAL_NAMES: ('1', '2', '5', '7', '9'), CHORD_SYMBOL: 'maj9sus2', CONFIGURATION: {MAJ_SYMBOL: 'maj', MIN_SYMBOL: 'min', DIM_SYMBOL: 'dim'}}),
        (('1', 'b3', '5', '7', '9'), None, {INTERVAL_NAMES: ('1', 'b3', '5', '7', '9'), CHORD_SYMBOL: 'minmaj9', CONFIGURATION: {MAJ_SYMBOL: 'maj', MIN_SYMBOL: 'min', DIM_SYMBOL: 'dim'}}),
        (('1', 'b3', '5', '7', '9'), {MIN_SYMBOL: 'm', MAJ_SYMBOL: 'Ma'}, {INTERVAL_NAMES: ('1', 'b3', '5', '7', '9'), CHORD_SYMBOL: 'mMa9', CONFIGURATION: {MAJ_SYMBOL: 'Ma', MIN_SYMBOL: 'm', DIM_SYMBOL: 'dim'}})
    ]
)
def test_get_chord_symbol(intervals: Iterable[str | int], config: Optional[ChordStyle], expected: dict[str, str]) -> None:
    assert api.get_chord_symbol(intervals, config) == expected
