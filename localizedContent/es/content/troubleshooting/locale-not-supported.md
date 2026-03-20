---
uid: locale-not-supported
title: Configuración regional no admitida
author: Morten Lønskov
updated: 2025-09-02
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

# Configuración regional no admitida

Es posible que veas el siguiente mensaje de advertencia en los mensajes:

```plaintext
La configuración regional XXXX no es compatible
```

en la vista de mensajes de Tabular Editor 3.

![Mensaje de configuración regional no admitida en mensajes](~/content/assets/images/troubleshooting/locale-not-supported-message-view.png)

Este problema suele producirse cuando tu equipo usa una **configuración regional que el motor de Analysis Services (SSAS) no admite**.  
En la mayoría de los casos, el error se desencadena por otro problema o advertencia subyacente, pero este mensaje se muestra como consecuencia en los mensajes.

---

## Escenarios y soluciones

### 1. Conexión a una instancia local de SSAS

Si ejecutas SQL Server Analysis Services (SSAS) localmente en tu equipo:

- **Solución:** Cambia la **cuenta de servicio** que usa la instancia de SSAS.  
  Actualizar la cuenta suele resolver incompatibilidades de configuración regional no admitida.

---

### 2. Conexión a un SSAS remoto, Azure AS o Power BI

Al conectarte a una instancia remota, tienes dos posibles soluciones:

#### Opción A: especificar la configuración regional en la cadena de conexión

Configura explícitamente una configuración regional compatible (p. ej., inglés: 1033) añadiendo `LocaleIdentifier=1033` a tu cadena de conexión.

**Ejemplo (Azure AS):**

```plaintext
Data source=asazure://westeurope.asazure.windows.net/instance-name;LocaleIdentifier=1033
```

#### Opción B: Cambiar la configuración regional en tu equipo

Ajusta la configuración regional y de idioma de tu sistema local para que coincida con una configuración regional compatible.

- **Configuración recomendada:**
  - **Formato regional:** Inglés (Estados Unidos)
  - **Idioma de visualización de Windows:** Inglés (Estados Unidos)