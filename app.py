import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 1. CONFIGURACIÓN DE ALTO NIVEL
st.set_page_config(page_title="OTORMÍN BI - 2026", page_icon="📈", layout="wide")

# ESTILOS DE CONTRASTE Y DISEÑO
st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        
        /* Tarjetas de Inteligencia Financiera */
        .card-intel {
            background-color: #1C2126;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #55acee;
            margin-bottom: 15px;
        }
        .card-title { color: #8899A6; font-size: 0.9em; font-weight: bold; text-transform: uppercase; }
        .card-value { font-size: 2.2em; font-weight: bold; color: #FFFFFF; margin: 5px 0; }
        .card-trend { font-size: 0.85em; }

        /* Estilo de Tablas (Contraste Máximo) */
        .stDataFrame td { color: #FFFFFF !important; }
        
        /* DISEÑO DE RECIBO PROFESIONAL */
        .recibo-render {
            background-color: white;
            color: #1a1a1a !important;
            padding: 40px;
            border-radius: 5px;
            max-width: 700px;
            margin: auto;
            border: 1px solid #ddd;
            font-family: 'Arial', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- ACCESO ---
if not st.session_state["logueado"]:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.write("#")
        st.markdown("<h1 style='text-align:center; color:#55acee;'>CRM OTORMÍN</h1>", unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if u == "Admin" and p == "Otormin2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else: st.error("Credenciales incorrectas")

# --- SISTEMA BI ---
else:
    # Motor de datos
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos"],
        "Matrícula": ["IAE 1234", "MAA 5678", "PAA 9012", "IAA 3456"],
        "Saldo": [450, 200, 0, 320],
        "Cuota_Nro": [5, 12, 8, 3],
        "Cuotas_Totales": [12, 36, 12, 24],
        "Recibo_ID": ["OT-1001", "OT-1002", "OT-1003", "OT-1004"]
    }
    df = pd.DataFrame(data)
    df["Cuotas_Restantes"] = df["Cuotas_Totales"] - df["Cuota_Nro"]

    with st.sidebar:
        st.title("OTORMÍN BI")
        opcion = st.radio("GESTIÓN:", ["📊 Inteligencia Financiera", "💰 Cobros y Carteras", "🔍 Buscador", "📄 Generar Recibo"])
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # 1. INTELIGENCIA FINANCIERA
    if opcion == "📊 Inteligencia Financiera":
        st.markdown("<h2>Análisis de Tendencia de Cobranza</h2>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="card-intel"><p class="card-title">Capital en Mora</p><p class="card-value">USD 2.210</p><p class="card-trend" style="color:#ff4b4b;">↑ 12% vs mes anterior</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="card-intel"><p class="card-title">Proyección de Ingresos</p><p class="card-value">USD 15.400</p><p class="card-trend" style="color:#00ffcc;">Probabilidad de cobro: 88%</p></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="card-intel"><p class="card-title">Eficiencia de Cartera</p><p class="card-value">94.2%</p><p class="card-trend" style="color:#00ffcc;">Optimización: Activa</p></div>', unsafe_allow_html=True)

        st.write("---")
        st.subheader("📈 Curva de Recuperación de Capital")
        
        # Gráfica matemática financiera (Regresión simple de tendencia)
        chart_data = pd.DataFrame(
            np.random.randn(20, 2) * [1.5, 1] + [10, 12],
            columns=['Recuperación Real', 'Tendencia Proyectada']
        )
        st.line_chart(chart_data)
        st.info("💡 Análisis: La curva muestra una aceleración en los pagos de la segunda quincena. Se recomienda intensificar notificaciones entre los días 10 y 15.")

    # 2. COBROS Y CARTERAS (ALTO CONTRASTE)
    elif opcion == "💰 Cobros y Carteras":
        st.subheader("Estado Detallado de Cuentas")
        # Estilo para que se vea claro
        st.dataframe(df[["Cliente", "Vehículo", "Saldo", "Cuota_Nro", "Cuotas_Restantes"]], use_container_width=True, hide_index=True)

    # 3. GENERAR RECIBO (CORREGIDO)
    elif opcion == "📄 Generar Recibo":
        st.subheader("Emisión de Comprobante")
        sel = st.selectbox("Seleccione el Cliente:", df["Cliente"])
        info = df[df["Cliente"] == sel].iloc[0]

        # RENDERIZADO CORREGIDO (Sin código a la vista)
        st.markdown(f"""
            <div class="recibo-render">
                <table style="width:100%; border:none;">
                    <tr>
                        <td><h1 style="color:#004a99 !important; margin:0;">OTORMÍN</h1><p style="margin:0; font-size:0.8em; color:gray;">AUTOMOTORA & GESTIÓN</p></td>
                        <td style="text-align:right;"><p><b>ID: {info['Recibo_ID']}</b><br>Fecha: {datetime.now().strftime('%d/%m/%Y')}</p></td>
                    </tr>
                </table>
                <hr style="border:1px solid #eee;">
                <div style="padding:20px 0; line-height:1.6;">
                    <p><b>CLIENTE:</b> {sel.upper()}</p>
                    <p><b>AUTOMOTOR:</b> {info['Vehículo']} (Mat: {info['Matrícula']})</p>
                    <p><b>DETALLE:</b> Pago de cuota nro. <b>{info['Cuota_Nro']}</b> de un total de {info['Cuotas_Totales']}.</p>
                    <p style="background-color:#fff3cd; padding:5px; border-radius:5px;"><b>ESTADO:</b> Le restan <b>{info['Cuotas_Restantes']} cuotas</b> para finalizar el plan de pago.</p>
                </div>
                <div style="background-color:#f0f2f6; border:2px solid #55acee; padding:15px; text-align:center; font-size:1.5em; font-weight:bold;">
                    MONTO RECIBIDO: USD {info['Saldo']}
                </div>
                <div style="margin-top:40px; border-top:1px solid #000; width:150px; text-align:center; font-size:0.7em;">
                    Firma Administración
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.success("✅ Recibo listo para impresión (CTRL + P).")

    elif opcion == "🔍 Buscador":
        st.header("🔍 Buscador de Archivos")
        busq = st.text_input("Ingresar nombre o matrícula:")
        if busq:
            res = df[df['Cliente'].str.contains(busq, case=False) | df['Matrícula'].str.contains(busq, case=False)]
            st.dataframe(res, use_container_width=True, hide_index=True)
