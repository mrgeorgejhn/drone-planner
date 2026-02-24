import streamlit as st
import os

# Configuración de la página
st.set_page_config(page_title="Calculadora de Planeación de Vuelo - Univalle", page_icon="🛸")

# --- ENCABEZADO CON LOGO Y AUTORES ---
col_logo, col_titulo = st.columns([1, 4])

# Intentar cargar el logo desde la carpeta img
ruta_logo = os.path.join("img", "logo.png") # Asegúrate de que el nombre coincida (logo.png, logo.jpg, etc.)

with col_logo:
    if os.path.exists(ruta_logo):
        st.image(ruta_logo, width=120)
    else:
        st.error("Logo no encontrado en /img")

with col_titulo:
    st.title("Calculadora de Planeación de Vuelo")
    st.markdown("""
    **Autores:** *Profesor. Eduardo Peña Abadía* *Profesor. Jorge Hernán Navarro*
    """)

st.divider()

# --- BARRA LATERAL (Parámetros de entrada) ---
st.sidebar.header("Configuración")
area = st.sidebar.number_input("Área del terreno (Hectáreas)", min_value=0.1, value=5.0, step=0.5)
precision = st.sidebar.selectbox("Nivel de Precisión", ["Alta", "Buena"])

# --- LÓGICA DE DATOS (Basada en tus CSV) ---
params = {
    'Alta': {
        'alt': (60, 100), 'vel': (4, 7), 'dist_gcp': 250, 'perim': 10, 'sep_max': 15
    },
    'Buena': {
        'alt': (80, 120), 'vel': (4, 7), 'dist_gcp': 300, 'perim': 15, 'sep_max': 20
    }
}

p = params[precision]

# --- RESULTADOS ---
st.subheader(f"📍 Reporte para Precisión {precision}")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Altura (min-max)", f"{p['alt'][0]}m - {p['alt'][1]}m")
with c2:
    st.metric("Velocidad (min-max)", f"{p['vel'][0]} - {p['vel'][1]} m/s")
with c3:
    if area <= 5:
        puntos, distri = 5, "4 Periferia / 1 Centro"
    elif area <= 30:
        puntos, distri = 9, "8 Periferia / 1 Centro"
    else:
        puntos, distri = "Según distancia", "Cobertura Perimetral"
    st.metric("GCP Mínimos", puntos)

# --- DETALLES DE UBICACIÓN ---
st.markdown("### 🛠️ Especificaciones Técnicas")
st.write(f"**Distribución aconsejada:** {distri}")
st.write(f"**Distancia al perímetro:** {p['perim']} metros.")
st.write(f"**Distancia máxima entre puntos de control:** {p['dist_gcp']} metros.")

if area > 30:
    st.warning(f"⚠️ Nota para terrenos grandes: La separación perimetral no debe sobrepasar los {p['sep_max']}m.")

st.info("Nota: Los terrenos medidos con parámetros distintos a estos corren el riesgo de perder precisión en área y alturas.")

# --- PIE DE PÁGINA ---
st.divider()
st.caption("Investigación sobre parámetros de vuelo en zona plana - Universidad del Valle.")