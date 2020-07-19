import datetime
import os
from os import path
import sys

from datetime import datetime , timedelta
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import pandas as pd
import functools

from fileoperation_package.common import fileoperation_csv_v1_2

list_todo = []
list_done = []

def copy_listitem():
    # 選択中アイテムのインデックス
    tuple = listbox_todo.curselection()
    for i in tuple:
        list_done.append(list_todo[i])
    strvar_done.set(list_done)

def delete_listitem():
    tuple = listbox_todo.curselection()
    delete_list = []
    # 削除する項目をlistへまとめている
    for i in tuple:
        delete_list.append(list_todo[i])
    # 削除する項目からlistの要素を削除
    for i in range(len(delete_list)):
        list_todo.remove(delete_list[i])
    strvar_todo.set(list_todo)

def delete_donelistitem():
    tuple = listbox_done.curselection()
    delete_list = []
    # 削除する項目をlistへまとめている
    for i in tuple:
        delete_list.append(list_done[i])
    # 削除する項目からlistの要素を削除
    for i in range(len(delete_list)):
        list_done.remove(delete_list[i])
    strvar_done.set(list_done)

def pop_listitem():
    # 選択中アイテムのインデックス

    tuple = listbox_todo.curselection()
    delete_list = []
    # 削除する項目をlistへまとめている
    for i in tuple:
        list_done.append(list_todo[i])
        delete_list.append(list_todo[i])
    # 削除する項目からlistの要素を削除
    for i in range(len(delete_list)):
        list_todo.remove(delete_list[i])
    strvar_todo.set(list_todo)
    strvar_done.set(list_done)

def insertpop_listitem():
    # donelistの選択項へ、"_○○"の文字列を追加して、todolist項は削除
    #[1] todolistの選択項の取得(なければ終了)
    if listbox_todo.curselection():
        select_tuple = listbox_todo.curselection()
    # 選択項が複数の場合有るので、初めのものだけ取得
    for i in select_tuple:
        select_term_todo = list_todo[i]
        select_index_todo = i
        break

    # donelistの最後の項に追加
    list_done[-1] = list_done[-1] + "_" + list_todo[select_index_todo]
    del list_todo[select_index_todo]

    # GUI上のlistの更新,GUIの選択位置を変える
    strvar_todo.set(list_todo)
    strvar_done.set(list_done)

def insert_listitem():
    # donelistの選択項へ、"_○○"の文字列を追加
    #[1] todolistの選択項の取得(なければ終了)
    if listbox_todo.curselection():
        select_tuple = listbox_todo.curselection()
    # 選択項が複数の場合有るので、初めのものだけ取得
    for i in select_tuple:
        select_term_todo = list_todo[i]
        select_index_todo = i
        break

    # donelistの最後の項に追加
    list_done[-1] = list_done[-1] + "_" + list_todo[select_index_todo]

    # GUI上のlistの更新,GUIの選択位置を変える
    strvar_todo.set(list_todo)
    strvar_done.set(list_done)


def add_todolist():
    # todolistへ、テキストボックスの文字列を追加

    # if 文字列で空白とnull以外を処理
    # そこに、strip()でスペース除去して、スペースだけも追加しない様に配慮
    if en_todo.get().strip():
        list_todo.append(en_todo.get())
        strvar_todo.set(list_todo)

    # GUI上のtodolistの更新,GUIの選択位置を変える
    strvar_todo.set(list_todo)
    listbox_todo.selection_clear(0, len(list_todo))
    listbox_todo.select_set(len(list_todo)-1)

def read_listitem_from_csv():
    # csvからlistを読み取り、todolistへ追加
    df = fileoperation_csv_v1_2.transform_csv_to_df()
    df_todolist = df.iloc[:, 0]
    df_todolist = df_todolist.dropna()
    list_todo = df_todolist.values.tolist()

    # GUI上のtodolistの更新
    strvar_todo.set(list_todo)

def move_upward():
    # todolistの選択項目を上に移動
    # 選択項の取得(なければ終了)
    if listbox_todo.curselection():
        select_tuple = listbox_todo.curselection()
    # 選択項が複数の場合有るので、初めのものだけ取得
    for i in select_tuple:

        # 一番上(i==0なら処理終了)
        if i == 0:
            return

        select_term = list_todo[i]
        select_index = i
        break

    # 選択項を削除して、一つ上のindexへ追加
    del list_todo[select_index]
    list_todo.insert(select_index - 1, select_term)

    # GUI上のtodolistの更新,GUIの選択位置を変える
    strvar_todo.set(list_todo)
    listbox_todo.selection_clear(0, len(list_todo))
    listbox_todo.select_set(select_index - 1)

