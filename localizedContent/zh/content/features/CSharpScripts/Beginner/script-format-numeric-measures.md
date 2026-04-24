---
uid: script-format-numeric-measures
title: 格式化数值度量值
author: Morten Lønskov
updated: 2023-11-29
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---

# 格式化数值度量值

## 脚本用途

可让你快速为所选度量值设置默认格式字符串。

<br></br>

> [!NOTE]
> 该脚本采用了一些命名规范，因此你可能需要根据自己的规范进行调整。 <br></br> <br></br>

## 脚本

### 脚本标题

```csharp
// This script is meant to format all measures with a default formatstring
foreach (var ms in Selected.Measures) {
//Don't set format string on hidden measures
	if (ms.IsHidden) continue;
// If the format string is empty continue. 
	if (!string.IsNullOrWhiteSpace(ms.FormatString)) continue;
//If the data type is int set a whole number format string
	if (ms.DataType == DataType.Int64) ms.FormatString = "#,##0";
//If the datatype is double or decimal 
	if (ms.DataType == DataType.Double || ms.DataType == DataType.Decimal) {
    //and the name contains # or QTY then set the format string to a whole number
		if (ms.Name.Contains("#")
			|| ms.Name.IndexOf("QTY", StringComparison.OrdinalIgnoreCase) >= 0) ms.FormatString = "#,##0";
		//otherwise set it a decimal format string. 
    else ms.FormatString = "#,##0.00";
	}
}
```

### 说明

该脚本会遍历所选的每个度量值，并根据不同条件设置默认格式字符串。