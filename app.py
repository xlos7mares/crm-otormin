import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
from fpdf import FPDF

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO NEGRO
st.set_page_config(page_title="CRM OTORMÍN 2026", page_icon="🚗", layout="wide")

# Aplicar el estilo negro profundo que te gustaba
st.markdown("""
    <style>
        .stApp { background-color: #0E1117; color: white; }
        [data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #30363d; }
        .stMetric { background-color: #1E2329; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
        .stDataFrame { background-color: #1E2329; border-radius: 10px; }
        h1, h2, h3 { color: #55acee !important; }
    </style>
""", unsafe_allow_html=True)

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# 2. LOGIN
if not st.session_state["logueado"]:
    st.markdown("<h1 style='text-align: center;'>🚗 CRM OTORMÍN 2026</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        with st.form("login_otormin"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if u == "Admin" and p == "Otormin2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else: st.error("Acceso denegado")

# 3. SISTEMA ACTIVO
else:
    # Datos Demo mejorados
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos"],
        "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO"],
        "Saldo (USD)": [450, 0, 0, 320],
        "Cuota Nro": [5, 12, 8, 3],
        "latitude": [-32.3162, -32.3210, -32.3050, -32.3320],
        "longitude": [-58.0850, -58.0790, -58.0910, -58.0820]
    }
    df = pd.DataFrame(data)

    with st.sidebar:
        st.title("OTORMÍN")
        opcion = st.radio("MENÚ:", ["📊 Tablero", "💰 Cobros", "🔍 Buscador", "📄 Documentos", "📍 Mapa"])
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    st.markdown(f"<h1 style='text-align: center;'>OTORMÍN - {opcion.upper()}</h1>", unsafe_allow_html=True)

    if opcion == "📊 Tablero":
        c1, c2, c3 = st.columns(3)
        c1.metric("EN MORA", "5 Clientes", "USD 2.210")
        c2.metric("A COBRAR", "4 Clientes", "USD 1.850")
        c3.metric("TOTAL CARTERA", "20 Unidades", "USD 15.400")
        st.line_chart([10, 25, 15, 30])

    elif opcion == "💰 Cobros":
        st.dataframe(df[["Cliente", "Vehículo", "Estado", "Saldo (USD)"]], use_container_width=True, hide_index=True)

    elif opcion == "🔍 Buscador":
        busq = st.text_input("Buscar cliente o vehículo...")
        if busq:
            res = df[df['Cliente'].str.contains(busq, case=False) | df['Vehículo'].str.contains(busq, case=False)]
            st.dataframe(res, use_container_width=True)

    elif opcion == "📄 Documentos":
        st.subheader("Generación de Recibo Oficial PDF")
        sel = st.selectbox("Seleccione Cliente:", df["Cliente"])
        info = df[df["Cliente"] == sel].iloc[0]
        
        # Lógica para crear el PDF
        if st.button("Preparar PDF"):
            pdf = FPDF()
            pdf.add_page()
            
            # Encabezado con estética Otormín
            pdf.set_fill_color(22, 27, 34)
            pdf.rect(0, 0, 210, 40, 'F')
            pdf.set_font("Arial", 'B', 20)
            pdf.set_text_color(85, 172, 238)
            pdf.cell(0, 20, "AUTOMOTORA OTORMÍN 2026", 0, 1, 'C')
            
            # Datos del Recibo
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", 'B', 12)
            pdf.ln(20)
            pdf.cell(0, 10, f"RECIBO INTERNO NRO: #OT-00{datetime.now().second}{info['Cuota Nro']}", 0, 1)
            pdf.cell(0, 10, f"FECHA: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1)
            pdf.ln(10)
            
            # Tabla de datos
            pdf.set_font("Arial", '', 12)
            pdf.cell(50, 10, "CLIENTE:", 1)
            pdf.cell(0, 10, f" {sel}", 1, 1)
            pdf.cell(50, 10, "VEHÍCULO:", 1)
            pdf.cell(0, 10, f" {info['Vehículo']}", 1, 1)
            pdf.cell(50, 10, "NRO DE CUOTA:", 1)
            pdf.cell(0, 10, f" {info['Cuota Nro']}", 1, 1)
            pdf.cell(50, 10, "IMPORTE:", 1)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, f" USD {info['Saldo (USD)']}", 1, 1)
            
            pdf.ln(20)
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(0, 10, "Este documento sirve como comprobante oficial de pago.", 0, 1, 'C')

            # Generar salida del PDF para descarga
            pdf_output = pdf.output(dest='S').encode('latin-1')
            
            st.download_button(
                label="📥 Descargar Recibo PDF",
                data=pdf_output,
                file_name=f"Recibo_Otormin_{sel}.pdf",
                mime="application/pdf"
            )

    elif opcion == "📍 Mapa":
        st.map(df[["latitude", "longitude"]])
