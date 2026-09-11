---
uid: te-cli-cicd
title: Integración de CI/CD
author: Peer Grønnerup
updated: 2026-09-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# Integración de CI/CD

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

La CLI de Tabular Editor está diseñada para ejecutarse sin supervisión en pipelines de integración y entrega continuas. Un único binario, una salida estructurada, un modo no interactivo, anotaciones de CI nativas para GitHub Actions y Azure DevOps, y resultados de pruebas compatibles con VSTEST hacen que la CLI sea un reemplazo natural de las invocaciones ad hoc de TE2.

> [!WARNING]
> **No uses la CLI en pipelines de producción durante la versión preliminar pública limitada.** Hay dos riesgos específicos de esta versión preliminar que afectan a los propietarios de pipelines:
>
> - **Caducidad estricta.** El binario preliminar deja de funcionar el **2026-10-31**; cualquier pipeline que dependa de él fallará en esa fecha, independientemente de tu calendario de versiones.
> - **Sin garantía de compatibilidad con versiones anteriores.** Los comandos, las opciones, los formatos de salida y los códigos de salida pueden cambiar entre compilaciones preliminares, así que quizá tengas que actualizar los pasos del pipeline cuando actualices el binario incluido en el repositorio.
>
> Compila y evalúa en pipelines que no sean de producción, y comparte tus comentarios en el repositorio público [TabularEditor/CLI](https://github.com/TabularEditor/CLI) para que la versión GA se ajuste a tus necesidades.

## Qué hace que la CLI sea adecuada para CI

- **Un único binario autocontenido.** Sin necesidad de instalar un entorno de ejecución, sin `TabularEditor.exe`, sin `start /wait`.
- **Opción global `--non-interactive`.** Desactiva todas las indicaciones; falla de inmediato con errores claros y útiles.
- **Simulación por defecto.** `te deploy` y `te refresh` imprimen el TMSL exacto que enviarían; añade `--execute` para que el comando se ejecute de verdad. Ambos piden confirmación en la terminal, así que `--execute --force` es obligatorio en CI, donde no se puede responder a una solicitud interactiva.
- **Si falla, falla.** `te deploy` sale con un código distinto de cero cuando el servidor acepta los metadatos pero deja objetos con errores, y `te script` sale con un código distinto de cero cuando un script emite un Report de error; un control basado en el código de salida no puede dar por buena una ejecución con errores.
- **`--ci vsts` / `--ci github`.** Emite anotaciones nativas del pipeline en stderr, con el código del hallazgo (`code=` en Azure DevOps, `title=` en GitHub). `azdo` / `azure-devops` y `gh` son alias aceptados; `none` significa que no se emiten anotaciones, y un valor mal escrito se rechaza antes de que se ejecute el comando, en lugar de no emitir nada en silencio.
- **`--trx <file>`.** Genera resultados VSTEST que Azure DevOps puede consumir al publicar los resultados de pruebas.
- **Errores estructurados.** `--error-format json` emite `{"error": "...", "hint": "..."}` en stderr para que los pasos del pipeline puedan fallar con un mensaje útil.
- **Un único JSON de hallazgos.** `te validate`, `te bpa run`, `te test run` y `te query` comparten un único documento JSON legible por máquina con `--output-format json`: un `summary`, un array plano `findings[]` con `severity`/`source`/`code`/`message` y, cuando sea posible, un `objectPath` que puedes volver a pasar a `te get`. Consulta @te-cli-findings.

## Agregar la CLI a tu repositorio

Durante la versión preliminar pública limitada, el acceso a la CLI requiere iniciar sesión en [tabulareditor.com](https://tabulareditor.com/download-tabular-editor-cli), por lo que los pipelines no pueden descargar el archivo desde una URL pública. La forma reproducible más sencilla es incluir en tu repositorio el binario que corresponda a tu runner y hacer referencia a él desde cada paso del pipeline.

Una estructura habitual:

```
your-repo/
└── tools/
    └── te/
        ├── te         # Linux / macOS binary (needs chmod +x at runtime)
        └── te.exe     # Windows binary
```

Coloca el binario **extraído** —no el archivo comprimido— para que el pipeline pueda invocarlo directamente. Elige la compilación que coincida con el SO y la arquitectura de tu runner; consulta @te-cli-install para ver la tabla de nombres de archivo. El binario autocontenido ocupa ~70 MB; considera usar Git LFS si tu repositorio es sensible al tamaño.

> [!NOTE]
> Al hacer commit del binario, también dejas fijada la versión de la CLI que hayas incluido en el repositorio, lo cual es deseable para la reproducibilidad de la CI. Para actualizar, sustituye el binario en `tools/te/` y haz commit: los mensajes del commit serán tu registro de versiones. Ten en cuenta que el binario preliminar caduca el **2026-10-31** independientemente de cuándo lo hayas incorporado al repositorio, así que una copia incluida en el repositorio no es una dependencia permanente; planifica actualizarla (y volver a validar tu pipeline con la nueva superficie de la API) siguiendo la cadencia de las compilaciones preliminares.

## GitHub Actions

Un flujo de trabajo completo de despliegue y pruebas. El ejemplo asume que el binario `te` de Linux está incluido en `tools/te/te` y que las credenciales de una entidad de servicio se guardan en los secretos del repositorio (`AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`).

```yaml
name: Deploy semantic model

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
      AZURE_CLIENT_SECRET: ${{ secrets.AZURE_CLIENT_SECRET }}
      AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Tabular Editor CLI
        run: |
          chmod +x ./tools/te/te
          echo "$GITHUB_WORKSPACE/tools/te" >> $GITHUB_PATH

      - name: Validate
        run: te validate --model ./model --ci github --trx validate.trx

      - name: Best Practice Analyzer (gate)
        run: te bpa run --model ./model --fail-on error --ci github --trx bpa.trx

      - name: Deploy
        run: |
          te deploy --model ./model \
            --target-server "${{ vars.WORKSPACE }}" \
            --target-database "${{ vars.MODEL }}" \
            --auth env \
            --non-interactive \
            --execute \
            --force \
            --ci github

      - name: Regression tests
        run: |
          te test run \
            -s "${{ vars.WORKSPACE }}" \
            -d "${{ vars.MODEL }}" \
            --auth env --non-interactive \
            --ci github --trx tests.trx

      - name: Publish test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: trx-results
          path: '*.trx'
```

## Azure DevOps Pipelines

El equivalente en Azure DevOps Pipelines del flujo de trabajo de GitHub Actions anterior. El ejemplo asume que `te.exe` está incluido en `tools\te\te.exe`. `--ci vsts` emite comandos `##vso[...]` que el pipeline interpreta como errores, advertencias y actualizaciones del estado de la tarea.

```yaml
trigger:
  - main

pool:
  vmImage: 'windows-latest'

variables:
  - group: 'te-cli-secrets'   # Contains AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID

steps:
  - checkout: self

  - powershell: Write-Host "##vso[task.prependpath]$(Build.SourcesDirectory)\tools\te"
    displayName: 'Set up Tabular Editor CLI'

  - script: te validate --model ./model --ci vsts --trx validate.trx
    displayName: 'Validate'

  - script: te bpa run --model ./model --fail-on error --ci vsts --trx bpa.trx
    displayName: 'BPA gate'

  - script: |
      te deploy --model ./model ^
        --target-server "$(WORKSPACE)" --target-database "$(MODEL)" ^
        --auth env --non-interactive --execute --force --ci vsts
    displayName: 'Deploy'
    env:
      AZURE_CLIENT_ID: $(AZURE_CLIENT_ID)
      AZURE_CLIENT_SECRET: $(AZURE_CLIENT_SECRET)
      AZURE_TENANT_ID: $(AZURE_TENANT_ID)

  - script: te test run -s "$(WORKSPACE)" -d "$(MODEL)" --auth env --non-interactive --ci vsts --trx tests.trx
    displayName: 'Regression tests'
    env:
      AZURE_CLIENT_ID: $(AZURE_CLIENT_ID)
      AZURE_CLIENT_SECRET: $(AZURE_CLIENT_SECRET)
      AZURE_TENANT_ID: $(AZURE_TENANT_ID)

  - task: PublishTestResults@2
    condition: always()
    inputs:
      testResultsFormat: 'VSTest'
      testResultsFiles: '*.trx'
```

## Patrones de compuerta del BPA

`te deploy` y `te save-as` ejecutan el Best Practice Analyzer como comprobación previa por defecto. Hay tres comportamientos que conviene definir de antemano:

- **Aplicar**: el valor predeterminado. El pipeline falla si BPA detecta infracciones con severidad >= error. Combínalo con `--fail-on warning` en un paso independiente de `te bpa run` si quieres que las advertencias también hagan fallar el pipeline.
- **Corrección automática**: `--fix-bpa` aplica las `fixExpression`s en memoria al artefacto desplegado. Los archivos de origen no se modifican. Es útil cuando la fuente de verdad está en el modelo y quieres que los despliegues normalicen el estilo sin intervención del desarrollador.
- **Omitir**: `--skip-bpa` desactiva el control para un solo comando. Útil para correcciones urgentes de emergencia; no se recomienda como valor predeterminado.

```bash
# Treat warnings as failures in PR validation
te bpa run --model ./model --fail-on warning --ci github --trx bpa.trx

# Auto-fix during deploy (source unchanged)
te deploy --model ./model --target-server my-ws --target-database my-model --fix-bpa --execute --force --ci github

# Emergency bypass
te deploy --model ./model --target-server my-ws --target-database my-model --skip-bpa --execute --force --ci github
```

Consulta @te-cli-config para controlar globalmente el control del BPA mediante las claves de configuración `bpa.onDeploy` / `bpa.onSave`.

## Validación de scripts

Los C# Script pueden comprobarse en compilación sin cargar ningún modelo: un paso de lint sin conexión para validar PR:

```bash
# Compile-check C# scripts without a model (offline lint)
te script --file ./scripts/fix.csx --validate
```

## Patrones de actualización

La actualización en los pipelines suele ser un paso posterior al despliegue. Añade `--execute --force` (sin `--execute`, el comando solo imprime el TMSL que ejecutaría; sin `--force`, se detiene para pedir una confirmación que nadie puede dar), usa `--non-interactive` y elige un `--type` determinista:

```bash
# Full refresh of the whole model after deploy
te refresh -s my-ws -d my-model --type full --execute --force --non-interactive

# Refresh a single fact table (e.g., daily incremental pipeline)
te refresh -s my-ws -d my-model --table Sales --type full --execute --force --non-interactive

# Recalculate only (useful after calculation-group changes)
te refresh -s my-ws -d my-model --type calculate --execute --force --non-interactive
```

En los flujos de trabajo de actualización incremental, usa `--apply-refresh-policy` (pasa `true`, `false` o el nombre de una tabla para limitar la actualización a esa tabla) junto con `--effective-date <yyyy-MM-dd>` y `--execute --force`. Consulta @te-cli-commands para más detalles.

## Patrones de artefactos

Genera TMSL o XMLA como artefacto sin desplegarlo, para que los DBA o un trabajo posterior puedan revisarlo o aplicarlo:

```bash
# Produce the TMSL script that a deploy would send - do not deploy (dry run is the default)
te deploy --model ./model --target-server my-ws --target-database my-model > deploy.tmsl

# Produce the TMSL refresh command - do not execute (dry run is the default)
te refresh -s my-ws -d my-model --type full > refresh.tmsl
```

Confirma estos artefactos en git, súbelos al almacenamiento de artefactos del pipeline o pásalos entre trabajos. Son texto sin formato y se pueden comparar fácilmente en las pull requests.

## Gestión de secretos

| Enfoque                                                                                                                                              | Cuándo usarlo                                                       | Notas                                                                                                                                                                                                                                                                                                     |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Principal de servicio mediante variables de entorno (`AZURE_CLIENT_ID` / `AZURE_CLIENT_SECRET` / `AZURE_TENANT_ID`, `--auth env`) | CI/CD general                                                       | Asigna los secretos del pipeline a variables de entorno a nivel de paso o de trabajo. Nunca pases secretos en los argumentos de comandos.                                                                                                                                 |
| Entidad de servicio mediante `te auth login`, una vez por trabajo (`echo $SECRET \| te auth login -u $ID -p - -t $TENANT`)        | Trabajos de varios pasos                                            | El inicio de sesión se almacena en caché, así que los comandos `te` posteriores obtienen tokens de forma silenciosa; no hace falta establecer `AZURE_CLIENT_*` en cada paso ni volver a pasar `-u/-p/-t`. Canaliza el secreto a través de stdin en lugar de interpolarlo. |
| Identidad administrada (`--auth managed-identity`)                                                                                | Máquinas virtuales de Azure, Azure Container Apps y Azure Functions | No hay secretos que gestionar. Se prefiere en entornos alojados en Azure.                                                                                                                                                                                                 |
| Certificado (`--certificate <path>`)                                                                                              | Escenarios empresariales con rotación de certificados               | Monta el certificado como un paso de archivo seguro; pasa `--certificate-password` mediante variables de entorno.                                                                                                                                                                         |

> [!WARNING]
> No hagas echo de secretos ni de la salida de `te auth status` en los registros del pipeline. La CLI escribe advertencias en stderr cuando se pasan secretos en la línea de comandos; haz caso a esas advertencias en CI.

## Páginas relacionadas

- @te-cli-auth - métodos de autenticación en detalle.
- @te-cli-config - configuración y reemplazos del perfil.
- @te-cli-automation - patrones generales de scripting.
- @te-cli-migrate - migración de un pipeline existente basado en TE2.
