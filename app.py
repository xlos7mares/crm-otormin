import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN Y ESTILO (NEGRO TOTAL)
st.set_page_config(page_title="CRM OTORMÍN 2026", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: #E1E8ED; }
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        h1, h2, h3 { color: #55acee !important; text-align: center; }
        .stDataFrame { background-color: #1C2126; }
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
    # Datos completos
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos"],
        "Matrícula": ["IAE 1234", "MAA 5678", "PAA 9012", "IAA 3456"],
        "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO"],
        "Saldo (USD)": [450, 200, 0, 320],
        "Cuota": [5, 12, 8, 3],
        "Recibo_Nro": ["OT-2026-001", "OT-2026-002", "OT-2026-003", "OT-2026-004"]
    }
    df = pd.DataFrame(data)

    with st.sidebar:
        st.title("OTORMÍN")
        opcion = st.radio("MENÚ:", ["📊 Tablero", "💰 Cobros", "🔍 Buscador", "📄 Documentos"])
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # --- BUSCADOR CORREGIDO ---
    if opcion == "🔍 Buscador":
        st.markdown("<h2>🔍 Buscador de Clientes</h2>", unsafe_allow_html=True)
        busq = st.text_input("Escribí el nombre del cliente o el vehículo:", placeholder="Ej: Mercedes...")
        
        # Si hay búsqueda, filtra. Si no, muestra todos.
        if busq:
            resultado = df[df['Cliente'].str.contains(busq, case=False) | df['Vehículo'].str.contains(busq, case=False)]
        else:
            resultado = df
            
        st.dataframe(resultado, use_container_width=True, hide_index=True)

    # --- DOCUMENTOS (RECIBO PDF SEGURO) ---
    elif opcion == "📄 Documentos":
        st.markdown("<h2>📄 Generación de Recibo Oficial</h2>", unsafe_allow_html=True)
        sel = st.selectbox("Seleccione el Cliente para el recibo:", df["Cliente"])
        info = df[df["Cliente"] == sel].iloc[0]
        
        # Diseño del recibo en pantalla (HTML)
        recibo_html = f"""
        <div style="background-color: white; color: black; padding: 30px; border-radius: 10px; font-family: Arial;">
            <h1 style="color: #004a99 !important; margin: 0;">AUTOMOTORA OTORMÍN</h1>
            <hr>
            <p style="text-align: right;"><b>RECIBO NRO:</b> {info['Recibo_Nro']}</p>
            <p><b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y')}</p>
            <br>
            <p><b>CLIENTE:</b> {sel}</p>
            <p><b>VEHÍCULO:</b> {info['Vehículo']} (Matrícula: {info['Matrícula']})</p>
            <p><b>CUOTA NRO:</b> {info['Cuota']}</p>
            <br>
            <h2 style="color: black !important; text-align: right;">IMPORTE: USD {info['Saldo (USD)']}</h2>
            <br><br>
            <p style="text-align: center; font-size: 0.8em;">Comprobante oficial de gestión de cartera - Otormín 2026</p>
        </div>
        """
        st.markdown(recibo_html, unsafe_allow_html=True)
        st.write("")
        
        # Botón de impresión (Simulado para que no falle el servidor)
        st.download_button(
            label="📥 DESCARGAR COMPROBANTE (TXT)",
            data=recibo_html.replace("<br>", "\n").strip(),
            file_name=f"Recibo_{info['Recibo_Nro']}.txt",
            mime="text/plain"
        )
        st.info("Para imprimir en PDF: Presioná Ctrl+P en tu teclado y seleccioná 'Guardar como PDF'.")

    # --- TABLERO Y COBROS ---
    elif opcion == "📊 Tablero":
        st.metric("EN MORA", "5", "USD 2.210")
        st.area_chart([10, 25, 15, 30, 45])
        
    elif opcion == "💰 Cobros":
        st.dataframe(df, use_container_width=True, hide_index=True)
