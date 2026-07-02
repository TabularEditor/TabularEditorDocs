---
uid: te-cli-install
title: Instalación y configuración
author: Peer Grønnerup
updated: 2026-06-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# Instalación y configuración

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

Tabular Editor CLI se distribuye como un único ejecutable autónomo llamado `te` (`te.exe` en Windows). No tiene dependencias externas de tiempo de ejecución.

## Descargar

1. Inicia sesión en [tabulareditor.com](https://tabulareditor.com/download-tabular-editor-cli) con tu cuenta de Tabular Editor.
2. Descarga el archivo para tu plataforma y arquitectura:

   | Plataforma | 64 bits (Intel/AMD)         | ARM64                                                    | Archivo   |
   | ---------- | ---------------------------------------------- | -------------------------------------------------------- | --------- |
   | Windows    | `te-win-x64.zip`                               | `te-win-arm64.zip`                                       | `.zip`    |
   | macOS      | `te-osx-x64.tar.gz` (Intel) | `te-osx-arm64.tar.gz` (Apple Silicon) | `.tar.gz` |
   | Linux      | `te-linux-x64.tar.gz`                          | `te-linux-arm64.tar.gz`                                  | `.tar.gz` |

   Elige la compilación ARM64 en Mac con Apple Silicon (M1 o posterior), en dispositivos Windows on ARM y en servidores Linux basados en ARM (incluidos AWS Graviton, Azure Ampere y Raspberry Pi de 64 bits). Elige la compilación `x64` en el resto de casos.

## Instalar

Descomprime el archivo en una carpeta de tu elección y añade esa carpeta a `PATH` para poder ejecutar `te` desde cualquier directorio de trabajo.

### Windows (PowerShell)

#### x64

```powershell
Expand-Archive te-win-x64.zip -DestinationPath "$env:LOCALAPPDATA\Programs\te"
[Environment]::SetEnvironmentVariable(
  "PATH",
  [Environment]::GetEnvironmentVariable("PATH", "User") + ";$env:LOCALAPPDATA\Programs\te",
  "User")
```

#### ARM64

```powershell
Expand-Archive te-win-arm64.zip -DestinationPath "$env:LOCALAPPDATA\Programs\te"
[Environment]::SetEnvironmentVariable(
  "PATH",
  [Environment]::GetEnvironmentVariable("PATH", "User") + ";$env:LOCALAPPDATA\Programs\te",
  "User")
```

### macOS

#### Apple Silicon (ARM64)

```bash
mkdir -p ~/.local/bin
tar -xzf te-osx-arm64.tar.gz -C ~/.local/bin
chmod +x ~/.local/bin/te
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc   # or ~/.bashrc
```

#### Intel (x64)

```bash
mkdir -p ~/.local/bin
tar -xzf te-osx-x64.tar.gz -C ~/.local/bin
chmod +x ~/.local/bin/te
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc   # or ~/.bashrc
```

En macOS, el binario está firmado con nuestro Apple Developer ID y notarizado por Apple, por lo que la primera ejecución se completa sin la advertencia de Gatekeeper "no se puede verificar el desarrollador". Se recomienda tener acceso a internet en la primera ejecución para que Gatekeeper pueda obtener el ticket de notarización; si la primera ejecución se hace sin conexión, puede aparecer brevemente un aviso antes de que se desbloquee cuando vuelva la conexión.

### Linux

#### x64

```bash
mkdir -p ~/.local/bin
tar -xzf te-linux-x64.tar.gz -C ~/.local/bin
chmod +x ~/.local/bin/te
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc   # or ~/.zshrc
```

#### ARM64

```bash
mkdir -p ~/.local/bin
tar -xzf te-linux-arm64.tar.gz -C ~/.local/bin
chmod +x ~/.local/bin/te
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc   # or ~/.zshrc
```

> [!NOTE]
> El cambio en PATH surte efecto en las **nuevas** sesiones de la shell. Para ejecutar `te` en la shell en la que realizaste la instalación, abre una nueva terminal o recarga tu perfil: `source ~/.bashrc` / `source ~/.zshrc` en macOS/Linux, o cierra y vuelve a abrir PowerShell en Windows.

## Verificar

Comprueba la versión instalada y consulta la lista de comandos disponibles:

```bash
te --version
te --help
```

`te --help` muestra un índice de ayuda en color que agrupa los comandos por familia. Todos los subcomandos aceptan `--help` para ver el uso detallado:

```bash
te deploy --help
te bpa run --help
```

## Ocultar el banner de vista previa

De forma predeterminada, la CLI muestra un banner amarillo de versión preliminar en stderr. Para ocultarlo, ejecuta:

```bash
te config set hidePreviewNotice true
```

> [!WARNING]
> El banner vuelve a aparecer en cada comando durante los **14 días previos a la fecha de finalización de la versión preliminar** (2026-09-30), independientemente de `hidePreviewNotice`. Esto garantiza que tengas una advertencia visible antes de que la CLI deje de funcionar.

## Autocompletado del shell

La CLI proporciona scripts de autocompletado para **Bash**, **Zsh**, **PowerShell** y **Fish**. Pick the block that matches your shell - each one installs the completion persistently for new shell sessions.

### Bash (macOS/Linux)

```bash
mkdir -p ~/.local/share/bash-completion/completions
te completion bash > ~/.local/share/bash-completion/completions/te
```

### Zsh (macOS/Linux)

```zsh
mkdir -p ~/.zfunc
te completion zsh > ~/.zfunc/_te
echo 'fpath=(~/.zfunc $fpath); autoload -U compinit; compinit' >> ~/.zshrc
```

### PowerShell (Windows/macOS/Linux)

```powershell
Add-Content $PROFILE 'te completion pwsh | Out-String | Invoke-Expression'
```

### Fish (macOS/Linux)

```bash
te completion fish > ~/.config/fish/completions/te.fish
```

Abre una nueva sesión del shell para que el autocompletado surta efecto.

El autocompletado abarca subcomandos, opciones globales y rutas de modelos (cuando el autocompletado con tabulador en el sistema de archivos tiene sentido).

## Matriz de características multiplataforma

La mayoría de las funcionalidades son idénticas en todas las plataformas. Unas pocas dependen de transportes exclusivos de Windows:

| Funcionalidad                                                                                                                           | Windows | macOS / Linux |
| --------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------- |
| Cargar/guardar BIM y TMDL                                                                                                               | Sí      | Sí            |
| Desplegar en Power BI / Fabric / Azure Analysis Services                                                                                | Sí      | Sí            |
| Best Practice Analyzer y Analizador VertiPaq                                                                                            | Sí      | Sí            |
| C# Script                                                                                                                               | Sí      | Sí            |
| Consultas DAX en modelos en la nube                                                                                                     | Sí      | Sí            |
| Autenticación: navegador, código de dispositivo, entidad de servicio, env, variables de entorno, identidad administrada | Sí      | Sí            |
| Conectarse a una instancia local de SSAS (transporte TCP)                                                            | Sí      | **No**        |
| Conectarse a Power BI Desktop (transporte por canalización con nombre)                                               | Sí      | **No**        |

> [!IMPORTANT]
> Las conexiones locales a SSAS y Power BI Desktop dependen de protocolos de transporte solo disponibles en Windows. Todos los flujos de trabajo basados en la nube (Power BI Service, Fabric y Azure Analysis Services) funcionan en cualquier plataforma.

## Actualización

Para actualizar a una compilación de vista previa más reciente, descarga el archivo más reciente y sobrescribe la instalación anterior. La configuración y las credenciales almacenadas en caché se guardan fuera de la carpeta de instalación (consulta <xref:te-cli-config> y <xref:te-cli-auth>) y se conservan al actualizar.

## Desinstalación

1. Elimina la carpeta de instalación.
2. Elimina la entrada de PATH.
3. (Opcional) Borra las credenciales en caché y la configuración:
   - Ejecuta primero `te auth logout`: elimina todos los tokens en caché y los registros de SPN del backend activo (almacén de claves del SO o alternativa basada en archivo).
   - Borra `~/.config/te/` (configuración y perfiles guardados).
   - Borra `~/.te-cli/` (archivos residuales de caché; solo está presente cuando se usó la alternativa basada en archivos o como residuo de compilaciones anteriores de la CLI).
   - Para purgar también las entradas del almacén de claves nativo del SO —normalmente innecesario, ya que `te auth logout` ya las elimina—, consulta:
     - **Windows:** Administrador de credenciales → Credenciales de Windows → entradas llamadas `com.tabulareditor.cli...` o `te-cli`.
     - **Linux:** `secret-tool search Component te-cli` y `secret-tool clear ...`, o usa Seahorse.
     - **macOS:** Acceso a Llaveros → busca `com.tabulareditor.cli`.

## Siguientes pasos

- @te-cli-auth - autenticación en Power BI, Fabric o Azure Analysis Services.
- @te-cli-commands - referencia completa de comandos.
- @te-cli-interactive - modo REPL guiado.
