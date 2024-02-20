=================================================
ARISTOXENUS INTERNAL STANDARD SYMBOL PRESCRIPTION
=================================================

This is a guide to the form of interval structure symbolism and nomenclature that the program uses
for its internal reference, and which is the default representational style used for display to the user. 
The included parsers are generally capable of encoding/decoding the most common symbols and names, so the user
is NOT bound by the program's prescription when entering symbols.


.. contents:: Table of Contents


CHORDS
------

Goals
+++++

Aristoxenus adopts a set of chord names that aim to:

1. Be easily understandable in the context of existing chord name conventions
2. Employ consistency in the structural arrangement and meaning of symbols
3. Represent a 1:1 correspondence between symbol and interval, so they can easily be generated and parsed.

Not all of these goals can be equally satisfied in each case, and the prescription compromises strict structural perfection for the sake of human readability.

Add/No Notation
+++++++++++++++
Whevenver the composition of a chord needs to be spelled out exactly, the "add" and "no" suffixes can be added to any chord symbol to make
explicit corrections to a chord's voicing.

The 'add' type prefixes indicate that the specified interval is to be added to the structure of the preceding symbol, without implying
any other interval or structure.

    - Cmaj7add13 -> C, E, G, B, A

The 'no' type prefixes indicate that the specified interval is removed from the structure of the preceding symbol, without implying the removal of
any other interval or structure.

    - Cmaj13no11 -> C, E, G, B, D, A

Triads
++++++

- Major 3 is indicated with 'maj' suffix.
- Minor 3 is indicated with lowercase 'min' suffix.

- A chord that replaces the 3 with a 2 or 4 is indicated with the 'sus' suffix, plus the appropriate numeral

    - "Cmaj", "Emin", "Gsus2", "Dmaj", "Fmin", "Asus4", etc.

In user-generated chord symbols, the parser will also recognize the following symbols:

- Major triads: "M", "Δ", (nothing)
- Minor triads: "m", "-""

    - major triads: "CM", "DM", "EbΔ", "BΔ", "F", "G#", 
    - minor triads: "Em", "Dm", "F-", "G-"

The symbol interpretation always assumes that a chord contains a p5 unless one of the symbols indicates otherwise.
Therefore, we refer to augmented chords as 'maj#5' and diminished chords as 'mb5'. If either of these symbols appears in
the compound symbol and is not qualified by "add" or "no" (see below), then it will be understood as replacing the implicit p5 in the chord.

- "Cmaj#5" -> C E G#
- "Aminb5" -> A C Eb
- "Ebmajb5" -> Eb G Bb

In user-generated symbols, the parser will also recognize the following symbols:

- Augmented triads: "aug", "+""
- Diminished triads: "dim", "ø"

    - augmented triads: "Caug", "Daug", "F+", "G#+"
    - diminished triads: "Fdim", "Gbdim", "Bbø", "Aø"

Other triads with altered fifths are also possible:

    - "Cmajb5" (an uncommon triad, but useful as a base for a dominant 7 chord)
    - "Emin#5" (an awkward way to name a major triad in the first inversion)

In situations where there is an ambiguity between possibile interpretations of a compound symbol, the parsers will always interpret an 
accidental immediately after an alphabetic note name as modifying the pitch of the note name:

    - "C#5" means "a 5 chord (powerchord) built from C#", NOT "C augmented"
    - "Eb5" means "a 5 chord (powerchord) built from Eb", NOT "E major flat five"

The internal symbol generation uses 1:1 symbols wherever possible, partly to avoid these kinds of ambiguities:

    - "C#maj#5" unambiguously means "a major chord built from C#, but override the fifth with a #5"
    - "Emajb5" unambiguously means "a major chord built from E, but override the fifth with a b5"


Tetrads 
+++++++

Seventh chords are formed according to common idioms:

- When "7" is appended to a note name alone, it indicates b7 over a major triad. 
- When "7" is appended to the "dim" suffix, it indicates a bb7 over a diminished triad.
- When "7" is appended to the "maj" suffix, it indicates natural 7.
- When "7" is applied to any other chord type suffix, it indicates a b7 over that chord type.
- When "maj7" is appended to a note name alone, it indicates a natural 7 over a major triad.
- When "maj7" is appended to another chord type suffix, it indicates a natural 7 over that chord type.

