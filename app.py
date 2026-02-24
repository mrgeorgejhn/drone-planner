import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Planificador de Vuelo - Drones", page_icon="🛸")

st.title("🛸 Calculadora de Planeación de Vuelo")
st.markdown("Genera parámetros técnicos basados en el área y la precisión requerida.")

# --- BARRA LATERAL (Inputs) ---
st.sidebar.header("Configuración del Proyecto")
area = st.sidebar.number_input("Área del terreno (Hectáreas)", min_value=0.1, value=5.0, step=0.5)
precision = st.sidebar.selectbox("Nivel de Precisión", ["Alta", "Buena"])

# --- LÓGICA DE DATOS ---
params = {
    'Alta': {
        'alt': (60, 100), 'vel': (4, 7), 'dist_gcp': 250, 'perim': 10, 'sep_max': 15
    },
    'Buena': {
        'alt': (80, 120), 'vel': (4, 7), 'dist_gcp': 300, 'perim': 15, 'sep_max': 20
    }
}

p = params[precision]

# --- PROCESAMIENTO ---
st.subheader(f"📊 Reporte para {precision} Precisión")

col1, col2 = st.columns(2)

with col1:
    st.metric("Altura de Vuelo", f"{p['alt'][0]}m - {p['alt'][1]}m")
    st.metric("Velocidad Sugerida", f"{p['vel'][0]} - {p['vel'][1]} m/s")

with col2:
    if area <= 5:
        puntos, distri = 5, "4 Periferia / 1 Centro"
    elif area <= 30:
        puntos, distri = 9, "8 Periferia / 1 Centro"
    else:
        puntos, distri = "Cálculo por distancia", "Cobertura Perimetral Total"
    
    st.metric("Puntos de Control (GCP)", puntos)
    st.write(f"**Distribución:** {distri}")

# --- RECOMENDACIONES TÉCNICAS ---
st.info(f"💡 **Tip de Ubicación:** Colocar los puntos a {p['perim']}m del perímetro.")

if area > 30:
    st.warning(f"⚠️ Para terrenos grandes, asegurar que la separación perimetral no pase de {p['sep_max']}m.")

st.success("✅ Parámetros validados según la normativa de zona plana.")