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

    - Cmaj#5  
    - Aminb5    
    - Ebmajb5

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

    - Amin7
    - G7      
    - Dmaj7       
    - Fdim7

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

The parsers will attempt to return one or more names for a given scale from 
the known names that match a given scale type. However, the names given to
scales are, at best, obscure and, at worst, actually impedimental to the 
understanding of the underlying structure.

The goals of the prescription of scale names are:

    1. Describe some interval of the scale that exists in contradistinction to a
    comparable interval of the diatonic scale, in order that the scale labels 
    might approach some amount of actual descriptiveness.
    2. Establish a canonical primary form of a given interval structure so that 
    inversions of that structure will always be related to it, rather than being
    mistaken for a separate structure.
    3. Establish a relative system of modal rotation, so that the existing names
    of the modes are employed in a consistent way across the different scales, 
    given the canonical structures mentioned above.


    HEPTATONIC SCALES
    -----------------

    The heptatonic series comprise the most common and uncommon scales. Beyond
    this series are many other scales, but few that are found in common use, or
    which cannot adequately be described using 'pantonic' scale rules. Even inside
    the heptatonic series, there are many scales that are so uncommon that we don't
    bother incorporating them into our system of nomenclature.