def move_downward():
    # todolistの選択項目を下に移動
    # 選択項の取得(なければ終了)
    if listbox_todo.curselection():
        select_tuple = listbox_todo.curselection()

    # 選択項が複数の場合有るので、初めのものだけ取得
    for i in select_tuple:

        # 一番下なら処理終了
        if i == len(list_todo) + 1:
            return

        select_term = list_todo[i]
        select_index = i
        break

    # 選択項を削除して、一つ上のindexへ追加
    del list_todo[select_index]
    list_todo.insert(select_index + 1, select_term)

    # GUI上のtodolistの更新,GUIの選択位置を変える
    strvar_todo.set(list_todo)
    listbox_todo.selection_clear(0, len(list_todo))
    listbox_todo.select_set(select_index + 1)

def add_current_time():
    for en in en_list:
        val_en = en.get()
        #テキストボックスが空の場合に、時刻を入力する
        if not val_en:
            en.delete(0, tk.END)
            current_time = datetime.now().strftime("%H:%M")
            en.insert(0, current_time)
            break




def output_accoundability_chart():
    # todolist, donelist, 時刻をdfにして、本日の日付名のcsvファイルとして出力

    # 日付をlistへ格納
    list_en_start = []
    list_en_end = []
    i = 0
    for en in en_list:
        val_en = en.get()

        if i % 2 == 0:
            list_en_start.append(val_en)
        else:
            list_en_end.append(val_en)
        i = i + 1

    # todolist, donelist, 時刻をdfにして結合
    df_todo = pd.DataFrame(list_todo, columns=["todo_list"])
    df_done = pd.DataFrame(list_done, columns=["done_list"])
    df_en_start = pd.DataFrame(list_en_start, columns=["start_time"])
    df_en_end = pd.DataFrame(list_en_end, columns=["end_time"])
    df_todos = [pd.DataFrame(list_todos[i], columns=["todo_list"]) for i in range(5)]

    df_all = pd.concat([df_todo, df_done, df_en_start, df_en_end,
                        df_todos[0], df_todos[1], df_todos[2], df_todos[3], df_todos[4]], axis=1)
    # df_all.replace(np.nan, ' ')
    # df_all.dropna
    print(df_all)

    #　csvファイルへ出力
    if not os.path.isdir('output'):
        os.mkdir('output')

    now = datetime.now()
    curr_day = '{0:%Y%m%d}'.format(now)
    fullpath_output = "output/accounta_{}.csv".format(curr_day)
    fileoperation_csv_v1_2.transform_df_to_csv(df_all, fullpath_output)

def get_df_from_previous_output():
    """本日or前日の結果をcsvファイルから読み取りdfとして返してくれるメソッド

    :return: df
    """
    now = datetime.now()
    today = '{0:%Y%m%d}'.format(now)
    fullpath_today = "output/accounta_{}.csv".format(today)

    yesterday = now - timedelta(days=1)
    yesterday = '{0:%Y%m%d}'.format(yesterday)
    fullpath_yesterday = "output/accounta_{}.csv".format(yesterday)

    if os.path.exists(fullpath_today):
        df = fileoperation_csv_v1_2.transform_spesific_csv_to_df(fullpath_today)
    elif os.path.exists(fullpath_yesterday):
        df = fileoperation_csv_v1_2.transform_spesific_csv_to_df(fullpath_yesterday)
    else:
        df = pd.DataFrame()

    return df

def initialset_todo_list(df):
    """dfから読み取りtodolistを抽出しリストとして返してくれるメソッド

    :param df:
    :return: list_todo
    """
    df_todolist = df.iloc[:, 0]
    df_todolist = df_todolist.dropna()
    list_todo = df_todolist.values.tolist()
    return list_todo

def initialset_done_list(df):
    """dfから読み取りdonelistを抽出しリストとして返してくれるメソッド

    :param df:
    :return: done_todo
    """
    df_donelist = df.iloc[:, 1]
    df_donelist = df_donelist.dropna()
    list_done = df_donelist.values.tolist()
    return list_done

