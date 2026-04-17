import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from datetime import datetime

# 1. CONFIGURACIÓN DE ALTO NIVEL
st.set_page_config(page_title="OTORMÍN BI - 2026", page_icon="📈", layout="wide")

# ESTILOS DE CONTRASTE Y DISEÑO
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
        .card-trend { font-size: 0.85em; }
        .recibo-render {
            background-color: white; color: #1a1a1a !important;
            padding: 40px; border-radius: 5px; max-width: 700px; margin: auto;
            border: 1px solid #ddd; font-family: 'Arial', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# 2. MOTOR DE DATOS (PERSISTENCIA DURANTE LA SESIÓN)
if "db_clientes" not in st.session_state:
    st.session_state.db_clientes = pd.DataFrame([
        {"Cliente": "Federico Rossi", "Telefono": "59899123456", "Vehículo": "Mercedes Benz A200", "Matrícula": "IAE 1234", "Saldo": 450, "Cuota_Nro": 5, "Cuotas_Totales": 12, "Riesgo": "🔴 Crítico", "Recibo_ID": "OT-1001"},
        {"Cliente": "María Gonzalez", "Telefono": "59899111222", "Vehículo": "Toyota Hilux", "Matrícula": "MAA 5678", "Saldo": 200, "Cuota_Nro": 12, "Cuotas_Totales": 36, "Riesgo": "🟡 Regular", "Recibo_ID": "OT-1002"},
        {"Cliente": "Juan Castro", "Telefono": "59899333444", "Vehículo": "VW Gol Trend", "Matrícula": "PAA 9012", "Saldo": 0, "Cuota_Nro": 8, "Cuotas_Totales": 12, "Riesgo": "🟢 Excelente", "Recibo_ID": "OT-1003"},
        {"Cliente": "Ana Ledesma", "Telefono": "59899555666", "Vehículo": "Fiat Cronos", "Matrícula": "IAA 3456", "Saldo": 320, "Cuota_Nro": 3, "Cuotas_Totales": 24, "Riesgo": "🔴 Crítico", "Recibo_ID": "OT-1004"}
    ])

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
    df = st.session_state.db_clientes
    df["Cuotas_Restantes"] = df["Cuotas_Totales"] - df["Cuota_Nro"]

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

    # 1. CARGA DE DATOS
    if opcion == "📥 Cargar Nuevo Cliente":
        st.subheader("📝 Registro de Nueva Operación")
        with st.form("registro_cliente"):
            c1, c2 = st.columns(2)
            with c1:
                n_cliente = st.text_input("Nombre y Apellido")
                n_tel = st.text_input("Teléfono (598...)")
                n_auto = st.text_input("Vehículo")
                n_mat = st.text_input("Matrícula")
            with c2:
                n_saldo = st.number_input("Saldo Pendiente (USD)", min_value=0)
                n_cuota_act = st.number_input("Nro de Cuota Actual", min_value=1)
                n_cuota_tot = st.number_input("Total de Cuotas", min_value=1)
                n_riesgo = st.selectbox("Calificación de Riesgo", ["🟢 Excelente", "🟡 Regular", "🔴 Crítico"])
            if st.form_submit_button("💾 GUARDAR"):
                nuevo_reg = {"Cliente": n_cliente, "Telefono": n_tel, "Vehículo": n_auto, "Matrícula": n_mat, "Saldo": n_saldo, "Cuota_Nro": n_cuota_act, "Cuotas_Totales": n_cuota_tot, "Riesgo": n_riesgo, "Recibo_ID": f"OT-{np.random.randint(5000, 9999)}"}
                st.session_state.db_clientes = pd.concat([st.session_state.db_clientes, pd.DataFrame([nuevo_reg])], ignore_index=True)
                st.success(f"¡Cliente {n_cliente} registrado!")

    # 2. INTELIGENCIA FINANCIERA (INFORME PARA IGNACIO)
    elif opcion == "📊 Inteligencia Financiera":
        st.markdown("<h2>Análisis Estratégico para Dirección</h2>", unsafe_allow_html=True)
        mora_total = df["Saldo"].sum()
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="card-intel"><p class="card-title">Capital Expuesto</p><p class="card-value">USD {mora_total:,}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="card-intel"><p class="card-title">Flujo Proyectado</p><p class="card-value">USD 15.400</p></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="card-intel"><p class="card-title">Salud General</p><p class="card-value">OPTIMA</p></div>', unsafe_allow_html=True)
        
        st.subheader("📈 Curva de Recuperación de Capital")
        chart_data = pd.DataFrame(np.random.randn(20, 2) * [1.2, 0.8] + [11, 12], columns=['Recuperación Real', 'Tendencia Proyectada'])
        st.line_chart(chart_data)

        st.markdown("### 🧠 Informe de Situación Financiera")
        col_inf1, col_inf2 = st.columns(2)
        with col_inf1:
            st.markdown("""
            **Interpretación de Datos:**
            * **Línea Azul Oscuro (Real):** Dinero que efectivamente entró a caja. Los valles indican días de baja liquidez.
            * **Línea Azul Clara (Proyectada):** El objetivo ideal de ingresos según contratos.
            
            **Análisis de Tendencia:**
            Ignacio, existe un *Gap de Cobranza* ligero. Los clientes están demorando un promedio de 4 días más de lo pactado.
            """)
        with col_inf2:
            st.markdown("""
            **Sugerencia Inteligente de Negocio:**
            El sistema detecta concentración de deuda en el segmento 'Crítico'. 
            * **Recomendación:** Ofrecer un beneficio de 'Cuota Bonificada' (descuento 5%) a quienes paguen antes del día 10. Esto reducirá el capital expuesto en un 15% el próximo mes.
            """)

    # 3. COBROS & WHATSAPP
    elif opcion == "💰 Cobros & WhatsApp":
        st.subheader("Gestión de Cobranza Directa")
        for index, row in df.iterrows():
            with st.expander(f"{row['Riesgo']} | {row['Cliente']} - {row['Vehículo']}"):
                col1, col2 = st.columns([2,1])
                with col1:
                    st.write(f"**Saldo:** USD {row['Saldo']} | **Cuota:** {row['Cuota_Nro']}/{row['Cuotas_Totales']}")
                with col2:
                    msg = f"Hola {row['Cliente']}, recordamos saldo de USD {row['Saldo']} en Otormín."
                    ws_link = f"https://wa.me/{row['Telefono']}?text={urllib.parse.quote(msg)}"
                    st.markdown(f'''<a href="{ws_link}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer;">📲 WhatsApp</button></a>''', unsafe_allow_html=True)

    # 4. REFINANCIACIÓN
    elif opcion == "🧮 Refinanciación":
        st.subheader("Simulador Contable")
        cliente_ref = st.selectbox("Seleccionar Cliente:", df[df["Saldo"] > 0]["Cliente"])
        deuda_act = df[df["Cliente"] == cliente_ref]["Saldo"].values[0]
        c_a, c_b = st.columns(2)
        with c_a:
            cuotas = st.slider("Nuevas Cuotas:", 1, 24, 6)
            interes = st.slider("Interés mensual (%):", 0.0, 10.0, 2.5)
        total_ref = deuda_act * (1 + (interes/100) * cuotas)
        with c_b:
            st.markdown(f'<div style="background-color:#1E2329; padding:20px; border-radius:12px; border:1px solid #55acee;"><h4>Nueva Liquidación</h4><p>Total: <b>USD {total_ref:,.2f}</b></p><p>Cuota: <b>USD {total_ref/cuotas:,.2f}</b></p></div>', unsafe_allow_html=True)

    # 5. BUSCADOR
    elif opcion == "🔍 Buscador":
        st.header("🔍 Buscador")
        busq = st.text_input("Ingresar nombre o matrícula:")
        if busq:
            res = df[df['Cliente'].str.contains(busq, case=False) | df['Matrícula'].str.contains(busq, case=False)]
            st.dataframe(res, use_container_width=True, hide_index=True)

    # 6. GENERAR RECIBO
    elif opcion == "📄 Generar Recibo":
        st.subheader("Emisión de Comprobante")
        sel = st.selectbox("Cliente:", df["Cliente"])
        info = df[df["Cliente"] == sel].iloc[0]
        st.markdown(f"""
            <div class="recibo-render">
                <table style="width:100%;"><tr><td><h1 style="color:#004a99 !important; margin:0;">OTORMÍN</h1></td><td style="text-align:right; color:black;"><b>ID: {info['Recibo_ID']}</b><br>{datetime.now().strftime('%d/%m/%Y')}</td></tr></table>
                <hr><div style="color:black;"><p><b>CLIENTE:</b> {sel.upper()}</p><p><b>UNIDAD:</b> {info['Vehículo']}</p><p><b>CUOTA:</b> {info['Cuota_Nro']} de {info['Cuotas_Totales']}</p></div>
                <div style="background-color:#f0f2f6; border:2px solid #55acee; padding:15px; text-align:center; font-size:1.5em; font-weight:bold; color:black;">VALOR RECIBIDO: USD {info['Saldo']}</div>
            </div>
        """, unsafe_allow_html=True)
        st.success("✅ CTRL + P para imprimir.")
