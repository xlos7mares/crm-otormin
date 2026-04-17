import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime

# 1. CONFIGURACIÓN DE ALTO NIVEL
st.set_page_config(page_title="OTORMÍN BI - SISTEMA INTEGRADO", page_icon="🏦", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        .card-intel {
            background-color: #1C2126; padding: 20px; border-radius: 12px;
            border-left: 5px solid #55acee; margin-bottom: 15px;
        }
        .recibo-render {
            background-color: white; color: black !important;
            padding: 40px; border-radius: 5px; max-width: 700px; margin: auto;
        }
    </style>
""", unsafe_allow_html=True)

# 2. GESTIÓN DE BASE DE DATOS EN MEMORIA
if "db_clientes" not in st.session_state:
    st.session_state.db_clientes = pd.DataFrame([
        {"Cliente": "Federico Rossi", "Telefono": "59899123456", "Vehículo": "Mercedes Benz A200", "Matrícula": "IAE 1234", "Saldo": 450, "Cuota_Nro": 5, "Cuotas_Totales": 12, "Riesgo": "🔴 Crítico", "Recibo_ID": "OT-1001"},
        {"Cliente": "María Gonzalez", "Telefono": "59899111222", "Vehículo": "Toyota Hilux", "Matrícula": "MAA 5678", "Saldo": 200, "Cuota_Nro": 12, "Cuotas_Totales": 36, "Riesgo": "🟡 Regular", "Recibo_ID": "OT-1002"}
    ])

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# --- ACCESO ---
if not st.session_state["logueado"]:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.write("#")
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
    with st.sidebar:
        st.title("BI CONTABLE")
        # NOMBRES SIMPLES PARA EVITAR ERRORES DE LECTURA
        opcion = st.radio("MÓDULOS:", [
            "Cargar Datos",
            "Dashboard", 
            "Caja & WhatsApp", 
            "Refinanciación",
            "Emisión de Recibos"
        ])
        st.write("---")
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # --- MÓDULO 1: CARGAR DATOS ---
    if opcion == "Cargar Datos":
        st.subheader("📝 Registro de Nueva Operación")
        with st.form("form_carga"):
            c1, c2 = st.columns(2)
            with c1:
                nuevo_nombre = st.text_input("Nombre del Cliente")
                nuevo_tel = st.text_input("Teléfono")
                nuevo_auto = st.text_input("Vehículo")
                nueva_mat = st.text_input("Matrícula")
            with c2:
                nuevo_saldo = st.number_input("Saldo (USD)", min_value=0)
                n_cuota = st.number_input("Cuota Actual", min_value=1)
                t_cuotas = st.number_input("Total Cuotas", min_value=1)
                nuevo_riesgo = st.selectbox("Riesgo", ["🟢 Excelente", "🟡 Regular", "🔴 Crítico"])
            
            if st.form_submit_button("💾 GUARDAR"):
                nuevo_reg = {
                    "Cliente": nuevo_nombre, "Telefono": nuevo_tel, "Vehículo": nuevo_auto,
                    "Matrícula": nueva_mat, "Saldo": nuevo_saldo, "Cuota_Nro": n_cuota,
                    "Cuotas_Totales": t_cuotas, "Riesgo": nuevo_riesgo, 
                    "Recibo_ID": f"OT-{np.random.randint(2000, 9999)}"
                }
                st.session_state.db_clientes = pd.concat([st.session_state.db_clientes, pd.DataFrame([nuevo_reg])], ignore_index=True)
                st.success("¡Cliente guardado!")

    # --- MÓDULO 2: DASHBOARD ---
    elif opcion == "Dashboard":
        st.subheader("Análisis de Solvencia")
        df_act = st.session_state.db_clientes
        c1, c2, c3 = st.columns(3)
        c1.metric("Mora Total", f"USD {df_act['Saldo'].sum():,}")
        c2.metric("Clientes", len(df_act))
        c3.metric("Críticos", len(df_act[df_act['Riesgo'] == '🔴 Crítico']))
        st.area_chart(df_act["Saldo"])

    # --- MÓDULO 3: CAJA & WHATSAPP ---
    elif opcion == "Caja & WhatsApp":
        st.subheader("Gestión de Cobranza")
        df_act = st.session_state.db_clientes
        for i, r in df_act.iterrows():
            with st.expander(f"{r['Riesgo']} | {r['Cliente']} - {r['Vehículo']}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**Deuda:** USD {r['Saldo']} | **Cuota:** {r['Cuota_Nro']}/{r['Cuotas_Totales']}")
                with col2:
                    msg = f"Otormín: Hola {r['Cliente']}, recordamos saldo de USD {r['Saldo']}."
                    ws_url = f"https://wa.me/{r['Telefono']}?text={urllib.parse.quote(msg)}"
                    st.markdown(f'<a href="{ws_url}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; width:100%;">📲 WhatsApp</button></a>', unsafe_allow_html=True)

    # --- MÓDULO 4: REFINANCIACIÓN (ESTE ES EL QUE ESTABA VACÍO) ---
    elif opcion == "Refinanciación":
        st.subheader("Simulador de Refinanciación")
        df_act = st.session_state.db_clientes
        cli = st.selectbox("Seleccionar Deudor:", df_act[df_act["Saldo"] > 0]["Cliente"])
        monto = df_act[df_act["Cliente"] == cli]["Saldo"].values[0]
        
        c_a, c_b = st.columns(2)
        with c_a:
            cuotas = st.number_input("Nuevas cuotas:", 1, 24, 6)
            interes = st.slider("Interés mensual (%):", 0.0, 10.0, 2.0)
        
        total = monto * (1 + (interes/100) * cuotas)
        
        with c_b:
            st.markdown(f"""
                <div style="background-color:#1C2126; padding:20px; border-radius:10px; border:1px solid #55acee;">
                    <h4>Nueva Liquidación</h4>
                    <p>Total con Interés: <b>USD {total:,.2f}</b></p>
                    <p>Cuota mensual: <b>USD {total/cuotas:,.2f}</b></p>
                </div>
            """, unsafe_allow_html=True)

    # --- MÓDULO 5: RECIBOS ---
    elif opcion == "Emisión de Recibos":
        df_act = st.session_state.db_clientes
        sel = st.selectbox("Titular:", df_act["Cliente"])
        inf = df_act[df_act["Cliente"] == sel].iloc[0]
        st.markdown(f"""
            <div class="recibo-render">
                <h2 style="color:#004a99 !important; text-align:center;">OTORMÍN</h2>
                <hr>
                <div style="color:black;">
                    <p><b>CLIENTE:</b> {sel.upper()}</p>
                    <p><b>UNIDAD:</b> {inf['Vehículo']} (Mat: {inf['Matrícula']})</p>
                    <p><b>CUOTA:</b> {inf['Cuota_Nro']} de {inf['Cuotas_Totales']}</p>
                </div>
                <div style="background-color:#f0f2f6; border:2px solid #55acee; padding:15px; text-align:center; font-size:1.5em; font-weight:bold; color:black;">
                    VALOR RECIBIDO: USD {inf['Saldo']}
                </div>
            </div>
        """, unsafe_allow_html=True)
