---
uid: script-create-m-parameter
title: 创建 M 参数
author: Kurt Buhler
updated: 2023-02-28
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 创建 M 分区

## 脚本用途

如果您想创建新的动态 M 参数，用于 Power Query 查询（M 分区或共享表达式）。

## 脚本

### 创建新的 M 分区

```csharp
// 此脚本会在模型的“Shared Expressions”中创建一个新的 M 参数。
//
// 创建一个名为 "New Parameter" 的共享表达式
Model.AddExpression( 
    "New Parameter", 
    @"
""Parameter Text"" meta
[
	IsParameterQuery = true,
	IsParameterQueryRequired = true,
	Type = type text
]"
);

// 输出提示，说明如何配置并使用该参数
Info ( 
    "已创建名为 'New Parameter' 的共享表达式，它是一个 M 参数模板。" + 
    "\n------------------------------------------------------\n" + 
    "配置方法：" +
    "\n------------------------------------------------------\n    " + 
    "1. 将文本 'New Parameter' 替换为所需的参数值\n    " +
    "2. 按需设置数据类型\n    " +
    "3. 将 M 分区中出现的相关值替换为该参数的引用。" );
```

### 说明

此代码片段会在“共享表达式”中创建一个新的 M 参数，并可在 M 分区的 Power Query 中引用。

## 输出示例

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-new-m-parameter.png" alt="An example of the Info box that appears to inform the user that the M Parameter was successfully created, and recommending next steps to configure / use it in the M Partitions." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> Info 提示框示例：用于告知用户已成功创建 M 参数，并建议下一步如何在 M 分区中配置/使用它。</figcaption>
</figure>