import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

loc = 'PAV.xlsx'


def basa(s):
    x = pd.read_excel(loc, sheet_name=s)
    x.columns
    x['Unnamed: 1'][1:]
    names = x.columns.tolist()
    # print(names)

    plt.figure()
    for i in range(0, len(names) - 1, 2):
        plt.plot(x[names[i]][1:], x[names[i + 1]][1:], 'o-', label=names[i])
    plt.grid()
    plt.title("T(x)")
    plt.xlabel("log(f), Гц")
    plt.ylabel("tgd")
    plt.legend()
    plt.show()

    for i in range(0, len(names) - 1, 2):
        lis = list(x[names[i + 1]][1:])
        mx = max(lis)
        ind = lis.index(mx)
        print(mx, ind, x[names[i + 1]][ind + 1], x[names[i]][ind + 1])

    return

basa("САФ")
# print(x)
