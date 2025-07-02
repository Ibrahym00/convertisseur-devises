import requests
import csv
from datetime import datetime

def convertir_devise(source, cible, montant):
    url = f"https://open.er-api.com/v6/latest/{source}"
    response = requests.get(url)

    try:
        data = response.json()
    except Exception as e:
        print("Erreur JSON :", e)
        print("Réponse brute :", response.text)
        return

    if response.status_code != 200 or "rates" not in data:
        print("Erreur lors de la récupération des données.")
        return

    taux = data["rates"].get(cible)

    if taux is None:
        print(f"Devise cible '{cible}' introuvable.")
        return

    resultat = montant * taux
    print(f"{montant} {source} = {resultat:.2f} {cible}")

    # 🔽 Sauvegarde de l'historique
    enregistrer_conversion(source, cible, montant, resultat, taux)

def enregistrer_conversion(source, cible, montant, resultat, taux):
    with open("historique.csv", mode="a", newline="", encoding="utf-8") as fichier:
        writer = csv.writer(fichier)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            source,
            cible,
            montant,
            taux,
            resultat
        ])

# Exemple d'utilisation
source = input("Devise source (ex: EUR) : ").upper()
cible = input("Devise cible (ex: USD) : ").upper()
montant = float(input("Montant à convertir : "))

convertir_devise(source, cible, montant)
