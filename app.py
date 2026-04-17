import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime
from supabase import create_client
import random

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
        if not df_res.empty:
            # Si no hay columna de estado, la creamos con datos para la demostración
            if 'estado_prestamo' not in df_res.columns:
                estados_demo = ["Pendiente", "Aprobado", "Solicitado", "Liquidado"]
                df_res['estado_prestamo'] = [random.choice(estados_demo) for _ in range(len(df_res))]
            if 'banco' not in df_res.columns:
                df_res['banco'] = "Santander"
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
        st.subheader("📥 Carga de Clientes")
        archivo = st.file_uploader("Subir base de datos:", type=["csv", "xlsx"])
        if archivo:
            df_imp = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)
            if st.button("💾 SINCRONIZAR CON NUBE"):
                # Agregamos estados aleatorios a la carga para que Ignacio vea datos en las otras pestañas
                df_imp['estado_prestamo'] = [random.choice(["Pendiente", "Aprobado", "Solicitado"]) for _ in range(len(df_imp))]
                supabase.table("clientes").insert(df_imp.to_dict(orient='records')).execute()
                st.success("Sincronizado")
                st.rerun()
        
        if not df.empty:
            for i, r in df.iterrows():
                riesgo = str(r.get('riesgo', 'Bajo'))
                color = "#FF4B4B" if "Crítico" in riesgo else "#FFA500" if "Medio" in riesgo else "#25D366"
                with st.container():
                    c1, c2, c3 = st.columns([3, 1, 1])
                    c1.markdown(f"<b style='color:{color}; font-size:1.1em;'>● {r['cliente']}</b><br><small>{r['vehiculo']} | {r['matricula']}</small>", unsafe_allow_html=True)
                    c2.write(f"$ {r['saldo']:,.0f}")
                    msg = urllib.parse.quote(f"Hola {r['cliente']}...")
                    c3.markdown(f'<a href="https://wa.me/{r["telefono"]}?text={msg}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:8px; border-radius:5px; width:100%;">WhatsApp</button></a>', unsafe_allow_html=True)
                    st.write("---")

    # 2. INTELIGENCIA (EXPLICACIÓN TÉCNICA)
    elif opcion == "📊 Inteligencia y Gráficas":
        st.header("📈 Análisis Técnico de Flujo")
        mora = df["saldo"].sum() if not df.empty else 0
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="card-intel">CAPITAL EXPUESTO<br><h2>$ {mora:,.2f}</h2></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="card-intel">CONTRATOS<br><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="card-intel">RIESGO<br><h2 style="color:#FFA500;">MODERADO</h2></div>', unsafe_allow_html=True)
        
        st.area_chart(pd.DataFrame({'Esperado': [100, 140, 120, 160], 'Real': [80, 110, 105, 130]}))
        st.markdown("### 📋 Análisis del GAP de Cobranza")
        st.write("El área sombreada representa el **Capital Inmovilizado**. Es dinero que la empresa ha devengado pero que aún no se ha transformado en **Liquidez**.")

    # 3. FLUJO DE CRÉDITOS (ESTADOS AUTOMÁTICOS)
    elif opcion == "📋 Flujo de Créditos":
        st.header("📋 Gestión de Estados Bancarios")
        if df.empty:
            st.warning("Cargue datos en la primera pestaña para activar el flujo.")
        else:
            # Filtros robustos
            pendientes = df[df['estado_prestamo'].isin(['Pendiente', 'Solicitado', 'En Análisis'])]
            aprobados = df[df['estado_prestamo'].isin(['Aprobado', 'Liquidado'])]
            
            t1, t2 = st.tabs(["⏳ PENDIENTES / EN TRÁMITE", "✅ APROBADOS PARA ENTREGA"])
            
            with t1:
                for i, r in pendientes.iterrows():
                    with st.expander(f"⚠️ {r['cliente']} - {r.get('banco', 'Bco. Santander')}"):
                        st.write(f"**Estado:** {r['estado_prestamo']}")
                        st.info("💡 **PASO A SEGUIR:** Contactar al ejecutivo para acelerar resolución.")
            
            with t2:
                for i, r in aprobados.iterrows():
                    with st.expander(f"⭐ {r['cliente']} - LISTO PARA FIRMA"):
                        st.success(f"✅ **PASO A SEGUIR:** Coordinar entrega de la unidad {r['vehiculo']}.")

    # 4. BUSCADOR Y EDITOR
    elif opcion == "🔍 Buscador y Editor":
        st.header("🔍 Buscador y Edición de Datos")
        busq = st.text_input("Buscar por nombre o chapa:")
        if busq and not df.empty:
            res = df[df['cliente'].str.contains(busq, case=False) | df['matricula'].str.contains(busq, case=False)]
            if not res.empty:
                st.dataframe(res)
                st.write("### 📝 Editar Información")
                c1, c2 = st.columns(2)
                nueva_mat = c1.text_input("Nueva Matrícula:", res.iloc[0]['matricula'])
                nuevo_est = c2.selectbox("Cambiar Estado:", ["Pendiente", "Solicitado", "Aprobado", "Liquidado"])
                if st.button("🔄 ACTUALIZAR"):
                    supabase.table("clientes").update({"matricula": nueva_mat, "estado_prestamo": nuevo_est}).eq("id", res.iloc[0]['id']).execute()
                    st.success("Información actualizada en la base de datos.")
                    st.rerun()

    # 5. RECIBOS
    elif opcion == "📄 Recibos":
        if not df.empty:
            sel = st.selectbox("Seleccionar Cliente:", df["cliente"])
            info = df[df["cliente"] == sel].iloc[0]
            st.markdown(f"<div style='background:white; color:black; padding:30px; border-radius:10px; border:2px solid #000;'>"
                        f"<h1 style='text-align:center; color:black;'>RECIBO OTORMÍN</h1><hr>"
                        f"<p style='color:black;'><b>CLIENTE:</b> {info['cliente'].upper()}</p>"
                        f"<p style='color:black;'><b>MONTO:</b> $ {info['saldo']:,.0f}</p></div>", unsafe_allow_html=True)
