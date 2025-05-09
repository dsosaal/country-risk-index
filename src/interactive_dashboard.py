import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
from fpdf import FPDF  
import base64
import matplotlib.pyplot as plt
import io
import os
import xlsxwriter





# ===========================
# Configuración del Dashboard
# ===========================
st.set_page_config(page_title="Country Risk Dashboard", layout="wide")

st.title("Country Risk Index Dashboard")
st.markdown("This interactive map displays the Country Risk Index, a measure that evaluates the economic risk level of each country based on factors such as inflation, GDP growth, current account balance, and external debt. Darker colors indicate higher risk, while lighter colors represent lower risk. Select a year to see how the risk has evolved across countries.")

# ===========================
# Cargar Datos
# ===========================
@st.cache_data
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
    selected_year = st.selectbox("Choose a year for the map", years, index=len(years) - 1)

    # Filtrar los datos para el año seleccionado
    df_filtered = df[df['year'] == selected_year]

    # ===========================
    # Mapa Interactivo (Plotly Choropleth)
    # ===========================
    st.subheader(f"Interactive Country Risk Index Map. - {selected_year}")

    fig_map = px.choropleth(
        df_filtered,
        locations="country",
        locationmode="country names",
        color="risk_score",
        hover_name="country",
        color_continuous_scale="RdYlGn_r",
        range_color=(0, 100),
        title=f"Country Risk Index - {selected_year}"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # ===========================
    # Gráfico Comparativo de Indicadores
    # ===========================
    st.subheader("Indicator comparison")

    countries = df['country'].unique().tolist()
    selected_countries = st.multiselect("Choose countries.", countries, default=countries)
    df_filtered_countries = df[df['country'].isin(selected_countries)]

    fig_line = px.line(
        df_filtered_countries,
        x="year",
        y="risk_score",
        color="country",
        title="Country risk index trends",
        labels={"risk_score": "Country risk"}
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # ===========================
    # Resumen automático
    # ===========================
    st.subheader("Summary")
    
    highest_risk = df_filtered.loc[df_filtered['risk_score'].idxmax()]
    lowest_risk = df_filtered.loc[df_filtered['risk_score'].idxmin()]

    analysis_text = (
        f"In the year {selected_year}, the country with the highest risk was {highest_risk['country']} "
        f"with a score of {highest_risk['risk_score']:.2f}.\n\n"
        f"In the same year, the country with the lowest risk was {lowest_risk['country']} "
        f"with a score of {lowest_risk['risk_score']:.2f}."
    )

    st.markdown(analysis_text)

    # ===========================
    # Exportar a Excel (Descarga directa)
    # ===========================
    st.subheader("Export data to Excel")

    # Crear un buffer en memoria para el archivo Excel
    buffer = io.BytesIO()

    # Crear el archivo Excel en el buffer
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Hoja 1: Datos de análisis
        df_filtered.to_excel(writer, sheet_name="Data", index=False)
        
        # Hoja 2: Gráficos (capturas)
        workbook = writer.book
        worksheet = workbook.add_worksheet("Charts")
        writer.sheets["Charts"] = worksheet

        # Exportar el mapa y el gráfico como imágenes
        map_img_path = "outputs/reports/map_image.png"
        line_img_path = "outputs/reports/line_image.png"
        
        # Guardar imágenes usando kaleido
        fig_map.write_image(map_img_path, engine="kaleido")
        fig_line.write_image(line_img_path, engine="kaleido")

        # Insertar las imágenes en la hoja de gráficos
        worksheet.insert_image("B2", map_img_path)
        worksheet.insert_image("B22", line_img_path)

    # Colocar el puntero del buffer al inicio
    buffer.seek(0)

    # Descargar el archivo directamente (un solo botón)
    st.download_button(
        label="Download",
        data=buffer,
        file_name="Country_Risk_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


