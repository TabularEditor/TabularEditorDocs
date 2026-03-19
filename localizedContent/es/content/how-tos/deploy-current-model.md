---
uid: deploy-current-model
title: Implementar el modelo cargado actualmente
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

## Implementación

Si quieres implementar el modelo cargado actualmente en una nueva base de datos o sobrescribir una base de datos existente con los cambios del modelo (por ejemplo, al cargarlo desde un archivo Model.bim), usa el Asistente de implementación en "Model" > "Deploy...".

Tabular Editor incluye un Asistente de implementación que ofrece varias ventajas frente a la implementación desde SSDT, especialmente al implementar en una base de datos existente. Después de elegir un servidor y una base de datos de destino, tienes las siguientes opciones para esta implementación:

![Asistente de implementación](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/Deployment.png)

Si dejas desmarcada la casilla "Deploy Connections", te aseguras de que todos los Data sources de la base de datos de destino permanezcan intactos. Recibirás un error si tu modelo contiene una o más tablas con un Data source que no exista ya en la base de datos de destino.

Del mismo modo, si dejas desmarcada la casilla "Deploy Table Partitions", te aseguras de que las particiones existentes de tus tablas no se modifiquen y de que los datos de las particiones se mantengan intactos.

Cuando la casilla "Deploy Roles" está marcada, los roles de la base de datos de destino se actualizarán para reflejar los del modelo cargado; sin embargo, si la casilla "Deploy Role Members" está desmarcada, los miembros de cada rol permanecerán sin cambios en la base de datos de destino.