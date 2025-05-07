import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_risk_index(csv_path="data/processed/country_risk_score.csv",
                    output_path="outputs/reports/country_risk_score.png"):
    # Cargar y ordenar los datos
    df = pd.read_csv(csv_path)
    df = df.sort_values("risk_score", ascending=False).reset_index(drop=True)

    # Crear paleta de colores: más oscuro = más riesgo
    colors = sns.color_palette("Reds", n_colors=len(df))
    colors = colors[::-1]  # invertir para que más alto = más oscuro
    color_dict = dict(zip(df['country'], colors))

    # Crear gráfica
    plt.figure(figsize=(10, 6))
    bars = plt.barh(
        y=df['country'],
        width=df['risk_score'],
        color=[color_dict[c] for c in df['country']]
    )

    # Agregar etiquetas
    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"{df['risk_score'][i]:.1f}", va='center', fontsize=10)

    plt.title("Índice Compuesto de Riesgo País\n(0 = menor riesgo, 100 = mayor riesgo)")
    plt.xlabel("Riesgo País (Score)")
    plt.xlim(0, 100)
    plt.tight_layout()
    plt.gca().invert_yaxis()

    # Crear carpeta si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Guardar imagen
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Gráfica guardada en {output_path}")


# Ejecución directa (opcional)
if __name__ == "__main__":
    plot_risk_index()
