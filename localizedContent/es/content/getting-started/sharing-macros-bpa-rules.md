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

Tabular Editor lee varios archivos de configuración desde una ubicación fija en la máquina de cada usuario: `%LOCALAPPDATA%\\TabularEditor3\\` para Tabular Editor 3, o `%LOCALAPPDATA%\\TabularEditor\\` para Tabular Editor 2. Los más importantes son [`MacroActions.json`](xref:supported-files#macroactionsjson) (las macros del usuario), [`BPARules.json`](xref:supported-files#bparulesjson) (las reglas locales del Best Practice Analyzer (BPA) del usuario) y `Preferences.json` (las preferencias generales de la aplicación). Consulta [Tipos de archivo compatibles](xref:supported-files#local-setting-files) para ver una descripción completa de estos y de los demás archivos de configuración local.

Ese comportamiento predeterminado funciona para un único desarrollador. Los equipos que quieren un conjunto compartido y coherente de macros o preferencias para todo un equipo, un departamento o entre el desarrollo local y la CI se topan con una pregunta obvia: ¿cómo se mantiene sincronizado un archivo en una ruta local fija con algo compartido y controlado por versiones?

![Diagrama del flujo de configuración compartida](~/content/assets/images/sharing-config-two-paths.png)

> [!NOTE]
> Si lo que quieres compartir son reglas de BPA, esto ya está resuelto. Consulta [Compartir reglas de BPA](#sharing-bpa-rules) más abajo. El resto de esta página trata sobre macros y preferencias, que no tienen el mismo soporte nativo.

## Empieza con un repositorio central de Git

Sea cual sea el mecanismo que uses para llevar archivos a la máquina de un desarrollador, debería obtenerlos de un único repositorio central de Git dedicado a la configuración compartida: macros y, opcionalmente, un `Preferences.json` base compartido de preferencias. Tratar ese repositorio como la fuente de verdad, en lugar del equipo de un desarrollador concreto, es lo que hace que compartir tenga sentido:

- Los cambios en una macro se pueden revisar mediante una solicitud de extracción, igual que revisarías un cambio en un modelo semántico.
- Obtienes un historial completo de quién cambió qué macro y cuándo, y puedes revertir un cambio erróneo igual que revertirías cualquier otro commit.
- Los nuevos miembros del equipo obtienen toda la biblioteca de macros del equipo clonando un único repositorio, en lugar de copiar archivos desde la máquina de un compañero.
- El mismo repositorio también puede servir como origen para colecciones de reglas de BPA (consulta más abajo), de modo que los estándares compartidos del equipo vivan en un solo lugar en vez de quedar dispersos entre varios mecanismos de sincronización.

## ¿El mismo repositorio que tu modelo semántico o un repositorio independiente?

Antes de elegir un mecanismo de sincronización, decide dónde se almacenan las macros compartidas y las reglas de BPA: en el mismo repositorio que tu modelo semántico o en un repositorio dedicado.

El mismo repositorio que tu modelo semántico es la opción predeterminada más sencilla y el punto de partida adecuado. Las macros y las reglas son archivos que están junto al modelo y se versionan de forma conjunta. Con [GitHub Flow](xref:github-flow), al crear una rama de funcionalidad a partir de `main`, obtienes las macros y las reglas vigentes en ese momento, sin pasos adicionales. La actualización viene incluida con el uso de ramas, algo que ya haces en cada tarea. Un cambio en una macro implica otra rama de funcionalidad y otro pull request, como cualquier otro cambio. Los revisores ven en el diff que solo afecta a `MacroActions.json`, así que no hay confusión sobre lo que se está revisando.

Un repositorio independiente y dedicado tiene sentido cuando ya tienes varios repositorios de modelos semánticos realmente independientes: distintos equipos o departamentos, cada uno manteniendo el suyo. Sin él, cada repositorio del modelo necesita su propia copia de las macros y las reglas compartidas. Mantener esas copias sincronizadas se convierte en un problema manual en sí mismo, justo lo contrario de lo que se suponía que debía resolver centralizarlas.

Incluso en ese caso de varios equipos, comprueba si la necesidad real es un único repositorio separado de macros o una base compartida con margen para adiciones locales: por ejemplo, un conjunto de macros para toda la organización sobre el que cada departamento añade las suyas. Esa es una cuestión de múltiples orígenes, no de usar el mismo repositorio o un repositorio separado. Las colecciones de reglas de BPA admiten esto de forma nativa (consulta [Compartir reglas de BPA](#sharing-bpa-rules) más arriba). Para las macros, consulta [Combinar varios orígenes de macros](#combining-multiple-macro-sources) más abajo.

Si hoy tu equipo mantiene un único repositorio de modelo semántico, el enfoque de repositorio único es la opción más sencilla y la preocupación por la duplicación aún no aplica. Piensa si eso seguirá siendo así dentro de un año, porque más adelante sacar las macros compartidas del repositorio del modelo da más trabajo que empezar con ellas separadas.

Elijas lo que elijas, los mecanismos de sincronización que se describen a continuación funcionan igual. Un repositorio de macros dedicado solo significa que acceden a un segundo repositorio, en lugar de a uno que ya tienes clonado.

## Compartir macros

Las macros son distintas: Tabular Editor lee un único archivo `MacroActions.json` por usuario, desde una ruta fija, sin ningún equivalente al sistema de colecciones de reglas de BPA. Consulta la [referencia de la Vista de macros](xref:macros-view-reference) para ver cómo está estructurado el archivo.

> [!NOTE]
> **Por qué no hay una función integrada para cargar macros de forma remota:** Las macros son C# Scripts. Tabular Editor, deliberadamente, no descarga ni carga macros desde una ubicación fuera del control del usuario, como una página web, un repositorio de GitHub o un "marketplace" público. Cargar y ejecutar código arbitrario desde un origen remoto sin un paso explícito por tu parte supondría un riesgo de seguridad real. Cualquier mecanismo para compartirlas debe implicar algo que el usuario o el equipo configure por su cuenta.

Tres enfoques que usan los equipos para reducir la brecha entre un repositorio central y la ruta local fija de Tabular Editor. Los tres mueven `MacroActions.json` entre tu repositorio Git y esa ruta local fija; Tabular Editor solo lee y escribe la copia local, sin concepto de Git. Lo que cambia entre las opciones es qué se encarga de ese movimiento, en qué dirección y qué lo desencadena:

### Opción A: enlace simbólico

La ruta fija se convierte en un enlace a tu repositorio, de modo que Tabular Editor lee y escribe de forma transparente tu copia de trabajo de `MacroActions.json`.

```powershell
New-Item -ItemType SymbolicLink -Path "$env:LOCALAPPDATA\TabularEditor3\MacroActions.json" -Target "C:\path\to\your\repo\MacroActions.json"
```

(Para Tabular Editor 2, usa `%LOCALAPPDATA%\TabularEditor\` en lugar de `%LOCALAPPDATA%\TabularEditor3\`.)

- Bidireccional: las ediciones hechas en la interfaz gráfica de Tabular Editor llegan directamente a tu copia de trabajo, listas para revisar y hacer commit como cualquier otro cambio de archivo.
- Sigue necesitando un `git pull` explícito para traer los cambios de un compañero de equipo. El enlace simbólico elimina el paso de copia manual, no la necesidad de sincronizar con el repositorio remoto.
- Crear un enlace simbólico en Windows requiere tener habilitado el Modo de desarrollador o usar una consola elevada, algo que a menudo queda bloqueado por directivas en equipos restringidos. Cuando sea así, TI puede conceder el permiso de forma centralizada (mediante una directiva de dispositivo o el derecho `SeCreateSymbolicLinkPrivilege`) como parte del despliegue de Tabular Editor, para que los desarrolladores no tengan que elevar privilegios por su cuenta. Después, un pequeño script independiente puede crear el enlace una vez que un desarrollador haya clonado el repositorio.

### Opción B: hook de pre-commit

Un [hook pre-commit de Git](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks), incluido en el repositorio, que copia `MacroActions.json` del repositorio a `%LOCALAPPDATA%\TabularEditor3\` cada vez que haces un commit (`%LOCALAPPDATA%\TabularEditor\` para Tabular Editor 2).

- No necesitas permisos elevados ni activar el modo de desarrollador. Basta con copiar el archivo y funciona independientemente de dónde hayas clonado el repositorio. El origen es relativo a la raíz del repositorio; el destino, `%LOCALAPPDATA%`, se resuelve automáticamente para cada usuario.
- Unidireccional, y se sincroniza al hacer commit, no al hacer pull. No puedes ver el cambio de un compañero antes de que se fusione su PR y hagas un pull tú mismo, así que rara vez importa, salvo que tu rama pase mucho tiempo sin incorporar `main`. Un hook `post-merge` o `post-checkout` cierra esa brecha si fuera necesario.
- Una edición hecha en la GUI de Tabular Editor permanece en local hasta que la copies manualmente de vuelta al repositorio y hagas commit. Si no, el hook la sobrescribirá silenciosamente la próxima vez que se ejecute.

### Opción C: una herramienta que copia al ejecutar `apply`

Los gestores de dotfiles como [chezmoi](https://www.chezmoi.io/) resuelven el mismo problema de forma general. Guarda el archivo en un repositorio, cópialo a su ubicación de destino con un comando `apply` y copia de vuelta las ediciones locales con un comando `add`. Nada se enlaza ni se escribe automáticamente.

- Ofrece los mismos beneficios prácticos que la opción B (sin permisos elevados ni dependencia de una ruta concreta del clon local), pero en este caso ambos sentidos se gestionan mediante comandos explícitos, algo que algunos equipos prefieren frente a la propagación silenciosa de cambios que ofrece un enlace simbólico.
- El inconveniente es que hay que aprender una herramienta de terceros con conceptos propios, probablemente más de lo que requeriría por sí solo un único archivo JSON. La excepción sería un equipo que ya gestiona así otras configuraciones de las máquinas de desarrollo (por ejemplo, una configuración compartida de VS Code o de Git); en ese caso, las macros pasan a ser un archivo más dentro de un sistema que ya se usa.

> [!NOTE]
> Ninguna de ellas es "el" mecanismo oficial. Son distintas compensaciones para el mismo problema. Elige una y úsala de forma coherente en lugar de mezclar mecanismos según el archivo.

### Combinar varias fuentes de macros

Ninguna de las tres opciones anteriores puede combinar más de una fuente a la vez. Todas se limitan a mover un único archivo de un lugar a otro. Para combinar un conjunto central de macros con uno departamental o personal, necesitas un script que las fusione antes de que Tabular Editor lea el archivo. Esto es una solución alternativa, no una funcionalidad integrada: a diferencia de las reglas BPA, las macros no tienen un equivalente nativo a las colecciones de reglas. Mantenlo lo bastante simple como para que cualquier desarrollador pueda entenderlo y corregirlo.

## Compartir preferencias

`Preferences.json` tiene la misma limitación de ruta fija que las macros, sin compatibilidad nativa con varias fuentes. Cualquiera de las tres opciones anteriores funciona exactamente igual en este caso.

## Compartir reglas del BPA

Tabular Editor ofrece compatibilidad nativa para combinar reglas de Best Practice Analyzer de varias fuentes, sin necesidad de enlaces simbólicos ni soluciones alternativas:

- **Las colecciones de reglas** permiten que un modelo use reglas del modelo actual, del `BPARules.json` del usuario local, de un `BPARules.json` a nivel de máquina y de cualquier cantidad de colecciones adicionales que agregues explícitamente. Esas fuentes adicionales incluyen un archivo ubicado en otro lugar del disco (con compatibilidad con rutas relativas al modelo, para que el archivo de reglas pueda estar en el mismo repositorio), un recurso compartido de red o una dirección URL HTTP/HTTPS. Las colecciones tienen un orden de precedencia definido, por lo que una regla central compartida puede sobrescribirse a nivel de modelo cuando sea necesario. Consulta [Agregar una colección de reglas](xref:best-practice-analyzer#adding-a-rule-collection) para ver cómo agregar y priorizar colecciones.
- Las **reglas integradas** (Tabular Editor 3) incorporan directamente en la aplicación un conjunto seleccionado y versionado de reglas de buenas prácticas, que se actualiza automáticamente con cada versión, con artículos de la base de conocimientos enlazados desde cada regla. Estas conviven con tus reglas personalizadas en lugar de sustituirlas. Consulta [Reglas BPA integradas](xref:built-in-bpa-rules).

Con estas dos funciones, la mayoría de los escenarios de "cómo compartimos las reglas de BPA en el equipo" quedan cubiertos de forma nativa. Un archivo de reglas compartido, versionado en un repositorio e incluido como colección mediante una ruta relativa, un recurso compartido de red o una URL suele ser todo lo que necesitas. No hace falta ningún enlace simbólico ni hook, ya que Tabular Editor lee la colección directamente en lugar de hacerlo a través de una ruta personal fija.

> [!NOTE]
> Como las colecciones de reglas pueden apuntar a una ruta relativa, un recurso compartido de red o una URL, la pregunta anterior de si usar el mismo repositorio o uno independiente importa mucho menos para las reglas de BPA que para las macros. Una colección de reglas funciona igual independientemente del repositorio en el que esté el archivo de reglas, ya que no hace falta copiar nada ni crear un enlace simbólico en una ruta local fija. Esta es una ventaja práctica del soporte nativo de BPA para varios orígenes frente a los mecanismos de copia de archivos que las macros requieren actualmente.

### Qué tipo de colección usar

De las tres formas de agregar una colección de reglas externa, la opción recomendada por defecto para la mayoría de los equipos es un archivo con ruta relativa en un repositorio Git, por motivos que las otras dos opciones no comparten:

- Las colecciones basadas en URL son de solo lectura. Tabular Editor no permite editar una colección de reglas cargada desde una URL HTTP/HTTPS. Es una restricción razonable para algo como las [reglas BPA estándar de Analysis Services de Microsoft](https://github.com/microsoft/Analysis-Services/tree/master/BestPracticeRules), que se consumen tal cual. Eso descarta usar una URL como ubicación principal para un conjunto de reglas que el propio equipo edita activamente: habría que mantener el archivo real en otro lugar y tratar la URL como un espejo de solo lectura, lo que añade más complejidad de la que compensa.
- Los recursos compartidos de red presuponen que todas las máquinas pueden acceder a la misma ubicación de red. Esto encaja en una configuración local o de una sola oficina, pero encaja mal con un equipo distribuido, con personas que trabajan en remoto o con un agente de CI/CD orientado a la nube que no tendrá montada la red interna.
- Una ruta relativa incluida en el propio repositorio Git del modelo semántico evita ambos problemas. Se puede editar por completo; es un archivo normal que se edita y revisa como cualquier otro en el repositorio, y no presupone ninguna topología de red. Cualquier máquina que tenga clonado el repositorio también tiene el archivo de reglas, ya sea el portátil de un desarrollador o un agente de compilación de CI/CD.

Conviene conocer una limitación: las rutas relativas solo se resuelven cuando el modelo se carga desde disco (un modelo de "Guardar en carpeta"), no cuando Tabular Editor se conecta directamente a una instancia activa de Analysis Services o Power BI. Esto rara vez importa en un desarrollo en paralelo basado en Git y [Guardar en carpeta](xref:parallel-development#what-is-save-to-folder), ya que el modelo permanece en disco en todo momento. Compruébalo si parte del equipo se conecta directamente a un Workspace activo.

Si el equipo ya tiene una ubicación de red compartida y accesible, y prefiere no introducir un archivo por repositorio, un recurso compartido de red es una alternativa viable. Sacrifica la portabilidad a cambio de la comodidad que ofrezca la configuración actual de uso compartido de archivos. Reserva una colección basada en URL para consumir un conjunto de reglas externo y de solo lectura (como las reglas estándar de Microsoft), no para reglas que mantiene tu equipo.

## Resumen

| Objetivo                                                                                  | Enfoque                                                                                                                                                                                                                                                                                                                                                                         |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Decide dónde deben ubicarse las macros y reglas compartidas                               | El mismo repositorio que tu modelo semántico si solo mantienes uno de este tipo; un repositorio dedicado aparte si mantienes varios; consulta [¿El mismo repositorio o uno aparte?](#same-repo-as-your-semantic-model-or-a-separate-repo)                                                                                                                                       |
| Compartir reglas de BPA con el equipo                                                     | Colección de archivos con rutas relativas en un repositorio Git (opción predeterminada recomendada); consulta [Qué tipo de colección usar](#which-collection-type-to-use). También puedes usar un recurso compartido de red o una colección de URL; consulta la sección enlazada para conocer las ventajas e inconvenientes. |
| Obtén un conjunto de reglas base seleccionado y mantenido, sin necesidad de configuración | [Reglas BPA integradas](xref:built-in-bpa-rules) (TE3)                                                                                                                                                                                                                                                                                                       |
| Compartir macros o preferencias de forma bidireccional                                    | Enlace simbólico (opción A). Aún requiere `git pull` para incorporar los cambios de un compañero; puede que el equipo de TI tenga que conceder permisos en equipos bloqueados                                                                                                                                                                |
| Compartir macros o preferencias, sin permisos elevados                                    | Hook de pre-commit (opción B): unidireccional; se sincroniza al hacer commit, no al hacer pull                                                                                                                                                                                                                                               |
| Compartir macros o preferencias, de forma explícita y revisable                           | Una herramienta de gestión de dotfiles como chezmoi (opción C): requiere aprender más, y es mejor si ya la usas para otras configuraciones                                                                                                                                                                                                   |
| Combinar varios orígenes de macros (central + departamento + personal) | Un script de combinación que concatena los arrays en el único archivo que lee Tabular Editor; es una solución alternativa, no integrada                                                                                                                                                                                                                                         |
| Cargar macros desde una ubicación que el usuario no controla                              | No se admite, por diseño: las macros son código ejecutable                                                                                                                                                                                                                                                                                                      |

## Siguientes pasos

- @best-practice-analyzer
- @built-in-bpa-rules
- @macros-view-reference
- @parallel-development
