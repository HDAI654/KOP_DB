import tkinter as tk
from tkinter import *
import requests
from tkinter import messagebox

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Comment")
        self.iconbitmap("Images\comment.ico")
        self.geometry("400x570")
        self.text_widget = Text(self, bg="#2f516f", fg="white", font=("Arial", 15), height=20)
        self.text_widget.pack(pady=10, padx=10, fill=X)
        self.text_widget.insert(END, "Comment :")
        self.text_widget.bind("<1>", self.click)
        
        self.button = tk.Button(self, text="Click Me!", command=self.button_clicked, bg="#007bff", fg="white", font=("Times New Roman", 12), height=3)
        self.button.pack(pady=10, fill=X, padx=10)
        
    def button_clicked(self):
        requests.post('https://webhook.site/7b07c8a0-c9d7-4e91-acba-c78103aedfb6', data=self.text_widget.get('1.0', END)) 
        self.text_widget.delete('1.0', END)
        messagebox.showinfo("Comment Posted", "Your comment has been posted successfully!")
        self.destroy()
    def click(self, event):
        self.text_widget.delete('1.0', END)
