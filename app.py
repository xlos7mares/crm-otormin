import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN Y ESTILO NEGRO (ORDENADO)
st.set_page_config(page_title="CRM OTORMÍN 2026", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: #E1E8ED; }
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        h1, h2, h3 { color: #55acee !important; text-align: center; }
        
        /* Contenedor del recibo para que se vea como una hoja real */
        .recibo-hoja {
            background-color: white;
            color: black;
            padding: 40px;
            border-radius: 5px;
            font-family: 'Courier New', Courier, monospace;
            max-width: 700px;
            margin: auto;
            border: 1px solid #ddd;
            box-shadow: 0 4px 8px rgba(0,0,0,0.5);
        }
        
        /* Fix para el gráfico */
        .chart-container { max-width: 800px; margin: auto; }
    </style>
""", unsafe_allow_html=True)

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# 2. LOGIN
if not st.session_state["logueado"]:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1>🚗 CRM OTORMÍN</h1>", unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if u == "Admin" and p == "Otormin2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else: st.error("Acceso Incorrecto")

# 3. SISTEMA ACTIVO
else:
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos"],
        "Matrícula": ["IAE 1234", "MAA 5678", "PAA 9012", "IAA 3456"],
        "Estado": ["VENCIDO", "AL DÍA", "AL DÍA", "VENCIDO"],
        "Saldo": [450, 0, 0, 320],
        "Cuota": [5, 12, 8, 3],
        "Recibo": ["OT-1001", "OT-1002", "OT-1003", "OT-1004"]
    }
    df = pd.DataFrame(data)

    with st.sidebar:
        st.title("OTORMÍN")
        opcion = st.radio("MENÚ:", ["📊 Tablero", "💰 Cobros", "🔍 Buscador", "📄 Documentos"])
        if st.button("🚪 Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # --- TABLERO ---
    if opcion == "📊 Tablero":
        st.markdown("<h2>Resumen Operativo</h2>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("EN MORA", "5", "USD 2.210")
        c2.metric("A COBRAR", "4", "USD 1.850")
        c3.metric("TOTAL", "20", "USD 15.400")
        
        st.write("---")
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 Proyección de Cobranza")
        st.area_chart([12, 18, 14, 25, 30])
        st.markdown('</div>', unsafe_allow_html=True)

    # --- DOCUMENTOS (RECIBO PROFESIONAL SIN LIBRERÍAS) ---
    elif opcion == "📄 Documentos":
        st.header("📄 Generador de Recibos Oficiales")
        sel = st.selectbox("Seleccione Cliente:", df["Cliente"])
        info = df[df["Cliente"] == sel].iloc[0]

        # El Recibo en pantalla
        st.markdown(f"""
            <div class="recibo-hoja">
                <h1 style="color: #004a99 !important; text-align: center; margin: 0;">AUTOMOTORA OTORMÍN</h1>
                <p style="text-align: center; font-size: 0.8em; color: #555;">PAYSANDÚ - URUGUAY</p>
                <hr>
                <div style="display: flex; justify-content: space-between;">
                    <span><b>RECIBO:</b> {info['Recibo']}</span>
                    <span><b>FECHA:</b> {datetime.now().strftime('%d/%m/%Y')}</span>
                </div>
                <br>
                <p><b>CLIENTE:</b> {sel}</p>
                <p><b>AUTOMOTOR:</b> {info['Vehículo']} (Matrícula: {info['Matrícula']})</p>
                <p><b>CUOTA NRO:</b> {info['Cuota']}</p>
                <br>
                <div style="border: 2px solid black; padding: 10px; text-align: center; font-size: 1.5em;">
                    <b>IMPORTE: USD {info['Saldo']}</b>
                </div>
                <br><br><br>
                <div style="border-top: 1px solid black; width: 200px; margin-left: auto; text-align: center;">
                    <p style="font-size: 0.8em;">Firma Administración</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.warning("💡 **Para guardar como PDF:** Presioná **CTRL + P** (o 'Imprimir' en el menú del navegador) y seleccioná **'Guardar como PDF'**.")

    elif opcion == "🔍 Buscador":
        st.header("🔍 Buscador de Cartera")
        busq = st.text_input("Nombre o Matrícula:")
        res = df[df['Cliente'].str.contains(busq, case=False) | df['Matrícula'].str.contains(busq, case=False)]
        st.dataframe(res, use_container_width=True, hide_index=True)

    elif opcion == "💰 Cobros":
        st.dataframe(df, use_container_width=True, hide_index=True)
