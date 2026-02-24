import streamlit as st
import os
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Calculadora Pro - Univalle", page_icon="🛸", layout="wide")

# --- ESTILOS ---
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
col_logo, col_titulo = st.columns([1, 4])

# Intentamos cargar el logo (asegúrate que el archivo esté en /img)
ruta_logo = os.path.join("img", "logo.png") 

with col_logo:
    if os.path.exists(ruta_logo):
        st.image(ruta_logo, width=150)
    else:
        st.warning("⚠️ Sube el logo a img/logo.png")

with col_titulo:
    st.title("Calculadora de Planeación de Vuelo")
    st.markdown("""
    **Investigadores:**
    * **Profesor.** Eduardo Peña Abadía
    * **Profesor.** Jorge Hernán Navarro
    
    *Universidad del Valle - Facultad de Ingeniería*
    """)

st.divider()

# --- INPUTS ---
with st.sidebar:
    st.header("⚙️ Parámetros del Proyecto")
    area_ha = st.number_input("Área del terreno (Ha)", min_value=0.1, value=5.0, step=1.0)
    precision = st.selectbox("Nivel de Precisión Requerido", ["Alta", "Buena"])
    st.info("Esta herramienta calcula la altura, velocidad y distribución de GCPs en zona plana.")

# --- LÓGICA TÉCNICA ---
params = {
    'Alta': {
        'alt': (60, 100), 'vel': (4, 7), 'dist_gcp': 250, 'perim': 10, 'sep_max': 15
    },
    'Buena': {
        'alt': (80, 120), 'vel': (4, 7), 'dist_gcp': 300, 'perim': 15, 'sep_max': 20
    }
}
p = params[precision]

# --- RESULTADOS PRINCIPALES ---
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Altura de Vuelo", f"{p['alt'][0]}-{p['alt'][1]} m")
with c2:
    st.metric("Velocidad", f"{p['vel'][0]}-{p['vel'][1]} m/s")

# Lógica de distribución de puntos
if area_ha <= 5:
    n_puntos, desc_puntos, pts_coords = 5, "4 Perif. / 1 Centro", "5ha"
elif area_ha <= 30:
    n_puntos, desc_puntos, pts_coords = 9, "8 Perif. / 1 Centro", "30ha"
else:
    # Estimación para terrenos grandes
    lado_m = np.sqrt(area_ha * 10000)
    perim_m = lado_m * 4
    estimado = int(np.ceil(perim_m / p['dist_gcp'])) + 1
    n_puntos, desc_puntos, pts_coords = f"+{estimado}", "Distribución según distancia", "grande"

with c3:
    st.metric("GCP Mínimos", n_puntos)
with c4:
    st.metric("Dist. Máx GCP", f"{p['dist_gcp']} m")

# --- GRÁFICO DE DISTRIBUCIÓN (Periferia vs Centro) ---
st.subheader("🗺️ Esquema Sugerido de Puntos de Control (GCP)")

def generar_grafico(tipo):
    fig, ax = plt.subplots(figsize=(6, 6))
    # Dibujar el terreno (cuadrado)
    ax.add_patch(plt.Rectangle((0, 0), 100, 100, fill=False, color='black', linestyle='--', label='Límite Terreno'))
    
    if tipo == "5ha":
        # 4 esquinas (periferia) y 1 centro
        px = [10, 90, 10, 90, 50]
        py = [10, 10, 90, 90, 50]
        labels = ['P', 'P', 'P', 'P', 'C']
    elif tipo == "30ha":
        # 8 periferia y 1 centro
        px = [10, 50, 90, 10, 90, 10, 50, 90, 50]
        py = [10, 10, 10, 50, 50, 90, 90, 90, 50]
        labels = ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'C']
    else:
        # Esquema para terrenos grandes (muestra el concepto)
        px = [10, 35, 65, 90, 90, 90, 65, 35, 10, 10, 40, 60]
        py = [10, 10, 10, 10, 50, 90, 90, 90, 90, 50, 40, 60]
        labels = ['P']*10 + ['C']*2

    # Graficar Periferia
    ax.scatter([x for i, x in enumerate(px) if labels[i] == 'P'], 
               [y for i, y in enumerate(py) if labels[i] == 'P'], 
               color='#d62728', s=150, label='Periferia (P)', zorder=5)
    
    # Graficar Centro
    ax.scatter([x for i, x in enumerate(px) if labels[i] == 'C'], 
               [y for i, y in enumerate(py) if labels[i] == 'C'], 
               color='#1f77b4', s=150, label='Centro (C)', zorder=5)

    ax.set_xlim(-10, 110)
    ax.set_ylim(-10, 110)
    ax.set_aspect('equal')
    ax.legend(loc='upper right')
    ax.set_title("Ubicación conceptual de los puntos")
    plt.axis('off')
    return fig

col_graph, col_info = st.columns([2, 1])

with col_graph:
    st.pyplot(generar_grafico(pts_coords))

with col_info:
    st.markdown("### 📋 Notas de Campo")
    st.write(f"**Distribución:** {desc_puntos}")
    st.write(f"**Distancia al borde:** {p['perim']}m aprox.")
    if area_ha > 30:
        st.warning(f"Terreno extenso: Mantener separación máxima de {p['dist_gcp']}m entre puntos y no exceder {p['sep_max']}m del perímetro.")

st.divider()
st.info("⚠️ Los terrenos medidos con parámetros distintos a estos corren el riesgo de perder precisión en área y alturas.")