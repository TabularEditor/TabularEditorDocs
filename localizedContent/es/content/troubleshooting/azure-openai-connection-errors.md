---
uid: azure-openai-connection-errors
title: Errores de conexión de Azure OpenAI
author: Morten Lønskov
updated: 2026-04-15
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.26.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Errores de conexión de Azure OpenAI

Esta página cubre los errores de conexión más comunes al usar Azure OpenAI como proveedor para @ai-assistant. Consulta la [sección de configuración de Azure OpenAI](xref:ai-assistant#azure-openai) para ver los detalles de configuración.

## 403 "El acceso público está deshabilitado. Por favor, configura el punto de conexión privado"

Este error 403 proviene del propio Azure OpenAI, lo que significa que la solicitud HTTP llegó al punto de conexión público en lugar de a tu punto de conexión privado. Azure la rechaza porque el acceso público está deshabilitado en el recurso.

La causa típica es un proxy del sistema que resuelve el DNS fuera del túnel de tu VPN. Tu estación de trabajo resuelve el nombre de host de Azure OpenAI a la IP privada mediante Azure Private DNS, pero el servidor proxy usa su propio resolvedor, llega a la IP pública y la solicitud es rechazada.

Para confirmar que el DNS de tu estación de trabajo se resuelve correctamente:

```text
nslookup yourresource.openai.azure.com
```

Un resultado que apunte a un rango de direcciones IP privadas (por ejemplo, `10.x.x.x`) confirma que tu estación de trabajo está configurada correctamente y que el problema está en la ruta del proxy.

Opciones para resolverlo:

- Agrega el nombre de host de Azure OpenAI a la lista de exclusión en **Herramientas > Preferencias > Configuración del proxy** para que la solicitud omita el proxy y vaya directamente por el túnel de la VPN. Separa varios nombres de host con punto y coma
- Pide a tu equipo de red que actualice el archivo PAC del proxy para omitir `*.openai.azure.com`, o que configure el servidor proxy para resolver las zonas de Azure Private DNS
- Usa el split tunneling para que los rangos de IP de los puntos de conexión privados de Azure se enruten directamente en lugar de pasar por el proxy

Consulta @proxy-settings para la configuración general del proxy en Tabular Editor.

## Errores de conexión SSL

Si el **punto de conexión del servicio** usa el alias `privatelink` (por ejemplo, `https://your-resource.privatelink.openai.azure.com`), la validación SSL falla porque el certificado de Azure OpenAI se emite para `*.openai.azure.com`, no para `*.privatelink.openai.azure.com`.

Usa el nombre de host estándar del recurso en el campo del punto de conexión del servicio y deja que el DNS lo resuelva a la IP privada:

```text
https://your-resource.openai.azure.com
```

## "Error al obtener la respuesta de la IA" con 404 o DeploymentNotFound

El valor del campo **Nombre del modelo** no coincide con ninguna implementación de tu recurso de Azure OpenAI. Azure OpenAI requiere el **nombre de la implementación** en cada llamada a la API, no el nombre del modelo subyacente ni el nombre del recurso.

Verifica el nombre de la implementación:

1. Inicia sesión en el [portal de Azure AI Foundry](https://ai.azure.com) y selecciona tu recurso
2. Abre **Implementaciones** (o **Modelos + puntos de conexión** si el recurso se ha actualizado a Foundry)
3. Copia el valor de la columna **Nombre**

Es posible que las implementaciones creadas antes de que tu organización adoptara Azure AI Foundry no aparezcan en el portal. Enuméralas desde la CLI de Azure:

```bash
az cognitiveservices account deployment list --name "<resource-name>" --resource-group "<resource-group>" --output table
```

El campo de nombre del modelo distingue entre mayúsculas y minúsculas.
