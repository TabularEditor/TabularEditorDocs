---
uid: sharing-macros-bpa-rules
title: Compartir macros, reglas de BPA y preferencias en todo el equipo
author: Just Blindbæk
updated: 2026-09-23
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

Esta página explica cómo un equipo, un departamento o un pipeline de CI mantiene sincronizados estos archivos de ruta fija con una copia compartida que está bajo control de versiones.

![Diagrama del flujo de configuración compartida](~/content/assets/images/sharing-config-two-paths.png)

> [!NOTE]
> Las reglas de BPA tienen compatibilidad nativa con orígenes compartidos, como se explica en [Compartir reglas de BPA](#sharing-bpa-rules). El resto de esta página trata sobre macros y preferencias.

## Empieza con un repositorio central de Git

Mantén las macros compartidas y, si lo deseas, un archivo base compartido `Preferences.json` en un repositorio central de Git y trátalo como la fuente de referencia. Sea cual sea el mecanismo que uses para copiar los archivos en las máquinas de los desarrolladores, los obtiene de ese repositorio, de modo que:

- cualquier cambio en una macro pasa por una pull request, igual que un cambio en un modelo semántico
- el historial de commits muestra quién cambió cada macro y cuándo, y puedes revertir un cambio erróneo como cualquier otro commit
- los nuevos miembros del equipo obtienen la biblioteca de macros del equipo al clonar un repositorio
- el mismo repositorio puede contener las colecciones de reglas de BPA del equipo (consulta [Compartir reglas de BPA](#sharing-bpa-rules)), lo que mantiene los estándares compartidos en un solo lugar

## ¿El mismo repositorio que tu modelo semántico o un repositorio independiente?

Antes de elegir un mecanismo de sincronización, decide si las macros compartidas y las reglas de BPA están en el mismo repositorio que tu modelo semántico o en un repositorio dedicado.

Empieza con el repositorio del modelo semántico, donde las macros y las reglas son archivos que están junto al modelo y se versionan conjuntamente. En [GitHub Flow](xref:github-flow), una feature branch creada desde `main` contiene las macros y las reglas vigentes en ese momento, sin ningún paso adicional. Un cambio en una macro se realiza en otra feature branch y otra pull request, y el diff muestra que solo afecta a `MacroActions.json`.

Usa un repositorio independiente y dedicado cuando tengas varios repositorios de modelos semánticos independientes, por ejemplo, uno por equipo o departamento. Sin él, cada repositorio de modelos semánticos necesita su propia copia de las macros y reglas compartidas, y tendrás que mantener esas copias sincronizadas manualmente.

En un entorno con varios equipos, comprueba si necesitas un único repositorio compartido de macros o una línea base compartida con incorporaciones locales, como un conjunto de macros para toda la organización al que un departamento añade sus propias macros. Las colecciones de reglas de BPA admiten de forma nativa varios orígenes (consulta [Compartir reglas de BPA](#sharing-bpa-rules)); para las macros, consulta [Combinar varios orígenes de macros](#combining-multiple-macro-sources).

Si tu equipo mantiene un único repositorio para el modelo semántico, usa el enfoque del mismo repositorio. Si esperas tener más repositorios de modelos semánticos en el plazo de un año, empieza con un repositorio independiente: sacar más adelante las macros compartidas de un repositorio de modelos semánticos da más trabajo.

Los mecanismos de sincronización siguientes funcionan igual en ambas configuraciones. Con un repositorio dedicado de macros, apuntan a un segundo clon.

## Compartir macros

Tabular Editor lee un archivo `MacroActions.json` por usuario desde una ruta fija, y las macros no tienen un equivalente a las colecciones de reglas de BPA. Consulta la [referencia de la Vista de macros](xref:macros-view-reference) para conocer la estructura del archivo.

> [!NOTE]
> Tabular Editor no descarga ni carga macros desde una página web, un repositorio de GitHub, un marketplace ni ninguna otra ubicación remota. Las macros son C# Scripts, así que compartirlas depende del mecanismo que tú o tu equipo configuren y gestionen.

Tabular Editor solo lee y escribe la copia local de `MacroActions.json` y no tiene integración con Git para este archivo. Cada una de las siguientes opciones mueve el archivo entre tu repositorio Git y la ruta local fija. Se diferencian en qué realiza el traslado, en qué dirección y qué lo activa.

### Opción A: enlace simbólico

Reemplaza el archivo de la ruta fija por un enlace simbólico al archivo de tu repositorio. Tabular Editor pasa a leer y escribir tu copia de trabajo de `MacroActions.json`.

```powershell
New-Item -ItemType SymbolicLink -Path "$env:LOCALAPPDATA\TabularEditor3\MacroActions.json" -Target "C:\path\to\your\repo\MacroActions.json"
```

(Para Tabular Editor 2, usa `%LOCALAPPDATA%\TabularEditor\` en lugar de `%LOCALAPPDATA%\TabularEditor3\`.)

- El enlace es bidireccional: los cambios que hagas en la interfaz de Tabular Editor se reflejan en tu copia de trabajo, listos para revisarlos y hacer commit.
- Aun así, debes ejecutar `git pull` para obtener los cambios de otro miembro del equipo.
- Crear un enlace simbólico en Windows requiere el Modo de desarrollador o una consola elevada, algo que las directivas suelen bloquear en equipos administrados. TI puede conceder el permiso de forma centralizada (mediante una directiva de dispositivo o el derecho `SeCreateSymbolicLinkPrivilege`) al implementar Tabular Editor, y un pequeño script crea el enlace después de que un desarrollador clone el repositorio.

### Opción B: hook de pre-commit

Un [hook pre-commit de Git](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks), versionado en el repositorio, copia `MacroActions.json` del repositorio a `%LOCALAPPDATA%\\TabularEditor3\\` en cada commit (`%LOCALAPPDATA%\\TabularEditor\\` para Tabular Editor 2).

- No requiere permisos elevados ni el Modo de desarrollador. La ruta de origen es relativa a la raíz del repositorio y `%LOCALAPPDATA%` se resuelve por usuario. El hook funciona dondequiera que un desarrollador clone el repositorio.
- La copia es unidireccional y se ejecuta en cada commit. El cambio de un compañero te llega después de que se fusione su pull request y hagas pull de `main`. Si tu rama pasa mucho tiempo sin hacer `pull` de `main`, añade un hook `post-merge` o `post-checkout`.
- Una edición realizada en la interfaz de usuario de Tabular Editor permanece local hasta que la copies de vuelta al repositorio y hagas commit. Si no lo haces, el hook la sobrescribe en el siguiente commit.

### Opción C: una herramienta que copia al ejecutar `apply`

Los gestores de dotfiles, como [chezmoi](https://www.chezmoi.io/), mantienen el archivo en un repositorio, lo copian a su ubicación de destino con un comando `apply` y copian de vuelta las ediciones locales con un comando `add`. Nada se escribe automáticamente.

- Como la opción B, no requiere permisos elevados ni depende de una ruta de clonación específica. Ambas direcciones requieren comandos explícitos.
- Tienes que aprender una herramienta de terceros para un único archivo JSON. Si tu equipo ya gestiona así otras configuraciones de las máquinas de desarrollo (por ejemplo, una configuración compartida de VS Code o Git), las macros son un archivo más dentro de ese sistema.

> [!NOTE]
> Ninguna de estas opciones es un mecanismo oficial, así que elige una y úsala para todos los archivos compartidos.

### Combinar varias fuentes de macros

Cada una de las opciones anteriores mueve un solo archivo, y las macros no admiten de forma nativa varios orígenes. Para combinar un conjunto central de macros con uno departamental o personal, escribe un script que fusione los archivos antes de que Tabular Editor lea `MacroActions.json`. Haz que el script sea lo bastante simple como para que cualquier desarrollador del equipo pueda corregirlo.

## Compartir preferencias

`Preferences.json` tiene la misma ruta fija que las macros y no admite de forma nativa varios orígenes. Cualquiera de las tres opciones anteriores sirve en este caso.

## Compartir reglas del BPA

Tabular Editor combina de forma nativa reglas de Best Practice Analyzer de varios orígenes:

- **Colecciones de reglas**: un modelo obtiene reglas del modelo actual, del `BPARules.json` del usuario local, de un `BPARules.json` de todo el sistema y de cualquier colección adicional que agregues. Una colección adicional es un archivo en disco, un recurso compartido de red o una URL HTTP/HTTPS. Las rutas de archivo pueden ser relativas al modelo, lo que permite alojar el archivo de reglas en el repositorio del modelo. Las colecciones tienen un orden de prioridad y una regla del modelo anula una regla central compartida. Consulta [Agregar una colección de reglas](xref:best-practice-analyzer#adding-a-rule-collection).
- **Reglas integradas** (Tabular Editor 3): un conjunto versionado de reglas de procedimientos recomendados que se incluye con la aplicación, se actualiza con cada versión y vincula cada regla con un artículo de la base de conocimientos. Se ejecutan junto con tus reglas personalizadas. Consulta [Reglas BPA integradas](xref:built-in-bpa-rules).

Un archivo de reglas compartido en un repositorio, agregado como colección mediante una ruta relativa, un recurso compartido de red o una URL, cubre la mayoría de los escenarios de equipo. Tabular Editor lee la colección directamente, así que no hace falta ningún enlace simbólico ni hook, y la decisión anterior de usar el mismo repositorio o uno independiente tiene poco efecto sobre las reglas de BPA.

### Qué tipo de colección usar

Para la mayoría de los equipos, usa un archivo con ruta relativa en el repositorio Git del modelo semántico:

- **URL**: Tabular Editor no permite editar una colección de reglas cargada desde una URL HTTP/HTTPS. Usa una URL para conjuntos de reglas que consumas sin cambios, como las [reglas BPA estándar de Analysis Services de Microsoft](https://github.com/microsoft/Analysis-Services/tree/master/BestPracticeRules). Para las reglas que edita tu equipo, mantendrías el archivo en otro lugar y publicarías en esa URL un espejo de solo lectura.
- **Recurso compartido de red**: cada máquina necesita acceso a la misma ubicación de red. Esto funciona en una implementación local o de una sola oficina, pero no para desarrolladores remotos ni para agentes de CI/CD hospedados en la nube sin acceso a tu red interna.
- **Ruta relativa**: el archivo de reglas es un archivo normal del repositorio, que se edita y revisa como cualquier otro. Cada máquina con el repositorio clonado, incluidos los agentes de compilación de CI/CD, tiene el archivo de reglas.

Las rutas relativas solo se resuelven cuando el modelo se carga desde el disco (un modelo de "Guardar en carpeta"). No se resuelven cuando Tabular Editor se conecta directamente a una instancia de Analysis Services o Power BI. El desarrollo en paralelo con Git y [Guardar en carpeta](xref:parallel-development#what-is-save-to-folder) carga el modelo desde el disco, por lo que esto solo afecta a los miembros del equipo que se conectan directamente a un Workspace en vivo.

Si tu equipo ya tiene una ubicación de red compartida a la que todos los equipos pueden acceder, también sirve un recurso compartido de red.

## Resumen

| Objetivo                                                                                  | Enfoque                                                                                                                                                                                                                                                                     |
| ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Decide dónde se guardan las macros o reglas compartidas                                   | El mismo repositorio que el modelo semántico si mantienes un único repositorio para el modelo; un repositorio dedicado aparte si mantienes varios. Consulta [¿El mismo repo o un repo independiente?](#same-repo-as-your-semantic-model-or-a-separate-repo) |
| Compartir reglas de BPA con el equipo                                                     | Colección de archivos con rutas relativas en un repositorio de Git. Consulta [Qué tipo de colección usar](#which-collection-type-to-use) para las colecciones de recursos compartidos de red y de URL                                                       |
| Obtén un conjunto base de reglas mantenido, sin necesidad de configuración                | [Reglas BPA integradas](xref:built-in-bpa-rules) (Tabular Editor 3)                                                                                                                                                                                      |
| Compartir macros o preferencias de forma bidireccional                                    | Enlace simbólico (opción A). Requiere hacer `git pull` para obtener los cambios de un compañero de equipo y tener permiso para crear enlaces simbólicos                                                                                  |
| Compartir macros o preferencias, sin permisos elevados                                    | Hook de pre-commit (opción B). Unidireccional; se sincroniza al hacer commit                                                                                                                                                             |
| Comparte macros o preferencias con comandos explícitos                                    | Un gestor de dotfiles, como chezmoi (opción C). Es ideal si tu equipo ya lo usa para otras configuraciones                                                                                                                               |
| Combinar varios orígenes de macros (central + departamento + personal) | Un script de fusión que combina los arrays en el único archivo que lee Tabular Editor                                                                                                                                                                                       |
| Cargar macros desde una ubicación que el usuario no controla                              | No se admite. Las macros son código ejecutable                                                                                                                                                                                                              |

## Siguientes pasos

- @best-practice-analyzer
- @built-in-bpa-rules
- @macros-view-reference
- @parallel-development
