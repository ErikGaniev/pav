import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

loc = 'PAV.xlsx'
tgd = 0.7


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
    names = x.columns.tolist()
    # print(names)

    # graph(x, names)

    max_array = []
    names_out = []
    for i in range(0, len(names) - 1, 2):
        lis = list(x[names[i + 1]][1:])
        mx = max(lis)
        ind = lis.index(mx)
        max_array.append([names[i], mx, ind, x[names[i + 1]][ind + 1], x[names[i]][ind + 1]])
        names_out.append(names[i])
        # print(max_array)

    return x, names_out, max_array


xsav, name_sav, array_sav = basa("САФ")
lsav = len(array_sav)
# print(array_sav)
print(name_sav)
print(lsav)

xoil, name_oil, array_oil = basa("Нефти_нов")
loil = len(array_oil)
print(array_oil)

df = np.zeros((lsav, loil))
# print(df)
df = pd.DataFrame(df, index=name_sav, columns=name_oil)

# print(df)

# print(df[name_oil[0]][name_sav[0]])

for i in range(len(array_sav)):
    for j in range(len(array_oil)):
        df[name_oil[j]][name_sav[i]] = np.fabs(array_oil[j][4] - array_sav[i][4])

print(df)
