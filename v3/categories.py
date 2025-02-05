import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os
import re

from entities.role import Role
from entities.category import Category, InventoryManager
from entities.user import User
from entities.equipment import  Equipment



class CategoriesApp:
    def __init__(self, master):
        self.master = master
              

        self.master = master

        self.bg_color = "#f0f0f0"
        self.title_color = "#4a7a8c"
        self.button_color = "#558C8C"
        self.button_text_color = "#ffffff"
        self.frame_color = "#d9d9d9"
        self.font = ("Helvetica", 12)

        # Configure overall background color
        self.master.configure(bg=self.bg_color)
        
        self.bg_color = "#f5f5f5"
        self.button_color = "#007BFF"
        self.button_text_color = "white"
        self.font = ("Helvetica", 10)

        self.master.configure(bg=self.bg_color)

        # Frame for categories (left side)
        self.category_frame = tk.Frame(self.master, bg=self.bg_color)
        self.category_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Category Treeview
        self.category_tree = ttk.Treeview(self.category_frame, columns=("Category"), show="headings")
        self.category_tree.heading("Category", text="Category")
        self.category_tree.column("Category", width=150, anchor="center")
        self.category_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Category buttons
        self.category_button_frame = tk.Frame(self.category_frame, bg=self.bg_color)
        self.category_button_frame.pack(fill="x", padx=5, pady=5)

        self.add_category_button = tk.Button(self.category_button_frame, text="Add Category", command=self.add_category,
                                             bg=self.button_color, fg=self.button_text_color, font=self.font)
        self.add_category_button.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.edit_category_button = tk.Button(self.category_button_frame, text="Edit Category", command=self.edit_category,
                                              bg=self.button_color, fg=self.button_text_color, font=self.font)
        self.edit_category_button.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.remove_category_button = tk.Button(self.category_button_frame, text="Remove Category", command=self.remove_category,
                                                bg=self.button_color, fg=self.button_text_color, font=self.font)
        self.remove_category_button.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        # Frame for equipment (right side)
        self.equipment_frame = tk.Frame(self.master, bg=self.bg_color)
        self.equipment_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        

        # Responsive layout
        self.master.grid_columnconfigure(0, weight=4)  # Categories take space
        self.master.grid_rowconfigure(0, weight=1)

        # Simulate an inventory manager
        self.inventory_manager = InventoryManager(os.path.join(os.path.dirname(__file__), 'entities', 'data.json'))
        self.inventory_manager.load_data()


        # Initialize the current_category attribute
        self.categories = self.inventory_manager.categories

        if self.categories:
            self.current_category = self.categories[0] #if self.inventory_manager.categories else None
            for category in self.categories:
                self.category_tree.insert("", "end", values=(category.name,))




       
        


    def add_category(self):
        self.open_add_category_window()

    def edit_category(self):
        print("Edit Category Clicked")

    def remove_category(self):
        self.remove_category()

    def add_equipment(self):
        print("Add Equipment Clicked")


    


    
 
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    #def open_category_window(self):
        

    def open_add_category_window(self):
        add_category_window = tk.Toplevel(self.master)
        add_category_window.title("Add Category")
        self.center_window(add_category_window, 300, 150)

        tk.Label(add_category_window, text="Category Name:", font=self.font).pack(pady=5)
        name_entry = tk.Entry(add_category_window, font=self.font)
        name_entry.pack(pady=5)

        def on_add_confirm():
            name = name_entry.get()
            if name:
                self.inventory_manager.add_category(self.inventory_manager.newId(), name)
                self.category_tree.insert("", "end", values=(name,))
                add_category_window.destroy()

        tk.Button(add_category_window, text="Add", command=on_add_confirm, bg=self.button_color, fg=self.button_text_color, font=self.font).pack(pady=10)

    def remove_category(self):
        selected_item = self.category_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a category to remove.")
            return

        category_name = self.category_tree.item(selected_item, "values")[0]
        confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove '{category_name}'?")
        if confirm:
            self.inventory_manager.categories = [cat for cat in self.inventory_manager.categories if cat.name != category_name]
            self.category_tree.delete(selected_item)

    def select_category(self):
        selected_category = self.category_listbox.curselection()
        if not selected_category:
            messagebox.showwarning("Warning", "Please select a category.")
            return

        category_name = self.category_listbox.get(selected_category)
        self.current_category = self.inventory_manager.get_category(category_name)
        self.refresh_equipment_list()

        # Update the category label in the bottom frame
        self.category_label.config(text=f"Selected Category: {category_name}", fg="grey")

        # Close the category window after selecting a category
        self.category_window.destroy()

    def save_data(self):
        data = {
            "equipment_list": [item.__dict__ for item in self.inventory_manager.get_all_equipment()],
            "categories": [category.__dict__ for category in self.inventory_manager.get_all_categories()]
        }
        try:
            with open("equipment_data.json", "w") as file:
                json.dump(data, file, indent=4)  # Use indent for pretty-printing and better readability
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        if os.path.exists("equipment_data.json"):
            try:
                with open("equipment_data.json", "r") as file:
                    data = json.load(file)
                    # Load equipment_list
                    equipment_list = data.get("equipment_list", [])
                    for item in equipment_list:
                        self.inventory_manager.add_equipment(item["name"], item["quantity"], item["condition"], item["available_to_use"])
                    
                    # Load categories
                    categories = data.get("categories", [])
                    for category_data in categories:
                        category = Category(category_data["name"])
                        for item in category_data.get("equipment_list", []):
                            equipment = Equipment(item["name"], item["quantity"], item["condition"], item["available_to_use"])
                            category.add_equipment(equipment)
                        self.inventory_manager.categories.append(category)
                
                self.refresh_equipment_list()
            except json.JSONDecodeError:
                print("Error: equipment_data.json contains invalid JSON data. Resetting to default.")
                # Reset the file to avoid further errors
                with open("equipment_data.json", "w") as file:
                    json.dump({"equipment_list": [], "categories": []}, file)
            except Exception as e:
                print(f"Error loading data: {e}")
