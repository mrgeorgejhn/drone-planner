import streamlit as st
import os

# Configuración de la página
st.set_page_config(page_title="Calculadora de Planeación de Vuelo - Univalle", page_icon="🛸")

# --- ENCABEZADO CON LOGO Y AUTORES ---
col_logo, col_titulo = st.columns([1, 4])

# Ruta del logo (ajusta el nombre del archivo si es necesario, p.ej. logo_univalle.png)
ruta_logo = os.path.join("img", "logo.png") 

with col_logo:
    if os.path.exists(ruta_logo):
        st.image(ruta_logo, width=120)
    else:
        st.error("Logo no encontrado")

with col_titulo:
    st.title("Calculadora de Planeación de Vuelo")
    st.markdown("""
    **Autores:** *Profesor. Eduardo Peña Abadía* *Profesor. Jorge Hernán Navarro*
    """)

st.divider()

# --- BARRA LATERAL (Entradas sin límite de área) ---
st.sidebar.header("Configuración de Vuelo")
area = st.sidebar.number_input("Área del terreno (Hectáreas)", min_value=0.1, value=5.0, step=1.0)
precision = st.sidebar.selectbox("Nivel de Precisión", ["Alta", "Buena"])

# --- LÓGICA DE DATOS SEGÚN EXCEL ---
params = {
    'Alta': {
        'alt': (60, 100), 'vel': (4, 7), 'dist_gcp': 250, 'perim': 10, 'sep_max': 15
    },
    'Buena': {
        'alt': (80, 120), 'vel': (4, 7), 'dist_gcp': 300, 'perim': 15, 'sep_max': 20
    }
}

p = params[precision]

# --- CÁLCULOS DINÁMICOS ---
st.subheader(f"📍 Reporte Técnico: Precisión {precision}")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Altura (min-max)", f"{p['alt'][0]}m - {p['alt'][1]}m")
with c2:
    st.metric("Velocidad (min-max)", f"{p['vel'][0]} - {p['vel'][1]} m/s")
with c3:
    # Lógica de GCP escalable
    if area <= 5:
        puntos, distri = "5", "4 Periferia / 1 Centro"
    elif area <= 30:
        puntos, distri = "9", "8 Periferia / 1 Centro"
    else:
        # Para terrenos de 50 Ha o más según el Excel
        puntos, distri = "Cálculo según Distancia", "Cobertura Perimetral Total"

    st.metric("GCP Mínimos", puntos)

# --- ESPECIFICACIONES DE DISTRIBUCIÓN ---
st.markdown("### 🛠️ Especificaciones Técnicas de Campo")

col_a, col_b = st.columns(2)
with col_a:
    st.write(f"**Distancia Máxima entre GCP:** {p['dist_gcp']}m")
    st.write(f"**Ubicación con relación al perímetro:** {p['perim']}m")

with col_b:
    st.write(f"**Distribución:** {distri}")
    if area > 30:
        st.write(f"**Separación Perimetral Máxima:** {p['sep_max']}m")

# Mensajes de advertencia institucionales
if area > 30:
    st.warning(f"⚠️ **Atención:** Para terrenos grandes (>30-50 Ha), es crítico conservar el parámetro de distancia máxima ({p['dist_gcp']}m) y asegurar que la separación perimetral no sobrepase los {p['sep_max']}m.")

st.info("💡 *Nota:* Los terrenos medidos con parámetros distintos a los establecidos corren el riesgo de no contar con una buena precisión en área y alturas.")

# --- PIE DE PÁGINA ---
st.divider()
st.caption("Investigación sobre parámetros de vuelo en zona plana - Universidad del Valle.")