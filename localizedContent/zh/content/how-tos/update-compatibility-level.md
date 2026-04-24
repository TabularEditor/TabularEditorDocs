---
uid: update-compatibility-level
title: 更新兼容级别
author: Morten Lønskov
updated: 2026-01-12
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 更新兼容级别

模型的 **兼容级别** 决定你可以使用哪些 Tabular Object Model (TOM) 功能。 当 Microsoft 引入自定义日历或 DAX 用户定义函数等新功能时，这些功能通常需要在较新的兼容级别下才会开放。 你需要先升级，这些功能才会出现在 Tabular Editor 中。 当 Microsoft 引入自定义日历或 DAX 用户定义函数等新功能时，这些功能通常需要在较新的兼容级别下才会开放。 你需要先升级，这些功能才会出现在 Tabular Editor 中。

> [!WARNING]
> 兼容级别升级是不可逆的。 不能。 不支持降级，而且这也不是安全或可靠的补救措施。 将其视为一次架构升级，并先验证你的部署目标。

## 兼容级别与兼容模式

兼容级别和兼容模式是两个独立的属性，用途不同：

| 属性                            | 控制内容                            | 值                                              |
| ----------------------------- | ------------------------------- | ---------------------------------------------- |
| `Database.CompatibilityLevel` | 可用的 TOM 功能（例如自定义日历、DAX UDF 等）   | `1200`、`1500`、`1600`、`1701`、`1702` 等。          |
| `Database.CompatibilityMode`  | 模型面向的平台、可用的 TOM 对象和属性，以及适用的版本限制 | `Unknown`、`AnalysisServices`、`PowerBI`、`Excel` |

如果你需要更改目标平台，而不是解锁新的 TOM 功能，请参阅[更改兼容模式](xref:change-compatibility-mode)。

## 何时升级

在以下情况下升级：

- Power BI Desktop 中有某个功能，但在 Tabular Editor 中缺少对应的 TOM 属性
- 你需要新引入的功能，例如 **自定义日历**（1701+）或 **DAX 用户定义函数**（1702+）
- 你正在跨环境统一开发标准，并希望各环境的最低功能集保持一致

## 开始之前

### 备份你的模型

因为升级不可逆：

- 备份模型元数据（最好连同整个项目一起备份）
- 在进行任何更改之前，先在源代码管理中创建一个干净的 commit

### 确认目标端支持情况

不同平台（SSAS、Azure Analysis Services、Fabric/Power BI Premium）对兼容级别的支持情况不同。 如果你的部署目标不支持所选级别，将无法部署。 不同平台（SSAS、Azure Analysis Services、Fabric/Power BI Premium）对兼容级别的支持情况不同。 如果你的部署目标不支持所选级别，将无法部署。 请参阅 [Analysis Services 中表格模型的兼容级别](https://learn.microsoft.com/en-us/analysis-services/tabular-models/compatibility-level-for-tabular-models-in-analysis-services)

## 更新兼容级别

![更新兼容级别](~/content/assets/images/how-to/updatecompatabilitylevel.gif)

### 打开模型

使用以下任一方式在 Tabular Editor 中打开你的模型：

- 打开基于文件的模型定义（`.bim` 文件）
- 连接到正在运行的模型（通过 XMLA endpoint 连接到 SSAS/AAS/Power BI 语义模型）

### 选择模型根节点

在 **TOM Explorer** 中，选择顶层的 **Model**（根节点）。

### 找到兼容级别

在 **Properties** 面板中：

1. 展开 **Database**
2. 找到 **兼容级别**

### 设置新的级别

将兼容级别设置为所需功能的最低级别（或平台支持的最高级别）。

示例：

- **自定义日历：** 1701+
- **DAX UDFs：** 1702+

> [!NOTE]
> 随着平台演进，某些功能所需的最低级别可能会发生变化。 始终在最新文档中核对前置条件。 [!NOTE]
> 随着平台演进，某些功能所需的最低级别可能会发生变化。 始终在最新文档中核对前置条件。 某些级别/功能仅适用于 Power BI，在 SSAS/AAS 上可能不可用。

### 保存

保存模型以应用更改：

- 如果连接到远程模型，保存会将元数据更改回写到服务器
- 如果编辑的是基于文件的模型，保存会更新磁盘上的元数据

保存后，Tabular Editor 会显示新启用的对象和属性。

## 选择合适的级别

### 适用于 SSAS/AAS 部署

选择[服务器版本所支持的最新兼容级别](https://learn.microsoft.com/en-us/analysis-services/tabular-models/compatibility-level-for-tabular-models-in-analysis-services)

### 适用于 Power BI Desktop

查询 Power BI Desktop 引擎，查看它支持哪些兼容级别。 查询 Power BI Desktop 引擎，查看它支持哪些兼容级别。 使用 [DAX Studio 或 DAX 查询视图](https://www.sqlbi.com/blog/marco/2024/03/10/compatibility-levels-and-engine-supported-by-power-bi-desktop/)：

```sql
SELECT * FROM $SYSTEM.DISCOVER_PROPERTIES
WHERE [PropertyName] = 'ProviderVersion'
   OR [PropertyName] = 'DBMSVersion'
   OR [PropertyName] = 'SupportedCompatibilityLevels'
```

## 故障排查

### 升级后无法部署到 SSAS/AAS

你可能选择了目标服务器不支持的兼容级别。 升级前先确认目标服务器是否支持。 升级前先确认目标服务器是否支持。

**参考：** [Analysis Services 中表格模型的兼容级别](https://learn.microsoft.com/en-us/analysis-services/tabular-models/compatibility-level-for-tabular-models-in-analysis-services)

### 我可以降级吗？

不能。 不支持降级，而且这也不是安全或可靠的补救措施。

## 验证

更新并保存后：

- 确认 Tabular Editor 中的 **数据库 → 兼容级别** 已反映新值
- 验证预期功能是否已显示（例如，兼容级别达到 1702 及以上时，**Functions** 节点将可用）
- 如果部署目标为 SSAS/AAS，请根据服务器支持的兼容级别验证部署是否可行