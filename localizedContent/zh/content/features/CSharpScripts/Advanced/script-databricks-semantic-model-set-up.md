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

此脚本作为 Tabular Editor x Databricks 系列的一部分创建。 在 Databricks Unity Catalog 中，表名不能使用大写字母。 在不使用大写字母的前提下，让表名更易读的一种常见做法是采用 snake_case。 另外，虽然列名可以包含空格，但通常不建议这样做，因为用起来很麻烦；因此数据工程师多半会使用 snake_case、camelCase 或 PascalCase。

不过，我们希望语义模型的用户在模型中看到业务友好的名称。

下面的脚本会遍历模型中的所有表，并确保应用友好的 Proper Case 格式。

在此过程中，它还会遵循一些最佳实践建议：将所有列的默认汇总方式设为“无”，并为所有 DateTime 类型字段设置格式字符串（脚本当前使用格式 'yyyy-mm-dd'；如果你更偏好其他格式，可在第 61 行修改脚本） <br></br>

> [!NOTE]
> 此脚本并非仅供 Databricks 使用——你可以把它用于任何你喜欢的模型，不管数据源是什么；只是它在设计时考虑了 Databricks 的一些限制。 <br></br>

## 脚本

### Databricks 语义模型设置

```csharp
/*
 * Title: Databricks 语义模型设置
 * Author: Johnny Winter, greyskullanalytics.com
 *
 *  此脚本执行后，将遍历模型中的所有表和列，并将其重命名为更友好的名称。
 *  采用 snake_case、camelCase 或 PascalCase 的名称都会转换为 Proper Case。
 *  无需选择表，因为会处理模型中的所有表；只需运行脚本即可。
 *  在遍历列的同时，还会将默认汇总设置为 none，并为所有 DateTime 类型字段设置格式字符串
 *  (目前设置的格式为 'yyyy-mm-dd'，如有需要可在第 61 行更改)。
 *
 */
using System;
using System.Globalization;

//将脚本创建为类，以便复用 
class p {

    public static void ConvertCase(dynamic obj)
    {
        TextInfo textInfo = CultureInfo.CurrentCulture.TextInfo;
        //将下划线替换为空格
        var oldName = obj.Name.Replace("_", " ");
        var newName = new System.Text.StringBuilder();
        for(int i = 0; i < oldName.Length; i++) {
            //首字母始终大写:
            if(i == 0) newName.Append(Char.ToUpper(oldName[i]));

            //当出现两个大写字母后跟一个小写字母时
            //在第一个字母后插入空格:
            else if(i + 2 < oldName.Length && char.IsLower(oldName[i + 2]) && char.IsUpper(oldName[i + 1]) && char.IsUpper(oldName[i]))
            {
                newName.Append(oldName[i]);
                newName.Append(" ");
            }

            //其他情况下，当小写字母后跟大写字母时，应在第一个字母后
            //插入空格:
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
        //若上述步骤尚未处理，则应用 Proper Case
        obj.Name = textInfo.ToTitleCase(newName.ToString());
    }
}

foreach(var t in Model.Tables) {
//转换表名
    p.ConvertCase(t);
//转换列名
    foreach(var c in t.Columns) {
        p.ConvertCase(c);
        c.SummarizeBy = AggregateFunction.None;
        if (c.DataType == DataType.DateTime)
        {c.FormatString = "yyyy-mm-dd";}
    }
}
```

### 说明

此脚本执行后，会遍历模型中的所有表和列，并将其重命名为更友好的名称。 以 snake_case、camelCase 或 PascalCase 命名的名称都会转换为 Proper Case。 无需选择表，因为会处理模型中的所有表；直接运行脚本即可。 在遍历列的同时，它还会将默认汇总设置为“无”，并为所有 DateTime 类型字段设置格式字符串。

