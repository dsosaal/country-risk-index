from src.index_builder import main as run_index_builder
from src.visualizations import plot_risk_index

def main():
    print("Calculando el índice compuesto de riesgo país...")
    run_index_builder()
    
    print("Generando la visualización del índice...")
    plot_risk_index()
    
    print("Proceso completo: índice calculado y gráfico guardado.")

if __name__ == "__main__":
    main()

