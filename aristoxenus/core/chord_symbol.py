import re
from typing import Iterable, Optional

from aristoxenus.core.annotations import ChordStyle
from aristoxenus.core.constants import (
    CHORD_11,
    CHORD_13,
    CHORD_2,
    CHORD_3,
    CHORD_4,
    CHORD_5,
    CHORD_6,
    CHORD_7,
    CHORD_9,
    CHORD_ADD,
    CHORD_AUGMENTED_SYMBOLS,
    CHORD_DIM,
    CHORD_DIM_SYMBOLS,
    CHORD_DOUBLE_FLAT_3,
    CHORD_DOUBLE_FLAT_7,
    CHORD_FLAT_3,
    CHORD_FLAT_5,
    CHORD_FLAT_7,
    CHORD_HALFDIM_SYMBOLS,
    CHORD_LEGAL_ALT5,
    CHORD_LEGAL_SUS,
    CHORD_LEGAL_THIRD,
    CHORD_MAJ,
    CHORD_MAJOR_SYMBOLS,
    CHORD_MIN,
    CHORD_MINOR_SYMBOLS,
    CHORD_NO,
    CHORD_SHARP_3,
    CHORD_SHARP_5,
    CHORD_SUS,
    CHORD_SYMBOL,
    DIM_SYMBOL,
    EMPTY_STRING,
    EXTENSION,
    FLAT_SYMBOL,
    MAIN,
    MAJ_SYMBOL,
    MIN_SYMBOL,
    MODIFICATION,
    NOTE_NAME,
    RE_PARSE_CHORD_SYMBOL,
    RELATIVE,
    SHARP_SYMBOL,
    SLASH,
    SLASH_SYMBOL
)
from aristoxenus.core.errors import StringValidationError
from aristoxenus.core.interval import (
    calculate_interval, 
    sort_interval_names
)
from aristoxenus.core.validation import validate_alphabetic_name


