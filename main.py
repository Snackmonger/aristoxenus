import pandas

from src.models import diagrams




diagr = diagrams.guitar_tuning(format_='plain')
data = pandas.DataFrame(diagr)

print(data)