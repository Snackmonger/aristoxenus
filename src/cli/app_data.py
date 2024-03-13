from rich import theme


MAIN_THEME = theme.Theme({
    "title": "red u",
    "emphasis1": "dark_slate_gray2",
    "emphasis2": "yellow",
    "warning": "black on white"
})


TOPIC_DATA = {"aristoxenus": "Description of the historical figure, Aristoxenus of Tarentum.",
              "author": "Description about the author of this library.",
              "history": "Project history", 


              "future": """
              
              [title]Future Ideas[/title]
              ============

              Eventually, I would like to develop this library so that it can procedurally generate melodies. As a base for this, I will have to develop a
              way to encode 'creative' ideas as a shorthand for melodic formation in a programmatic way. An offshoot of this functionality would also aim to
              use the system to be able to generate practice material in the form of etudes based on different permutations.
              """,

              "scales": """
              
              [title]Aristoxenus Scale System for Heptatonic Ordering with Logic and Ease[/title]
              ====================================================================
              
              In the internal workings of the program, it's useful to be able to refer to scales as having a 'canonical' form. 
              This form allows us to characterize scales in simple and consistent ways, rather than relying on the rather 
              capricious names that make up abstract scale theory. In the internal system, the heptatonic series is derived 
              from the transformation of scale tones of the diatonic scale, such that each scale is diationic with one note moved.
              The series is concluded with the sister scale of the diatonic, which in ancient times was called chromatic; this 
              scale is diatonic with two notes moved and was included in the library for reasons pertaining to historical interest. 
              Each scale in the system is given a single canonical name. The system treats modal names as degrees of rotation, 
              since the names themselves have no relation to the thing they describe. Thus, ionian is always mode 1 of the 
              canonical scale, dorian is always mode 2, etc. The modal names are never understood as implying anything about the 
              interval structure of the resulting scaleform; they simply indicate how many degrees of rotation the form is from the 
              canonical parent.
              
              The scales are:
              
              diatonic      :   The ancient scale made of two diatonic tetrachords. This is the fundamental reference point of the system.
              altered       :   Diatonic #1. Named because "altered" is already a common name.
              hemitonic     :   Diatonic b2. Named because the first interval above the tonic is the hemitone.
              hemiolic      :   Diatonic #2. Named because the first interval above the tonic is the hemiolion.
                ---             Diatonic #4 is a rotation of diatonic already.
              diminished    :   Diatonic b5. Named because of the characteristic diminished fifth above the tonic.
              augmented     :   Diatonic #5. Named because of the characteristic augmented fifth above the tonic.
              harmonic      :   Diatonic b6. Named because "harmonic major" is already a common name.
              biseptimal    :   Diatonic #6. Named because the scale sounds like it both has a major and minor seventh.
                ---             Diatonic b7 is a rotation of diatonic already.
              paleochromatic:   The ancient scale made of two chromatic tetrachords, but it has been renamed to avoid confusion with the modern chromatic scale.
              
              """}
