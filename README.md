# Análisis de Solicitudes de Prestaciones de Salud

## Objetivo

Analizar las características de las solicitudes de prestaciones de salud e identificar factores asociados al estado de autorización de las mismas.

## Dataset

El conjunto de datos contiene información sobre solicitudes de prestaciones, incluyendo:

- Id enmascarado del paciente
- Estado de solicitud
- Tipo de prestación
- Área de prestación
- Código prestación
- Descripción prestación
- Edad
- Sexo
- Origen del prestador
- Prestador de Salud
- Prestador Tipo
- Prestador Origen
- Departamento de residencia
- Departamento del prestador
- Fecha Solicitud
- Fecha Autorizacion

## Análisis Exploratorio de Datos (EDA)

Se realizaron las siguientes tareas:

- Análisis descriptivo de variables
-Limpieza de datos.
- Análisis de variables univariante
- Análisis de variables multivariantes


### Principales hallazgos

- La distribución de solicitudes por paciente muestra una alta concentración en una única solicitud.
- La mayoría de las solicitudes fueron autorizadas.
- Acto Médico concentra la mayor cantidad de registros.
- Las áreas de Cardiología y Traumatología presentan el mayor volumen de solicitudes.
- Los prestadores IAMC son los más representados.
- Montevideo concentra la mayor cantidad de solicitudes.
- El grupo etario entre 31-45 años tiene un porcentaje levemente menor de aprobaciones frente a los otros grupos.
- No se observan correlaciones lineales fuertes con la variable objetivo.