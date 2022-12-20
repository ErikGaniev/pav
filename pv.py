import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

loc = 'PAV.xlsx'


def graph(q, str_name):
    plt.figure()
    for i in range(0, len(str_name) - 1, 2):
        plt.plot(q[str_name[i]][1:], q[str_name[i + 1]][1:], 'o-', label=str_name[i])
    plt.grid()
    plt.title("T(x)")
    plt.xlabel("log(f), Гц")
    plt.ylabel("tgd")
    plt.legend()
    plt.show()


def basa(s):
    x = pd.read_excel(loc, sheet_name=s)
    x.columns
    x['Unnamed: 1'][1:]
    names = x.columns.tolist()
    # print(names)

    #graph(x, names)

    max_array = []
    for i in range(0, len(names) - 1, 2):
        lis = list(x[names[i + 1]][1:])
        mx = max(lis)
        ind = lis.index(mx)
        max_array.append([names[i], mx, ind, x[names[i + 1]][ind + 1], x[names[i]][ind + 1]])
    # print(max_array)

    return max_array


array_sav = basa("САФ")
print(array_sav)

array_oil = basa("Нефти_нов")
print(array_oil)
