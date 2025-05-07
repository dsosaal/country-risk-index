import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ===========================
# Configuración del Dashboard
# ===========================
st.set_page_config(page_title="Country Risk Dashboard", layout="wide")

st.title("Country Risk Index Dashboard")
st.markdown("Visualiza la evolución del riesgo país por indicador y año.")

# ===========================
# Cargar Datos
# ===========================
@st.cache
def load_data():
    try:
        df = pd.read_csv("data/processed/historical_index.csv")
        return df
    except FileNotFoundError:
        st.error("❌ No se encontró el archivo historical_index.csv. Verifica la ruta.")
        return pd.DataFrame()

df = load_data()

# Verificar que haya datos
if df.empty:
    st.error("No hay datos disponibles en historical_index.csv.")
else:
    # ===========================
    # Filtros Interactivos
    # ===========================
    countries = df['country'].unique().tolist()
    indicators = df['indicator'].unique().tolist()
    years = sorted(df['year'].unique())

    selected_countries = st.multiselect("Selecciona Países", countries, default=countries)
    selected_indicators = st.multiselect("Selecciona Indicadores", indicators, default=indicators)
    selected_years = st.slider("Selecciona el Rango de Años", 
                               min_value=min(years), 
                               max_value=max(years), 
                               value=(min(years), max(years)))

    # Filtrar Datos
    df_filtered = df[
        (df['country'].isin(selected_countries)) &
        (df['indicator'].isin(selected_indicators)) &
        (df['year'].between(selected_years[0], selected_years[1]))
    ]

    # ===========================
    # Visualización
    # ===========================
    st.subheader("Evolución del Índice de Riesgo País")

    if not df_filtered.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(
            data=df_filtered,
            x="year",
            y="value",
            hue="country",
            style="indicator",
            markers=True,
            ax=ax
        )
        plt.title("Evolución del Índice de Riesgo País por Año")
        plt.xlabel("Año")
        plt.ylabel("Valor del Indicador")
        plt.grid(True, linestyle="--", alpha=0.6)
        st.pyplot(fig)
    else:
        st.warning("No hay datos para la selección actual. Ajusta los filtros.")
