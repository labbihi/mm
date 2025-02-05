import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os
import re

from entities import equipment, category
#from Sport_Equipment_Manager import *
from main import *

class LoginWindow:
        def __init__(self, master):
            

            # Define colors and styles
            self.bg_color = "#f0f0f0"
            self.title_color = "#4a7a8c"
            self.button_color = "#558C8C"
            self.button_text_color = "#ffffff"
            self.frame_color = "#d9d9d9"
            self.font = ("Helvetica", 12)


            self.master = master
            self.master.title("Login")
            self.master.geometry("700x400")
            self.master.configure(bg=self.bg_color)

            
            self.master.grid_rowconfigure(0, weight=1)
            self.master.grid_rowconfigure(1, weight=1)
            self.master.grid_rowconfigure(2, weight=1)
            self.master.grid_columnconfigure(0, weight=1)
            self.master.grid_columnconfigure(1, weight=1)


           
            self.logo = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "logo.png"))
            self.logo = self.logo.subsample(20, 20)  # Adjust the subsample values to resize the image
            self.logo_label = tk.Label(master, image=self.logo, bg="#f0f0f0")
            self.logo_label.grid(row=0, column=0, columnspan=2, pady=10)

            self.title_label = tk.Label(master, text="Material Manager", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
            self.title_label.grid(row=1, column=0, columnspan=2, pady=10)



            self.username_label = tk.Label(master, text="Username:", font=("Helvetica", 12))
            self.username_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
            self.username_entry = tk.Entry(master, font=("Helvetica", 12))
            self.username_entry.grid(row=2, column=1, padx=20, pady=10)

            self.password_label = tk.Label(master, text="Password:", font=("Helvetica", 12))
            self.password_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
            self.password_entry = tk.Entry(master, show="*", font=("Helvetica", 12))
            self.password_entry.grid(row=3, column=1, padx=20, pady=10)

            self.login_button = tk.Button(master, text="Login", command=self.check_login, bg="#558C8C", fg="#ffffff", font=("Helvetica", 16))
            self.login_button.grid(row=4, columnspan=2, pady=20, padx=20)

            self.footer_label = tk.Label(master, text="Lycée Qualifiant AL IRFANE - DR TAROUDANT- ARFE SOUSS MASSA-  copyright © 2025", font=self.font, bg=self.title_color, fg=self.button_text_color)
            self.footer_label.grid(row=5, columnspan=2, pady=20, padx=20)

        def check_login(self):
            username = self.username_entry.get()
            password = self.password_entry.get()
            if username == "admin" and password == "admin":  # Simple check for demonstration
                self.master.destroy()
                #root = tk.Tk()
                app = Application()
                root.mainloop()
            else:
                messagebox.showerror("Error", "Invalid username or password")

if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginWindow(root)
    root.mainloop()