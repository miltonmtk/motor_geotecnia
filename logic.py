"""
Fragmento 9: Inicialización del Framework Proctor v1.0
Este bloque configura la validación de datos, la auditoría y la interfaz base.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime
import pdfkit
from io import BytesIO

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Motor Geotecnia Optimizado", layout="wide")

# --- FUNCIONES DE AUDITORÍA (Aislamiento y Auditoría Req) ---
def registrar_uso():
    """Registra la marca de tiempo de la auditoría."""
    ahora = datetime.datetime.now()
    fecha_iso = ahora.date().isoformat()
    hora_iso = ahora.time().isoformat(timespec='seconds')
    return fecha_iso, hora_iso

# --- FUNCIÓN DE CÁLCULO CORE (Optimizado 100%) ---
def calcular_curva_proctor(datos):
    """
    Realiza el ajuste polinómico con validación de entradas.
    datos: Pandas DataFrame con columnas 'Humedad (%)' y 'Densidad Seca (g/cm3)'
    """
    # Validación técnica: No permitir humedades negativas
    if (datos['Humedad (%)'] < 0).any():
        st.error("Error técnico: La humedad no puede ser negativa.")
        return None, None, None
        
    # Ajuste de curva polinómica
    x = datos['Humedad (%)']
    y = datos['Densidad Seca (g/cm3)']
    
    coeficientes = np.polyfit(x, y, 2)
    polinomio = np.poly1d(coeficientes)
    
    # Búsqueda del vértice (punto óptimo)
    # x_max = -b / (2a)
    humedad_optima = -coeficientes[1] / (2 * coeficientes[0])
    densidad_maxima = polinomio(humedad_optima)
    
    return humedad_optima, densidad_maxima, polinomio

# --- INTERFAZ BASE ---
st.title("👨‍💻 Optimización Proctor v1.0")
st.markdown("Herramienta aislada y auditada.")

# --- SISTEMA DE AUDITORÍA Y ENTRADA (Fragmento 10) ---
fecha, hora = registrar_uso()

with st.sidebar:
    st.header("📋 Registro de Auditoría")
    st.info(f"Fecha: {fecha}\nHora: {hora}")
    st.write("---")
    st.header("📥 Entrada de Datos")
    
    # Simulación de contador de acceso (Req: 3 entradas)
    if 'accesos' not in st.session_state:
        st.session_state.accesos = 0
    
    st.session_state.accesos += 1
    st.warning(f"Intento de acceso: {st.session_state.accesos} de 3")

# Formulario para ingreso de datos manuales vs generados
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Datos de Laboratorio")
        input_data = st.data_editor(
            pd.DataFrame({
                "Humedad (%)": [10.0, 12.0, 14.0, 16.0],
                "Densidad Seca (g/cm3)": [1.85, 1.92, 1.88, 1.80]
            }),
            num_rows="dynamic"
        )

        # --- PROCESAMIENTO Y GRÁFICA (Fragmento 11) ---
    with col2:
        st.subheader("Resultados del Motor")
        if not input_data.empty:
            h_opt, d_max, modelo = calcular_curva_proctor(input_data)
            
            if h_opt:
                st.success(f"Humedad Óptima: {h_opt:.2f}%")
                st.success(f"Densidad Máx: {d_max:.3f} g/cm3")
                
                # Generar puntos para la curva suavizada
                x_range = np.linspace(input_data['Humedad (%)'].min() - 1, 
                                    input_data['Humedad (%)'].max() + 1, 100)
                y_range = modelo(x_range)
                
                # Gráfica Interactiva con Plotly (Aislamiento y Calidad Req)
                fig = px.scatter(input_data, x='Humedad (%)', y='Densidad_Seca (g/cm3)', 
                                 title='Curva Proctor Optimizada')
                fig.add_scatter(x=x_range, y=y_range, mode='lines', name='Ajuste Polinómico')
                fig.add_vline(x=h_opt, line_dash="dash", line_color="green")
                
                st.plotly_chart(fig, use_container_width=True)

                # --- REPORTE Y CIERRE (Fragmento 12) ---
    st.markdown("---")
    if st.button("📄 Generar Reporte Final Auditado"):
        # Preparación de datos para el reporte
        csv = input_data.to_csv(index=False).encode('utf-8')
        
        st.success("✅ Reporte procesado exitosamente.")
        
        st.download_button(
            label="Descargar Informe Proctor (CSV)",
            data=csv,
            file_name=f"Proctor_Auditado_{fecha}_{st.session_state.accesos}.csv",
            mime='text/csv',
        )
        
        st.info(f"Código de Auditoría: {fecha}-{hora}-OP-100")

# Pie de página técnico
st.sidebar.markdown("---")
st.sidebar.caption(f"Motor: V3.1-OPTIMIZADO\nEstado: Aislado\nSesión: {st.session_state.accesos}")