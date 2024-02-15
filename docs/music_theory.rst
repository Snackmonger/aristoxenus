=======================================
ARISTOXENUS MUSIC THEORY REFERNCE GUIDE
=======================================

.. contents:: Table of Contents

Abstract Concepts
=================

Pitch height
------------
In English, and many other languages, the multiplication of a frequency is expressed in terms of height, and the division of frequency
is expressed in terms of depth. This is a type of widespread, but not universal metaphor.

For the ancient Greeks, who named their notes after the corresponding strings of the lyre, the note called 'lowest' (*nete*)
referred to what English speakers think of as the 'highest' pitch of the system, while the note called 'highest' (*hypate*)
referred to what English speakers think of as the 'lowest' pitch. 
The philosopher and historian Plutarch of Chaeroneia (mid 1st- early 2nd century A.D.) has this to say about the idea of high and low pitch:
    Or is it a ridiculous thing to allot 'first' and 'middle' and 'last' to positions, when we observe that the note *hypate* is 
    the highest and first (τὸν ἀνωτάτω καὶ πρῶτον) on the lyre, but the low and last (τὸν κάτω καὶ τὸν τελευταῖον) on the auloi; 
    or, moreover, that the note *mese* sounds sharper than hypate and heavier than *nete*, in whatever position of the lyre someone 
    might place it, as long as the tuning is consistent? [#]_

In more modern times, it has sometimes been assumed that the tendency to conceptualize pitch in terms of height is actually reflective
of innate human perceptual associations. Since the 1970s, renewed scholarly interest in the question has cast doubts on some of those
old assumptions, and scholars are increasingly finding that linguistics plays a crucial role in how and when humans adopt metaphors to
describe pitch relationships. Although the question of the innateness of pitch perception has not been conclusively answered, it has become
increasingly clear that cultures that do not employ language relating to height have a strong tendency not to conceptualize pitch in terms of height, and may
actually even adopt the contradictory orientation. [#]_

The contradictory orientation, in which the high notes are characterized as low and vice-versa, is known in the Greek theorists as well, 
for instance Nicomachus of Gerasa:
    An octave is a systema either above *mese* until *proslambanomenos*, or below *mese* until *nete hyperbolaion* in eight strings… [#]_

The note name *proslambanomenos* means 'additional', and it was a note added beyond the *hypate hypaton*, which literally means 'highest of the highs'. For English speakers,
however, this is the 'lowest' note of the system, which the author characterizes as being "above *mese*", (*mese* means the 'middle' note). By contrast,
the note *nete hyperbolaion* literally means 'lowest of the excessive notes' (referring to the fact that this tetrachord was a late addition that exceeded the span of previous musical systems),
but is what English speakers would characterize as the 'highest' note of the system.

Now, in spite of the fact that the Greeks did call their notes after their height and depth, they were inconsistent about applying these names to the abstract concept of pitch. This means that 
even though a note might be called 'high', they did not extend this description to other musical features. For instance, a melody that moves towards a note called
'high' is never described as an 'ascent'. Similarly, a movement toward the note called 'low' is never described as a 'descent'. Terms for high and low, ascent and descent, do not apear consistently
in Greek until around the 10th century (although they are rarely used in inconsistent ways before then). So, even while some terms relating to height were used by the Greeks in their note names, they do not seem to have
extended this concept to other types of musical metaphorical language.

Notes are characterized as 'sharp' and 'heavy' in the Greek system. The note called 'lowest' is the 'sharpest' in the Greek system, which we would call 'highest'. Conversely, the note
called 'highest' is the 'heaviest' in the Greek system, which we would call 'lowest'. When the Greeks referred to changes of pitch, they did not call that 'ascent/descent' as we do, 
but they also did not refer to it as 'sharpening/weighting' as the terms 'sharp' and 'heavy' might suggest. Instead, they refer to the increase of pitch as a 'tightening', and to the decrease
of pitch as a 'loosening', again deriving the terminology from the strings of the lyre.

.. [#]  Plut. *Platonicae Quaestiones*, 1008e.
.. [#]  See, e.g. Smith-Sera 1992, Martino-Marks 1999, Shayan 2011, Dolscheid-Shayan-Majid-Cassanto 2013, Dolscheid 2017, Majid 2018, Dolscheid 2020.
.. [#]  Nicomachus of Gerasa, *Harmonicum Enchiridion*, 12.1.

Next Topic
----------
This is the beginning of the next topic. Does it get added under the previous one in the table of contents?

Glossary
========

Octave 
------
    (Gk. *dià pasõn*, "though all (the notes)")

An octave is the name the 1:2 ratio between two frequencies (or 2:1).
A frequency that stands in this ratio to another frequency can be said to be the 'octave' of that frequency, and vice-versa.
- 440Hz is a lower 'octave' of 88Hz
- 660Hz is a higher 'octave' of 330Hz

The term 'octave' is also used in a related sense to refer not to the notes that define the limits of the relationship,
but to the amount of distance between those limits.
- A major third is within the range of an 'octave' (i.e a pitch and its octave), but a major ninth is outside the range of an 'octave'

When one note is an octave of another note, it carries the same alphabetic name. We can distinguish notes with the same name in different octaves
by assigning a numeral to the name, thereby creating scientific notation (e.g. C2, A#5, D#|Eb3)


Interval
--------
    (Gk. *diastema*, "standing apart")

An interval is the name we give to the magnitude of difference between two frequencies. The perfect intervals of an octave can be expressed as simple
fractions (1/1, 2/1, 4/3, 3/2), in which the numerator represents the lower frequency and the denominator represents the higher. In 12-tone equal temperament, 
most intervals will not correspond exactly to their ideal fractional representation; the octave, diatessaron, and diapente are fairly close to their ideal mathematical forms,
the ditone and hemiolion are quite far from their ideal mathematical forms.

In the Aristoxenus library, the nomenclature module is designed specifically to accommodate systems of twelve named notes, but the specific temperament and intonation
of those notes is not inherently tied to 12-tone equal tempered frequencies. So, an interval described as a 'ditone' might be assigned a frequency value closer or further from 
that of a true ditone (depending on the system of temperament) even though its alphabetic representation remains the same.


Interval Structure
------------------
Generic term used by the Aristoxenus library to refer to all types structures made up of more than one pitch, whether chords, chordioids, scales, intervals, sytemata, or chromatics.

Interval structures are stored simply as integers; their binary representation serves as a map of their structures, in which the least significant bit serves as the lowest
note of the structure, and all other flipped bits are contextualized as intervals above that bass. Since all intervals and interval structures use the least significant bit
as the basis for the rest of the structure, all simple intervals and compound interval structures used by the library will be odd numbers.


Binomial
--------

This is the term used in the Aristoxenus library to refer to notes of the type 'G#|Ab', in which
a note is simultaneously characterized by two names (hence 'binomial'), separated by the '|' bar character. I don't think anyone else 
refers to notes with the term 'binomial', but it was convenient to have a simple, one-word descriptor for notes as
absolute enharmonic values, in contradistinction to the sharps and flats (which have relative enharmonic values). The program uses the binomial notes
as a template for named alphabetic structures when considering abstract relationships, then renders those 
structures more precisely into sharps and/or flats when requested.

When the 'imaginary' binomials are combined with scientific numerals, they exist in a 1:1 relationship with the frequencies
of the 12-tone octave, since each frequency corresponds to one (and only one) symbol. The 'real' note names (i.e. sharps 
and/or flats), on the other hand, exist in a 2:1 relationship, since each frequency corresponds to two different symbols.


Plain / Scientific
------------------

The Aristoxenus library refers to note names in two ways: notes that carry a numeral representing their octave are referred to
as 'scientific', and notes that do not are referred to as 'plain'. Thus, notes can be a combination of sharp, flat, or binomial
on the one hand, and plain or scientific on the other, and any combination of the two (e.g. 'plain sharps', 'scientific flats', 'plain binomials', 'scientific binomials').


Tetrachord
----------
    (Gk. *tetrachordon*, "four-string (group)")



Genus
-----
    (Gk. *genos*, "kind, type")


Species
-------
    (Gk. *eidos*, "appearance, form" or *schema*, "appearance, form")


Close Voicing
-------------


Spread Voicing
--------------


Drop Voicing
------------

Term used to refer to a type of chord in which one or more of the intervals has been "dropped" by an octave from its normal range. These chords are common 
in guitar performance, where the standard tuning makes root-position voicings more difficult.