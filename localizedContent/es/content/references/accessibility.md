---
uid: accessibility
title: Accesibilidad
author: Morten Lønskov
updated: 2026-09-21
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Accesibilidad

Esta página recopila la configuración de Tabular Editor 3 que influye en la legibilidad y la facilidad de uso de la aplicación, e indica para qué sirve cada opción. La mayoría se encuentra en **Herramientas > Preferencias > Interfaz de usuario**.

## Modo para daltónicos

Tabular Editor usa colores para mostrarte qué ha cambiado. [Cambios no guardados](xref:unsaved-changes) marcan en verde los objetos agregados, en rojo los eliminados y en naranja los editados, y la vista de comparación de modelos usa esos mismos tres colores.

Activa **Modo para daltónicos** en **Herramientas > Preferencias > Interfaz de usuario**, en el grupo **Accesibilidad**. Entonces, los objetos agregados se marcan en verde azulado en lugar de verde, lo que los sitúa en un canal que sí se puede distinguir, y deja los eliminados y los editados como están, ya que esos dos ya estaban suficientemente separados. La configuración se aplica al Explorador TOM y a la vista de comparación de modelos, y cambia tanto el matiz de la fila como el distintivo del icono del objeto.

Esta opción está desactivada de forma predeterminada y se guarda por usuario.

## Acceso mediante teclado

Se puede acceder a todas las acciones de Tabular Editor desde los menús, y a los menús se puede acceder con el teclado. Puedes asignar tus propios atajos a los comandos que usas con frecuencia en **Herramientas > Preferencias > Teclado**, donde también se enumeran los atajos ya asignados.

Consulta @shortcuts3 para ver la lista completa de atajos predeterminados.

## Tamaño del texto y escalado de pantalla

Tabular Editor sigue el escalado de pantalla configurado en Windows, de modo que aumentar el factor de escala en **Configuración > Sistema > Pantalla** amplía toda la interfaz en lugar de solo una parte de ella.

Los editores de DAX, M, SQL y C# permiten configurar su propia fuente y tamaño en **Herramientas > Preferencias > Editor de DAX > General** y en las páginas equivalentes para los demás lenguajes. Aumentar la fuente del editor suele ser un mejor primer paso que escalar toda la aplicación, ya que es en las expresiones donde más se lee.

## Temas y contraste

Tabular Editor incluye varios temas, entre ellos algunos oscuros. Elige uno en **Herramientas > Preferencias > Interfaz de usuario** o en **Ventana > Tema**. Consulta [Cambiar temas y paletas](xref:user-interface#changing-themes-and-palettes).

Los temas cambian la apariencia de la propia aplicación. El resaltado de sintaxis dentro de los editores de código se configura por separado, en **Herramientas > Preferencias > Editor de DAX**, por lo que puedes combinar un tema oscuro con una paleta clara del editor si así te resulta más legible.

## Idioma

La interfaz está disponible en varios idiomas. Elige uno en **Herramientas > Preferencias > Interfaz de usuario**, en el grupo **Idioma**. La configuración surtirá efecto después de reiniciar la aplicación. Consulta @personalizing-te3.

## Reportar un problema de accesibilidad

Si hay algo en Tabular Editor 3 que no puedas usar, dínoslo: las opciones anteriores son las que tenemos, y la lista crece en función de lo que la gente reporte. Usa **Ayuda > Soporte de la comunidad** o **Ayuda > Soporte dedicado** si tu licencia lo incluye.
