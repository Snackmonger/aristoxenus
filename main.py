import pandas

from src.models import diagrams




diagr = diagrams.guitar_fretboard(format_='plain')

diagr = diagrams.filter_guitar_fretboard(diagr, ['C', 'E', 'G', 'B'])


data = pandas.DataFrame(diagr)

print(data)