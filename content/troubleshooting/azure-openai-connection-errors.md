---
uid: azure-openai-connection-errors
title: Azure OpenAI connection errors
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

# Azure OpenAI connection errors

This page covers common connection failures when using Azure OpenAI as the provider for the @ai-assistant. See the [Azure OpenAI configuration section](xref:ai-assistant#azure-openai) for setup details.

## 403 "Public access is disabled. Please configure private endpoint"

This 403 comes from Azure OpenAI itself, which means the HTTP request reached the public endpoint rather than your private endpoint. Azure rejects it because public access is disabled on the resource.

The typical cause is a system proxy that resolves DNS outside your VPN tunnel. Your workstation resolves the Azure OpenAI hostname to the private IP via Azure Private DNS, but the proxy server uses its own resolver, reaches the public IP, and gets rejected.

To confirm DNS on your workstation is resolving correctly:

```text
nslookup yourresource.openai.azure.com
```

A result pointing to a private IP range (for example `10.x.x.x`) confirms that your workstation side is correct and that the issue is on the proxy path.

Options to resolve:

- Add your Azure OpenAI hostname to the bypass list under **Tools > Preferences > Proxy Settings** so the request skips the proxy and goes directly through the VPN tunnel. Separate multiple hostnames with semicolons
- Ask your network team to update the proxy PAC file to bypass `*.openai.azure.com`, or to configure the proxy server to resolve Azure Private DNS zones
- Use split tunneling so Azure private endpoint IP ranges route directly rather than via the proxy

See @proxy-settings for general Tabular Editor proxy configuration.

## SSL connection errors

If the **Service endpoint** uses the `privatelink` alias (for example `https://your-resource.privatelink.openai.azure.com`), SSL validation fails because the Azure OpenAI certificate is issued for `*.openai.azure.com`, not `*.privatelink.openai.azure.com`.

Use the standard resource hostname in the service endpoint field and let DNS resolve it to the private IP:

```text
https://your-resource.openai.azure.com
```

## "Error getting AI response" with 404 or DeploymentNotFound

The value in the **Model name** field does not match a deployment in your Azure OpenAI resource. Azure OpenAI requires the **deployment name** in every API call, not the underlying model name and not the resource name.

Verify the deployment name:

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com) and select your resource
2. Open **Deployments** (or **Models + endpoints** if the resource has been upgraded to Foundry)
3. Copy the value from the **Name** column

Deployments created before your organization adopted Azure AI Foundry may not appear in the portal. List them from the Azure CLI:

```bash
az cognitiveservices account deployment list --name "<resource-name>" --resource-group "<resource-group>" --output table
```

The model name field is case-sensitive.
