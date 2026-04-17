import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime

# 1. CONFIGURACIÓN DE ALTO NIVEL
st.set_page_config(page_title="OTORMÍN BI - SISTEMA CONTABLE", page_icon="🏦", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        
        .card-intel {
            background-color: #1C2126;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #55acee;
            margin-bottom: 15px;
        }
        .card-title { color: #8899A6; font-size: 0.9em; font-weight: bold; text-transform: uppercase; }
        .card-value { font-size: 2.2em; font-weight: bold; color: #FFFFFF; margin: 5px 0; }
        
        .recibo-render {
            background-color: white;
            color: #1a1a1a !important;
            padding: 40px;
            border-radius: 5px;
            max-width: 700px;
            margin: auto;
            border: 1px solid #ddd;
        }
    </style>
""", unsafe_allow_html=True)

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- ACCESO ---
if not st.session_state["logueado"]:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 style='text-align:center; color:#55acee;'>🏦 GESTIÓN OTORMÍN</h1>", unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if u == "Admin" and p == "Otormin2026":
                    st.session_state["logueado"] = True
                    st.rerun()
                else: st.error("Acceso denegado")

else:
    # 4. MOTOR DE DATOS CONTABLES
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma"],
        "Telefono": ["59899123456", "59899111222", "59899333444", "59899555666"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos"],
        "Matrícula": ["IAE 1234", "MAA 5678", "PAA 9012", "IAA 3456"],
        "Saldo_Pendiente": [450, 200, 0, 320],
        "Cuota_Nro": [5, 12, 8, 3],
        "Cuotas_Totales": [12, 36, 12, 24],
        "Riesgo": ["🔴 Crítico", "🟡 Regular", "🟢 Excelente", "🔴 Crítico"],
        "Ultimo_Pago": ["2026-03-10", "2026-04-05", "2026-04-15", "2026-02-28"]
    }
    df = pd.DataFrame(data)

    with st.sidebar:
        st.title("BI CONTABLE")
        opcion = st.radio("MÓDULOS:", [
            "📊 Dashboard Financiero", 
            "💰 Caja Diaria & Cobros", 
            "🧮 Refinanciación",
            "🔍 Auditoría de Cartera",
            "📄 Emisión de Recibos"
        ])
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # 1. DASHBOARD FINANCIERO (INTELIGENCIA)
    if opcion == "📊 Dashboard Financiero":
        st.markdown("<h2>Análisis de Solvencia y Cartera</h2>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown('<div class="card-intel"><p class="card-title">Cuentas a Cobrar</p><p class="card-value">USD 2.210</p></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="card-intel"><p class="card-title">Cash Flow Proyectado</p><p class="card-value">USD 15.400</p></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="card-intel"><p class="card-title">Ratio de Cobro</p><p class="card-value">94.2%</p></div>', unsafe_allow_html=True)
        
        st.subheader("📈 Proyección de Liquidez Mensual")
        st.line_chart(np.random.randn(10, 2) + [15, 15])

    # 2. CAJA DIARIA & COBROS (WHATSAPP INTEGRADO)
    elif opcion == "💰 Caja Diaria & Cobros":
        st.subheader("Registro de Ingresos y Gestión WhatsApp")
        for i, r in df.iterrows():
            with st.expander(f"{r['Riesgo']} | {r['Cliente']} - {r['Vehículo']}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**Deuda Actual:** USD {r['Saldo_Pendiente']}")
                    st.write(f"**Último Pago registrado:** {r['Ultimo_Pago']}")
                with col2:
                    msg = f"Otormín Finanzas: Hola {r['Cliente']}, recordamos saldo pendiente de USD {r['Saldo_Pendiente']} por su {r['Vehículo']}."
                    ws_url = f"https://wa.me/{r['Telefono']}?text={urllib.parse.quote(msg)}"
                    st.markdown(f'<a href="{ws_url}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; width:100%;">📲 Cobrar vía WhatsApp</button></a>', unsafe_allow_html=True)

    # 3. REFINANCIACIÓN (MATEMÁTICA APLICADA)
    elif opcion == "🧮 Refinanciación":
        st.subheader("Simulador de Estructura de Deuda")
        cli = st.selectbox("Seleccionar Deudor:", df[df["Saldo_Pendiente"] > 0]["Cliente"])
        monto = df[df["Cliente"] == cli]["Saldo_Pendiente"].values[0]
        
        c_a, c_b = st.columns(2)
        with c_a:
            cuotas = st.number_input("Extender a cuántas cuotas:", 1, 24, 6)
            interes = st.slider("Tasa de mora mensual (%):", 0.0, 5.0, 2.5)
        
        total = monto * (1 + (interes/100) * cuotas)
        cuota_val = total / cuotas
        
        with c_b:
            st.markdown(f"""
                <div style="background-color:#1E2329; padding:20px; border-radius:10px; border:1px solid #55acee;">
                    <h4>Nueva Liquidación</h4>
                    <p>Monto Original: USD {monto}</p>
                    <p>Intereses Generados: USD {total - monto:,.2f}</p>
                    <p><b>Nueva Cuota: USD {cuota_val:,.2f}</b></p>
                </div>
            """, unsafe_allow_html=True)

    # 4. EMISIÓN DE RECIBOS (CONTABILIDAD FORMAL)
    elif opcion == "📄 Emisión de Recibos":
        sel = st.selectbox("Titular:", df["Cliente"])
        inf = df[df["Cliente"] == sel].iloc[0]
        
        st.markdown(f"""
            <div class="recibo-render">
                <table style="width:100%; color:black;">
                    <tr>
                        <td><h2 style="color:#004a99 !important; margin:0;">OTORMÍN</h2></td>
                        <td style="text-align:right;"><b>No: {inf['Recibo_ID']}</b><br>{datetime.now().strftime('%d/%m/%Y')}</td>
                    </tr>
                </table>
                <hr style="border:0.5px solid #eee;">
                <div style="color:black; line-height:1.8;">
                    <p><b>CLIENTE:</b> {sel.upper()}</p>
                    <p><b>UNIDAD:</b> {inf['Vehículo']} (Mat: {inf['Matrícula']})</p>
                    <p><b>CONCEPTO:</b> Cuota nro {inf['Cuota_Nro']} de {inf['Cuotas_Totales']}.</p>
                    <p style="background-color:#fff3cd; padding:5px;"><b>PROYECCIÓN:</b> Restan {inf['Cuotas_Totales'] - inf['Cuota_Nro']} cuotas para la liberación del título.</p>
                </div>
                <div style="background-color:#f0f2f6; border:2px solid #55acee; padding:15px; text-align:center; font-size:1.5em; font-weight:bold; color:black;">
                    VALOR RECIBIDO: USD {inf['Saldo_Pendiente']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.success("✅ Documento contable listo. CTRL+P para imprimir.")
