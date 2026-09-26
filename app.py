import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Laboratorio Máquinas I - UPTC",
    page_icon="⚡",
    layout="wide",
)

st.title(
    "⚡ Práctica VI: Motor de Corriente Continua con Excitación Independiente"
)
st.markdown(
    "**Escuela de Ingeniería Electrónica - UPTC Sogamoso** | Herramienta de Tabulación y Procesamiento de Datos"
)
st.markdown("---")

# Pestañas para las pruebas
tab_arranque, tab_carga = st.tabs(
    ["A. Prueba de Arranque (RPM vs Ia)", "C. Prueba con Carga"]
)

# ---------------------------------------------------------
# SECCIÓN A: ARRANQUE
# ---------------------------------------------------------
with tab_arranque:
    st.header("A. Procedimiento de Arranque (Sin Carga)")
    st.write(
        "Ingrese las mediciones tomadas durante la exclusión gradual del reóstato de arranque."
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Tabla de Datos (Arranque)")
        data_arranque = pd.DataFrame(
            {
                "Ia (A)": [2.5, 2.0, 1.5, 1.0, 0.8],
                "RPM": [500, 1000, 1600, 2100, 2500],
            }
        )

        df_arranque = st.data_editor(
            data_arranque, num_rows="dynamic", key="editor_arranque"
        )

    with col2:
        st.subheader("Gráfica: Velocidad vs Corriente de Armadura")
        if not df_arranque.empty and len(df_arranque) > 1:
            fig_arranque = px.line(
                df_arranque,
                x="Ia (A)",
                y="RPM",
                markers=True,
                title="RPM vs. Corriente de Armadura (Ia)",
                labels={"Ia (A)": "Corriente de Armadura Ia (A)", "RPM": "RPM"},
            )
            fig_arranque.update_traces(
                line_color="#D32F2F", line_width=3, marker_size=8
            )
            st.plotly_chart(fig_arranque, use_container_width=True)
        else:
            st.info("Ingrese al menos dos filas de datos para generar la gráfica.")

# ---------------------------------------------------------
# SECCIÓN C: PRUEBA CON CARGA
# ---------------------------------------------------------
with tab_carga:
    st.header("C. Prueba con Carga (Variación en Freno Electromagnético)")
    st.write(
        "Ingrese las mediciones para cada nivel de carga aplicado con el freno."
    )

    col_input, col_calc = st.columns([1, 1])

    with col_input:
        st.subheader("1. Mediciones Experimentales")
        data_carga = pd.DataFrame(
            {
                "Ia (A)": [0.8, 1.2, 1.7, 2.3, 3.0],
                "Vt (V)": [32.0, 31.8, 31.5, 31.2, 30.8],
                "D - Distancia (m)": [0.2, 0.2, 0.2, 0.2, 0.2],
                "F - Fuerza/Peso (N)": [0.3, 0.8, 1.5, 2.3, 3.2],
                "RPM": [2480, 2410, 2320, 2200, 2050],
            }
        )

        df_carga = st.data_editor(
            data_carga, num_rows="dynamic", key="editor_carga"
        )

    # Procesamiento matemático de las ecuaciones del laboratorio
    if not df_carga.empty:
        # P_in = Vt * Ia
        df_carga["Pin (W)"] = df_carga["Vt (V)"] * df_carga["Ia (A)"]

        # Torque = F * D
        df_carga["Torque tau (N.m)"] = (
            df_carga["F - Fuerza/Peso (N)"] * df_carga["D - Distancia (m)"]
        )

        # omega = 2 * pi * RPM / 60
        omega = df_carga["RPM"] * (2 * np.pi / 60)

        # P_out = Torque * omega
        df_carga["Pout (W)"] = df_carga["Torque tau (N.m)"] * omega

        # Eficiencia (%) = (Pout / Pin) * 100
        df_carga["Eficiencia n (%)"] = np.where(
            df_carga["Pin (W)"] > 0,
            (df_carga["Pout (W)"] / df_carga["Pin (W)"]) * 100,
            0,
        )

    with col_calc:
        st.subheader("2. Parámetros Calculados Automáticamente")
        st.dataframe(
            df_carga[
                [
                    "Ia (A)",
                    "Pin (W)",
                    "Torque tau (N.m)",
                    "Pout (W)",
                    "Eficiencia n (%)",
                ]
            ].style.format("{:.2f}"),
            use_container_width=True,
        )

    st.markdown("---")
    st.subheader("3. Curvas de Características de la Máquina")

    if not df_carga.empty and len(df_carga) > 1:
        opcion_grafica = st.selectbox(
            "Seleccione la relación que desea graficar:",
            [
                "Pout, RPM, Torque y Eficiencia vs Ia",
                "Característica Mecánica: RPM vs Torque (tau)",
            ],
        )

        if opcion_grafica == "Pout, RPM, Torque y Eficiencia vs Ia":
            # Gráfica múltiple respecto a Ia
            fig_multi = go.Figure()

            # Pout vs Ia
            fig_multi.add_trace(
                go.Scatter(
                    x=df_carga["Ia (A)"],
                    y=df_carga["Pout (W)"],
                    mode="lines+markers",
                    name="Pout (W)",
                )
            )

            # RPM vs Ia
            fig_multi.add_trace(
                go.Scatter(
                    x=df_carga["Ia (A)"],
                    y=df_carga["RPM"],
                    mode="lines+markers",
                    name="RPM",
                    yaxis="y2",
                )
            )

            # Torque vs Ia
            fig_multi.add_trace(
                go.Scatter(
                    x=df_carga["Ia (A)"],
                    y=df_carga["Torque tau (N.m)"],
                    mode="lines+markers",
                    name="Torque (N.m)",
                    yaxis="y3",
                )
            )

            # Eficiencia vs Ia
            fig_multi.add_trace(
                go.Scatter(
                    x=df_carga["Ia (A)"],
                    y=df_carga["Eficiencia n (%)"],
                    mode="lines+markers",
                    name="Eficiencia (%)",
                    yaxis="y4",
                )
            )

            fig_multi.update_layout(
                title="Variables de Salida vs. Corriente de Armadura (Ia)",
                xaxis=dict(title="Corriente de Armadura Ia (A)"),
                yaxis=dict(title="Pout (W)", titlefont=dict(color="#1f77b4")),
                yaxis2=dict(
                    title="RPM",
                    titlefont=dict(color="#ff7f0e"),
                    overlaying="y",
                    side="right",
                ),
                yaxis3=dict(
                    title="Torque (N.m)",
                    titlefont=dict(color="#2ca02c"),
                    overlaying="y",
                    side="left",
                    position=0.05,
                ),
                yaxis4=dict(
                    title="Eficiencia (%)",
                    titlefont=dict(color="#d62728"),
                    overlaying="y",
                    side="right",
                    position=0.95,
                ),
                height=500,
            )

            st.plotly_chart(fig_multi, use_container_width=True)

        else:
            # RPM vs Torque
            fig_mecanica = px.line(
                df_carga,
                x="Torque tau (N.m)",
                y="RPM",
                markers=True,
                title="Característica Mecánica: RPM vs Torque (τ)",
                labels={
                    "Torque tau (N.m)": "Par de Carga Torque τ (N.m)",
                    "RPM": "Velocidad de Giro (RPM)",
                },
            )
            fig_mecanica.update_traces(
                line_color="#1E88E5", line_width=3, marker_size=8
            )
            st.plotly_chart(fig_mecanica, use_container_width=True)

# Opción de descarga
st.markdown("---")
st.subheader("4. Exportar Datos Procesados")
csv_data = df_carga.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Descargar Tabla Calculada (CSV)",
    data=csv_data,
    file_name="laboratorio_motor_cc_uptc.csv",
    mime="text/csv",
)