def add_time_from_df(df):
    """csvファイルから読み取ったdfから開始終了時間だけをテキストボックスへ入力

    :return:なし
    """
    # 2列目と3列目を抽出
    df_startendtime = df.iloc[:, 2:4]

    total_count = 0
    i = 0
    for en in en_list:
        # nan含まれていたら終了(文字列で判断するために、一度strで文字列にしている！！)
        if "nan" in str(df_startendtime.iloc[i, 0]):
            break
        elif i >= len(df_startendtime):
            break
        en.delete(0, tk.END)
        if total_count % 2 == 0:
            en.insert(0, df_startendtime.iloc[i, 0])
        else:
            en.insert(0, df_startendtime.iloc[i, 1])
            i = i + 1
        total_count = total_count + 1

#  ------------↓weektab用の関数
def move_upward_w(list_todo, listbox_todo, strvar_todo):
    # todolistの選択項目を上に移動
    # 選択項の取得(なければ終了)
    if listbox_todo.curselection():
        select_tuple = listbox_todo.curselection()
    # 選択項が複数の場合有るので、初めのものだけ取得
    for i in select_tuple:

        # 一番上(i==0なら処理終了)
        if i == 0:
            return

        select_term = list_todo[i]
        select_index = i
        break

    # 選択項を削除して、一つ上のindexへ追加
    del list_todo[select_index]
    list_todo.insert(select_index - 1, select_term)

    # GUI上のtodolistの更新,GUIの選択位置を変える
    strvar_todo.set(list_todo)
    listbox_todo.selection_clear(0, len(list_todo))
    listbox_todo.select_set(select_index - 1)


def move_downward_w(list_todo, listbox_todo, strvar_todo):
    # todolistの選択項目を下に移動
    # 選択項の取得(なければ終了)
    if listbox_todo.curselection():
        select_tuple = listbox_todo.curselection()

    # 選択項が複数の場合有るので、初めのものだけ取得
    for i in select_tuple:

        # 一番下なら処理終了
        if i == len(list_todo) + 1:
            return

        select_term = list_todo[i]
        select_index = i
        break

    # 選択項を削除して、一つ上のindexへ追加
    del list_todo[select_index]
    list_todo.insert(select_index + 1, select_term)

    # GUI上のtodolistの更新,GUIの選択位置を変える
    strvar_todo.set(list_todo)
    listbox_todo.selection_clear(0, len(list_todo))
    listbox_todo.select_set(select_index + 1)


def add_todolist_w(en_todo, list_todo, strvar_todo):
    # todolistへ、テキストボックスの文字列を追加

    # if 文字列で空白とnull以外を処理
    # そこに、strip()でスペース除去して、スペースだけも追加しない様に配慮
    if en_todo.get().strip():
        list_todo.append(en_todo.get())
        strvar_todo.set(list_todo)

    # GUI上のtodolistの更新,GUIの選択位置を変える
    strvar_todo.set(list_todo)
    listbox_todo.selection_clear(0, len(list_todo))
    listbox_todo.select_set(len(list_todo)-1)


def delete_listitem_w(list_todo, listbox_todo, strvar_todo):

    tuple = listbox_todo.curselection()
    delete_list = []
    # 削除する項目をlistへまとめている
    for i in tuple:
        delete_list.append(list_todo[i])
    # 削除する項目からlistの要素を削除
    for i in range(len(delete_list)):
        list_todo.remove(delete_list[i])
    strvar_todo.set(list_todo)


def initialset_todo_list_w(df):
    """dfから読み取りdonelistを抽出しリストとして返してくれるメソッド

    :param df:
    :return: done_todo
    """
    df_new = df.dropna()
    list = df_new.values.tolist()
    return list
# ----------------------↓GUI配置と実行-----------------------------------------------

root = tk.Tk()

root.geometry("800x550")
# root.title(path.splitext(path.basename(__file__))[0])
root.title(path.splitext(path.basename(sys.argv[0]))[0])
# 生成⇒pack⇒place この順番！
# frame_1 = tk.Frame(root, width=300, height=300, background="#fef")
# frame_1.pack()

# 1. Notebookオブジェクトを作成
notebook = ttk.Notebook(root)

# 2. タブとなるフレームを作成
tab_today = tk.Frame(notebook)
tab_week = tk.Frame(notebook)

