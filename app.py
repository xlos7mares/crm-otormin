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
    # Motor de datos unificado
    data = {
        "Cliente": ["Federico Rossi", "María Gonzalez", "Juan Castro", "Ana Ledesma"],
        "Telefono": ["59899123456", "59899111222", "59899333444", "59899555666"],
        "Vehículo": ["Mercedes Benz A200", "Toyota Hilux", "VW Gol Trend", "Fiat Cronos"],
        "Matrícula": ["IAE 1234", "MAA 5678", "PAA 9012", "IAA 3456"],
        "Saldo": [450, 200, 0, 320],
        "Cuota_Nro": [5, 12, 8, 3],
        "Cuotas_Totales": [12, 36, 12, 24],
        "Recibo_ID": ["OT-1001", "OT-1002", "OT-1003", "OT-1004"],
        "Riesgo": ["🔴 Crítico", "🟡 Regular", "🟢 Excelente", "🔴 Crítico"]
    }
    df = pd.DataFrame(data)
    df["Cuotas_Restantes"] = df["Cuotas_Totales"] - df["Cuota_Nro"]

    with st.sidebar:
        st.title("OTORMÍN BI")
        opcion = st.radio("GESTIÓN:", [
            "📊 Inteligencia Financiera", 
            "💰 Cobros & WhatsApp", 
            "🧮 Simulador de Refinanciación",
            "🔍 Buscador", 
            "📄 Generar Recibo"
        ])
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
        
        chart_data = pd.DataFrame(
            np.random.randn(20, 2) * [1.5, 1] + [10, 12],
            columns=['Recuperación Real', 'Tendencia Proyectada']
        )
        st.line_chart(chart_data)
        st.info("💡 Análisis: La curva muestra una aceleración en los pagos de la segunda quincena. Se recomienda intensificar notificaciones entre los días 10 y 15.")

    # 2. COBROS & WHATSAPP (Con Semáforo de Riesgo)
    elif opcion == "💰 Cobros & WhatsApp":
        st.subheader("Gestión Directa de Cobranza y Riesgo")
        
        for index, row in df.iterrows():
            with st.expander(f"{row['Riesgo']} | {row['Cliente']} - {row['Vehículo']}"):
                col1, col2 = st.columns([2,1])
                with col1:
                    st.write(f"**Saldo Pendiente:** USD {row['Saldo']}")
                    st.write(f"**Matrícula:** {row['Matrícula']}")
                    st.write(f"**Estado de Cuotas:** {row['Cuota_Nro']} de {row['Cuotas_Totales']} (Faltan {row['Cuotas_Restantes']})")
                with col2:
                    # Mensaje dinámico de WhatsApp
                    msg = f"Hola {row['Cliente']}, Automotora Otormín le informa que tiene un saldo pendiente de USD {row['Saldo']} por su {row['Vehículo']}. Quedamos a las órdenes para regularizar."
                    ws_link = f"https://wa.me/{row['Telefono']}?text={urllib.parse.quote(msg)}"
                    st.markdown(f'''<a href="{ws_link}" target="_blank" style="text-decoration:none;">
                        <button style="background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; width:100%; cursor:pointer; font-weight:bold;">
                            📲 Notificar WhatsApp
                        </button></a>''', unsafe_allow_html=True)

    # 3. SIMULADOR DE REFINANCIACIÓN
    elif opcion == "🧮 Simulador de Refinanciación":
        st.subheader("Simulador de Refinanciación de Deuda")
        cliente_ref = st.selectbox("Seleccionar Cliente para Refinanciar:", df[df["Saldo"] > 0]["Cliente"])
        deuda_act = df[df["Cliente"] == cliente_ref]["Saldo"].values[0]
        
        st.warning(f"Deuda actual de {cliente_ref}: **USD {deuda_act}**")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            nuevas_cuotas = st.slider("Nuevas Cuotas:", 1, 12, 3)
            tasa_interes = st.slider("Tasa de interés mensual compensatoria (%):", 0.0, 10.0, 1.5)
        
        # Matemática financiera básica
        interes_total = deuda_act * (tasa_interes / 100) * nuevas_cuotas
        total_refinanciado = deuda_act + interes_total
        valor_cuota = total_refinanciado / nuevas_cuotas
        
        with col_s2:
            st.markdown(f"""
                <div style="background-color:#1E2329; padding:25px; border-radius:12px; border:1px solid #55acee;">
                    <h4 style="margin-top:0; color:#55acee;">Propuesta de Refinanciación</h4>
                    <p>Total con Interés: <b>USD {total_refinanciado:,.2f}</b></p>
                    <p>Valor por Cuota: <b>USD {valor_cuota:,.2f}</b></p>
                    <p>Costo del Refinanciamiento: <span style="color:#ff4b4b;">USD {interes_total:,.2f}</span></p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("✅ Aplicar y Generar Registro"):
                st.success(f"Propuesta para {cliente_ref} lista para enviar.")

    # 4. BUSCADOR
    elif opcion == "🔍 Buscador":
        st.header("🔍 Buscador de Cartera")
        busq = st.text_input("Ingresar nombre o matrícula:")
        if busq:
            res = df[df['Cliente'].str.contains(busq, case=False) | df['Matrícula'].str.contains(busq, case=False)]
            st.dataframe(res, use_container_width=True, hide_index=True)

    # 5. GENERAR RECIBO (DISEÑO PROFESIONAL)
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
        
        st.write("")
        st.success("✅ Recibo listo para impresión (CTRL + P).")
