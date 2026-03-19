---
uid: connect-ssas
title: Conectar e implementar en SSAS
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

## Conectar/implementar en bases de datos tabulares de SSAS

Al pulsar CTRL+SHIFT+O, puedes abrir un modelo tabular directamente desde una base de datos tabular que ya se ha implementado. Introduce la dirección del servidor y (opcionalmente) proporciona un nombre de usuario y una contraseña. Después de hacer clic en "Aceptar", se te mostrará una lista de las bases de datos del servidor. Selecciona la que quieras cargar y haz clic en "Aceptar" de nuevo.

![](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/Connect.png)

El cuadro de diálogo mostrado también te permite conectarte a instancias de Azure Analysis Services si proporcionas el nombre completo de la instancia de Azure AS, empezando por "azureas://". Puedes usar la lista desplegable "Instancia local" para buscar y conectarte a cualquier instancia en ejecución de Power BI Desktop o a áreas de trabajo Integradas de Visual Studio. **Ten en cuenta que, aunque Tabular Editor puede realizar cambios en un modelo de Power BI a través de TOM, Microsoft no lo admite y podría dañar el archivo .pbix. ¡Continúa bajo tu propia responsabilidad!**

Cada vez que pulses CTRL+S después de cargar la base de datos, esta se actualizará con los cambios que hayas hecho en Tabular Editor. Herramientas cliente (Excel, Power BI, DAX Studio, etc.) deberían poder ver inmediatamente los cambios en la base de datos a partir de ese momento. Ten en cuenta que, según los cambios realizados, puede que necesites recalcular manualmente los objetos del modelo para poder consultarlo correctamente.

Si quieres guardar el modelo en modo conectado en un archivo Model.bim, elige "Guardar como..." en el menú "Archivo".