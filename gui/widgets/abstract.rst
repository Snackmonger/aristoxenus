WIDGET ABSTRACTS
================


FINGERING DIAGRAM WIDGET
++++++++++++++++++++++++

The fingering diagram widget displays a grid representing the frets on a section of a guitar fretboard. In its default form, it allows the user to 
choose various options for displaying scale and arpeggio forms in positional fingerings of 4 or 5 fret spans in standard tuning. 

STRING FINGERING PANEL:
    For each STRING in the diagram, we have an option to define FINGER STRETCH, so that the user 
    can decide the format of the fingering of individual strings.

SCALE FORM PANEL:
    Allows the user to set the basic parameters of the diagram.

        KEYNOTE
            dropdown menu, always in binomial form.
        SCALE
            dropdown menu, derived from the heptatonic transformations.
        POSITION 
            dropdown menu, with values derived from the scale's notes on the lowest string.
            Position options need to be reloaded each time the scale is changed, therefore, 
            we should always force the position dropdown menu to one of the available options,
            so it can't accidentally remain set on a position that's no longer legal.

MAIN PANEL:
    The main panel will be different depending on which mode the program is in.
    
SCALE MODE:
    Scale mode allows the user to assign shapes and colours to the diagram nodes. 

NODE OPTIONS:
    Nodes in the diagrams will have some options so the user can control how the diagram looks.
        
        SHAPE
            MenuOption(circle, triangle, inverse triangle, square, diamond)
        COLOUR 
            this could be a colour picker widget? boxes? radial dial?
        TEXTCOLOUR 
            same
        TEXTSIZE 
            combobox widget

ARPEGGIO MODE:
    Arpeggio mode allows the user to see how arpeggios fit into positional fingerings. 
    
    It does this by making scale notes look like grey circles, but chord tones still have the same node options available as in
    scale mode. 
    
    The current chord is chosen from a dropdown menu of all scale degrees. 
    
    Arpeggio mode also has a dropdown menu to choose the basic composition of the chord: tertial, quartal, triad, tetrad, pentad, hexad.
    
    Arpeggio mode also has a toggle to decide whether the intervals are represented from the tonic of the parent 
    scale, or from the root of the current chord.


