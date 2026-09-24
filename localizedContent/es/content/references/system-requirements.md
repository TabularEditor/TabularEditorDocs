---
uid: system-requirements
title: Requisitos del sistema
author: Morten Lønskov
updated: 2026-09-14
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

Tabular Editor 3 es una aplicación de escritorio para Windows. A partir de la versión 3.27.0, se publica para dos runtimes de .NET, dos arquitecturas de procesador y en tres formatos de paquete.

## Sistema operativo

- Windows 10, Windows 11, Windows Server 2016, Windows Server 2019 o versiones posteriores

Las versiones de Windows compatibles en cada momento se rigen por la política de Microsoft sobre sistemas operativos compatibles con .NET para el runtime que instales; por lo tanto, la lista de sistemas compatibles puede reducirse con el tiempo, independientemente de Tabular Editor.

## Qué se publica

| Runtime                                                    | Arquitectura | Formatos                                    |
| ---------------------------------------------------------- | ------------ | ------------------------------------------- |
| .NET 10 _(recomendado)_ | x64, ARM64   | instalador `.exe`, `.msi` y `.zip` portátil |
| .NET 8                                     | x64, ARM64   | instalador `.exe`, `.msi` y `.zip` portátil |

Las compilaciones de .NET 10 y .NET 8 son _funcionalmente idénticas_. No hay nada disponible en una que falte en la otra, y ambas pueden instalarse una junto a la otra.

Las compilaciones ARM64 son nativas a partir de la versión 3.23.0.

## Entorno de ejecución para «.NET»

| Compilación       | Necesita                                                                                                                                                                                                                                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Instalador `.exe` | El [.NET Desktop Runtime](https://dotnet.microsoft.com/download/dotnet) correspondiente: [10](https://dotnet.microsoft.com/download/dotnet/10.0) o [8](https://dotnet.microsoft.com/download/dotnet/8.0). El instalador se ofrece a descargarlo e instalarlo por ti |
| `.msi`            | El .NET Desktop Runtime correspondiente, ya instalado. El MSI _no_ lo incluye, lo que lo hace adecuado para el despliegue sin supervisión                                                                                                                                           |
| `.zip` portátil   | Nada. Es autónomo                                                                                                                                                                                                                                                                                   |

Debe ser el runtime _Desktop_. El runtime de ASP.NET Core y el runtime base de .NET no incluyen las bibliotecas de Windows Forms y WPF que necesita la aplicación.

## Elegir una compilación

Elige el **instalador `.exe` x64 de .NET 10** salvo que tengas una razón para no hacerlo. Las razones son:

- **ARM64**: usas un PC basado en ARM
- **.NET 8**: tu organización aún no puede instalar el .NET Desktop Runtime de .NET 10
- **`.msi`**: vas a realizar un despliegue centralizado. Consulta la [instalación silenciosa](xref:installation-activation-basic)
- **`.zip` portátil**: no puedes instalar software en el equipo o quieres varias versiones en paralelo

## Componentes opcionales

| Componente                                                                                     | Necesario para                                                                | Notas                                                                                                                                                                                                                                                               |
| ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [runtime de Microsoft Edge WebView2](https://developer.microsoft.com/microsoft-edge/webview2/) | La página **Primeros pasos** de la aplicación y el @ai-assistant | Viene incluido en las instalaciones actuales de Windows. Si no está disponible, Tabular Editor recurre al control de navegador integrado o ofrece un enlace para abrir la página en tu navegador predeterminado                                     |
| Funciones de IA                                                                                | El @ai-assistant y el servidor MCP                               | Un componente del instalador, seleccionado de forma predeterminada. Se puede desmarcar durante la instalación, y un administrador puede deshabilitar las funciones de IA de todos modos mediante la directiva `DisableAi` en @policies |

## Dónde encontrar las descargas

Consulta @downloads para la versión actual y @release-history para las anteriores.

## Pasos a seguir

- @downloads
- @getting-started
- @installation-activation-basic
