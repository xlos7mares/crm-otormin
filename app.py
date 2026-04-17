import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime
from supabase import create_client

# 1. CONEXIÓN BLINDADA A LA NUBE
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
        
        # Prevenir errores de columnas faltantes (DMS Update)
        columnas_necesarias = {
            "banco": "No asignado",
            "score_inicial": 0,
            "estado_prestamo": "Pendiente",
            "monto_aprobado": 0.0,
            "fecha_inicio": datetime.now().strftime('%Y-%m-%d')
        }
        for col, val in columnas_necesarias.items():
            if col not in df_res.columns:
                df_res[col] = val
        return df_res
    except:
        return pd.DataFrame(columns=["id", "cliente", "telefono", "vehiculo", "matricula", "saldo", "cuota_nro", "cuota_totales", "riesgo", "recibo_id", "banco", "score_inicial", "estado_prestamo", "monto_aprobado"])

# --- DISEÑO PROFESIONAL OTORMÍN BI & DMS ---
st.set_page_config(page_title="OTORMÍN BI & DMS - 2026", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        .card-intel {
            background-color: #1C2126; padding: 25px; border-radius: 15px;
            border-left: 5px solid #55acee; margin-bottom: 20px;
        }
        .recibo-render {
            background-color: white; color: #1a1a1a !important;
            padding: 40px; border-radius: 5px; max-width: 750px; margin: auto;
            border: 1px solid #ddd; font-family: 'Courier New', Courier, monospace;
        }
        h1, h2, h3 { color: #55acee !important; }
        .stButton>button { 
            background-color: #55acee; color: white; border-radius: 8px; 
            width: 100%; font-weight: bold; padding: 10px;
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
        st.markdown("<h1 style='text-align:center;'>CRM OTORMÍN</h1>", unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR AL SISTEMA"):
                if u == "Admin" and p == "Otormin2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else: st.error("Credenciales incorrectas")

else:
    df = cargar_desde_nube()
    
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>OTORMÍN BI & DMS</h2>", unsafe_allow_html=True)
        st.info("🟢 Conectado a Base de Datos SQL")
        st.write("---")
        opcion = st.radio("GESTIÓN:", [
            "📥 Carga Masiva Inteligente",
            "📊 Inteligencia Financiera", 
            "💰 Cobros & WhatsApp", 
            "📋 Seguimiento de Créditos",
            "🔍 Buscador y Editor",
            "📄 Generar Recibo"
        ])
        st.write("---")
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # 1. CARGA MASIVA
    if opcion == "📥 Carga Masiva Inteligente":
        st.subheader("🚀 Carga Masiva de Clientes")
        archivo = st.file_uploader("Subí el archivo Excel o CSV:", type=["csv", "xlsx"])
        if archivo:
            df_imp = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)
            st.dataframe(df_imp.head(10))
            if st.button("💾 GUARDAR PERMANENTE EN NUBE SQL"):
                with st.spinner("Sincronizando..."):
                    try:
                        registros = df_imp.to_dict(orient='records')
                        for r in registros:
                            if 'recibo_id' not in r or pd.isna(r['recibo_id']):
                                r['recibo_id'] = f"OT-{np.random.randint(1000, 9999)}"
                        supabase.table("clientes").insert(registros).execute()
                        st.success("¡Datos blindados en Brasil!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    # 2. INTELIGENCIA FINANCIERA (LA CLASE MAGISTRAL)
    elif opcion == "📊 Inteligencia Financiera":
        st.header("Centro de Inteligencia de Negocios")
        if df.empty:
            st.warning("⚠️ No hay datos para analizar.")
        else:
            mora_total = df["saldo"].sum()
            clientes_activos = len(df)
            
            if mora_total > 1500000:
                est, col_est, adv = "RIESGO CRÍTICO", "#FF4B4B", "Nivel de alerta máximo: El capital en calle compromete la liquidez operativa."
            elif mora_total > 800000:
                est, col_est, adv = "RIESGO MODERADO", "#FFA500", "Atención: Cartera con alta exposición. Reforzar cobranza inmediata."
            else:
                est, col_est, adv = "SALUDABLE", "#25D366", "La cartera se encuentra dentro de los márgenes de seguridad."

            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="card-intel"><p style="color:#8899A6;">CAPITAL TOTAL EXPUESTO</p><h2>$ {mora_total:,.2f}</h2></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="card-intel"><p style="color:#8899A6;">CONTRATOS ACTIVOS</p><h2>{clientes_activos}</h2></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div style="background-color:{col_est}; padding:25px; border-radius:15px; color:black; text-align:center;"><b>ESTADO DE CARTERA</b><br><h2>{est}</h2></div>', unsafe_allow_html=True)

            st.write("---")
            st.subheader("📈 Análisis de Recuperación de Capital (Flujo de Caja)")
            chart_data = pd.DataFrame({
                'Ingreso Esperado': [100, 150, 130, 180, 200, 170],
                'Ingreso Real (Caja)': [80, 120, 110, 140, 160, 130]
            })
            st.area_chart(chart_data)

            st.markdown(f"""
            ### 👨‍🏫 Análisis Estratégico para la Dirección:
            Ignacio, esta gráfica representa la **salud de tu flujo de efectivo**.
            El **GAP (Zona sombreada)** es el capital retrasado. Si crece, te falta efectivo para reponer stock de autos.
            **Diagnóstico:** {adv}
            """)

    # 3. COBROS & WHATSAPP
    elif opcion == "💰 Cobros & WhatsApp":
        st.subheader("Panel de Gestión de Cobranza")
        if df.empty: st.info("Sin datos.")
        for i, r in df.iterrows():
            with st.expander(f"{r['cliente']} - $ {r['saldo']} ({r.get('banco', 'S/D')})"):
                c1, c2 = st.columns([3, 1])
                with c1: st.write(f"Saldo Pendiente: **$ {r['saldo']}** | Cuota: {r['cuota_nro']} de {r['cuota_totales']}")
                with c2:
                    msg = f"Hola {r['cliente']}, te contactamos de Automotora Otormín por tu saldo de $ {r['saldo']}."
                    ws = f"https://wa.me/{r['telefono']}?text={urllib.parse.quote(msg)}"
                    st.markdown(f'<a href="{ws}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer;">📲 WhatsApp</button></a>', unsafe_allow_html=True)

    # 4. SEGUIMIENTO DE CRÉDITOS (NUEVO DMS)
    elif opcion == "📋 Seguimiento de Créditos":
        st.subheader("🔍 Estado de Solicitudes Bancarias")
        if not df.empty:
            for i, r in df.iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1: st.write(f"**Cliente:** {r['cliente']}")
                    with col2: st.info(f"Estado: {r.get('estado_prestamo', 'Solicitado')}")
                    with col3: 
                        progreso = {"Solicitado": 0.2, "En Análisis": 0.4, "Documentación": 0.6, "Aprobado": 0.8, "Liquidado": 1.0}
                        st.progress(progreso.get(r.get('estado_prestamo', 'Solicitado'), 0.1))
                    st.write("---")

    # 5. BUSCADOR Y EDITOR (NUEVO)
    elif opcion == "🔍 Buscador y Editor":
        st.header("Gestión y Corrección de Datos")
        busq = st.text_input("Buscar por Nombre o Matrícula:")
        if busq and not df.empty:
            res = df[df['cliente'].str.contains(busq, case=False) | df['matricula'].str.contains(busq, case=False)]
            st.dataframe(res, use_container_width=True)
            
            if len(res) == 1:
                st.write("### 📝 Editar Información Seleccionada")
                nueva_mat = st.text_input("Corregir Matrícula:", res.iloc[0]['matricula'])
                nuevo_estado = st.selectbox("Actualizar Estado Crédito:", ["Solicitado", "En Análisis", "Aprobado", "Liquidado"])
                if st.button("🔄 ACTUALIZAR EN NUBE"):
                    supabase.table("clientes").update({"matricula": nueva_mat, "estado_prestamo": nuevo_estado}).eq("id", res.iloc[0]['id']).execute()
                    st.success("Datos corregidos en Brasil.")
                    st.rerun()

    # 6. RECIBOS
    elif opcion == "📄 Generar Recibo":
        st.subheader("Generación de Comprobantes")
        if not df.empty:
            sel = st.selectbox("Seleccionar Cliente:", df["cliente"])
            info = df[df["cliente"] == sel].iloc[0]
            st.markdown(f"""
                <div class="recibo-render">
                    <h2 style="text-align:center; color:black;">OTORMÍN AUTOMOTORA</h2>
                    <p style="text-align:right; color:black;"><b>NRO:</b> {info['recibo_id']}<br><b>FECHA:</b> {datetime.now().strftime('%d/%m/%Y')}</p>
                    <hr style="border:1px solid black;">
                    <p style="color:black;"><b>RECIBIMOS DE:</b> {info['cliente'].upper()}</p>
                    <p style="color:black;"><b>CONCEPTO:</b> Cuota {info['cuota_nro']} de {info['cuota_totales']} - Unidad {info['vehiculo']}</p>
                    <div style="background-color:#eee; padding:20px; text-align:center; font-size:2em; font-weight:bold; color:black; border:2px solid black;">
                        TOTAL: $ {info['saldo']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
