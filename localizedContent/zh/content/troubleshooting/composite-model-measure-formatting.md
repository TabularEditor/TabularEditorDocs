---
uid: composite-model-measure-formatting
title: 复合模型中的度量值格式属性
author: 支持团队
updated: 2026-01-26
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

# 复合模型中的度量值格式属性

在使用通过实时连接连接到 Analysis Services (SSAS/AAS) 的复合模型时，你在编辑度量值的格式属性时可能会遇到验证错误，或出现令人困惑的行为。 常见的错误信息是：

**"度量值不允许同时具有 FormatString 和 Format Expression。"**

本文将说明原因，并介绍如何解决。

---

## 了解问题

复合模型通过实时连接，将本地 Power BI 表与 SSAS/AAS 语义模型中的远程表组合在一起。 在这种架构下，度量值的格式设置可能会产生歧义：

- **FormatString**：静态格式定义（例如，用于货币的“0.00”）。
- **格式字符串表达式**：在查询时计算的动态格式字符串。

之所以会报错，是因为模型最终同时包含了静态格式和动态格式表达式——这种状态不被 Tabular Object Model（TOM）允许。

### 为什么会这样

在复合模型中：

1. **所有权模糊**：远程度量值归远程 SSAS/AAS 模型所有。 当你在 Tabular Editor 中编辑格式设置时，可能是在试图覆盖远程元数据，从而产生冲突。

2. **元数据同步**：当度量值上存在格式字符串表达式时，FormatString 通常会显示为“自定义”，用来表示已启用动态格式。 如果你随后又尝试同时设置静态的 FormatString，这两个属性都会被填充，从而触发验证错误。

3. **持久化限制**：对远程度量值元数据的更改可能无法可靠地保存，因为远程模型保留最终控制权。 这会让本地复合模型处于不一致的状态。

---

## 根本原因

### 远程度量值格式设置

如果问题度量值是在远程 SSAS/AAS 模型中定义的：

- 格式应在源模型中管理，而不是在 Power BI 复合模型中管理。
- 尝试在 Power BI 中覆盖远程度量值格式，可能会导致 FormatString 和 Format String Expression 同时被填充，从而引发验证错误。

### 脚本或自动化同时设置两个属性

- 如果您使用 C# 脚本、Power Query 转换或 BPA 规则来应用格式，请确保每个度量值只采用一种方式（静态或动态二选一，不要同时使用）。

### 带格式表达式的计算组

- 计算组可以定义格式字符串表达式，用于覆盖度量值格式。 如果某个计算项的格式表达式处于生效状态，UI 可能仍会显示度量值的静态 FormatString，从而看起来像是两者都已设置。

### 版本或环境限制

- 度量值的动态格式字符串支持范围有限，在某些 Power BI 版本或部署模式（Report Server）下可能无法获得完全支持。
- 如果您使用的是 2025 年之前的 Power BI Desktop，或 2025 年一月之前的 Power BI Report Server，则可能不支持度量值的动态格式。

---

## 解决方案

解决方案取决于度量值是**远程**（来自 SSAS/AAS）还是**本地**（在复合模型中创建）。

### 如果度量值是远程的（来自 SSAS/AAS）

这是最常见的场景。 远程度量值归源语义模型所有。

**推荐做法：**

1. **在源模型中管理格式。** 用 SQL Server Management Studio 打开 SSAS/AAS，或使用连接到源模型的 Tabular Editor，然后在其中设置格式。

2. **如需 Report 专属格式，** 请在 Power BI 复合模型中创建一个本地“包装器”度量值：

   - 在本地模型中新建一个度量值，用来引用远程度量值。
   - 为包装器度量值应用所需的格式字符串。
   - 在 Report 中使用包装器度量值，而不是远程度量值。

   **取舍：** 这种方式会产生重复对象并增加维护成本，但在实时连接场景下，这是应用 Report 专属格式最可靠的方法。

### 如果该度量值是本地的（在复合模型中创建）

**静态格式（最常见）：**

1. 在 Tabular Editor 中选择该度量值。
2. 清空 **格式字符串表达式** 字段（设为空/null）。
3. 将该度量值的 **格式字符串** 设置为所需的静态格式（例如，百分比用 `"0.00%"`，货币用 `"$#,##0.00"`）。
4. 保存模型。

**动态格式：**

1. 选择该度量值。
2. 保留或将 **格式字符串表达式** 设置为你需要的 DAX 表达式（这是你唯一应该使用的格式设置属性）。
3. 将 **格式字符串** 保持为“Custom”（不要同时再设置静态格式字符串）。
4. 确认你的环境支持动态格式字符串（Power BI Desktop 2025 或更高版本，或 Power BI Report Server 2025 年一月及以后版本）。

---

## 快速故障排查清单

