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

    Cmaj#5  Aminb5    Ebmajb5

Exceptionally, 'dim7' is prescribed instead of the structural 'minbb7b5', for
its readability and common usage. Although 'dim' and 'aug' are not prescribed 
in any other contexts, the user should note that these symbols refer to 
*triads* with a 3rd and 5th, rather than simply the interval of an altered 5th.

Seventh chords are formed according to common idioms:

- The '7' suffix indicates b7
- The '7' suffix indicates a bb7 if combined in 'dim7' suffix
- The '7' suffix indicates natural 7 if combined in the 'maj7' suffix
    - A chord suffixed 'maj7' implies a major 3 with natural 7, unless
    combined with another suffix that suggests that there should be a 
    minor 3.
E.g.:

    Amin7     G7      Dmaj7       Fdim7
