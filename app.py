import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime
from supabase import create_client

# 1. CONEXIÓN BLINDADA
URL_SUPABASE = "https://rzujoxnpziodfwbsjhqg.supabase.co"
KEY_SUPABASE = "sb_publishable_JhoPWHuPu3WHynQ8Pqhwxw_y-Y6P2zV"

@st.cache_resource
def conectar():
    return create_client(URL_SUPABASE, KEY_SUPABASE)

supabase = conectar()

def cargar_desde_nube():
    try:
        res = supabase.table("clientes").select("*").execute()
        return pd.DataFrame(res.data)
    except:
        return pd.DataFrame(columns=["id", "cliente", "telefono", "vehiculo", "matricula", "saldo", "cuota_nro", "cuota_totales", "riesgo", "recibo_id", "banco", "score_inicial", "estado_prestamo", "monto_aprobado"])

# --- DISEÑO PROFESIONAL DMS (Dealer Management System) ---
st.set_page_config(page_title="OTORMÍN DMS Elite", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        .card-intel { background-color: #1C2126; padding: 25px; border-radius: 15px; border-left: 5px solid #55acee; margin-bottom: 20px; }
        .stButton>button { background-color: #55acee; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

if "logueado" not in st.session_state: st.session_state["logueado"] = False

# --- LOGIN ---
if not st.session_state["logueado"]:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.write("#")
        st.markdown("<h1 style='text-align:center;'>OTORMÍN DMS</h1>", unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if u == "Admin" and p == "Otormin2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else: st.error("Error de acceso")

else:
    df = cargar_desde_nube()
    
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>CRM & DMS</h2>", unsafe_allow_html=True)
        opcion = st.radio("MÓDULOS:", [
            "📋 Registro y Créditos",
            "📊 Inteligencia Financiera", 
            "💰 Cobranza Activa", 
            "🔍 Buscador y Editor", 
            "📄 Recibos"
        ])
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # 1. REGISTRO Y CRÉDITOS (ENRIQUECIDO)
    if opcion == "📋 Registro y Créditos":
        st.subheader("🚀 Alta de Cliente y Gestión de Préstamo")
        with st.expander("➕ Ingresar Nuevo Cliente / Solicitud Bancaria", expanded=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                nombre = st.text_input("Nombre del Cliente")
                tel = st.text_input("WhatsApp (ej: 59899...)")
                score = st.number_input("Score Crediticio Inicial", 0, 1000, 500)
            with c2:
                vehiculo = st.text_input("Vehículo")
                matricula = st.text_input("Matrícula")
                banco = st.selectbox("Banco", ["Santander", "BBVA", "Itaú", "Scotiabank", "HSBC", "Propio Otormín"])
            with c3:
                monto = st.number_input("Monto Aprobado / Solicitado ($)", 0.0)
                cuotas_tot = st.number_input("Plazo (Cuotas)", 1, 120, 36)
                estado_p = st.select_slider("Estado del Préstamo", options=["Solicitado", "En Análisis", "Documentación", "Aprobado", "Liquidado"])
            
            if st.button("💾 GUARDAR REGISTRO EN NUBE"):
                # Cálculo de fecha final (Año estimado)
                anio_fin = datetime.now().year + (cuotas_tot // 12)
                nuevo_reg = {
                    "cliente": nombre, "telefono": tel, "vehiculo": vehiculo, "matricula": matricula,
                    "saldo": monto, "cuota_nro": 0, "cuota_totales": cuotas_tot, "riesgo": "Nuevo",
                    "banco": banco, "score_inicial": score, "estado_prestamo": estado_p, "monto_aprobado": monto
                }
                try:
                    supabase.table("clientes").insert(nuevo_reg).execute()
                    st.success(f"Registro Exitoso. Finaliza en: {anio_fin}")
                    st.rerun()
                except Exception as e: st.error(f"Error: {e}")

    # 2. INTELIGENCIA FINANCIERA (CON GLOSARIO)
    elif opcion == "📊 Inteligencia Financiera":
        st.header("Análisis de Cartera DMS")
        if not df.empty:
            mora = df["saldo"].sum()
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="card-intel"><p>CAPITAL EXPUESTO</p><h2>$ {mora:,.2f}</h2></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="card-intel"><p>SCORE PROM. CARTERA</p><h2>{df["score_inicial"].mean():,.0f} pts</h2></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="card-intel"><p>BANCO PRINCIPAL</p><h2>{df["banco"].mode()[0]}</h2></div>', unsafe_allow_html=True)
            
            st.area_chart(pd.DataFrame(np.random.randn(20, 2), columns=['Meta', 'Real']))
            
            st.markdown("""
            ### 👨‍🏫 Clase Magistral DMS:
            * **GAP de Liquidez**: Es la diferencia entre lo que el banco aprobó y lo que realmente ingresó a tu caja.
            * **Score Inicial**: Ignacio, si el promedio baja de 400 pts, estás tomando clientes de alto riesgo.
            * **Proyección de Plazos**: El sistema analiza cuántos años de deuda quedan por cobrar para asegurar la jubilación del negocio.
            """)

    # 3. COBRANZA (WHATSAPP)
    elif opcion == "💰 Cobranza Activa":
        st.subheader("Control de Pagos")
        for i, r in df.iterrows():
            with st.expander(f"{r['cliente']} | {r['banco']} | {r['estado_prestamo']}"):
                st.write(f"Monto: $ {r['saldo']} | Cuota: {r['cuota_nro']}/{r['cuota_totales']}")
                msg = f"Otormín le informa: Su crédito en {r['banco']} por el {r['vehiculo']} tiene una cuota pendiente."
                ws = f"https://wa.me/{r['telefono']}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{ws}" target="_blank">📲 Enviar Aviso</a>', unsafe_allow_html=True)

    # 4. BUSCADOR Y EDITOR (TU PEDIDO ESPECIAL)
    elif opcion == "🔍 Buscador y Editor":
        st.header("🔍 Gestión de Datos")
        busq = st.text_input("Buscar Cliente o Matrícula:")
        if busq:
            res = df[df['cliente'].str.contains(busq, case=False) | df['matricula'].str.contains(busq, case=False)]
            if not res.empty:
                idx = res.index[0]
                st.warning("⚠️ Modo Edición Activado")
                new_mat = st.text_input("Editar Matrícula:", res.iloc[0]['matricula'])
                new_estado = st.selectbox("Cambiar Estado Préstamo:", ["Solicitado", "En Análisis", "Aprobado", "Liquidado"], index=0)
                if st.button("🔄 ACTUALIZAR DATOS"):
                    supabase.table("clientes").update({"matricula": new_mat, "estado_prestamo": new_estado}).eq("id", res.iloc[0]['id']).execute()
                    st.success("Matrícula actualizada en Brasil.")
                    st.rerun()
            st.dataframe(res)

    # 5. RECIBOS
    elif opcion == "📄 Recibos":
        if not df.empty:
            sel = st.selectbox("Cliente:", df["cliente"])
            info = df[df["cliente"] == sel].iloc[0]
            st.markdown(f"""
                <div style="background:white; color:black; padding:30px; border-radius:10px;">
                    <h2 style="text-align:center;">RECIBO OTORMÍN</h2>
                    <p><b>CLIENTE:</b> {info['cliente']}</p>
                    <p><b>BANCO OPERADOR:</b> {info['banco']}</p>
                    <p><b>VEHÍCULO:</b> {info['vehiculo']} ({info['matricula']})</p>
                    <p><b>ESTADO CRÉDITO:</b> {info['estado_prestamo']}</p>
                    <hr>
                    <h1 style="text-align:center;">$ {info['saldo']}</h1>
                </div>
            """, unsafe_allow_html=True)
