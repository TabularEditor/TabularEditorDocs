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

你可能会看到以下警告信息：

```plaintext
不支持 XXXX 区域设置
```

在 Tabular Editor 3 的“信息视图”中。

![区域设置不受支持信息](~/content/assets/images/troubleshooting/locale-not-supported-message-view.png)

当你的本地计算机使用 **Analysis Services (SSAS) 引擎不支持的区域设置** 时，通常会出现此问题。  
在大多数情况下，该错误由其他潜在问题或警告触发，但最终会表现为这条信息。  
在大多数情况下，该错误由其他潜在问题或警告触发，但最终会表现为这条信息。

---

## 场景与解决方案

### 1。 1。 连接到本地 SSAS 实例

如果你在本地计算机上运行 SQL Server Analysis Services (SSAS)：

- **解决方案：** 更改 SSAS 实例使用的 **服务账户**。  
  更新该账户通常可以解决由于区域设置不受支持而导致的不匹配问题。  
  更新该账户通常可以解决由于区域设置不受支持而导致的不匹配问题。

---

### 2。 2。 连接到远程 SSAS、Azure AS 或 Power BI

连接到远程实例时，有两种可行的解决方案：

#### 选项 A：在连接字符串中指定区域设置

在连接字符串中添加 `LocaleIdentifier=1033`，即可显式设置受支持的区域设置(例如：英语 – 1033)。

**示例（Azure AS）：**

```plaintext
数据源=asazure://westeurope.asazure.windows.net/instance-name;LocaleIdentifier=1033
```

#### 选项 B：更改计算机上的区域设置

将本地系统的区域和语言设置调整为受支持的区域设置。

- **推荐设置：**
  - **区域格式：** 英语（美国）
  - **Windows 显示语言：** 英语（美国）