# 3. Notebookにタブを追加
notebook.add(tab_today, text="本日")
notebook.add(tab_week, text="今週")
# ウィンドウサイズが変わった時用にタブのレスポンシブを有効化
notebook.pack(expand=True, fill="both")

scrollbar = tk.Scrollbar(tab_today)
# sid=tikinter.RiGHT は右位置、fill="y"は縦に一杯という意味
# scrollbar.pack(side=tk.RIGHT, fill="y")



strvar_todo = tk.StringVar()



#--------[本日タスクタブ↓]----------------------------------------------------
# todolistを前回のファイルをもとに復元
df_from_csv = get_df_from_previous_output()
list_todo = initialset_todo_list(df_from_csv)
strvar_todo.set(list_todo)
strvar_done = tk.StringVar()


# widegetの宣言(テキストのリスト以外) マスターはtab_today
lbl_todolist = tk.Label(tab_today, text='Todo_list')
lbl_donelist = tk.Label(tab_today, text='Done_list')
lbl_start = tk.Label(tab_today, text='start')
lbl_end = tk.Label(tab_today, text='end')
listbox_todo = tk.Listbox(tab_today,  listvariable=strvar_todo, selectmode="single", height=10)
listbox_done = tk.Listbox(tab_today,  listvariable=strvar_done, selectmode="single", height=10)
button_copy = tk.Button(tab_today,  text="Copy⇒", command=copy_listitem)
button_pop = tk.Button(tab_today,  text=" Pop⇒", command=pop_listitem,
                       bg='pale violet red', fg='snow')
button_insert_pop = tk.Button(tab_today,  text=" Insert⇒\n(pop)", font=("", 9), command=insertpop_listitem,
                              bg='pale violet red', fg='snow')
button_insert = tk.Button(tab_today,  text=" Insert⇒", command=insert_listitem)
button_delete = tk.Button(tab_today,  text="DEL", command=delete_listitem)
button_read = tk.Button(tab_today,  text="Read_from_csv", command=read_listitem_from_csv)
button_add = tk.Button(tab_today,  text="Add↑", command=add_todolist)
button_upward = tk.Button(tab_today,  text="↑", command=move_upward)
button_downward = tk.Button(tab_today,  text="↓", command=move_downward)
button_time = tk.Button(tab_today, text="Now↑", command=add_current_time,
                        bg='navy', fg='snow')
button_delete_done = tk.Button(tab_today,  text="DEL", command=delete_donelistitem)
button_output = tk.Button(tab_today, text="Output_to csv", command=output_accoundability_chart,
                          bg='orange', fg='snow', font=("", 12))
en_todo = tk.Entry(master=tab_today)

# スクロールバーをtodolistと連動させる
listbox_todo["yscrollcommand"] = scrollbar.set
scrollbar["command"] = listbox_todo.yview
default_index = 14
listbox_todo.select_set(default_index)
listbox_todo.see(default_index)
listbox_todo.pack()

#テキストボックスの宣言(まとめて)
en_list = [tk.Entry(master=tab_today) for _ in range(0, 36)]


# まとめてパッキング！(分けても良いが)
[widget.pack() for widget in (lbl_todolist, lbl_donelist, lbl_start, lbl_end, listbox_todo, listbox_done,
                              button_copy, button_pop, button_delete, scrollbar, en_todo, button_delete_done)]
[en.pack() for en in en_list]

# (本日の日付のファイルがある場合)テキストボックスとdonelistを前回のファイルを基に復元
now = datetime.now()
today = '{0:%Y%m%d}'.format(now)
fullpath_today = "output/accounta_{}.csv".format(today)

if os.path.exists(fullpath_today):
    add_time_from_df(df_from_csv)

    list_done = initialset_done_list(df_from_csv)
    strvar_done.set(list_done)


# 場所決め 何だかんだ、placeで直接やった方が柔軟で良い感じ

