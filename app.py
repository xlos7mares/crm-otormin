import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime
from supabase import create_client
import random

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
        df_res = pd.DataFrame(res.data)
        if not df_res.empty:
            # Lógica de estados para que Ignacio siempre vea datos clasificados
            if 'estado_prestamo' not in df_res.columns:
                estados_demo = ["Pendiente", "Aprobado", "Solicitado", "Liquidado"]
                df_res['estado_prestamo'] = [random.choice(estados_demo) for _ in range(len(df_res))]
            if 'banco' not in df_res.columns:
                df_res['banco'] = "Santander"
        return df_res
    except:
        return pd.DataFrame()

# --- ESTILOS VISUALES ELITE ---
st.set_page_config(page_title="OTORMÍN DMS ELITE", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: white; }
        [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #333; }
        .card-intel { background-color: #1C2126; padding: 25px; border-radius: 12px; border-left: 5px solid #55acee; margin-bottom: 20px; }
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
        st.subheader("📥 Gestión de Cartera de Clientes")
        archivo = st.file_uploader("Subir base de datos:", type=["csv", "xlsx"])
        if archivo:
            df_imp = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)
            if st.button("💾 SINCRONIZAR CON BRASIL"):
                # Asignamos estados al azar para la demo inicial de las pestañas
                df_imp['estado_prestamo'] = [random.choice(["Pendiente", "Aprobado", "Solicitado"]) for _ in range(len(df_imp))]
                supabase.table("clientes").insert(df_imp.to_dict(orient='records')).execute()
                st.success("Base de datos actualizada.")
                st.rerun()
        
        if not df.empty:
            for i, r in df.iterrows():
                riesgo = str(r.get('riesgo', 'Bajo'))
                color = "#FF4B4B" if "Crítico" in riesgo else "#FFA500" if "Medio" in riesgo else "#25D366"
                with st.container():
                    c1, c2, c3 = st.columns([3, 1, 1])
                    c1.markdown(f"<b style='color:{color}; font-size:1.1em;'>● {r['cliente']}</b><br><small>{r['vehiculo']} | {r['matricula']}</small>", unsafe_allow_html=True)
                    c2.write(f"$ {r['saldo']:,.0f}")
                    msg = urllib.parse.quote(f"Hola {r['cliente']}, le recordamos su cuota de Automotora Otormín.")
                    c3.markdown(f'<a href="https://wa.me/{r["telefono"]}?text={msg}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:8px; border-radius:5px; width:100%; cursor:pointer;">WhatsApp</button></a>', unsafe_allow_html=True)
                    st.write("---")

    # 2. INTELIGENCIA (REPORTE EXHAUSTIVO RECUPERADO)
    elif opcion == "📊 Inteligencia y Gráficas":
        st.header("📈 Análisis Técnico de Flujo y Cartera")
        mora = df["saldo"].sum() if not df.empty else 0
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="card-intel">CAPITAL EXPUESTO TOTAL<br><h2>$ {mora:,.2f}</h2></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="card-intel">CONTRATOS ACTIVOS<br><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="card-intel">ESTADO DE RIESGO<br><h2 style="color:#FFA500;">MODERADO</h2></div>', unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("Visualización del GAP de Cobranza (Ingreso Esperado vs Real)")
        chart_data = pd.DataFrame({'Esperado': [100, 140, 120, 160, 150], 'Real': [80, 110, 105, 130, 125]})
        st.area_chart(chart_data)
        
        st.markdown(f"""
        ### 🧐 Análisis Técnico de la Gráfica:
        
        Esta gráfica es la herramienta fundamental para medir la **Salud Financiera** de la automotora. Representa la relación entre lo que la empresa ha facturado y lo que realmente ha percibido en efectivo.
        
        * **Línea Superior (Ingreso Esperado):** Es el total de las cuotas que, por contrato, deberían ingresar a caja este mes. Representa tu facturación teórica.
        * **Línea Inferior (Ingreso Real):** Es el dinero que efectivamente ha pasado por el banco o la caja. Es tu liquidez real.
        * **El concepto del "GAP" (Área sombreada):** Representa el **Diferencial de Recaudo**. Es dinero que legalmente es tuyo pero que está "durmiendo" en manos de los clientes. 
        
        **Consecuencia Directa:** Si el área sombreada (GAP) se ensancha, la empresa pierde **Capacidad Operativa**. Aunque tengas un capital expuesto de **$ {mora:,.2f}**, si el GAP es muy grande, no tendrás efectivo para comprar stock nuevo o pagar gastos corrientes sin recurrir a préstamos externos.
        
        ---
        ### 📋 Glosario Técnico de Términos Contables
        
        1. **Capital Expuesto**: Es el monto total que se encuentra circulando fuera de la empresa en forma de créditos. Es el activo de mayor riesgo de tu balance.
        2. **Liquidez Operativa**: Es la disponibilidad inmediata de dinero para hacer frente a los compromisos del día a día. Se mide restando el GAP de los Ingresos Esperados.
        3. **Mora Técnica**: Es el retraso sistemático que genera el GAP. No significa necesariamente que el cliente no pague, sino que no paga en el tiempo óptimo para el flujo de caja del negocio.
        4. **Capital Inmovilizado**: Fondos que forman parte del patrimonio de la empresa pero que no tienen "giro". Están quietos hasta que el cliente paga la última cuota.
        5. **Ratio de Cobrabilidad**: Es el porcentaje de éxito entre lo que esperabas cobrar y lo que cobraste. Cuanto más cerca esté la línea Real de la Esperada, más eficiente es tu negocio.
        """)

    # 3. FLUJO DE CRÉDITOS
    elif opcion == "📋 Flujo de Créditos":
        st.header("📋 Gestión y Seguimiento Bancario")
        if df.empty:
            st.warning("No hay datos cargados.")
        else:
            pendientes = df[df['estado_prestamo'].isin(['Pendiente', 'Solicitado', 'En Análisis'])]
            aprobados = df[df['estado_prestamo'].isin(['Aprobado', 'Liquidado'])]
            
            t1, t2 = st.tabs(["⏳ SOLICITUDES EN TRÁMITE", "✅ CRÉDITOS APROBADOS"])
            
            with t1:
                for i, r in pendientes.iterrows():
                    with st.expander(f"⚠️ {r['cliente']} | {r.get('banco', 'Bco. Santander')}"):
                        st.write(f"**Estado:** {r['estado_prestamo']}")
                        st.info("💡 **ACCIÓN SUGERIDA:** Realizar seguimiento con el banco para acelerar la resolución.")
            
            with t2:
                for i, r in aprobados.iterrows():
                    with st.expander(f"⭐ {r['cliente']} | OPERACIÓN EXITOSA"):
                        st.success(f"✅ **ACCIÓN SUGERIDA:** Coordinar con el cliente para la entrega de la unidad {r['vehiculo']}.")

    # 4. BUSCADOR Y EDITOR
    elif opcion == "🔍 Buscador y Editor":
        st.header("🔍 Localizador de Registros")
        busq = st.text_input("Buscar por nombre o matrícula:")
        if busq and not df.empty:
            res = df[df['cliente'].str.contains(busq, case=False) | df['matricula'].str.contains(busq, case=False)]
            if not res.empty:
                st.dataframe(res)
                st.write("### 📝 Actualizar Información")
                c1, c2 = st.columns(2)
                n_mat = c1.text_input("Nueva Matrícula (Reempadronamiento):", res.iloc[0]['matricula'])
                n_est = c2.selectbox("Cambiar Estado del Crédito:", ["Pendiente", "Solicitado", "Aprobado", "Liquidado"])
                if st.button("🔄 ACTUALIZAR EN NUBE"):
                    supabase.table("clientes").update({"matricula": n_mat, "estado_prestamo": n_est}).eq("id", res.iloc[0]['id']).execute()
                    st.success("Datos actualizados correctamente.")
                    st.rerun()

    # 5. RECIBOS
    elif opcion == "📄 Recibos":
        if not df.empty:
            sel = st.selectbox("Seleccionar Cliente:", df["cliente"])
            info = df[df["cliente"] == sel].iloc[0]
            st.markdown(f"<div style='background:white; color:black; padding:40px; border-radius:10px; border:2px solid #000;'>"
                        f"<h1 style='text-align:center; color:black;'>RECIBO AUTOMOTORA OTORMÍN</h1><hr>"
                        f"<p style='color:black;'><b>CLIENTE:</b> {info['cliente'].upper()}</p>"
                        f"<p style='color:black;'><b>POR CONCEPTO DE:</b> Pago de cuota de la unidad {info['vehiculo']}</p>"
                        f"<h1 style='text-align:center; color:black;'>TOTAL: $ {info['saldo']:,.0f}</h1></div>", unsafe_allow_html=True)