Examples:

- "G7" -> G B D F
- "Amin7" -> A C E G
- "Dmaj7" -> D F A C 
- "Fdim7" -> F Ab Cb Ebb
- "Gminmaj7" -> G Bb D F#
- "Bdimmaj7" -> B D F A#

When a seventh chord contains an altered fifth, we will always generate a compound symbol in which the 5 symbol comes *after* the 7 symbol. The reasoning behind this
is that "half-diminished" chords are generally written "m7b5" or "min7b5", and so we should also expect to have "maj7#5" or "7#5", and other symbols of that sort. 

- "Emin7b5"
- "G7b5"
- "Fmaj7#5"

In practice, chords with altered fifths are written in a wide variety of ways, and the parser will understand the variants, as long as none of the symbols conflicts with the others.

- "Gaug7", "G7aug", "Gaugb7" "G7+", "G+7", "G+b7" are all equivalent to the prescribed "G7#5"

In user generated symbols, the alias symbols of chord types will be treated as equivalent to the prescribed symbol:

- "BM7" and "BΔ7" are equivalent to "Bmaj7", but "B7" will imply a b7, as above.
- "G-7" and "Gm7" are equivalent to "Gmin7"

Conflicting symbols will be parsed along the same lines as in the triads:

- "Eb7" means "a b7 over a major triad built from Eb", NOT "a b7 over a major triad built from E"

However, the "b7" symbol will be understood correctly when it occurs after any other suffix:

- "Emajb7" is equivalent to "E7"
- "Eminb7" is equivalent to "Emin7".
- "Eminb5b7" is equivalent to "Emin7b5"

Sixth chords are formed according to common idioms:

- The '6' suffix indicates a major triad with a natural 6 (structurally, a min7 chord in the first inversion)
- The 'min6' indicates a minor triad with a natural 6 (structurally, a min7b5 chord in the first inversion)

Examples:

- "C6" -> C E G A (=Amin7)
- "Cm6" -> C Eb G A (=Am7b5)
- "Cdim6" -> C Eb Gb A (=Cdim7)

Other Polyads
+++++++++++++

The numerals 9, 11, and 13 may replace 7 in chord names. When this happens, 
the position of the numeral is interpreted along the same lines as the 7 in the 
seventh chords, but chord will also include all odd-numbered tones between
the seventh and the numeral.

Examples:

- Cmaj7   -> C, E, G, B
- Cmaj9   -> C, E, G, B, D
- Cmaj11  -> C, E, G, B, D, F
- Cmaj13  -> C, E, G, B, D, F, A
- Cm13    -> C, Eb, G, Bb, D, F, A

As above, an altered 5th comes *after* the numeral. E.g.:

- Cm9b5   -> C, Eb, Gb, Bb, D
- Cmaj7#5 -> C, E, G#, B
- C7#5    -> C, E, G#, Bb

However, since 'dim7' is a prescribed symbol, no altered 5th is necessary in, e.g.:

    - Cdim11  -> C, Eb, Gb, A, D, F

If an altered version of one of these extensions appears after an
unaltered precedent, and there are no other intervening symbols,
the chord will contain all the unaltered intervals, plus the 
altered interval. E.g.:

    - Cmaj11b13 -> C, E, G, B, D, F, Ab

However, if the unaltered symbol also included an altered fifth,
which is placed after the 7, 9, 11, or 13, then the additional
alteration is placed after the altered fifth. E.g.:

    - Cmaj11b5b13 -> C, E, Gb, B, D, F, Ab

While these symbols are easily understood by the parser, they are difficult for humans to read, and may be better replaced by a polychord symbol, e.g. "Cmaj7b5@Dminb5" (see below).


Polychords
----------

When a chord contains more than n intervals that cannot easily be fit into one of the structures in the list of most common candidates,
the program may attempt to assign a polychordal name to the interval structure (the tolerance can be set by the user). The prescription is to:

    - compare the intervals of the simple triads to establish the base type of the chord
    - once the base triad is found, superimpose the simple triads/tetrads/pentads, etc. and their inversions over each interval of the chromatic scale and compile a list of possible candidates

