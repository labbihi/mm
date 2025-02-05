import tkinter as tk
import matplotlib.pyplot as plt

from statistiques2 import show_statistiques

from equipment_manager2 import *

from categories import *



class Application(tk.Tk):
    def __init__(self):
        super().__init__()

    

        # Définir les couleurs et styles
        self.bg_color = "#f0f0f0"
        self.title_color = "#4a7a8c"
        self.button_color = "#558C8C"
        self.button_text_color = "#ffffff"
        self.frame_color = "#d9d9d9"
        self.font = ("Helvetica", 12)

        self.title("Material Manager")
        self.geometry("800x600")
        self.configure(bg=self.bg_color)

        # Configurer les colonnes et les lignes pour être responsive
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)  # Header
        self.grid_rowconfigure(1, weight=4)  # Menu Principal
        self.grid_rowconfigure(2, weight=5)  # Content
        self.grid_rowconfigure(3, weight=1)  # Footer
        
        # Frame Header
        self.header_frame = tk.Frame(self, bg=self.title_color, height=50)
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="ew")

        self.header_label = tk.Label(self.header_frame, text="Material Manager", font=("Helvetica", 20, "bold"), bg=self.title_color, fg=self.button_text_color)
        self.header_label.pack(pady=10)
        
        # Frame Menu Principal
        self.menu_frame = tk.Frame(self)  # Reduced width
        self.menu_frame.grid(row=1, column=0, sticky="ns", padx=10)

        # Ajouter les boutons dans la frame du menu avec grid pour qu'ils prennent toute la largeur et une taille fixe
        button_width = 15  # Reduced button width

        self.menu_button1 = tk.Button(self.menu_frame, text="Home", font=self.font, bg=self.button_color, fg=self.button_text_color, width=button_width, command=self.show_content_home)
        self.menu_button2 = tk.Button(self.menu_frame, text="Materials", font=self.font, bg=self.button_color, fg=self.button_text_color, width=button_width, command=self.show_content_materials)
        self.menu_button3 = tk.Button(self.menu_frame, text="Categories", font=self.font, bg=self.button_color, fg=self.button_text_color, width=button_width, command=self.show_content_categories)
        self.menu_button4 = tk.Button(self.menu_frame, text="Account", font=self.font, bg=self.button_color, fg=self.button_text_color, width=button_width, command=self.show_content_account)
        self.menu_button5 = tk.Button(self.menu_frame, text="Administration", font=self.font, bg=self.button_color, fg=self.button_text_color, width=button_width, command=self.show_content_administration)
        
        self.menu_button1.grid(row=0, column=0, sticky="ew", pady=5)
        self.menu_button2.grid(row=1, column=0, sticky="ew", pady=5)
        self.menu_button3.grid(row=2, column=0, sticky="ew", pady=5)
        self.menu_button4.grid(row=3, column=0, sticky="ew", pady=5)
        self.menu_button5.grid(row=4, column=0, sticky="ew", pady=5)
        
        # Frame Contenu du Menu Sélectionné
        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.grid(row=1, column=1, columnspan=2, rowspan=2, sticky="nsew")
        
        
        
        # Frame Footer
        self.footer_frame = tk.Frame(self, bg=self.title_color, height=30)
        self.footer_frame.grid(row=3, column=0, columnspan=3, sticky="ew")
        
        self.footer_label = tk.Label(self.footer_frame, text="Lycée Qualifiant AL IRFANE - DR TAROUDANT- ARFE SOUSS MASSA-  copyright © 2025", font=self.font, bg=self.title_color, fg=self.button_text_color)
        self.footer_label.pack(pady=5)



    def show_content_home(self):
        # Clear the frame before adding new content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        show_statistiques(self.content_frame, self.title_color, self.font, self.bg_color)
      
    
    def show_content_materials(self):
        
        # Clear the frame before adding new content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        EquipmentApp(self.content_frame)
    
    def show_content_categories(self):
        # Clear the frame before adding new content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        CategoriesApp(self.content_frame)
    
    def show_content_account(self):
        # Clear the frame before adding new content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        #It is a space or development area which allows you to manage the account (change of personal information)
        message = "Il s'agit d'un espace encore de développement qui vous permet de gérer votre compte (modifier vos informations personnelles). \n \n It is a space or development area which allows you to manage the account (change of personal information)."
        label = ttk.Label(self.content_frame, text=message , font=("Helvetica", 12))
        label.grid(row=0, column=0, padx=10, pady=10)
    
    def show_content_administration(self):
        # Clear the frame before adding new content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        #It is a space or development area which allows you to manage the account (change of personal information)
        message = "Est une espèce encore de développement qui permet aux administrateur de gérer les comptes utilisateurs attribués en rôle à chaque utilisateur \n \n Is a species still in development that allows administrators to manage user accounts assigned as roles to each user."
        label = ttk.Label(self.content_frame, text=message , font=("Helvetica", 12))
        label.grid(row=0, column=0, padx=10, pady=10)
        


#if __name__ == "__main__":
#    app = Application()
#    app.mainloop()
