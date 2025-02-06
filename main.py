import tkinter as tk
from PL.main_form import Application
from ttkthemes import ThemedTk
from tkinter import ttk


if __name__ == "__main__":
    root = ThemedTk(theme="black")
    root.title("DataBase Viewer")
    root.iconbitmap("Images\database.ico")
    page = Application(root, the="black")
    root.resizable(False, False)
    root.mainloop()
    