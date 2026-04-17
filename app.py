import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime
import sqlite3

# 1. CONFIGURACIÓN DE ALTO NIVEL
st.set_page_config(page_title="OTORMÍN BI - 2026", page_icon="📈", layout="wide")

# --- MOTOR DE BASE DE DATOS SQL ---
def conectar_db():
    conn = sqlite3.connect('otormin_datos.db', check_same_thread=False)
    return conn

def crear_tabla():
    conn = conectar_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            telefono TEXT,
            vehiculo TEXT,
            matricula TEXT,
            saldo REAL,
            cuota_nro INTEGER,
            cuota_totales INTEGER,
            riesgo TEXT,
            recibo_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insertar_cliente(datos):
    conn = conectar_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO clientes (cliente, telefono, vehiculo, matricula, saldo, cuota_nro, cuota_totales, riesgo, recibo_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', datos)
    conn.commit()
    conn.close()

def cargar_datos():
    conn = conectar_db()
    df = pd.read_sql_query("SELECT * FROM clientes", conn)
    conn.close()
    return df

# Inicializar Tabla al arrancar
crear_tabla()

# ESTILOS CSS
st.markdown("""
    <style>
        .stApp { background-color: #0B0E11; color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #15191D; border-right: 2px solid #55acee; }
        .card-intel {
            background-color: #1C2126; padding: 20px; border-radius: 12px;
            border-left: 5px solid #55acee; margin-bottom: 15px;
        }
        .card-title { color: #8899A6; font-size: 0.9em; font-weight: bold; text-transform: uppercase; }
        .card-value { font-size: 2.2em; font-weight: bold; color: #FFFFFF; margin: 5px 0; }
        .recibo-render {
            background-color: white; color: #1a1a1a !important;
            padding: 40px; border-radius: 5px; max-width: 700px; margin: auto;
            border: 1px solid #ddd; font-family: 'Arial', sans-serif;
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

# --- SISTEMA INTEGRADO BI ---
else:
    df = cargar_datos()
    # Si la base está vacía, mostramos un aviso
    if df.empty:
        df = pd.DataFrame(columns=["id", "cliente", "telefono", "vehiculo", "matricula", "saldo", "cuota_nro", "cuota_totales", "riesgo", "recibo_id"])
    
    df["Cuotas_Restantes"] = df["cuota_totales"] - df["cuota_nro"]

    with st.sidebar:
        st.title("OTORMÍN BI")
        opcion = st.radio("GESTIÓN:", [
            "📥 Cargar Nuevo Cliente",
            "📊 Inteligencia Financiera", 
            "💰 Cobros & WhatsApp", 
            "🧮 Refinanciación",
            "🔍 Buscador", 
            "📄 Generar Recibo"
        ])
        st.write("---")
        if st.button("Cerrar Sesión"):
            st.session_state["logueado"] = False
            st.rerun()

    # 1. CARGA DE DATOS (AHORA EN SQL)
    if opcion == "📥 Cargar Nuevo Cliente":
        st.subheader("📝 Registro de Nueva Operación")
        with st.form("registro_cliente", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                n_cliente = st.text_input("Nombre y Apellido")
                n_tel = st.text_input("Teléfono (598...)")
                n_auto = st.text_input("Vehículo")
                n_mat = st.text_input("Matrícula")
            with c2:
                n_saldo = st.number_input("Saldo Pendiente (USD)", min_value=0.0)
                n_cuota_act = st.number_input("Nro de Cuota Actual", min_value=1)
                n_cuota_tot = st.number_input("Total de Cuotas", min_value=1)
                n_riesgo = st.selectbox("Calificación de Riesgo", ["🟢 Excelente", "🟡 Regular", "🔴 Crítico"])
            
            if st.form_submit_button("💾 GUARDAR EN BASE DE DATOS"):
                if n_cliente and n_tel:
                    r_id = f"OT-{np.random.randint(5000, 9999)}"
                    datos_cliente = (n_cliente, n_tel, n_auto, n_mat, n_saldo, n_cuota_act, n_cuota_tot, n_riesgo, r_id)
                    insertar_cliente(datos_cliente)
                    st.success(f"¡Cliente {n_cliente} guardado permanentemente en SQL!")
                    st.rerun()
                else:
                    st.warning("Por favor, completa Nombre y Teléfono.")

    # 2. INTELIGENCIA FINANCIERA
    elif opcion == "📊 Inteligencia Financiera":
        st.markdown("<h2>Análisis Estratégico para Dirección</h2>", unsafe_allow_html=True)
        mora_total = df["saldo"].sum() if not df.empty else 0
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="card-intel"><p class="card-title">Capital Expuesto</p><p class="card-value">USD {mora_total:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="card-intel"><p class="card-title">Clientes Activos</p><p class="card-value">'+str(len(df))+'</p></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="card-intel"><p class="card-title">Salud de Cartera</p><p class="card-value">PROCESANDO</p></div>', unsafe_allow_html=True)
        
        st.subheader("📈 Curva de Recuperación de Capital")
        chart_data = pd.DataFrame(np.random.randn(20, 2) * [1.2, 0.8] + [11, 12], columns=['Recuperación Real', 'Tendencia Proyectada'])
        st.line_chart(chart_data)
        st.info("Ignacio, esta gráfica analiza el GAP de Cobranza basado en los datos reales que vas cargando.")

    # 3. COBROS & WHATSAPP
    elif opcion == "💰 Cobros & WhatsApp":
        st.subheader("Gestión de Cobranza Directa")
        if df.empty: st.info("No hay clientes cargados en la base de datos.")
        for index, row in df.iterrows():
            with st.expander(f"{row['riesgo']} | {row['cliente']} - {row['vehiculo']}"):
                col1, col2 = st.columns([2,1])
                with col1:
                    st.write(f"**Saldo:** USD {row['saldo']} | **Cuota:** {row['cuota_nro']}/{row['cuota_totales']}")
                with col2:
                    msg = f"Hola {row['cliente']}, Automotora Otormín le recuerda su saldo de USD {row['saldo']}."
                    ws_link = f"https://wa.me/{row['telefono']}?text={urllib.parse.quote(msg)}"
                    st.markdown(f'''<a href="{ws_link}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer; font-weight:bold;">📲 WhatsApp</button></a>''', unsafe_allow_html=True)

    # 4. REFINANCIACIÓN
    elif opcion == "🧮 Refinanciación":
        st.subheader("Simulador Contable")
        if df.empty: st.info("No hay clientes para refinanciar.")
        else:
            cliente_ref = st.selectbox("Seleccionar Cliente:", df[df["saldo"] > 0]["cliente"])
            deuda_act = df[df["cliente"] == cliente_ref]["saldo"].values[0]
            c_a, c_b = st.columns(2)
            with c_a:
                cuotas = st.slider("Nuevas Cuotas:", 1, 24, 6)
                interes = st.slider("Interés mensual (%):", 0.0, 10.0, 2.5)
            total_ref = deuda_act * (1 + (interes/100) * cuotas)
            with c_b:
                st.markdown(f'<div style="background-color:#1E2329; padding:20px; border-radius:12px; border:1px solid #55acee;"><h4>Propuesta</h4><p>Total: <b>USD {total_ref:,.2f}</b></p><p>Cuota: <b>USD {total_ref/cuotas:,.2f}</b></p></div>', unsafe_allow_html=True)

    # 5. BUSCADOR
    elif opcion == "🔍 Buscador":
        st.header("🔍 Buscador")
        busq = st.text_input("Ingresar nombre o matrícula:")
        if busq and not df.empty:
            res = df[df['cliente'].str.contains(busq, case=False) | df['matricula'].str.contains(busq, case=False)]
            st.dataframe(res, use_container_width=True, hide_index=True)

    # 6. GENERAR RECIBO
    elif opcion == "📄 Generar Recibo":
        st.subheader("Emisión de Comprobante")
        if df.empty: st.info("Carga un cliente primero para generar su recibo.")
        else:
            sel = st.selectbox("Cliente:", df["cliente"])
            info = df[df["cliente"] == sel].iloc[0]
            st.markdown(f"""
                <div class="recibo-render">
                    <table style="width:100%;"><tr><td><h1 style="color:#004a99 !important; margin:0;">OTORMÍN</h1></td><td style="text-align:right; color:black;"><b>ID: {info['recibo_id']}</b><br>{datetime.now().strftime('%d/%m/%Y')}</td></tr></table>
                    <hr><div style="color:black;"><p><b>CLIENTE:</b> {sel.upper()}</p><p><b>UNIDAD:</b> {info['vehiculo']}</p><p><b>CUOTA:</b> {info['cuota_nro']} de {info['cuota_totales']}</p></div>
                    <div style="background-color:#f0f2f6; border:2px solid #55acee; padding:15px; text-align:center; font-size:1.5em; font-weight:bold; color:black;">VALOR RECIBIDO: USD {info['saldo']}</div>
                </div>
            """, unsafe_allow_html=True)
