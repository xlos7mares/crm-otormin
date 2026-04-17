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
        # Aseguramos que existan las columnas de DMS para evitar errores
        for col, val in {"banco": "S/D", "score_inicial": 0, "estado_prestamo": "Liquidado"}.items():
            if col not in df_res.columns: df_res[col] = val
        return df_res
    except:
        return pd.DataFrame()

# --- ESTILOS VISUALES (SideBar Negra y Tarjetas) ---
st.set_page_config(page_title="OTORMÍN DMS ELITE", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: white; }
        [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #333; }
        .card-intel { background-color: #1C2126; padding: 20px; border-radius: 12px; border-left: 5px solid #55acee; margin-bottom: 15px; }
        .stButton>button { background-color: #55acee; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
        .status-pill { padding: 4px 10px; border-radius: 20px; font-size: 0.8em; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

if "logueado" not in st.session_state: st.session_state["logueado"] = False

# --- LOGIN ---
if not st.session_state["logueado"]:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 style='text-align:center; color:#55acee;'>CRM OTORMÍN</h1>", unsafe_allow_html=True)
        with st.form("login"):
            u, p = st.text_input("Usuario"), st.text_input("Contraseña (Otormin2026)", type="password")
            if st.form_submit_button("INGRESAR"):
                if u == "Admin" and p == "Otormin2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else: st.error("Acceso denegado")
else:
    df = cargar_desde_nube()
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3202/3202926.png", width=100)
        st.markdown("<h2 style='color:white;'>MENÚ DMS</h2>", unsafe_allow_html=True)
        opcion = st.radio("", ["📥 Carga y Listado CRM", "📊 Inteligencia Ignacio", "📋 Flujo de Créditos", "🔍 Buscador y Editor", "📄 Recibos"])
        st.write("---")
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # 1. CARGA Y LISTADO (CON COLORES DE RIESGO)
    if opcion == "📥 Carga y Listado CRM":
        st.subheader("📥 Carga Masiva y Control de Riesgo")
        archivo = st.file_uploader("Subir base de datos:", type=["csv", "xlsx"])
        if archivo:
            df_imp = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)
            if st.button("💾 GUARDAR TODO EN NUBE SQL"):
                supabase.table("clientes").insert(df_imp.to_dict(orient='records')).execute()
                st.success("Sincronizado con Brasil")
                st.rerun()
        
        st.write("---")
        st.subheader("👥 Listado Actual con Semáforo de Riesgo")
        for i, r in df.iterrows():
            # Lógica de color de riesgo
            riesgo = str(r.get('riesgo', 'Bajo'))
            color = "#FF4B4B" if "Crítico" in riesgo else "#FFA500" if "Medio" in riesgo or "Regular" in riesgo else "#25D366"
            
            with st.container():
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.markdown(f"<b style='color:{color}; font-size:1.1em;'>● {r['cliente']}</b><br><small>{r['vehiculo']} | {r['matricula']}</small>", unsafe_allow_html=True)
                c2.write(f"**Saldo:** $ {r['saldo']:,.0f}")
                msg = urllib.parse.quote(f"Estimado {r['cliente']}, Automotora Otormín le recuerda su saldo pendiente de $ {r['saldo']}.")
                c3.markdown(f'<a href="https://wa.me/{r["telefono"]}?text={msg}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer; width:100%;">📲 WhatsApp</button></a>', unsafe_allow_html=True)
                st.write("---")

    # 2. INTELIGENCIA PARA IGNACIO (EXPLICACIÓN EXHAUSTIVA)
    elif opcion == "📊 Inteligencia Ignacio":
        st.header("📈 Análisis de Salud Financiera")
        mora = df["saldo"].sum()
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="card-intel">CAPITAL EXPUESTO (CARTERA)<br><h2>$ {mora:,.2f}</h2></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="card-intel">CLIENTES ACTIVOS<br><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="card-intel">ESTADO DE CARTERA<br><h2 style="color:#FFA500;">MODERADO</h2></div>', unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("El GAP de Cobranza: ¿Por qué te falta efectivo?")
        # Gráfica de área con Gap sombreado
        chart_data = pd.DataFrame({
            'Flujo Esperado (Contratos)': [100, 140, 120, 160, 150],
            'Flujo Real (Dinero en Caja)': [80, 110, 105, 130, 125]
        })
        st.area_chart(chart_data)
        
        st.markdown(f"""
        ### 👨‍🏫 Clase Magistral de Finanzas para Ignacio:
        
        **¿Qué estamos viendo en esta gráfica?**
        La línea superior representa la **facturación teórica** (lo que los clientes firmaron que iban a pagar). La línea inferior es la **realidad de tu caja** (lo que efectivamente entró).
        
        **El concepto del "GAP" (La zona sombreada):**
        En contabilidad, esto se llama *Diferencial de Recaudo*. Esa zona sombreada es **tu dinero que está "durmiendo"** en el bolsillo de los clientes. 
        * **Peligro:** Si la zona sombreada se hace más ancha, aunque seas "millonario" en papeles por tener **$ {mora:,.2f}** para cobrar, no vas a tener dinero para pagar la luz o comprar otro auto mañana.
        
        **Nomenclatura que debes dominar:**
        1.  **Liquidez Operativa:** Es tu capacidad de pagar gastos hoy. El GAP atenta contra tu liquidez.
        2.  **Riesgo de Incobrabilidad:** Cuanto más tiempo pase el dinero en el GAP, más probable es que ese cliente nunca pague.
        3.  **Capital Inmovilizado:** Es ese millón de pesos que tienes "en la calle". Para el banco, eres solvente, pero para tu día a día, es dinero que no puedes usar.
        """)

    # 3. FLUJO DE CRÉDITOS (PENDIENTES Y APROBADOS)
    elif opcion == "📋 Flujo de Créditos":
        st.header("📋 Gestión de Solicitudes Bancarias")
        
        pendientes = df[df['estado_prestamo'].isin(['Solicitado', 'En Análisis', 'Documentación', 'Pendiente'])]
        aprobados = df[df['estado_prestamo'].isin(['Aprobado', 'Liquidado'])]
        
        tab1, tab2 = st.tabs(["⏳ SOLICITUDES PENDIENTES", "✅ CRÉDITOS APROBADOS"])
        
        with tab1:
            for i, r in pendientes.iterrows():
                with st.expander(f"⚠️ {r['cliente']} - {r.get('banco', 'Banco S/D')}"):
                    st.write(f"**Estado Actual:** {r['estado_prestamo']}")
                    st.progress(0.4)
                    st.info(f"👉 **PASO A SEGUIR:** Llamar al ejecutivo de {r.get('banco','el banco')} para verificar por qué no ha pasado a aprobación.")
        
        with tab2:
            for i, r in aprobados.iterrows():
                with st.expander(f"⭐ {r['cliente']} - LISTO PARA ENTREGA"):
                    st.write(f"**Monto Aprobado:** $ {r.get('monto_aprobado', r['saldo'])}")
                    st.success(f"👉 **PASO A SEGUIR:** Coordinar con el cliente la firma de títulos y la entrega de la unidad {r['vehiculo']}.")

    # 4. BUSCADOR Y EDITOR (REEMPADRONAMIENTO)
    elif opcion == "🔍 Buscador y Editor":
        st.header("🔍 Localizador y Corrector de Datos")
        busq = st.text_input("Buscar por Nombre o Matrícula:")
        if busq:
            res = df[df['cliente'].str.contains(busq, case=False) | df['matricula'].str.contains(busq, case=False)]
            st.dataframe(res)
            if not res.empty:
                st.write("### 📝 Editar Información (Reempadronamiento)")
                c1, c2 = st.columns(2)
                with c1: nueva_mat = st.text_input("Nueva Matrícula:", res.iloc[0]['matricula'])
                with c2: nuevo_estado = st.selectbox("Cambiar Estado Crédito:", ["Solicitado", "Aprobado", "Liquidado"], index=0)
                
                if st.button("🔄 ACTUALIZAR DATOS EN BRASIL"):
                    supabase.table("clientes").update({
                        "matricula": nueva_mat, 
                        "estado_prestamo": nuevo_estado
                    }).eq("id", res.iloc[0]['id']).execute()
                    st.success("Base de datos actualizada correctamente.")
                    st.rerun()

    # 5. RECIBOS
    elif opcion == "📄 Recibos":
        sel = st.selectbox("Cliente:", df["cliente"])
        info = df[df["cliente"] == sel].iloc[0]
        st.markdown(f"""
            <div style="background:white; color:black; padding:40px; border-radius:10px; border:2px solid #000;">
                <h1 style="text-align:center; color:black;">RECIBO OTORMÍN</h1>
                <p><b>FECHA:</b> {datetime.now().strftime('%d/%m/%Y')}</p>
                <p><b>CLIENTE:</b> {info['cliente'].upper()}</p>
                <p><b>CONCEPTO:</b> Cuota {info['cuota_nro']} de {info['cuota_totales']}</p>
                <hr>
                <h1 style="text-align:center; color:black;">$ {info['saldo']:,.0f}</h1>
            </div>
        """, unsafe_allow_html=True)
