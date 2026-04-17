import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime

# 1. CONFIGURACIÓN BI - OTORMÍN
st.set_page_config(page_title="OTORMÍN BI - 2026", page_icon="📈", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        
        /* Tarjetas de Inteligencia */
        .card-intel {
            background-color: #1C2126;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #55acee;
            margin-bottom: 15px;
        }
        .card-title { color: #8899A6; font-size: 0.9em; font-weight: bold; }
        .card-value { font-size: 2.2em; font-weight: bold; color: #FFFFFF; }

        /* Estilo Semáforo */
        .status-pill {
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.8em;
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
                else: st.error("Acceso denegado")

# --- SISTEMA ---
else:
    # 4. MOTOR DE DATOS (Agregamos Teléfono para WhatsApp y Riesgo)
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma"],
        "Telefono": ["59899123456", "59899111222", "59899333444", "59899555666"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos"],
        "Matrícula": ["IAE 1234", "MAA 5678", "PAA 9012", "IAA 3456"],
        "Saldo": [450, 200, 0, 320],
        "Cuota_Nro": [5, 12, 8, 3],
        "Cuotas_Totales": [12, 36, 12, 24],
        "Riesgo": ["🔴 Crítico", "🟡 Regular", "🟢 Excelente", "🔴 Crítico"]
    }
    df = pd.DataFrame(data)

    with st.sidebar:
        st.title("OTORMÍN BI")
        opcion = st.radio("GESTIÓN:", ["📊 Inteligencia", "💰 Cobros & WhatsApp", "🧮 Simulador Refinanc.", "📄 Recibos"])
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # --- 1. INTELIGENCIA ---
    if opcion == "📊 Inteligencia":
        st.markdown("<h2>Análisis de Salud de Cartera</h2>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown('<div class="card-intel"><p class="card-title">MOROSIDAD</p><p class="card-value">USD 2.210</p></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="card-intel"><p class="card-title">PROYECCIÓN</p><p class="card-value">USD 15.400</p></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="card-intel"><p class="card-title">EFICIENCIA</p><p class="card-value">94.2%</p></div>', unsafe_allow_html=True)
        st.area_chart(np.random.randn(15, 2) + [10, 10])

    # --- 2. COBROS & WHATSAPP ---
    elif opcion == "💰 Cobros & WhatsApp":
        st.subheader("Gestión Directa de Cobranza")
        
        for index, row in df.iterrows():
            with st.expander(f"{row['Riesgo']} | {row['Cliente']} - {row['Vehículo']}"):
                col1, col2 = st.columns([2,1])
                with col1:
                    st.write(f"**Saldo Pendiente:** USD {row['Saldo']}")
                    st.write(f"**Cuota:** {row['Cuota_Nro']} de {row['Cuotas_Totales']}")
                with col2:
                    # Link dinámico de WhatsApp
                    msg = f"Hola {row['Cliente']}, Automotora Otormín le informa que tiene un saldo pendiente de USD {row['Saldo']} por su {row['Vehículo']}. Quedamos a las órdenes."
                    ws_link = f"https://wa.me/{row['Telefono']}?text={urllib.parse.quote(msg)}"
                    st.markdown(f'''<a href="{ws_link}" target="_blank" style="text-decoration:none;">
                        <button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer;">
                            📲 Notificar WhatsApp
                        </button></a>''', unsafe_allow_html=True)

    # --- 3. SIMULADOR DE REFINANCIACIÓN ---
    elif opcion == "🧮 Simulador Refinanc.":
        st.subheader("Simulador de Refinanciación de Deuda")
        cliente_ref = st.selectbox("Seleccionar Cliente para Refinanciar:", df[df["Saldo"] > 0]["Cliente"])
        deuda_act = df[df["Cliente"] == cliente_ref]["Saldo"].values[0]
        
        st.warning(f"Deuda actual de {cliente_ref}: **USD {deuda_act}**")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            nuevas_cuotas = st.slider("Nuevas Cuotas:", 1, 12, 3)
            tasa_interes = st.slider("Tasa de interés mensual (%):", 0.0, 5.0, 1.5)
        
        # Cálculo de Interés Simple para refinanciación rápida
        interes_total = deuda_act * (tasa_interes / 100) * nuevas_cuotas
        total_refinanciado = deuda_act + interes_total
        valor_cuota = total_refinanciado / nuevas_cuotas
        
        with col_s2:
            st.markdown(f"""
                <div style="background-color:#1E2329; padding:20px; border-radius:10px; border:1px solid #55acee;">
                    <h4 style="margin:0;">Nueva Estructura</h4>
                    <p>Total con Interés: <b>USD {total_refinanciado:,.2f}</b></p>
                    <p>Valor por Cuota: <b>USD {valor_cuota:,.2f}</b></p>
                    <p>Costo del Refinanciamiento: USD {interes_total:,.2f}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("✅ Aplicar Refinanciación"):
                st.success("Propuesta de refinanciación preparada para el cliente.")

    # --- 4. RECIBOS ---
    elif opcion == "📄 Recibos":
        sel = st.selectbox("Cliente:", df["Cliente"])
        info = df[df["Cliente"] == sel].iloc[0]
        st.markdown(f"""
            <div style="background-color:white; color:black; padding:30px; border-radius:5px;">
                <h2 style="color:#004a99 !important;">OTORMÍN</h2>
                <hr>
                <p><b>CLIENTE:</b> {sel}</p>
                <p><b>VEHÍCULO:</b> {info['Vehículo']} ({info['Matrícula']})</p>
                <p><b>CUOTA NRO:</b> {info['Cuota_Nro']} | <b>TOTAL:</b> USD {info['Saldo']}</p>
                <p style="color:gray; font-size:0.8em;">Faltan {info['Cuotas_Totales'] - info['Cuota_Nro']} cuotas para finalizar.</p>
            </div>
        """, unsafe_allow_html=True)
