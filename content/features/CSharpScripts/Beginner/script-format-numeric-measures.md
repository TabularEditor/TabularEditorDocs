---
uid: script-format-numeric-measures
title: Format Numeric Measures
author: Morten Lønskov
updated: 2023-11-29
applies_to:
  products:
    - product: TE2
      none: true
    - product: TE3
      full: true
---
# Format Numeric Measures

## Script Purpose
Allows you to quickly set default format strings on the measures selected. 

<br></br>
> [!NOTE] 
> The script uses certain naming standards so you might wish to adjust it to suit yours. 
<br></br>

## Script

### Script Title
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
### Explanation
The script takes each of the selected measures and loops through them to set a default format string according to various conditions. 