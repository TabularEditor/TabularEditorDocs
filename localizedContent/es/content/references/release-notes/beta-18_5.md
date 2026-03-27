# Tabular Editor 3 BETA-18.5

> [!IMPORTANT]
> Hay una versión más reciente de Tabular Editor disponible. Puedes encontrar la versión más reciente [aquí](https://docs.tabulareditor.com/references/release-notes).

- Descarga [Tabular Editor 3 BETA-18.5](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.5.x86.msi)
- Descarga [Tabular Editor 3 BETA-18.5 (64 bits)](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.5.x64.msi)
- [Todas las versiones](https://docs.tabulareditor.com/projects/te3/en/latest/downloads.html)

## Nuevas características en BETA-18.5:

- El cuadro de diálogo Buscar (CTRL+F) ahora permite buscar en todo el modelo. Cuando seleccionas esta opción en la lista desplegable, aparece otra lista desplegable que te permite elegir qué propiedades de los objetos quieres buscar. También hay opciones para expresiones regulares, expresiones con barra invertida y también [búsqueda con LINQ dinámico, similar a Tabular Editor 2.x](https://docs.tabulareditor.com/Advanced-Filtering-of-the-Explorer-Tree.html) (también puedes habilitar LINQ dinámico escribiendo `:` como primer carácter en el campo "Buscar qué"). Los resultados de la búsqueda se muestran en una ventana independiente y, al hacer doble clic en un elemento de esa ventana, irás directamente a él, resaltando la propiedad correspondiente en la cuadrícula de propiedades:

![image](https://user-images.githubusercontent.com/30911111/119983803-edd94f80-bfc0-11eb-91cb-aee084e0c83d.png)

- Se agregó compatibilidad con la sintaxis literal de fecha de DAX `dt"2021-05-27"`
- Se actualizó TOM a la versión 19.21.0

## Correcciones de errores y actualizaciones menores en BETA-18.5:

- Se agregó un editor de cadenas multilínea para la propiedad SourceExpressions de las tablas
- Se garantiza que los nombres de las relaciones no se regeneren al cortar y pegar
- Se agregó compatibilidad con BPA para la palabra clave `it` en FixExpressions; consulta https://github.com/TabularEditor/TabularEditor/issues/846
- Se mejoró el comportamiento de la ventana Buscar/Reemplazar al cambiar entre documentos o elementos de la interfaz de usuario
- Se corrigió un error con el orden de precedencia de la palabra clave NOT; consulta https://github.com/TabularEditor/TabularEditor3/issues/5.
