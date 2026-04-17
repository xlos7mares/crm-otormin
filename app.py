import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN
st.set_page_config(page_title="CRM OTORMÍN 2026", layout="wide")

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# 2. PANTALLA DE LOGIN
if not st.session_state["logueado"]:
    st.markdown("<h1 style='text-align: center;'>🚗 CRM OTORMÍN 2026</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        with st.form("login"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if u == "Admin" and p == "Otormin2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")

# 3. SISTEMA PRINCIPAL
else:
    with st.sidebar:
        st.title("OTORMÍN")
        opcion = st.radio("MENÚ:", ["📊 Inteligencia", "💰 Cobros", "📍 Mapa"])
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    st.markdown(f"<h1 style='text-align: center;'>OTORMÍN - {opcion}</h1>", unsafe_allow_html=True)

    df = pd.DataFrame({
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro"],
        "Estado": ["VENCIDO", "AL DÍA", "AL DÍA"],
        "latitude": [-32.31, -32.32, -32.30],
        "longitude": [-58.08, -58.07, -58.09]
    })

    if opcion == "📊 Inteligencia":
        st.metric("EN MORA", "5 Clientes", "USD 2.210")
        st.line_chart([10, 20, 15, 25])
    elif opcion == "💰 Cobros":
        st.table(df[["Cliente", "Estado"]])
    elif opcion == "📍 Mapa":
        st.map(df)
        
