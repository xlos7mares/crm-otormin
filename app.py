
import streamlit as st
import pandas as pd
from datetime import datetime

# --- IMPORTACIÓN SEGURA ---
try:
    from fpdf import FPDF
    PDF_READY = True
except ImportError:
    PDF_READY = False

# 1. CONFIGURACIÓN Y ESTILO BLINDADO
st.set_page_config(page_title="CRM OTORMÍN 2026", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: #E1E8ED; }
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        h1, h2, h3 { color: #55acee !important; text-align: center; }
        
        /* Controlar el tamaño de los gráficos y métricas para que no se deformen */
        .main-container { max-width: 1000px; margin: 0 auto; }
        div[data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #55acee; }
        .stPlotlyChart, .stAreaChart { max-height: 300px; }
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
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # --- TABLERO (CON TAMAÑO CONTROLADO) ---
    if opcion == "📊 Tablero":
        st.markdown("<h2>Resumen de Gestión</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("EN MORA", "5", "USD 2.210")
        col2.metric("A COBRAR", "4", "USD 1.850")
        col3.metric("TOTAL", "20", "USD 15.400")
        
        st.write("---")
        st.subheader("Proyección de Ingresos")
        # Limitamos el ancho del gráfico para que no se "rompa" visualmente
        _, chart_col, _ = st.columns([0.1, 0.8, 0.1])
        with chart_col:
            st.area_chart([10, 25, 15, 30, 45])

    # --- DOCUMENTOS (RECIBO PDF REAL) ---
    elif opcion == "📄 Documentos":
        st.header("📄 Generador de Recibos PDF")
        sel = st.selectbox("Seleccione Cliente:", df["Cliente"])
        info = df[df["Cliente"] == sel].iloc[0]

        st.markdown(f"""
            <div style="border: 1px solid #55acee; padding: 20px; border-radius: 10px; background-color: #15191D;">
                <h4 style="color:white !important; margin-top:0;">Previsualización del Recibo</h4>
                <p><b>Recibo Nro:</b> {info['Recibo']} | <b>Cliente:</b> {sel}</p>
                <p><b>Vehículo:</b> {info['Vehículo']} ({info['Matrícula']})</p>
                <p><b>Cuota:</b> {info['Cuota']} | <b>Importe:</b> USD {info['Saldo']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")

        if PDF_READY:
            if st.button("📥 GENERAR Y DESCARGAR PDF"):
                pdf = FPDF()
                pdf.add_page()
                # Encabezado azul
                pdf.set_fill_color(85, 172, 238)
                pdf.rect(0, 0, 210, 40, 'F')
                pdf.set_font("Arial", 'B', 24)
                pdf.set_text_color(255, 255, 255)
                pdf.cell(0, 20, "AUTOMOTORA OTORMÍN", 0, 1, 'C')
                
                # Cuerpo
                pdf.set_text_color(0, 0, 0)
                pdf.ln(30)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"RECIBO NRO: {info['Recibo']}", 0, 1, 'R')
                pdf.cell(0, 10, f"FECHA: {datetime.now().strftime('%d/%m/%Y')}", 0, 1, 'R')
                pdf.ln(10)
                
                # Datos en tabla
                pdf.cell(60, 10, "Cliente:", 1)
                pdf.cell(0, 10, f" {sel}", 1, 1)
                pdf.cell(60, 10, "Vehículo:", 1)
                pdf.cell(0, 10, f" {info['Vehículo']} - Mat: {info['Matrícula']}", 1, 1)
                pdf.cell(60, 10, "Cuota Nro:", 1)
                pdf.cell(0, 10, f" {info['Cuota']}", 1, 1)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(60, 10, "IMPORTE:", 1)
                pdf.cell(0, 10, f" USD {info['Saldo']}", 1, 1)
                
                pdf_bytes = pdf.output(dest='S').encode('latin-1')
                st.download_button(label="💾 Bajar PDF", data=pdf_bytes, file_name=f"Recibo_{info['Recibo']}.pdf", mime="application/pdf")
        else:
            st.warning("⚠️ Cargando componentes del sistema. Por favor, refrescá la página en 30 segundos.")

    elif opcion == "🔍 Buscador":
        st.header("🔍 Buscador")
        busq = st.text_input("Filtrar por nombre:")
        res = df[df['Cliente'].str.contains(busq, case=False)]
        st.dataframe(res, use_container_width=True, hide_index=True)

    elif opcion == "💰 Cobros":
        st.dataframe(df, use_container_width=True, hide_index=True)
