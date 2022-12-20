import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

loc = 'PAV.xlsx'
x = pd.read_excel(loc, sheet_name="САФ")
print(x)
