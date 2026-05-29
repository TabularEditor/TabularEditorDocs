---
uid: locale-not-supported
title: Configuración regional no compatible
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

# Configuración regional no compatible

Es posible que veas alguno de los siguientes mensajes de advertencia:

```plaintext
The XXXX locale is not supported
```

```plaintext
XXXX is an invalid culture identifier
```

en la vista de mensajes de Tabular Editor 3.

![Mensaje de configuración regional no admitida](~/content/assets/images/troubleshooting/locale-not-supported-message-view.png)

Este problema suele producirse cuando tu equipo usa una **configuración regional que el motor de Analysis Services (SSAS) no admite**.  
En la mayoría de los casos, el error se desencadena por otro problema o advertencia subyacente, pero este mensaje se muestra como consecuencia.

---

## Escenarios y soluciones

### 1. Conexión a una instancia local de SSAS

Si estás ejecutando SQL Server Analysis Services (SSAS) localmente en tu equipo:

- **Solución:** Cambia la **cuenta de servicio** que usa la instancia de SSAS.  
  Actualizar la cuenta suele resolver incompatibilidades con configuraciones regionales no admitidas.

---

### 2. Conexión a una instancia remota de SSAS, Azure AS o Power BI

Al conectarte a una instancia remota, tienes dos soluciones posibles:

#### Opción A: Especificar la configuración regional en la cadena de conexión

Establece explícitamente una configuración regional admitida (por ejemplo, inglés – 1033) añadiendo `LocaleIdentifier=1033` a la cadena de conexión.

**Ejemplo (Azure AS):**

```plaintext
Data Source=asazure://westeurope.asazure.windows.net/instance-name;LocaleIdentifier=1033
```

#### Opción B: Cambiar la configuración regional de tu equipo

Ajusta la configuración regional y de idioma de tu sistema local para que coincida con una configuración regional admitida.

- **Ajustes recomendados:**
  - **Formato regional:** Inglés (Estados Unidos)
  - **Idioma para mostrar de Windows:** Inglés (Estados Unidos)