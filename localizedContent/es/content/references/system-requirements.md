---
uid: system-requirements
title: Requisitos del sistema
author: Morten Lønskov
updated: 2026-10-23
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
# Requisitos del sistema

Tabular Editor 3 es una aplicación de escritorio de Windows. A partir de la versión 3.27.0, se publica en dos tiempos de ejecución de .NET, para dos arquitecturas de procesador, en tres formatos de paquete.

## Sistema operativo

- Windows 10, Windows 11, Windows Server 2016, Windows Server 2019 o versiones posteriores

Las versiones de Windows compatibles en un momento dado se rigen por la política de sistemas operativos compatibles con .NET de Microsoft para el tiempo de ejecución que instales, por lo que puede reducirse con el tiempo independientemente de Tabular Editor.

## Qué se publica

| Entorno de ejecución | Arquitectura | Formatos |
|---|---|---|
| .NET 10 *(recomendado)* | x64, ARM64 | Instalador `.exe`, `.msi`, `.zip` portátil |
| .NET 8 | x64, ARM64 | Instalador `.exe`, `.msi`, `.zip` portátil |

Las compilaciones de .NET 10 y .NET 8 son *funcionalmente idénticas*. No hay nada disponible en una que no esté disponible en la otra. Instalar una compilación con el instalador `.exe` o `.msi` reemplaza la otra compilación. Consulte [Cambiar entre los paquetes .NET 8 y .NET 10](xref:installation-activation-basic#switching-between-the-net-8-and-net-10-packages).

Las compilaciones ARM64 son nativas, a partir de la versión 3.23.0.

## Entorno de ejecución de .NET

| Build | Necesita |
|---|---|
| Instalador `.exe` | El [.NET Desktop Runtime](https://dotnet.microsoft.com/download/dotnet) correspondiente: [10](https://dotnet.microsoft.com/download/dotnet/10.0) u [8](https://dotnet.microsoft.com/download/dotnet/8.0). El instalador te ofrece descargarlo e instalarlo por ti |
| `.msi` | El .NET Desktop Runtime correspondiente, instalado previamente. El MSI *no* lo incluye, lo cual es lo que lo hace adecuado para una implementación desatendida |
| `.zip` portátil | Nada. Es autónomo |

Debe ser el tiempo de ejecución de *Desktop*. El entorno de ejecución de ASP.NET Core y el entorno de ejecución de .NET normal no incluyen las bibliotecas de Windows Forms y WPF que necesita la aplicación.

## Elegir una compilación

Elige el **instalador `.exe` de .NET 10 x64** a menos que tengas una razón para no hacerlo. Las razones son:

- **ARM64**: estás en un PC basado en ARM
- **.NET 8**: tu empresa aún no puede instalar el tiempo de ejecución de escritorio de .NET 10.
- **`.msi`**: estás realizando una implementación centralizada. Consulta [Instalación silenciosa](xref:installation-activation-basic)
- **`.zip` portátil**: no puede instalar software en el equipo o desea tener varias versiones instaladas simultáneamente.

## Componentes opcionales

| Componente | Necesario para | Notas |
|---|---|---|
| [Entorno de ejecución de Microsoft Edge WebView2](https://developer.microsoft.com/microsoft-edge/webview2/) | La página **Introducción** de la aplicación y el @ai-assistant | Presente en las instalaciones actuales de Windows. Cuando no está presente, Tabular Editor recurre al control de navegador integrado u ofrece un enlace para abrir la página en su navegador predeterminado |
| Funciones de IA | El @ai-assistant y el servidor MCP | Un componente del instalador, seleccionado de forma predeterminada. Se puede anular su selección durante la instalación, y un administrador puede deshabilitar las funciones de IA independientemente de ello con las @policies `DisableAi` |

## Dónde están las descargas

Consulte @downloads para ver la versión actual y @release-history para ver las versiones anteriores.

## Próximos pasos

- @downloads
- @getting-started
- @instalación-activación-básica
