import streamlit as st
import requests
from datetime import datetime
import csv
import pandas as pd
from PIL import Image

# Configuration de la page
st.set_page_config(page_title="💱 Convertisseur de Devises", layout="centered")

# Affichage du logo
logo = Image.open("logo.png")
st.image(logo, width=120)

# Titre principal
st.title("💱 Convertisseur de Devises en Temps Réel")

# Liste des devises disponibles
devises_disponibles = ["EUR", "USD", "XOF", "GBP", "JPY", "CAD", "CNY", "CHF", "AUD", "BRL", "INR"]

# Menu de navigation (dans la sidebar)
onglet = st.sidebar.radio("📋 Menu", ["Convertir", "Historique"])

# === Onglet 1 : Conversion ===
if onglet == "Convertir":
    col1, col2 = st.columns(2)
    with col1:
        source = st.selectbox("Devise source", options=devises_disponibles, index=0)
    with col2:
        cible = st.selectbox("Devise cible", options=devises_disponibles, index=1)

    montant = st.number_input("Montant à convertir", min_value=0.0, value=1.0)

    if st.button("Convertir"):
        url_source = f"https://open.er-api.com/v6/latest/{source}"
        url_cible = f"https://open.er-api.com/v6/latest/{cible}"

        try:
            taux_source = requests.get(url_source).json()["rates"].get(cible)
            taux_inverse = requests.get(url_cible).json()["rates"].get(source)
        except:
            taux_source, taux_inverse = None, None

        if taux_source and taux_inverse:
            resultat = montant * taux_source
            inverse_resultat = montant * taux_inverse

            st.success(f"{montant} {source} = {resultat:.2f} {cible}")
            st.info(f"🔁 Inverse : {montant} {cible} = {inverse_resultat:.2f} {source}")

            # Enregistrement dans l'historique
            with open("historique.csv", mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    source,
                    cible,
                    montant,
                    taux_source,
                    resultat
                ])
        else:
            st.error("Erreur lors de la conversion. Vérifie les devises.")

# === Onglet 2 : Historique ===
else:
    st.subheader("🕓 Historique des conversions")
    try:
        df = pd.read_csv("historique.csv", names=["Date", "Devise source", "Devise cible", "Montant", "Taux", "Résultat"])
        st.dataframe(df[::-1], use_container_width=True)  # Affiche les lignes les plus récentes en haut
    except FileNotFoundError:
        st.warning("Aucune conversion enregistrée pour l’instant.")


st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>© 2025 – Créé par Ibrahim DABRE</div>", unsafe_allow_html=True)
