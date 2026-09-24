---
uid: deploy-current-model
title: Desplegar el modelo cargado
author: Morten Lønskov
updated: 2026-09-15
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Desplegar el modelo cargado

El despliegue envía al servidor el modelo que tienes abierto, ya sea creando una base de datos nueva o sobrescribiendo una existente. Es la forma de llevar a un servidor un modelo guardado en un archivo `.bim` o en una carpeta, y de pasar un modelo de un entorno al siguiente.

Abre el asistente con **Modelo > Desplegar...**, elige el servidor y la base de datos de destino y, a continuación, elige cuánto del modelo quieres enviar.

## Qué controla cada opción

El valor del asistente radica en lo que te permite _dejar intacto_ en el destino. Cada opción es una decisión sobre si el destino conserva su propia versión de algo:

- **Desplegar la estructura del modelo** envía los metadatos del modelo. Este es el despliegue en sí; si lo desmarcas, no habrá nada que hacer.
- **Desplegar Data source** envía los Data source explícitos. Desmárcala para conservar las cadenas de conexión y credenciales propias del destino, que normalmente es lo que conviene al pasar de desarrollo a pruebas.
- **Desplegar particiones de tabla** sincroniza las particiones con los metadatos del modelo. Desmárcala para dejar intactas las particiones existentes y los datos que contienen. Si está habilitada, las particiones del destino que no estén en el modelo se eliminan junto con sus datos.
  - **Desplegar particiones regidas por políticas de actualización incremental** aparece cuando la opción anterior está habilitada y te permite desplegar todas las particiones _excepto_ las que genera una política de actualización incremental.
- **Desplegar roles del modelo** envía los roles definidos en el modelo. Desmárcala para conservar los roles del destino tal y como están.
  - **Desplegar miembros de roles del modelo** envía la pertenencia a los roles. Los miembros de los roles suelen administrarse en el servidor y no en los metadatos, por lo que es normal desmarcar esta opción.

@deployment cubre todo esto en detalle, junto con el script TMSL que genera el asistente, qué hace un despliegue con los datos que ya existen en el destino y cómo desplegar desde la línea de comandos o un pipeline.

> [!NOTE]
> Desplegar no es lo mismo que guardar. Si abriste el modelo desde un servidor, **Archivo > Guardar** guarda los cambios en _esa_ base de datos, como se describe en @connect-ssas. Usa el despliegue cuando el destino esté en otro lugar.
