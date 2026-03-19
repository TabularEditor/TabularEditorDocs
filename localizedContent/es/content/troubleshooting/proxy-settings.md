---
uid: proxy-settings
title: Configuración del proxy
author: Daniel Otykier
updated: 2024-11-07
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

# Configuración del proxy

Debido a las diferencias en el comportamiento del proxy entre .NET Core (utilizado por Tabular Editor 3) y .NET Framework (utilizado por Tabular Editor 2 y DAX Studio), es posible que tengas problemas al conectarte a servicios externos, como el servicio de Power BI, cuando uses Tabular Editor 3 detrás de un servidor proxy.

Por ejemplo, podrías ver el siguiente mensaje de error al intentar conectarte al servicio Power BI:

![No such host is known-error](~/content/assets/images/troubleshooting/proxy-error.png)

Los mensajes de error típicos que puedes ver son:

**Título:** `Could not connect to server`

**Mensaje:**

- `No such host is known. (login.microsoftonline.com:443)`
- `Unable to obtain authentication token using the credentials provided`
- `The requested address is not valid in its context. (login.microsoftonline.com:443)`

Cuando esto sucede, lo primero que debes probar es cambiar la configuración del proxy en Tabular Editor 3. Puedes encontrar estos ajustes en **Tools > Preferencias > Proxy Settings**:

![Proxy settings in Tabular Editor 3](~/content/assets/images/troubleshooting/proxy-settings.png)

En la mayoría de los casos, cambiar el **Tipo de proxy** de `None` a `System` resolverá el problema. Esta opción indica a Tabular Editor 3 que use la configuración del proxy del sistema definida en Windows. Si sigues teniendo problemas, puedes intentar configurar el **Tipo de proxy** como `Custom` e introducir manualmente la dirección y el puerto del servidor proxy.

> [!IMPORTANT]
> Después de cambiar la configuración del proxy, debes reiniciar Tabular Editor 3 para que los cambios surtan efecto.

# Gestión del proxy en .NET Core frente a .NET Framework

Si la sugerencia anterior no resuelve el problema, a partir de la versión 3.21.0 de Tabular Editor puedes probar la siguiente solución alternativa:

> [!NOTE]
> Las soluciones que se describen a continuación requieren Tabular Editor 3.21.0 o posterior, ya que las opciones de configuración de AS solo están disponibles en la biblioteca cliente AMO/TOM v. [19.94.1.1](https://www.nuget.org/packages/Microsoft.AnalysisServices/19.94.1.1). Las versiones anteriores de Tabular Editor 3 usan una versión más antigua de esta biblioteca cliente, que ignora estas opciones de configuración.

Crea un archivo llamado <a href="https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/AnalysisServices.AppSettings.json" download="AnalysisServices.AppSettings.json">**AnalysisServices.AppSettings.json**</a> y colócalo en la carpeta de instalación de Tabular Editor 3 (es decir, la misma carpeta en la que se encuentra TabularEditor3.exe). Añade el siguiente contenido al archivo:

```json
{
  "asConfiguration": {
    "authentication": {
      "msalConnectivityMode": "external"
    }
  }
}
```

Para habilitar la compatibilidad con proxy externo de MSAL para todas las aplicaciones .NET Core de tu equipo, también puedes establecer la siguiente variable de entorno en lugar de usar el archivo AppSettings como se describe arriba:

| Nombre de la variable de entorno                                     | Valor de la variable de entorno |
| -------------------------------------------------------------------- | ------------------------------- |
| MS_AS_MsalConnectivityMode | 1                               |

# Habilitar diagnósticos

Si, después de intentar las soluciones descritas anteriormente, sigues sin poder conectarte, puede ser útil activar el registro de diagnósticos avanzados. Puedes hacerlo ya sea modificando el archivo **AnalysisServices.AppSettings.json** para que quede de la siguiente forma:

```json
{
  "asConfiguration": {
    "authentication": {
      "msalConnectivityMode": "external"
    },
    "diagnostics": {
      "authenticationTrace": {
        "isEnabled": true,
        "traceLevel": 4,
        "fileName": "<path to trace file>"
      }
    }
  }
}
```

o, si usas variables de entorno, configurando lo siguiente:

| Nombre de la variable de entorno                                                               | Valor de la variable de entorno                   |
| ---------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| MS_AS_AADAUTHENTICATOR_LOG      | 1                                                 |
| MS_AS_AADAUTHENTICATOR_LOGLEVEL | 4                                                 |
| MS_AS_AADAUTHENTICATOR_LOGFILE  | \<path to trace file\> |

`<path to trace file>` debe apuntar a un archivo ubicado en un directorio existente. Es decir. si quieres que el archivo se escriba en `c:\temp\logs\as-auth.log`, debes asegurarte de que exista el directorio `c:\temp\logs`.

El contenido de este archivo de seguimiento es útil al ponerte en contacto con el soporte técnico de Microsoft.

> [!IMPORTANT]
> Debes reiniciar Tabular Editor 3 después de realizar cambios en el archivo **AnalysisServices.AppSettings.json** o después de modificar variables de entorno.