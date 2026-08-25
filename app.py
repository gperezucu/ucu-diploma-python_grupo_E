import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# ============================================================
# 1. CARGA DE DATOS
# ============================================================

# Se carga el archivo procesado generado durante la primera fase del proyecto.
df = pd.read_csv(
    "data/processed/FNR_solicitudes_limpias_2024_2025.csv"
)


# ============================================================
# 2. ENCABEZADO DE LA APLICACIÓN
# ============================================================

st.title("Análisis de solicitudes del Fondo Nacional de Recursos")

st.markdown(
    """
    Aplicación interactiva para explorar las solicitudes del **Fondo Nacional
    de Recursos (FNR)** correspondientes a los años **2024 y 2025**.

    Los filtros disponibles permiten analizar dinámicamente la distribución
    de las solicitudes según **edad, sexo y estado de la solicitud**.
    """
)


# ============================================================
# 3. SIDEBAR - FILTROS
# ============================================================

st.sidebar.markdown("## Filtros")

st.sidebar.markdown(
    """
    Utilice los controles para seleccionar el subconjunto de datos
    que desea analizar.
    """
)


# ------------------------------------------------------------
# Filtro 1: rango de edad
# ------------------------------------------------------------

edad_min = int(df["edad_años"].min())
edad_max = int(df["edad_años"].max())

rango_edad = st.sidebar.slider(
    "Rango de edad",
    min_value=edad_min,
    max_value=edad_max,
    value=(edad_min, edad_max)
)


# ------------------------------------------------------------
# Filtro 2: sexo
# ------------------------------------------------------------

opciones_sexo = sorted(
    df["sexo"].dropna().unique().tolist()
)

sexo_seleccionado = st.sidebar.radio(
    "Sexo",
    options=["Todos"] + opciones_sexo
)


# ------------------------------------------------------------
# Filtro 3: estado de la solicitud
# ------------------------------------------------------------

opciones_estado = sorted(
    df["estado_solicitud"].dropna().unique().tolist()
)

estado_seleccionado = st.sidebar.selectbox(
    "Estado de la solicitud",
    options=["Todos"] + opciones_estado
)


# ============================================================
# 4. APLICACIÓN DE LOS FILTROS
# ============================================================

# Primero se aplica el filtro obligatorio de rango de edad.
df_filtrado = df[
    df["edad_años"].between(
        rango_edad[0],
        rango_edad[1]
    )
].copy()


# Si se selecciona un sexo específico, se aplica el filtro.
if sexo_seleccionado != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["sexo"] == sexo_seleccionado
    ]


# Si se selecciona un estado específico, se aplica el filtro.
if estado_seleccionado != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["estado_solicitud"] == estado_seleccionado
    ]


# ============================================================
# 5. REGISTROS FILTRADOS
# ============================================================

st.subheader("Registros filtrados")

st.markdown(
    """
    La siguiente tabla muestra una muestra de los registros que cumplen
    con los filtros seleccionados.
    """
)

st.write(
    "Cantidad de registros filtrados:",
    len(df_filtrado)
)


# Si los filtros no devuelven resultados, se informa al usuario.
if df_filtrado.empty:

    st.warning(
        "No existen registros que cumplan con la combinación de filtros seleccionada."
    )

else:

    st.dataframe(
        df_filtrado.head(20),
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # 6. RESUMEN DESCRIPTIVO
    # ========================================================

    st.subheader("Resumen descriptivo de la edad")

    st.markdown(
        """
        Las estadísticas descriptivas se calculan utilizando exclusivamente
        los registros resultantes de los filtros seleccionados.
        """
    )


    media = df_filtrado["edad_años"].mean()

    mediana = df_filtrado["edad_años"].median()

    desvio = df_filtrado["edad_años"].std()

    minimo = df_filtrado["edad_años"].min()

    maximo = df_filtrado["edad_años"].max()

    rango = maximo - minimo

    q1 = df_filtrado["edad_años"].quantile(0.25)

    q2 = df_filtrado["edad_años"].quantile(0.50)

    q3 = df_filtrado["edad_años"].quantile(0.75)


    resumen = pd.DataFrame({

        "Media": [round(media, 2)],

        "Mediana": [round(mediana, 2)],

        "Desv. estándar": [round(desvio, 2)],

        "Mínimo": [round(minimo, 2)],

        "Q1": [round(q1, 2)],

        "Q2": [round(q2, 2)],

        "Q3": [round(q3, 2)],

        "Máximo": [round(maximo, 2)],

        "Rango": [round(rango, 2)]

    })


    st.dataframe(
        resumen,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # 7. HISTOGRAMA
    # ========================================================

    st.subheader("Distribución de la edad")

    st.markdown(
        """
        El histograma representa la distribución de edades de los pacientes
        después de aplicar los filtros seleccionados.
        """
    )


    fig, ax = plt.subplots(
        figsize=(10, 4)
    )


    ax.hist(
        df_filtrado["edad_años"],
        bins=20,
        edgecolor="white",
        color="#000066"
    )


    ax.set_title(
        "Distribución de la edad de los pacientes"
    )

    ax.set_xlabel(
        "Edad (años)"
    )

    ax.set_ylabel(
        "Cantidad de solicitudes"
    )


    st.pyplot(fig)


    # ========================================================
    # 8. GRÁFICO DE DISPERSIÓN
    # ========================================================

    # Se calcula la cantidad de solicitudes registrada para cada edad.
    solicitudes_por_edad = (
        df_filtrado
        .groupby("edad_años")
        .size()
        .reset_index(
            name="cantidad_solicitudes"
        )
    )


    st.subheader(
        "Relación entre edad y cantidad de solicitudes"
    )

    st.markdown(
        """
        Cada punto representa una edad y la cantidad de solicitudes
        correspondientes a pacientes de esa edad dentro del conjunto filtrado.
        """
    )


    fig2, ax2 = plt.subplots(
        figsize=(10, 4)
    )


    ax2.scatter(
        solicitudes_por_edad["edad_años"],
        solicitudes_por_edad["cantidad_solicitudes"],
        alpha=0.7,
        color="#000066"
    )


    ax2.set_title(
        "Cantidad de solicitudes según edad"
    )

    ax2.set_xlabel(
        "Edad (años)"
    )

    ax2.set_ylabel(
        "Cantidad de solicitudes"
    )


    st.pyplot(fig2)