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
        df_res = pd.DataFrame(res.data)
        # Aseguramos columnas DMS
        for col, val in {"banco": "S/D", "score_inicial": 0, "estado_prestamo": "Liquidado"}.items():
            if col not in df_res.columns: df_res[col] = val
        return df_res
    except:
        return pd.DataFrame()

# --- ESTILOS VISUALES (SIDEBAR NEGRO Y DISEÑO ELITE) ---
st.set_page_config(page_title="OTORMÍN DMS ELITE", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: white; }
        [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #333; }
        .card-intel { background-color: #1C2126; padding: 20px; border-radius: 12px; border-left: 5px solid #55acee; margin-bottom: 15px; }
        .stButton>button { background-color: #55acee; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
        hr { border: 0.5px solid #333; }
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
        st.write("---")
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # 1. CARGA Y LISTADO (SEMÁFORO DE RIESGO)
    if opcion == "📥 Carga y Listado CRM":
        st.subheader("📥 Gestión de Base de Datos y Riesgo")
        archivo = st.file_uploader("Subir base de datos:", type=["csv", "xlsx"])
        if archivo:
            df_imp = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)
            if st.button("💾 GUARDAR TODO EN NUBE SQL"):
                supabase.table("clientes").insert(df_imp.to_dict(orient='records')).execute()
                st.success("Base de datos sincronizada con Brasil")
                st.rerun()
        
        st.write("---")
        st.subheader("👥 Cartera de Clientes (Control de Riesgo)")
        if df.empty: st.info("Cargue datos para visualizar el listado.")
        for i, r in df.iterrows():
            # Semáforo de riesgo
            riesgo = str(r.get('riesgo', 'Bajo'))
            color = "#FF4B4B" if "Crítico" in riesgo else "#FFA500" if "Medio" in riesgo or "Regular" in riesgo else "#25D366"
            
            with st.container():
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.markdown(f"<b style='color:{color}; font-size:1.1em;'>● {r['cliente']}</b><br><small>{r['vehiculo']} | {r['matricula']}</small>", unsafe_allow_html=True)
                c2.write(f"**Saldo:** $ {r['saldo']:,.0f}")
                msg = urllib.parse.quote(f"Hola {r['cliente']}, Automotora Otormín le recuerda su saldo pendiente de $ {r['saldo']}.")
                c3.markdown(f'<a href="https://wa.me/{r["telefono"]}?text={msg}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer; width:100%;">📲 WhatsApp</button></a>', unsafe_allow_html=True)
                st.write("---")

    # 2. INTELIGENCIA Y GRÁFICAS (EXPLICACIÓN TÉCNICA)
    elif opcion == "📊 Inteligencia y Gráficas":
        st.header("📈 Análisis Técnico de Cartera")
        mora = df["saldo"].sum() if not df.empty else 0
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="card-intel">CAPITAL EXPUESTO TOTAL<br><h2>$ {mora:,.2f}</h2></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="card-intel">CONTRATOS ACTIVOS<br><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="card-intel">RIESGO DE CARTERA<br><h2 style="color:#FFA500;">MODERADO</h2></div>', unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("Visualización del Flujo de Efectivo (GAP de Cobranza)")
        chart_data = pd.DataFrame({'Ingreso Esperado': [100, 140, 120, 160, 150], 'Ingreso Real (Caja)': [80, 110, 105, 130, 125]})
        st.area_chart(chart_data)
        
        st.markdown(f"""
        ### 🧐 Explicación Técnica de la Gráfica:
        
        Esta herramienta permite visualizar la **salud del flujo de efectivo**. 
        La línea superior representa la facturación teórica, mientras que la línea inferior muestra el ingreso real a caja.
        
        **El concepto del "GAP" (Zona sombreada):**
        Representa el **Diferencial de Recaudo**. Es capital que, aunque figura como ganado, permanece en manos de terceros.
        * **Impacto Operativo:** Un GAP amplio indica que la empresa tiene solvencia (patrimonio) pero puede presentar tensiones de **Liquidez** (falta de efectivo inmediato para compras o gastos).
        * **Acción Recomendada:** Reducir la brecha mediante gestión de cobranza para transformar ese capital inmovilizado en dinero líquido.
        
        ---
        ### 📋 Glosario Técnico de Términos
        
        1. **Capital Expuesto**: Monto total adeudado por la clientela. Representa el riesgo vivo de la empresa.
        2. **Liquidez**: Capacidad inmediata de la empresa para cumplir con sus obligaciones financieras.
        3. **GAP de Cobranza**: Diferencia métrica entre lo devengado (esperado) y lo percibido (real).
        4. **Capital Inmovilizado**: Activos que no pueden convertirse en efectivo de forma inmediata sin afectar la operación.
        """)

    # 3. FLUJO DE CRÉDITOS (ESTADOS Y PASOS)
    elif opcion == "📋 Flujo de Créditos":
        st.header("📋 Seguimiento de Solicitudes y Aprobaciones")
        if df.empty: st.info("No hay registros bancarios.")
        else:
            pendientes = df[df['estado_prestamo'].isin(['Solicitado', 'En Análisis', 'Documentación', 'Pendiente'])]
            aprobados = df[df['estado_prestamo'].isin(['Aprobado', 'Liquidado'])]
            
            t1, t2 = st.tabs(["⏳ PENDIENTES DE RESOLUCIÓN", "✅ APROBADOS / LISTOS"])
            with t1:
                for i, r in pendientes.iterrows():
                    with st.expander(f"⚠️ {r['cliente']} | {r.get('banco', 'Banco S/D')}"):
                        st.write(f"**Estado Actual:** {r['estado_prestamo']}")
                        st.info(f"**ACCIÓN REQUERIDA:** Realizar seguimiento con el ejecutivo de cuenta para agilizar la aprobación.")
            with t2:
                for i, r in aprobados.iterrows():
                    with st.expander(f"⭐ {r['cliente']} | OPERACIÓN EXITOSA"):
                        st.success(f"**ACCIÓN REQUERIDA:** Coordinar entrega de la unidad {r['vehiculo']} y firma de documentación final.")

    # 4. BUSCADOR Y EDITOR (REEMPADRONAMIENTO)
    elif opcion == "🔍 Buscador y Editor":
        st.header("🔍 Localizador y Edición de Matrículas")
        busq = st.text_input("Ingrese Nombre o Matrícula para buscar:")
        if busq and not df.empty:
            res = df[df['cliente'].str.contains(busq, case=False) | df['matricula'].str.contains(busq, case=False)]
            st.dataframe(res)
            if not res.empty:
                st.write("### 📝 Editar Información (Reempadronamiento)")
                c1, c2 = st.columns(2)
                with c1: nueva_mat = st.text_input("Corregir Matrícula:", res.iloc[0]['matricula'])
                with c2: nuevo_estado = st.selectbox("Estado del Crédito:", ["Solicitado", "Aprobado", "Liquidado"], index=0)
                
                if st.button("🔄 ACTUALIZAR EN NUBE SQL"):
                    supabase.table("clientes").update({"matricula": nueva_mat, "estado_prestamo": nuevo_estado}).eq("id", res.iloc[0]['id']).execute()
                    st.success("Datos actualizados correctamente en Brasil.")
                    st.rerun()

    # 5. RECIBOS
    elif opcion == "📄 Recibos":
        if df.empty: st.warning("No hay datos para generar recibos.")
        else:
            sel = st.selectbox("Seleccionar Cliente:", df["cliente"])
            info = df[df["cliente"] == sel].iloc[0]
            st.markdown(f"""
                <div style="background:white; color:black; padding:40px; border-radius:10px; border:2px solid #000;">
                    <h1 style="text-align:center; color:black;">RECIBO OTORMÍN</h1>
                    <p style="text-align:right;"><b>FECHA:</b> {datetime.now().strftime('%d/%m/%Y')}</p>
                    <p><b>CLIENTE:</b> {info['cliente'].upper()}</p>
                    <p><b>CONCEPTO:</b> Pago de cuota {info['cuota_nro']} de {info['cuota_totales']}</p>
                    <hr style="border:1px solid black;">
                    <h1 style="text-align:center; color:black;">$ {info['saldo']:,.0f}</h1>
                </div>
            """, unsafe_allow_html=True)