def encode_chord_symbol(interval_names: Iterable[str], style: Optional[ChordStyle] = None) -> str:
    '''
    Parse a list of interval names into a chord symbol.

    Major, minor, and diminished chords can have customizable symbols, so
    you could have e.g. 'maj', or 'M', or 'Δ', etc. according to preference.

    Half-diminished, augmented, and other types of altered chords are
    simply spelled with an explicit alteration, e.g. min7b5, 7#5, maj7#5,
    so they cannot be customized.

    Sus chords are always 'sus', so they cannot be customized.

    NOTE: Interval names are treated as a set, so this function will never 
    return a chord in 'slash' notation.

    Parameters
    ----------
    interval_names: Iterable[str]
        The interval names (e.g. '1', 'b3', etc.) you want to parse as a chord.
    maj_symbol : str, optional
        What symbol will represent major chords, by default "maj"
    min_symbol : str, optional
        What symbol will represent minor chords, by default "min"
    dim_symbol : str, optional
        What symbol will represent diminished chords, by default "dim"
    '''
    style = style or {}
    maj_symbol = style.get(MAJ_SYMBOL, CHORD_MAJ)
    min_symbol = style.get(MIN_SYMBOL, CHORD_MIN)
    dim_symbol = style.get(DIM_SYMBOL, CHORD_DIM)
    dim7_structure = [CHORD_FLAT_3, CHORD_FLAT_5, CHORD_DOUBLE_FLAT_7]
    dom7_structure = [CHORD_3, CHORD_FLAT_7]
    natural_extensions = [CHORD_9, CHORD_11, CHORD_13]

    parse = set(interval_names)

    # A chord symbol is made up of a series of suffixes, each of which
    # implies something about the chord's structure. Not all suffixes
    # will be present (and in fact cannot all be present simultaneously).
    # They have been ordered with a view to making the resulting symbols
    # easier to read, including a few unusual chord structures implied
    # in some of the more exotic parent scales we offer.
    normal3: str = EMPTY_STRING
    primary: str = EMPTY_STRING
    secondary: str = EMPTY_STRING
    sus: str = EMPTY_STRING
    alt5: str = EMPTY_STRING
    alt7: str = EMPTY_STRING
    add: str = EMPTY_STRING
    no5: str = EMPTY_STRING
    no3: str = EMPTY_STRING
    extensions: str = EMPTY_STRING

    # Any note that has already been handled is removed so it
    # will not be misunderstood later.
    parse.discard(str(1))

    # Convenience functions to help categorize the base structure.
    def has_third() -> Optional[str]:
        for x in CHORD_LEGAL_THIRD:
            if x in interval_names:
                return x
        return None

    def has_p5() -> Optional[str]:
        if CHORD_5 in interval_names:
            return CHORD_5
        return None

    def has_alt5() -> Optional[str]:
        for x in CHORD_LEGAL_ALT5:
            if x in interval_names:
                return x
        return None

    def is_dim() -> bool:
        return set(dim7_structure).issubset(interval_names)

    def is_dom() -> bool:
        return set(dom7_structure).issubset(interval_names)

    def has_sus() -> Optional[tuple[str, ...]]:
        candidates: list[str] = []
        for x in CHORD_LEGAL_SUS:
            if x in interval_names:
                candidates.append(x)
        if candidates:
            return tuple(candidates)
        return None

    # Pre-handle special cases.
    # Diminished chord implies specific structure.
    if is_dim():
        normal3 = dim_symbol
        primary = CHORD_7
        parse.difference_update(set(dim7_structure))
    else:
        # Exotic chords are allowed to have bb7 in our system, but since the
        # bb accidental might conflict with the note name in a 7th chord
        # (e.g. 'Bbb7'), we compel it to take the alt7 slot instead of the
        # primary 7 slot (e.g. Bbmajbb7, Ebbminbb7).
        if CHORD_DOUBLE_FLAT_7 in parse:
            alt7 = CHORD_DOUBLE_FLAT_7
            parse.discard(CHORD_DOUBLE_FLAT_7)
        # A chord with an altered 5th must always have an explicit alt5 symbol,
        # unless it's diminished.
        if (n := has_alt5()):
            alt5 = n
            parse.discard(n)
        # A chord with no 5th must have an explicit no5 symbol.
        elif not has_p5():
            no5 = CHORD_NO + CHORD_5
        else:
            # The fifth is implied in any other chord and has no symbol.
            parse.discard(CHORD_5)
    # Dominant chord implies specific structure.
    if is_dom():
        primary = CHORD_7
        parse.difference_update(set(dom7_structure))

    # Main chord parsing is mostly a 1:1 symbol matching, with a few
    # exceptions.

    # Chords in our system are always given an explicit symbol for
    # their third, unless they are one of the implicit symbols
    # above, or they have a suspension in place of a third.
    if (n := has_third()):
        if is_dim() or is_dom():
            pass
        elif n == CHORD_3:
            normal3 = maj_symbol
            # A 7 symbol in a major chord implies a natural 7
            if CHORD_7 in parse:
                primary = CHORD_7
                parse.discard(CHORD_7)
        elif n == CHORD_FLAT_3:
            normal3 = min_symbol
            # A 7 symbol in most chords implies a flat 7, so
            # the natural 7 requires a special symbol.
            if CHORD_7 in parse:
                parse.discard(CHORD_7)
                primary = maj_symbol + CHORD_7
            if CHORD_FLAT_7 in parse:
                parse.discard(CHORD_FLAT_7)
                primary = CHORD_7
        parse.discard(n)
    # Our system allows for sus chords with notes that could technically be
    # considered thirds. We categorize #3 and bb3 as 'sus' chords a) because
    # they cannot reasonably be labeled major or minor, b) so that their
    # accidental cannot stand next to the root note (i.e. e.g. Dsusbb3 is less
    # ambiguous than Dbb3).
    elif (candidates := has_sus()):
        # Normally, we expect to have only one medial note (a third or a
        # suspended note). If there's more than one note that could stand
        # as a suspension, treat the first as a suspension, and any others
        # as additions (e.g. 1, 2, 4, 5 -> sus2add4).
        candidates = list(candidates)
        main = candidates.pop(0)
        sus = CHORD_SUS + main
        parse.discard(main)
        for x in candidates:
            if x:
                add += CHORD_ADD + x
                parse.discard(x)
        if CHORD_7 in parse:
            parse.discard(CHORD_7)
            primary = maj_symbol + CHORD_7
        elif CHORD_FLAT_7 in parse:
            parse.discard(CHORD_FLAT_7)
            primary = CHORD_7
    # Any chord without a medial must have an explicit no3 symbol
    else:
        no3 = CHORD_NO + CHORD_3

    # Our system treats primary extension symbols as implying ALL previous
    # extensions in the series, i.e. a 13 chord includes 7, 9, 11, 13.
    # If this series is interrupted by a missing or altered note, then the
    # primary extension is the last continuous extension, and any following
    # natural extensions are treated as additions (e.g. C9#11add13).
    largest: str = EMPTY_STRING
    if primary:
        checked: list[str] = []
        for i, extension in enumerate(natural_extensions):
            prev = natural_extensions[i - 1] if i > 0 else None
            if extension in parse:
                if not prev or prev in checked:
                    largest = extension
                    parse.discard(extension)
                    checked.append(extension)
                else:
                    add += CHORD_ADD + extension
                    parse.discard(extension)
                    checked.append(extension)
        if largest:
            primary = primary.replace(CHORD_7, largest)

    # The secondary suffix does not implicitly absorb any other intervals,
    # so that 1, 3, 5, 6, 9, 11, 13 -> maj6add9add11add13
    if CHORD_6 in parse:
        secondary = CHORD_6
        parse.discard(CHORD_6)

    # If the primary suffix already exists, treat the 6 as an addition.
    if secondary and primary:
        add += CHORD_ADD + secondary
        secondary = EMPTY_STRING

    # Any extension with an accidental can simply be suffixed on its own.
    # Natural extensions may encounter ambiguities and must be treated as
    # additions (e.g. Emaj7#11 vs Emaj711, better: Emaj7add11)
    for extension in list(parse):
        if not any([SHARP_SYMBOL in extension, FLAT_SYMBOL in extension]):
            add += CHORD_ADD + extension
            parse.discard(extension)

    # By this point, the list of intervals only contains non-chord tone
    # extensions with accidentals.
    extensions = EMPTY_STRING.join(parse)

    # Most suffixes will be empty strings in any given chord.
    symbols: list[str] = [
        normal3,
        primary,
        secondary,
        sus,
        no3,
        no5,
        alt5,
        alt7,
        extensions,
        add
    ]
    return EMPTY_STRING.join(symbols)


