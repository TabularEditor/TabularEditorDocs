---
uid: scripting-referencing-objects
title: Crear scripts y hacer referencia a objetos
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

## Crear scripts y hacer referencia a objetos

Puedes usar la función de arrastrar y soltar para generar scripts de objetos de las siguientes formas:

- Arrastra uno o varios objetos a otra aplicación de Windows (editor de texto o SSMS)
  Se generará código JSON que representa el/los objeto(s) arrastrados. Al arrastrar el nodo Model, una tabla, un rol o un Data source, se crea un script "CreateOrReplace".

- Al arrastrar un objeto (una medida, una columna o una tabla) al Editor de expresiones DAX, se insertará una referencia DAX totalmente calificada al objeto en cuestión.

- Al arrastrar un objeto al editor de scripts avanzados, se insertará el código C# necesario para acceder al objeto a través del árbol TOM.