import tkinter as tk
from tkinter import ttk
import requests
import math

# Fonction pour récupérer les taux de change depuis l'API Open Exchange Rates
def get_exchange_rates():
    try:
        response = requests.get("https://open.er-api.com/v6/latest")
        if response.status_code == 200:
            return response.json()["rates"]
        else:
            return None
    except requests.RequestException:
        return None

# Récupérer les taux de change depuis l'API
exchange_rates_data = get_exchange_rates()

# Vérifier si les données ont été récupérées avec succès
if exchange_rates_data is None:
    print("Erreur lors de la récupération des taux de change depuis l'API")
else:
    # Facteurs de conversion pour chaque catégorie d'unités
    conversion_factors = {
        # Devises
        'Devises': exchange_rates_data,
        # Temps
        'Temps': {
            'Secondes': 1,
            'Minutes': 60,
            'Heures': 3600,
            'Jours': 86400,
            'Semaines': 604800,
            'Mois': 2628000,
            'Années': 31536000
        },
        # Températures
        'Températures': {
            'Celsius': 1,
            'Fahrenheit': 1,
            'Kelvin': 1
        },

        # Angles
        'Angles': {
            'Degrés': 1,
            'Radians': 1,
            'Grades': 1
        },

        # Distances
        'Distances': {
            'Millimètres': 0.001,
            'Centimètres': 0.01,
            'Décimètres': 0.1,
            'Mètres': 1,
            'Décamètres': 10,
            'Hectomètres': 100,
            'Kilomètres': 1000
        },
        # Masses
        'Masses': {
            'Milligrammes': 0.001,
            'Centigrammes': 0.01,
            'Décigrammes': 0.1,
            'Grammes': 1,
            'Décagrammes': 10,
            'Hectogrammes': 100,
            'Kilogrammes': 1000
        },
        # Volumes
        'Volumes': {
            'Millilitres': 0.001,
            'Centilitres': 0.01,
            'Décilitres': 0.1,
            'Litres': 1,
            'Décalitres': 10,
            'Hectolitres': 100,
            'Kilolitres': 1000,
            'Mètres cubes': 1000,
            'Pieds cubes': 28316.8,
            'Pouces cubes': 16.3871,
            'Gallons': 3785.41,
            'Gallons impériaux': 4546.09
        },
        # Superficie
        'Superficie': {
            'Millimètres carrés': 0.000001,
            'Centimètres carrés': 0.0001,
            'Décimètres carrés': 0.01,
            'Mètres carrés': 1,
            'Hectares': 10000,
            'Kilomètres carrés': 1000000,
            'Acres': 4046.86
        },
        # Vitesse
        'Vitesse': {
            'Mètres par seconde': 1,
            'Kilomètres par heure': 0.277778,
            'Miles par heure': 0.44704,
            'Nœuds': 0.514444
        },
        # Fréquence
        'Fréquence': {
            'Hertz': 1,
            'Kilohertz': 1000,
            'Megahertz': 1000000,
            'Gigahertz': 1000000000
        },
        # Pression
        'Pression': {
            'Pascal': 1,
            'Bar': 100000,
            'PSI': 6895,
            'Atmosphères': 101325
        },
        # Énergie
        'Énergie': {
            'Joules': 1,
            'Calories': 4.184,
            'Watt-heures': 3600,
            'Kilowatt-heures': 3600000
        }
    }

    # Création de l'interface graphique avec les données de l'API
    root = tk.Tk()
    root.title("Convertisseur d'unités")

    # Frame pour les listes déroulantes
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky="nsew")

    # Label et liste déroulante pour la catégorie d'unité
    label_category = ttk.Label(frame, text="Catégorie d'unité :")
    label_category.grid(row=0, column=0, padx=(0, 10))
    selected_category = tk.StringVar()
    dropdown_category = ttk.Combobox(frame, textvariable=selected_category, values=list(conversion_factors.keys()), state="readonly", width=20)
    dropdown_category.grid(row=0, column=1)

    # Label et liste déroulante pour l'unité de départ
    label_from = ttk.Label(frame, text="Unité de départ :")
    label_from.grid(row=1, column=0, padx=(0, 10), pady=(10, 0))
    selected_from = tk.StringVar()
    dropdown_from = ttk.Combobox(frame, textvariable=selected_from, state="readonly", width=20)
    dropdown_from.grid(row=1, column=1, pady=(10, 0))

    # Label et liste déroulante pour l'unité de destination
    label_to = ttk.Label(frame, text="Unité de destination :")
    label_to.grid(row=2, column=0, padx=(0, 10), pady=(10, 0))
    selected_to = tk.StringVar()
    dropdown_to = ttk.Combobox(frame, textvariable=selected_to, state="readonly", width=20)
    dropdown_to.grid(row=2, column=1, pady=(10, 0))

    # Bouton pour effectuer la conversion
    def convert():
        unit_category = selected_category.get()
        unit_from = selected_from.get()
        unit_to = selected_to.get()
        
        try:
            value = float(entry_value.get())
            
            # Vérifier si l'unité appartient à la catégorie "Températures"
            if unit_category == 'Températures':
                result = convert_temperature(value, unit_from, unit_to)
            # Vérifier si l'unité appartient à la catégorie "Angles"
            elif unit_category == 'Angles':
                result = convert_angle(value, unit_from, unit_to)
            # Si ce n'est ni une température ni un angle, utiliser les facteurs de conversion normaux
            else:
                factor_from = conversion_factors[unit_category][unit_from]
                factor_to = conversion_factors[unit_category][unit_to]
                result = value * factor_from / factor_to
            
            label_result.config(text=f"{result} {unit_to}")
        except ValueError:
            label_result.config(text="Veuillez entrer un nombre valide.")
        except KeyError:
            label_result.config(text="Veuillez sélectionner une catégorie.")

    # Fonction pour convertir les températures
    def convert_temperature(value, unit_from, unit_to):
        if unit_from == unit_to:
            return value
        elif unit_from == 'Celsius' and unit_to == 'Fahrenheit':
            return (value * 9/5) + 32
        elif unit_from == 'Fahrenheit' and unit_to == 'Celsius':
            return (value - 32) * (5/9)
        elif unit_from == 'Celsius' and unit_to == 'Kelvin':
            return value + 273.15
        elif unit_from == 'Kelvin' and unit_to == 'Celsius':
            return value - 273.15
        elif unit_from == 'Fahrenheit' and unit_to == 'Kelvin':
            return (value + 459.67) * (5/9)
        elif unit_from == 'Kelvin' and unit_to == 'Fahrenheit':
            return value * 9/5 - 459.67

    # Fonction pour convertir les angles
    def convert_angle(value, unit_from, unit_to):
        if unit_from == unit_to:
            return value
        elif unit_from == 'Degrés' and unit_to == 'Radians':
            return value * (math.pi/180)
        elif unit_from == 'Radians' and unit_to == 'Degrés':
            return value * (180/math.pi)
        elif unit_from == 'Degrés' and unit_to == 'Grades':
            return value * (10/9)
        elif unit_from == 'Grades' and unit_to == 'Degrés':
            return value * (9/10)
        elif unit_from == 'Radians' and unit_to == 'Grades':
            return value * (200/math.pi)
        elif unit_from == 'Grades' and unit_to == 'Radians':
            return value * (math.pi/200)

    convert_button = ttk.Button(frame, text="Convertir", command=convert)
    convert_button.grid(row=3, columnspan=2, pady=(10, 0))

    # Entrée pour saisir la valeur à convertir
    label_value = ttk.Label(frame, text="Valeur :")
    label_value.grid(row=4, column=0, padx=(0, 10), pady=(10, 0))
    entry_value = ttk.Entry(frame)
    entry_value.grid(row=4, column=1, pady=(10, 0))

    # Label pour afficher le résultat de la conversion
    label_result = ttk.Label(frame, text="")
    label_result.grid(row=5, columnspan=2)

    # Fonction pour mettre à jour les unités en fonction de la catégorie sélectionnée
    def update_units(*args):
        category = selected_category.get()
        if category:
            units = list(conversion_factors[category].keys())
            selected_from.set(units[0])
            selected_to.set(units[1])
            dropdown_from['values'] = units
            dropdown_to['values'] = units

    # Mettre à jour les unités initiales
    update_units()

    # Associer la fonction de mise à jour des unités à la sélection de la catégorie
    selected_category.trace('w', update_units)

    root.mainloop()
