=============================================================
ARISTOXENUS STANDARD STRUCTURAL SYMBOL PRESCRIPTION (12-TONE)
=============================================================

This is a guide to the form of interval structure symbolism and nomenclature that the program uses
for its internal reference, and which is the default representational style used for display to the user. 
The included parsers are generally capable of encoding/decoding the most common symbols and names, so the user
is NOT bound by the program's prescription when entering symbols.

CHORDS
------

Chord names are meant to (as much as is practical):

1. Be easily understandable in the context of existing chord name conventions
2. Employ consistency in the structural arrangement and meaning of symbols
3. Represent a 1:1 correspondence between symbol and interval

Not all of these goals are met with the same ease, and the existing prescription
is a compromise between them.

- Major third is indicated with 'maj' suffix.
- Minor third is indicated with lowercase 'min' suffix.

We assume that a chord contains a p5 unless a symbol indicates otherwise.
Therefore, we refer to augmented chords as 'maj#5' and diminished chords
as 'mb5'. E.g.:

    - Cmaj#5 >> C E G#
    - Aminb5 >> A C Eb
    - Ebmajb5 >> Eb G Bb

Exceptionally, 'dim7' is prescribed instead of the structural 'minbb7b5', for
its readability and common usage. Although 'dim' and 'aug' are not prescribed 
in any other contexts, the user should note that these symbols refer to 
*triads* with a 3rd and 5th, rather than simply the interval of an altered 5th.

Seventh chords are formed according to common idioms:

- The '7' suffix indicates b7
- The '7' suffix indicates a bb7 if combined in 'dim7' suffix
- The '7' suffix indicates natural 7 if combined in the 'maj7' suffix
- A chord suffixed 'maj7' implies a major 3 with natural 7, unless combined with another suffix that suggests that there should be a minor 3. 

E.g.:

    - Amin7 >> A C E G
    - G7 >> G B D F
    - Dmaj7 >> D F A C 
    - Fdim7 >> F Ab Cb Ebb
    - Gmmaj7 >> G Bb D F#

Extensions 9, 11, and 13 may replace 7 in the above constructions.
Each new extention also includes the previous one(s). The resulting 
chord will have an idiomatic seventh as above, but the extensions are 
always natural intervals. 

    - Cmaj7   >> C, E, G, B
    - Cmaj9   >> C, E, G, B, D
    - Cmaj11  >> C, E, G, B, D, F
    - Cmaj13  >> C, E, G, B, D, F, A
    - Cm13    >> C, Eb, G, Bb, D, F, A

As above, an altered 5th comes *after* the 
numeral. E.g.:

    - Cm9b5   >> C, Eb, Gb, Bb, D
    - Cmaj7#5 >> C, E, G#, B
    - C7#5    >> C, E, G#, Bb

However, since 'dim7' is a prescribed synbol, no altered 5th is
necessary in, e.g.:

    - Cdim11  >> C, Eb, Gb, A, D, F

If an altered version of one of these extensions appears after an
unaltered precedent, and there are no other intervening symbols,
the chord will contain all the unaltered intervals, plus the 
altered interval. E.g.:

    - Cmaj11b13 >> C, E, G, B, D, F, Ab

However, if the unaltered symbol also included an altered fifth,
which is placed after the 7, 9, 11, or 13, then the additional
alteration is placed after the altered fifth. E.g.:

    - Cmaj11b5b13 >> C, E, Gb, B, D, F, Ab

The 'add' type prefixes indicate that the specified interval is 
added to the structure of the preceding symbol, without including
any other interval. 

SCALES
------

When scale structures are parsed, our parsers will attempt to return one or more names for a given scale from 
the known names that match a given scale type. However, the names given to scales are, at best, obscure and, at worst, actually impedimental to the 
understanding of the underlying structure. Therefore, we employ a system of unique canonical names for structures that serve as headings
for internal use and are at least partially descriptive with respect to some part of the interval structure.

The principles of the prescription of scale names are:

1. Assign a one-word label based on some interval of the scale that exists in contradistinction to a comparable interval of the diatonic scale, in order that the scale labels might approach some amount of actual descriptiveness. If the label cannot describe the structure in some way, then it should have 
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

    - diatonic aeolian, A >> A B C D E F G
    - augmented aeolian, A >> A B C D E F G#
    - hemiolic aeolian, A >> A B C D# E F G

Modal Symbols
-------------

Interval structures can be expressed as modal symbols. 

The point of reference for each modal name is the parallel mode of the diatonic scale, and every modifier is understood
as *replacing* the corresponding note of the diatonic mode. If the modifier symbol is
already present in the underlying diatonic mode, no replacement will take place. In this 
context, the modifier symbols can never be used to make a scale other than a heptatonic scale. E.g.:

    - aeoliannat3 >> altered aeolian
    - lydianb3 >> harmonic lydian
    - phrygianbb7 >> hemitonic phrygian

The canonical modal symbol of any given interval structure will be derived from the canonical scales outlined above. Thus, the
program will always identify a collection as 'doriannat7', never 'ionianb3', since the canonical form of the parent scale is 'altered ionian'
and under this paradigm 'doriannat7' means 'altered dorian'.

Modifier symbols are '#', 'b', and 'nat' (= natural) plus a numeral between 2 and 7 (we do
not allow for a sharp tonic, although it may be conceptually useful). No matter how the user
attempts to rationalize a modal symbol, the parser will relate it to the canonical scales and
their modes when seeking a match:

    - mixolydianb6 >> altered aeolian
    - lydian#6 >> hemiolic lydian
    - dorian#4nat7 >> harmonic lydian

Extended Modal Symbols
----------------------

In the same way as chords, we allow that a scale of more than 7 notes might include extra interval symbols with the 'add' suffix, or that a scale of
fewer than 7 notes might drop an interval with the 'no' suffix. The numerals must be flat or sharp as absolute references (a 'no5' does not negate a b5 in 'locrianno5', the symbol must be 'locriannob5')

Because scales with even numbers of notes are often symmetrical along at least one axis, the relation of any given extended modal symbol to the canonical form
is inherently arbitrary. We prescribe taking the first instance of the tonic tetrad in the diatonic scale, if it exists, and using that as the canonical mode. If the tonic
tetrad is not found in the diatonic, we follow the sequence of the heptatonic scales as they are presented above until we find a scale in which the tetrad appears, and
consider the first mode in which that tetrad appears to be the canonical mode.

Octatonic Scales
----------------

There are a number of octatonic scales that we treat as canonical. These scales are often symmetrical, and have fewer modes than they have notes. Therefore, we
cannot say that 


Diminished Scales
-----------------

