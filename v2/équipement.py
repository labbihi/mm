import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Données fictives pour chaque matière académique
data = {
    "Physique": {
        "equipments": ["Oscilloscopes", "Multimètres", "Lentilles", "Systèmes optiques", "Bobines"],
        "quantities": [10, 15, 8, 5, 12],
        "conditions": ["Neuf", "Bon", "Usé", "Endommagé"],
        "condition_counts": [8, 12, 6, 2],
        "availability_labels": ["Disponible", "Indisponible"],
        "availability_counts": [20, 5],
    },
    "Chimie": {
        "equipments": ["Béchers", "Pipettes", "Microscopes", "Tubes à essai", "Agitateurs"],
        "quantities": [20, 30, 10, 50, 8],
        "conditions": ["Neuf", "Bon", "Usé", "Endommagé"],
        "condition_counts": [15, 20, 10, 5],
        "availability_labels": ["Disponible", "Indisponible"],
        "availability_counts": [25, 10],
    },
    "Mathématiques": {
        "equipments": ["Calculatrices", "Règles", "Compas", "Rapporteurs", "Crayons"],
        "quantities": [50, 40, 30, 25, 100],
        "conditions": ["Neuf", "Bon", "Usé", "Endommagé"],
        "condition_counts": [30, 40, 20, 10],
        "availability_labels": ["Disponible", "Indisponible"],
        "availability_counts": [60, 15],
    },
    "Art": {
        "equipments": ["Pinceaux", "Toiles", "Peintures", "Crayons", "Chevalets"],
        "quantities": [30, 20, 50, 40, 10],
        "conditions": ["Neuf", "Bon", "Usé", "Endommagé"],
        "condition_counts": [10, 25, 15, 5],
        "availability_labels": ["Disponible", "Indisponible"],
        "availability_counts": [35, 10],
    },
    "Anglais": {
        "equipments": ["Livres", "Dictionnaires", "Ordinateurs", "Tableaux", "Cahiers"],
        "quantities": [100, 50, 20, 10, 200],
        "conditions": ["Neuf", "Bon", "Usé", "Endommagé"],
        "condition_counts": [80, 60, 30, 10],
        "availability_labels": ["Disponible", "Indisponible"],
        "availability_counts": [150, 20],
    },
    "Arabe": {
        "equipments": ["Livres", "Cahiers", "Stylos", "Tableaux", "Ordinateurs"],
        "quantities": [80, 120, 200, 15, 10],
        "conditions": ["Neuf", "Bon", "Usé", "Endommagé"],
        "condition_counts": [60, 90, 40, 10],
        "availability_labels": ["Disponible", "Indisponible"],
        "availability_counts": [100, 25],
    },
    "Français": {
        "equipments": ["Livres", "Cahiers", "Stylos", "Tableaux", "Ordinateurs"],
        "quantities": [90, 110, 180, 20, 15],
        "conditions": ["Neuf", "Bon", "Usé", "Endommagé"],
        "condition_counts": [70, 80, 30, 10],
        "availability_labels": ["Disponible", "Indisponible"],
        "availability_counts": [120, 20],
    },
    "SVT": {
        "equipments": ["Microscopes", "Lames", "Échantillons", "Loupes", "Ordinateurs"],
        "quantities": [15, 50, 100, 30, 10],
        "conditions": ["Neuf", "Bon", "Usé", "Endommagé"],
        "condition_counts": [10, 30, 15, 5],
        "availability_labels": ["Disponible", "Indisponible"],
        "availability_counts": [40, 10],
    },
    "Sport": {
        "equipments": ["Ballons", "Raquettes", "Filets", "Chaussures", "Gants"],
        "quantities": [20, 15, 10, 25, 30],
        "conditions": ["Neuf", "Bon", "Usé", "Endommagé"],
        "condition_counts": [15, 20, 10, 5],
        "availability_labels": ["Disponible", "Indisponible"],
        "availability_counts": [50, 15],
    },
}

def show_statistics():
    # Fermer la fenêtre des statistiques précédente si elle existe
    if hasattr(show_statistics, "stats_window") and show_statistics.stats_window.winfo_exists():
        show_statistics.stats_window.destroy()

    # Récupérer la matière sélectionnée
    matiere = combo_matiere.get()
    matiere_data = data.get(matiere)
    if not matiere_data:
        tk.messagebox.showerror("Erreur", "Données non disponibles pour cette matière.")
        return

    # Créer une nouvelle fenêtre pour les statistiques
    show_statistics.stats_window = tk.Toplevel()
    show_statistics.stats_window.title(f"Statistiques des Matériels - {matiere}")
    show_statistics.stats_window.geometry("900x700")
    show_statistics.stats_window.configure(bg="#f0f0f0")

    # Titre
    title_label = tk.Label(show_statistics.stats_window, text=f"Statistiques des Matériels - {matiere}", font=("Helvetica", 20, "bold"), fg="#4a7a8c", bg="#f0f0f0")
    title_label.pack(pady=20)

    # Créer les graphiques
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    # 1️⃣ Histogramme - Quantité des équipements
    axes[0].bar(matiere_data["equipments"], matiere_data["quantities"], color=["blue", "green", "red", "purple", "orange"])
    axes[0].set_title("Quantité des Équipements")
    axes[0].set_ylabel("Quantité")
    axes[0].set_xlabel("Équipements")
    axes[0].tick_params(axis='x', rotation=30)

    # 2️⃣ Diagramme circulaire - Répartition des conditions
    axes[1].pie(matiere_data["condition_counts"], labels=matiere_data["conditions"], autopct="%1.1f%%", colors=["lightblue", "lightgreen", "pink", "gray"])
    axes[1].set_title("État des Équipements")

    # 3️⃣ Graphique - Disponibilité des équipements
    axes[2].bar(matiere_data["availability_labels"], matiere_data["availability_counts"], color=["green", "red"])
    axes[2].set_title("Disponibilité des Équipements")

    # Afficher les graphiques dans la fenêtre
    canvas = FigureCanvasTkAgg(fig, master=show_statistics.stats_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Bouton Quitter
    quit_button = tk.Button(show_statistics.stats_window, text="Quitter", command=show_statistics.stats_window.destroy, bg="#558C8C", fg="white", font=("Helvetica", 14), padx=20, pady=10)
    quit_button.pack(pady=10)

# Créer la fenêtre principale
root = tk.Tk()
root.title("Sélection de la Matière")
root.geometry("400x200")
root.configure(bg="#f0f0f0")

# Titre
title_label = tk.Label(root, text="Choisissez une matière", font=("Helvetica", 16, "bold"), fg="#4a7a8c", bg="#f0f0f0")
title_label.pack(pady=20)

# Liste déroulante pour choisir la matière
combo_matiere = ttk.Combobox(root, values=list(data.keys()), font=("Helvetica", 14), state="readonly")
combo_matiere.pack(pady=10)
combo_matiere.current(0)  # Sélectionner la première matière par défaut

# Bouton pour afficher les statistiques
btn_show_stats = tk.Button(root, text="Afficher les Statistiques", command=show_statistics, bg="#558C8C", fg="white", font=("Helvetica", 14), padx=20, pady=10)
btn_show_stats.pack(pady=10)

# Lancer l'application
root.mainloop()



