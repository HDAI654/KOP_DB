import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import sqlite3
from tkinter import messagebox
from .comment import App
from DAL.read_table import read
from .editor_form import edit
from DAL.repository import CRUD
class Application(Frame):
    def __init__(self, screen, the):
        super().__init__(screen)
        self.my_theme = the
        self.master = screen
        self.pack()
        self.create_widgets()
    def read_data(self, addres):
        self.name = addres.split("/")[-1]
        self.data={f"{self.name}":{"names":[], "data":{}}}
        try:
            conn = sqlite3.connect(addres)
            cursor = conn.cursor()
        except:
            pass

        try:
            Tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        except:
            pass

        for i in Tables:
            tname = str(i[0])
            self.data[self.name]["names"].append(tname)
            try:
                info = list(cursor.execute(f"SELECT * FROM {self.data[self.name]['names'][-1]};").fetchall())
            except:
                pass
            self.data[self.name]["data"][tname] = info        
        self.create_tab(name=self.name)
        conn.commit()
        cursor.close()
        conn.close()
    def open_file(self):
        try:
            file = filedialog.askopenfile(mode="r", filetypes=[("DataBase Files", "*.db"), ("All Files", "*.*")])
            self.address = file.name
            self.master.title("DataBase Viewer | "+self.address)
            self.read_data(addres=file.name)
        except:
            pass
    def create_widgets(self):
    
         # Create a menu bar
        self.menu_bar = tk.Menu(self.master)
        
        # Create a pull-down menu and add it to the menu bar
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_separator()
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)



        self.menu_bar.add_command(label="Comment", command=self.comment_window)
        self.menu_bar.add_command(label="Exit", command=lambda:self.master.destroy())
        self.menu_bar.add_command(label="Change Theme", command=self.change_theme)
        self.menu_bar.add_command(label="Close", command=self.fclose)
        self.menu_bar.add_command(label="Refresh", command=self.frefresh)
        self.menu_bar.add_command(label="Edit", command=self.fedit)


        self.master.config(menu=self.menu_bar)

        ##make a notebook
        self.notebook=ttk.Notebook(self.master, width=600, height=600)
        self.notebook.pack()
    def change_theme(self):
        self.theme_window = Toplevel(self.master)
        self.theme_window.overrideredirect(True)
        self.theme_window.title("Change Theme")
        self.theme_window.geometry("300x300+200+200")

        #Add combobox for ThemedTk themes
        self.combobox = ttk.Combobox(self.theme_window, values=["smog", "equilux", "arc", "adapta", "black", "blue", "clearlooks", "elegance", "kroc", "radiance", "ubuntu", "yaru", "plastik", "keramik"], show="Themes List")
        self.combobox.pack(side=TOP, anchor=CENTER)
        # Button
        self.button = ttk.Button(self.theme_window, text="Apply", command=self.apply_theme)
        self.button.pack(side=BOTTOM, anchor=CENTER)
    def apply_theme(self):
        try:
            self.my_theme = self.combobox.get()
            self.master.set_theme(self.combobox.get())
            self.combobox.destroy()
            self.button.destroy()
            self.theme_window.destroy()
        except:
            pass
    def create_tab(self, name):
        try:
            conn = sqlite3.connect(self.address)
            cursor = conn.cursor()
            for i in self.master.winfo_children():
                i.destroy()
            self.create_widgets()
            # Create tab frame
            for item in self.data[name]["names"]:
                
                page = Frame(self.notebook)
                cursor.execute(f"SELECT * FROM {item}")
                names = [description[0] for description in cursor.description]
                tbl = ttk.Treeview(page, show="headings", height=600, columns=names)
                # yscrolbar
                yscroll = ttk.Scrollbar(page, orient=VERTICAL, command=tbl.yview)
                yscroll.pack(side=RIGHT, fill=Y)
                tbl.configure(yscrollcommand=yscroll.set)
                # xscrolbar
                xscroll = ttk.Scrollbar(page, orient=HORIZONTAL, command=tbl.xview)
                xscroll.pack(side=TOP, fill=X)
                tbl.configure(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
                tbl.pack(fill=BOTH, expand=1)
                
                # Add heads
                n = 1
                for fn in names:
                    tbl.column(f"# {n}", width=int(600/len(names)), anchor=CENTER)
                    tbl.heading(f"# {n}", text=fn)
                    n+=1
                
                # Add rows
                rt = 1
                for row in self.data[name]["data"][item]:
                    tbl.insert("", "end", text=str(rt), values=list(row))
                    rt+=1
                tbl.pack(padx=2, pady=2)
                self.notebook.add(page, text=item)

            conn.commit()
            cursor.close()
            conn.close()
        except:
            messagebox.showerror("Error", "I can't open your file")
    def comment_window(self):
        page = App()
        page.mainloop()
    def fedit(self):
        selected_tab_index = self.notebook.select()
        tbl = str(self.notebook.tab(selected_tab_index, "text"))
        crud = CRUD()
        win = edit(value=read(self.address, tbl=tbl), fields=crud.get_fields(address=self.address, tbl=tbl), theme=self.my_theme, address=self.address, ntbl=tbl)
        win.mainloop()        
    def fclose(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.create_widgets()
    def frefresh(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.create_widgets()
        self.read_data(self.address)