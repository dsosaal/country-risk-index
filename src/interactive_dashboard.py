import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# ===========================
# Configuración del Dashboard
# ===========================
st.set_page_config(page_title="Country Risk Dashboard", layout="wide")

st.title("Country Risk Index Dashboard")
st.markdown("Visualiza la evolución del índice de riesgo país en un mapa interactivo.")

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
    selected_year = st.selectbox("Selecciona el Año", years, index=len(years) - 1)

    # Filtrar los datos para el año seleccionado
    df_filtered = df[df['year'] == selected_year]

    # ===========================
    # Cargar el shapefile (mapa de países)
    # ===========================
    @st.cache
    def load_geojson():
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        world = world[(world.continent == "North America") | (world.continent == "South America")]
        world = world[world.name.isin(["Brazil", "Colombia", "Mexico", "Peru"])]
        return world
    
    world = load_geojson()
    world = world.merge(df_filtered, left_on="name", right_on="country", how="left")

    # ===========================
    # Crear el mapa interactivo
    # ===========================
    m = folium.Map(location=[15, -80], zoom_start=4, tiles="cartodb positron")

    for _, row in world.iterrows():
        color = "green" if pd.isna(row['risk_score']) else folium.colors.linear.YlOrRd_09.scale(0, 100)(row['risk_score'])
        folium.GeoJson(
            data=row['geometry'],
            style_function=lambda x, color=color: {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.6,
            },
            tooltip=folium.Tooltip(f"{row['country']}: {row['risk_score']:.2f}" if not pd.isna(row['risk_score']) else "Sin datos")
        ).add_to(m)

    st.subheader(f"Mapa Interactivo del Índice de Riesgo País - {selected_year}")
    st_folium(m, width=800, height=500)