- [ ] **确定度量值归属**：该度量值是远程的（SSAS/AAS）还是本地的（复合模型）？
- [ ] **检查格式字符串表达式**：即使你没设置，也要确认它是否已被填充。 在属性网格中，查找非空的“格式字符串表达式”字段。
- [ ] **检查脚本和规则**：如果你使用 C# Script 或 BPA 规则来设置度量值格式，确保它们不会在同一次执行中同时设置 FormatString 和 格式字符串表达式。
- [ ] **检查计算组**：确认是否有任何计算组项定义了格式字符串表达式，可能会覆盖或与该度量值的格式冲突。
- [ ] **确认环境版本**：确认你的 Power BI Desktop（2025 或更高版本）或 Power BI Report Server（2025 年一月及以后版本）的版本，尤其是在使用动态格式时。

---

## 分步示例

### 示例 1：修复采用静态格式的远程度量值

**场景：** 你在远程 SSAS 模型中有一个“Sales Amount”度量值，并希望在 Power BI Report 中将其格式化为货币。

**步骤：**

1. 在 Tabular Editor 中，直接连接到 SSAS/AAS 模型（不要连接到 Power BI 复合模型）。
2. 找到“Sales Amount”度量值。
3. 将其 **格式字符串** 设置为 `"$#,##0.00"`。
4. 将模型保存回 SSAS/AAS。
5. 返回到已连接 Power BI 复合模型的 Tabular Editor；此时格式应已继承。

如果 Report 中的格式仍显示不正确，请创建一个本地包装度量值（见下文）。

### 示例 2：创建用于 Report 专用格式的包装度量值

**场景：** 需要在此特定 Report 中以不同格式显示来自 SSAS 的 Sales Amount 度量值。

**步骤：**

1. 在 Tabular Editor 中连接到 Power BI 复合模型。
2. 在本地表中创建一个新度量值（如果有度量值表，则在该表中创建）：
   ```
   Sales Amount (Formatted) = [Sales Amount]
   ```
3. 将新度量值的 **格式字符串** 设置为所需格式（例如 `"$#,##0.00"`）。
4. 保存模型。
5. 更新 Report 中的 Visual，使其使用包装度量值，而不是原始的远程度量值。

### 示例 3：为本地度量值设置动态格式

**场景：** 你在复合模型中有一个本地度量值，并希望根据阈值应用条件格式。

**步骤：**

1. 在 Tabular Editor 中选择该度量值。
2. 确保 **格式字符串** 为空（不要设置静态格式）。
3. 将 **格式字符串表达式** 设置为你的条件表达式：
   ```dax
   IF(
       [YourMeasure] > 1000,
       "#,##0.00",
       "0.00"
   )
   ```
4. 也**不要**再设置静态的格式字符串。
5. 保存模型。
6. 确认你的 Power BI 版本支持动态格式字符串（Power BI Desktop 2025+ 或 PBIRS 2025 年一月+）。

---

## 预防最佳实践

1. **尽早确定格式策略**：决定每个度量值要用静态格式还是动态格式，并且每个度量值只选一种方式并保持一致。

2. **检查远程度量值**：在复合模型中编辑格式之前，先确认该度量值是否为远程度量值。 如果是这样，就在源 SSAS/AAS 模型中管理格式设置。

3. **使用与版本相匹配的功能**：如果你使用动态格式字符串，请确保所有相关环境（Power BI Desktop、Report Server、Analysis Services）都支持你所用的 Power BI 版本中的该功能。

4. **以防御性方式编写脚本**：如果你编写 C# Script 或 BPA 规则来格式化度量值，请将逻辑拆分开，确保每个度量值只设置一个格式相关属性，并加入防护检查，先确认另一个属性是否已填写。

5. **切换为静态格式时清除格式字符串表达式**：如果某个度量值之前使用了动态格式，在尝试设置静态 FormatString 之前，务必先清除格式字符串表达式。

---

## 更多资源

- **[Microsoft Docs - 度量值格式字符串](https://learn.microsoft.com/en-us/analysis-services/tmsl/measures-object-tmsl)**：关于在 Tabular Object Model 中进行度量值格式设置的官方文档。
- **[Power BI 中的复合模型](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-composite-models)**：了解实时连接与复合模型架构。
- **[动态格式字符串](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-dynamic-format-strings)**：功能可用性及使用指南。

---

## 仍需要帮助？

如果以上步骤仍未解决你的问题：

1. **确认度量值是否为本地度量值**：在 Tabular Editor 中直接连接你的 Power BI 文件（.pbix），确认该度量值是在本地定义的，而不是远程定义的。

2. **导出诊断信息**：运行下面的 Tabular Editor 脚本以审核所有度量值：
   ```csharp
   var measures = Model.AllMeasures;
   foreach (var m in measures)
   {
       var hasStaticFormat = !string.IsNullOrEmpty(m.FormatString);
       var hasDynamicFormat = !string.IsNullOrEmpty(m.FormatStringExpression);
       if (hasStaticFormat && hasDynamicFormat)
       {
           Output($"CONFLICT - {m.Name}: FormatString='{m.FormatString}', Expression='{m.FormatStringExpression}'");
       }
       else if (hasStaticFormat)
       {
           Output($"STATIC - {m.Name}: '{m.FormatString}'");
       }
       else if (hasDynamicFormat)
       {
           Output($"DYNAMIC - {m.Name}: '{m.FormatStringExpression}'");
       }
   }
   ```

3. **联系支持**：提供诊断输出结果，以及你的 Power BI 和 Tabular Editor 版本号。
