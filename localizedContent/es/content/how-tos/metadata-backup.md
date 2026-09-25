---
uid: metadata-backup
title: Metadata Backup
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Metadata Backup

Si lo deseas, Tabular Editor puede guardar automáticamente una copia de seguridad de los metadatos del modelo existente antes de cada guardado (cuando estés conectado a una base de datos existente) o despliegue. Esto resulta útil si no utilizas un sistema de control de versiones, pero aun así necesitas revertir a una versión anterior de tu modelo.

To enable this setting, go to **Tools > Preferences** (**File > Preferences** in Tabular Editor 2), enable the checkbox and choose a folder to place the metadata backups:

<img src="../assets/images/metadata-backup-01.png" width="300" />

Si la configuración está habilitada, se guardará en esta ubicación una versión comprimida (zip) de los metadatos del modelo existente cada vez que uses el Asistente de implementación o cuando hagas clic en el botón "Guardar" mientras estés conectado a una base de datos (workspace).