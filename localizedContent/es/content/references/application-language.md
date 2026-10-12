---
uid: references-application-language
title: Idioma de la aplicación
author: Morten Lønskov
updated: 2026-01-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
description: Cambia el idioma de visualización de la interfaz de usuario de Tabular Editor 3.
---

# Idioma de la aplicación

Tabular Editor 3 admite varios idiomas en la interfaz de usuario. Puedes alternar entre ellos en cualquier momento.

> [!NOTE]
> Tabular Editor 3 aún no está totalmente localizado. En concreto, por ahora no hemos localizado las propiedades individuales de TOM.

## Idiomas admitidos

| Idioma  | Estado                |
| ------- | --------------------- |
| Inglés  | Totalmente compatible |
| Español | En vista previa       |
| Chino   | En vista previa       |
| Francés | Beta                  |
| Alemán  | Beta                  |
| Japonés | Beta                  |

> [!NOTE]
> Los idiomas en **Preview** tienen traducidos los elementos principales de la interfaz, pero la cobertura puede ser incompleta. Los idiomas **Beta** son experimentales y pueden tener lagunas importantes o incoherencias. Envía un **Report** de problemas en [GitHub](https://github.com/TabularEditor/TabularEditor3/issues).

### Idiomas en Preview

Que un idioma tenga soporte beta significa que ha sido verificado por un traductor humano, pero es posible que Tabular Editor 3 aún no esté totalmente localizado. En concreto, por ahora no hemos localizado las propiedades individuales de TOM.

### Idiomas Beta

Los idiomas beta se han traducido exclusivamente con IA y no han sido revisados por traductores humanos. Planeamos pasar los idiomas Beta a Preview en el segundo trimestre de 2026.

## Cambiar el idioma

Hay dos formas de cambiar el idioma de la aplicación:

### Desde el menú Ventana

1. Haz clic en **Ventana** > **Idioma**
2. Selecciona el idioma deseado
3. Haz clic en **OK** cuando se te solicite reiniciar
4. Reinicia Tabular Editor 3 manualmente

[Cambiar el idioma a través del menú Ventana](~/content/assets/images/user-interface/chaning-language-windows-ui.png)

### Desde Preferencia

1. Haz clic en **Herramientas** > **Preferencia**
2. Ve a la sección **UI**
3. Selecciona el idioma que desees en el menú desplegable **Idioma**
4. Haz clic en **Aceptar** cuando se te solicite reiniciar
5. Reinicia Tabular Editor 3 manualmente

[Cambiar idioma desde el menú Ventana](~/content/assets/images/user-interface/chaning-language-preferences.png)

## Requisito de reinicio

**Debes reiniciar Tabular Editor 3** para que los cambios de idioma surtan efecto. La aplicación te pide que reinicies, pero no se reinicia automáticamente. Guarda tu trabajo antes de cambiar el idioma.

[Cambiar idioma desde el menú Ventana](~/content/assets/images/user-interface/chaning-language-restart-pop-up.png)

## Idioma de instalación

Durante la instalación, el instalador te pide que selecciones un idioma (inglés, español o chino). Esto establece tu preferencia de idioma inicial, y Tabular Editor 3 se mostrará en ese idioma al iniciarse por primera vez.

El instalador guarda tu selección en el archivo de preferencias de tu carpeta LocalAppData. Puedes cambiarlo más adelante con cualquiera de los dos métodos anteriores.

## Persistencia del idioma

Tu preferencia de idioma se guarda en `UiPreferences.json` en tu perfil de usuario. La configuración se mantiene tras las actualizaciones de la aplicación y los reinicios.

## Enviar comentarios

### Problemas de traducción

Si encuentras traducciones incorrectas o texto faltante:

- Abre una incidencia en [GitHub](https://github.com/TabularEditor/TabularEditor3/issues)
- Incluye el idioma, el texto incorrecto y en qué parte de la interfaz de usuario aparece
- Sugiere la traducción correcta si es posible

## Véase también

- [Preferencias](xref:preferences)
- [Descripción general de la interfaz de usuario](xref:user-interface)