def decode_chord_symbol(chord_symbol: str) -> tuple[str, ...]:
    '''
    Parse a chord symbol into a list of interval names.

    NOTE: Chords may use Roman or alphabetic names for their root. If the
    Root is alphabetic, it may take another alphabetic name as a slash
    modifier; if the root is Roman, it may not take a slash notation.

    Parameters
    ----------
    chord_symbol : str
        The chord symbol you want to parse. Most common symbols should be
        recognized.

    Returns
    -------
    tuple[str, ...]
        A tuple of interval names implied in the chord symbol.

    Raises
    ------
    StringValidationError
        If the chord symbol contains an illegal character/configuration.
    '''
    intervals: set[str] = {str(1), CHORD_5}
    # Regex sorts elements into five categories.
    #
    # 1) The root symbol defines the note name or Roman interval relative to
    # which the chord's structure is understood.
    # 2) The main symbol generally defines the third and may imply something
    # about the 7.
    # 3) The extension symbol defines the 7th or any natural note that is
    # allowed to replace it.
    # 4) The modification symbol(s) include any other interval symbol,
    # or an add, no, or sus.
    # 5) The slash symbol is an annotation about ths inversion of the chord,
    # relative to the chord's root.
    #
    # After this, we have most information about a chord, and just need to
    # check edge cases and transform symbols into interval names.
    match = re.search(RE_PARSE_CHORD_SYMBOL, chord_symbol)
    if match is None:
        raise StringValidationError(chord_symbol, CHORD_SYMBOL)

    root = match.group(NOTE_NAME)
    main = match.group(MAIN)
    extension = match.group(EXTENSION)
    modifications = match.group(MODIFICATION)
    slash = match.group(SLASH)
    ext_series: list[str] = [CHORD_7, CHORD_9, CHORD_11, CHORD_13]
    sus_intervals: list[str] = [
        CHORD_DOUBLE_FLAT_3, CHORD_SHARP_3, CHORD_4, CHORD_2]

    # Slash chords must use alphabetic names.
    if slash is not None:
        if not validate_alphabetic_name(root) or not validate_alphabetic_name(slash):
            raise StringValidationError(chord_symbol, CHORD_SYMBOL)

    # Bare chords imply major, e.g. 'C', 'A', 'F#'
    if main is None:
        intervals.add(CHORD_3)
        # 'C7', 'A11', 'F#13'
        if extension in ext_series:
            i = ext_series.index(extension) + 1
            for interval in ext_series[:i]:
                if interval == CHORD_7:
                    interval = CHORD_FLAT_7
                intervals.add(interval)
            extension = None

    # Major chords, e.g. 'Cmaj', 'AM', 'F#Δ'
    elif main in CHORD_MAJOR_SYMBOLS:
        intervals.add(CHORD_3)
        # Major 7 implies natural 7, e.g. 'Cmaj7', 'AM7', 'F#Δ7'
        if extension in ext_series:
            i = ext_series.index(extension) + 1
            for interval in ext_series[:i]:
                intervals.add(interval)
            extension = None

    # Diminished chords, e.g. 'Cdim', 'Ao'
    elif main in CHORD_DIM_SYMBOLS:
        intervals.add(CHORD_FLAT_3)
        intervals.add(CHORD_FLAT_5)
        intervals.discard(CHORD_5)
        # Diminished 7 implies bb7, e.g. 'Cdim7', 'Ao9'
        if extension in ext_series:
            i = ext_series.index(extension) + 1
            for interval in ext_series[:i]:
                if interval == CHORD_7:
                    interval = CHORD_DOUBLE_FLAT_7
                intervals.add(interval)
            extension = None

    # Augmented chords, e.g. 'Caug', 'A+'
    elif main in CHORD_AUGMENTED_SYMBOLS:
        intervals.add(CHORD_3)
        intervals.add(CHORD_SHARP_5)
        intervals.discard(CHORD_5)

    # Half-diminished chords, e.g. 'Cø'
    elif main in CHORD_HALFDIM_SYMBOLS:
        intervals.add(CHORD_FLAT_3)
        intervals.add(CHORD_FLAT_5)
        intervals.discard(CHORD_5)

    # Minor chords, e.g. 'Cmin', 'Am', 'F#-'
    elif main in CHORD_MINOR_SYMBOLS:
        intervals.add(CHORD_FLAT_3)

    # Apart from major and diminished chords, above, a 7 implies a flat 7,
    # and a natural 7 must be indicated as a major 7.
    if extension:
        for symb in CHORD_MAJOR_SYMBOLS:
            if symb in extension:
                base = extension.replace(symb, EMPTY_STRING)
                if base in ext_series:
                    i = ext_series.index(base) + 1
                    for interval in ext_series[:i]:
                        intervals.add(interval)
        if extension in ext_series:
            i = ext_series.index(extension) + 1
            for interval in ext_series[:i]:
                if interval == CHORD_7:
                    interval = CHORD_FLAT_7
                intervals.add(interval)

    # Check modifications
    sub: list[str] = []
    if modifications:
        # Special chords in our system might have sus bb3, #3.
        for sus in sus_intervals:
            if (n := CHORD_SUS + sus) in modifications:
                modifications.replace(n, EMPTY_STRING)
                intervals.add(sus)
                sub.extend([CHORD_3, CHORD_FLAT_3])

        # Special chords in our system might have bb7.
        if CHORD_DOUBLE_FLAT_7 in modifications:
            if (n := CHORD_NO + CHORD_DOUBLE_FLAT_7) in modifications:
                sub.append(CHORD_DOUBLE_FLAT_7)
                modifications.replace(n, '')
            else:
                if (n := CHORD_ADD + CHORD_DOUBLE_FLAT_7) in modifications:
                    intervals.add(CHORD_DOUBLE_FLAT_7)
                    modifications.replace(n, EMPTY_STRING)
                else:
                    intervals.add(CHORD_DOUBLE_FLAT_7)
                    modifications.replace(CHORD_DOUBLE_FLAT_7, EMPTY_STRING)

        # Most remaining symbols will be a bare interval name, an addition, or
        # a subtraction.
        INTERVALS = (13, 11, 9, 6, 5, 4, 3, 2)
        for number in INTERVALS:
            for accidental in [SHARP_SYMBOL, FLAT_SYMBOL, EMPTY_STRING]:
                interval = accidental + str(number)
                if (n := CHORD_ADD + interval) in modifications:
                    intervals.add(interval)
                    modifications = modifications.replace(n, EMPTY_STRING)
                if (n := CHORD_NO + interval) in modifications:
                    sub.append(interval)
                    modifications = modifications.replace(n, EMPTY_STRING)
                if interval in modifications:
                    intervals.add(interval)
                    modifications = modifications.replace(
                        interval, EMPTY_STRING)
                    if interval in [CHORD_SHARP_5, CHORD_FLAT_5]:
                        intervals.remove(CHORD_5)

        # Augmented symbols are either main or modification, e.g. Caug7 vs. C7aug
        for aug in CHORD_AUGMENTED_SYMBOLS:
            if aug in modifications:
                intervals.discard(CHORD_5)
                intervals.add(CHORD_SHARP_5)

    # Subtractions are treated last in case they depend on an implication
    # in a preceding symbol.
    for s in sub:
        if s in intervals:
            intervals.remove(s)

    # If we have a slash chord, we need to make sure that the slashed interval
    # is actually present before we try to rotate to make it the bass. If not,
    # assume that the main chord is in root position superimposed over the
    # given bass, and perform no rotation. This entails that 'Cmaj7/E' gives
    # ('3', '5', '7', '1'), but Dmin7/E gives ('2', '1', 'b3', '5', 'b7').
    _intervals = list(sort_interval_names(intervals))
    if slash:
        bass_interval = calculate_interval(root, slash)[RELATIVE]
        if bass_interval not in _intervals:
            _intervals.insert(0, bass_interval)
        i = _intervals.index(bass_interval)
        return tuple(_intervals[i:] + _intervals[:i])

    return sort_interval_names(intervals)


def get_chord_style(chord_symbol: str) -> ChordStyle:
    '''
    Attempt to extract chord style information from a given chord symbol.

    Parameters
    ----------
    chord_symbol : str
        A symbol representing a chord structure, e.g. 'Emin7/G'

    Returns
    -------
    ChordStyle
        A dictionary of details about the sub-symbols and formatting used in 
        the chord symbol.

    Raises
    ------
    StringValidationError
        If the chord symbol cannot be parsed.
    '''
    # TODO: write tests
    match = re.search(RE_PARSE_CHORD_SYMBOL, chord_symbol)
    if match is None:
        raise StringValidationError(chord_symbol, CHORD_SYMBOL)
    style: ChordStyle = {}
    if SLASH_SYMBOL in chord_symbol:
        style[SLASH] = True
    for maj in CHORD_MAJOR_SYMBOLS:
        if match.group(MAIN) == maj or maj in match.group(EXTENSION):
            style[MAJ_SYMBOL] = maj
    for minor in CHORD_MINOR_SYMBOLS:
        if match.group(MAIN) == minor:
            style[MIN_SYMBOL] = minor
    for dim in CHORD_DIM_SYMBOLS:
        if match.group(MAIN) == dim:
            style[DIM_SYMBOL] = dim
    return style
