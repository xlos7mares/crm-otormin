import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# --- TRUCO DE IMPORTACIÓN SEGURA ---
try:
    from fpdf import FPDF
    PDF_DISPONIBLE = True
except ImportError:
    PDF_DISPONIBLE = False

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO NEGRO PROFESIONAL
st.set_page_config(page_title="CRM OTORMÍN 2026", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
        /* Fondo negro total */
        .stApp { background-color: #0B0E11; color: #E1E8ED; }
        
        /* Sidebar oscura con borde azul */
        [data-testid="stSidebar"] { 
            background-color: #15191D; 
            border-right: 2px solid #55acee; 
        }
        
        /* Tarjetas de métricas (Tablero) */
        div[data-testid="stMetricValue"] { color: #55acee; font-weight: bold; }
        div[data-testid="metric-container"] {
            background-color: #1C2126;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #30363d;
        }
        
        /* Títulos */
        h1, h2, h3 { color: #55acee !important; font-family: 'Segoe UI', sans-serif; }
        
        /* Botones personalizados */
        .stButton>button {
            width: 100%;
            background-color: #55acee;
            color: white;
            border: none;
            border-radius: 5px;
            height: 3em;
            font-weight: bold;
        }
        .stButton>button:hover { background-color: #3d89c7; border: none; color: white; }
    </style>
""", unsafe_allow_html=True)

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- PANTALLA DE ACCESO ---
if not st.session_state["logueado"]:
    st.write("#")
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 style='text-align: center;'>🚗 CRM OTORMÍN</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Gestión de Cartera Automotriz</p>", unsafe_allow_html=True)
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
    # Datos de Cartera
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
        st.markdown("<h2 style='text-align: center;'>OTORMÍN</h2>", unsafe_allow_html=True)
        st.write("---")
        opcion = st.radio("MENÚ DE GESTIÓN:", ["📊 Tablero", "💰 Cobros", "🔍 Buscador", "📄 Documentos", "📍 Mapa de Cobranza"])
        st.write("---")
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    st.markdown(f"<h2>Sección: {opcion.upper()}</h2>", unsafe_allow_html=True)

    if opcion == "📊 Tablero":
        c1, c2, c3 = st.columns(3)
        c1.metric("EN MORA", "5", "USD 2.210")
        c2.metric("A COBRAR", "4", "USD 1.850")
        c3.metric("TOTAL", "20", "USD 15.400")
        st.subheader("📈 Proyección de Ingresos")
        st.area_chart([10, 25, 15, 30, 45])

    elif opcion == "💰 Cobros":
        st.subheader("📋 Lista de Cobranza Activa")
        st.dataframe(df[["Cliente", "Vehículo", "Estado", "Saldo (USD)"]], use_container_width=True, hide_index=True)

    elif opcion == "🔍 Buscador":
        txt = st.text_input("Buscar cliente por nombre o auto:")
        if txt:
            res = df[df['Cliente'].str.contains(txt, case=False) | df['Vehículo'].str.contains(txt, case=False)]
            st.table(res[["Cliente", "Vehículo", "Estado", "Saldo (USD)"]])

    elif opcion == "📄 Documentos":
        st.subheader("📄 Generador de Recibos PDF")
        sel = st.selectbox("Seleccione el Cliente:", df["Cliente"])
        info = df[df["Cliente"] == sel].iloc[0]
        
        st.info(f"Preparando documento para: {sel} | Vehículo: {info['Vehículo']}")
        
        if PDF_DISPONIBLE:
            if st.button("📥 GENERAR Y DESCARGAR PDF"):
                pdf = FPDF()
                pdf.add_page()
                # Encabezado
                pdf.set_fill_color(85, 172, 238)
                pdf.rect(0, 0, 210, 30, 'F')
                pdf.set_font("Arial", 'B', 20)
                pdf.set_text_color(255, 255, 255)
                pdf.cell(0, 15, "AUTOMOTORA OTORMÍN 2026", 0, 1, 'C')
                
                # Cuerpo
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("Arial", 'B', 12)
                pdf.ln(25)
                pdf.cell(0, 10, f"RECIBO INTERNO NRO: #OT-{info['Recibo_Int']}", 0, 1)
                pdf.cell(0, 10, f"FECHA: {datetime.now().strftime('%d/%m/%Y')}", 0, 1)
                pdf.ln(5)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(10)
                
                pdf.set_font("Arial", '', 12)
                pdf.cell(50, 10, "CLIENTE:", 0)
                pdf.cell(0, 10, str(sel), 0, 1)
                pdf.cell(50, 10, "VEHÍCULO:", 0)
                pdf.cell(0, 10, str(info['Vehículo']), 0, 1)
                pdf.cell(50, 10, "CUOTA NRO:", 0)
                pdf.cell(0, 10, str(info['Cuota']), 0, 1)
                pdf.cell(50, 10, "IMPORTE:", 0)
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, f"USD {info['Saldo (USD)']}", 0, 1)
                
                pdf.ln(30)
                pdf.set_font("Arial", 'I', 10)
                pdf.cell(0, 10, "Comprobante de pago provisorio emitido por sistema CRM.", 0, 1, 'C')
                
                # Salida
                pdf_bytes = pdf.output(dest='S').encode('latin-1')
                st.download_button(
                    label="📂 Click aquí para bajar PDF",
                    data=pdf_bytes,
                    file_name=f"Recibo_Otormin_{sel}.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("⚠️ El servidor está activando el módulo PDF. Por favor, esperá 30 segundos y recargá la página.")

    elif opcion == "📍 Mapa de Cobranza":
        st.subheader("📍 Ubicación Geográfica de Cartera")
        st.map(df.rename(columns={'lat': 'latitude', 'lon': 'longitude'}))
