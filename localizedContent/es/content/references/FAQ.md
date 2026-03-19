---
uid: faq
title: Preguntas frecuentes
---

# Preguntas frecuentes

## ¿Qué es Tabular Editor?

En esencia, Tabular Editor ofrece una interfaz de usuario para editar los metadatos que componen un modelo tabular de Analysis Services. La principal diferencia entre usar Tabular Editor para editar un modelo y usar Visual Studio es que Tabular Editor no carga ningún _dato_, solo _metadatos_. Esto significa que no se realizan validaciones ni cálculos cuando creas y modificas medidas, carpetas de visualización, etc. Las validaciones y los cálculos solo se ejecutan cuando el usuario decide guardar los cambios en la base de datos. Esto te da una mejor experiencia de desarrollo en modelos de tamaño medio a grande, que suelen ser lentos de manejar en Visual Studio.

Además, Tabular Editor incluye muchas [funcionalidades](../getting-started/boosting-productivity-te3.md) que, por lo general, aumentarán tu productividad y facilitarán ciertas tareas.

## ¿Por qué necesitamos otra herramienta más para SSAS Tabular?

Si trabajas con Analysis Services Tabular, quizá ya conozcas SQL Server Data Tools (Visual Studio), [Editor de DAX](https://www.sqlbi.com/tools/dax-editor/), [DAX Studio](https://www.sqlbi.com/tools/dax-studio/), [BISM Normalizer](http://bism-normalizer.com/) y [BIDSHelper](https://bidshelper.codeplex.com/). Todas son herramientas excelentes, cada una con sus propios fines. Tabular Editor no pretende sustituir a ninguna de estas herramientas; más bien, debería verse como un complemento de ellas. Consulta el artículo [Por qué Tabular Editor](https://tabulareditor.com/why-tabular-editor) para ver por qué Tabular Editor tiene sentido.

## ¿Por qué Tabular Editor no está disponible como complemento para Visual Studio?

Aunque se agradecería una mejor experiencia de usuario para trabajar con modelos tabulares dentro de Visual Studio, una herramienta independiente ofrece algunas ventajas frente a un complemento: en primer lugar, **no necesitas una instalación de Visual Studio/SSDT para usar Tabular Editor**. Tabular Editor solo requiere las bibliotecas AMO, que suponen una instalación bastante pequeña en comparación con VS. En segundo lugar, TabularEditor.exe puede ejecutarse con opciones de línea de comandos para implementación, scripting, etc., algo que no sería posible en un proyecto .vsix (complemento).

También vale la pena mencionar que Tabular Editor se puede descargar como un [archivo .zip independiente](https://github.com/TabularEditor/TabularEditor/releases/latest/download/TabularEditor.Portable.zip), lo que significa que no necesitas instalar nada. En otras palabras, puedes ejecutar Tabular Editor sin tener permisos de administrador en tu equipo con Windows. Simplemente descarga el archivo zip, extráelo y ejecuta TabularEditor.exe.

## ¿Qué funcionalidades están previstas para las próximas versiones?

Puedes ver la hoja de ruta actual [aquí](roadmap.md).
