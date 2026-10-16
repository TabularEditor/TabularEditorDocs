---
uid: deploy-current-model
title: Implementar el modelo cargado
author: Morten Lønskov
updated: 2026-09-15
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Implementar el modelo cargado

La implementación envía el modelo que tienes abierto a un servidor, ya sea creando una base de datos nueva o sobrescribiendo una existente. Así es como llevas a un servidor un modelo almacenado en un archivo `.bim` o en una carpeta, y cómo lo promocionas de un entorno a otro.

Abre el asistente desde **Model > Deploy...**, elige el servidor y la base de datos de destino y, después, decide qué parte del modelo quieres enviar.

## Qué controla cada opción

La utilidad del asistente está en lo que te permite _dejar intacto_ en el destino. Cada opción implica decidir si el destino conserva su propia versión de algo:

- **Implementar la estructura del modelo** envía los metadatos del modelo. Esta es la implementación en sí; si la desmarcas, no queda nada por hacer.
- **Implementar Data sources** envía los Data sources explícitos. Desmárcala para que el destino conserve sus propias cadenas de conexión y credenciales, que suele ser lo que quieres al pasar de desarrollo a pruebas.
- **Implementar particiones de tabla** sincroniza las particiones con los metadatos del modelo. Desmárcala para dejar intactas las particiones existentes y los datos que contienen. Si está activada, las particiones del destino que no estén en el modelo se eliminan junto con sus datos.
  - **Implementar particiones regidas por políticas de actualización incremental** aparece cuando la opción anterior está activada y te permite implementar todas las particiones _excepto_ las que genera una política de actualización incremental.
- **Implementar roles del modelo** envía los roles definidos en el modelo. Desmárcala para conservar los roles del destino tal como están.
  - **Implementar miembros de roles del modelo** envía la asignación de miembros a los roles. Los miembros de los roles suelen administrarse en el servidor en lugar de en los metadatos, así que es normal desmarcar esta opción.

@deployment cubre todo esto en detalle, junto con el script TMSL que genera el asistente, lo que una implementación hace con los datos que ya existen en el destino y cómo implementar desde la línea de comandos o desde un pipeline.

> [!NOTE]
> Implementar no es lo mismo que guardar. Si abriste el modelo desde un servidor, **Archivo > Guardar** guarda los cambios en _esa_ base de datos, como se describe en @connect-ssas. Usa la implementación cuando el destino esté en otro lugar.
