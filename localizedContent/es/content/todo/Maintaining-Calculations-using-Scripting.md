Este artículo muestra cómo puedes usar la funcionalidad Advanced Scripting en Tabular Editor para mantener la lógica DAX de forma coherente en varios objetos. En el [artículo Useful Script Snippets](/Useful-script-snippets), ya vimos [cómo podemos usar Custom Actions para generar rápidamente muchas medidas](/Useful-script-snippets#generate-time-intelligence-measures) con una lógica similar, lo cual puede ser útil, por ejemplo, al crear cálculos de inteligencia temporal.

En este artículo, vamos a ampliar esta idea creando un "framework" de scripting que nos permitirá definir de forma centralizada todos los cálculos que necesitamos en un archivo TSV (valores separados por tabulaciones). La ventaja de usar un archivo TSV es que se puede editar fácilmente en Excel y, al mismo tiempo, es sencillo de analizar y cargar desde un script en Tabular Editor.

Para este artículo, nos centraremos en la tabla de hechos Internet Sales y en las dimensiones relacionadas del clásico Adventure Works:

![image](https://user-images.githubusercontent.com/8976200/44193845-85cd5d80-a134-11e8-8f39-2da1380fdc63.png)

La tabla de hechos tiene varias columnas numéricas que simplemente se agregan como siete medidas `SUM` sencillas:

![image](https://user-images.githubusercontent.com/8976200/44196409-270be200-a13c-11e8-9994-0a8f2fa19e1a.png)

A efectos de este artículo, las llamaremos **medidas base**. En un escenario real, la fórmula de las medidas base podría ser más compleja, pero en general eso no importa, como veremos en un momento. La idea central es que usaremos nuestro archivo TSV para definir un conjunto de fórmulas que involucren las medidas base, además de los contextos de filtro que se aplicarán fuera de los cálculos.

\*\*\* TODO \*\*\*

, siempre y cuando los cálculos que intentamos crear puedan seguir construyéndose a partir de una o más medidas base, evaluadas dentro de cualquier contexto de filtro válido.

\*\*\* TODO \*\*\*
