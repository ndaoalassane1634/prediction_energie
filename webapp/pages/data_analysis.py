# pages/data_analysis.py
from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from scripts.data_cleaning import clean_data
import numpy as np
import seaborn as sns
def get_log_color(value, min_value, max_value):
    
    log_min = np.log(min_value + 1)
    log_max = np.log(max_value + 1)
    log_value = np.log(value + 1)

    norm_value = (log_value - log_min) / (log_max - log_min)

    r = int(255 * norm_value)
    g = int(255 * (1 - norm_value))
    b = 0

    return f'#{r:02x}{g:02x}{b:02x}'
def plot_total_ghg_emissions_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['TotalGHGEmissions'], kde=True, bins=30, color='blue')
    plt.title('Distribution des émissions totales de GES')
    plt.xlabel('Total GHG Emissions')
    plt.ylabel('Nombre de bâtiments')
    st.pyplot()

def plot_scatterplot(df):
    st.set_option('deprecation.showPyplotGlobalUse', False)

    plt.figure(figsize=(10, 6))
    plt.scatter(df.index, df['SiteEnergyUse(kBtu)'], alpha=0.5)
    plt.title('Distribution de la consommation énergétique')
    plt.xlabel('Index')
    plt.ylabel('Site Energy Use (kBtu)')
    st.pyplot()

def plot_year_built_distribution(df):

    plt.figure(figsize=(10, 6))

    # Création des intervalles d'années regroupées par 5
    bins = range(df['YearBuilt'].min(), df['YearBuilt'].max() + 6, 5)
    labels = [f"{b}-{b+4}" for b in bins[:-1]]
    df['YearBuiltGroup'] = pd.cut(df['YearBuilt'], bins=bins, labels=labels, right=False)

    # Calcul du nombre de bâtiments dans chaque groupe d'années
    counts = df['YearBuiltGroup'].value_counts().sort_index()

    # Création du barplot
    counts.plot(kind='bar')
    plt.title('Distribution selon l\'année de construction (groupée par intervalles de 5)')
    plt.xlabel('Années de construction')
    plt.ylabel('Nombre de bâtiments')
    plt.xticks(rotation=45)
    st.pyplot()

def show_data_analysis():
    data_file = 'data/data.csv'

    df = clean_data(data_file)

    col1, col2, col3 = st.columns([2, 2, 2])  
    with col1:
        selected_category = st.selectbox("Sélectionner une catégorie :", ['BuildingType', 'LargestPropertyUseType'])

    with col2:
        if selected_category == 'BuildingType':
            categories = df['BuildingType'].unique()
        elif selected_category == 'LargestPropertyUseType':
            categories = df['LargestPropertyUseType'].unique()
        selected_category_values = st.multiselect(f"Sélectionner les valeurs de {selected_category} :", categories)

    with col3:
        neighborhoods = df['Neighborhood'].unique() 
        selected_neighborhood = st.selectbox("Sélectionner un quartier :", neighborhoods)

    if len(selected_category_values) > 0:
        filtered_df = df[df[selected_category].isin(selected_category_values)]
    else:
        filtered_df = df

    filtered_df = filtered_df[filtered_df['Neighborhood'] == selected_neighborhood]

    col4, col5 = st.columns(2)

    with col4:
        plot_scatterplot(filtered_df)

    with col5:
        m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)

        min_value = filtered_df['SiteEnergyUse(kBtu)'].min()
        max_value = filtered_df['SiteEnergyUse(kBtu)'].max()

        for idx, row in filtered_df.iterrows():
            color = get_log_color(row['SiteEnergyUse(kBtu)'], min_value, max_value)
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=5,
                popup=f"Consommation énergétique : {row['SiteEnergyUse(kBtu)']}",
                color=color,
                fill=True,
                fill_color=color
            ).add_to(m)

        folium_static(m)

    col6, col7 = st.columns(2)
    with col6:
        plot_year_built_distribution(filtered_df)



    median_consumption = filtered_df['SiteEnergyUse(kBtu)'].median()
    total_consumption = filtered_df['SiteEnergyUse(kBtu)'].sum()
    effectif_total = filtered_df['SiteEnergyUse(kBtu)'].shape[0]


    with col7:
        st.metric("Consommation médiane", f"{median_consumption:.2f} kBtu")
        st.metric("Consommation totale", f"{total_consumption:.2f} kBtu")
        st.metric("Effectif", f"{effectif_total:.2f} ")

    col8, col9 = st.columns(2)
    with col8:
        plt.figure(figsize=(8, 6))
        plt.hist(filtered_df['PropertyGFATotal'], bins=20, alpha=0.7)
        plt.title('Distribution du PropertyGFATotal')
        plt.xlabel('PropertyGFATotal')
        plt.ylabel('Fréquence')
        st.pyplot()
    with col9:
        plot_total_ghg_emissions_distribution(filtered_df)
