---
uid: te-cli-skill
title: Habilidad de agente de IA
author: Morten Lønskov
updated: 2026-06-04
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# Habilidad de agente de IA

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

Tabular Editor CLI incluye un **skill de agente** listo para usar que enseña a los agentes de programación con IA a manejar la interfaz de línea de comandos `te`. Es un único archivo Markdown, [`SKILL.md`](https://github.com/TabularEditor/CLI/tree/main/skills/te-cli), que reúne las convenciones de la CLI, la referencia de comandos, los flujos de trabajo y los aspectos a tener en cuenta. Una vez instalado, un agente responde a «despliega este modelo» o «añade una medida que calcule el margen» con invocaciones idiomáticas de `te`, en lugar de adivinar o inventarse parámetros.

El skill se mantiene en el repositorio público [TabularEditor/CLI](https://github.com/TabularEditor/CLI/tree/main/skills/te-cli) y hace un seguimiento de las funcionalidades en versión preliminar de la CLI a medida que evoluciona.

## Qué es un skill

Un skill es un archivo Markdown que un agente de IA carga bajo demanda en función de tu prompt. Su frontmatter YAML (`name`, `description`, `version`) le indica al agente **cuándo** cargarlo y **qué** cubre. El cuerpo en Markdown le enseña al agente **cómo** realizar la tarea.

## Qué cubre el skill

El skill enseña al agente toda la superficie de `te`:

- todos los comandos de `te` en todas sus familias: load, save, init, deploy, refresh, bpa, validate, query, script, format y más
- patrones de autenticación: interactiva, entidad de servicio con secreto o certificado, variables de entorno, identidad administrada
- gramática de rutas de objeto: forma con barras, forma DAX y comodines
- el modelo de staging: comportamiento de `--save`, `--stage` y `--revert`
- Correspondencias de migración de TE2 a CLI
- Recetas de CI/CD para GitHub Actions y Azure DevOps
- formatos de salida, códigos de salida, variables de entorno y claves de configuración
- una hoja de referencia de propiedades comunes de `-q`
- los escollos que hacen tropezar a los agentes en la práctica

Esto cubre lo mismo que el resto de esta sección documenta para humanos. Consulta @te-cli-commands para la referencia de comandos, @te-cli-auth para la autenticación y @te-cli-cicd para patrones de canalización.

## Descarga el archivo del skill

Este skill es un único archivo: [`SKILL.md`](https://github.com/TabularEditor/CLI/blob/main/skills/te-cli/SKILL.md).

1. Abre [`SKILL.md`](https://github.com/TabularEditor/CLI/blob/main/skills/te-cli/SKILL.md) en GitHub.
2. Haz clic en **Download raw file** (en la parte superior derecha del visor de archivos).
3. Guarda el archivo en un lugar práctico.

Moverás este archivo a una ubicación específica de la herramienta en los pasos de instalación que se indican a continuación. Para ver qué cambió entre versiones antes de descargar una copia más reciente, consulta el [CHANGELOG](https://github.com/TabularEditor/CLI/blob/main/skills/te-cli/CHANGELOG.md).

## Elige un ámbito de instalación

Todos los agentes admiten dos ámbitos de instalación:

- **Ámbito de proyecto** - la habilidad está disponible solo en un proyecto o repositorio. Úsalo cuando no todos los proyectos trabajen con modelos semánticos.
- **Ámbito de usuario** - la habilidad está disponible en todos los proyectos de tu máquina. Úsalo si trabajas con modelos semánticos en muchos repositorios.

## Instalación para Claude Code

Claude Code carga las habilidades desde una carpeta con un nombre específico dentro de `.claude/skills/`. El campo `description` se compara con tus prompts, así que la habilidad solo se carga cuando corresponde; no consume tokens cuando estás trabajando en código no relacionado.

**Ámbito de proyecto** - la habilidad solo se carga dentro de este proyecto:

1. En la raíz de tu proyecto, crea la carpeta `.claude/skills/te-cli/`.
2. Coloca el archivo `SKILL.md` descargado dentro de esa carpeta.

La ruta final es `<your-project>/.claude/skills/te-cli/SKILL.md`.

**Ámbito de usuario** - la habilidad se carga en todos los proyectos del usuario actual:

1. Crea una carpeta `te-cli` dentro de tu directorio de habilidades de Claude a nivel de usuario:
   - **macOS / Linux:** `~/.claude/skills/te-cli/`
   - **Windows:** `%USERPROFILE%\.claude\skills\te-cli\` (normalmente `C:\Users\<you>\.claude\skills\te-cli\`)
2. Coloca el archivo `SKILL.md` descargado dentro de esa carpeta.

> [!NOTE]
> Claude Code vigila los directorios de habilidades y detecta habilidades nuevas o editadas durante la sesión actual; no necesitas reiniciar. La excepción es crear un directorio `.claude/skills/` que no existía al iniciar la sesión: reinicia Claude Code una vez para que empiece a vigilar el nuevo directorio.

### Verifica que la habilidad se haya cargado

Dentro de una sesión de Claude Code, ejecuta:

```
/skills
```

Deberías ver `te-cli` en la lista. Si no aparece, confirma la ruta del archivo y que el archivo empiece con `---` y tenga `name: te-cli` en la segunda línea; después, reinicia Claude Code.

Para hacer una prueba de humo funcional, pregunta:

```
what does `te deploy --xmla` do?
```

Claude responde con el comportamiento documentado: genera un script TMSL/XMLA en stdout en lugar de desplegarlo, lo que confirma que la skill está cargada y en uso.

## Instalación para Claude.ai y Claude Desktop

Claude.ai (web y escritorio) incluye una función integrada de **Skills**. Las Skills requieren ejecución de código, y debes subirlas como un archivo ZIP de la carpeta de la skill, en lugar del `SKILL.md` suelto.

1. Activa la ejecución de código: ve a **Configuración > Capacidades** y habilita **Ejecución de código y creación de archivos**. En los planes Team y Enterprise, un propietario lo habilita en la configuración de la organización.
2. Coloca el `SKILL.md` descargado dentro de una carpeta llamada `te-cli` y, después, comprime esa carpeta en `te-cli.zip`.
3. Ve a **Configuración > Capacidades > Skills** (también accesible desde **Personalizar > Skills**).
4. Haz clic en **+**, elige **Subir una skill** y selecciona `te-cli.zip`. Claude lee el `SKILL.md` incluido y muestra un resumen de la skill.
5. Activa la skill. Se carga automáticamente cuando mencionas `te` o un concepto relacionado.

Las skills personalizadas que subas serán privadas y solo estarán disponibles en tu cuenta, a menos que un propietario habilite el uso compartido en toda la organización en Team o Enterprise.

Consulta el [artículo de ayuda sobre Skills de Anthropic](https://support.claude.com/en/articles/12512180-use-skills-in-claude) para ver el flujo actual de la interfaz si la redacción ha cambiado.

## Instalación para GitHub Copilot

GitHub Copilot en VS Code es compatible de forma nativa con el estándar abierto Agent Skills: el mismo formato `SKILL.md` que usan Claude Code y Codex. Este es el enfoque recomendado porque la skill solo se carga cuando es relevante. En configuraciones de Copilot anteriores a Agent Skills, usa como alternativa el archivo de instrucciones personalizadas siempre activo que aparece más abajo.

### Agent Skills (VS Code)

Coloca la skill en una carpeta con nombre dentro de un directorio de skills. El nombre de la carpeta debe coincidir con el campo `name` del frontmatter, así que usa `te-cli` y mantén intacto el frontmatter YAML.

- **Alcance del Workspace:** `.github/skills/te-cli/SKILL.md` (Copilot también lee `.claude/skills/` y `.agents/skills/`).
- **Ámbito de usuario:** `~/.copilot/skills/te-cli/SKILL.md` (Copilot también lee `~/.claude/skills/` y `~/.agents/skills/`).

Escribe `/` en Copilot Chat para confirmar que `te-cli` aparece como comando de barra, o abre el editor de personalizaciones del agente con **Chat: Abrir personalizaciones** desde la Paleta de comandos.

## Instalar para OpenAI Codex CLI

Codex CLI carga skills de forma nativa desde una carpeta con nombre dentro de `.agents/skills/`, el mismo modelo basado en directorios que usa Claude Code. Conserva el frontmatter YAML: Codex requiere los campos `name` y `description` y usa la descripción para decidir cuándo cargar la skill.

**Ámbito de proyecto**: la skill se carga solo dentro de este proyecto:

1. En la raíz del proyecto, crea la carpeta `.agents/skills/te-cli/`.
2. Coloca el archivo `SKILL.md` descargado dentro de esa carpeta.

Codex busca hacia arriba desde tu directorio de trabajo, así que una skill incluida en la raíz del repositorio (`$REPO_ROOT/.agents/skills/te-cli/`) se comparte con todos los que trabajan en el repositorio.

**Ámbito personal**: la skill se carga en todos los proyectos del usuario actual:

1. Crea la carpeta `te-cli` dentro de tu directorio personal de skills de Codex: `~/.agents/skills/te-cli/`.
2. Coloca el archivo `SKILL.md` descargado dentro de esa carpeta.

Ejecuta `/skills` en la CLI de Codex o en el IDE para confirmar que `te-cli` aparece en la lista, y escribe `te-cli` para mencionar una skill explícitamente.

## Instalar para agentes genéricos

Para herramientas que siguen la [convención `AGENTS.md`](https://agents.md) o aceptan un archivo de instrucciones arbitrario —Aider, Continue, agentes internos personalizados—:

1. Descarga `SKILL.md`.
2. Elimina el bloque de frontmatter YAML de la parte superior (todo lo que haya entre la primera y la segunda línea `---`, incluidas esas líneas).
3. Cambia el nombre del archivo a `AGENTS.md` y colócalo en la raíz del proyecto, o donde la herramienta espere su archivo de instrucciones.
4. La siguiente invocación del agente en ese proyecto detectará las instrucciones.

## Actualizar la skill

Para obtener una versión más reciente:

1. Abre [`SKILL.md`](https://github.com/TabularEditor/CLI/blob/main/skills/te-cli/SKILL.md) en GitHub y usa **Download raw file** para descargar la copia más reciente.
2. Sustituye el archivo que instalaste antes:
   - **Skills nativas (Claude Code, Codex, Copilot Agent Skills):** sobrescribe `SKILL.md` en la carpeta de la skill.
   - **Claude.ai / Desktop:** vuelve a comprimir en ZIP la carpeta `te-cli` y vuelve a subirla desde la interfaz de Skills.
   - **Instalaciones mediante archivos de instrucciones (instrucciones personalizadas de Copilot, AGENTS.md):** vuelve a pegar el texto completo en `.github/copilot-instructions.md` o `AGENTS.md`.

Consulta el [CHANGELOG](https://github.com/TabularEditor/CLI/blob/main/skills/te-cli/CHANGELOG.md) para ver qué cambió entre versiones.

## Siguientes pasos

- @te-cli-install - descarga, instala y verifica la CLI en sí.
- @te-cli-auth - autentícate en Power BI, Fabric y Azure Analysis Services.
- @te-cli-commands - referencia completa de comandos.
- @te-cli-automation - salida estructurada y patrones de scripting.
- @te-cli-cicd - pipelines de GitHub Actions y Azure DevOps.
