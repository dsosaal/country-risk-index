import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd



# ===========================
# Configuración del Dashboard
# ===========================
st.set_page_config(page_title="Country Risk Dashboard", layout="wide")

st.title("Country Risk Index Dashboard")
st.markdown("Visualiza la evolución del índice de riesgo país en un mapa interactivo y gráfico comparativo.")

# ===========================
# Cargar Datos
# ===========================
@st.cache
def load_data():
    df = pd.read_csv("data/processed/historical_risk_index.csv")
    return df

df = load_data()

# Verificar que haya datos
if df.empty:
    st.error("No hay datos disponibles.")
else:
    # ===========================
    # Filtros Interactivos
    # ===========================
    years = sorted(df['year'].unique())
    selected_year = st.selectbox("Selecciona el año para el mapa", years, index=len(years) - 1)

    # Filtrar los datos para el año seleccionado
    df_filtered = df[df['year'] == selected_year]

    # ===========================
    # Mapa Interactivo (Plotly Choropleth)
    # ===========================
    st.subheader(f"Mapa interactivo del Índice de Riesgo País - {selected_year}")

    fig_map = px.choropleth(
        df_filtered,
        locations="country",
        locationmode="country names",
        color="risk_score",
        hover_name="country",
        color_continuous_scale="RdYlGn_r",
        range_color=(0, 100),
        title=f"Índice de Riesgo País - {selected_year}"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # ===========================
    # Gráfico Comparativo de Indicadores
    # ===========================
    st.subheader("Comparación de indicadores")

    countries = df['country'].unique().tolist()
    selected_countries = st.multiselect("Selecciona países", countries, default=countries)
    df_filtered_countries = df[df['country'].isin(selected_countries)]

    fig_line = px.line(
        df_filtered_countries,
        x="year",
        y="risk_score",
        color="country",
        title="Evolución del Índice de Riesgo País",
        labels={"risk_score": "Riesgo País"}
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # ===========================
    # Análisis Automático
    # ===========================
    st.subheader("Descripcion basica del Índice de Riesgo País")
    
    highest_risk = df_filtered.loc[df_filtered['risk_score'].idxmax()]
    lowest_risk = df_filtered.loc[df_filtered['risk_score'].idxmin()]

    st.markdown(f"En el año **{selected_year}**, el país con mayor riesgo fue **{highest_risk['country']}** con un índice de **{highest_risk['risk_score']:.2f}**.")
    st.markdown(f"En el mismo año, el país con menor riesgo fue **{lowest_risk['country']}** con un índice de **{lowest_risk['risk_score']:.2f}**.")