x_list = 100
lbl_todolist.place(x=x_list+10, y=50, width=200, height=50)
lbl_donelist.place(x=x_list+330, y=50, width=200, height=50)
lbl_start.place(x=x_list+540, y=75, width=25, height=25)
lbl_end.place(x=x_list+590, y=75, width=25, height=25)
listbox_todo.place(x=x_list, y=100, width=200, height=300)
scrollbar.place(x=x_list+220, y=100, width=15, height=300)
listbox_done.place(x=x_list+325, y=100, width=200, height=300)
button_upward.place(x=x_list-50, y=200, width=25, height=25)
button_downward.place(x=x_list-50, y=230, width=25, height=25)
button_read.place(x=x_list, y=425, width=100, height=25)
button_add.place(x=x_list+110, y=415, width=50, height=40)
button_delete.place(x=x_list+175, y=425, width=50, height=25)
en_todo.place(x=x_list+10, y=475, width=200, height=30)
y_pop = 135
button_pop.place(x=x_list+250, y=y_pop, width=50, height=50)
button_copy.place(x=x_list+250, y=y_pop+65, width=50, height=50)
button_insert_pop.place(x=x_list+250, y=y_pop+130, width=50, height=50)
button_insert.place(x=x_list+250, y=y_pop+195, width=50, height=50)
button_time.place(x=x_list+555, y=420, width=50, height=30)
button_delete_done.place(x=x_list+400,  y=425, width=50, height=25)
button_output.place(x=x_list+530, y=470, width=100, height=30)

y_height = 16.25
y_en = 99 - y_height
for i in range(0, len(en_list)):

    if i % 2 == 0:
        y_en = y_en + y_height
        x_en = x_list + 530
    else:
        x_en = x_list + 530 + 55
    print(i, x_en, y_en)
    en_list[i].place(x=x_en, y=y_en, width=50, height=y_height)


#  --------[週タスクタブ↓]----------------------------------------------------

# リスト内包表記でまとめて宣言
# todolistを前回のファイルをもとに復元
dfs_from_csv = df_from_csv.iloc[:, 4:]
# df_from_csvs = [pd.DataFrame(np.random.randn(5, 1)) for _ in range(5)]
print(dfs_from_csv.iloc[:, 0])
list_todos = [initialset_todo_list_w(dfs_from_csv.iloc[:, i]) for i in range(5)]
strvar_todos = [tk.StringVar() for _ in range(5)]
[strvar_todos[i].set(list_todos[i]) for i in range(5)]

week_strs = ['月', '火', '水', '木', '金']
lblw_todolists = [tk.Label(tab_week, text=week_strs[i]) for i in range(5)]
listbox_todos = [tk.Listbox(tab_week,  listvariable=strvar_todos[i], selectmode="single", height=10) for i in range(5)]
en_todo_w = tk.Entry(master=tab_week)

# 引数あるコマンド
button_upwards = [tk.Button(tab_week,  text="↑",
                            command=functools.partial(move_upward_w,
                                                      list_todo=list_todos[i], listbox_todo=listbox_todos[i],
                                                      strvar_todo=strvar_todos[i])) for i in range(5)]
button_downwards = [tk.Button(tab_week,  text="↓",
                              command=functools.partial(move_downward_w,
                                                        list_todo=list_todos[i],
                                                        listbox_todo=listbox_todos[i],
                                                        strvar_todo=strvar_todos[i])) for i in range(5)]

button_adds = [tk.Button(tab_week,  text="↑",
                         command=functools.partial(add_todolist_w,
                                                   en_todo=en_todo_w,
                                                   list_todo=list_todos[i],
                                                   strvar_todo=strvar_todos[i])) for i in range(5)]

button_deletes = [tk.Button(tab_week,  text="DEL",
                            command=functools.partial(delete_listitem_w,
                                                      list_todo=list_todos[i],
                                                      listbox_todo=listbox_todos[i],
                                                      strvar_todo=strvar_todos[i])) for i in range(5)]
# パッキング！
# [lblw_todolist.pack() for lblw_todolist in lblw_todolists]
# [listbox_todo.pack() for listbox_todo in listbox_todos]
# [button_upward.pack() for button_upward in button_upwards]

# 配置決め
[lblw_todolists[i].place(x=25 + i * 150, y=50, width=125, height=50) for i in range(5)]
[listbox_todos[i].place(x=25 + i * 150, y=100, width=125, height=200) for i in range(5)]
[button_upwards[i].place(x=0 + i * 150, y=150, width=25, height=25) for i in range(5)]
[button_downwards[i].place(x=0 + i * 150, y=175, width=25, height=25) for i in range(5)]
[button_adds[i].place(x=50 + i * 150, y=315, width=25, height=25) for i in range(5)]
[button_deletes[i].place(x=80 + i * 150, y=315, width=25, height=25) for i in range(5)]
en_todo_w.place(x=300, y=375, width=200, height=30)

root.mainloop()