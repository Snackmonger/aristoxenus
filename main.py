import pandas

from src.models import diagrams




diagr = diagrams.guitar_fretboard(format_='plain')

#diagr = diagrams.filter_guitar_fretboard(diagr, ['C', 'E', 'G', 'B'])

data = pandas.DataFrame(diagr)

print(data)

ff = diagrams.get_positional_fingering(diagr, 5, 5)

gg = diagrams.filter_guitar_fretboard(ff, ['A', 'C#|Db', 'E', 'G'])

data = pandas.DataFrame(gg)

print(data)