Although polychord symbols can be decoded into complex multi-octave interval structures, we restrict encoding polychord symbols to
the limits of the double octave; intervals beyond this range will be brought within it.


SCALES
------

When scale structures are parsed, our parsers will attempt to return one or more names for a given scale from 
the known names that match a given scale type. However, we also employ a system of unique canonical names for structures that serve as headings
for internal use and are at least vaguely descriptive with respect to some part of the interval structure.

The principles of the prescription of scale names are:

1. Assign a one-word label based on some interval of the scale that exists in contradistinction to a comparable interval of the diatonic scale, in order that the scale labels might approach some amount of actual descriptiveness. If the label cannot describe the structure in some way, then it should have some relationship to a relevant concept.
2. Establish a canonical primary form of a given interval structure so that inversions of that structure will always be related to it, rather than being mistaken for being a separate structure (e.g. ionian#4 and ionianb7 describe inversions of the same structure).
3. Establish a relative system of modal rotation, so that the existing names of the modes are employed in a consistent way across the different scales, given the canonical structures mentioned above.


HEPTATONIC SCALES
-----------------

The heptatonic series comprise the most common scales. Even many of these scales are
quite uncommon.

Diatonic Scale
    C D E F G A B

    A scale derived from the conjunction of two diatonic tetrachords, etymologized 
    by the Greeks as being arranged so that the intervals dividing the diatessaron 
    are 'stretched across' (*dia* 'across, apart' + *tonikos* from *teino* 'stretch') 
    to the greatest extent allowed under the rules of tetrachord construction.

Altered Scale
    C# D E F G A B

    A common designation from modern times, often Jazz music context. Structurally
    represents diatonic #1, but this makes every other interval 'altered' compared
    to the new relative tonic.

Hemitonic Scale
    C Db E F G A B 

    Our own designation, derived from the fact that the scale is the diatonic, except
    that the first interval is the hemitone instead of the tone.

Hemiolic Scale
    C D# E F G A B 

    Our own designation, derived from the fact that the scale is the diatonic, except
    that the first interval is the hemiolion instead of the tone.

Diminished Scale
    C D E F Gb A B

    Our own designation. There are many scales labelled diminished. This one is so-called
    because it is diatonic b5, and thus conceptually 'diminished' relative to the diatonic.

Augmented Scale
    C D E F G# A B

    Our own designation. There are many scales labelled augmented. This one is so-called
    because it is diatonic #5, and thus conceptually 'augmented' relative to the diatonic.

Harmonic Scale
    C D E F G Ab B

    Borrowing from the common designation 'harmonic major' scale. So-called because it is
    traditionally seen as the major version of the 'harmonic minor' scale (in our designation,
    however, that scale is labelled 'augmented aeolian').

Biseptimal scale
    C D E F G A# B 

    Placeholder name for now... Named for the fact that the scale enharmonically seems to have a b7 and natural 7.

Paleochromatic Scale
    C Db E F Gb A B

    The paleochromatic scale is the 'chromatic' scale of the ancient Greeks, derived from the conjunction of two chromatic tetrachords, 
    which were etymologized as being a more colourful (*chroma* 'colour') form of tetrachord. We have added the prefix to distinguish 
    between the modern sense of 'chromatic scale' (*paleo-* 'old, ancient').


Modes of the Heptatonic Series
------------------------------

We do not prescribe using the modes as descriptions of interval structures, but rather
as descriptions of relationships to a canonical primary centres of interval structures.
In this way, each modal name always describes the same degree of the scale, relative to 
the canonical forms described above (Ionian is always the canonical form).

Thus, we always relate the structures as expressions of an enumerated onomastic series:
    
        1. Ionian
        2. Dorian
        3. Phrygian
        4. Lydian
        5. Mixolydian
        6. Aeolian
        7. Locrian

Some people like to imagine that there is something like a 'Lydian' characteristic or an
'Aeolian' characteristic that governs the choice of names. The modal names of the scales
are inconsistent with any of the structures that the ancient Greeks laid out, but even 
the ancient Greeks applied the names inconsistently and with great variation in meaning.
Therefore, we preserve the names as a useful sequence, since many people already know it
in order, but we relieve ourselves of the necessity of thinking that a scale is misnamed
because an 'Aeolian' should have a b3, or that a 'Lydian' should have a #4.

We prescribe that the name of the canonical scale comes first, then the name of the mode. The parsers will recognize both orders as having the same meaning.

    - diatonic aeolian, A -> A B C D E F G
    - augmented aeolian, A -> A B C D E F G#
    - hemiolic aeolian, A -> A B C D# E F G

Modal Symbols
-------------

Interval structures can be expressed as modal symbols. 

The point of reference for each modal name is the parallel mode of the diatonic scale, and every modifier is understood
as *replacing* the corresponding note of the diatonic mode. If the modifier symbol is
already present in the underlying diatonic mode, no replacement will take place. In this 
context, the modifier symbols can never be used to make a scale other than a heptatonic scale. E.g.:

    - aeoliannat3 -> altered aeolian
    - lydianb3 -> harmonic lydian
    - phrygianbb7 -> hemitonic phrygian

The canonical modal symbol of any given interval structure will be derived from the canonical scales outlined above. Thus, the
program will always identify a collection as 'doriannat7', never 'ionianb3', since the canonical form of the parent scale is 'altered ionian'
and under this paradigm 'doriannat7' means 'altered dorian'.

Modifier symbols are '#', 'b', and 'nat' (= natural) plus a numeral between 2 and 7 (we do
not allow for a sharp tonic, although it may be conceptually useful). No matter how the user
attempts to rationalize a modal symbol, the parser will relate it to the canonical scales and
their modes when seeking a match:

    - mixolydianb6 -> altered aeolian
    - lydian#6 -> hemiolic lydian
    - dorian#4nat7 -> harmonic lydian

Extended Modal Symbols
----------------------

In the same way as chords, we allow that a scale of more than 7 notes might include extra interval symbols with the 'add' suffix, or that a scale of
fewer than 7 notes might drop an interval with the 'no' suffix. The numerals must be flat or sharp as absolute references (a 'no5' does not negate a b5 in 'locrianno5', the symbol must be 'locriannob5').

When handling scales outside the heptatonic series, we prescribe the use of simple names outlined in the following sections, rather than using the modal symbols. Because scales with even numbers of notes are often symmetrical along at least one axis, the relation of any given extended modal symbol to the canonical form is inherently arbitrary. If the parser is forced to generate a modal symbol, it will follow the following prescription:

    - If the tonic tetrad of the given structure appears in the diatonic scale, take the first mode in which it appear as canonical. 
    - If the tonic tetrad is not found in the diatonic scale, we follow the sequence of the heptatonic scales as they are presented above until we find a scale in which the tetrad appears, and consider the first mode in which that tetrad appears to be the canonical mode. 


OCTATONIC SCALES
----------------

Octatonic scales can simply be considered as heptatonic scales with chromatic notes, but we do prescribe a set of symbols for dealing with 
specific types of octatonic interval structures.

Tonic-Diminished Scales
-----------------------

When a chord containing a natural 6 or flat 7 is superimposed with a diminished 7th chord a tone sharper, the resulting scale is 
a tonic-diminished scale. The symmetries of these scales mean that every other chord is an inversion of either the tonic or a diminished 7th, provided
we take 'thirds' consisting of every other interval (other chords are still possible of course). E.g.:

    - maj6 diminished: C D E F G Ab A B = C6, Ddim7, C6/E, Fdim7, C6/G, Abdim7, C6/A, Bdim7
    - min6 diminished: C D Eb F G Ab A B = Cm6, Ddim7, Cm6/Eb, Fdim7, Cm6/G, Abdim7, Cm6/A, Bdim7
    - dom7 diminished: C D E F G Ab Bb B = C7, Ddim7, C7/E, Fdim7, C7/G, Abdim7, C7/Bb, Bdim7
    - dom7b5 diminished: C D E F Gb Ab A Bb = C7b5, Ddim7, C7b5/E, Fdim7, C7b5/Gb, Abdim7, C7b5/Bb, Bdim7

The maj6 diminished is an inversion of the min7 diminished, and the min6 diminished is an inversion of the m7b5 diminished. In addition, the
7b5 diminished is an inversion of its own tritone mirror.


