import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="CRM OTORMÍN 2026",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CONTROL DE SESIÓN
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- PANTALLA DE ACCESO (LOGIN) ---
if not st.session_state["logueado"]:
    st.markdown("<style>.stApp { background-color: #0E1117; color: white; }</style>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.write("#")
        st.markdown("<h1 style='text-align: center; color: #55acee;'>🚗 CRM OTORMÍN 2026</h1>", unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR AL SISTEMA"):
                if u == "Admin" and p == "Otormin2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else:
                    st.error("Acceso Denegado")

# --- SISTEMA ACTIVO ---
else:
    # Estilos Visuales
    st.markdown("""
        <style>
            .stApp { background-color: #0E1117; color: white; }
            [data-testid="stSidebar"] { background-color: #161B22; }
            .card {
                background-color: #1E2329;
                padding: 20px;
                border-radius: 10px;
                border-top: 4px solid #55acee;
                text-align: center;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Datos
    df = pd.DataFrame({
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
        "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
        "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
        "Saldo (USD)": [450, 0, 0, 320, 0],
        "latitude": [-32.3162, -32.3210, -32.3050, -32.3320, -32.3120],
        "longitude": [-58.0850, -58.0790, -58.0910, -58.0820, -58.1000]
    })

    # Barra Lateral
    with st.sidebar:
        st.title("OTORMÍN")
        opcion = st.radio("MENÚ:", ["📊 Inteligencia", "💰 Cobros", "🔍 Buscador", "📄 Documentos", "📍 Mapa"])
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # Contenido Central
    st.markdown(f"<h1 style='text-align: center;'>CRM OTORMÍN - {opcion.upper()}</h1>", unsafe_allow_html=True)

    if opcion == "📊 Inteligencia":
        c1, c2, c3 = st.columns(3)
        c1.markdown('<div class="card"><h3>EN MORA</h3><h2 style="color:red">5 Clientes</h2><p>USD 2.210</p></div>', unsafe_allow_html=True)
        c2.markdown('<div class="card"><h3>A COBRAR</h3><h2 style="color:cyan">4 Clientes</h2><p>USD 1.850</p></div>', unsafe_allow_html=True)
        c3.markdown('<div class="card"><h3>TOTAL CARTERA</h3><h2>20 Registros</h2><p>USD 15.400</p></div>', unsafe_allow_html=True)
        st.line_chart({"Cobros Estimados": [15, 30, 22, 45, 38]})

    elif opcion == "💰 Cobros":
        st.subheader("📋 Gestión de Cartera")
        st.dataframe(df[["Cliente", "Vehículo", "Vencimiento", "Estado", "Saldo (USD)"]], use_container_width=True, hide_index=True)

    elif opcion == "🔍 Buscador":
        busq = st.text_input("Buscar cliente...")
        if busq:
            res = df[df['Cliente'].str.contains(busq, case=False)]
            for _, r in res.iterrows():
                with st.expander(f"👤 {r['Cliente']}"):
                    st.write(f"Auto: {r['Vehículo']} | Saldo: ${r['Saldo (USD)']}")

    elif opcion == "📄 Documentos":
        st.subheader("📄 Generación de Recibos")
        sel = st.selectbox("Cliente:", df["Cliente"])
        if st.button("Generar PDF Oficial"):
            st.success(f"Recibo de Automotora Otormín para {sel} generado con éxito.")

    elif opcion == "📍 Mapa":
        st.subheader("📍 Mapa de Deudores (Paysandú)")
        st.map(df[["latitude", "longitude"]])
