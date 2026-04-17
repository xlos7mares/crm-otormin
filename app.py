import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime
import sqlite3

# 1. CONFIGURACIÓN DE ALTO NIVEL
st.set_page_config(page_title="OTORMÍN BI - 2026", page_icon="📈", layout="wide")

# --- MOTOR SQL ---
def conectar_db():
    return sqlite3.connect('otormin_datos.db', check_same_thread=False)

def crear_tabla():
    conn = conectar_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT, telefono TEXT, vehiculo TEXT, matricula TEXT,
            saldo REAL, cuota_nro INTEGER, cuota_totales INTEGER,
            riesgo TEXT, recibo_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

def cargar_datos():
    conn = conectar_db()
    df = pd.read_sql_query("SELECT * FROM clientes", conn)
    conn.close()
    return df

crear_tabla()

# ESTILOS CSS
st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        .card-intel {
            background-color: #1C2126; padding: 20px; border-radius: 12px;
            border-left: 5px solid #55acee; margin-bottom: 15px;
        }
        .recibo-render {
            background-color: white; color: #1a1a1a !important;
            padding: 40px; border-radius: 5px; max-width: 700px; margin: auto;
            border: 1px solid #ddd; font-family: 'Arial', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- LOGIN ---
if not st.session_state["logueado"]:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.write("#")
        st.markdown("<h1 style='text-align:center; color:#55acee;'>CRM OTORMÍN</h1>", unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if u == "Admin" and p == "Otormin2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else: st.error("Acceso denegado")

else:
    df = cargar_datos()
    with st.sidebar:
        st.title("OTORMÍN BI")
        opcion = st.radio("GESTIÓN:", ["📥 Carga Masiva Inteligente", "📊 Inteligencia Financiera", "💰 Cobros & WhatsApp", "🧮 Refinanciación", "🔍 Buscador", "📄 Generar Recibo"])
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # --- MÓDULO 1: CARGA MASIVA INTELIGENTE ---
    if opcion == "📥 Carga Masiva Inteligente":
        st.subheader("🚀 Importador Inteligente de Excel/CSV")
        st.write("No importa el orden de tus columnas, aquí las emparejamos.")
        
        archivo = st.file_uploader("Subí el archivo de la automotora:", type=["csv", "xlsx"])
        
        if archivo:
            df_temp = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)
            st.write("### Vista previa de tu archivo:")
            st.dataframe(df_temp.head(3))
            
            st.write("### 🧠 Mapeo de Columnas")
            st.info("Asigná tus columnas a los datos que necesita la App:")
            
            cols_app = ["cliente", "telefono", "vehiculo", "matricula", "saldo", "cuota_nro", "cuota_totales", "riesgo"]
            mapeo = {}
            
            c1, c2 = st.columns(2)
            for i, col_std in enumerate(cols_app):
                with (c1 if i % 2 == 0 else c2):
                    mapeo[col_std] = st.selectbox(f"¿Cuál es '{col_std}' en tu archivo?", [None] + list(df_temp.columns))

            if st.button("🚀 PROCESAR E IMPORTAR A SQL"):
                try:
                    # Reordenar y renombrar
                    df_final = df_temp[[mapeo[c] for c in cols_app if mapeo[c] is not None]].copy()
                    df_final.columns = [c for c in cols_app if mapeo[c] is not None]
                    
                    # Agregar Recibo_ID automático
                    df_final['recibo_id'] = [f"OT-{np.random.randint(5000, 9999)}" for _ in range(len(df_final))]
                    
                    conn = conectar_db()
                    df_final.to_sql('clientes', conn, if_exists='append', index=False)
                    conn.close()
                    st.success(f"¡Éxito! Se integraron {len(df_final)} clientes a la base de datos.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: Asegurate de haber mapeado las columnas correctamente. {e}")

    # --- RESTO DE MÓDULOS (Dashboard, Cobros, etc. igual que antes) ---
    elif opcion == "📊 Inteligencia Financiera":
        st.header("Análisis Estratégico")
        mora = df["saldo"].sum() if not df.empty else 0
        st.metric("Capital Expuesto", f"USD {mora:,.2f}")
        st.line_chart(np.random.randn(20, 2) + [10, 12])
        st.markdown("### Informe Financiero")
        st.write("El **GAP de Cobranza** mide el retraso entre el vencimiento pactado y el ingreso real.")

    elif opcion == "💰 Cobros & WhatsApp":
        st.subheader("Gestión de Cobranza")
        for i, r in df.iterrows():
            with st.expander(f"{r['riesgo']} | {r['cliente']}"):
                msg = f"Hola {r['cliente']}, recordamos saldo de USD {r['saldo']} en Otormín."
                ws = f"https://wa.me/{r['telefono']}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{ws}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; width:100%;">📲 WhatsApp</button></a>', unsafe_allow_html=True)

    elif opcion == "📄 Generar Recibo":
        if not df.empty:
            sel = st.selectbox("Cliente:", df["cliente"])
            inf = df[df["cliente"] == sel].iloc[0]
            st.markdown(f'<div class="recibo-render"><h2>OTORMÍN</h2><hr><p><b>CLIENTE:</b> {sel.upper()}</p><p><b>UNIDAD:</b> {inf["vehiculo"]}</p><div style="background:#f0f2f6; padding:15px; text-align:center;"><b>USD {inf["saldo"]}</b></div></div>', unsafe_allow_html=True)
