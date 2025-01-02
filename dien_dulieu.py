from numpy import nan as NA
import pandas as pd

data = pd.DataFrame([[1., 6.5, 3.],
                     [1., NA, NA],
                     [NA, NA, NA],
                     [NA, 6.5, 3.]])
print(data)
print("-"*10)
cleaned = data.fillna(data.mean())
print(cleaned)
cleaned2 = data.fillna(data.mode())
print(cleaned2)
cleaned3 = data.fillna(data.median())
print(cleaned3)