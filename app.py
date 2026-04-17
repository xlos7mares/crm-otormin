import streamlit as st
import pandas as pd

# CONFIGURACIÓN BÁSICA
st.set_page_config(page_title="CRM OTORMÍN 2026", layout="wide")

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# LOGIN
if not st.session_state["logueado"]:
    st.title("🚗 CRM OTORMÍN 2026")
    with st.form("login"):
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.form_submit_button("INGRESAR"):
            if u == "Admin" and p == "Otormin2026":
                st.session_state["logueado"] = True
                st.rerun()
            else:
                st.error("Error de acceso")
else:
    # MENÚ
    with st.sidebar:
        st.header("OTORMÍN")
        opcion = st.radio("Menú", ["Tablero", "Cobros", "Mapa"])
        if st.button("Salir"):
            st.session_state["logueado"] = False
            st.rerun()

    st.header(f"Sección: {opcion}")
    
    # DATOS MÍNIMOS
    df = pd.DataFrame({
        "Cliente": ["Federico Rossi", "María Gonzalez"],
        "Estado": ["VENCIDO", "AL DÍA"],
        "lat": [-32.31, -32.32],
        "lon": [-58.08, -58.07]
    })

    if opcion == "Tablero":
        st.metric("EN MORA", "5 Clientes")
        st.bar_chart([10, 20, 15, 25])
    elif opcion == "Cobros":
        st.table(df[["Cliente", "Estado"]])
    elif opcion == "Mapa":
        st.map(df)
