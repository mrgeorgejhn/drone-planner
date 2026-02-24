import streamlit as st
import os
import matplotlib.pyplot as plt
import numpy as np

# Configuración de página con Layout ancho
st.set_page_config(page_title="Calculadora Univalle", page_icon="🛸", layout="wide")

# --- CSS PERSONALIZADO PARA MEJORAR VISIBILIDAD ---
st.markdown("""
    <style>
    /* Forzar fondo claro en las métricas para que se vea el texto */
    [data-testid="stMetricValue"] {
        color: #d32f2f !important;
        font-size: 2rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #333333 !important;
        font-weight: bold !important;
    }
    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
col_logo, col_titulo = st.columns([1, 3])

ruta_logo = os.path.join("img", "logo.png")
with col_logo:
    if os.path.exists(ruta_logo):
        st.image(ruta_logo, width=150)
    else:
        st.info("Logo en /img/logo.png")

with col_titulo:
    st.title("Calculadora de Planeación de Vuelo")
    st.markdown(f"""
    **Investigadores:**
    Profesor. Eduardo Peña Abadía | Profesor. Jorge Hernán Navarro
    
    *Facultad de Ingeniería - Universidad del Valle*
    """)

st.divider()

# --- INPUTS ---
with st.sidebar:
    st.header("⚙️ Parámetros")
    area_ha = st.number_input("Área del terreno (Ha)", min_value=0.1, value=5.0, step=1.0)
    precision = st.selectbox("Nivel de Precisión", ["Alta", "Buena"])
    st.divider()
    st.caption("Investigación: Parámetros en zona plana.")

# --- LÓGICA ---
params = {
    'Alta': {'alt': (60, 100), 'vel': (4, 7), 'dist_gcp': 250, 'perim': 10, 'sep_max': 15},
    'Buena': {'alt': (80, 120), 'vel': (4, 7), 'dist_gcp': 300, 'perim': 15, 'sep_max': 20}
}
p = params[precision]

# --- BLOQUE DE INFORMACIÓN GENERADA ---
st.subheader(f"📊 Información Generada (Precisión {precision})")

# Usamos contenedores con fondo para asegurar visibilidad
cont = st.container()
with cont:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Altura Vuelo", f"{p['alt'][0]}-{p['alt'][1]} m")
    c2.metric("Velocidad", f"{p['vel'][0]}-{p['vel'][1]} m/s")
    
    if area_ha <= 5:
        n_puntos, desc_puntos, modo = 5, "4 Perif. / 1 Centro", "5ha"
    elif area_ha <= 30:
        n_puntos, desc_puntos, modo = 9, "8 Perif. / 1 Centro", "30ha"
    else:
        lado = np.sqrt(area_ha * 10000)
        estimado = int(np.ceil((lado * 4) / p['dist_gcp'])) + 1
        n_puntos, desc_puntos, modo = f"+{estimado}", "Red Perimetral", "grande"
        
    c3.metric("GCP Mínimos", n_puntos)
    c4.metric("Dist. Máx GCP", f"{p['dist_gcp']} m")

# --- GRÁFICO ---
st.markdown("### 🗺️ Esquema de Distribución Sugerido")

def draw_plot(modo):
    # Ajuste de estilo para que se vea bien en cualquier tema
    fig, ax = plt.subplots(figsize=(7, 5), facecolor='#fdfdfd')
    ax.set_facecolor('#fdfdfd')
    
    # El terreno
    ax.add_patch(plt.Rectangle((0, 0), 100, 100, fill=True, color='#eeeeee', alpha=0.5, label='Área Terreno'))
    ax.add_patch(plt.Rectangle((0, 0), 100, 100, fill=False, color='#cc0000', linewidth=2))
    
    if modo == "5ha":
        px, py = [10, 90, 10, 90, 50], [10, 10, 90, 90, 50]
    elif modo == "30ha":
        px = [10, 50, 90, 10, 90, 10, 50, 90, 50]
        py = [10, 10, 10, 50, 50, 90, 90, 90, 50]
    else:
        px = [10, 35, 65, 90, 90, 90, 65, 35, 10, 10, 50]
        py = [10, 10, 10, 10, 50, 90, 90, 90, 90, 50, 50]

    ax.scatter(px[:-1], py[:-1], color='red', s=200, label='Periferia', edgecolors='black', zorder=5)
    ax.scatter(px[-1], py[-1], color='blue', s=250, marker='X', label='Centro', zorder=5)

    for i, (x, y) in enumerate(zip(px, py)):
        ax.text(x+2, y+2, f"GCP{i+1}", fontsize=10, fontweight='bold')

    ax.set_xlim(-15, 115)
    ax.set_ylim(-15, 115)
    ax.axis('off')
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=2)
    return fig

col_g, col_t = st.columns([2, 1])
with col_g:
    st.pyplot(draw_plot(modo))

with col_t:
    st.info(f"**Recomendación de Ubicación:**\n\nLos puntos rojos deben situarse a **{p['perim']}m** del borde interno del predio.")
    if area_ha > 30:
        st.warning(f"**Nota Terreno Grande:** Asegurar que la separación entre puntos no exceda los {p['dist_gcp']}m.")

st.divider()
st.caption("⚠️ Nota: El incumplimiento de estos parámetros afecta la precisión del modelo final.")