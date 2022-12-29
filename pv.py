import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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


def basa(loc_func, s):
    x = pd.read_excel(loc_func, sheet_name=s)
    names = x.columns.tolist()
    # print(names)

    # graph(x, names)
    tgd = 0.7
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


def main():
    # loc = input("Введите директорию exel таблицы: ")
    loc = 'PAV.xlsx'
    # tgd = 0.7

    # label_pav = input("Введите название страницы пава: ")
    label_pav = "САТ"

    # label_oil = input("Введите название страницы нефти: ")
    label_oil = "Нефти_нов"

    tgd = 0.7
    # label_names = ["САФ", "САТ", "Сульфанор Б2", "АОС", "Составы"]

    xsav, name_sav, array_sav, part_sav = basa(loc, label_pav)
    lsav = len(array_sav)
    # print(array_sav)
    # print(name_sav)
    # print(lsav)

    xoil, name_oil, array_oil, part_oil = basa(loc, label_oil)
    loil = len(array_oil)
    # print(xoil["Арланское скв.456"].to_string())
    # print(array_oil)
    # print(part_oil)
    # print(part_oil[0][0])

    # graph(xoil, xoil.columns.tolist())
    df1 = np.zeros((lsav, loil))
    df1 = pd.DataFrame(df1, index=name_sav, columns=name_oil)

    for i in range(len(array_sav)):
        for j in range(len(array_oil)):
            df1[name_oil[j]][name_sav[i]] = np.fabs(array_oil[j][4] - array_sav[i][4])

    # print(df1)

    df2 = np.zeros((lsav, loil))
    df2 = pd.DataFrame(df2, index=name_sav, columns=name_oil)

    for i in range(len(array_sav)):
        for j in range(len(array_oil)):
            if part_oil[j][3] <= array_sav[i][4] <= part_oil[j][1]:
                df2[name_oil[j]][name_sav[i]] = 1
            else:
                df2[name_oil[j]][name_sav[i]] = 0
    # print(df2.to_string())

    # Сохраните объект тепловой карты в переменной, чтобы легко получить к нему доступ,
    # когда вы захотите включить дополнительные функции (например, отображение заголовка).
    # Задайте диапазон значений для отображения на цветовой карте от -1 до 1 и установите для аннотации (annot) значение True,
    # чтобы отобразить числовые значения корреляции на тепловой карте.

    plt.figure(figsize=(16, 6))
    heatmap = sns.heatmap(df2, annot=True, cmap='crest', cbar=False)
    heatmap.set_title(label_pav + " проверка эфективно по 2 методу", fontdict={'fontsize': 12}, pad=12)
    heatmap.xaxis.tick_top()
    plt.show()

    # print(df2)

    df3 = np.zeros((lsav, loil))
    df3 = pd.DataFrame(df3, index=name_sav, columns=name_oil)

    # print(part_sav[1][3], part_sav[1][1])
    for i in range(len(array_sav)):
        for j in range(len(array_oil)):
            if part_oil[j][3] <= part_sav[i][3] <= part_oil[j][1] or part_sav[i][3] <= part_oil[j][3] <= part_sav[i][1]:
                df3[name_oil[j]][name_sav[i]] = 1
            else:
                df3[name_oil[j]][name_sav[i]] = 0
    # print(df3)

    with pd.ExcelWriter(label_pav + '.xlsx') as writer:
        df1.to_excel(writer, sheet_name='Sheet_name_1')
        df2.to_excel(writer, sheet_name='Sheet_name_2')
        df3.to_excel(writer, sheet_name='Sheet_name_3')


if __name__ == '__main__':
    main()
