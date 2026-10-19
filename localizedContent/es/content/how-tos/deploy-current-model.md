---
uid: deploy-current-model
title: Implementar el modelo cargado
author: Morten Lønskov
updated: 2026-10-11
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Implementar el modelo cargado

La implementación transfiere el modelo que tiene abierto a un servidor, ya sea creando una nueva base de datos o sobrescribiendo una existente. Es la forma de llevar un modelo almacenado en un archivo «.bim» o en una carpeta a un servidor, y de trasladar un modelo de un entorno a otro.

Abra el asistente con **Modelo > Implementar...**, elija el servidor y la base de datos de destino y, a continuación, elija qué parte del modelo desea enviar.

## Qué controla cada opción

El valor del asistente reside en lo que te permite *dejar tal cual* en el destino. Cada opción es una decisión sobre si el destino conserva su propia versión de algo:

- **Implementar estructura del modelo** envía los metadatos del modelo. Esta es la implementación en sí; si se desmarca, no queda nada por hacer.
- **Implementar orígenes de datos** envía orígenes de datos explícitos. Desmárquela para conservar las cadenas de conexión y las credenciales propias del destino, que suele ser lo que se desea al pasar del entorno de desarrollo al de pruebas.
- **Implementar particiones de tabla** sincroniza las particiones con los metadatos del modelo. Desmárquela para dejar intactas las particiones existentes y los datos que contienen. Si está habilitada, las particiones del destino que no están en el modelo se eliminan junto con sus datos.
  - **Implementar particiones regidas por directivas de actualización incremental** aparece cuando la opción anterior está habilitada y le permite implementar todas las particiones *excepto* las que genera una directiva de actualización incremental.
- **Implementar expresiones compartidas** envía las expresiones compartidas del modelo. Desmárquela para conservar las expresiones compartidas propias del destino. Esta opción está disponible en Tabular Editor 3.
- **Implementar roles de modelo** envía los roles definidos en el modelo. Desmárcala para mantener los roles del destino tal como están.
  - **Implementar miembros de roles de modelo** envía la pertenencia a los roles. Los miembros de los roles suelen gestionarse en el servidor en lugar de en los metadatos, por lo que es normal desmarcar esta opción.
- **Implementar metadatos lingüísticos (sinónimos de preguntas y respuestas, instrucciones de IA y esquema de datos de IA)** envía los metadatos lingüísticos de cada cultura. Desmárquela para conservar los sinónimos de preguntas y respuestas, las instrucciones de IA y el esquema de datos de IA configurados en el servicio Power BI.

@deployment trata todo esto en detalle, junto con el script TMSL que genera el asistente, lo que hace una implementación con los datos que ya están en el destino y cómo implementar desde la línea de comandos o un pipeline.

> [!NOTE]
> Implementar no es lo mismo que guardar. Si ha abierto el modelo desde un servidor, **Archivo > Guardar** vuelve a escribir en *esa* base de datos, como se describe en @connect-ssas. Use la implementación cuando el destino esté en otro lugar.
