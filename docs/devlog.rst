==========================
Aristoxenus Library DevLog
==========================

.. contents:: Table of Contents

27/09/2023
==========
    Added models for pitch structures with methods for rotation and easy collation of variants. I have taken a mostly functional-style
    approach to this program, but the impulse to write classes is strong. We don't really have much state that needs preserving, and 
    the classes' methods really just refer back to functions that operate independently of state. After writing the classes, I started
    using them to simplify operations in some of the other functions, but now this seems like a defect, since they just refer to the
    functions anyway... what's the point of the classes, and why should the functions come to depend on them?

    The classes gave me an opportunity to learn a little bit about decorators. I am still pretty unconfident with decorator syntax, especially
    understanding how the nested structure affects type hinting, and how we can keep similarly-named parameters from becomming confused. I'm sure 
    I will completely re-write these at some point in the future, especially since Python 3.12 is adding some new type-hintning support for generics.
    Eventually the classes will be useful for encapsulating more complex data (for which the functions don't yet exist), so I'll avoid scrapping them,
    hideous though they are.

    The new `permutation` module introduces some simple functions that take basic structures and turn them into other structures.
        `chordify`
            Turns a scale into a chord scale, with any pattern of chord structures (e.g. triads, tetrads, pentads, tertial, quartal, quintal, and even beyond)
        `inversions`
            Permutes all the possible rotations of a given interval structure. Essentially this amounts to getting all inversions/modes.
        `iterate_intervals`
            Returns the individual intervals of any interval collection. We can use `inversions` on a given scale to find out the modes, then call this function to 
            grab all the individual intervals, which can then be used to check against known structures.
        `drop_voicing`
            Takes a close-voiced chord (or any interval structure within an octave) and applies a given transformation, displacing certain intervals into a different
            octave to create a new voicing of the same chord.
        

    Refined some of the bitwise operations a bit, and cleaned up some redundant code there and elsewhere. I am learning more about how to do functional-style 
    programming better, so I have looked for places where `map`, `reduce`, and `filter` might simplify the code. Still have a lot to learn.

    Begin replacing docstrings with something more consistent. They take up a lot of space, but, if nothing else, they have already proven
    valueable since I keep forgetting what I was thinking when I wrote the functions in the first place. Doctests are super helpful too!

    Reorganized the filestructure a bit. I'm not super happy with it, but the program keeps growing and apparent needs keep changing, so it's 
    hard to anticipate what I'll want even a week from now. Some of the code is hard to place, since it relies on multiple modules, but doesn't
    quite fit the mold of this module or that.


14/09/2023
==========
    I started learning Python around 15 February, 2023. This will serve as a DevLog for what has, surprisingly, become a much more involved
    project than I originally thought. 
    
    This is a passion project that serves as a sort of motivation and road-map to learning Python; 
    if I need to write a function that does X, I am forced to learn it and implement it. Usually, investigating solutions to unfamiliar
    problems introduces me to lots of new concepts I didn't know about before.

    This project actually began a couple months ago.  Since I was interested in music, writing a music-related program was an attractive choice. The original version
    of the program was pretty simple, since I had only been studying Python for about 2 months at that point. One of the things that
    irked me was how many times I was typing out note names in order to do things like enharmonic conversion; I decided that when the
    time came to revise the program (after learning a bit more about programming) I would try to write it in such a way that all the 
    different variants for things like C# D# F# G# A# = Db Eb Gb Ab Bb would be automatically defined through functions. 
    
    This formed the backbone for the current `nomenclature` module, which does some cool things:

    `chromatic`
        Creates a chromatic scale using sharps, flats, or binomial (e.g. C#|Db) note names.
    `decode_enharmonic`
        Translates any note with lots of sharps or flats back into a neutral binomial form (e.g. A#### -> 'C#|Db').
    `encode_enharmonic`
        Translates a note name so as to have another alphabetic name, plus however many sharps or flats bring it into the same enharmonic value (e.g. C#, A -> A###).
    `scientific_range`
        Creates a long chromatic scale of 9 octaves (108 notes), made up of scientific note names (e.g. C4) in any of the three accidental styles from `chromatic`.
    `equal_temperament`
        Creates a range of frequencies corresponding to the range of the scientific note names (108 frequencies).
    `convert_note_to_frequency`
        Translate scientific notes (e.g. A4) of any accidental type (#, b, #/b) to frequencies (e.g. 440 hz) 
    `convert_frequency_to_note`
        Translate a frequency to a scientific note name, in any of the three accidental styles from `chromatic`.
    `force_heptatonic_scale`
        Force a given heptatonic interval structure to follow ABCDEFG nomenclature regardless of any accidentals.
    `best_heptatonic_scale`
        Choose the best name for a given interval structure and tonic note name.

    I also began working on a module related to nomenclature, `parsing`, which can do a few things so far:

    `parse_chord_symbol`
        Attempt to generate an interval map from the sub-symbols in a given chord symbol (e.g. Em7b5 >> 0b10001001001).
        This function delegates to auxiliary functions `parse_slash_chord_symbol` and `parse_polychord_symbol`, each of 
        which does what it says.

    `parse_scale_structure`
        Attempts to give a name to a heptatonic scale. This function is only partially operational so far, since we need to develop the `permutation`
        module to help create the variants that the parser will check against.

    This naturally entailed writing some bitwise operation functions to help process interval structures as integers, which was the beginning of the `bitwise` module.
    I have seen some other programs use bits to represent a scale, but they seem to use the most significant bit as the lowest pitch, wheras I use the least significant bit. 
    The advantages of their way is that it's easy to create modal rotations, since the bit-length is always consistent. The disadvantage is that intervallic structures larger
    than 12 bits must be dealt with as separate structures, so the 12-bit framework really works best for scales and chords that fit within an octave.

    In my way (which I'm sure is not really "my" way), the advantage is that we can always keep adding more intervals to the structure, and it can theoretically grow to any size. This means that 
    we can represent the whole compass of a given instrument without needing to adopt a different system of tracking pitch relationships. A piano is treated
    in fundamentally the same way as a triad, and many functions in the program do not need to distinguish between them based on size (although some certainly do). The disadvantage of my way is
    that every interval structure needs to track its expected number of bits, because we will inevitably lose intervals to leading zeroes if we try to rotate
    the structure. A second disadvantage is that our theoretical structure might exceed the 108-note-name limit (artificially) imposed by the `nomenclature` module.
    All in all, these seem like pretty minor concessions for what is otherwise a pretty straightforward and robust way of handling pitch relationships.

