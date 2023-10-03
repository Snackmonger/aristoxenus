import pandas as pd

from data import intervallic_canon, keywords
from src import bitwise

x = intervallic_canon.HEPTATONIC_SYSTEM

data = {}
for scale, name in x.items():
    data.update({name: bitwise.inversions(scale, 12)})

dataframe = pd.DataFrame(data, index=keywords.MODAL_NAME_SERIES)

print(dataframe)

locate = dataframe.loc['lydian']

print(locate)

print(bin(int(locate['harmonic'])))
'

# Tonal matrix
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# '