import requests

import pandas as pd
import streamlit as st


# Configuración de la página y API
st.set_page_config(page_title="Steam Sales Prediction", layout="wide")
API_URL = "http://api:8000"


def predictions_page():
    st.header("🎮 Predicciones de ventas en Steam")
    col1, col2, col3 = st.columns(3)

    day_of_week = col1.radio(
        "Selecciona un día de la semana:",
        options=[
            ("Lunes", 1),
            ("Martes", 2), 
            ("Miércoles", 3),
            ("Jueves", 4),
            ("Viernes", 5),
            ("Sábado", 6),
            ("Domingo", 7)
        ],
        format_func=lambda x: x[0],
        help="Selecciona el día de la semana",
        index=0
    )
    
    # Extraer solo el valor numérico
    day_of_week = day_of_week[1]

    season = col2.radio(
        "Selecciona una estación:",
        options=[
            ("Verano", 1),
            ("Otoño", 2), 
            ("Invierno", 3),
            ("Primavera", 4)
        ],
        format_func=lambda x: x[0],
        help="Selecciona la estación del año",
        index=0
    )
    
    # Extraer solo el valor numérico
    season = season[1]
    
    holiday = col3.checkbox("Feriado")
    st.write("---")
    if st.button("Obtener predicción"):
        payload = {
            "DayOfWeek": int(day_of_week),
            "Season": int(season),
            "Holiday": int(holiday)
        }
        try:
            resp = requests.post(f"{API_URL}/predict/", json=payload)
            resp.raise_for_status()
            ventas = resp.json().get("prediction")
            st.success(f"Ventas esperadas: ${ventas:.2f}")
        except Exception as e:
            st.error(f"Error al predecir: {e}")

def registry_page():
    st.header("📜 Registro de predicciones")
    try:
        resp = requests.get(f"{API_URL}/registry/")
        resp.raise_for_status()
        df = pd.DataFrame(resp.json())
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # Ordenar por timestamp descendente
        df = df.sort_values(by="timestamp", ascending=False)

        # Quitar el id
        df = df.drop(columns=["id"])

        # Mostrar headers en español
        df.columns = [col.replace("timestamp", "Fecha") for col in df.columns]
        df.columns = [col.replace("prediction", "Ventas esperadas") for col in df.columns]
        
        # Expandir la columna input_data
        df = df.join(pd.json_normalize(df["input_data"]))
        df = df.drop(columns=["input_data"])
        df = df.rename(columns={
            "DayOfWeek": "Día de la semana",
            "Season": "Estación",
            "Holiday": "Feriado",
        })

        # Formatear valores booleanos como "Sí" o "No"
        df["Feriado"] = df["Feriado"].map({0: "No", 1: "Sí"})

        # Formatear valores numéricos
        df["Ventas esperadas"] = df["Ventas esperadas"].map(lambda x: f"${x:.2f}")

        # Formatear numero de día de la semana y estación
        df["Día de la semana"] = df["Día de la semana"].map({1: "Lunes", 2: "Martes", 3: "Miércoles", 4: "Jueves", 5: "Viernes", 6: "Sábado", 7: "Domingo"})
        df["Estación"] = df["Estación"].map({1: "Verano", 2: "Otoño", 3: "Invierno", 4: "Primavera"})

        # Reordenar columnas
        df = df[["Fecha", "Ventas esperadas", "Día de la semana", "Estación", "Feriado"]]

        st.dataframe(df)
    except Exception as e:
        if (e.args[0] == "timestamp"):
            st.info("No existen registros de predicciones actualmente.")
        else:
            st.error(f"No se pudo cargar ningún registro: {e}")

# Definición de páginas usando st.navigation (Streamlit 1.45)
pages = [
    st.Page(predictions_page, title="🎮 Predicciones"),
    st.Page(registry_page,    title="📜 Registro"),
]

def main():
    selected_page = st.navigation(pages, position="top", expanded=True)
    selected_page.run()

if __name__ == "__main__":
    main()
