---
uid: messages-view
title: Vista de mensajes
author: Daniel Otykier
updated: 2021-09-08
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Escritorio
          full: true
        - edition: Empresarial
          full: true
        - edition: Empresarial
          full: true
---

# Vista de mensajes

La vista de mensajes en Tabular Editor 3 es una ventana de herramientas que muestra varios tipos de mensajes relacionados con el Dataset actual.

> [!TIP]
> Puede hacer doble clic en un mensaje para ir al origen del error en el árbol del modelo o en el editor de scripts.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/messages-view.png" alt="Message View" style="width: 500px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Ventana de mensajes en Tabular Editor. Ofrece una visión general de todas las advertencias y errores de su Dataset </figcaption>
</figure>

La vista de mensajes le indicará el origen y el objeto que genera el mensaje.

Se muestran dos tipos de mensajes, errores y advertencias

- Errores: Esta pestaña muestra cualquier error que impida que su modelo se implemente o se guarde. Por ejemplo, si tiene una expresión no válida en un elemento de cálculo o una dependencia circular en una relación.
- Advertencias: Esta pestaña muestra cualquier advertencia que no concuerda con los estándares, pero que no impide que su modelo pueda utilizarse. Por ejemplo, tener referencias a medidas con nombres totalmente cualificados.
-

## Copiar mensajes

La vista de mensajes permite copiar el mensaje de error con Ctrl+C.

A partir de Tabular Editor 3.23.0, Ctrl+C copia la celda seleccionada de forma predeterminada. Use Ctrl+Shift+C (o Copiar fila en el menú contextual) para copiar a nivel de fila.

> [!TIP]
> Haga clic con el botón derecho en una celda para elegir Copiar celda / Copiar fila.

![Copia de vista de mensajes](~/content/assets/images/messages-view-copy.png)

