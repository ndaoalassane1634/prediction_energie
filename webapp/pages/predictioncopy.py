import streamlit as st
import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

def load_model():
    model_path = '/home/alou/cours/co2/webapp/model/model_pipelineenergy.joblib'
    with open(model_path, 'rb') as f:
        model = joblib.load(f)
    return model

def predict(model, df):
    features = df.drop(columns=['Log_SiteEnergyUse'], errors='ignore')
    predictions = model.predict(features)
    return predictions

def calculate_metrics(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return rmse, mae, r2

def show_prediction_page():
    st.title("Prédiction de la consommation énergétique")

    model = load_model()

    uploaded_file = st.file_uploader("Télécharger un fichier CSV", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        if 'Log_SiteEnergyUse' not in df.columns:
            st.error("Le fichier CSV doit contenir une colonne 'Log_SiteEnergyUse'")
            return
        df.dropna(subset=['Log_SiteEnergyUse'], inplace=True)

        df['PredictedLog_SiteEnergyUse'] = predict(model, df)

        if 'Log_SiteEnergyUse' in df:
            y_true = df['Log_SiteEnergyUse']
            y_pred = df['PredictedLog_SiteEnergyUse']
            rmse, mae, r2 = calculate_metrics(y_true, y_pred)

            col1, col2, col3 = st.columns(3)
            col1.metric("RMSE", f"{rmse:.2f}")
            col2.metric("MAE", f"{mae:.2f}")
            col3.metric("R²", f"{r2:.2f}")

        st.write("Aperçu des prédictions :")
        st.write(df.head())

        csv = df.to_csv(index=False)
        st.download_button(
            label="Télécharger les prédictions en CSV",
            data=csv,
            file_name='predictions.csv',
            mime='text/csv'
        )

show_prediction_page()
