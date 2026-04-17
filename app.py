import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime

# 1. CONFIGURACIÓN Y ESTILO
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

# 2. GESTIÓN DE BASE DE DATOS EN MEMORIA (Para pruebas)
if "db_clientes" not in st.session_state:
    # Datos iniciales de ejemplo
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
        opcion = st.radio("MÓDULOS:", [
            "📥 Cargar Nuevo Cliente",
            "📊 Dashboard Financiero", 
            "💰 Caja & WhatsApp", 
            "🧮 Refinanciación",
            "📄 Emisión de Recibos"
        ])
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # --- MÓDULO 1: CARGA DE DATOS (NUEVO) ---
    if opcion == "📥 Cargar Nuevo Cliente":
        st.subheader("📝 Registro de Nueva Operación")
        st.info("Completá los datos para que se impacten en el Dashboard y la lista de Cobros.")
        
        with st.form("form_carga"):
            c1, c2 = st.columns(2)
            with c1:
                nuevo_nombre = st.text_input("Nombre y Apellido del Cliente")
                nuevo_tel = st.text_input("Teléfono (Ej: 59899...)")
                nuevo_auto = st.text_input("Vehículo (Marca y Modelo)")
                nueva_mat = st.text_input("Matrícula")
            with c2:
                nuevo_saldo = st.number_input("Saldo Pendiente (USD)", min_value=0)
                n_cuota = st.number_input("Cuota Actual", min_value=1)
                t_cuotas = st.number_input("Total de Cuotas del Plan", min_value=1)
                nuevo_riesgo = st.selectbox("Calificación de Riesgo", ["🟢 Excelente", "🟡 Regular", "🔴 Crítico"])
            
            if st.form_submit_button("💾 GUARDAR EN CARTERA"):
                nuevo_reg = {
                    "Cliente": nuevo_nombre, "Telefono": nuevo_tel, "Vehículo": nuevo_auto,
                    "Matrícula": nueva_mat, "Saldo": nuevo_saldo, "Cuota_Nro": n_cuota,
                    "Cuotas_Totales": t_cuotas, "Riesgo": nuevo_riesgo, 
                    "Recibo_ID": f"OT-{np.random.randint(2000, 9999)}"
                }
                # Actualizar la base de datos en memoria
                st.session_state.db_clientes = pd.concat([st.session_state.db_clientes, pd.DataFrame([nuevo_reg])], ignore_index=True)
                st.success(f"¡Cliente {nuevo_nombre} cargado con éxito!")

    # --- MÓDULO 2: DASHBOARD (Usa los datos cargados) ---
    elif opcion == "📊 Dashboard Financiero":
        st.subheader("Análisis de Solvencia")
        df_act = st.session_state.db_clientes
        mora_total = df_act["Saldo"].sum()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Capital en Mora", f"USD {mora_total:,}")
        c2.metric("Clientes Activos", len(df_act))
        c3.metric("Ratio de Riesgo Crítico", f"{len(df_act[df_act['Riesgo'] == '🔴 Crítico'])}")
        
        st.write("---")
        st.dataframe(df_act[["Cliente", "Vehículo", "Saldo", "Riesgo"]], use_container_width=True)

    # --- MÓDULO 3: COBROS & WHATSAPP ---
    elif opcion == "💰 Caja & WhatsApp":
        st.subheader("Gestión de Cobranza Directa")
        df_act = st.session_state.db_clientes
        for i, r in df_act.iterrows():
            with st.expander(f"{r['Riesgo']} | {r['Cliente']} - {r['Vehículo']}"):
                st.write(f"**Deuda:** USD {r['Saldo']} | **Cuota:** {r['Cuota_Nro']}/{r['Cuotas_Totales']}")
                msg = f"Otormín: Hola {r['Cliente']}, recordamos saldo de USD {r['Saldo']}."
                ws_url = f"https://wa.me/{r['Telefono']}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{ws_url}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; width:100%;">📲 WhatsApp</button></a>', unsafe_allow_html=True)

    # --- MÓDULO 4: RECIBOS ---
    elif opcion == "📄 Emisión de Recibos":
        df_act = st.session_state.db_clientes
        sel = st.selectbox("Titular:", df_act["Cliente"])
        inf = df_act[df_act["Cliente"] == sel].iloc[0]
        
        st.markdown(f"""
            <div class="recibo-render">
                <table style="width:100%; color:black;">
                    <tr>
                        <td><h2 style="color:#004a99 !important; margin:0;">OTORMÍN</h2></td>
                        <td style="text-align:right;"><b>ID: {inf['Recibo_ID']}</b><br>{datetime.now().strftime('%d/%m/%Y')}</td>
                    </tr>
                </table>
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
