import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# 1. CONFIGURACIÓN
st.set_page_config(page_title="CRM OTORMÍN 2026", page_icon="🚗", layout="wide")

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# 2. LOGIN
if not st.session_state["logueado"]:
    st.markdown("<h1 style='text-align: center; color: #55acee;'>🚗 CRM OTORMÍN 2026</h1>", unsafe_allow_html=True)
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
    # Datos Demo
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos"],
        "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO"],
        "Saldo (USD)": [450, 0, 0, 320],
        "latitude": [-32.3162, -32.3210, -32.3050, -32.3320],
        "longitude": [-58.0850, -58.0790, -58.0910, -58.0820]
    }
    df = pd.DataFrame(data)

    # Sidebar
    with st.sidebar:
        st.title("OTORMÍN")
        opcion = st.radio("MENÚ:", ["📊 Tablero", "💰 Cobros", "🔍 Buscador", "📄 Documentos", "📍 Mapa"])
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    st.markdown(f"<h1 style='text-align: center;'>OTORMÍN - {opcion.upper()}</h1>", unsafe_allow_html=True)

    # --- MÓDULOS ---
    if opcion == "📊 Tablero":
        st.metric("EN MORA", "5 Clientes", "USD 2.210")
        st.line_chart([10, 25, 15, 30])

    elif opcion == "💰 Cobros":
        st.dataframe(df[["Cliente", "Vehículo", "Estado", "Saldo (USD)"]], use_container_width=True, hide_index=True)

    elif opcion == "🔍 Buscador":
        busq = st.text_input("Buscar cliente...")
        if busq:
            res = df[df['Cliente'].str.contains(busq, case=False)]
            st.write(res)

    elif opcion == "📄 Documentos":
        st.subheader("Generación de Recibos")
        sel = st.selectbox("Seleccione Cliente:", df["Cliente"])
        info = df[df["Cliente"] == sel].iloc[0]
        
        texto_recibo = f"RECIBO OTORMÍN\nFecha: {datetime.now().date()}\nCliente: {sel}\nAuto: {info['Vehículo']}\nSaldo: {info['Saldo (USD)']}"
        
        st.text_area("Previsualización:", texto_recibo)
        st.download_button("💾 Descargar Recibo", texto_recibo, file_name=f"Recibo_{sel}.txt")

    elif opcion == "📍 Mapa":
        st.map(df[["latitude", "longitude"]])
