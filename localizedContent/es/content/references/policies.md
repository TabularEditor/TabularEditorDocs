---
uid: policies
title: Políticas
author: Morten Lønskov
updated: 2026-10-23
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "Tabular Editor 2 reads the legacy registry key only, and honors only the policies marked TE2 below."
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          partial: true
          note: "General policies only"
        - edition: Business
          partial: true
          note: "General policies only"
        - edition: Enterprise
          full: true
    - product: Tabular Editor CLI
      partial: true
      note: "On Windows, and only for the policies marked CLI below."
---

# Directivas

Si administras Tabular Editor para una organización, puedes limitar sus funciones y configurar el Asistente de IA y el servidor MCP en nombre de tus usuarios a través de la política de grupo. Establece los valores en el registro de Windows manualmente o utiliza las plantillas administrativas que se incluyen con Tabular Editor 3.

La mayoría de las políticas son políticas generales, disponibles en todas las ediciones de Tabular Editor 3. Las políticas que configuran el Asistente de IA y el servidor MCP requieren [Tabular Editor 3 Edición Enterprise](xref:editions) y se indican a continuación con la etiqueta **Enterprise**.

> [!NOTE]
> Esta funcionalidad requiere las siguientes versiones de Tabular Editor:
>
>   - Tabular Editor [2.17.0](https://github.com/TabularEditor/TabularEditor/releases/tag/2.17.0) o una versión posterior
>   - Tabular Editor [3.3.5](https://github.com/TabularEditor/TabularEditor3/releases/tag/3.3.5) o una versión posterior, para las políticas generales
>   - Tabular Editor 3.27 o una versión posterior, para las claves de registro que se indican a continuación, para las políticas de todo el equipo y para todas las políticas empresariales
>   - Tabular Editor CLI 0.7 o posterior

## Claves del registro

Las políticas se leen a partir de seis claves, y la primera clave que define un valor decide ese valor. Todas las claves bajo `HKEY_LOCAL_MACHINE` tienen prioridad sobre todas las claves bajo `HKEY_CURRENT_USER`, por lo que el usuario no puede anular una política para todo el equipo establecida a través de la Configuración del equipo. Dentro de un subárbol, una clave específica del producto tiene prioridad sobre la clave compartida, que a su vez tiene prioridad sobre la clave heredada:

```
HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3
HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS
HKEY_LOCAL_MACHINE\Software\Policies\Kapacity\Tabular Editor
HKEY_CURRENT_USER\Software\Policies\Tabular Editor ApS\TE3
HKEY_CURRENT_USER\Software\Policies\Tabular Editor ApS
HKEY_CURRENT_USER\Software\Policies\Kapacity\Tabular Editor
```

- `Tabular Editor ApS\TE3` solo lo lee Tabular Editor 3. Tabular Editor CLI lee «Tabular Editor ApS\TECLI» en su lugar; las otras cuatro claves son las mismas para ambos.
- `Tabular Editor ApS` es la clave compartida, leída tanto por Tabular Editor 3 como por la CLI.
- `Kapacity\Tabular Editor` es la clave utilizada por las versiones anteriores. Sigue siendo leída y es la única clave que lee Tabular Editor 2, así que establezca también una política allí si también tiene que llegar a Tabular Editor 2.

La prioridad se aplica a cada valor por separado: un valor «DisableTelemetry» de 0 para todo el equipo anula un valor «DisableTelemetry» de 1 por usuario, mientras que un valor «DisableCSharpScripts» establecido solo por usuario sigue aplicándose.
Los nombres de los valores no distinguen entre mayúsculas y minúsculas.

## Tipos de valores

| Tipo de ajuste | Tipo de registro | Notas |
|--|--|--|
| Política de activación/desactivación | `REG_DWORD` | Cualquier valor distinto de cero aplica la política. `0` y la ausencia del valor significan que no se aplica. |
| Opción | `REG_SZ` | El nombre de la opción, por ejemplo `Read`, que es lo que escribe la plantilla administrativa. También se acepta un `REG_DWORD` que contenga la posición de la opción en la lista. |
| Número | `REG_DWORD` | Lo que escribe la plantilla administrativa. También se acepta un `REG_SZ` que contenga el número. |
| Lista | `REG_MULTI_SZ` | Una entrada por línea. También se acepta un `REG_SZ` cuyas entradas estén separadas por punto y coma. |
| Ruta, dirección o nombre | `REG_SZ` | |

Tabular Editor lee los valores de las políticas una sola vez, al iniciarse. Los cambios surtirán efecto la próxima vez que inicie la aplicación.

## Políticas generales

Para aplicar una de estas políticas, añada un valor `REG_DWORD` con el nombre que se indica a continuación y un valor distinto de cero. La columna **Productos** muestra qué productos cumplen la política: **TE3** es Tabular Editor 3, **CLI** es Tabular Editor CLI y **TE2** es Tabular Editor 2, que solo lee la clave heredada.

|Valor|Productos|Cuando se aplica...|
|--|--|--|
| DisableUpdates | TE3, TE2 | Tabular Editor no comprobará si hay versiones más recientes disponibles en línea. Los usuarios tampoco pueden buscar actualizaciones manualmente. |
| DisableCSharpScripts | TE3, TE2 | Tabular Editor no permitirá a los usuarios crear ni ejecutar scripts de C#. |
| DisableMacros | TE3, TE2 | Tabular Editor no permitirá a los usuarios guardar ni ejecutar macros. Las macros almacenadas en la carpeta `%LocalAppData%` no se cargan cuando se inicia la aplicación. |
| DisableBpaDownload | TE3, CLI, TE2 | No se pueden descargar de la web las reglas del Best Practice Analyzer. Las reglas almacenadas localmente o junto al modelo siguen funcionando. |
| DisableWebDaxFormatter | TE3, CLI, TE2 | El formateador DAX que envía código a daxformatter.com está deshabilitado. Tabular Editor 3 sigue ofreciendo su formateador integrado, que no envía nada a través de la red. |
| DisableErrorReports | TE3 | Los usuarios no pueden enviar informes de errores o bloqueos al equipo de asistencia de Tabular Editor. |
| DisableTelemetry | TE3, CLI | No se recopilan ni se envían datos de uso anónimos al equipo de asistencia de Tabular Editor. |
| DisableDaxOptimizer | TE3 | La integración con DAX Optimizer no está disponible. |
| DisableDaxOptimizerUpload | TE3 | Los usuarios no pueden cargar archivos del Analizador VertiPaq a través de la integración con el Optimizador de DAX. Se aplica de forma implícita cuando se activa `DisableDaxOptimizer`. |
| RequireDaxOptimizerObfuscation | TE3 | Los usuarios no pueden cargar archivos del Analizador VertiPaq en texto plano a través de la integración con DAX Optimizer; solo se pueden cargar archivos ofuscados. Se aplica de forma implícita cuando se activa `DisableDaxOptimizer` o `DisableDaxOptimizerUpload`. |
| DisableDaxPackageManager | TE3 | El administrador de paquetes DAX no está disponible. |
| DisableAi | TE3 | Todas las funciones de IA están desactivadas: el Asistente de IA, el servidor MCP y todas las funciones basadas en IA no están disponibles, no se carga nada relacionado con la IA cuando se inicia la aplicación y se borra cualquier configuración de proveedor almacenada, incluida la clave de la API. |
| DisableAiChat | TE3 | El panel de chat del Asistente de IA no está disponible. Otras funcionalidades de IA, incluido el servidor MCP, no se ven afectadas. |
| DisableMcpServer | TE3 | El servidor MCP no está disponible, por lo que las herramientas de agentes externos no pueden conectarse a Tabular Editor 3. El chat del asistente de IA no se ve afectado. |
| RequireMcpAccessToken | TE3 | Los clientes que se conecten al servidor MCP deben presentar el token de acceso que se muestra en el cuadro de diálogo **Herramientas > Servidor MCP...**, y los usuarios no pueden desactivar este requisito. |
| RequireNativeLibrarySignatureVerification | TE3 | Tabular Editor 3 verifica la firma Authenticode de las bibliotecas del editor de código, «Scintilla.dll» y «Lexilla.dll», antes de cargarlas. Si el equipo no puede validar la cadena de certificados del editor, los editores de código no se inician y Tabular Editor 3 se cierra. En el editor de directivas de grupo, esta directiva se denomina **Requerir la verificación de la firma de las bibliotecas de soporte del editor de código**. |

### En Tabular Editor CLI

Tabular Editor CLI respeta las políticas marcadas como **CLI** más arriba, en Windows, leyendo las mismas claves en el mismo orden que Tabular Editor 3. También respeta `BlockUnsafeScripts` de las [políticas Enterprise](#scripts-and-macros) que se indican a continuación, para `te script`, `te macro run` y `te bpa run --fix`.

Una operación rechazada no pasa desapercibida. «te» indica la política que la ha rechazado y sale con un código distinto de cero, por lo que un paso del «pipeline» falla en lugar de parecer que se ha completado con éxito sin que se haya hecho nada.

La CLI no tiene ediciones, por lo que una política que requiere Tabular Editor 3 Edición Enterprise en la aplicación de escritorio simplemente la aplica la CLI, independientemente de la licencia que tenga el equipo.

## Políticas Enterprise

Estas políticas determinan lo que puede hacer un script de C# y configuran el Asistente de IA y el servidor MCP. Todas ellas requieren Tabular Editor 3 Edición Enterprise y pertenecen a `Tabular Editor ApS\TE3`, excepto `BlockUnsafeScripts`, que también respeta Tabular Editor CLI y que, por tanto, pertenece a la clave compartida `Tabular Editor ApS`. En su lugar, colócala bajo «TE3» o «TECLI» para que afecte solo a uno de los dos.

### Scripts y macros

|Valor|Tipo|Qué hace|
|--|--|--|
| BlockUnsafeScripts | Activado/desactivado | Los scripts y las macros de C# solo están permitidos cuando permanecen dentro del modelo semántico. Un script que lee o escribe un archivo, accede a la red, inicia otro programa, incorpora código externo o envía un comando directamente al servidor se rechaza antes de que se ejecute nada de eso. |

La restricción se aplica dondequiera que se ejecute un script: **Ejecutar script** y **Ejecutar con vista previa** en un documento de script, **Aplicar corrección** en Best Practice Analyzer, el Asistente de IA, el servidor MCP y `te script`, `te macro run` y `te bpa run --fix` en la línea de comandos. Un script rechazado no es un script fallido. Nada llega al modelo, la lista de errores permanece vacía y un cuadro de diálogo **Script no ejecutado** indica el nombre de la política y lo que usó el script.

Una macro que se extiende fuera del modelo se omite en todos los menús, por lo que no se puede ejecutar por accidente. Sigue apareciendo en **Ver > Macros** con su columna **Bloqueada** rellenada, y aún se puede abrir y editar, de modo que se puede volver a incluir dentro de los límites en lugar de tener que reescribirla desde cero. El guardado de dicha macro se realiza correctamente y se indica que se ha guardado, pero que no se ejecutará.

Lo que se considera que permanece dentro del modelo se decide analizando el script compilado en lugar de buscando en su texto, por lo que también se rechazan las rutas indirectas a los mismos lugares: reflexión, árboles de expresiones, `Activator`, `AppDomain`, lectores XML o deserialización. Entre los [métodos auxiliares](xref:script-helper-methods) integrados, los tres que escriben fuera del modelo, `SaveFile`, `ExecuteCommand` y `Bpa.ExportCsv`, se consideran inseguros; los que solo leen, incluidos `ReadFile`, `ExecuteDax`, `EvaluateDax`, `ExecuteReader` y `ExportProperties`, no se consideran inseguros. Consulte [Políticas de administrador](xref:csharp-scripts#administrator-policies) para ver la misma regla desde el punto de vista del autor del script.

En el editor de directivas de grupo, esta opción se llama **Permitir únicamente secuencias de comandos y macros que se mantengan dentro del modelo** y, como se escribe en la clave compartida, se encuentra directamente bajo **Plantillas administrativas > Tabular Editor** en lugar de en la subcarpeta **Tabular Editor 3**.

### Límites de permisos

Cada uno de estos establece un límite superior a lo que el Asistente de IA y el servidor MCP pueden alcanzar para un tipo de recurso. Los valores aceptados son «Denegar», «Leer» y «Escribir», excepto para los datos del modelo, donde «Leer» es el ajuste más alto con sentido.

Un límite restringe lo que un usuario puede conceder: un permiso existente que supere el límite se reduce a este, la opción correspondiente en **Herramientas > Preferencias > Funciones de IA > Permisos** y en el cuadro de diálogo **Herramientas > Servidor MCP...** se muestra como de solo lectura, y el Asistente de IA ya no solicita un permiso que no se le puede conceder. Ninguna concesión supera un límite: ni un permiso permanente, ni uno concedido para un solo modelo, ni uno concedido en una versión anterior. La propia elección del usuario se mantiene intacta en sus preferencias, por lo que vuelve a aplicarse si se elimina la directiva.

|Valor|Valores aceptados|Limita el acceso a...|
|--|--|--|
| MaxModelMetadataAccess | Denegar, Leer, Escribir | Los metadatos del modelo abierto: nombres de tablas, columnas y medidas, expresiones, descripciones, resultados del Best Practice Analyzer y estadísticas de VertiPaq. «Write» también permite al asistente ejecutar sus propios scripts de C# en el modelo. Con «Denegar», no se envía nada en absoluto sobre el modelo abierto: ni el resumen del modelo, ni el aviso de que el modelo ha cambiado, ni la selección actual. |
| MaxModelDataAccess | Denegar, Leer | Valores de datos del modelo, es decir, los resultados de las consultas DAX. |
| MaxBpaAccess | Denegar, Leer, Escribir | Reglas del Best Practice Analyzer. `Read` permite listar las reglas y ejecutar el análisis; `Write` permite además añadir y modificar reglas. |
| MaxDocumentsAccess | Denegar, Leer, Escribir | Los documentos que el usuario tiene abiertos, como scripts de C# y consultas DAX. `Read` permite leer su contenido; `Write` permite además modificarlos. |
| MaxMacrosAccess | Denegar, Lectura, Escritura | La biblioteca de macros del usuario. |
| McpMaxModelMetadataAccess | Denegar, Lectura, Escritura | Los mismos cinco recursos, solo para el servidor MCP. |
| McpMaxModelDataAccess | Denegar, Leer | |
| McpMaxBpaAccess | Denegar, Lectura, Escritura | |
| McpMaxDocumentsAccess | Denegar, Lectura, Escritura | |
| McpMaxMacrosAccess | Denegar, Lectura, Escritura | |

Los cinco valores «McpMax...» se aplican únicamente al servidor MCP. Cuando uno de ellos no está establecido, el servidor MCP hereda el límite «Max...» correspondiente. Solo pueden reducir ese límite, nunca aumentarlo, por lo que a un agente desatendido nunca se le permite más que al asistente interactivo.

### Proveedor de IA

|Valor|Tipo|Valores aceptados|Qué hace|
|--|--|--|--|
| AiProvider | Opción | None, OpenAI, Anthropic, AzureOpenAI, Custom | Vincula el Asistente de IA a un proveedor. `None` desactiva el asistente de IA; el servidor MCP no se ve afectado. |
| AiEndpoint | Dirección | | Bloquea el punto de conexión o la URL base a los que se envían las solicitudes, por ejemplo, una pasarela interna o un recurso de Azure OpenAI. |
| AiModel | Nombre | | Bloquea el modelo o el nombre de la implementación de Azure OpenAI. El selector de modelos del panel de chat se reemplaza por un indicador sencillo, por lo que los usuarios no pueden cambiar de modelo. |
| AiOrganizationId | Nombre | | Bloquea la organización de OpenAI a la que se facturan las solicitudes. |
| AiProjectId | Nombre | | Bloquea el proyecto de OpenAI al que se facturan las solicitudes. |
| AiAllowedProviders | Lista | Cualquiera de los nombres de proveedores anteriores | Restringe qué proveedores pueden configurar los usuarios. Se permite un proveedor establecido por `AiProvider` tanto si aparece en la lista como si no, y siempre se ofrece `None`. Una lista de elementos permitidos no es una forma de impedir que un usuario desactive el asistente. |
| AiAllowedEndpointHosts | Lista | Nombres de host | Restringe los hosts a los que puede apuntar un extremo, por ejemplo, «gateway.contoso.com» o «*.contoso.com». |

Los ajustes bloqueados aparecen como de solo lectura en **Herramientas > Preferencias > Funciones de IA > Asistente de IA**, y el Asistente de IA utiliza la configuración bloqueada, independientemente de lo que el usuario hubiera elegido antes. No se escribe nada en las propias preferencias del usuario, por lo que su proveedor, su punto de conexión, su modelo y su clave de API vuelven a aparecer si se elimina la política. Las claves de API nunca se distribuyen mediante directivas.

Los nombres de host se comparan únicamente con la parte del host de la URL del punto de conexión. La coincidencia no distingue entre mayúsculas y minúsculas y no tiene en cuenta el puerto. Un «*.» inicial cubre los subdominios de un dominio, pero no el dominio en sí, así que enumera ambos si se desean los dos. La lista se aplica a todos los proveedores siempre que se establezca un punto de conexión, por lo que no se puede usar una anulación de la URL base para evitarla.

Se rechaza cualquier configuración que la política no permita, y el Asistente de IA indica qué regla la ha rechazado en lugar de enviar la solicitud: un proveedor que no está en la lista de permitidos, un host de punto de conexión que no está en la lista de permitidos de hosts, un punto de conexión que no es una URL válida cuando se aplica una lista de permitidos de hosts, o un proveedor de Azure OpenAI o personalizado bloqueado que no tiene ningún punto de conexión.

### Instrucciones personalizadas

|Valor|Tipo|Qué hace|
|--|--|--|
| AiCustomInstructionsPath | Ruta | Indica una carpeta de instrucciones personalizadas que el Asistente de IA carga para cada usuario, además de las que se incluyen con el producto. Se admite una ruta UNC a un recurso compartido de red de solo lectura. Cuando una instrucción de la organización y la propia instrucción de un usuario comparten el mismo identificador, prevalece la de la organización. |
| DisableUserCustomInstructions | Activado/desactivado | El Asistente de IA ignora las instrucciones personalizadas que el usuario ha colocado en su propia carpeta, y el botón que abre esa carpeta está desactivado. Las instrucciones que se incluyen con el producto y cualquier carpeta de la organización siguen cargándose. |

### Servidor MCP

|Valor|Tipo|Qué hace|
|--|--|--|
| McpDisabledTools | Lista | Nombres de las herramientas MCP que nunca se ofrecen a un cliente conectado. Las herramientas enumeradas no aparecen en la lista de herramientas del cliente y no se ejecutan aunque un cliente solicite una por su nombre. El chat del asistente de IA no se ve afectado. |
| McpPort | Número, de 1024 a 49151 | Bloquea el puerto en el que escucha el servidor MCP, de modo que se pueda compartir una configuración de cliente en toda una organización. El valor predeterminado es 42100. El servidor solo escucha en la dirección de bucle invertido. |

### Registro de auditoría

Tabular Editor 3 mantiene un registro local de la actividad del Asistente de IA y del servidor MCP: llamadas a herramientas, decisiones sobre permisos, configuración y sesiones del servidor. El texto de una solicitud o de una respuesta nunca se registra.

El registro es una función de la Edición Enterprise. En las licencias Enterprise, Consultancy y Trial, se registra, y **Abrir carpeta de auditoría** aparece en **Herramientas > Preferencias > Funciones de IA** y en el cuadro de diálogo **Herramientas > Servidor MCP...**. En las ediciones Desktop y Business, y antes de activar una licencia, no se escribe nada, no se crea ninguna carpeta y no se muestra ninguno de los dos botones. Consulta @ai-audit-log.

|Valor|Tipo|Qué hace|
|--|--|--|
| AiAuditLogPath | Ruta | Redirige el registro de auditoría para que se pueda recopilar de forma centralizada. Se admite una ruta UNC a un recurso compartido de red. Cuando la directiva no está establecida, el registro se escribe en `%LocalAppData%\TabularEditor3\AI\audit`, un archivo `ai-audit-<date>.jsonl` por día, con los scripts registrados en `audit\scripts\<date>`. |
| AiAuditLogRetentionDays | Número, de 0 a 3650 | Número de días del registro de auditoría que se conservarán; los archivos más antiguos se eliminan. «0» conserva todo. El valor predeterminado es 30 días. |

## Qué sucede sin la Edición Enterprise

Las políticas de la Edición Enterprise nunca se ignoran sin más. Si se establece alguno de los valores de las tablas Enterprise anteriores (aunque Tabular Editor no pueda interpretar ni siquiera uno) y la copia instalada de Tabular Editor 3 no tiene licencia para la edición Enterprise, el Asistente de IA y el servidor MCP se negarán a iniciarse, y el Asistente de IA informará de que tu organización ha configurado políticas de IA que requieren Tabular Editor 3 Edición Enterprise, indicando los valores en cuestión. Todo lo demás en Tabular Editor 3 sigue funcionando, y las políticas generales anteriores siguen aplicándose.

Las políticas Enterprise también fallan de forma cerrada cuando no se puede interpretar un valor. Un límite de permisos mal escrito deniega el recurso en lugar de interpretarse como «sin límite», y un nombre de proveedor que Tabular Editor no reconozca hace que el Asistente de IA no esté disponible en lugar de recurrir a la propia elección del usuario.

`BlockUnsafeScripts` falla de forma cerrada de la misma manera, y vale la pena saber exactamente cómo, porque va más allá de las superficies de la IA. En una copia que no tiene licencia para la edición Enterprise, la presencia del valor impide que se ejecute **ningún** script ni macro, sean seguros o no, y se muestra un mensaje en el que se indica la edición necesaria; las macros desaparecen de los menús hasta que se activa una licencia Enterprise, momento en el que vuelven a aparecer sin necesidad de reiniciar. Un valor que el lector no puede interpretar aplica la restricción en lugar de eliminarla. Un «0» explícito no la aplica, pero sigue contando como configurado, por lo que también deja las superficies de IA detrás de la barrera de Enterprise.

Para desactivar todas las funciones de IA sin una licencia Enterprise, use la política general «DisableAi».

## Ver qué políticas están vigentes

Abra **Herramientas > Preferencias > Tabular Editor > Actualizaciones y comentarios**. Cuando se establece cualquier política, la sección **Gestionado por su organización** enumera todos los valores que Tabular Editor ha encontrado, el valor en sí y la clave de registro y el subárbol de registro de los que procede. Los valores que Tabular Editor no ha podido interpretar se marcan como *(no válido)*, lo cual es la forma más rápida de encontrar una errata en una política que parece no tener ningún efecto.

Los controles que una política ha bloqueado o limitado en otros lugares de **Preferencias** y en el cuadro de diálogo **Herramientas > Servidor MCP...** se muestran como de solo lectura y llevan una información sobre herramientas que indica que la configuración está controlada por la política de su organización.

## Uso de las plantillas administrativas

Tabular Editor 3.27 y versiones posteriores instalan un par de plantillas administrativas de directivas de grupo, de modo que las directivas anteriores se pueden configurar desde el editor de directivas de grupo en lugar de editando el registro. Las encontrarás en la carpeta «Policies» de la carpeta de instalación, que por defecto es «C:\Program Files\Tabular Editor 3\Policies»:

- `TabularEditorApS.admx`
- `en-US\TabularEditorApS.adml`

Para usarlas en un solo equipo, copie ambos archivos en `%SystemRoot%\PolicyDefinitions`, manteniendo la estructura de carpetas `en-US`:

```
C:\Windows\PolicyDefinitions\TabularEditorApS.admx
C:\Windows\PolicyDefinitions\en-US\TabularEditorApS.adml
```

Para usarlos en un dominio, cópielos en el almacén central de un controlador de dominio, manteniendo la misma estructura:

```
\\<your-domain>\SYSVOL\<your-domain>\Policies\PolicyDefinitions\TabularEditorApS.admx
\\<your-domain>\SYSVOL\<your-domain>\Policies\PolicyDefinitions\en-US\TabularEditorApS.adml
```

A continuación, abra el Editor de directivas de grupo local (`gpedit.msc`) o el Editor de administración de directivas de grupo y busque en:

- **Configuración del equipo > Plantillas administrativas > Tabular Editor** para las políticas de todo el equipo
- **Configuración del usuario > Plantillas administrativas > Tabular Editor** para las políticas por usuario

Las políticas compartidas por Tabular Editor 3 y la CLI se encuentran directamente bajo **Tabular Editor**. Las políticas que solo aplica Tabular Editor 3 se encuentran en **Tabular Editor > Tabular Editor 3**, con el Asistente de IA, el servidor MCP y la integración de DAX Optimizer en sus propias subcarpetas.

Al establecer una política como **Habilitada**, se escribe su valor de registro. Establecerla en **Deshabilitada** o dejarla en **No configurada** significa que la directiva no se aplica. Las plantillas no escriben en la clave heredada «Kapacity\Tabular Editor», por lo que debe establecer esa clave manualmente si una política también tiene que llegar a Tabular Editor 2.

En el caso de las políticas Enterprise, **Desactivada** elimina el valor del registro en lugar de escribir un «0». Esto es deliberado: el mero hecho de que exista un valor Enterprise es lo que hace que el Asistente de IA y el servidor MCP dependan de la comprobación de la licencia Enterprise, por lo que una política que un administrador acabe de desactivar no debe dejar ningún valor.

## Desactivación de las comunicaciones web

Si desea asegurarse de que Tabular Editor no realice solicitudes web, especifique las políticas `DisableUpdates`, `DisableBpaDownload`, `DisableWebDaxFormatter`, `DisableErrorReports`, `DisableTelemetry`, `DisableDaxOptimizer`, `DisableDaxPackageManager` y `DisableAi`.

> [!NOTE]
> Incluso cuando se especifican las políticas anteriores, Tabular Editor 3 seguirá realizando solicitudes ocasionales a `https://api.tabulareditor.com` con fines de validación de la licencia. Si Tabular Editor 3 no puede acceder a este punto de conexión (debido a un cortafuegos o un proxy), el usuario tendrá que [activar manualmente](xref:installation-activation-basic#manual-activation-no-internet) el producto cada 30 días.

## Desactivación de scripts personalizados

Si desea asegurarse de que Tabular Editor no permita a los usuarios ejecutar código arbitrario, especifique las políticas `DisableCSharpScripts` y `DisableMacros`.

Si su organización desea conservar los scripts, pero no a costa de permitir que cualquier script acceda al sistema de archivos, a la red o a otro programa, utilice `BlockUnsafeScripts` en su lugar. Los scripts y las macros siguen funcionando con el modelo, y solo se rechazan las partes que salen de él. Esa política requiere la Edición Enterprise; las dos anteriores se aplican en todas las ediciones.

## Desactivar las funciones de IA

Si desea impedir todas las funcionalidades de IA, especifique la política `DisableAi`. Esto evita que se cargue nada relacionado con la IA al iniciar el programa y elimina cualquier configuración de clave de API almacenada. Se aplica en todas las ediciones y no requiere licencia Enterprise.

A partir de la versión 3.27.0, el instalador también lee la política, a partir de las seis claves y con la misma prioridad. Una nueva instalación deja fuera el componente de IA, y una actualización lo elimina de un equipo que lo tenga. Una instalación existente conserva los archivos de IA hasta la siguiente actualización, y Tabular Editor 3 no los carga mientras la política esté establecida. Establezca el valor como un `REG_DWORD` de `1`: el instalador trata el `1` como *deshabilitado* y cualquier otro valor presente como *no deshabilitado*, donde la aplicación acepta cualquier número distinto de cero. Consulte [Aplicar la decisión con la directiva DisableAi](xref:installation-activation-basic#enforcing-the-decision-with-the-disableai-policy) para implementar la selección de funciones y la directiva conjuntamente.

Para que el Asistente de IA siga estando disponible, pero limitando lo que puede hacer, usa en su lugar las políticas para empresas mencionadas anteriormente: establece los límites de permisos en función de lo que tu organización considere oportuno, bloquea el proveedor y el punto de conexión a una pasarela que gestiones y usa `McpDisabledTools` para impedir que los agentes conectados utilicen determinadas herramientas.
