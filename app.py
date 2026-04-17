import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
import os

# --- IMPORTACIÓN SEGURA DE FPDF ---
try:
    from fpdf import FPDF
    PDF_DISPONIBLE = True
except ImportError:
    PDF_DISPONIBLE = False

# 1. CONFIGURACIÓN Y ESTILO (NEGRO Y AZUL)
st.set_page_config(page_title="CRM OTORMÍN 2026", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: #E1E8ED; }
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        h1, h2, h3 { color: #55acee !important; text-align: center; }
        .metric-container {
            display: flex;
            justify-content: space-around;
            background-color: #1C2126;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #30363d;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# 2. LOGIN
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

# 3. SISTEMA OPERATIVO
else:
    # Datos extendidos para el recibo
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos"],
        "Matrícula": ["IAE 1234", "MAA 5678", "PAA 9012", "IAA 3456"],
        "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO"],
        "Saldo (USD)": [450, 0, 0, 320],
        "Cuota_Actual": [5, 12, 8, 3],
        "Recibo_Nro": ["OT-2026-001", "OT-2026-002", "OT-2026-003", "OT-2026-004"],
        "lat": [-32.3162, -32.3210, -32.3050, -32.3320],
        "lon": [-58.0850, -58.0790, -58.0910, -58.0820]
    }
    df = pd.DataFrame(data)

    with st.sidebar:
        st.title("OTORMÍN")
        opcion = st.radio("MENÚ:", ["📊 Tablero", "💰 Cobros", "🔍 Buscador", "📄 Documentos", "📍 Mapa"])
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    st.markdown(f"<h2>Sección: {opcion.upper()}</h2>", unsafe_allow_html=True)

    if opcion == "📊 Tablero":
        st.markdown(f"""
            <div class="metric-container">
                <div style="text-align:center"><strong>EN MORA</strong><br><span style="font-size:2em; color:#55acee">5</span></div>
                <div style="text-align:center"><strong>A COBRAR</strong><br><span style="font-size:2em; color:#55acee">4</span></div>
                <div style="text-align:center"><strong>TOTAL</strong><br><span style="font-size:2em; color:#55acee">20</span></div>
            </div>
        """, unsafe_allow_html=True)
        st.area_chart([10, 25, 15, 30, 45])

    elif opcion == "💰 Cobros":
        st.subheader("Lista de Cobranza")
        st.dataframe(df[["Cliente", "Vehículo", "Estado", "Saldo (USD)"]], use_container_width=True, hide_index=True)

    elif opcion == "📄 Documentos":
        st.subheader("Generación de Recibo PDF")
        sel = st.selectbox("Seleccione Cliente:", df["Cliente"])
        info = df[df["Cliente"] == sel].iloc[0]
        
        # Previsualización de datos que irán al PDF
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Cliente:** {sel}")
            st.write(f"**Vehículo:** {info['Vehículo']}")
        with col2:
            st.write(f"**Recibo Int:** {info['Recibo_Nro']}")
            st.write(f"**Importe:** USD {info['Saldo (USD)']}")

        if PDF_DISPONIBLE:
            if st.button("📥 GENERAR PDF OFICIAL"):
                pdf = FPDF()
                pdf.add_page()
                
                # --- ENCABEZADO Y LOGO ---
                # Si existe logo.png lo pone, sino hace un cuadro azul
                if os.path.exists("logo.png"):
                    pdf.image("logo.png", 10, 8, 33)
                else:
                    pdf.set_fill_color(85, 172, 238)
                    pdf.rect(0, 0, 210, 35, 'F')
                
                pdf.set_font("Arial", 'B', 22)
                pdf.set_text_color(255, 255, 255)
                pdf.cell(0, 15, "AUTOMOTORA OTORMÍN", 0, 1, 'C')
                pdf.set_font("Arial", 'I', 10)
                pdf.cell(0, 5, "Gestión de Cartera - Paysandú, Uruguay", 0, 1, 'C')
                
                # --- DATOS DEL RECIBO ---
                pdf.set_text_color(0, 0, 0)
                pdf.ln(25)
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, f"RECIBO INTERNO: {info['Recibo_Nro']}", 0, 1, 'R')
                pdf.set_font("Arial", '', 11)
                pdf.cell(0, 10, f"Fecha de emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, 'R')
                pdf.ln(5)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(10)
                
                # --- CUERPO DEL DOCUMENTO ---
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, "DETALLES DEL CLIENTE Y COBRO:", 0, 1)
                pdf.set_font("Arial", '', 12)
                
                # Tabla de datos
                pdf.cell(50, 10, "Nombres y Apellidos:", 1)
                pdf.cell(0, 10, f" {sel}", 1, 1)
                
                pdf.cell(50, 10, "Datos del Automotor:", 1)
                pdf.cell(0, 10, f" {info['Vehículo']} (Matrícula: {info['Matrícula']})", 1, 1)
                
                pdf.cell(50, 10, "Cuota Nro:", 1)
                pdf.cell(0, 10, f" {info['Cuota_Actual']}", 1, 1)
                
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(50, 10, "IMPORTE RECIBIDO:", 1)
                pdf.set_text_color(200, 0, 0)
                pdf.cell(0, 10, f" USD {info['Saldo (USD)']}", 1, 1)
                
                # --- FIRMA Y PIE ---
                pdf.set_text_color(0, 0, 0)
                pdf.ln(30)
                pdf.line(120, pdf.get_y(), 190, pdf.get_y())
                pdf.set_font("Arial", 'I', 10)
                pdf.cell(0, 10, "Firma de Administración Otormín", 0, 1, 'R')
                
                pdf_output = pdf.output(dest='S').encode('latin-1')
                st.download_button(
                    label="💾 Descargar Recibo PDF",
                    data=pdf_output,
                    file_name=f"Recibo_{info['Recibo_Nro']}_{sel.replace(' ','_')}.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("Instalando componentes PDF... Reintente en 30 segundos.")

    elif opcion == "📍 Mapa":
        st.map(df.rename(columns={'lat': 'latitude', 'lon': 'longitude'}))
