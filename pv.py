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
    part_array = []
    for i in range(0, len(names) - 1, 2):
        lis = list(x[names[i + 1]][1:])
        mx = max(lis)
        ind = lis.index(mx)
        max_array.append([names[i], mx, ind, x[names[i + 1]][ind + 1], x[names[i]][ind + 1]])
        names_out.append(names[i])
        w1 = np.zeros_like(lis)
        w2 = np.zeros_like(lis)
        w1[0:ind] = lis[0:ind]
        w2[ind:] = lis[ind:]
        # print(w2)
        w1 = sorted(enumerate(w1), key=lambda p: abs(p[1] - mx * tgd))
        w2 = sorted(enumerate(w2), key=lambda p: abs(p[1] - mx * tgd))
        part_array.append([w1[0][1], x[names[i]][w1[0][0] + 1], w2[0][1], x[names[i]][w2[0][0] + 1]])

    return x, names_out, max_array, part_array


label_pav = "САТ"
label_oil = "Нефти_нов"
xsav, name_sav, array_sav, part_sav = basa(label_pav)
lsav = len(array_sav)
# print(array_sav)
print(name_sav)
# print(lsav)

xoil, name_oil, array_oil, part_oil = basa(label_oil)
loil = len(array_oil)
# print(xoil["Арланское скв.456"].to_string())
# print(array_oil)
print(part_oil)
# print(part_oil[0][0])

# graph(xoil, xoil.columns.tolist())
df1 = np.zeros((lsav, loil))
df1 = pd.DataFrame(df1, index=name_sav, columns=name_oil)

for i in range(len(array_sav)):
    for j in range(len(array_oil)):
        df1[name_oil[j]][name_sav[i]] = np.fabs(array_oil[j][4] - array_sav[i][4])

print(df1)

df2 = np.zeros((lsav, loil))
df2 = pd.DataFrame(df2, index=name_sav, columns=name_oil)

for i in range(len(array_sav)):
    for j in range(len(array_oil)):
        if part_oil[j][3] <= array_sav[i][4] <= part_oil[j][1]:
            df2[name_oil[j]][name_sav[i]] = 1
        else:
            df2[name_oil[j]][name_sav[i]] = 0
print(df2.to_string())

df3 = np.zeros((lsav, loil))
df3 = pd.DataFrame(df3, index=name_sav, columns=name_oil)

print(part_sav[1][3], part_sav[1][1])
for i in range(len(array_sav)):
    for j in range(len(array_oil)):
        if part_oil[j][3] <= part_sav[i][3] <= part_oil[j][1] or part_sav[i][3] <= part_oil[j][3] <= part_sav[i][1]:
            df3[name_oil[j]][name_sav[i]] = 1
        else:
            df3[name_oil[j]][name_sav[i]] = 0
print(df3)

with pd.ExcelWriter(label_pav + '.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Sheet_name_1')
    df2.to_excel(writer, sheet_name='Sheet_name_2')
    df3.to_excel(writer, sheet_name='Sheet_name_3')
