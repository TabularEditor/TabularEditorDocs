---
uid: metadata-backup
title: Copia de seguridad de metadatos
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

## Copia de seguridad de metadatos

Si lo deseas, Tabular Editor puede guardar automáticamente una copia de seguridad de los metadatos del modelo existente antes de cada guardado (cuando estés conectado a una base de datos existente) o despliegue. Esto resulta útil si no utilizas un sistema de control de versiones, pero aun así necesitas revertir a una versión anterior de tu modelo.

Para habilitar esta configuración, ve a "Archivo" > "Preferencias", activa la casilla y elige una carpeta donde guardar las copias de seguridad de metadatos:

<img src="https://user-images.githubusercontent.com/8976200/91543926-3de69100-e91f-11ea-88de-3def2b97eae0.png" width="300" />

Si la configuración está habilitada, se guardará en esta ubicación una versión comprimida (zip) de los metadatos del modelo existente cada vez que uses el Asistente de implementación o cuando hagas clic en el botón "Guardar" mientras estés conectado a una base de datos (workspace).