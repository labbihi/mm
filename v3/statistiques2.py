import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os
import re

from entities.category import Category, InventoryManager

def show_statistiques(content_frame, title_color, font, bg):
        
        # Supprimer les widgets existants
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        inventory_manager = InventoryManager(os.path.join(os.path.dirname(__file__), 'entities', 'data.json'))
        inventory_manager.load_data()

        
        current_category = "Informatique"
        



        category_combobox = ttk.Combobox(content_frame, values=[category.name for category in  inventory_manager.categories], state="readonly", font=font)
        category_combobox.set(current_category)
        category_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        def on_category_select(event):
            selected_category_name = category_combobox.get()           
            refresh_equipment_list(selected_category_name)

        category_combobox.bind("<<ComboboxSelected>>", on_category_select)


        def refresh_equipment_list(category_name):

            data = inventory_manager.get_category_for_statistique(category_name)


            # Récupérer les données de la matière sélectionnée
            matiere = category_name
            matiere_data = data.get(matiere)

            # Titre
            title_label = tk.Label(content_frame, text=f"Statistique de la catégorie: {matiere}",
                    font=font, fg=title_color, bg=bg)
            title_label.grid(row=1, column=0, columnspan=3, pady=10)

            # Création des graphiques
            fig, axes = plt.subplots(1, 3, figsize=(10, 4))

            # Histogramme - Quantité des équipements
            fig.set_size_inches(11, 4)  # Increase width and minimize height
            axes[0].bar(matiere_data["equipments"], matiere_data["quantities"], color=["blue", "green", "red", "purple", "orange"])
            axes[0].set_title("Quantité des Équipements")
            axes[0].set_ylabel("Quantité")
            axes[0].tick_params(axis='x', rotation=30)
            
            # Diagramme circulaire - Répartition des conditions
            # Vérifiez que la longueur des labels et des counts correspond
            if len(matiere_data["condition_counts"]) == len(matiere_data["conditions"]):
                axes[1].pie(matiere_data["condition_counts"], labels=matiere_data["conditions"], autopct="%1.1f%%",
                        colors=["lightblue", "lightgreen", "pink", "gray"])
                axes[1].set_title("État des Équipements")
            else:
                print("Erreur: Le nombre de conditions et de counts ne correspond pas.")

            # Graphique - Disponibilité des équipements
            axes[2].bar(matiere_data["availability_labels"], matiere_data["availability_counts"], color=["green", "red"])
            axes[2].set_title("Disponibilité des Équipements")

            # Affichage du graphique dans Tkinter
            canvas = FigureCanvasTkAgg(fig, master=content_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=2, column=0, columnspan=3)


        refresh_equipment_list(current_category)
