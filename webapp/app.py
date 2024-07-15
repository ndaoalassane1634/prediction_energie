# app.py
import streamlit as st
from pages.data_analysis import show_data_analysis
from pages.predictioncopy import show_prediction_page
from scripts.data_cleaning import clean_data
import warnings
warnings.filterwarnings('ignore')
def wide_space_default():
    st.set_page_config(layout='wide')


wide_space_default()
logo_path = './assets/logo_en.PNG'
st.image(logo_path, width=100)  
st.subheader("Tableau de bord d'analyse énergétique")

selected_tab = st.sidebar.selectbox(
    "Sélectionner une option :",
    ["Accueil", "Analyse des données", "Prédictions"]
)

def load_data():
    data_file = 'data/data.csv'
    df = clean_data(data_file)
    return df

df = load_data()

if selected_tab == "Accueil":
    st.subheader("Agilité, Précision et Profits")
    st.write("Sélectionnez une option dans la barre latérale.")
elif selected_tab == "Analyse des données":
    show_data_analysis()
elif selected_tab == "Prédictions":
    show_prediction_page()
