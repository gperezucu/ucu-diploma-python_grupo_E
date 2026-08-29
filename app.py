import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Dashboard FNR",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

st.title("🏥Dashboard de solicitudes del FNR")

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

st.subheader("Resumen general")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Solicitudes",
    f"{len(df_filtrado):,}".replace(",", ".")
)

col2.metric(
    "Edad promedio",
    f"{df_filtrado['edad_años'].mean():.1f} años"
)

col3.metric(
    "Departamentos",
    df_filtrado["departamento_residencia"].nunique()
)

col4.metric(
    "Prestaciones",
    df_filtrado["prestacion_desc"].nunique()
)
# ============================================================
# 5. REGISTROS FILTRADOS
# ============================================================

st.subheader("Registros filtrados")

st.markdown(
    """
    La siguiente tabla muestra el detalle de los registros filtrados    
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
        "Distribución de edad de los pacientes"
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
        correspondientes a pacientes de esa edad.
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

    # ========================================================
    # 9. MAPA GEOGRÁFICO
    # ========================================================

    st.subheader("Distribución geográfica por departamento de las solicitudes")

    st.markdown(
        """
        El mapa muestra la distribución territorial de las solicitudes

        Las coordenadas utilizadas representan un punto de referencia de cada
        departamento y no la ubicación exacta de los pacientes.
        """
    )

# Agrupar las solicitudes por departamento
mapa_departamentos = (
    df_filtrado
    .groupby(
        ["departamento_residencia", "latitud", "longitud"]
    )
    .size()
    .reset_index(name="cantidad_solicitudes")
)

fig_mapa = px.scatter_map(
    mapa_departamentos,
    lat="latitud",
    lon="longitud",
    size="cantidad_solicitudes",
    hover_name="departamento_residencia",
    hover_data={
        "cantidad_solicitudes": True,
        "latitud": False,
        "longitud": False
    },
    size_max=50,
    zoom=5,
    center={
        "lat": -32.8,
        "lon": -56.0
    },
    height=600
)

fig_mapa.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0}
)

st.plotly_chart(
    fig_mapa,
    use_container_width=True
)

# ========================================================
# 9. TOP 10 ÁREAS DE PRESTACIÓN
# ========================================================

st.subheader("Top 10 áreas de prestación")

st.markdown(
    """
    El gráfico muestra las 10 áreas de prestación con mayor cantidad
    de solicitudes.
    """
)

top_10_areas = (
    df_filtrado["area_prestacion"]
    .value_counts()
    .head(10)
    .sort_values()
)

fig3, ax3 = plt.subplots(figsize=(10, 5))

ax3.barh(
    top_10_areas.index,
    top_10_areas.values,
    color="#000066"
)

ax3.set_title("Top 10 áreas de prestación por cantidad de solicitudes")
ax3.set_xlabel("Cantidad de solicitudes")
ax3.set_ylabel("Área de prestación")

st.pyplot(fig3)

# ========================================================
# 10. TOP 20 PRESTACIONES
# ========================================================

st.subheader("Top 20 prestaciones más solicitadas")

st.markdown(
    """
    El gráfico muestra las 20 prestaciones con mayor cantidad de solicitudes.
    """
)

top_20_prestaciones = (
    df_filtrado["prestacion_desc"]
    .value_counts()
    .head(20)
    .sort_values()
)

fig4, ax4 = plt.subplots(figsize=(10, 8))

ax4.barh(
    top_20_prestaciones.index,
    top_20_prestaciones.values,
    color="#000066"
)

ax4.set_title("Top 20 prestaciones por cantidad de solicitudes")
ax4.set_xlabel("Cantidad de solicitudes")
ax4.set_ylabel("Prestación")

plt.tight_layout()

st.pyplot(fig4)