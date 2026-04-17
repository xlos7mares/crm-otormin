import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime
from supabase import create_client

# 1. CONEXIÓN
URL_SUPABASE = "https://rzujoxnpziodfwbsjhqg.supabase.co"
KEY_SUPABASE = "sb_publishable_JhoPWHuPu3WHynQ8Pqhwxw_y-Y6P2zV"

@st.cache_resource
def conectar():
    return create_client(URL_SUPABASE, KEY_SUPABASE)

supabase = conectar()

def cargar_desde_nube():
    try:
        res = supabase.table("clientes").select("*").execute()
        df_res = pd.DataFrame(res.data)
        # Si la tabla tiene datos, aseguramos que las columnas nuevas existan en el DataFrame
        if not df_res.empty:
            for col, val in {"banco": "S/D", "score_inicial": 0, "estado_prestamo": "Pendiente"}.items():
                if col not in df_res.columns: df_res[col] = val
        return df_res
    except:
        return pd.DataFrame()

# --- ESTILOS ---
st.set_page_config(page_title="OTORMÍN DMS ELITE", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: white; }
        [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #333; }
        .card-intel { background-color: #1C2126; padding: 20px; border-radius: 12px; border-left: 5px solid #55acee; margin-bottom: 15px; }
        .stButton>button { background-color: #55acee; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

if "logueado" not in st.session_state: st.session_state["logueado"] = False

# --- LOGIN ---
if not st.session_state["logueado"]:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 style='text-align:center; color:#55acee;'>CRM OTORMÍN</h1>", unsafe_allow_html=True)
        with st.form("login"):
            u, p = st.text_input("Usuario"), st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if u == "Admin" and p == "Otormin2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else: st.error("Acceso denegado")
else:
    df = cargar_desde_nube()
    with st.sidebar:
        st.markdown("<h2 style='color:white; text-align:center;'>OTORMÍN DMS</h2>", unsafe_allow_html=True)
        st.write("---")
        opcion = st.radio("", ["📥 Carga y Listado CRM", "📊 Inteligencia y Gráficas", "📋 Flujo de Créditos", "🔍 Buscador y Editor", "📄 Recibos"])
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # 1. CARGA Y LISTADO
    if opcion == "📥 Carga y Listado CRM":
        st.subheader("📥 Gestión de Base de Datos")
        archivo = st.file_uploader("Subir archivo:", type=["csv", "xlsx"])
        if archivo:
            df_imp = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)
            if st.button("💾 GUARDAR TODO EN NUBE SQL"):
                supabase.table("clientes").insert(df_imp.to_dict(orient='records')).execute()
                st.success("Sincronizado")
                st.rerun()
        
        st.write("---")
        if not df.empty:
            for i, r in df.iterrows():
                riesgo = str(r.get('riesgo', 'Bajo'))
                color = "#FF4B4B" if "Crítico" in riesgo else "#FFA500" if "Medio" in riesgo else "#25D366"
                with st.container():
                    c1, c2, c3 = st.columns([3, 1, 1])
                    c1.markdown(f"<b style='color:{color};'>● {r['cliente']}</b><br><small>{r['vehiculo']} | {r['matricula']}</small>", unsafe_allow_html=True)
                    c2.write(f"$ {r['saldo']:,.0f}")
                    msg = urllib.parse.quote(f"Hola {r['cliente']}...")
                    c3.markdown(f'<a href="https://wa.me/{r["telefono"]}?text={msg}" target="_blank">📲 WhatsApp</a>', unsafe_allow_html=True)
                    st.write("---")

    # 2. INTELIGENCIA (EXPLICACIÓN TÉCNICA)
    elif opcion == "📊 Inteligencia y Gráficas":
        st.header("📈 Análisis Técnico de Cartera")
        mora = df["saldo"].sum() if not df.empty else 0
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="card-intel">CAPITAL EXPUESTO<br><h2>$ {mora:,.2f}</h2></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="card-intel">CONTRATOS<br><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="card-intel">ESTADO RIESGO<br><h2 style="color:#FFA500;">MODERADO</h2></div>', unsafe_allow_html=True)
        
        st.area_chart(pd.DataFrame({'Esperado': [100, 140, 120, 160], 'Real': [80, 110, 105, 130]}))
        st.markdown("### 🧐 Explicación de la Gráfica:")
        st.write("La zona sombreada es el **GAP de Cobranza** (Diferencial de Recaudo). Es capital que tienes en la calle pero que no ha entrado a caja, afectando tu **Liquidez Operativa**.")

    # 3. FLUJO DE CRÉDITOS (CORREGIDO PARA QUE MUESTRE TODO)
    elif opcion == "📋 Flujo de Créditos":
        st.header("📋 Seguimiento de Solicitudes")
        if df.empty:
            st.info("No hay datos cargados.")
        else:
            # Lógica inclusiva: si no tiene estado o es Pendiente/Solicitado, va a la pestaña 1
            pendientes = df[df['estado_prestamo'].isin(['Solicitado', 'En Análisis', 'Documentación', 'Pendiente']) | df['estado_prestamo'].isna()]
            aprobados = df[df['estado_prestamo'].isin(['Aprobado', 'Liquidado'])]
            
            t1, t2 = st.tabs(["⏳ PENDIENTES DE RESOLUCIÓN", "✅ APROBADOS / LISTOS"])
            with t1:
                if pendientes.empty: st.write("No hay solicitudes pendientes.")
                for i, r in pendientes.iterrows():
                    with st.expander(f"⚠️ {r['cliente']} | {r.get('banco', 'S/D')}"):
                        st.write(f"**Estado:** {r.get('estado_prestamo', 'Pendiente')}")
                        st.info("**ACCIÓN:** Realizar seguimiento con el ejecutivo para apurar aprobación.")
            with t2:
                if aprobados.empty: st.write("No hay créditos aprobados aún.")
                for i, r in aprobados.iterrows():
                    with st.expander(f"⭐ {r['cliente']} | LISTO"):
                        st.success(f"**ACCIÓN:** Coordinar entrega de la unidad {r['vehiculo']}.")

    # 4. BUSCADOR Y EDITOR
    elif opcion == "🔍 Buscador y Editor":
        st.header("🔍 Buscador y Edición")
        busq = st.text_input("Nombre o Matrícula:")
        if busq and not df.empty:
            res = df[df['cliente'].str.contains(busq, case=False) | df['matricula'].str.contains(busq, case=False)]
            st.dataframe(res)
            if not res.empty:
                st.write("### Editar Información")
                c1, c2 = st.columns(2)
                nueva_mat = c1.text_input("Nueva Matrícula:", res.iloc[0]['matricula'])
                nuevo_est = c2.selectbox("Estado Crédito:", ["Pendiente", "Solicitado", "Aprobado", "Liquidado"])
                if st.button("🔄 ACTUALIZAR"):
                    supabase.table("clientes").update({"matricula": nueva_mat, "estado_prestamo": nuevo_est}).eq("id", res.iloc[0]['id']).execute()
                    st.success("Actualizado")
                    st.rerun()

    # 5. RECIBOS
    elif opcion == "📄 Recibos":
        if not df.empty:
            sel = st.selectbox("Cliente:", df["cliente"])
            info = df[df["cliente"] == sel].iloc[0]
            st.markdown(f"<div style='background:white; color:black; padding:30px; border-radius:10px; border:2px solid #000;'>"
                        f"<h2 style='text-align:center; color:black;'>RECIBO OTORMÍN</h2><hr>"
                        f"<p style='color:black;'><b>CLIENTE:</b> {info['cliente'].upper()}</p>"
                        f"<p style='color:black;'><b>CONCEPTO:</b> Cuota {info['cuota_nro']} de {info['cuota_totales']}</p>"
                        f"<h1 style='text-align:center; color:black;'>$ {info['saldo']:,.0f}</h1></div>", unsafe_allow_html=True)
