---
uid: policies
title: Directivas
author: Daniel Otykier
updated: 2026-09-22
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "Tabular Editor 2 solo lee la clave heredada del Registro y solo tiene en cuenta las directivas marcadas como TE2 más abajo."
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          partial: true
          note: "Solo directivas generales"
        - edition: Business
          partial: true
          note: "Solo directivas generales"
        - edition: Enterprise
          full: true
    - product: CLI de Tabular Editor
      partial: true
      note: "En Windows, y solo para las directivas marcadas como CLI más abajo."
---

# Directivas

Si administras Tabular Editor para una organización, puedes limitar sus funciones y configurar el Asistente de IA y el servidor MCP para tus usuarios mediante directivas de grupo. Define manualmente los valores en el Registro de Windows o usa las plantillas administrativas incluidas con Tabular Editor 3.

La mayoría de las directivas son directivas generales, disponibles en todas las ediciones de Tabular Editor 3. Las directivas que configuran el Asistente de IA y el servidor MCP requieren la [Edición Enterprise de Tabular Editor 3](xref:editions) y están marcadas como **Enterprise** más abajo.

> [!NOTE]
> Esta funcionalidad requiere las siguientes versiones de Tabular Editor:
>
> - Tabular Editor [2.17.0](https://github.com/TabularEditor/TabularEditor/releases/tag/2.17.0) o posterior
> - Tabular Editor [3.3.5](https://github.com/TabularEditor/TabularEditor3/releases/tag/3.3.5) o posterior, para las directivas generales
> - Tabular Editor 3.27 o posterior, para las siguientes claves del Registro, para directivas aplicables a todo el equipo y para todas las directivas Enterprise
> - CLI de Tabular Editor 0.7 o posterior

## Claves del Registro

Las directivas se leen de seis claves, y la primera clave que define un valor es la que determina ese valor. Toda clave en `HKEY_LOCAL_MACHINE` tiene prioridad sobre cualquier clave en `HKEY_CURRENT_USER`, de modo que una directiva para todo el equipo establecida mediante Configuración del equipo no puede ser anulada por el usuario. Dentro de una misma rama del Registro, una clave específica del producto tiene prioridad sobre la clave compartida, que a su vez tiene prioridad sobre la clave heredada:

```
HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3
HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS
HKEY_LOCAL_MACHINE\Software\Policies\Kapacity\Tabular Editor
HKEY_CURRENT_USER\Software\Policies\Tabular Editor ApS\TE3
HKEY_CURRENT_USER\Software\Policies\Tabular Editor ApS
HKEY_CURRENT_USER\Software\Policies\Kapacity\Tabular Editor
```

- `Tabular Editor ApS\TE3` solo la lee Tabular Editor 3. La CLI de Tabular Editor lee `Tabular Editor ApS\TECLI` en su lugar; las otras cuatro claves son las mismas para ambos.
- `Tabular Editor ApS` es la clave compartida; la leen tanto Tabular Editor 3 como la CLI.
- `Kapacity\Tabular Editor` es la clave que usan las versiones anteriores. Se sigue leyendo, y es la única clave que lee Tabular Editor 2, así que establece ahí la directiva si debe aplicarse también a Tabular Editor 2.

La precedencia se aplica a cada valor por separado: un `DisableTelemetry` para todo el equipo con valor 0 anula un `DisableTelemetry` a nivel de usuario con valor 1, mientras que un `DisableCSharpScripts` establecido solo a nivel de usuario sigue aplicándose.
Los nombres de los valores no distinguen mayúsculas de minúsculas.

## Tipos de valores

| Tipo de configuración                 | Tipo de registro | Notas                                                                                                                                                                                                          |
| ------------------------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Directiva de activación/desactivación | `REG_DWORD`      | Cualquier valor distinto de cero impone la directiva. `0` y la ausencia del valor significan, en ambos casos, que no se aplica.                                                |
| Opción                                | `REG_SZ`         | El nombre de la opción, por ejemplo `Read`. También se acepta un `REG_DWORD` que contenga la posición de la opción en la lista; es lo que escribe la plantilla administrativa. |
| Lista                                 | `REG_MULTI_SZ`   | Una entrada por línea. También se acepta un `REG_SZ` cuyas entradas estén separadas por puntos y coma.                                                                         |
| Ruta, dirección o nombre              | `REG_SZ`         |                                                                                                                                                                                                                |

Tabular Editor lee los valores de directiva una sola vez, al iniciarse. El cambio surtirá efecto la próxima vez que inicies la aplicación.

## Directivas generales

Para aplicar una de ellas, agrega un valor `REG_DWORD` con el nombre que aparece a continuación y asígnale un valor distinto de cero. La columna **Productos** muestra qué productos respetan la directiva: **TE3** es Tabular Editor 3, **CLI** es la CLI de Tabular Editor y **TE2** es Tabular Editor 2, que solo lee la clave heredada.

| Valor                          | Productos     | Cuando se aplica...                                                                                                                                                                                                                                                                                |
| ------------------------------ | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DisableUpdates                 | TE3, TE2      | Tabular Editor no comprobará si hay versiones más recientes disponibles en línea. Los usuarios tampoco pueden buscar actualizaciones manualmente.                                                                                                                                                                  |
| DisableCSharpScripts           | TE3, TE2      | Tabular Editor no permitirá a los usuarios crear ni ejecutar C# Scripts.                                                                                                                                                                                                                                                           |
| DisableMacros                  | TE3, TE2      | Tabular Editor no permitirá a los usuarios guardar ni ejecutar macros. Las macros almacenadas en la carpeta `%LocalAppData%` no se cargan al iniciar la aplicación.                                                                                                                                                |
| DisableBpaDownload             | TE3, CLI, TE2 | Las reglas de Best Practice Analyzer no se pueden descargar desde la web. Las reglas almacenadas localmente o junto con el modelo siguen funcionando.                                                                                                                                                              |
| DisableWebDaxFormatter         | TE3, CLI, TE2 | El formateador de DAX que envía el código a daxformatter.com está deshabilitado. Tabular Editor 3 sigue ofreciendo su formateador integrado, que no envía nada a través de la red.                                                                                                                 |
| DisableErrorReports            | TE3           | Los usuarios no pueden enviar Reports de errores o cierres inesperados al equipo de soporte de Tabular Editor.                                                                                                                                                                                                                     |
| DisableTelemetry               | TE3, CLI      | No se recopilan ni se envían datos de uso anónimos al equipo de soporte de Tabular Editor.                                                                                                                                                                                                                                         |
| DisableDaxOptimizer            | TE3           | La integración con el Optimizador de DAX no está disponible.                                                                                                                                                                                                                                                                       |
| DisableDaxOptimizerUpload      | TE3           | Los usuarios no pueden cargar archivos del Analizador VertiPaq mediante la integración con el Optimizador de DAX. Se aplica implícitamente cuando se aplica `DisableDaxOptimizer`.                                                                                                                                 |
| RequireDaxOptimizerObfuscation | TE3           | Los usuarios no pueden cargar archivos del Analizador VertiPaq en texto sin formato mediante la integración con el Optimizador de DAX; solo se pueden cargar archivos ofuscados. Se aplica implícitamente cuando se aplica `DisableDaxOptimizer` o `DisableDaxOptimizerUpload`.                                    |
| DisableDaxPackageManager       | TE3           | El administrador de paquetes de DAX no está disponible.                                                                                                                                                                                                                                                                            |
| DisableAi                      | TE3           | Toda la funcionalidad de IA está desactivada: el Asistente de IA, el servidor MCP y cualquier función basada en IA no están disponibles. No se carga nada relacionado con la IA al iniciar la aplicación y se borra cualquier configuración del proveedor almacenada, incluida la clave de la API. |
| DisableAiChat                  | TE3           | El panel de chat del Asistente de IA no está disponible. El resto de la funcionalidad de IA, incluido el servidor MCP, no se ve afectada.                                                                                                                                                                          |
| DisableMcpServer               | TE3           | El servidor MCP no está disponible, así que las herramientas de agentes externos no pueden conectarse a Tabular Editor 3. El chat del Asistente de IA no se ve afectado.                                                                                                                                           |
| RequireMcpAccessToken          | TE3           | Los clientes que se conecten al servidor MCP deben presentar el token de acceso que se muestra en el cuadro de diálogo **Herramientas > Servidor MCP...**, y los usuarios no pueden desactivar ese requisito.                                                                      |

### En la CLI de TE

La CLI de Tabular Editor respeta las directivas marcadas con **CLI** más arriba en Windows y lee las mismas claves en el mismo orden que Tabular Editor 3. También respeta `BlockUnsafeScripts` de las [directivas Enterprise](#scripts-and-macros) siguientes, para `te script`, `te macro run` y `te bpa run --fix`.

Una operación rechazada no pasa desapercibida. `te` indica la directiva que la rechazó y finaliza con un código distinto de cero, por lo que el paso de la canalización falla en lugar de aparentar que tuvo éxito sin haber hecho nada.

La CLI no tiene ediciones, así que una directiva que requiere la Edición Enterprise de Tabular Editor 3 en la aplicación de escritorio se aplica igualmente en la CLI, sea cual sea la licencia que tenga el equipo.

## Directivas Enterprise

Estas directivas determinan lo que puede hacer un C# Script y configuran el Asistente de IA y el servidor MCP. Todas requieren la Edición Enterprise de Tabular Editor 3 y deben colocarse en `Tabular Editor ApS\TE3`, excepto `BlockUnsafeScripts`, que también respeta la CLI de Tabular Editor y que, por tanto, debe ubicarse en la clave compartida `Tabular Editor ApS`. Colócalo en `TE3` o `TECLI` para que solo afecte a uno de los dos.

### Scripts y macros

| Valor              | Tipo                 | Qué hace                                                                                                                                                                                                                                                                                                           |
| ------------------ | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| BlockUnsafeScripts | Activado/desactivado | Los C# Script y las macros solo se permiten si se mantienen dentro del modelo semántico. Un script que lea o escriba un archivo, acceda a la red, inicie otro programa, cargue código externo o envíe un comando directamente al servidor se rechaza antes de que se ejecute nada. |

La restricción se aplica allí donde se ejecute un script: **Ejecutar script** y **Ejecutar con vista previa** en un documento de script, **Aplicar corrección** en el Best Practice Analyzer, el Asistente de IA, el servidor MCP, y `te script`, `te macro run` y `te bpa run --fix` en la línea de comandos. Un script rechazado no es un script fallido. Nada llega al modelo, la lista de errores permanece vacía y un cuadro de diálogo **Script no ejecutado** indica la directiva y lo que utilizó el script.

Una macro que accede a recursos fuera del modelo se omite de todos los menús, para que no pueda ejecutarse por accidente. Sigue apareciendo la macro en **Ver > Macros** con la columna **Bloqueada** rellenada, y aún puede abrirse y editarse, para que pueda volver a ajustarse a la directiva en lugar de reescribirse desde cero. Guardar una macro de este tipo funciona e indica que se ha guardado, pero que no se ejecutará.

Lo que cuenta como permanecer dentro del modelo se decide analizando el script compilado en lugar de buscar en su texto, por lo que también se rechazan las rutas indirectas a los mismos destinos: reflexión, árboles de expresiones, `Activator`, `AppDomain`, lectores XML o deserialización. Entre los [métodos auxiliares](xref:script-helper-methods) integrados, los tres que escriben fuera del modelo, `SaveFile`, `ExecuteCommand` y `Bpa.ExportCsv`, se consideran inseguros; los que solo leen, incluidos `ReadFile`, `ExecuteDax`, `EvaluateDax`, `ExecuteReader` y `ExportProperties`, no. Consulta [Directivas del administrador](xref:csharp-scripts#administrator-policies) para ver la misma regla desde la perspectiva del autor del script.

En el Editor de directivas de grupo, esta se llama **Permitir solo scripts y macros que permanezcan dentro del modelo** y, como se escribe en la clave compartida, aparece directamente en **Plantillas administrativas > Tabular Editor** en lugar de en la subcarpeta **Tabular Editor 3**.

### Límites de permisos

Cada uno de estos establece un límite máximo de acceso para el Asistente de IA y el servidor MCP a un tipo de recurso. Los valores aceptados son `Deny`, `Read` y `Write`, salvo para los datos del modelo, donde `Read` es el ajuste más alto con sentido.

Un límite fija el máximo que un usuario puede conceder: un permiso existente por encima del límite se reduce hasta él, la opción correspondiente en **Herramientas > Preferencias > Funciones de IA > Permisos** y en el cuadro de diálogo **Herramientas > Servidor MCP...** se muestra en modo de solo lectura, y el Asistente de IA deja de pedir permisos que no se le pueden conceder. Ninguna concesión de permisos prevalece sobre un límite: ni un permiso permanente, ni uno concedido para un solo modelo, ni uno concedido en una versión anterior. La elección del usuario se deja intacta en sus preferencias, por lo que vuelve a aplicarse si se quita la directiva.

| Valor                     | Valores aceptados       | Limita el acceso a...                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MaxModelMetadataAccess    | Deny, Read, Write       | Los metadatos del modelo abierto: nombres de tablas, columnas y medidas, expresiones, descripciones, resultados de Best Practice Analyzer y estadísticas de VertiPaq. `Write` también permite al asistente ejecutar sus propios C# Scripts en el modelo. Con `Deny`, no se envía absolutamente nada sobre el modelo abierto: ni un resumen del modelo, ni un aviso de que el modelo ha cambiado, ni la selección actual. |
| MaxModelDataAccess        | Deny, Read              | Los valores de datos del modelo, es decir, los resultados de las consultas DAX.                                                                                                                                                                                                                                                                                                                                                                                                          |
| MaxBpaAccess              | Deny, Read, Write       | Reglas del Best Practice Analyzer. `Read` permite enumerar las reglas y ejecutar el análisis; `Write` también permite agregar y modificar reglas.                                                                                                                                                                                                                                                                                                                        |
| MaxDocumentsAccess        | Deny, Read, Write       | Los documentos que el usuario tiene abiertos, como C# Scripts y consultas DAX. `Read` permite leer su contenido; `Write` además permite modificarlos.                                                                                                                                                                                                                                                                                                                    |
| MaxMacrosAccess           | Deny, Read, Write       | La biblioteca de macros del usuario.                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| McpMaxModelMetadataAccess | Deny, Read, Write       | Los mismos cinco recursos, exclusivamente para el servidor MCP.                                                                                                                                                                                                                                                                                                                                                                                                                          |
| McpMaxModelDataAccess     | Deny, Read              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| McpMaxBpaAccess           | Deny, Read, Write       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| McpMaxDocumentsAccess     | Denegar, Leer, Escribir |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| McpMaxAccesoAMacros       | Denegar, Leer, Escribir |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

Los cinco valores `McpMax...` se aplican únicamente al servidor MCP. Cuando no se establece uno de ellos, el servidor MCP hereda el límite `Max...` correspondiente. Solo pueden reducir ese límite, nunca aumentarlo, por lo que un agente desatendido nunca puede tener más permisos que el asistente interactivo.

### Proveedor de IA

| Valor                  | Tipo      | Valores aceptados                                       | Qué hace                                                                                                                                                                                                                                                                                               |
| ---------------------- | --------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| AiProvider             | Selección | None, OpenAI, Anthropic, AzureOpenAI, Custom            | Restringe el Asistente de IA a un único proveedor. `None` desactiva el Asistente de IA; el servidor MCP no se ve afectado.                                                                                                                                             |
| AiEndpoint             | Dirección |                                                         | Fija el endpoint o la URL base a la que se envían las solicitudes, por ejemplo, un Gateway interno o un recurso de Azure OpenAI.                                                                                                                                                       |
| AiModel                | Nombre    |                                                         | Fija el modelo o el nombre de implementación de Azure OpenAI. El selector de modelos del panel de chat se sustituye por un indicador simple, por lo que los usuarios no pueden cambiar de modelo.                                                                      |
| AiOrganizationId       | Nombre    |                                                         | Fija la organización de OpenAI a la que se facturan las solicitudes.                                                                                                                                                                                                                   |
| AiProjectId            | Nombre    |                                                         | Fija el proyecto de OpenAI al que se facturan las solicitudes.                                                                                                                                                                                                                         |
| AiAllowedProviders     | Lista     | Cualquiera de los nombres de los proveedores anteriores | Restringe qué proveedores pueden configurar los usuarios. Un proveedor establecido por `AiProvider` se permite tanto si figura en la lista como si no, y `None` siempre se ofrece; una lista de permitidos no sirve para evitar que un usuario desactive el asistente. |
| AiAllowedEndpointHosts | Lista     | Nombres de host                                         | Restringe a qué hosts puede apuntar un endpoint; por ejemplo, `Gateway.contoso.com` o `*.contoso.com`.                                                                                                                                                                                 |

La configuración bloqueada aparece como de solo lectura en **Herramientas > Preferencias > Funciones de IA > Asistente de IA**, y el Asistente de IA usa la configuración bloqueada independientemente de lo que el usuario hubiera elegido antes. No se escribe nada en las preferencias del propio usuario, por lo que su proveedor, endpoint, modelo y clave API vuelven a aparecer si se quita la directiva. Las claves API nunca se distribuyen mediante directiva.

Los nombres de host solo se comparan con la parte de host de la URL del endpoint. La comparación no distingue entre mayúsculas y minúsculas y omite el puerto. Un `*.` inicial cubre los subdominios de un dominio, pero no el dominio en sí; por tanto, incluye ambos en la lista si necesitas los dos. La lista se aplica a todos los proveedores siempre que se establezca un endpoint, así que no se puede usar una sobrescritura de la URL base para eludirla.

Se rechaza cualquier configuración que la directiva no permita, y el Asistente de IA indica qué regla la rechazó en lugar de enviar la solicitud: un proveedor que no esté en la lista de permitidos, un host del endpoint que no esté en la lista de hosts permitidos, un endpoint que no sea una URL válida cuando se aplique una lista de hosts permitidos, o un proveedor de Azure OpenAI o Custom bloqueado sin ningún endpoint.

### Instrucciones personalizadas

| Valor                         | Tipo                 | Qué hace                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ----------------------------- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AiCustomInstructionsPath      | Ruta                 | Especifica una carpeta de Instrucciones personalizadas que el Asistente de IA carga para todos los usuarios, además de las que se incluyen con el producto. Se admite una ruta UNC a un recurso compartido de red de solo lectura. Si una instrucción de la organización y una instrucción del propio usuario comparten el mismo identificador, prevalece la de la organización. |
| DisableUserCustomInstructions | Activado/desactivado | El Asistente de IA ignora las Instrucciones personalizadas que el usuario haya colocado en su propia carpeta, y el botón que abre esa carpeta está desactivado. Las instrucciones incluidas con el producto, así como cualquier carpeta de la organización, siguen cargándose.                                                                                                                   |

### Servidor MCP

| Valor            | Tipo                                    | Qué hace                                                                                                                                                                                                                                                                                                                 |
| ---------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| McpDisabledTools | Lista                                   | Nombres de herramientas MCP que nunca se ofrecen a un cliente conectado. Las herramientas listadas no aparecen en la lista de herramientas del cliente y no se ejecutan, incluso si el cliente solicita alguna por su nombre. El chat de AI Assistant no se ve afectado. |
| McpPort          | Número: de 1024 a 49151 | Fija el puerto en el que escucha el servidor MCP, de modo que se pueda compartir una única configuración de cliente en toda la organización. El valor predeterminado es 42100. El servidor solo escucha en la dirección de loopback.                                     |

### Registro de auditoría

Tabular Editor 3 mantiene un registro local de la actividad de AI Assistant y del servidor MCP: llamadas a herramientas, decisiones de permisos, configuración y sesiones del servidor. El texto de un prompt o de una respuesta nunca se registra.

El registro es una característica de la Edición Enterprise. En las licencias Enterprise, Consultancy y Trial, sí se guarda el registro, y **Abrir carpeta de auditoría** aparece en **Herramientas > Preferencia > Funciones de IA** y en el cuadro de diálogo **Herramientas > Servidor MCP...**. En las licencias Desktop y Business, y antes de activar una licencia, no se guarda nada, no se crea ninguna carpeta y no se muestra ninguno de los dos botones. Consulta @ai-audit-log.

| Valor                   | Tipo                | Qué hace                                                                                                                                                                                                                                                                                                                                                                                                       |
| ----------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AiAuditLogPath          | Ruta                | Redirige el registro de auditoría para que pueda recopilarse de forma centralizada. Se admite una ruta UNC a un recurso compartido de red. Cuando la política no está configurada, el registro se escribe en `%LocalAppData%\TabularEditor3\AI\audit`, con un archivo `ai-audit-<date>.jsonl` al día y los scripts registrados en `audit\scripts\<date>`. |
| AiAuditLogRetentionDays | Número, de 0 a 3650 | Cuántos días conservar el registro de auditoría; los archivos más antiguos se eliminan. `0` lo conserva todo. El valor predeterminado es 30 días.                                                                                                                                                                                                              |

## Qué ocurre sin la Edición Enterprise

Las políticas Enterprise nunca se ignoran sin avisar. Si se configura cualquiera de los valores de las tablas Enterprise anteriores —aunque sea uno que Tabular Editor no pueda interpretar— y la copia instalada de Tabular Editor 3 no tiene licencia para la Edición Enterprise, el Asistente de IA y el servidor MCP se niegan a iniciarse, y el Asistente de IA muestra un Report indicando que tu organización ha configurado políticas de IA que requieren la Edición Enterprise de Tabular Editor 3, e identifica los valores en cuestión. Todo lo demás en Tabular Editor 3 sigue funcionando, y las políticas generales anteriores se siguen aplicando.

Las políticas Enterprise también fallan en modo cerrado cuando no se puede interpretar un valor. Un límite de permisos mal escrito deniega el recurso en lugar de leerse como "sin límite", y un nombre de proveedor que Tabular Editor no reconoce hace que el Asistente de IA no esté disponible en lugar de recurrir a la propia elección del usuario.

`BlockUnsafeScripts` falla en modo cerrado de la misma manera, y conviene saber exactamente cómo, porque afecta a más que solo las funciones de IA. En una copia sin licencia para la Edición Enterprise, la mera presencia del valor impide la ejecución de **todos** los scripts y macros, sean seguros o no, con mensajes que indican la edición requerida; las macros desaparecen de los menús hasta que se activa una licencia Enterprise y vuelven a aparecer sin necesidad de reiniciar. Un valor que el lector no puede interpretar aplica la restricción en lugar de levantarla. Un `0` explícito no la aplica, pero sigue contando como configurado, así que también sitúa las funciones de IA tras la barrera de Enterprise.

Para desactivar toda la funcionalidad de IA sin una licencia Enterprise, usa la política general `DisableAi`.

## Ver qué políticas están en vigor

Abre **Herramientas > Preferencias > Tabular Editor > Actualizaciones y comentarios**. Cuando hay alguna política configurada, una sección **Administrado por tu organización** enumera todos los valores que encontró Tabular Editor, el propio valor y la clave y colmena del Registro de la que procede. Un valor que Tabular Editor no pudo interpretar se marca como _(no válido)_, lo que es la forma más rápida de encontrar un error tipográfico en una política que parece no tener efecto.

Los controles que una política haya bloqueado o limitado en otras partes de **Preferencias**, y en el cuadro de diálogo **Herramientas > Servidor MCP...**, se muestran como de solo lectura y llevan un mensaje emergente que indica que la configuración está controlada por la política de tu organización.

## Uso de las plantillas administrativas

Tabular Editor 3.27 y versiones posteriores instalan un par de plantillas administrativas de Directiva de Grupo, de modo que las políticas anteriores pueden configurarse desde el editor de Directiva de Grupo en lugar de editar el Registro. Las encontrarás en la carpeta `Policies` de la carpeta de instalación, que de forma predeterminada es `C:\Program Files\Tabular Editor 3\Policies`:

- `TabularEditorApS.admx`
- `en-US\TabularEditorApS.adml`

Para usarlos en un único equipo, copia ambos archivos en `%SystemRoot%\PolicyDefinitions`, manteniendo la estructura de carpetas `en-US`:

```
C:\Windows\PolicyDefinitions\TabularEditorApS.admx
C:\Windows\PolicyDefinitions\en-US\TabularEditorApS.adml
```

Para usarlos en todo un dominio, cópialos en el almacén central de un controlador de dominio, manteniendo la misma estructura:

```
\\<your-domain>\SYSVOL\<your-domain>\Policies\PolicyDefinitions\TabularEditorApS.admx
\\<your-domain>\SYSVOL\<your-domain>\Policies\PolicyDefinitions\en-US\TabularEditorApS.adml
```

A continuación, abre el Editor de directivas de grupo local (`gpedit.msc`) o el Editor de administración de directivas de grupo y busca en:

- **Configuración del equipo > Plantillas administrativas > Tabular Editor** para directivas de todo el equipo
- **Configuración de usuario > Plantillas administrativas > Tabular Editor** para directivas por usuario

Las directivas compartidas por Tabular Editor 3 y la CLI se encuentran directamente bajo **Tabular Editor**. Las directivas que aplica exclusivamente Tabular Editor 3 están en **Tabular Editor > Tabular Editor 3**; el Asistente de IA, el servidor MCP y la integración con el Optimizador de DAX tienen cada uno su propia subcarpeta.

Al establecer una directiva en **Habilitada** se escribe su valor en el Registro. Establecerla en **Deshabilitada** o dejarla en **No configurada** significa que la directiva no se aplica. Las plantillas no escriben en la clave heredada `Kapacity\Tabular Editor`, así que establece esa clave manualmente si una directiva también debe aplicarse a Tabular Editor 2.

Para las directivas de Enterprise, **Deshabilitada** elimina el valor del Registro en lugar de escribir un `0`. Eso es intencionado: la mera presencia de un valor de Enterprise es lo que hace que el Asistente de IA y el servidor MCP queden sujetos a la comprobación de licencia Enterprise, así que una directiva que un administrador acaba de desactivar no debe dejar ningún valor residual.

## Deshabilitar las comunicaciones web

Si quieres asegurarte de que Tabular Editor no realice solicitudes web, especifica las directivas `DisableUpdates`, `DisableBpaDownload`, `DisableWebDaxFormatter`, `DisableErrorReports`, `DisableTelemetry`, `DisableDaxOptimizer`, `DisableDaxPackageManager` y `DisableAi`.

> [!NOTE]
> Incluso cuando se especifican las políticas anteriores, Tabular Editor 3 seguirá realizando solicitudes ocasionales a `https://api.tabulareditor.com` para validar la licencia. Si Tabular Editor 3 no puede acceder a este endpoint (debido a un cortafuegos o un proxy), el usuario tendrá que [activar manualmente](xref:installation-activation-basic#manual-activation-no-internet) el producto cada 30 días.

## Deshabilitar los scripts personalizados

Si quieres asegurarte de que Tabular Editor no permita a los usuarios ejecutar código arbitrario, especifica las políticas `DisableCSharpScripts` y `DisableMacros` para deshabilitar las macros.

Si tu organización quiere seguir usando scripts, pero no a costa de permitir que cualquier script acceda al sistema de archivos, a la red o a otro programa, usa `BlockUnsafeScripts` en su lugar. Los scripts y las macros siguen funcionando sobre el modelo, y solo se rechazan las partes que intentan salir de él. Esa directiva requiere la Edición Enterprise; las dos anteriores se aplican en todas las ediciones.

## Deshabilitar las funciones de IA

Si quieres impedir toda la funcionalidad de IA, especifica la directiva `DisableAi`. Esto evita que se cargue al inicio cualquier componente relacionado con la IA y borra cualquier configuración de clave de API almacenada previamente. Se aplica en todas las ediciones y no requiere una licencia Enterprise.

A partir de la versión 3.27.0, el instalador también lee la directiva en las seis claves y con la misma precedencia, y omite por completo el componente de IA, de modo que los ensamblados de IA nunca se escriben en la carpeta de instalación de un equipo cuya directiva deshabilita la IA. Establece el valor como un `REG_DWORD` de `1`: el instalador interpreta `1` como _desactivar_ y cualquier otro valor presente como _no desactivado_, mientras que la aplicación acepta cualquier número distinto de cero. Consulta [Implementar sin las funciones de IA](xref:installation-activation-basic#deploying-without-the-ai-features) para implementar conjuntamente la selección de características y la directiva.

Para mantener disponible AI Assistant, pero limitar lo que puede hacer, usa en su lugar las políticas Enterprise anteriores: ajusta los límites de permisos a lo que tu organización considere adecuado, bloquea el proveedor y el endpoint en un Gateway que administres y usa `McpDisabledTools` para impedir que los agentes conectados accedan a herramientas concretas.
