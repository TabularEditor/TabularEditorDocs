---
uid: locale-not-supported
title: 区域设置不受支持
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

# 区域设置不受支持

你可能会看到以下任一条警告信息：

```plaintext
The XXXX locale is not supported
```

```plaintext
XXXX is an invalid culture identifier
```

在 Tabular Editor 3 的“信息视图”中。

![“区域设置不受支持”信息](~/content/assets/images/troubleshooting/locale-not-supported-message-view.png)

当你的本地计算机使用 **Analysis Services (SSAS) 引擎不支持的区域设置** 时，通常会出现此问题。  
大多数情况下，这个错误是由其他潜在问题或警告触发的，因此才会显示这条信息。

---

## 场景与解决方案

### 1. 连接到本地 SSAS 实例

如果你是在本机本地运行 SQL Server Analysis Services (SSAS)：

- **解决方案：** 更改 SSAS 实例使用的 **服务账户**。  
  更新账户通常可以解决因区域设置不受支持而导致的不匹配问题。

---

### 2. 连接到远程 SSAS、Azure AS 或 Power BI

连接到远程实例时，有两种可行的解决方案：

#### 方案 A：在连接字符串中指定区域设置

在连接字符串中添加 `LocaleIdentifier=1033`，以显式设置受支持的区域设置 (例如英语 – 1033)。

**示例（Azure AS）：**

```plaintext
Data Source=asazure://westeurope.asazure.windows.net/instance-name;LocaleIdentifier=1033
```

#### 方案 B：更改本机的区域设置

调整你本地系统的区域和语言设置，使其与受支持的区域设置一致。

- **建议设置：**
  - \*\*区域格式：\*\*英语（美国）
  - \*\*Windows 显示语言：\*\*英语（美国）