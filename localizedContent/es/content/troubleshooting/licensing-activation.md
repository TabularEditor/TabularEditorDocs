---
uid: licensing-activation
title: Instalar y activar Tabular Editor 3
author: Morten Lønskov
updated: 2026-10-05
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Instalar y activar Tabular Editor 3

Esta página explica los problemas habituales de instalación y activación de Tabular Editor 3 y cómo resolverlos. Para el flujo de activación estándar, consulta @getting-started. Para escenarios de implementación avanzada (instalación desatendida, aprovisionamiento previo de licencias y configuración posterior a la instalación), consulta @installation-activation-basic.

## Verificar los requisitos del sistema

Confirma que el equipo cumple los requisitos antes de seguir con la resolución de problemas:

- **Sistema operativo:** Windows 10, Windows 11, Windows Server 2016, Windows Server 2019 o versiones posteriores
- **Arquitectura:** x64, ARM64 (nativo desde la versión 3.23.0)
- **.NET Runtime:** [.NET Runtime de Escritorio 8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

Usa el MSI correspondiente a tu arquitectura de la [página de descargas](xref:downloads). Una incompatibilidad entre el instalador y la arquitectura es una causa frecuente de instalaciones fallidas y de errores por dependencias faltantes al primer inicio.

## Inspeccionar la licencia activada

Tabular Editor 3 guarda los detalles de activación en el Registro de Windows, en `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`.

Para ver la clave de licencia actual del usuario de Windows activo, ejecuta lo siguiente en el Símbolo del sistema de Windows (Inicio > Ejecutar > cmd.exe):

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

You can also inspect and edit the values directly using `regedit.exe`. See [Registry details](xref:installation-activation-basic#registry-details) for every value in the key.

![Editor del Registro](~/content/assets/images/troubleshooting/registry-editor.png)

## El cuadro de diálogo de activación vuelve a aparecer

Tabular Editor 3 contacta con `https://api.tabulareditor.com` al iniciarse y periódicamente para validar la licencia. Si no se puede acceder a este punto de conexión debido a un cortafuegos o un proxy, la aplicación debe reactivarse cada 30 días. Consulta @policies para ver la lista completa de puntos de conexión utilizados.

Si los avisos de activación siguen apareciendo:

1. Confirma que se puede acceder a `api.tabulareditor.com` desde el equipo afectado.
2. Configura el proxy en **Herramientas > Preferencias > Configuración de proxy**. Consulta @proxy-settings para la solución de problemas específicos del proxy, incluida la anulación en **AnalysisServices.AppSettings.json** que habilita la compatibilidad de MSAL con proxies externos.
3. Si la red bloquea el tráfico saliente hacia el punto de conexión de activación, usa la [activación manual](#manual-activation-no-internet) que se indica a continuación.

## Activación manual (sin Internet)

Si el equipo donde se ejecuta Tabular Editor no puede acceder al punto de conexión de activación, el mensaje de activación ofrece un flujo manual.

![Aviso de activación manual](~/content/assets/images/getting-started/Activation_manual_firstprompt.png)

1. Introduce tu correo electrónico. Aparece un cuadro de diálogo con un enlace a una clave de activación.

2. Copia la URL y ábrela en otro equipo que tenga acceso a Internet. La URL devuelve un objeto JSON.

   ![Objeto JSON de activación manual](~/content/assets/images/getting-started/activation_manual_jsonobject.png)

3. Copia el objeto JSON completo y pégalo en el cuadro de diálogo del equipo sin conexión.

   ![Activación manual completada](~/content/assets/images/getting-started/activation_manual_dialogbox_filled.png)

Después, Tabular Editor 3 verifica la licencia.

## No se puede cambiar una clave de licencia desde la interfaz de usuario

The **Change license key** option under **Help > About Tabular Editor** appears only when no model is loaded. If the option is missing while a model is open, close the model under **File > Close model** and try again.

If the UI option still fails, reset the license through the Registry Editor::

1. Cierra todas las instancias de Tabular Editor 3.
2. Open the Registry Editor (Start > Run > regedit.exe).
3. Ubica `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`.
4. Delete the `LicenseKey`, `User`, `ActivationKey` and `Activation` values.
5. Reinicia Tabular Editor 3.

Alternatively, run the following in a Windows Command Prompt. A command reports an error if its value doesn't exist, and the remaining commands still run:

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v User /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v ActivationKey /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v Activation /f
```

The next launch prompts for a license key. Deleting the registry values leaves the installation activated on the licensing service; use the [Tabular Editor Self-service portal](https://tabulareditor.com/my-account/) to manage your activated licenses. .

> [!IMPORTANT]
> Una vez que se elimine una clave de licencia, el producto no podrá usarse por el usuario actual de Windows en ese equipo hasta que se introduzca una nueva clave de licencia.

## La licencia está en el usuario de Windows incorrecto

Las activaciones de Tabular Editor 3 se almacenan **por usuario** en `HKEY_CURRENT_USER`. Si varios usuarios comparten el mismo equipo, cada uno debe activar el producto en su propio perfil de usuario de Windows. Una licencia activada en una cuenta de Windows no es visible para otra cuenta de Windows en el mismo equipo.

Para comprobar qué cuenta de Windows tiene la licencia, inicia sesión como ese usuario y ejecuta la consulta del registro en [Inspeccionar la licencia activada](#inspect-the-activated-license).

### Cuenta de Windows vs. cuenta de Power BI / Entra

Una fuente habitual de confusión: la cuenta de Windows con la que se ejecuta Tabular Editor 3 es independiente de la cuenta de Microsoft Entra que se usa para autenticarse en un Workspace de Power BI / Fabric.

- **La activación de la licencia** se almacena en `HKEY_CURRENT_USER` del usuario de Windows que activó el producto. No está vinculada a ninguna identidad en la nube.
- **La autenticación del Workspace** se realiza al conectarse, en el cuadro de diálogo **Cargar modelo semántico desde base de datos**. Inicia sesión allí con la cuenta de Microsoft Entra que tenga permisos en el Workspace.

No necesitas iniciar Tabular Editor 3 con **Ejecutar como** usando otra cuenta de Windows solo porque te conectes a Power BI con una cuenta de Microsoft Entra distinta (por ejemplo, una cuenta de administrador sin correo habilitado). Inícialo con tu cuenta habitual de Windows, activa la licencia en esa cuenta e introduce las credenciales de administrador de Microsoft Entra en el cuadro de diálogo de conexión.

Para obtener información sobre cómo elegir el modo de autenticación adecuado (por ejemplo, **Microsoft Entra MFA** cuando tu inicio de sesión de Windows no coincide con tu cuenta de Power BI), consulta @xmla-as-connectivity.

## Un puesto Enterprise está en uso por otro usuario

Las licencias Enterprise se asignan por puesto. Para activar Tabular Editor 3 para un nuevo usuario cuando todos los puestos están ocupados, primero hay que cancelar la asignación del puesto al usuario actual desde el [portal de autoservicio de Tabular Editor](https://tabulareditor.com/my-account/). Esta acción la realiza el propietario de la suscripción o el administrador de licencias.

> [!NOTE]
> La reasignación de puestos solo es posible en la Edición Enterprise.

## Activación detrás de un proxy

Tabular Editor 3 usa solicitudes web salientes para la activación del producto, la comprobación de actualizaciones, el formato de DAX y la descarga de reglas externas de mejores prácticas. Si estás detrás de un proxy:

1. Configura **Herramientas > Preferencias > Configuración del proxy**. Cambia el **Tipo de proxy** entre `System` y `None`, reinicia Tabular Editor 3 y vuelve a intentar la activación.
2. Si la activación sigue fallando, consulta @proxy-settings para ver diagnósticos avanzados del proxy.
3. Si el acceso saliente a `api.tabulareditor.com` está bloqueado, usa [Activación manual](#manual-activation-no-internet).

> [!TIP]
> La configuración del proxy puede interferir con los cuadros de diálogo de autenticación y otras indicaciones externas. Después de cambiar el tipo de proxy, cierra siempre Tabular Editor 3 y vuelve a abrirlo antes de repetir la prueba.

## Comprueba que usas la versión más reciente

Los errores relacionados con la activación a veces se corrigen en versiones más recientes de Tabular Editor 3. Comprueba que usas la versión más reciente antes de enviar una solicitud de soporte. Comprueba si hay actualizaciones en **Herramientas > Preferencia > Actualizaciones y comentarios**, o descarga el instalador más reciente desde la [página de descargas](xref:downloads).
