This document is just a scratchpad of miscellaneous ideas. 

Auxiliary Chord Nomenclature for Internal Use Only
--------------------------------------------------

In order to be able to indicate voicings and inversions succinctly in chord symbols,
we could develop a system of annotations that can be attached to the base chord symbols
used by the program. 

Example
+++++++

Major 7th chord 

    Cmaj7           (close-voiced, root position by default)
    Cmaj7{1}[d2]    (drop 2, first inversion)
    Cmaj            (close-voiced, root position by default)
    Cmaj[d24]       (drop 2 and 4, root position by default)
    Cmaj7(1573)     (explicit BTAS instructions using a chord's known notes, will assume interval degrees)

Rules
+++++

Curly braces may be used in conjunction with square brackets, but neither can be used in conjunction with parentheses.

Curly Braces
    Annotate the inversion of the chord. We should accept classical-style voicings (e.g. {64} or {6/4}) or simple chars (e.g. {2})

    Triads
        53, 5/3, r, R = root position 
        63, 6/3, 1, f = first inversion
        64, 6/4, 2, s = second inversion

    If the triad annotations are applied to tetrads, we assume that they have these meanings:
        753, 7/5/3      (short form: 7)
        653, 6/5/3      (short form: 65, 6/5)
        643, 6/4/3      (short form: 43, 4/3)

    The tetrads also have 642, 6/4/2 = third inversion (short form: 24, 2/4)

Square Brackets
    Annotate the structure of the chord after the inversion has been performed, or on the root position if no inversion was specified.

    For this reason, a chord could be annotated as C{6/4}[o], and the actual structure would be 11/6, since the 4 was transposed up and octave by the o=open voicing annotation.

Parentheses
    Annotate the explicit structure of a chord based on the intervals indicated in its base symbol (relative intervals). The parentheses 

    Cmaj7(1537) -> C G E B
    Cmin7(1537) -> C G Eb Bb
    Cmaj7(1537) -> C G E B

PROBLEM: What happens when we want to put an 11 or 13 in a chord?

    Cmaj11(1593117) :-: will the 11 be interpreted as F or CC?

SOLUTION: Only allow this shorthand for triads/tetrads whose compass is within an octave

PROBLEM: What happens when we have a suspended tetrad?

    C7sus4(5417)

Double problem: we also do not even have a way of generating suspended chords with extensions properly! This symbol C7sus4 would recognize C7 C E G Bb, then sus4, yielding C E F G Bb...
    Solution (chord parsing module) -> if sus2/sus4 in chord name, check if maj/min in explicit symbols and remove if so. 
                                    -> or just simply add no3, nob3?

SOLUTION: what if we just rename 2 and 4 as 3, and treat 1357 as being equivalent to index 0123 of the root position chord?
          or simply treat 1(234)57 as equivalent to 0123 in the root position?
          This would work the same for 6th chords -> 1(234)5(67) 
          And for triads -> 1(234)5, since anything with a 6 or 7 is just an inversion of a simpler root position chord.

PROBLEM: The inversions in the figured bass follow SATB, but the parentheses follow BTAS. Is this inconsistency unreasonable? I kind of prefer reading bass to soprano


Chord Substitution Matrix
-------------------------

When comparing two chords, if one chord can be expressed as n-1/n or n/n+1 relative to another chord, where n is the number of notes in the
other chord, then the one chord will be considered a suitable substitute for the other. It necessarily follows that substitutes therefore exist
in complementary distributions, so that if one chord is a substitute for the other, then the other will also be a substitute for the one.

Example 
+++++++

C E G   and     E G B
=====================

The first chord can be expressed as {E G}/{E G B} relative to the second chord, and the second chord can be expressed as {E G}/{C E G} relative to the first chord. Therefore, the two chords are substitutes of each other.

F A C E     and     A C E G
===========================

{A C E}/{F A C E} or {A C E}/{A C E G}


Partial Chord Substitutions
+++++++++++++++++++++++++++

In jazz practice, a substitution might be based on the premise that a chord shares a 37 with its mate, but the notes are not necessarily distributed in an n/n+1 fashion.
