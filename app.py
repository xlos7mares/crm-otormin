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

# 2. MOTOR DE DATOS (PERSISTENCIA DURANTE LA SESIÓN)
if "db_clientes" not in st.session_state:
    # Datos iniciales precargados
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
    # Referencia a la base de datos actual
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

    # 1. CARGA DE DATOS (FUNCIONALIDAD NUEVA)
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
            
            if st.form_submit_button("💾 GUARDAR EN CARTERA"):
                nuevo_reg = {
                    "Cliente": n_cliente, "Telefono": n_tel, "Vehículo": n_auto,
                    "Matrícula": n_mat, "Saldo": n_saldo, "Cuota_Nro": n_cuota_act,
                    "Cuotas_Totales": n_cuota_tot, "Riesgo": n_riesgo, 
                    "Recibo_ID": f"OT-{np.random.randint(5000, 9999)}"
                }
                st.session_state.db_clientes = pd.concat([st.session_state.db_clientes, pd.DataFrame([nuevo_reg])], ignore_index=True)
                st.success(f"¡Cliente {n_cliente} registrado exitosamente!")

    # 2. INTELIGENCIA FINANCIERA
    elif opcion == "📊 Inteligencia Financiera":
        st.markdown("<h2>Análisis de Tendencia de Cobranza</h2>", unsafe_allow_html=True)
        
        mora_total = df["Saldo"].sum()
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="card-intel"><p class="card-title">Capital en Mora</p><p class="card-value">USD {mora_total:,}</p><p class="card-trend" style="color:#ff4b4b;">↑ Actualizado</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="card-intel"><p class="card-title">Proyección Mensual</p><p class="card-value">USD 15.400</p><p class="card-trend" style="color:#00ffcc;">Probabilidad: 88%</p></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="card-intel"><p class="card-title">Eficiencia de Cartera</p><p class="card-value">94.2%</p><p class="card-trend" style="color:#00ffcc;">Clientes: {len(df)}</p></div>', unsafe_allow_html=True)

        st.write("---")
        st.subheader("📈 Curva de Recuperación de Capital")
        chart_data = pd.DataFrame(np.random.randn(20, 2) * [1.5, 1] + [10, 12], columns=['Recuperación Real', 'Tendencia Proyectada'])
        st.line_chart(chart_data)

    # 3. COBROS & WHATSAPP
    elif opcion == "💰 Cobros & WhatsApp":
        st.subheader("Gestión Directa de Cobranza y Riesgo")
        for index, row in df.iterrows():
            with st.expander(f"{row['Riesgo']} | {row['Cliente']} - {row['Vehículo']}"):
                col1, col2 = st.columns([2,1])
                with col1:
                    st.write(f"**Saldo Pendiente:** USD {row['Saldo']}")
                    st.write(f"**Matrícula:** {row['Matrícula']}")
                    st.write(f"**Estado:** Cuota {row['Cuota_Nro']} de {row['Cuotas_Totales']}")
                with col2:
                    msg = f"Hola {row['Cliente']}, Automotora Otormín le informa que tiene un saldo pendiente de USD {row['Saldo']} por su {row['Vehículo']}."
                    ws_link = f"https://wa.me/{row['Telefono']}?text={urllib.parse.quote(msg)}"
                    st.markdown(f'''<a href="{ws_link}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; width:100%; cursor:pointer; font-weight:bold;">📲 WhatsApp</button></a>''', unsafe_allow_html=True)

    # 4. REFINANCIACIÓN
    elif opcion == "🧮 Refinanciación":
        st.subheader("Simulador Contable de Refinanciación")
        cliente_ref = st.selectbox("Seleccionar Cliente:", df[df["Saldo"] > 0]["Cliente"])
        deuda_act = df[df["Cliente"] == cliente_ref]["Saldo"].values[0]
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            nuevas_cuotas = st.slider("Dividir en cuántas cuotas:", 1, 24, 6)
            tasa_interes = st.slider("Interés mensual compensatorio (%):", 0.0, 10.0, 2.5)
        
        interes_total = deuda_act * (tasa_interes / 100) * nuevas_cuotas
        total_ref = deuda_act + interes_total
        
        with col_s2:
            st.markdown(f"""
                <div style="background-color:#1E2329; padding:25px; border-radius:12px; border:1px solid #55acee;">
                    <h4 style="margin:0; color:#55acee;">Nueva Liquidación</h4>
                    <p>Total Refinanciado: <b>USD {total_ref:,.2f}</b></p>
                    <p>Valor Cuota Mensual: <b>USD {total_ref/nuevas_cuotas:,.2f}</b></p>
                    <p>Interés aplicado: <span style="color:#ff4b4b;">USD {interes_total:,.2f}</span></p>
                </div>
            """, unsafe_allow_html=True)

    # 5. BUSCADOR
    elif opcion == "🔍 Buscador":
        st.header("🔍 Buscador de Cartera")
        busq = st.text_input("Ingresar nombre o matrícula:")
        if busq:
            res = df[df['Cliente'].str.contains(busq, case=False) | df['Matrícula'].str.contains(busq, case=False)]
            st.dataframe(res, use_container_width=True, hide_index=True)

    # 6. GENERAR RECIBO
    elif opcion == "📄 Generar Recibo":
        st.subheader("Emisión de Comprobante")
        sel = st.selectbox("Seleccione el Cliente:", df["Cliente"])
        info = df[df["Cliente"] == sel].iloc[0]

        st.markdown(f"""
            <div class="recibo-render">
                <table style="width:100%; border:none;">
                    <tr>
                        <td><h1 style="color:#004a99 !important; margin:0;">OTORMÍN</h1><p style="margin:0; font-size:0.8em; color:gray;">AUTOMOTORA & GESTIÓN</p></td>
                        <td style="text-align:right;"><p style="color:black;"><b>ID: {info['Recibo_ID']}</b><br>Fecha: {datetime.now().strftime('%d/%m/%Y')}</p></td>
                    </tr>
                </table>
                <hr style="border:1px solid #eee;">
                <div style="padding:20px 0; line-height:1.6; color:black;">
                    <p><b>CLIENTE:</b> {sel.upper()}</p>
                    <p><b>AUTOMOTOR:</b> {info['Vehículo']} (Mat: {info['Matrícula']})</p>
                    <p><b>DETALLE:</b> Pago de cuota nro. <b>{info['Cuota_Nro']}</b> de un total de {info['Cuotas_Totales']}.</p>
                    <p style="background-color:#fff3cd; padding:10px; border-radius:5px;"><b>ESTADO:</b> Al cliente le restan <b>{info['Cuotas_Restantes']} cuotas</b> para finalizar su plan.</p>
                </div>
                <div style="background-color:#f0f2f6; border:2px solid #55acee; padding:15px; text-align:center; font-size:1.5em; font-weight:bold; color:black;">
                    MONTO RECIBIDO: USD {info['Saldo']}
                </div>
                <div style="margin-top:50px; border-top:1px solid #000; width:180px; text-align:center; font-size:0.8em; color:black;">
                    Firma Administración
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.success("✅ Recibo listo para impresión (CTRL + P).")
