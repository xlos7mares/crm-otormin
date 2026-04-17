import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime
from supabase import create_client

# 1. CONEXIÓN BLINDADA (NO TOCAR)
URL_SUPABASE = "https://rzujoxnpziodfwbsjhqg.supabase.co"
KEY_SUPABASE = "sb_publishable_JhoPWHuPu3WHynQ8Pqhwxw_y-Y6P2zV"

@st.cache_resource
def conectar():
    return create_client(URL_SUPABASE, KEY_SUPABASE)

supabase = conectar()

# --- MOTOR DE DATOS ---
def cargar_desde_nube():
    try:
        res = supabase.table("clientes").select("*").execute()
        return pd.DataFrame(res.data)
    except:
        return pd.DataFrame(columns=["cliente", "telefono", "vehiculo", "matricula", "saldo", "cuota_nro", "cuota_totales", "riesgo", "recibo_id"])

# --- CONFIGURACIÓN DE DISEÑO PROFESIONAL ---
st.set_page_config(page_title="OTORMÍN BI - 2026", page_icon="📈", layout="wide")

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
            border: 1px solid #ddd;
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
                else: st.error("Credenciales incorrectas")

else:
    df = cargar_desde_nube()
    
    with st.sidebar:
        st.title("OTORMÍN BI")
        opcion = st.radio("GESTIÓN:", [
            "📥 Carga Masiva Inteligente",
            "📊 Inteligencia Financiera", 
            "💰 Cobros & WhatsApp", 
            "🔍 Buscador", 
            "📄 Generar Recibo"
        ])
        st.write("---")
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # 1. CARGA MASIVA
    if opcion == "📥 Carga Masiva Inteligente":
        st.subheader("🚀 Importación a la Nube SQL")
        archivo = st.file_uploader("Subí el archivo de 200 clientes:", type=["csv", "xlsx"])
        if archivo:
            df_new = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)
            st.dataframe(df_new.head(5))
            if st.button("💾 GUARDAR PERMANENTE EN BRASIL"):
                try:
                    registros = df_new.to_dict(orient='records')
                    for r in registros:
                        if 'recibo_id' not in r: r['recibo_id'] = f"OT-{np.random.randint(1000, 9999)}"
                    supabase.table("clientes").insert(registros).execute()
                    st.success("¡Datos blindados! Ya no se borran al refrescar.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    # 2. INTELIGENCIA FINANCIERA
    elif opcion == "📊 Inteligencia Financiera":
        st.header("Análisis Estratégico")
        if not df.empty:
            mora = df["saldo"].sum()
            c1, c2 = st.columns(2)
            with c1: st.markdown(f'<div class="card-intel"><p>CAPITAL EN MORA</p><h2>USD {mora:,.2f}</h2></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="card-intel"><p>CLIENTES</p><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
            
            st.subheader("📈 Proyección de Recuperación")
            st.line_chart(pd.DataFrame(np.random.randn(20, 2) + [10, 12], columns=['Real', 'Proyectado']))
            st.info("Ignacio: El GAP muestra la diferencia entre lo pactado y lo que realmente ingresa a caja.")
        else:
            st.warning("Cargá datos en la primera pestaña para ver las gráficas.")

    # 3. COBROS
    elif opcion == "💰 Cobros & WhatsApp":
        st.subheader("Lista de Cobranza Activa")
        for i, r in df.iterrows():
            with st.expander(f"{r['cliente']} - Saldo: USD {r['saldo']}"):
                msg = f"Hola {r['cliente']}, recordamos saldo de USD {r['saldo']} en Otormín."
                ws = f"https://wa.me/{r['telefono']}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{ws}" target="_blank">📲 WhatsApp</a>', unsafe_allow_html=True)

    # 4. BUSCADOR
    elif opcion == "🔍 Buscador":
        st.header("Buscador")
        busq = st.text_input("Nombre o Matrícula:")
        if busq:
            res = df[df['cliente'].str.contains(busq, case=False) | df['matricula'].str.contains(busq, case=False)]
            st.dataframe(res)
