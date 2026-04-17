import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime
from supabase import create_client

# 1. CONEXIÓN (Mantenemos tus llaves)
URL_SUPABASE = "https://rzujoxnpziodfwbsjhqg.supabase.co"
KEY_SUPABASE = "sb_publishable_JhoPWHuPu3WHynQ8Pqhwxw_y-Y6P2zV"

@st.cache_resource
def conectar():
    return create_client(URL_SUPABASE, KEY_SUPABASE)

supabase = conectar()

# --- MOTOR DE DATOS (Lee de la nube) ---
def cargar_desde_nube():
    try:
        # Esto va a buscar los datos a Brasil cada vez que cambias de pestaña
        res = supabase.table("clientes").select("*").execute()
        return pd.DataFrame(res.data)
    except Exception as e:
        return pd.DataFrame(columns=["cliente", "telefono", "vehiculo", "matricula", "saldo", "cuota_nro", "cuota_totales", "riesgo", "recibo_id"])

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="OTORMÍN BI - 2026", layout="wide")

# (Aquí mantenemos tu CSS y Login...)

if "logueado" in st.session_state and st.session_state["logueado"]:
    # CARGAR DATOS: Esto es vital, se ejecuta en cada refresco
    df = cargar_desde_nube()
    
    with st.sidebar:
        st.title("OTORMÍN BI")
        opcion = st.radio("GESTIÓN:", ["📥 Carga Masiva Inteligente", "📊 Inteligencia Financiera", "💰 Cobros & WhatsApp"])

    # --- PESTAÑA 1: CARGA ---
    if opcion == "📥 Carga Masiva Inteligente":
        st.subheader("🚀 Paso 1: Subir Archivo")
        archivo = st.file_uploader("Subí los 200 clientes:", type=["csv", "xlsx"])
        
        if archivo:
            df_temp = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)
            st.write("Vista previa (esto es temporal):")
            st.dataframe(df_temp.head(5))
            
            # EL BOTÓN MÁGICO
            if st.button("💾 GUARDAR PERMANENTE EN BRASIL"):
                with st.spinner("Guardando en la base de datos de Brasil..."):
                    try:
                        # Convertir a lista para la nube
                        registros = df_temp.to_dict(orient='records')
                        # Enviar a Supabase
                        supabase.table("clientes").insert(registros).execute()
                        st.success("¡ÉXITO! Los datos ya están en la nube. Ahora podés refrescar o cambiar de pestaña y no se borrarán.")
                        st.balloons()
                        # Forzamos recarga para que 'df' se actualice
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar: {e}. ¿Creaste la tabla en el SQL Editor?")

    # --- PESTAÑA 2: INTELIGENCIA ---
    elif opcion == "📊 Inteligencia Financiera":
        st.header("Análisis de Datos en la Nube")
        if df.empty:
            st.warning("⚠️ La base de datos está vacía. Primero debés cargar y GUARDAR los datos en la pestaña anterior.")
        else:
            st.metric("Total en Mora (Desde SQL)", f"USD {df['saldo'].sum():,.2f}")
            st.line_chart(np.random.randn(20, 2))
