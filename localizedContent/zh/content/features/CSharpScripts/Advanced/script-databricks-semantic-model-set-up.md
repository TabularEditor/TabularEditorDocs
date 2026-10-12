---
uid: script-databricks-semantic-model-set-up
title: Databricks 语义模型设置
author: Johnny Winter
updated: 2025-09-04
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Databricks 语义模型设置

## 脚本用途

该脚本作为 Tabular Editor x Databricks 系列的一部分编写。在 Databricks Unity Catalog 中，表名不能使用大写字母。在不使用大写字母的前提下，让表名更易读的一种常见做法是采用 snake_case。另外，虽然列名可以包含空格，但通常不建议这样做，因为用起来很麻烦；因此数据工程师多半会使用 snake_case、camelCase 或 PascalCase。

不过，我们希望语义模型的用户在模型中看到业务友好的名称。

下面的脚本会遍历模型中的所有表，并确保应用友好的 Proper Case 格式。

在此过程中，它还会遵循一些最佳实践建议：将所有列的默认汇总方式设为“无”，并为所有 DateTime 类型字段设置格式字符串（脚本当前使用格式 'yyyy-mm-dd'；如果你更偏好其他格式，可在第 61 行修改脚本） <br></br>

> [!NOTE]
> 此脚本并非仅供 Databricks 使用——你可以把它用于任何你喜欢的模型，不管数据源是什么；只是它在设计时考虑了 Databricks 的一些限制。 <br></br>

## 脚本

### Databricks 语义模型设置

```csharp
/*
 * Title: Databricks Semantic Model Set-Up
 * Author: Johnny Winter, greyskullanalytics.com
 *
 *  This script, when executed, will loop through all tables and columns in the model and rename with friendly names. 
 *  Names in snake_case, camelCase or PascalCase will all be converted to Proper Case.
 *  No table selections are required as all tables in the model will be processed, simply run the script.
 *  Whilst looping though columns it also sets default summarization to none and sets a format string for all DateTime type fields 
 *  (currently it sets format 'yyyy-mm-dd' but you can change this on line 61 if you wish).
 *
 */
using System;
using System.Globalization;

//create script as class so it can be reused 
class p {

    public static void ConvertCase(dynamic obj)
    {
        TextInfo textInfo = CultureInfo.CurrentCulture.TextInfo;
        //replace underscores with a space
        var oldName = obj.Name.Replace("_", " ");
        var newName = new System.Text.StringBuilder();
        for(int i = 0; i < oldName.Length; i++) {
            // First letter should always be capitalized:
            if(i == 0) newName.Append(Char.ToUpper(oldName[i]));

            // A sequence of two uppercase letters followed by a lowercase letter should have a space inserted
            // after the first letter:
            else if(i + 2 < oldName.Length && char.IsLower(oldName[i + 2]) && char.IsUpper(oldName[i + 1]) && char.IsUpper(oldName[i]))
            {
                newName.Append(oldName[i]);
                newName.Append(" ");
            }

            // All other sequences of a lowercase letter followed by an uppercase letter, should have a space
            // inserted after the first letter:
            else if(i + 1 < oldName.Length && char.IsLower(oldName[i]) && char.IsUpper(oldName[i+1]))
            {
                newName.Append(oldName[i]);
                newName.Append(" ");
            }
            else
            {
                newName.Append(oldName[i]);
            }
        }
        //apply Proper Case where this has not already been taken care of above
        obj.Name = textInfo.ToTitleCase(newName.ToString());
    }
}

foreach(var t in Model.Tables) {
//convert table names
    p.ConvertCase(t);
//convert column names
    foreach(var c in t.Columns) {
        p.ConvertCase(c);
        c.SummarizeBy = AggregateFunction.None;
        if (c.DataType == DataType.DateTime)
        {c.FormatString = "yyyy-mm-dd";}
    }
}
```

### 说明

此脚本执行后，会遍历模型中的所有表和列，并将其重命名为更友好的名称。以 snake_case、camelCase 或 PascalCase 命名的名称都会转换为 Proper Case。无需选择表，因为会处理模型中的所有表；直接运行脚本即可。在遍历列的同时，它还会将默认汇总设置为“无”，并为所有 DateTime 类型字段设置格式字符串。

