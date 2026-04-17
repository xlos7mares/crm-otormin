import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN VISUAL (ESTILO NEGRO PROFESIONAL)
st.set_page_config(page_title="CRM OTORMÍN 2026", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: #E1E8ED; }
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        h1, h2, h3 { color: #55acee !important; text-align: center; }
        
        /* DISEÑO DEL RECIBO TIPO HOJA REAL */
        .recibo-box {
            background-color: white;
            color: #1a1a1a;
            padding: 40px;
            border-radius: 8px;
            font-family: 'Arial', sans-serif;
            max-width: 750px;
            margin: auto;
            border: 1px solid #ccc;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }
        .header-recibo {
            border-bottom: 3px solid #55acee;
            padding-bottom: 10px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .datos-cliente { line-height: 1.8; font-size: 1.1em; }
        .monto-box {
            background-color: #f0f2f6;
            border: 2px solid #55acee;
            padding: 15px;
            text-align: center;
            font-size: 1.6em;
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# 2. ACCESO
if not st.session_state["logueado"]:
    st.write("#")
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

# 3. INTERFAZ DE GESTIÓN
else:
    # Datos actualizados con cuotas restantes
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos"],
        "Matrícula": ["IAE 1234", "MAA 5678", "PAA 9012", "IAA 3456"],
        "Saldo": [450, 200, 0, 320],
        "Cuota_Nro": [5, 12, 8, 3],
        "Cuotas_Restantes": [7, 24, 0, 21],
        "Recibo_ID": ["OT-1001", "OT-1002", "OT-1003", "OT-1004"]
    }
    df = pd.DataFrame(data)

    with st.sidebar:
        st.title("OTORMÍN")
        opcion = st.radio("MENÚ:", ["📊 Tablero", "💰 Cobros", "🔍 Buscador", "📄 Recibos"])
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    if opcion == "📄 Recibos":
        st.header("📄 Generador de Comprobantes Oficiales")
        sel = st.selectbox("Seleccione el Cliente:", df["Cliente"])
        info = df[df["Cliente"] == sel].iloc[0]

        # RENDERIZADO DEL RECIBO PROFESIONAL
        st.markdown(f"""
            <div class="recibo-box">
                <div class="header-recibo">
                    <div>
                        <h1 style="color: #004a99 !important; margin:0; text-align:left;">OTORMÍN</h1>
                        <small>AUTOMOTORA & GESTIÓN</small>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin:0;"><b>RECIBO INTERNO:</b> {info['Recibo_ID']}</p>
                        <p style="margin:0;"><b>FECHA:</b> {datetime.now().strftime('%d/%m/%Y')}</p>
                    </div>
                </div>
                
                <div class="datos-cliente">
                    <p><b>CLIENTE:</b> {sel.upper()}</p>
                    <p><b>VEHÍCULO:</b> {info['Vehículo']} (Matrícula: {info['Matrícula']})</p>
                    <p><b>DETALLE DE PAGO:</b> Pago de cuota nro. {info['Cuota_Nro']}</p>
                    <p><b>PENDIENTES:</b> Al cliente le restan <b>{info['Cuotas_Restantes']}</b> cuotas para finalizar el plan.</p>
                </div>
                
                <div class="monto-box">
                    IMPORTE: USD {info['Saldo']}
                </div>
                
                <div style="margin-top: 50px; display: flex; justify-content: space-around;">
                    <div style="border-top: 1px solid black; width: 200px; text-align: center;">
                        <p style="font-size: 0.8em;">Firma Administración</p>
                    </div>
                    <div style="border-top: 1px solid black; width: 200px; text-align: center;">
                        <p style="font-size: 0.8em;">Firma Cliente</p>
                    </div>
                </div>
                <p style="text-align: center; font-size: 0.7em; color: gray; margin-top: 30px;">
                    Paysandú, Uruguay - Sistema CRM Otormín 2026
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.success("✅ Recibo generado correctamente. Para guardarlo como PDF o imprimirlo, presiona **CTRL + P**.")

    elif opcion == "📊 Tablero":
        st.metric("MOROSIDAD", "5 Clientes", "USD 2.210")
        st.area_chart([10, 25, 15, 30, 45])

    elif opcion == "💰 Cobros":
        st.subheader("Estado de Cuentas")
        st.table(df[["Cliente", "Vehículo", "Saldo", "Cuota_Nro", "Cuotas_Restantes"]])

    elif opcion == "🔍 Buscador":
        st.header("🔍 Buscador de Archivos")
        busq = st.text_input("Ingresar nombre:")
        res = df[df['Cliente'].str.contains(busq, case=False)]
        st.dataframe(res, use_container_width=True, hide_index=True)
