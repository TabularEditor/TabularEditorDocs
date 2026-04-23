---
uid: azure-openai-connection-errors
title: Azure OpenAI 连接错误
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

# Azure OpenAI 连接错误

本页介绍将 Azure OpenAI 用作 @ai-assistant 提供程序时常见的连接失败问题。 设置详情请参阅[Azure OpenAI 配置部分](xref:ai-assistant#azure-openai)。

## 403 "公共访问已禁用。 请配置专用终结点"

此 403 错误来自 Azure OpenAI 本身，说明 HTTP 请求到达了公共终结点，而非你的专用终结点。 Azure 会拒绝该请求，因为此资源已禁用公共访问。

常见原因是系统代理在 VPN 隧道之外解析 DNS。 你的工作站通过 Azure Private DNS 将 Azure OpenAI 主机名解析为专用 IP，但代理服务器使用自己的解析器，访问到公共 IP，因此被拒绝。

要确认工作站上的 DNS 解析是否正确：

```text
nslookup yourresource.openai.azure.com
```

如果结果指向专用 IP 范围（例如 `10.x.x.x`），则说明工作站这一侧是正确的，问题出在代理路径上。

可用的解决办法：

- 在 **工具 > 偏好设置 > 代理设置** 中，将你的 Azure OpenAI 主机名添加到绕过列表，让请求跳过代理并直接通过 VPN 隧道发送。 多个主机名用分号分隔
- 让网络团队更新代理 PAC 文件，绕过 `*.openai.azure.com`；或者把代理服务器配置为能够解析 Azure Private DNS 区域
- 使用拆分隧道，使 Azure 专用终结点的 IP 范围直接路由，而不是经过代理

有关 Tabular Editor 的通用代理配置，请参阅 @proxy-settings。

## SSL 连接错误

如果 **服务终结点** 使用 `privatelink` 别名（例如 `https://your-resource.privatelink.openai.azure.com`），SSL 验证会失败，因为 Azure OpenAI 证书签发给的是 `*.openai.azure.com`，而不是 `*.privatelink.openai.azure.com`。

在服务终结点字段中使用标准资源主机名，并让 DNS 将其解析为专用 IP：

```text
https://your-resource.openai.azure.com
```

## "获取 AI 响应时出错"，出现 404 或 DeploymentNotFound

**模型名称** 字段中的值与 Azure OpenAI 资源中的任何部署都不匹配。 Azure OpenAI 要求在每次 API 调用中使用 **部署名称**，而不是底层模型名称，也不是资源名称。

确认部署名称：

1. 登录到 [Azure AI Foundry 门户](https://ai.azure.com) 并选择你的资源
2. 打开 **部署**（如果资源已升级到 Foundry，则为 **模型 + 终结点**）
3. 复制 **名称** 列中的值

在你的组织采用 Azure AI Foundry 之前创建的部署，可能不会显示在门户中。 使用 Azure CLI 列出这些部署：

```bash
az cognitiveservices account deployment list --name "<resource-name>" --resource-group "<resource-group>" --output table
```

“模型名称”字段区分大小写。
