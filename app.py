import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
from datetime import datetime
import PIL.Image as Image

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="CRM OTORMÍN 2026", 
    page_icon="🚗", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. CONTROL DE SESIÓN
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- PANTALLA DE ACCESO (LOGIN) ---
if not st.session_state["logueado"]:
    st.markdown("<style>.stApp { background-color: #0E1117; color: white; }</style>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.write("#")
        # Intentamos cargar el logo de Otormín si ya lo subiste
        try:
            logo_login = Image.open("logo.png")
            st.image(logo_login, use_container_width=True)
        except:
            st.markdown("<h1 style='text-align: center; color: #55acee;'>🚗 CRM OTORMÍN 2026</h1>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='text-align: center;'>Gestión de Cartera Exclusiva</h3>", unsafe_allow_html=True)
        
        with st.form("login_otormin"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR AL SISTEMA"):
                # Puedes cambiar estas credenciales solo para Otormín
                if u == "Admin" and p == "Otormin2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else: 
                    st.error("Credenciales de acceso incorrectas para Otormín")

# --- SISTEMA ACTIVO (POST-LOGIN) ---
else:
    # Estilos de la marca Otormín
    st.markdown("""
        <style>
            .stApp { background-color: #0E1117; color: white; }
            [data-testid="stSidebar"] { background-color: #161B22; }
            .card {
                background-color: #1E2329;
                padding: 20px;
                border-radius: 10px;
                border-top: 4px solid #55acee;
                text-align: center;
                margin-bottom: 20px;
            }
            .titulo-central {
                text-align: center;
                color: white;
                font-size: 2.2rem;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # Base de datos centralizada
    @st.cache_data
    def cargar_datos_otormin():
        data = {
            "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
            "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
            "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
            "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
            "Saldo (USD)": [450, 0, 0, 320, 0],
            "latitude": [-32.3162, -32.3210, -32.3050, -32.3320, -32.3120],
            "longitude": [-58.0850, -58.0790, -58.0910, -58.0820, -58.1000]
        }
        df = pd.DataFrame(data)
        
        # WhatsApp con mensaje personalizado de Otormín
        def link_wa(fila):
            msg = f"Automotora Otormín Informa: Estimado {fila['Cliente']}, le recordamos que su cuota del vehículo {fila['Vehículo']} se encuentra {fila['Estado']}. Saldo a liquidar: ${fila['Saldo (USD)']}. Saludos cordiales."
            return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
        
        df["WhatsApp"] = df.apply(link_wa, axis=1)
        return df

    df = cargar_datos_otormin()

    # --- NAVEGACIÓN LATERAL ---
    with st.sidebar:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            st.markdown("<h2 style='color:#55acee; text-align:center;'>OTORMÍN</h2>", unsafe_allow_html=True)
        
        st.markdown("### PANEL DE CONTROL")
        opcion = st.radio("Módulos Operativos:", [
            "📊 Inteligencia Otormín", 
            "💰 Gestión de Cobros", 
            "🔍 Buscador de Archivo",
            "📄 Documentos PDF",
            "📍 Mapa de Deudores"
        ])
        st.write("---")
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()
        st.info("Licencia Activa: Automotora Otormín")

    # --- CONTENIDO DE CADA MÓDULO ---
    st.markdown(f'<div class="titulo-central">CRM OTORMÍN - {opcion.upper()}</div>', unsafe_allow_html=True)
    st.write("---")

    if opcion == "📊 Inteligencia Otormín":
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown('<div class="card"><h3 style="color:#8899A6">EN MORA</h3><h2 style="color:#ff4b4b">5</h2><p>USD 2.210</p></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="card"><h3 style="color:#8899A6">A COBRAR</h3><h2 style="color:#55acee">4</h2><p>USD 1.850</p></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="card"><h3 style="color:#8899A6">TOTAL CARTERA</h3><h2>20</h2><p>USD 15.400</p></div>', unsafe_allow_html=True)
        st.subheader("📈 Proyección de Ingresos Otormín")
        st.line_chart({"Cobros Estimados": [15, 30, 22, 45, 38]})

    elif opcion == "💰 Gestión de Cobros":
        st.subheader("📋 Listado de Cartera y Cobranza")
        def color_estado(val):
            if val == "VENCIDO": return 'background-color: #701010; color: white'
            return 'background-color: #155123; color: white'
        
        st.dataframe(
            df.style.map(color_estado, subset=['Estado']),
            use_container_width=True, hide_index=True,
            column_config={
                "WhatsApp": st.column_config.LinkColumn("Notificar", display_text="📲 WhatsApp"),
                "Saldo (USD)": st.column_config.NumberColumn(format="$ %d")
            }
        )

    elif opcion == "🔍 Buscador de Archivo":
        busq = st.text_input("Buscar cliente por nombre o vehículo...", placeholder="Ej: Mercedes")
        if busq:
            res = df[df['Cliente'].str.contains(busq, case=False) | df['Vehículo'].str.contains(busq, case=False)]
            for _, r in res.iterrows():
                with st.expander(f"👤 FICHA DIGITAL: {r['Cliente']}"):
                    st.write(f"**Vehículo:** {r['Vehículo']}")
                    st.write(f"**Vencimiento:** {r['Vencimiento']}")
                    st.write(f"**Estado:** {r['Estado']}")
                    st.markdown(f"[📲 Enviar Recordatorio Otormín]({r['WhatsApp']})")

    elif opcion == "📄 Documentos PDF":
        st.subheader("📄 Generación Instantánea de Documentos")
        sel_c = st.selectbox("Seleccione Cliente:", df["Cliente"])
        tipo = st.radio("Documento a generar:", ["Recibo de Pago", "Convenio de Refinanciación", "Estado de Cuenta"])
        if st.button(f"Imprimir {tipo}"):
            st.success(f"El documento '{tipo}' para {sel_c} ha sido generado exitosamente.")
            st.info("Formato profesional con cabecera de Automotora Otormín.")

    elif opcion == "📍 Mapa de Deudores":
        st.subheader("📍 Geolocalización en Paysandú")
        # El mapa usa las columnas latitude y longitude de los datos cargados arriba
        st.map(df[["latitude", "longitude"]], color="#ff4b4b", size=40)
        st.info("💡 Mapa optimizado para rutas de cobro de Otormín.")
