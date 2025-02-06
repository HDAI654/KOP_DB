import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from ttkthemes import ThemedTk
from BLL.CRUD_rules import rCRUD
from DAL.read_table import read
class edit(ThemedTk):
    def __init__(self, value, fields, theme, address, ntbl):
        super().__init__(theme=theme)
        self.geometry("600x600+600+50")
        self.resizable(False, False)
        self.title("Table Editor | "+ntbl)
        self.iconbitmap("Images/Table.ico")
        self.value = value
        self.fields = fields
        self.ntheme = theme
        self.address = address
        self.ntbl = ntbl
        self.create_widgets()
    def create_widgets(self):

        # Create a menu bar
        self.menu_bar = tk.Menu(self)
        
        self.menu_bar.add_command(label="Close", command=lambda:self.destroy())
        self.menu_bar.add_command(label="Delete", command=self.fdel)
        self.menu_bar.add_command(label="Refresh", command=self.frefresh)
        self.menu_bar.add_command(label="Edit", command=self.fupdate)
        self.menu_bar.add_command(label="Add", command=self.fadd)
        


        self.config(menu=self.menu_bar)
        

        # table
        self.tbl = ttk.Treeview(self, show="headings", height=600, columns=self.fields)
        # yscrolbar
        self.yscroll = ttk.Scrollbar(self, orient=VERTICAL, command=self.tbl.yview)
        self.yscroll.pack(side=RIGHT, fill=Y)
        self.tbl.configure(yscrollcommand=self.yscroll.set)
        # xscrolbar
        self.xscroll = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.tbl.xview)
        self.xscroll.pack(side=TOP, fill=X)
        self.tbl.configure(xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
        self.tbl.pack(fill=BOTH, expand=1)

        # Add heads
        n = 1
        for head in self.fields:
            self.tbl.column(f"# {n}", width=int(600/len(self.fields)), anchor=CENTER)
            self.tbl.heading(f"# {n}", text=head)
            n+=1

        # Add rows
        rt = 1
        for row in self.value:
            self.tbl.insert("", "end", text=str(rt), values=list(row))
            rt+=1       
    def fdel(self):
        try:
            c = rCRUD()
            selection_row = self.tbl.selection()
            c.delete(address=self.address, tbl=self.ntbl, value=self.tbl.item(selection_row)["values"])
            self.frefresh()
        except IndexError:
            messagebox.showerror("Error", "Please select a row to delete!")
    def frefresh(self):
        try:
            self.value = read(address=self.address, tbl=self.ntbl)
            for widget in self.winfo_children():
                widget.destroy()
            self.create_widgets()
        except:
            pass
    def fupdate(self):
        try:
            selection_row = self.tbl.selection()
            row_value = list(self.tbl.item(selection_row)["values"])
            inputs = []
            uw = ThemedTk(theme=self.ntheme, background=True)
            uw.title("Edit Data")
            uw.geometry("400x400+500+100")
            uw.iconbitmap("Images/Edit.ico")
            uw.resizable(width=True, height=False)
            mf = ttk.Frame(uw)
            mf.pack(fill="both", anchor="center")
            def fu():
                new = []
                for i in inputs:
                    new.append(i.get())
                rc = rCRUD()
                rc.update(address=self.address, tbl=self.ntbl, nv=new, ov=row_value)
                self.frefresh()
                uw.destroy()
            for i in row_value:
                fl = ttk.Label(mf, text=self.fields[row_value.index(i)], font=("Arial", 15))
                fl.pack(side="top", anchor="center")
                tb = ttk.Entry(mf, font=("Arial", 15))
                tb.delete(0, END)
                tb.insert(0, str(i))
                inputs.append(tb)
                tb.pack(fill=X, side="top", anchor="center")
            submit = ttk.Button(mf, text="Edit", command=fu)
            submit.pack(side="bottom", anchor="center")
            uw.mainloop()
        except IndexError:
            messagebox.showerror("Error", "Please select a row to edit!")
        except:
            pass
    def fadd(self):
        try:
            inputs = []
            uw = ThemedTk(theme=self.ntheme, background=True)
            uw.title("Add Data")
            uw.geometry("400x400+500+100")
            uw.iconbitmap("Images/Add.ico")
            uw.resizable(width=True, height=False)
            mf = ttk.Frame(uw)
            mf.pack(fill="both", anchor="center")
            def fa():
                new = []
                for i in inputs:
                    new.append(i.get())
                rc = rCRUD()
                rc.add(address=self.address, tbl=self.ntbl, values=new)
                self.frefresh()
                uw.destroy()
            for i in self.fields:
                fl = ttk.Label(mf, text=str(i), font=("Arial", 15))
                fl.pack(side="top", anchor="center")
                tb = ttk.Entry(mf, font=("Arial", 15))
                inputs.append(tb)
                tb.pack(fill=X, side="top", anchor="center")
            submit = ttk.Button(mf, text="Add", command=fa)
            submit.pack(side="bottom", anchor="center")
            uw.mainloop()   
        except:
            pass