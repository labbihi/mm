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

class EquipmentApp:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg="#f0f0f0")

        # Define colors and styles
        self.bg_color = "#f0f0f0"
        self.title_color = "#4a7a8c"
        self.button_color = "#558C8C"
        self.button_text_color = "#ffffff"
        self.frame_color = "#d9d9d9"
        self.font = ("Helvetica", 12)

        # Configure grid layout
        self.master.grid_columnconfigure(0, weight=0)  # Fixed width for category selection
        self.master.grid_columnconfigure(1, weight=1)  # Resizable for equipment list
        self.master.grid_rowconfigure(0, weight=0)  # Fixed height for category selection
        self.master.grid_rowconfigure(1, weight=1)  # Resizable for equipment list
        self.master.grid_rowconfigure(2, weight=0)  # Fixed height for buttons

        # Initialize the inventory manager
        self.inventory_manager = InventoryManager(os.path.join(os.path.dirname(__file__), 'entities', 'data.json'))
        self.inventory_manager.load_data()

        # Initialize the current_category attribute
        self.categories = self.inventory_manager.categories
        self.current_category = None

        # Category selection
        self.category_combobox = ttk.Combobox(self.master, values=[category.name for category in self.categories], state="readonly", font=self.font)
        self.category_combobox.set("Select Category")
        self.category_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Bind category selection event
        def on_category_select(event):
            selected_category_name = self.category_combobox.get()
            self.current_category = self.inventory_manager.get_category(selected_category_name)
            self.refresh_equipment_list()
            self.category_label.config(text=f"Selected Category: {selected_category_name}", fg="grey")

        self.category_combobox.bind("<<ComboboxSelected>>", on_category_select)

        # Equipment Treeview (table) to display equipment details
        self.treeview = ttk.Treeview(self.master, columns=("Item", "Quantity", "Condition", "Available to Use"), show="headings")
        self.treeview.heading("Item", text="Item")
        self.treeview.heading("Quantity", text="Quantity")
        self.treeview.heading("Condition", text="Condition")
        self.treeview.heading("Available to Use", text="Available to Use")

        # Set column widths for better visibility
        self.treeview.column("Item", width=120, anchor="center")
        self.treeview.column("Quantity", width=90, anchor="center")
        self.treeview.column("Condition", width=100, anchor="center")
        self.treeview.column("Available to Use", width=100, anchor="center")

        # Place the Treeview with moderate expansion
        self.treeview.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Style for the Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background=self.title_color, foreground="white", borderwidth=2)
        style.configure("Treeview", background=self.bg_color, fieldbackground=self.bg_color, font=self.font, rowheight=25, borderwidth=2)
        style.map("Treeview", background=[("selected", self.button_color)])

        # Create a frame for the buttons below the table
        self.bottom_button_frame = tk.Frame(self.master, bg=self.bg_color)
        self.bottom_button_frame.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

        # Add buttons to the bottom frame
        self.add_button = tk.Button(self.bottom_button_frame, text="Add Equipment", command=self.open_add_equipment_window,
                                    bg=self.button_color, fg=self.button_text_color, font=self.font, bd=0, padx=10, pady=5)
        self.add_button.pack(side="left", fill="x", padx=5, pady=5)

        self.edit_button = tk.Button(self.bottom_button_frame, text="Edit Equipment", command=self.open_edit_equipment_window,
                                    bg=self.button_color, fg=self.button_text_color, font=self.font, bd=0, padx=10, pady=5)
        self.edit_button.pack(side="left", fill="x", padx=5, pady=5)

        self.remove_button = tk.Button(self.bottom_button_frame, text="Remove Equipment", command=self.remove_equipment,
                                    bg=self.button_color, fg=self.button_text_color, font=self.font, bd=0, padx=10, pady=5)
        self.remove_button.pack(side="left", fill="x", padx=5, pady=5)

        self.filter_button = tk.Button(self.bottom_button_frame, text="Filter Equipment", command=self.open_filter_window,
                                    bg=self.button_color, fg=self.button_text_color, font=self.font, bd=0, padx=10, pady=5)
        self.filter_button.pack(side="left", fill="x", padx=5, pady=5)

        self.reset_button = tk.Button(self.bottom_button_frame, text="Reset Filter", command=self.reset_filter,
                                    bg=self.button_color, fg=self.button_text_color, font=self.font, bd=0, padx=10, pady=5)
        self.reset_button.pack(side="left", fill="x", padx=5, pady=5)

        # Add a label to display the selected category
        self.category_label = tk.Label(self.bottom_button_frame, text="No category selected", fg="grey", font=self.font)
        self.category_label.pack(side="left", fill="x", padx=5, pady=5)

        # Store the current filter criteria
        self.current_filter_condition = "All"
        self.current_filter_availability = "All"

    def reset_filter(self):
        self.current_filter_condition = "All"
        self.current_filter_availability = "All"
        self.refresh_equipment_list()

    def open_filter_window(self):
        # Create filter window
        filter_window = tk.Toplevel(self.master)
        filter_window.title("Filter Equipment")
        self.center_window(filter_window, 500, 500)

        label = tk.Label(filter_window, text="Select filter criteria:", font=self.font)
        label.pack(pady=10)

        # Condition filter
        condition_label = tk.Label(filter_window, text="Condition:", font=self.font)
        condition_label.pack(pady=5)
        condition_combobox = ttk.Combobox(filter_window, values=["All", "New", "Good", "Fair", "Worn", "Damaged"], state="readonly", font=self.font)
        condition_combobox.set(self.current_filter_condition)
        condition_combobox.pack(pady=5)

        # Availability filter
        availability_label = tk.Label(filter_window, text="Availability:", font=self.font)
        availability_label.pack(pady=5)
        availability_combobox = ttk.Combobox(filter_window, values=["All", "Yes", "No"], state="readonly", font=self.font)
        availability_combobox.set(self.current_filter_availability)
        availability_combobox.pack(pady=5)

        # Confirm button
        def on_filter_confirm():
            self.current_filter_condition = condition_combobox.get()
            self.current_filter_availability = availability_combobox.get()
            self.apply_filter(self.current_filter_condition, self.current_filter_availability)
            filter_window.destroy()  # Close the filter window after applying the filter

        button_frame = tk.Frame(filter_window, bg=self.bg_color)
        button_frame.pack(pady=10)

        confirm_button = tk.Button(button_frame, text="Confirm", command=on_filter_confirm, bg=self.button_color, fg=self.button_text_color, font=self.font)
        confirm_button.pack(padx=10, pady=10)

    def apply_filter(self, condition, availability):
        filtered_items = self.inventory_manager.get_filtered_equipment(condition, availability)
        self.refresh_equipment_list(filtered_items)

    def open_add_equipment_window(self):
        if not self.current_category:
            messagebox.showwarning("Warning", "Please select a category first.")
            return

        add_window = tk.Toplevel(self.master)
        add_window.title("Add Equipment")
        self.center_window(add_window, 500, 500)

        tk.Label(add_window, text="Name:", font=self.font).pack(pady=5)
        name_entry = tk.Entry(add_window, font=self.font)
        name_entry.pack(pady=5)
        name_error_label = tk.Label(add_window, text="", font=self.font, fg="red")
        name_error_label.pack()

        tk.Label(add_window, text="Quantity:", font=self.font).pack(pady=5)
        quantity_entry = tk.Entry(add_window, font=self.font)
        quantity_entry.pack(pady=5)
        quantity_error_label = tk.Label(add_window, text="", font=self.font, fg="red")
        quantity_error_label.pack()

        tk.Label(add_window, text="Condition:", font=self.font).pack(pady=5)
        condition_combobox = ttk.Combobox(add_window, values=["New", "Good", "Fair", "Worn", "Damaged"], state="readonly", font=self.font)
        condition_combobox.pack(pady=5)
        condition_error_label = tk.Label(add_window, text="", font=self.font, fg="red")
        condition_error_label.pack()

        tk.Label(add_window, text="Available to Use:", font=self.font).pack(pady=5)
        availability_combobox = ttk.Combobox(add_window, values=["Yes", "No"], state="readonly", font=self.font)
        availability_combobox.pack(pady=5)
        availability_error_label = tk.Label(add_window, text="", font=self.font, fg="red")
        availability_error_label.pack()

        def validate_entries():
            valid = True
            if not re.match("^[A-Za-z ]*$", name_entry.get()):
                name_error_label.config(text="Name cannot contain numbers or special characters")
                valid = False
            else:
                name_error_label.config(text="")

            if not quantity_entry.get().isdigit():
                quantity_error_label.config(text="Quantity must be a number")
                valid = False
            else:
                quantity_error_label.config(text="")

            if not condition_combobox.get():
                condition_error_label.config(text="Condition cannot be empty")
                valid = False
            else:
                condition_error_label.config(text="")

            if not availability_combobox.get():
                availability_error_label.config(text="Availability cannot be empty")
                valid = False
            else:
                availability_error_label.config(text="")

            return valid

        def on_add_confirm():
            if validate_entries():
                name = name_entry.get()
                quantity = int(quantity_entry.get())
                condition = condition_combobox.get()
                available_to_use = availability_combobox.get() == "Yes"
                equipment = Equipment(self.inventory_manager.newEqId(),name, quantity, condition, available_to_use, self.current_category)
                self.current_category.add_equipment(equipment)
                self.refresh_equipment_list()
                self.inventory_manager.add_equipment_to_category(self.current_category.id, equipment)  # Save data after adding equipment
                add_window.destroy()

        tk.Button(add_window, text="Add", command=on_add_confirm, bg=self.button_color, fg=self.button_text_color, font=self.font).pack(pady=10)

    def open_edit_equipment_window(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to edit.")
            return

        item_index = self.treeview.index(selected_item)
        item = self.current_category.get_equipment()[item_index]

        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Equipment")
        self.center_window(edit_window, 500, 500)

        tk.Label(edit_window, text="Name:", font=self.font).pack(pady=5)
        name_entry = tk.Entry(edit_window, font=self.font)
        name_entry.insert(0, item.name)
        name_entry.pack(pady=5)
        name_error_label = tk.Label(edit_window, text="", font=self.font, fg="red")
        name_error_label.pack()

        tk.Label(edit_window, text="Quantity:", font=self.font).pack(pady=5)
        quantity_entry = tk.Entry(edit_window, font=self.font)
        quantity_entry.insert(0, item.quantity)
        quantity_entry.pack(pady=5)
        quantity_error_label = tk.Label(edit_window, text="", font=self.font, fg="red")
        quantity_error_label.pack()

        tk.Label(edit_window, text="Condition:", font=self.font).pack(pady=5)
        condition_combobox = ttk.Combobox(edit_window, values=["New", "Good", "Fair", "Worn", "Damaged"], state="readonly", font=self.font)
        condition_combobox.set(item.condition)
        condition_combobox.pack(pady=5)
        condition_error_label = tk.Label(edit_window, text="", font=self.font, fg="red")
        condition_error_label.pack()

        tk.Label(edit_window, text="Available to Use:", font=self.font).pack(pady=5)
        availability_combobox = ttk.Combobox(edit_window, values=["Yes", "No"], state="readonly", font=self.font)
        availability_combobox.set("Yes" if item.available_to_use else "No")
        availability_combobox.pack(pady=5)
        availability_error_label = tk.Label(edit_window, text="", font=self.font, fg="red")
        availability_error_label.pack()

        def validate_entries():
            valid = True
            if not re.match("^[A-Za-z ]*$", name_entry.get()):
                name_error_label.config(text="Name cannot contain numbers or special characters")
                valid = False
            else:
                name_error_label.config(text="")

            if not quantity_entry.get().isdigit():
                quantity_error_label.config(text="Quantity must be a number")
                valid = False
            else:
                quantity_error_label.config(text="")

            if not condition_combobox.get():
                condition_error_label.config(text="Condition cannot be empty")
                valid = False
            else:
                condition_error_label.config(text="")

            if not availability_combobox.get():
                availability_error_label.config(text="Availability cannot be empty")
                valid = False
            else:
                availability_error_label.config(text="")

            return valid

        def on_edit_confirm():
            if validate_entries():
                name = name_entry.get()
                quantity = int(quantity_entry.get())
                condition = condition_combobox.get()
                available_to_use = availability_combobox.get() == "Yes"
                self.current_category.get_equipment()[item_index] = Equipment(None, name, quantity, condition, available_to_use, self.current_category)
                self.refresh_equipment_list()
                self.inventory_manager.save_data()  # Save data after editing equipment
                edit_window.destroy()

        tk.Button(edit_window, text="Save", command=on_edit_confirm, bg=self.button_color, fg=self.button_text_color, font=self.font).pack(pady=10)

    def remove_equipment(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to remove.")
            return

        item_index = self.treeview.index(selected_item)
        item = self.current_category.get_equipment()[item_index]

        confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove '{item.name}'?")
        if confirm:
            self.current_category.remove_equipment(item)
            self.refresh_equipment_list()
            self.inventory_manager.save_data()  # Save data after removing equipment

    def refresh_equipment_list(self, items=None):
        for i in self.treeview.get_children():
            self.treeview.delete(i)

        if items is None:
            if self.current_category:
                items = self.current_category.get_equipment()
            else:
                items = []

        for item in items:
            available_to_use = "Yes" if item.available_to_use else "No"
            self.treeview.insert("", "end", values=(item.name, item.quantity, item.condition, available_to_use))

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def open_category_window(self):
        # Create a new window for category management
        self.category_window = tk.Toplevel(self.master)
        self.category_window.title("Category Management")
        self.center_window(self.category_window, 500, 500)

        # Add widgets for category management
        tk.Label(self.category_window, text="Category Management", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Listbox to display categories
        self.category_listbox = tk.Listbox(self.category_window, font=self.font)
        self.category_listbox.pack(pady=10, padx=10, fill="both", expand=True)

        # Populate the listbox with existing categories
        for category in self.inventory_manager.get_all_categories():
            self.category_listbox.insert(tk.END, category.name)

        # Frame for buttons
        button_frame = tk.Frame(self.category_window, bg=self.bg_color)
        button_frame.pack(pady=10)

        # Add Category Button
        add_button = tk.Button(button_frame, text="Add Category", command=self.open_add_category_window,
                               bg=self.button_color, fg=self.button_text_color, font=self.font)
        add_button.pack(side="left", padx=5)

        # Remove Category Button
        remove_button = tk.Button(button_frame, text="Remove Category", command=self.remove_category,
                                  bg=self.button_color, fg=self.button_text_color, font=self.font)
        remove_button.pack(side="left", padx=5)

        # Select Category Button
        select_button = tk.Button(button_frame, text="Select Category", command=self.select_category,
                                  bg=self.button_color, fg=self.button_text_color, font=self.font)
        select_button.pack(side="left", padx=5)

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
                self.inventory_manager.add_category(name)
                self.category_listbox.insert(tk.END, name)
                add_category_window.destroy()

        tk.Button(add_category_window, text="Add", command=on_add_confirm, bg=self.button_color, fg=self.button_text_color, font=self.font).pack(pady=10)

    def remove_category(self):
        selected_category = self.category_listbox.curselection()
        if not selected_category:
            messagebox.showwarning("Warning", "Please select a category to remove.")
            return

        category_name = self.category_listbox.get(selected_category)
        confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove '{category_name}'?")
        if confirm:
            self.inventory_manager.remove_category(selected_category[0].id)  #.categories.pop(selected_category[0])
            self.category_listbox.delete(selected_category)

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

    """  def save_data(self):
            data = {
                "equipment_list": [item.__dict__ for item in self.inventory_manager.get_all_equipment()],
                "categories": [category.__dict__ for category in self.inventory_manager.get_all_categories()]
            }
            try:
                with open("equipment_data.json", "w") as file:
                    json.dump(data, file, indent=4)  # Use indent for pretty-printing and better readability
            except Exception as e:
                print(f"Error saving data: {e}")
    """
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

if __name__ == "__main__":
    root = tk.Tk()
    app = EquipmentApp(root)
    root.mainloop()