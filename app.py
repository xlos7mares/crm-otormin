import streamlit as st
import pandas as pd
import urllib.parse

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="CRM OTORMÍN 2026",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTADO DE SESIÓN
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- ESTILOS VISUALES ---
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
    </style>
""", unsafe_allow_html=True)

# 3. PANTALLA DE LOGIN
if not st.session_state["logueado"]:
    _, col_centro, _ = st.columns([1, 1.5, 1])
    with col_centro:
        st.write("#")
        st.markdown("<h1 style='text-align: center; color: #55acee;'>🚗 CRM OTORMÍN 2026</h1>", unsafe_allow_html=True)
        with st.form("login_form"):
            user = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR AL SISTEMA"):
                if user == "Admin" and password == "Otormin2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else:
                    st.error("Acceso Denegado")

# 4. SISTEMA ACTIVO (POST-LOGIN)
else:
    # Datos de la Cartera (Otormín)
    @st.cache_data
    def cargar_datos():
        data = {
            "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma", "Roberto Peña"],
            "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos", "Ford Ranger"],
            "Vencimiento": ["2026-03-30", "2026-04-10", "2026-04-15", "2026-03-25", "2026-05-01"],
            "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO", "AL DÍA"],
            "Saldo (USD)": [450, 0, 0, 320, 0],
            "lat": [-32.3162, -32.3210, -32.3050, -32.3320, -32.3120],
            "lon": [-58.0850, -58.0790, -58.0910, -58.0820, -58.1000]
        }
        df = pd.DataFrame(data)
        # Link de WhatsApp
        def link_wa(fila):
            msg = f"Otormín Informa: Hola {fila['Cliente']}, cuota {fila['Vehículo']} {fila['Estado']}. Saldo: ${fila['Saldo (USD)']}."
            return f"https://wa.me/59899000000?text={urllib.parse.quote(msg)}"
        df["Notificar"] = df.apply(link_wa, axis=1)
        return df

    df = cargar_datos()

    # --- NAVEGACIÓN LATERAL ---
    with st.sidebar:
        st.title("OTORMÍN")
        st.markdown("### 🛠️ MENÚ PRINCIPAL")
        opcion = st.radio("Módulos:", [
            "📊 Tablero", 
            "💰 Cobros", 
            "🔍 Buscador",
            "📄 Documentos",
            "📍 Mapa"
        ])
        st.write("---")
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # --- CONTENIDO SEGÚN MÓDULO ---
    st.markdown(f"<h1 style='text-align: center;'>OTORMÍN - {opcion.upper()}</h1>", unsafe_allow_html=True)
    st.write("---")

    if opcion == "📊 Tablero":
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown('<div class="card"><h3 style="color:gray">EN MORA</h3><h2 style="color:red">5</h2><p>USD 2.210</p></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="card"><h3 style="color:gray">A COBRAR</h3><h2 style="color:cyan">4</h2><p>USD 1.850</p></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="card"><h3 style="color:gray">TOTAL</h3><h2>20</h2><p>USD 15.400</p></div>', unsafe_allow_html=True)
        st.subheader("📈 Proyección Semanal")
        st.line_chart({"Cobros": [15, 30, 22, 45]})

    elif opcion == "💰 Cobros":
        st.subheader("📋 Gestión de Cartera")
        # Semáforo de colores
        def color_estado(val):
            color = '#701010' if val == "VENCIDO" else '#155123'
            return f'background-color: {color}; color: white'
        
        st.dataframe(
            df.style.map(color_estado, subset=['Estado']),
            use_container_width=True, hide_index=True,
            column_config={"Notificar": st.column_config.LinkColumn(display_text="📲 WhatsApp")}
        )

    elif opcion == "🔍 Buscador":
        busqueda = st.text_input("Buscar por nombre o vehículo:")
        if busqueda:
            res = df[df['Cliente'].str.contains(busqueda, case=False) | df['Vehículo'].str.contains(busqueda, case=False)]
            for _, r in res.iterrows():
                with st.expander(f"👤 {r['Cliente']} - {r['Vehículo']}"):
                    st.write(f"Estado: {r['Estado']} | Saldo: ${r['Saldo (USD)']}")
                    st.markdown(f"[📲 Enviar Recordatorio]({r['Notificar']})")

    elif opcion == "📄 Documentos":
        st.subheader("📄 Generación de Comprobantes")
        cliente_sel = st.selectbox("Seleccione Cliente:", df["Cliente"])
        if st.button("Generar Recibo Oficial"):
            st.success(f"Recibo de Automotora Otormín para {cliente_sel} generado.")
            st.info("Módulo de descarga habilitado para versión Pro.")

    elif opcion == "📍 Mapa":
        st.subheader("📍 Geolocalización en Paysandú")
        # Renombramos para que el mapa lo tome directo
        df_mapa = df.rename(columns={'lat': 'latitude', 'lon': 'longitude'})
        st.map(df_mapa[["latitude", "longitude"]], color="#ff4b4b", size=40)
