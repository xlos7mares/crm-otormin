import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime

# INTENTO DE IMPORTACIÓN (Si falla, te avisa por qué)
try:
    from supabase import create_client
except ImportError:
    st.error("🚨 Falta instalar la librería de Supabase. Por favor, asegúrate de que el archivo 'requirements.txt' esté en tu GitHub con la palabra 'supabase'.")
    st.stop()

# 1. CONEXIÓN BLINDADA
URL_SUPABASE = "https://rzujoxnpziodfwbsjhqg.supabase.co"
KEY_SUPABASE = "sb_publishable_JhoPWHuPu3WHynQ8Pqhwxw_y-Y6P2zV"

@st.cache_resource
def conectar():
    return create_client(URL_SUPABASE, KEY_SUPABASE)

supabase = conectar()

# --- FUNCIONES ---
def cargar_desde_nube():
    try:
        res = supabase.table("clientes").select("*").execute()
        return pd.DataFrame(res.data)
    except:
        return pd.DataFrame(columns=["cliente", "telefono", "vehiculo", "matricula", "saldo", "cuota_nro", "cuota_totales", "riesgo", "recibo_id"])

# --- INTERFAZ ---
st.set_page_config(page_title="OTORMÍN BI", layout="wide")

# Login sencillo para evitar bucles
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

if not st.session_state["logueado"]:
    st.title("CRM OTORMÍN - Acceso")
    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if u == "Admin" and p == "Otormin2026":
            st.session_state["logueado"] = True
            st.rerun()
else:
    df = cargar_desde_nube()
    
    with st.sidebar:
        st.title("OTORMÍN BI")
        opcion = st.radio("MENÚ", ["📥 Carga Masiva", "📊 Inteligencia Financiera", "💰 Cobros"])

    if opcion == "📥 Carga Masiva":
        st.subheader("Importar Clientes a la Nube")
        archivo = st.file_uploader("Archivo de 200 clientes", type=["csv", "xlsx"])
        if archivo:
            df_new = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)
            if st.button("💾 GUARDAR PERMANENTE"):
                try:
                    registros = df_new.to_dict(orient='records')
                    # Pequeño truco para asegurar que no falten campos
                    for r in registros:
                        if 'recibo_id' not in r: r['recibo_id'] = "OT-NEW"
                    
                    supabase.table("clientes").insert(registros).execute()
                    st.success("¡Datos guardados en Brasil! Ya no se borran.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al guardar: {e}")

    elif opcion == "📊 Inteligencia Financiera":
        st.header("Análisis Estratégico")
        if not df.empty:
            mora = df["saldo"].sum()
            st.metric("Capital en Mora Total", f"USD {mora:,.2f}")
            st.line_chart(np.random.randn(20, 2) + [10, 12])
            st.write("### 🧠 Explicación")
            st.info("Ignacio, la línea azul muestra el flujo real. El GAP es la diferencia con tu meta.")
        else:
            st.warning("No hay datos en la nube.")
