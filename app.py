import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime
from supabase import create_client

# 1. CONEXIÓN Y CONFIGURACIÓN
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
        columnas_extra = {"banco": "Propio", "score_inicial": 500, "estado_prestamo": "Liquidado", "monto_aprobado": 0.0}
        for col, val in columnas_extra.items():
            if col not in df_res.columns: df_res[col] = val
        return df_res
    except:
        return pd.DataFrame()

# --- ESTILOS OTORMÍN ---
st.set_page_config(page_title="OTORMÍN BI & DMS", page_icon="🚗", layout="wide")
st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: white; }
        .card-intel { background-color: #1C2126; padding: 20px; border-radius: 10px; border-left: 5px solid #55acee; }
        .status-badge { padding: 5px 10px; border-radius: 5px; font-weight: bold; color: black; }
    </style>
""", unsafe_allow_html=True)

if "logueado" not in st.session_state: st.session_state["logueado"] = False

# --- LOGIN ---
if not st.session_state["logueado"]:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 style='text-align:center;'>OTORMÍN CRM</h1>", unsafe_allow_html=True)
        with st.form("login"):
            u, p = st.text_input("Usuario"), st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if u == "Admin" and p == "Otormin2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else: st.error("Error de acceso")
else:
    df = cargar_desde_nube()
    with st.sidebar:
        st.header("OTORMÍN DMS")
        opcion = st.radio("MENÚ:", ["📥 Carga y Listado", "📊 Inteligencia Ignacio", "📋 Flujo de Créditos", "🔍 Buscador/Editor", "📄 Recibos"])
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # 1. CARGA Y LISTADO (CON COLORES Y WHATSAPP)
    if opcion == "📥 Carga y Listado":
        st.subheader("🚀 Carga Masiva y Control Inmediato")
        archivo = st.file_uploader("Subir base de datos:", type=["csv", "xlsx"])
        if archivo:
            df_imp = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)
            if st.button("💾 GUARDAR TODO EN BRASIL"):
                supabase.table("clientes").insert(df_imp.to_dict(orient='records')).execute()
                st.success("Sincronizado con éxito")
                st.rerun()
        
        st.write("### 👥 Listado de Clientes en Sistema")
        for i, r in df.iterrows():
            color = "#25D366" if r['riesgo'] == "Bajo" else "#FFA500" if r['riesgo'] == "Medio" else "#FF4B4B"
            with st.container():
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.markdown(f"<b style='color:{color}'>● {r['cliente']}</b> | {r['vehiculo']} ({r['matricula']})", unsafe_allow_html=True)
                c2.write(f"Saldo: $ {r['saldo']}")
                msg = urllib.parse.quote(f"Hola {r['cliente']}, te hablamos de Otormín...")
                c3.markdown(f'<a href="https://wa.me/{r["telefono"]}?text={msg}" target="_blank">📲 WhatsApp</a>', unsafe_allow_html=True)
                st.write("---")

    # 2. INTELIGENCIA PARA IGNACIO (GLOSARIO Y GRÁFICAS)
    elif opcion == "📊 Inteligencia Ignacio":
        st.header("Análisis Estratégico de Cartera")
        mora = df["saldo"].sum()
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="card-intel">CAPITAL EXPUESTO<br><h2>$ {mora:,.2f}</h2></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="card-intel">CLIENTES ACTIVOS<br><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="card-intel">RIESGO GENERAL<br><h2>MODERADO</h2></div>', unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("📈 El GAP de Cobranza (Ingreso Esperado vs Real)")
        st.area_chart(pd.DataFrame({'Esperado': [100, 140, 120, 160], 'Real': [80, 110, 105, 130]}))
        
        st.markdown("""
        ### 👨‍🏫 Clase Magistral para Ignacio:
        * **GAP (Sombreado)**: Es el capital que "duerme". Si el área sombreada crece, tu caja sufre.
        * **Capital Expuesto**: Dinero tuyo que hoy tienen los clientes. Es una inversión de riesgo.
        * **Liquidez**: Lo que realmente entró al banco (línea inferior).
        
        ### 📖 Glosario del Empresario:
        1. **Mora**: Dinero que debería haber entrado y no entró.
        2. **Spread**: Tu ganancia entre el costo del auto y el total de cuotas.
        3. **Recupero**: Velocidad con la que el capital vuelve a tu mano para comprar otro auto.
        """)

    # 3. FLUJO DE CRÉDITOS (PASO A SEGUIR)
    elif opcion == "📋 Flujo de Créditos":
        st.header("Seguimiento de Préstamos Bancarios")
        for i, r in df.iterrows():
            with st.expander(f"{r['cliente']} - Estado: {r['estado_prestamo']}"):
                st.write(f"Banco: {r.get('banco', 'Propio')} | Score: {r.get('score_inicial', 0)}")
                if r['estado_prestamo'] == "Aprobado":
                    st.success("✅ PRÓXIMO PASO: Coordinar firma de títulos y entrega de unidad.")
                elif r['estado_prestamo'] == "En Análisis":
                    st.warning("⏳ PRÓXIMO PASO: Llamar al ejecutivo de cuenta para apurar resolución.")
                else:
                    st.info("ℹ️ Operación normal / Liquidada.")

    # 4. BUSCADOR Y EDITOR (REEMPADRONAMIENTO)
    elif opcion == "🔍 Buscador/Editor":
        st.header("Localizador y Editor de Datos")
        busq = st.text_input("Buscar Cliente o Matrícula:")
        if busq:
            res = df[df['cliente'].str.contains(busq, case=False) | df['matricula'].str.contains(busq, case=False)]
            st.dataframe(res)
            if not res.empty:
                st.write("### 📝 Editar Matrícula (Reempadronamiento)")
                nueva_mat = st.text_input("Nueva Matrícula:", res.iloc[0]['matricula'])
                if st.button("🔄 ACTUALIZAR MATRÍCULA"):
                    supabase.table("clientes").update({"matricula": nueva_mat}).eq("id", res.iloc[0]['id']).execute()
                    st.success("Matrícula actualizada en Brasil.")
                    st.rerun()

    # 5. RECIBOS
    elif opcion == "📄 Recibos":
        sel = st.selectbox("Seleccionar Cliente:", df["cliente"])
        info = df[df["cliente"] == sel].iloc[0]
        st.markdown(f"<div style='background:white; color:black; padding:30px; border-radius:10px; border: 2px solid #000;'>"
                    f"<h1 style='text-align:center; color:black;'>RECIBO OTORMÍN</h1>"
                    f"<p style='color:black;'><b>Recibimos de:</b> {info['cliente'].upper()}</p>"
                    f"<p style='color:black;'><b>Concepto:</b> Cuota {info['cuota_nro']} de {info['cuota_totales']}</p>"
                    f"<hr><h1 style='text-align:center; color:black;'>$ {info['saldo']}</h1></div>", unsafe_allow_html=True)
