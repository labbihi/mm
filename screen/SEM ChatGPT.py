import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import Listbox, Scrollbar


class InventoryManager:
    def __init__(self):
        self.equipment = []

    def add_item(self, item):
        self.equipment.append(item)

    def get_items(self, condition="All", availability="All"):
        filtered_items = []
        for item in self.equipment:
            if condition == "All" or item['condition'] == condition:
                if availability == "All" or (availability == "Available" and item['available']):
                    filtered_items.append(item)
        return filtered_items

    def edit_item(self, index, new_item):
        self.equipment[index] = new_item


class EquipmentApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sport Material Manager")
        self.master.geometry("900x800")

        # Define colors and styles
        self.bg_color = "#f0f0f0"
        self.title_color = "#4a7a8c"
        self.button_color = "#558C8C"
        self.button_text_color = "#ffffff"
        self.frame_color = "#d9d9d9"
        self.font = ("Helvetica", 12)

        # Configure overall background color
        self.master.configure(bg=self.bg_color)

        # Create a frame for the title (top of the window)
        self.title_frame = tk.Frame(self.master, bg=self.frame_color)
        self.title_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Create a large title label inside the frame
        self.title_label = tk.Label(self.title_frame, text="Welcome to Sport Material Manager!",
                                    font=("Helvetica", 24, "bold"), fg=self.title_color, bg=self.frame_color)
        self.title_label.pack(padx=10, pady=10)

        # Create button frame
        self.button_frame = tk.Frame(self.master, bg=self.bg_color)
        self.button_frame.grid(row=1, column=0, sticky="ns", padx=10, pady=10)

        # Initialize filter attributes
        self.current_filter_condition = "All"
        self.current_filter_availability = "All"

        # Create control buttons
        self.add_button = tk.Button(self.button_frame, text="Add Equipment",
                                    command=self.open_add_equipment_window,
                                    bg=self.button_color, fg=self.button_text_color, font=self.font)
        self.add_button.pack(side="top", fill="x", pady=5)

        self.edit_button = tk.Button(self.button_frame, text="Edit Equipment",
                                     command=self.open_edit_equipment_window,
                                     bg=self.button_color, fg=self.button_text_color, font=self.font)
        self.edit_button.pack(side="top", fill="x", pady=5)

        self.filter_frame = tk.Frame(self.button_frame)
        self.filter_frame.pack(side="top", fill="x", pady=5)

        condition_label = tk.Label(self.filter_frame, text="Condition:")
        condition_label.pack(side="left")
        self.condition_var = tk.StringVar(value="All")
        self.condition_combobox = ttk.Combobox(self.filter_frame, textvariable=self.condition_var,
                                               values=["All", "New", "Used"], state='readonly')
        self.condition_combobox.pack(side="left")

        availability_label = tk.Label(self.filter_frame, text="Availability:")
        availability_label.pack(side="left")
        self.availability_var = tk.StringVar(value="All")
        self.availability_combobox = ttk.Combobox(self.filter_frame, textvariable=self.availability_var,
                                                  values=["All", "Available", "Unavailable"], state='readonly')
        self.availability_combobox.pack(side="left")

        self.filter_button = tk.Button(self.button_frame, text="Filter", command=self.apply_filter)
        self.filter_button.pack(side="top", fill="x", pady=5)

        # Create a listbox to display equipment
        self.equipment_listbox = Listbox(self.master, width=50)
        self.equipment_listbox.grid(row=1, column=1, padx=10, pady=10)

        # Configure scrollbar for the listbox
        self.scrollbar = Scrollbar(self.master, orient="vertical")
        self.scrollbar.config(command=self.equipment_listbox.yview)
        self.equipment_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=2, sticky='ns')

        # Create an inventory manager
        self.inventory_manager = InventoryManager()

        # Add some fake data for demonstration purposes
        self.add_fake_data()

        # Refresh equipment list initially
        self.refresh_equipment_list()

    def open_add_equipment_window(self):
        self.open_equipment_window("Add Equipment")

    def open_edit_equipment_window(self):
        selected_item_index = self.equipment_listbox.curselection()
        if not selected_item_index:
            messagebox.showwarning("Edit Equipment", "Please select an item to edit.")
            return

        # Get the selected item's details
        selected_item_index = selected_item_index[0]
        selected_item = self.inventory_manager.equipment[selected_item_index]
        self.open_equipment_window("Edit Equipment", selected_item, selected_item_index)

    def open_equipment_window(self, title, item=None, index=None):
        window = tk.Toplevel(self.master)
        window.title(title)

        tk.Label(window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(window)
        name_entry.pack(pady=5)

        tk.Label(window, text="Condition:").pack(pady=5)
        condition_entry = ttk.Combobox(window, values=["New", "Used"], state='readonly')
        condition_entry.pack(pady=5)

        tk.Label(window, text="Availability:").pack(pady=5)
        availability_entry = ttk.Combobox(window, values=["Available", "Unavailable"], state='readonly')
        availability_entry.pack(pady=5)

        # Fill fields if editing an existing item
        if item:
            name_entry.insert(0, item['name'])
            condition_entry.set(item['condition'])
            availability_entry.set("Available" if item['available'] else "Unavailable")

        def save_item():
            name = name_entry.get()
            condition = condition_entry.get()
            availability = availability_entry.get() == "Available"
            if index is not None:
                # Edit existing item
                self.inventory_manager.edit_item(index,
                                                 {"name": name, "condition": condition, "available": availability})
            else:
                # Add new item
                self.inventory_manager.add_item({"name": name, "condition": condition, "available": availability})
            self.refresh_equipment_list()
            window.destroy()

        save_button = tk.Button(window, text="Save", command=save_item)
        save_button.pack(pady=20)

    def add_fake_data(self):
        # Simulating adding fake inventory data
        self.inventory_manager.add_item({"name": "Football", "condition": "New", "available": True})
        self.inventory_manager.add_item({"name": "Tennis Racket", "condition": "Used", "available": False})
        self.inventory_manager.add_item({"name": "Basketball", "condition": "New", "available": True})
        self.inventory_manager.add_item({"name": "Baseball Bat", "condition": "Used", "available": True})
        self.refresh_equipment_list()

    def refresh_equipment_list(self):
        self.equipment_listbox.delete(0, tk.END)  # Clear the listbox

        filtered_items = self.inventory_manager.get_items(self.current_filter_condition,
                                                          self.current_filter_availability)
        for item in filtered_items:
            availability_text = "Available" if item['available'] else "Unavailable"
            display_text = f"{item['name']} - Condition: {item['condition']} - {availability_text}"
            self.equipment_listbox.insert(tk.END, display_text)

    def apply_filter(self):
        # Apply selected filters
        self.current_filter_condition = self.condition_var.get()
        self.current_filter_availability = self.availability_var.get()
        self.refresh_equipment_list()


if __name__ == "__main__":
    root = tk.Tk()  # Create the main Tkinter window
    app = EquipmentApp(root)
    root.mainloop()