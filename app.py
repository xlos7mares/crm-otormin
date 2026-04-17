import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 1. ESTILO NEGRO OTORMÍN (CONTROL DE TAMAÑO)
st.set_page_config(page_title="CRM OTORMÍN 2026", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: #E1E8ED; }
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        h1, h2, h3 { color: #55acee !important; text-align: center; }
        
        /* Evita que el gráfico se estire al infinito */
        .chart-container { max-width: 800px; margin: auto; }
        
        /* Tarjetas de métricas ordenadas */
        div[data-testid="metric-container"] {
            background-color: #1C2126;
            border: 1px solid #30363d;
            padding: 10px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# 2. LOGIN
if not st.session_state["logueado"]:
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
                else: st.error("Acceso Incorrecto")

# 3. SISTEMA
else:
    # Datos base para el CRM
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos"],
        "Matrícula": ["IAE 1234", "MAA 5678", "PAA 9012", "IAA 3456"],
        "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO"],
        "Saldo": [450, 0, 0, 320],
        "Cuota": [5, 12, 8, 3],
        "Recibo": ["OT-1001", "OT-1002", "OT-1003", "OT-1004"]
    }
    df = pd.DataFrame(data)

    with st.sidebar:
        st.title("OTORMÍN")
        opcion = st.radio("MENÚ:", ["📊 Tablero", "💰 Cobros", "🔍 Buscador", "📄 Documentos"])
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # --- TABLERO SIN DEFORMIDADES ---
    if opcion == "📊 Tablero":
        st.markdown("<h2>Resumen Operativo</h2>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("EN MORA", "5", "USD 2.210")
        c2.metric("A COBRAR", "4", "USD 1.850")
        c3.metric("TOTAL", "20", "USD 15.400")
        
        st.write("---")
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 Proyección de Cobranza")
        st.area_chart([12, 18, 14, 25, 30])
        st.markdown('</div>', unsafe_allow_html=True)

    # --- DOCUMENTOS (RECIBO PDF REAL) ---
    elif opcion == "📄 Documentos":
        st.header("📄 Generador de Recibos Oficiales")
        sel = st.selectbox("Seleccione Cliente:", df["Cliente"])
        info = df[df["Cliente"] == sel].iloc[0]

        # Cuadro de datos previo
        st.info(f"Recibo: {info['Recibo']} | Auto: {info['Vehículo']} | Saldo: USD {info['Saldo']}")
        
        if st.button("📥 GENERAR Y BAJAR PDF"):
            try:
                from fpdf import FPDF
                
                pdf = FPDF()
                pdf.add_page()
                
                # Encabezado Azul Otormín
                pdf.set_fill_color(85, 172, 238)
                pdf.rect(0, 0, 210, 40, 'F')
                pdf.set_font("Arial", 'B', 24)
                pdf.set_text_color(255, 255, 255)
                pdf.cell(0, 20, "AUTOMOTORA OTORMÍN", 0, 1, 'C')
                
                # Cuerpo (Datos que pediste)
                pdf.set_text_color(0, 0, 0)
                pdf.ln(30)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"RECIBO NRO: {info['Recibo']}", 0, 1, 'R')
                pdf.cell(0, 10, f"FECHA: {datetime.now().strftime('%d/%m/%Y')}", 0, 1, 'R')
                pdf.ln(10)
                
                # Tabla de detalles
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(60, 10, "CLIENTE:", 1); pdf.set_font("Arial", '', 12); pdf.cell(0, 10, f" {sel}", 1, 1)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(60, 10, "VEHICULO:", 1); pdf.set_font("Arial", '', 12); pdf.cell(0, 10, f" {info['Vehículo']} (Mat: {info['Matrícula']})", 1, 1)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(60, 10, "CUOTA NRO:", 1); pdf.set_font("Arial", '', 12); pdf.cell(0, 10, f" {info['Cuota']}", 1, 1)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(60, 10, "IMPORTE:", 1); pdf.set_font("Arial", 'B', 12); pdf.cell(0, 10, f" USD {info['Saldo']}", 1, 1)
                
                pdf_bytes = pdf.output(dest='S').encode('latin-1')
                st.download_button(label="✅ Descarga lista - Click aquí", data=pdf_bytes, file_name=f"Recibo_{sel}.pdf", mime="application/pdf")
                
            except ImportError:
                st.error("⚠️ El sistema aún está instalando el módulo de PDF. Refrescá la página en 10 segundos.")

    elif opcion == "🔍 Buscador":
        st.header("🔍 Buscador de Cartera")
        busq = st.text_input("Nombre o Matrícula:")
        res = df[df['Cliente'].str.contains(busq, case=False) | df['Matrícula'].str.contains(busq, case=False)]
        st.dataframe(res, use_container_width=True, hide_index=True)

    elif opcion == "💰 Cobros":
        st.dataframe(df, use_container_width=True, hide_index=True)
