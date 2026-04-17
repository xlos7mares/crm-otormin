elif opcion == "📄 Documentos":
        st.subheader("📄 Generación de Recibos y Estados de Cuenta")
        cliente_sel = st.selectbox("Seleccione un cliente:", df["Cliente"])
        
        # Obtenemos los datos del cliente seleccionado
        datos_cliente = df[df["Cliente"] == cliente_sel].iloc[0]
        
        # Creamos el contenido del recibo
        contenido_recibo = f"""
        ========================================
        AUTOMOTORA OTORMÍN - RECIBO DE PAGO
        ========================================
        Fecha: {datetime.now().strftime('%d/%m/%Y')}
        Cliente: {cliente_sel}
        Vehículo: {datos_cliente['Vehículo']}
        Concepto: Pago de Cuota
        Total: USD {datos_cliente['Saldo (USD)']}
        ========================================
        Gracias por su confianza.
        """
        
        st.text_area("Previsualización del Recibo:", contenido_recibo, height=200)
        
        # BOTÓN DE DESCARGA REAL
        st.download_button(
            label="💾 Descargar Recibo (TXT)",
            data=contenido_recibo,
            file_name=f"Recibo_Otormin_{cliente_sel.replace(' ', '_')}.txt",
            mime="text/plain"
        )
        
        st.success(f"Recibo para {cliente_sel} preparado para descargar.")
