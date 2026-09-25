---
uid: update-compatibility-level
title: 更新兼容级别
author: Morten Lønskov
updated: 2026-09-14
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

模型的 **兼容级别** 决定你可以使用哪些 Tabular Object Model (TOM) 功能。 When Microsoft introduces new capabilities, like custom calendars or DAX user-defined functions, they're often gated behind a newer compatibility level. You'll need to upgrade before these features appear in Tabular Editor.

> [!WARNING]
> 兼容性升级是不可逆的。你可以升级，但无法可靠地降级。 Treat this like a schema upgrade and validate your deployment targets first.

## 兼容级别与兼容模式

兼容级别和兼容模式是两个独立的属性，用途不同：

| 属性                            | 控制内容                            | 值                                                                      |
| ----------------------------- | ------------------------------- | ---------------------------------------------------------------------- |
| `Database.CompatibilityLevel` | 可用的 TOM 功能（例如自定义日历、DAX UDF 等）   | `1200`, `1400`, `1500`, `1600`, `1700`, `1701`, `1702`, `1705`, `1706` |
| `Database.CompatibilityMode`  | 模型面向的平台、可用的 TOM 对象和属性，以及适用的版本限制 | `Unknown`、`AnalysisServices`、`PowerBI`、`Excel`                         |

如果你需要更改目标平台，而不是解锁新的 TOM 功能，请参阅[更改兼容模式](xref:change-compatibility-mode)。

## 何时升级

在以下情况下升级：

- Power BI Desktop 中有某个功能，但在 Tabular Editor 中缺少对应的 TOM 属性
- You need newly introduced capabilities like **custom calendars** (1701+), **DAX user-defined functions** (1702+), **user-context calculated columns** (1705+) or **String Indexing Behavior** (1706+)
- 你正在跨环境统一开发标准，并希望各环境的最低功能集保持一致

## 开始之前

### 备份你的模型

因为升级不可逆：

- 备份模型元数据（最好连同整个项目一起备份）
- 在进行任何更改之前，先在源代码管理中创建一个干净的 commit

### 确认目标端支持情况

Compatibility level support differs by platform (SSAS, Azure Analysis Services, Fabric/Power BI Premium). If your deployment target doesn't support the selected level, you'll be blocked from deploying. 请参阅 [Analysis Services 中表格模型的兼容级别](https://learn.microsoft.com/en-us/analysis-services/tabular-models/compatibility-level-for-tabular-models-in-analysis-services)

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

- **Calculation groups:** 1500+
- **自定义日历：** 1701+
- **DAX UDFs：** 1702+
- **User-context calculated columns** (the column's _Expression Context_ property): 1705+
- **String Indexing Behavior** on a column: 1706+

> [!NOTE]
> Minimum required levels for features can change as the platform evolves. Always verify prerequisites in current documentation. 某些级别/功能仅适用于 Power BI，在 SSAS/AAS 上可能不可用。

### 保存

保存模型以应用更改：

- 如果连接到远程模型，保存会将元数据更改回写到服务器
- 如果编辑的是基于文件的模型，保存会更新磁盘上的元数据

保存后，Tabular Editor 会显示新启用的对象和属性。

## 选择合适的级别

### 适用于 SSAS/AAS 部署

选择[服务器版本所支持的最新兼容级别](https://learn.microsoft.com/en-us/analysis-services/tabular-models/compatibility-level-for-tabular-models-in-analysis-services)

### 适用于 Power BI Desktop

Query your Power BI Desktop engine to see which compatibility levels it supports. 使用 [DAX Studio 或 DAX 查询视图](https://www.sqlbi.com/blog/marco/2024/03/10/compatibility-levels-and-engine-supported-by-power-bi-desktop/)：

```sql
SELECT * FROM $SYSTEM.DISCOVER_PROPERTIES
WHERE [PropertyName] = 'ProviderVersion'
   OR [PropertyName] = 'DBMSVersion'
   OR [PropertyName] = 'SupportedCompatibilityLevels'
```

## 故障排查

### 升级后无法部署到 SSAS/AAS

你可能选择了目标服务器不支持的兼容级别。 Validate server support before upgrading.

**参考：** [Analysis Services 中表格模型的兼容级别](https://learn.microsoft.com/en-us/analysis-services/tabular-models/compatibility-level-for-tabular-models-in-analysis-services)

### 我可以降级吗？

No. Downgrades aren't supported and aren't a safe or reliable remediation strategy.

## 验证

更新并保存后：

- 确认 Tabular Editor 中的 **数据库 → 兼容级别** 已反映新值
- 验证预期功能是否已显示（例如，兼容级别达到 1702 及以上时，**Functions** 节点将可用）
- 如果部署目标为 SSAS/AAS，请根据服务器支持的兼容级别验证部署是否可行