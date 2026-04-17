import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# --- TRUCO DE IMPORTACIÓN SEGURA PARA EVITAR EL ERROR ROJO ---
try:
    from fpdf import FPDF
    PDF_DISPONIBLE = True
except ImportError:
    PDF_DISPONIBLE = False

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO NEGRO TOTAL
st.set_page_config(page_title="CRM OTORMÍN 2026", page_icon="🚗", layout="wide")

# Estilos CSS avanzados para ordenar la "deformidad"
st.markdown("""
    <style>
        /* Fondo negro total y tipografía */
        .stApp { background-color: #0B0E11; color: #E1E8ED; font-family: 'Segoe UI', sans-serif; }
        
        /* Sidebar ordenada */
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        
        /* Títulos en azul Otormín */
        h1, h2, h3 { color: #55acee !important; text-align: center; }
        
        /* Contenedor de Métricas: Fijo y centrado, no deformable */
        .metric-container {
            display: flex;
            justify-content: space-around;
            background-color: #1C2126;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #30363d;
            margin-bottom: 30px;
        }
        .metric-box { text-align: center; flex: 1; }
        .metric-title { color: #8899A6; font-size: 0.9rem; font-weight: bold; }
        .metric-value { color: #55acee; font-size: 2.5rem; font-weight: bold; }
        .metric-delta { color: #8899A6; font-size: 0.9rem; }

        /* Contenedor del Gráfico: Ancho controlado para que no se deforme */
        .chart-container {
            background-color: #1C2126;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #30363d;
            max-width: 800px; /* Ancho máximo para el gráfico */
            margin: 0 auto; /* Centrado horizontal */
        }
    </style>
""", unsafe_allow_html=True)

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- PANTALLA DE ACCESO ---
if not st.session_state["logueado"]:
    st.write("#")
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1>🚗 CRM OTORMÍN</h1>", unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if u == "Admin" and p == "Otormin2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else: st.error("Credenciales Incorrectas")

# --- SISTEMA OPERATIVO ---
else:
    # Datos demo para Paysandú
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos"],
        "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO"],
        "Saldo (USD)": [450, 0, 0, 320],
        "Cuota": [5, 12, 8, 3],
        "Recibo_Int": [1024, 1025, 1026, 1027],
        "lat": [-32.3162, -32.3210, -32.3050, -32.3320],
        "lon": [-58.0850, -58.0790, -58.0910, -58.0820]
    }
    df = pd.DataFrame(data)

    with st.sidebar:
        st.markdown("<h2>OTORMÍN</h2>", unsafe_allow_html=True)
        st.write("---")
        opcion = st.radio("MENÚ DE GESTIÓN:", ["📊 Tablero", "💰 Cobros", "🔍 Buscador", "📄 Documentos", "📍 Mapa de Cobranza"])
        st.write("---")
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    st.markdown(f"<h2>Sección: {opcion.upper()}</h2>", unsafe_allow_html=True)
    st.write("---")

    # --- MÓDULO TABLERO (CORREGIDO Y ORDENADO) ---
    if opcion == "📊 Tablero":
        # Métricas en contenedor HTML personalizado para control total
        st.markdown("""
            <div class="metric-container">
                <div class="metric-box">
                    <div class="metric-title">EN MORA</div>
                    <div class="metric-value">5</div>
                    <div class="metric-delta">USD 2.210</div>
                </div>
                <div class="metric-box">
                    <div class="metric-title">A COBRAR</div>
                    <div class="metric-value">4</div>
                    <div class="metric-delta">USD 1.850</div>
                </div>
                <div class="metric-box">
                    <div class="metric-title">TOTAL CARTERA</div>
                    <div class="metric-value">20</div>
                    <div class="metric-delta">USD 15.400</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.subheader("📈 Proyección Semanal de Ingresos")
        
        # Gráfico centrado y con ancho controlado
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Usamos st.area_chart que queda muy bien en modo oscuro
        chart_data = pd.DataFrame({
            'Días': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie'],
            'Cobros Estimados': [10, 25, 15, 30, 45]
        }).set_index('Días')
        st.area_chart(chart_data, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- MÓDULO COBROS (MEJORADO) ---
    elif opcion == "💰 Cobros":
        st.subheader("📋 Lista de Cobranza Activa (Otormín)")
        
        # Estilo para la tabla
        def style_vencidos(val):
            color = '#701010' if val == 'VENCIDO' else '#155123'
            return f'background-color: {color}; color: white; font-weight: bold;'

        # Mostramos la tabla formateada y con ancho completo
        st.dataframe(
            df[["Cliente", "Vehículo", "Estado", "Saldo (USD)", "Cuota"]].style.map(style_vencidos, subset=['Estado']),
            use_container_width=True,
            hide_index=True
        )

    # --- RESTO DE MÓDULOS (Buscador, Documentos, Mapa) ---
    elif opcion == "🔍 Buscador":
        txt = st.text_input("Buscar cliente o auto:")
        if txt:
            res = df[df['Cliente'].str.contains(txt, case=False) | df['Vehículo'].str.contains(txt, case=False)]
            st.table(res[["Cliente", "Vehículo", "Estado", "Saldo (USD)"]])

    elif opcion == "📄 Documentos":
        st.subheader("📄 Generador de Recibos PDF")
        sel = st.selectbox("Seleccione el Cliente:", df["Cliente"])
        info = df[df["Cliente"] == sel].iloc[0]
        
        if PDF_DISPONIBLE:
            if st.button("📥 GENERAR Y DESCARGAR PDF"):
                # ... (Lógica del PDF idéntica a la versión anterior) ...
                pdf = FPDF()
                pdf.add_page()
                pdf.set_fill_color(85, 172, 238)
                pdf.rect(0, 0, 210, 30, 'F')
                pdf.set_font("Arial", 'B', 20)
                pdf.set_text_color(255, 255, 255)
                pdf.cell(0, 15, "AUTOMOTORA OTORMÍN 2026", 0, 1, 'C')
                pdf.set_text_color(0, 0, 0)
                pdf.ln(25)
                pdf.set_font("Arial", '', 12)
                pdf.cell(0, 10, f"Cliente: {sel}", 0, 1)
                pdf.cell(0, 10, f"Vehículo: {info['Vehículo']}", 0, 1)
                pdf.cell(0, 10, f"Importe: USD {info['Saldo (USD)']}", 0, 1)
                pdf_bytes = pdf.output(dest='S').encode('latin-1')
                st.download_button(label="📂 Click para bajar PDF", data=pdf_bytes, file_name=f"Recibo_{sel}.pdf", mime="application/pdf")
        else:
            st.error("⚠️ El servidor está activando el módulo PDF. Esperá 30 segundos y recargá.")

    elif opcion == "📍 Mapa de Cobranza":
        st.subheader("📍 Geolocalización de Deudores (Paysandú)")
        st.map(df.rename(columns={'lat': 'latitude', 'lon': 'longitude'}))
