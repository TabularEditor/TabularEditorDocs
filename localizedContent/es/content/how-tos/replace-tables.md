---
uid: replace-tables
title: Reemplazar tablas
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

## Reemplazar tablas

Puedes reemplazar una tabla simplemente copiando (CTRL+C) una tabla —incluso desde otra instancia de Tabular Editor— y, a continuación, seleccionando la tabla que quieras reemplazar antes de pegar (CTRL+V). Aparecerá un mensaje para que confirmes si realmente quieres reemplazar la tabla ("Sí"), insertarla como una tabla nueva ("No") o cancelar la operación por completo:

![image](https://user-images.githubusercontent.com/8976200/36545892-40983114-17ea-11e8-8825-e8de6fd4e284.png)

Si eliges "Sí", la tabla seleccionada se reemplazará por la tabla del portapapeles. Además, todas las relaciones que apunten a esa tabla o partan de ella se actualizarán para usar la nueva tabla. Para que esto funcione, las columnas que participen en relaciones deben tener el mismo nombre y tipo de datos tanto en la tabla original como en la tabla insertada.