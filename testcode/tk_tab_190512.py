import tkinter as tk
import tkinter.ttk as ttk


def press_button1():
    label1["text"] = "pressed button1"


def press_button2():
    label2["text"] = "pressed button2"


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x150")
    root.title("Notebook")

    # 1. Notebookオブジェクトを作成
    notebook = ttk.Notebook(root)

    # 2. タブとなるフレームを作成
    tab1 = tk.Frame(notebook)
    tab2 = tk.Frame(notebook)

    # 3. Notebookにタブを追加
    notebook.add(tab1, text="tab1")
    notebook.add(tab2, text="tab2")

    # ウィンドウサイズが変わった時用にタブのレスポンシブを有効化
    notebook.pack(expand=True, fill="both")

    # tabをマスターとしたウィジェット
    label1 = tk.Label(tab1, text="tab1 label1")
    button1 = tk.Button(tab1, text="tab1 button1", command=press_button1)

    label2 = tk.Label(tab2, text="tab1 label2")
    button2 = tk.Button(tab2, text="tab1 button2", command=press_button1)

    [widget.pack(pady=10) for widget in (label1, button1, label2, button2)]

    root.mainloop()