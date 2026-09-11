---
uid: te-cli-skill
title: Habilidad de agente de IA
author: Morten Lønskov
updated: 2026-09-04
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

Tabular Editor CLI incluye un **skill de agente** listo para usar que enseña a los agentes de programación con IA a manejar la interfaz de línea de comandos `te`. It's a skill folder - a [`SKILL.md`](https://github.com/TabularEditor/CLI/tree/main/skills/te-cli) entry point plus a `references/` set of on-demand deep-dive files - packed with the CLI's conventions, command reference, workflows, and gotchas. Una vez instalado, un agente responde a «despliega este modelo» o «añade una medida que calcule el margen» con invocaciones idiomáticas de `te`, en lugar de adivinar o inventarse parámetros.

El skill se mantiene en el repositorio público [TabularEditor/CLI](https://github.com/TabularEditor/CLI/tree/main/skills/te-cli) y hace un seguimiento de las funcionalidades en versión preliminar de la CLI a medida que evoluciona.

## Qué es un skill

A skill is a folder with a `SKILL.md` entry point that the agent loads on demand, based on your prompt. Su frontmatter YAML (`name`, `description`, `version`) le indica al agente **cuándo** cargarlo y **qué** cubre. The Markdown body teaches the agent **how** to do the job, and larger skills - like this one - bundle extra reference files under `references/` that the agent reads only when needed.

## Qué cubre el skill

El skill enseña al agente toda la superficie de `te`:

- every `te` command across all families - save-as, init, deploy, refresh, bpa, validate, query, script, util, and more
- patrones de autenticación: interactiva, entidad de servicio con secreto o certificado, variables de entorno, identidad administrada
- gramática de rutas de objeto: forma con barras, forma DAX y comodines
- the save model - dry run by default, `--save` to persist, and the interactive shell's `--stage`/`--revert`
- Correspondencias de migración de TE2 a CLI
- Recetas de CI/CD para GitHub Actions y Azure DevOps
- formatos de salida, códigos de salida, variables de entorno y claves de configuración
- a cheatsheet of common property names for `-p Name=Value`
- los escollos que hacen tropezar a los agentes en la práctica

Esto cubre lo mismo que el resto de esta sección documenta para humanos. Consulta @te-cli-commands para la referencia de comandos, @te-cli-auth para la autenticación y @te-cli-cicd para patrones de canalización.

## Download the skill

The skill lives in the [`skills/te-cli`](https://github.com/TabularEditor/CLI/tree/main/skills/te-cli) folder of the CLI repository - `SKILL.md` plus its `references/` subfolder.

1. Clone the [TabularEditor/CLI](https://github.com/TabularEditor/CLI) repository, or download the repository ZIP (**Code > Download ZIP**) and extract it.
2. Copy the whole `skills/te-cli/` folder somewhere convenient, keeping the `references/` subfolder next to `SKILL.md`.

You'll move this folder to a tool-specific location in the install steps below. Para ver qué cambió entre versiones antes de descargar una copia más reciente, consulta el [CHANGELOG](https://github.com/TabularEditor/CLI/blob/main/skills/te-cli/CHANGELOG.md).

## Elige un ámbito de instalación

Todos los agentes admiten dos ámbitos de instalación:

- **Ámbito de proyecto** - la habilidad está disponible solo en un proyecto o repositorio. Úsalo cuando no todos los proyectos trabajen con modelos semánticos.
- **Ámbito de usuario** - la habilidad está disponible en todos los proyectos de tu máquina. Úsalo si trabajas con modelos semánticos en muchos repositorios.

## Instalación para Claude Code

Claude Code carga las habilidades desde una carpeta con un nombre específico dentro de `.claude/skills/`. El campo `description` se compara con tus prompts, así que la habilidad solo se carga cuando corresponde; no consume tokens cuando estás trabajando en código no relacionado.

**Ámbito de proyecto** - la habilidad solo se carga dentro de este proyecto:

1. En la raíz de tu proyecto, crea la carpeta `.claude/skills/te-cli/`.
2. Copy the contents of the downloaded `te-cli` folder (`SKILL.md` and `references/`) into that folder.

The final path is `<your-project>/.claude/skills/te-cli/SKILL.md`, with `references/` alongside it.

**Ámbito de usuario** - la habilidad se carga en todos los proyectos del usuario actual:

1. Crea una carpeta `te-cli` dentro de tu directorio de habilidades de Claude a nivel de usuario:
   - **macOS / Linux:** `~/.claude/skills/te-cli/`
   - **Windows:** `%USERPROFILE%\.claude\skills\te-cli\` (normalmente `C:\Users\<you>\.claude\skills\te-cli\`)
2. Copy the contents of the downloaded `te-cli` folder (`SKILL.md` and `references/`) into that folder.

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
what does `te deploy` do without `--execute`?
```

Claude answers with the documented behavior - it's a dry run that prints the TMSL deployment script to stdout without deploying anything - which confirms the skill is loaded and in use.

## Instalación para Claude.ai y Claude Desktop

Claude.ai (web y escritorio) incluye una función integrada de **Skills**. Las Skills requieren ejecución de código, y debes subirlas como un archivo ZIP de la carpeta de la skill, en lugar del `SKILL.md` suelto.

1. Activa la ejecución de código: ve a **Configuración > Capacidades** y habilita **Ejecución de código y creación de archivos**. En los planes Team y Enterprise, un propietario lo habilita en la configuración de la organización.
2. Compress the whole downloaded `te-cli` folder (including `references/`) into `te-cli.zip`.
3. Ve a **Configuración > Capacidades > Skills** (también accesible desde **Personalizar > Skills**).
4. Haz clic en **+**, elige **Subir una skill** y selecciona `te-cli.zip`. Claude lee el `SKILL.md` incluido y muestra un resumen de la skill.
5. Activa la skill. Se carga automáticamente cuando mencionas `te` o un concepto relacionado.

Las skills personalizadas que subas serán privadas y solo estarán disponibles en tu cuenta, a menos que un propietario habilite el uso compartido en toda la organización en Team o Enterprise.

Consulta el [artículo de ayuda sobre Skills de Anthropic](https://support.claude.com/en/articles/12512180-use-skills-in-claude) para ver el flujo actual de la interfaz si la redacción ha cambiado.

## Instalación para GitHub Copilot

GitHub Copilot en VS Code es compatible de forma nativa con el estándar abierto Agent Skills: el mismo formato `SKILL.md` que usan Claude Code y Codex. Este es el enfoque recomendado porque la skill solo se carga cuando es relevante. For Copilot setups that predate Agent Skills, fall back to the generic `AGENTS.md` install below.

### Agent Skills (VS Code)

Place the skill folder contents (`SKILL.md` and `references/`) in a named folder under a skills directory. El nombre de la carpeta debe coincidir con el campo `name` del frontmatter, así que usa `te-cli` y mantén intacto el frontmatter YAML.

- **Alcance del Workspace:** `.github/skills/te-cli/SKILL.md` (Copilot también lee `.claude/skills/` y `.agents/skills/`).
- **Ámbito de usuario:** `~/.copilot/skills/te-cli/SKILL.md` (Copilot también lee `~/.claude/skills/` y `~/.agents/skills/`).

Escribe `/` en Copilot Chat para confirmar que `te-cli` aparece como comando de barra, o abre el editor de personalizaciones del agente con **Chat: Abrir personalizaciones** desde la Paleta de comandos.

## Instalar para OpenAI Codex CLI

Codex CLI carga skills de forma nativa desde una carpeta con nombre dentro de `.agents/skills/`, el mismo modelo basado en directorios que usa Claude Code. Conserva el frontmatter YAML: Codex requiere los campos `name` y `description` y usa la descripción para decidir cuándo cargar la skill.

**Ámbito de proyecto**: la skill se carga solo dentro de este proyecto:

1. En la raíz del proyecto, crea la carpeta `.agents/skills/te-cli/`.
2. Copy the contents of the downloaded `te-cli` folder (`SKILL.md` and `references/`) into that folder.

Codex busca hacia arriba desde tu directorio de trabajo, así que una skill incluida en la raíz del repositorio (`$REPO_ROOT/.agents/skills/te-cli/`) se comparte con todos los que trabajan en el repositorio.

**Ámbito personal**: la skill se carga en todos los proyectos del usuario actual:

1. Crea la carpeta `te-cli` dentro de tu directorio personal de skills de Codex: `~/.agents/skills/te-cli/`.
2. Copy the contents of the downloaded `te-cli` folder (`SKILL.md` and `references/`) into that folder.

Ejecuta `/skills` en la CLI de Codex o en el IDE para confirmar que `te-cli` aparece en la lista, y escribe `te-cli` para mencionar una skill explícitamente.

## Instalar para agentes genéricos

Para herramientas que siguen la [convención `AGENTS.md`](https://agents.md) o aceptan un archivo de instrucciones arbitrario —Aider, Continue, agentes internos personalizados—:

1. Download the skill folder.
2. In a copy of `SKILL.md`, remove the YAML frontmatter block at the top (everything between the first and second `---` lines, including those lines).
3. Rename that file to `AGENTS.md` and place it at your project root, or wherever the tool expects its instructions file.
4. Copy the `references/` folder next to your `AGENTS.md` so its relative links keep working.
5. La siguiente invocación del agente en ese proyecto detectará las instrucciones.

## Actualizar la skill

Para obtener una versión más reciente:

1. Grab the latest [`skills/te-cli`](https://github.com/TabularEditor/CLI/tree/main/skills/te-cli) folder from GitHub (re-clone, pull, or re-download the repository ZIP).
2. Replace what you previously installed:
   - **Native skills (Claude Code, Codex, Copilot Agent Skills):** replace the whole skill folder contents (`SKILL.md` and `references/`).
   - **Claude.ai / Desktop:** vuelve a comprimir en ZIP la carpeta `te-cli` y vuelve a subirla desde la interfaz de Skills.
   - **Instruction-file installs (AGENTS.md):** re-paste the body into `AGENTS.md` and refresh the copied `references/` folder.

Consulta el [CHANGELOG](https://github.com/TabularEditor/CLI/blob/main/skills/te-cli/CHANGELOG.md) para ver qué cambió entre versiones.

## Siguientes pasos

- @te-cli-install - descarga, instala y verifica la CLI en sí.
- @te-cli-auth - autentícate en Power BI, Fabric y Azure Analysis Services.
- @te-cli-commands - referencia completa de comandos.
- @te-cli-automation - salida estructurada y patrones de scripting.
- @te-cli-cicd - pipelines de GitHub Actions y Azure DevOps.
