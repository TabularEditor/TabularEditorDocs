---
uid: xmla-as-connectivity
title: Conectividad con XMLA / Analysis Services
author: Daniel Otykier
updated: 2024-05-01
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Escritorio
          none: true
        - edition: Empresa
          partial: true
          note: "Solo los puntos de conexión XMLA de Premium por usuario"
        - edition: Empresarial
          full: true
---

# Conectividad con XMLA / Analysis Services

Tabular Editor usa la [biblioteca cliente de AMO](https://learn.microsoft.com/en-us/analysis-services/amo/developing-with-analysis-management-objects-amo?view=asallproducts-allversions) para conectarse al punto de conexión XMLA de Power BI / Fabric o a instancias de SQL Server o Azure Analysis Services (Tabular). La autenticación y la autorización las gestiona la biblioteca cliente de AMO, lo que significa que Tabular Editor no almacena credenciales ni tokens. Además, los usuarios deben tener permisos suficientes para conectarse al punto de conexión XMLA o a una instancia de Analysis Services. En la mayoría de los casos, el usuario debe ser miembro del rol de administrador del servidor de Analysis Services o tener permisos de administración en el Workspace de Power BI.

En el siguiente artículo, usaremos el término "servidor de modelo semántico" para referirnos al servicio al que se accede a través del punto de conexión XMLA de Power BI / Fabric o de cualquier instancia de SQL Server Analysis Services Tabular (SSAS) o Azure Analysis Services (AAS).

## Cuadro de diálogo de conexión

Para conectarte al servidor de modelo semántico, ve a **Archivo** > **Abrir** > **Modelo desde BD...**, o pulsa **Ctrl+Shift+O**.

Se abrirá el cuadro de diálogo **Cargar modelo semántico desde la base de datos**, donde puedes especificar el nombre del servidor, una cadena de conexión XMLA o elegir una instancia local de SSAS en una lista desplegable. Además, puedes especificar el tipo de autenticación que vas a usar.

> [!NOTE]
> En Tabular Editor 2.x, las **Opciones avanzadas** (para especificar el modo de lectura/escritura y un color personalizado para la barra de estado) no están disponibles.

![Cuadro de diálogo de conexión](~/content/assets/images/connect-dialog.png)

## Seleccionar base de datos

Después de hacer clic en "Aceptar", Tabular Editor se conectará al servidor de modelo semántico y recuperará una lista de bases de datos a las que tienes acceso. Selecciona la base de datos con la que quieres trabajar y haz clic en "Aceptar".

## Propiedades avanzadas de la cadena de conexión

En todas las versiones de Tabular Editor, puedes especificar una cadena de conexión OLAP en el cuadro de texto **Server**, en lugar de solo el nombre del servidor.

Una cadena de conexión OLAP típica tiene este aspecto:

```
Provider=MSOLAP;Data source=servername;Initial Catalog=databasename;Seguridad Integrada=SSPI;
```

> [!NOTE]
> Si se especifica la propiedad `Initial Catalog` en la cadena de conexión, no se mostrará el cuadro de diálogo **Select Database**, y Tabular Editor se conectará directamente a la base de datos especificada.

Las cadenas de conexión OLAP admiten muchas propiedades además de las mostradas anteriormente. Para ver la lista completa de propiedades, consulta la [documentación de Microsoft](https://learn.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions).

Además de las propiedades enumeradas en la documentación, las cadenas de conexión de AMO también admiten las siguientes propiedades:

### Identificador de configuración regional

Puedes especificar el idioma que se usará para la conexión estableciendo la propiedad `Locale Identifier`. El valor es un número que corresponde a un idioma específico. Por ejemplo, `1033` corresponde a inglés (Estados Unidos).

```
Provider=MSOLAP;Data source=servername;Initial Catalog=databasename;Seguridad Integrada=SSPI;Locale Identifier=1033;
```

Esto es útil si quieres que los mensajes de error y otros mensajes del servidor estén en un idioma específico. Si no se especifica la propiedad `Locale Identifier`, se usa el idioma del sistema operativo del cliente.

La mayoría de las instancias de Analysis Services admiten varios idiomas. Consulta [esta página para ver la lista completa de identificadores de configuración regional (LCID)](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-fulltext-languages-transact-sql?view=sql-server-ver16).

## Configuración de XMLA de Fabric/Power BI

Hay que activar dos configuraciones de administrador para habilitar el punto de conexión XMLA en Fabric/Power BI.

### Habilitar el punto de conexión XMLA del inquilino

En el portal de administración de Fabric/Power BI, se debe habilitar la configuración de integración "Permitir puntos de conexión XMLA y Analizar en Excel con modelos semánticos locales"

A nivel de inquilino, la configuración puede estar restringida a ciertos usuarios. Si en tu organización esta configuración está restringida, asegúrate de que todos los usuarios necesarios tengan permiso para usar el punto de conexión XMLA a nivel de inquilino.

![Configuración de administrador del inquilino](~/content/assets/images/common/XMLASettings/TennantAdminSetting.png)

### Habilitar lectura y escritura de XMLA en la capacidad

Para usar el punto de conexión XMLA, el Workspace que hospeda un modelo semántico debe estar asignado a una capacidad (FSku o Power BI Premium Per User) y la capacidad debe tener XMLA con ["Read Write" habilitado en la configuración de la capacidad.](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#enable-xmla-read-write)

![Configuración del administrador del inquilino](~/content/assets/images/common/XMLASettings/CapacityAdminSetting.png)

La opción "Read Write" se habilita en el portal de administración, yendo a

1. Configuración de capacidad
2. Elegir el tipo de capacidad
3. Seleccionar la capacidad correspondiente
4. Ve a Cargas de trabajo de Power BI y desplázate hacia abajo hasta encontrar la configuración del punto de conexión XMLA y elige "Read Write"

### Permisos de usuario a nivel de Workspace

Para editar modelos usando el punto de conexión XMLA, la cuenta del usuario debe tener acceso al Workspace como **Colaborador**, **Miembro** o **Administrador**. En el Workspace, elige "Administrar acceso" y agrega la cuenta de usuario o un grupo de Entra ID al que pertenezca el usuario con el rol requerido. Para obtener más información sobre los roles en Workspaces, consulta la documentación de Microsoft: [Roles en Workspaces](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces)

### Lectura/escritura en el modelo semántico

Asegúrate de que la cuenta del usuario tenga permiso de escritura en el modelo semántico. Esto puede ser necesario incluso si el usuario es administrador del Workspace, como se mencionó anteriormente.

Para comprobar que tu cuenta tiene los permisos necesarios, empieza por localizar el modelo en el Workspace de Fabric/Power BI; luego haz clic en el icono de más opciones (3 puntos verticales) y ve a la página "Administrar permisos".

![Administrar permisos en el modelo semántico](~/content/assets/images/common/XMLASettings/ManagePermissionsonSemanticModel.png)

Comprueba o concede a la cuenta del usuario o al grupo de Entra ID al que pertenezca el rol de **Administrador del Workspace** o **Colaborador del Workspace**, o el **permiso de escritura** en el modelo semántico. Por ejemplo, en la captura de pantalla siguiente, solo los 3 usuarios resaltados en azul podrían acceder al modelo a través de Tabular Editor:

![Permisos de usuario en el modelo semántico](~/content/assets/images/common/XMLASettings/UserPermissionsonSemanticModel.png)

### Configurar el Workspace para modelos semánticos grandes

Para garantizar la mejor experiencia al editar modelos usando el punto de conexión XMLA, el Workspace debe tener el formato de almacenamiento semántico establecido en **Formato de almacenamiento de modelos semánticos grandes**. Ve a "Configuración del Workspace" en la esquina superior derecha del Workspace de Fabric/Power BI. Primero, ve a "Información de licencia"; después, comprueba si el formato de almacenamiento está establecido como grande y, si no es así, elige "Editar" para cambiar el formato de almacenamiento.

![Formato de almacenamiento de modelo semántico grande](~/content/assets/images/common/XMLASettings/LargeSemanticModelStorageFormat.png)

## Configuración adicional de Fabric/Power BI.

### Deshabilitar la actualización del paquete

Si un usuario distinto del propietario del modelo semántico necesita editar el modelo a través del punto de conexión XMLA, debe deshabilitarse la configuración de administración de seguridad de Fabric/Power BI denominada "Bloquear la republicación y deshabilitar la actualización del paquete".

![Configuración del administrador del inquilino](~/content/assets/images/common/XMLASettings/DisablePackageRefresh.png)

## Tipos de modelo no compatibles

Varios tipos de modelos no admiten conexiones XMLA, [enumerados a continuación](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#unsupported-semantic-models).

No se puede acceder a los siguientes modelos semánticos mediante el punto de conexión XMLA. Estos modelos semánticos no aparecerán en el Workspace en Tabular Editor ni en ninguna otra herramienta.

- Modelos semánticos basados en una conexión en directo a un modelo de Azure Analysis Services o SQL Server Analysis Services.
- Modelos semánticos basados en una conexión en directo a un modelo semántico de Power BI en otro Workspace.
- Modelos semánticos con datos push mediante la API REST.
- Modelos semánticos en Mi Workspace.
- Modelos semánticos de libros de Excel

En Fabric, el modelo semántico predeterminado de un Lakehouse o un Warehouse se puede abrir o conectar desde Tabular Editor, pero [no se puede editar](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#considerations-and-limitations). Además, algunas operaciones que requieren acceso de lectura a determinadas [DMVs](https://learn.microsoft.com/en-us/analysis-services/instances/use-dynamic-management-views-dmvs-to-monitor-analysis-services?view=asallproducts-allversions), como recopilar estadísticas del Analizador VertiPaq, podrían no estar admitidas en los modelos semánticos predeterminados.

## Solución de problemas de conexiones XMLA

### Probar una conexión sencilla

Estos pasos muestran cómo conectarse de la forma más fiable a un modelo semántico de Fabric/Power BI desde Tabular Editor.

1. Para conectarse a un modelo semántico en Fabric, seleccione 'Archivo' > 'Abrir' > 'Modelo desde BD' (atajo predeterminado Ctrl+Shift+O)

2. Se te mostrará un cuadro de diálogo (ver más abajo) y tendrás que pegar la cadena de conexión de Power BI en el cuadro de texto etiquetado como 'Servidor'. Deja el resto de opciones tal como aparecen en la captura de pantalla (son los valores predeterminados). La cadena de conexión tiene el formato que se muestra a continuación. Puedes encontrar esta cadena de conexión en el servicio (más detalles aquí en este [documento de Microsoft en las secciones 'Connecting to a Premium Workspace' y 'To get the workspace connection URL'](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#connecting-to-a-premium-workspace)

![Cargar modelo desde base de datos](~/content/assets/images/common/XMLASettings/LoadModelFromDatabase.png)

Copia y pega la cadena de conexión directamente desde el Workspace, en lugar de copiarla de otro sitio o de otra persona, o de modificarla de cualquier manera.

3. Según tu equipo (si tu inicio de sesión de Windows está vinculado a Entra ID o a tu proveedor de identidades), es posible que se te solicite iniciar sesión. Es importante que la cuenta que uses sea la que tenga permisos para acceder al Workspace. Si tu organización tiene varios tenants o si tienes varios inicios de sesión, puede que esto no coincida con tu inicio de sesión de Windows. Debes usar exactamente la credencial que se muestra en la interfaz web de Fabric para tu usuario.

![Authenticate to FabricPowerBI](~/content/assets/images/common/XMLASettings/AuthenticateToFabricPowerBI.png)

4. Después de autenticarte correctamente, verás el cuadro de diálogo "Choose database". Selecciona una y haz clic en "Ok".

![Choose Database](~/content/assets/images/common/XMLASettings/ChooseDatabase.png)

### Establece el tipo de autenticación en Microsoft Entra ID

En algunos casos, la opción de seguridad "Integrada" puede ser distinta de la cuenta de usuario que debería usarse para autenticarse frente al servicio de Fabric/Power BI. El siguiente paso es elegir la opción **Microsoft Entra MFA** en el cuadro de diálogo de apertura del modelo.

![Microsoft Entra MFA](~/content/assets/images/common/XMLASettings/LoadModelFromDatabaseMicrosoftEntraID.png)

Al elegir la opción "Microsoft Entra MFA" se obliga a usar la autenticación multifactor y te permite seleccionar la cuenta específica necesaria para conectarte al Workspace.

### Varios tenants

Si has verificado el nombre de usuario y la cadena de conexión como se indicó antes y sigues teniendo problemas, lo siguiente que debes comprobar es si ayuda añadir el GUID del tenant a la cadena de conexión. Esto puede ser un problema si perteneces a varios tenants.

El ID de tenant se puede encontrar directamente en Power BI haciendo clic en el signo de interrogación de la esquina superior derecha y seleccionando "About Power BI". El ID de tenant se muestra como parte de la "Tenant URL". Ten cuidado: el cuadro de texto suele ser demasiado pequeño para mostrarla completa en la ventana de Power BI. Haz doble clic en la URL que se muestra para resaltar la cadena completa; así podrás copiarla y pegarla.

La URL completa no es el ID de tenant. El ID de tenant es el GUID al final de la cadena, después de "ctid=". En la captura de pantalla de abajo, mi ID de tenant empieza por "ddec", pero el tuyo será distinto. Cuando tengas el ID de tenant, puedes cambiar la cadena de conexión que usaste antes: reemplaza la parte de la ruta que dice "myorg" por tu ID de tenant.

A continuación tienes un ejemplo. Tu ID de tenant y el nombre de tu Workspace serán distintos de los que se muestran.

- Anterior: `powerbi://api.powerbi.com/v1.0/myorg/WorkspaceName`
- Nuevo: `powerbi://api.powerbi.com/v1.0/eeds65sv-kl25-4d12-990a-770ca3eb6226/WorkspaceName`

También puedes usar el nombre del tenant (p. ej., `fabrikam.com`), como se muestra en [este artículo](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools#connecting-to-a-premium-workspace) sobre cómo conectarse a un Workspace Premium.

A continuación, intenta conectarte siguiendo al pie de la letra las instrucciones de la sección [Probar una conexión simple](#testing-a-simple-connection)

### Nombres duplicados

Puede haber problemas al conectarte a un modelo si el nombre del Workspace está duplicado con el de otro Workspace o si el nombre del modelo está duplicado con el de otro modelo.

Si hay nombres duplicados, consulta la documentación de Microsoft en las secciones ["Nombres de Workspace duplicados" y "Nombre de modelo semántico duplicado"](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#duplicate-workspace-names) para aprender a modificar la cadena de conexión y así solucionar estos problemas

### Gestión de proxy

Otra causa habitual de problemas de conectividad son los servidores proxy. Para más información, revisa [este artículo](xref:proxy-settings).

### Probar la conectividad con PowerShell

Si los problemas de conectividad persisten incluso después de intentar los pasos de solución de problemas anteriores, también es posible conectarse directamente al punto de conexión XMLA mediante las [bibliotecas cliente de Analysis Services proporcionadas por Microsoft](https://www.nuget.org/packages/Microsoft.AnalysisServices/), _sin_ usar Tabular Editor. Podemos hacerlo con un script sencillo de PowerShell, como se muestra a continuación. Si esta conexión también falla, es una señal clara de que el problema no está relacionado con Tabular Editor; en ese caso, considera abrir un caso de soporte con Microsoft. Al ponerte en contacto con Microsoft, indícales qué versión de **Microsoft.AnalysisServices.Tabular.dll** y **Microsoft.Identity.Client.dll** estás usando, e incluye también el script de PowerShell. Indícales también si estás usando las versiones de las DLL de .NET Core (Tabular Editor 3) o de .NET Framework (Tabular Editor 2). Evita mencionar Tabular Editor directamente en tu solicitud de soporte, ya que esto puede confundir al soporte de primer nivel. Después de crear el ticket de soporte, avísanos también en support@tabulareditor.com, ya que nos interesa hacer seguimiento de la frecuencia de estos problemas.

Para usar el script:

1. Navega hasta la carpeta de instalación de Tabular Editor 3 en el Explorador de Windows
2. Haz clic con el botón derecho en algún lugar de la carpeta y elige "Abrir en Terminal". Esto debería abrir una ventana de PowerShell. También puedes abrir una ventana de comandos normal y escribir `pwsh` para iniciar PowerShell.
3. Comprueba que la versión de PowerShell sea al menos la 6.2.0. Si el modo de lenguaje restringido está restringido, intenta abrir el terminal como administrador o solicita ayuda a tu equipo de administración de TI para ejecutar el script.
4. En el Bloc de notas, ajusta la URL XMLA del script siguiente para que coincida con el punto de conexión al que intentas acceder. Luego, copia el script modificado en la ventana de PowerShell y presiona [Enter] para ejecutarlo.

```powershell
# Ejecuta este script desde la carpeta de instalación de Tabular Editor 3, ya que esta carpeta
# contiene todas las DLL necesarias.

# Configuración
# TODO: Actualiza la URL de XMLA a continuación y modifica las propiedades de la cadena de conexión según sea necesario
$xmla = "powerbi://api.powerbi.com/v1.0/myorg/workspace-name"
$connectionString = "Provider=MSOLAP;Data Source=$xmla;Interactive Login=Always;Identity Mode=Connection"

# Cargar DLLs
Add-Type -Path "Microsoft.AnalysisServices.Tabular.dll"

# Crear el objeto Microsoft.AnalysisServices.Tabular.Server:
$server = New-Object Microsoft.AnalysisServices.Tabular.Server

try {
	# Conectar
	$server.Connect($connectionString)

	Write-Host "Conexión establecida." -ForegroundColor Green
	Write-Host "Conectado a: $($server.Name)"
}
catch {
	Write-Host "Error de conexión:" -ForegroundColor Red
	Write-Host $_.Exception.Message -ForegroundColor Red
}
```

Si el script **se ejecuta correctamente**, significa que tu máquina puede conectarse al punto de conexión XMLA usando las bibliotecas cliente de Microsoft. Si, al mismo tiempo, **no** puedes conectarte con Tabular Editor, abre un ticket en nuestra página de soporte de [Tabular Editor 2](https://github.com/TabularEditor/TabularEditor/issues) o [Tabular Editor 3](https://github.com/TabularEditor/TabularEditor3/issues), o envía un correo a support@tabulareditor.com (**solo para clientes de la Edición Enterprise de Tabular Editor 3**).

Si el script **falla**, algo en tu entorno está bloqueando la conectividad con el punto de conexión XMLA, por lo que Tabular Editor tampoco podrá conectarse. En este caso, ponte en contacto con tu departamento de TI para solucionar problemas con los firewalls/proxies antes de contactar con el soporte de Microsoft.

Si el script **se ejecuta correctamente** con las DLL de Tabular Editor 2, pero **falla** con las DLL de Tabular Editor 3 (o viceversa), ponte en contacto con el soporte de Microsoft, ya que en este caso el problema sería una discrepancia entre la versión de .NET Framework de las DLL (usadas por Tabular Editor 2) y la versión de .NET Core de las DLL (usadas por Tabular Editor 3).
