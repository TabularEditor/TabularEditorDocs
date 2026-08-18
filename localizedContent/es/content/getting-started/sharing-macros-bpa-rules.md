---
uid: sharing-macros-bpa-rules
title: Compartir macros, reglas de BPA y preferencias en todo el equipo
author: Just Blindbæk
updated: 2026-07-06
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Compartir macros, reglas de BPA y preferencias en todo el equipo

Tabular Editor lee varios archivos de configuración desde una ubicación fija en el equipo de cada usuario: `%LOCALAPPDATA%\\TabularEditor3\\` para Tabular Editor 3, o `%LOCALAPPDATA%\\TabularEditor\\` para Tabular Editor 2. Los más importantes son [`MacroActions.json`](xref:supported-files#macroactionsjson) (las macros del usuario), [`BPARules.json`](xref:supported-files#bparulesjson) (las reglas locales del Best Practice Analyzer (BPA) del usuario) y `Preferences.json` (preferencias generales de la aplicación). Consulta [Tipos de archivo admitidos](xref:supported-files#local-setting-files) para ver una descripción completa de estos y de los demás archivos de configuración local.

Esa configuración predeterminada funciona para un único desarrollador. Los equipos que quieren un conjunto compartido y coherente de macros o preferencias para todo el equipo, un departamento o entre el desarrollo local y la CI se topan con una pregunta evidente: ¿cómo se mantiene sincronizado un archivo en una ruta local fija con algo compartido y bajo control de versiones?

![Diagrama del flujo de configuración compartida](~/content/assets/images/sharing-config-two-paths.png)

> [!NOTE]
> Si lo que quieres compartir son reglas de BPA, esto ya está resuelto. Consulta [Compartir reglas de BPA](#sharing-bpa-rules) a continuación. El resto de esta página trata sobre macros y preferencias, que no tienen la misma compatibilidad nativa.

## Empieza con un repositorio central de Git

Sea cual sea el mecanismo que uses para llevar archivos al equipo de un desarrollador, debería obtenerlos de un único repositorio central de Git dedicado a la configuración compartida: macros y, opcionalmente, un `Preferences.json` compartido como línea base de preferencias. Considerar ese repositorio como la fuente de referencia, en lugar del equipo de un desarrollador concreto, es lo que hace que compartir tenga sentido:

- Los cambios en una macro se pueden revisar mediante una pull request, igual que revisarías un cambio en un modelo semántico.
- Tienes un historial completo de quién cambió qué macro y cuándo, y puedes revertir un cambio erróneo igual que revertirías cualquier otro commit.
- Los nuevos miembros del equipo obtienen toda la biblioteca de macros del equipo clonando un repositorio, en lugar de copiar archivos del ordenador de un compañero.
- El mismo repositorio también puede servir como origen para las colecciones de reglas de BPA (consulta más abajo), de modo que los estándares compartidos del equipo queden en un solo lugar en vez de estar dispersos entre varios mecanismos de sincronización.

## ¿El mismo repositorio que tu modelo semántico, o uno independiente?

Antes de elegir un mecanismo de sincronización, decide dónde están las macros compartidas y las reglas de BPA: en el mismo repositorio que tu modelo semántico o en un repositorio dedicado.

Usar el mismo repositorio que tu modelo semántico es la opción predeterminada más simple y el punto de partida adecuado. Las macros y las reglas son archivos que están junto al modelo y se versionan de forma conjunta. Con [GitHub Flow](xref:github-flow), al crear una rama de funcionalidad a partir de `main`, obtienes las macros y reglas vigentes en ese momento, sin ningún paso adicional. Mantenerlas actualizadas sale gratis gracias al uso de ramas, que ya haces para cada tarea. Un cambio en una macro es otra rama de características y otro pull request, como cualquier otro cambio. Los revisores ven en el diff que solo se modifica `MacroActions.json`, así que no hay confusión sobre qué está en revisión.

Un repositorio dedicado e independiente tiene sentido cuando ya tienes varios repositorios de modelos semánticos realmente independientes: distintos equipos o departamentos, cada uno con el suyo. Sin él, cada repositorio de modelos semánticos necesita su propia copia de las macros y reglas compartidas. Mantener sincronizadas esas copias se convierte en otro problema manual, justo lo contrario de lo que se pretendía resolver al centralizarlas.

Incluso en ese escenario con varios equipos, comprueba si la necesidad real es un único repositorio independiente de macros o una base compartida con espacio para añadidos locales: por ejemplo, un conjunto de macros para toda la organización con las propias de un departamento añadidas encima. Es una cuestión de múltiples orígenes, más que de elegir entre el mismo repositorio o uno separado. Las colecciones de reglas de BPA lo admiten de forma nativa (consulta [Compartir reglas de BPA](#sharing-bpa-rules) más arriba). Para las macros, consulta [Combinar varios orígenes de macros](#combining-multiple-macro-sources) más abajo.

Si tu equipo mantiene hoy un único repositorio de modelo semántico, el enfoque del mismo repositorio es la opción más simple y el problema de la duplicación todavía no se plantea. Considera si eso seguirá siendo cierto dentro de un año, ya que migrar más adelante las macros compartidas fuera de un repositorio de modelo semántico requiere más trabajo que empezar con ellas por separado.

Elijas lo que elijas, los mecanismos de sincronización descritos a continuación funcionan igual. Un repositorio dedicado de macros solo implica acceder a un segundo repositorio, en lugar de a uno que ya tienes en local.

## Compartir macros

Las macros son distintas: Tabular Editor lee un único archivo `MacroActions.json` por usuario, desde una ruta fija, sin ningún equivalente al sistema de colecciones de reglas de BPA. Consulta la [referencia de la Vista de macros](xref:macros-view-reference) para ver cómo se estructura el propio archivo.

> [!NOTE]
> **Por qué no hay una funcionalidad integrada de carga remota:** Las macros son C# Scripts. Tabular Editor no descarga ni carga macros de forma deliberada desde ubicaciones que estén fuera del control del usuario, como una página web, un repositorio de GitHub o un "marketplace" público. Cargar y ejecutar código arbitrario desde un origen remoto sin que el usuario dé un paso explícito sería un riesgo de seguridad real. Cualquier mecanismo para compartir debe implicar algo que el propio usuario o equipo configure por su cuenta.

Tres enfoques que usan los equipos para conectar un repositorio central con la ruta local fija de Tabular Editor. Los tres mueven `MacroActions.json` entre tu repositorio de Git y esa ruta local fija; Tabular Editor solo lee y escribe la copia local, sin ningún concepto de Git. Lo que varía entre las opciones es quién realiza ese traslado, en qué dirección y qué lo desencadena:

### Opción A: enlace simbólico

La ruta fija pasa a ser un enlace a tu repositorio, de modo que Tabular Editor lee y escribe de forma transparente tu copia de trabajo de `MacroActions.json`.

```powershell
New-Item -ItemType SymbolicLink -Path "$env:LOCALAPPDATA\TabularEditor3\MacroActions.json" -Target "C:\path\to\your\repo\MacroActions.json"
```

(Para Tabular Editor 2, usa `%LOCALAPPDATA%\\TabularEditor\\` en lugar de `%LOCALAPPDATA%\\TabularEditor3\\`.)

- Bidireccional: las ediciones realizadas en la GUI de Tabular Editor llegan directamente a tu copia de trabajo, listas para revisarlas y hacer un commit, como cualquier otro cambio de archivo.
- Sigue haciendo falta un `git pull` explícito para traer los cambios de un compañero. El enlace simbólico elimina el paso manual de copia, pero no la necesidad de sincronizar con el repositorio remoto.
- Crear un enlace simbólico en Windows requiere tener habilitado el Modo de desarrollador o usar una consola con privilegios elevados, algo que las directivas suelen bloquear en equipos muy restringidos. En esos casos, TI puede conceder el permiso de forma centralizada (mediante una directiva de dispositivo o el derecho `SeCreateSymbolicLinkPrivilege`) como parte del despliegue de Tabular Editor, para que los desarrolladores no tengan que elevar privilegios por su cuenta. Después, un pequeño script independiente puede crear el enlace una vez que el desarrollador haya clonado el repositorio.

### Opción B: hook de pre-commit

Un [hook de pre-commit de Git](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks), incluido en el repositorio, que copia `MacroActions.json` del repositorio a `%LOCALAPPDATA%\\TabularEditor3\\` cada vez que haces un commit (`%LOCALAPPDATA%\\TabularEditor\\` para Tabular Editor 2).

- No se necesitan permisos elevados ni el Modo de desarrollador. Basta con una copia de archivo sencilla, y funciona independientemente de dónde haya clonado el repositorio cada desarrollador. El origen es relativo a la raíz del repositorio; el destino, `%LOCALAPPDATA%`, se resuelve automáticamente para cada usuario.
- Unidireccional: se sincroniza al hacer commit, no al hacer pull. No puedes ver los cambios de un compañero hasta que se integre su PR y tú hagas pull, así que rara vez importa, salvo que tu rama pase mucho tiempo sin incorporar `main`. Un hook de `post-merge` o `post-checkout` cierra esa brecha si llega a importar.
- Una edición hecha en la GUI de Tabular Editor se queda en local hasta que la copies manualmente de vuelta al repositorio y hagas commit. De lo contrario, se sobrescribe silenciosamente la próxima vez que se ejecute el hook.

### Opción C: una herramienta de copia al aplicar

Los gestores de dotfiles como [chezmoi](https://www.chezmoi.io/) resuelven en general el mismo problema. Guarda el archivo en un repositorio, cópialo a su ubicación de destino con un comando `apply` y copia las ediciones locales de vuelta con un comando `add`. Nada se enlaza ni se escribe automáticamente.

- Los mismos beneficios prácticos que la opción B (sin permisos elevados ni dependencia de una ruta de clonación local concreta), pero en ambos sentidos se requieren comandos explícitos, algo que algunos equipos prefieren frente a la escritura silenciosa de un enlace simbólico.
- La contrapartida es tener que aprender una herramienta de terceros con sus propios conceptos, probablemente más de lo que necesita por sí solo un único archivo JSON. La excepción es un equipo que ya gestiona así otra configuración de la máquina del desarrollador (por ejemplo, una configuración compartida de VS Code o Git); en ese caso, las macros pasan a ser un archivo más dentro de un sistema que el equipo ya ha adoptado.

> [!NOTE]
> Ninguna de estas es «la» forma oficial de hacerlo. Cada una implica ventajas e inconvenientes distintos para el mismo problema. Elige una y úsala de forma coherente, en lugar de mezclar mecanismos según el archivo.

### Combinar varias fuentes de macros

Ninguna de las tres opciones anteriores puede combinar más de una fuente a la vez. Todas se limitan a mover un único archivo de un lugar a otro. Para combinar un conjunto central de macros con otro departamental o personal, necesitas un script que las fusione antes de que Tabular Editor lea el archivo. Esto es una solución alternativa, no una funcionalidad de primera clase: a diferencia de las reglas de BPA, las macros no tienen un equivalente nativo a las colecciones de reglas. Manténlo lo bastante simple como para que cualquier desarrollador pueda entenderlo y corregirlo.

## Compartir preferencias

`Preferences.json` tiene la misma limitación de ruta fija que las macros, sin compatibilidad nativa con múltiples fuentes. Cualquiera de las tres opciones anteriores funciona de forma idéntica en este caso.

## Compartir reglas de BPA

Tabular Editor ofrece compatibilidad de primera clase para combinar reglas de Best Practice Analyzer de varias fuentes, sin necesidad de enlaces simbólicos ni soluciones alternativas:

- Las **colecciones de reglas** permiten que un modelo tome reglas del modelo actual, del `BPARules.json` del usuario local, de un `BPARules.json` para toda la máquina y de cualquier cantidad de colecciones adicionales que añadas explícitamente. Esas fuentes adicionales incluyen un archivo en otra ubicación del disco (con compatibilidad con rutas relativas al modelo, por lo que el archivo de reglas puede estar en el mismo repositorio), un recurso compartido de red o una dirección URL HTTP/HTTPS. Las colecciones tienen un orden de precedencia definido, por lo que una regla central compartida puede sobrescribirse a nivel de modelo cuando sea necesario. Consulta [Administrar reglas de prácticas recomendadas](xref:best-practice-analyzer#managing-best-practice-rules) para saber cómo añadir y priorizar colecciones.
- **Reglas integradas** (Tabular Editor 3) incorporan en la propia aplicación un conjunto seleccionado y versionado de reglas de mejores prácticas, que se actualiza automáticamente con cada versión, con artículos de la base de conocimiento vinculados desde cada regla. Estas conviven con tus reglas personalizadas en lugar de sustituirlas. Consulta [Reglas BPA integradas](xref:built-in-bpa-rules).

Entre estas dos características, la mayoría de los escenarios de «cómo compartimos las reglas BPA en el equipo» quedan cubiertos de forma nativa. A menudo, basta con un archivo de reglas compartido, confirmado en un repositorio e incluido como colección mediante una ruta relativa, un recurso compartido de red o una URL. No se requiere ningún enlace simbólico ni hook, ya que Tabular Editor lee la colección directamente, en lugar de hacerlo desde una ruta personal fija.

> [!NOTE]
> Como las colecciones de reglas pueden apuntar a una ruta relativa, un recurso compartido de red o una URL, la cuestión anterior de usar el mismo repositorio o uno independiente importa mucho menos para las reglas BPA que para las macros. Una colección de reglas funciona igual independientemente del repositorio en el que esté el archivo de reglas, ya que no hace falta copiar nada ni crear enlaces simbólicos en una ruta local fija primero. Esta es una ventaja práctica del soporte nativo de BPA para varios orígenes frente a los mecanismos de copia de archivos que actualmente requieren las macros.

### Qué tipo de colección usar

De las tres formas de agregar una colección de reglas externa, el valor predeterminado recomendado para la mayoría de los equipos es un archivo con ruta relativa en un repositorio Git, por motivos que las otras dos opciones no comparten:

- Las colecciones basadas en URL son de solo lectura. Tabular Editor no permite editar una colección de reglas cargada desde una URL HTTP/HTTPS. Es una restricción razonable para algo como las [reglas BPA estándar de Analysis Services](https://github.com/microsoft/Analysis-Services/tree/master/BestPracticeRules) de Microsoft, que se consumen tal cual. Eso descarta una URL como ubicación principal para un conjunto de reglas que tu propio equipo edita activamente: mantendrías el archivo real en otro lugar y tratarías la URL como un espejo de solo lectura, lo que añade más complejidad de la que compensa.
- Los recursos compartidos de red asumen que todas las máquinas pueden acceder a la misma ubicación de red. Eso encaja en una configuración local o de una sola oficina, pero es una mala opción para un equipo distribuido, para cualquiera que trabaje en remoto o para un agente de canalización de CI/CD centrado en la nube que no tendrá montada la red interna de tu organización.
- Una ruta relativa incluida en el propio repositorio Git del modelo semántico evita ambos problemas. Es totalmente editable, un archivo normal que se edita y revisa como cualquier otro del repositorio, y no presupone ninguna topología de red. Cualquier máquina que tenga clonado el repositorio también tiene el archivo de reglas, ya sea el portátil de un desarrollador o un agente de compilación de CI/CD.

Hay una limitación que conviene conocer: las rutas relativas solo se resuelven cuando el modelo se carga desde disco (un modelo de tipo Guardar en carpeta), no cuando Tabular Editor se conecta directamente a una instancia activa de Analysis Services o Power BI. Esto rara vez importa en el desarrollo en paralelo basado en Git y [Guardar en carpeta](xref:parallel-development#what-is-save-to-folder), ya que el modelo permanece en disco en todo momento. Compruébalo si, en cambio, parte de tu equipo se conecta directamente a un Workspace activo.

Si tu equipo ya tiene una ubicación de red compartida y accesible, y prefiere no introducir un archivo por repositorio, un recurso compartido de red es una alternativa viable. Cambia portabilidad por la comodidad que ofrezca tu configuración actual de recursos compartidos. Reserva una colección basada en URL para consumir un conjunto de reglas externo y de solo lectura (como las reglas estándar de Microsoft), en lugar de las reglas que mantiene tu propio equipo.

## Resumen

| Objetivo                                                                                     | Enfoque                                                                                                                                                                                                                                                                                                                                                                                  |
| -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Decide dónde deben residir las macros o reglas compartidas                                   | En el mismo repositorio que tu modelo semántico si solo mantienes uno; en un repositorio dedicado independiente si mantienes varios; consulta [¿El mismo repositorio o uno independiente?](#same-repo-as-your-semantic-model-or-a-separate-repo)                                                                                                                                         |
| Compartir reglas de BPA con un equipo                                                        | Colección de archivos con rutas relativas en un repositorio Git (recomendada de forma predeterminada); consulta [Qué tipo de colección usar](#which-collection-type-to-use). También puedes usar un recurso compartido de red o una colección basada en URL; consulta la sección enlazada para conocer las ventajas e inconvenientes. |
| Obtener un conjunto de reglas base, seleccionado y mantenido, sin necesidad de configuración | [Reglas BPA integradas](xref:built-in-bpa-rules) (TE3)                                                                                                                                                                                                                                                                                                                |
| Compartir macros o preferencias, en ambos sentidos                                           | Enlace simbólico (opción A). Aún así, necesitas hacer `git pull` para incorporar los cambios de un compañero; puede que necesites que TI te conceda permisos en equipos con restricciones                                                                                                                                                             |
| Compartir macros o preferencias, sin permisos elevados                                       | Hook pre-commit (opción B): unidireccional; sincroniza al hacer commit, no al hacer pull                                                                                                                                                                                                                                                              |
| Compartir macros o preferencias, de forma explícita y revisable                              | Una herramienta de gestión de dotfiles como chezmoi (opción C): requiere aprender más; es mejor si ya la usas para otra configuración                                                                                                                                                                                                                 |
| Combinar varias fuentes de macros (central + del departamento + personal) | Un script de combinación que concatena los arrays en un único archivo que lee Tabular Editor; es una solución alternativa, no integrada                                                                                                                                                                                                                                                  |
| Cargar macros desde una ubicación que el usuario no controla                                 | No se admite, por diseño: las macros son código ejecutable                                                                                                                                                                                                                                                                                                               |

## Siguientes pasos

- @best-practice-analyzer
- @built-in-bpa-rules
- @macros-view-reference
- @parallel-development
