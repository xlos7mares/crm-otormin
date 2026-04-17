import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Intentamos importar la librería. Si falla, avisamos al usuario en lugar de romper la app.
try:
    from fpdf import FPDF
    PDF_READY = True
except:
    PDF_READY = False

# 1. ESTILO NEGRO OTORMÍN
st.set_page_config(page_title="CRM OTORMÍN 2026", page_icon="🚗", layout="wide")
st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: #E1E8ED; }
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        h1, h2, h3 { color: #55acee !important; text-align: center; }
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

    if opcion == "📄 Documentos":
        st.header("📄 Generador de Recibos PDF")
        sel = st.selectbox("Seleccione Cliente:", df["Cliente"])
        info = df[df["Cliente"] == sel].iloc[0]

        # CUADRO DE PREVISUALIZACIÓN NEGRO
        st.markdown(f"""
            <div style="border: 1px solid #55acee; padding: 20px; border-radius: 10px;">
                <h4>Previsualización del Recibo</h4>
                <p><b>Recibo Nro:</b> {info['Recibo']}</p>
                <p><b>Cliente:</b> {sel}</p>
                <p><b>Vehículo:</b> {info['Vehículo']} ({info['Matrícula']})</p>
                <p><b>Cuota:</b> {info['Cuota']} | <b>Importe:</b> USD {info['Saldo']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")

        if PDF_READY:
            if st.button("🛠️ PREPARAR PDF"):
                pdf = FPDF()
                pdf.add_page()
                
                # Encabezado con estética Otormín
                pdf.set_fill_color(85, 172, 238)
                pdf.rect(0, 0, 210, 40, 'F')
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", 'B', 24)
                pdf.cell(0, 20, "AUTOMOTORA OTORMÍN", 0, 1, 'C')
                
                # Cuerpo del documento
                pdf.set_text_color(0, 0, 0)
                pdf.ln(30)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"RECIBO INTERNO NRO: {info['Recibo']}", 0, 1, 'R')
                pdf.cell(0, 10, f"FECHA: {datetime.now().strftime('%d/%m/%Y')}", 0, 1, 'R')
                
                pdf.ln(10)
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "DETALLES DEL PAGO", 1, 1, 'C')
                pdf.set_font("Arial", '', 12)
                
                pdf.cell(60, 10, "Nombre Cliente:", 1)
                pdf.cell(0, 10, f" {sel}", 1, 1)
                pdf.cell(60, 10, "Automotor:", 1)
                pdf.cell(0, 10, f" {info['Vehículo']} - Mat: {info['Matrícula']}", 1, 1)
                pdf.cell(60, 10, "Nro de Cuota:", 1)
                pdf.cell(0, 10, f" {info['Cuota']}", 1, 1)
                pdf.cell(60, 10, "Importe Total:", 1)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f" USD {info['Saldo']}", 1, 1)
                
                pdf.ln(20)
                pdf.set_font("Arial", 'I', 10)
                pdf.cell(0, 10, "Este documento es un comprobante de gestión interna de Otormín.", 0, 1, 'C')

                # Generar descarga
                pdf_bytes = pdf.output(dest='S').encode('latin-1')
                st.download_button(
                    label="📥 DESCARGAR RECIBO PDF",
                    data=pdf_bytes,
                    file_name=f"Recibo_Otormin_{info['Recibo']}.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("⚠️ El sistema está cargando el motor de PDF. Esperá 30 segundos y recargá la página (F5).")

    elif opcion == "🔍 Buscador":
        st.header("🔍 Buscador de Archivo")
        busq = st.text_input("Buscar por cliente o auto:")
        res = df[df['Cliente'].str.contains(busq, case=False) | df['Vehículo'].str.contains(busq, case=False)]
        st.dataframe(res, use_container_width=True, hide_index=True)

    elif opcion == "📊 Tablero":
        st.metric("EN MORA", "5", "USD 2.210")
        st.area_chart([10, 25, 15, 30, 45])

    elif opcion == "💰 Cobros":
        st.dataframe(df, use_container_width=True, hide_index=True)
