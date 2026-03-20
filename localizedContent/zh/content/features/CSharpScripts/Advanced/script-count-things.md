---
uid: script-count-things
title: 统计模型对象数量
author: Kurt Buhler
updated: 2023-02-27
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 统计模型中的各类对象

## 脚本用途

如果你想快速了解模型里有哪些内容，以及各类对象有多少：

- 模型中有多少个度量值。
- 模型中有多少列和计算列。
- 模型中有多少个表和计算表格。
- 模型中有多少个关系、非活动关系等。

## 脚本

### 按类型统计模型对象数量

```csharp
// 此脚本会统计模型中的对象，并在弹出信息框中显示。
// 它不会对该模型写入任何更改。
//
// 当你打开一个新模型，需要对其内容进行“鸟瞰”时，就用这个脚本。
//
// 统计计算组和计算项
int _calcgroups = 0;
int _calcitems = 0;
foreach (  var _calcgroup  in Model.CalculationGroups )
{
    _calcgroups = _calcgroups + 1;
    foreach (  var _item  in _calcgroup.CalculationItems )
    {
        _calcitems = _calcitems + 1;
    }
}

// 统计分区和 DAX 参数
int _partitions = 0;
int _whatifparameters = 0;
int _fieldparameters = 0;
foreach (  var _table  in Model.Tables )
{
    foreach (  var _partition  in _table.Partitions )
    {
        string _type = Convert.ToString(_partition.SourceType);
        string _exp = Convert.ToString(_partition.Expression);
        if ( _type == "M" )
        {
            _partitions = _partitions + 1;
        }
        else if ( _type == "Calculated" && _exp.Contains("NAMEOF") )
        {
            _fieldparameters = _fieldparameters + 1;
        }
        else if ( _type == "Calculated" && _exp.Contains("GENERATESERIES") )
        {
            _whatifparameters = _whatifparameters + 1;
        }
            
    }
}

// 度量值平均长度
decimal _numLines = 0;
decimal _numChars = 0;
int _measures = Model.AllMeasures.Count();
foreach ( var _measure in Model.AllMeasures )
{
    _numLines = _numLines + _measure.Expression.Split("\n").Length;
    _numChars = _numChars + _measure.Expression.Length;
}
_numLines = Math.Round(_numLines / _measures, 1);
_numChars = Math.Round(_numChars / _measures, 1);


// 返回弹窗
Info ( "在该模型中，我们看到以下对象：\n\n"

        + "-----------------------------------------\n"
        + "数据对象\n"
        + "-----------------------------------------\n"
        + " ├─ PQ 表达式：" + Convert.ToString(Model.Expressions.Count()) + "\n"
        + " │\n"
        + " └─ 表：" + Convert.ToString(Model.Tables.Count()) + "\n"
        + "       ├─ 增量刷新表：" + 
            Convert.ToString(Model.Tables.Where(
                _ir => 
                Convert.ToString(_ir.EnableRefreshPolicy) 
                == 
                "True").Count()) + "\n"
                
        + "       │\n"
        + "       ├─ 计算表格：" + 
            Convert.ToString(
                Model.Tables.Where(
                    _tables => 
                    Convert.ToString(_tables.Columns[0].Type) 
                    == 
                    "CalculatedTableColumn").Count()) + "\n"

        + "       │   ├─ 假设参数：" + 
            Convert.ToString(_whatifparameters) + "\n"
        + "       │   └─ 字段参数：" + 
            Convert.ToString(_fieldparameters) + "\n"
        + "       │\n"
        + "       ├─ M 分区：" + 
            Convert.ToString(_partitions) + "\n"
        + "       │\n"
        + "       └─ 表列总数：" + 
            Convert.ToString(Model.AllColumns.Count()) + "\n\n"

        + "-----------------------------------------\n"
        + "DAX 对象\n"
        + "-----------------------------------------\n"
        + " ├─ 关系：" + 
            Convert.ToString(Model.Relationships.Count()) + "\n"
        + " │   ├─ 双向：" + 
            Convert.ToString(Model.Relationships.Where(
                _relationships => 
                Convert.ToString(_relationships.CrossFilteringBehavior) 
                == 
                "BothDirections").Count()) + "\n"

        + " │   ├─ 多对多：" + 
            Convert.ToString(Model.Relationships.Where(
                _relationships => 
                Convert.ToString(_relationships.FromCardinality) 
                == 
                "Many" 
                && 
                Convert.ToString(_relationships.ToCardinality) 
                == 
                "Many").Count()) + "\n"

        + " │   ├─ 一对一：" + 
            Convert.ToString(Model.Relationships.Where(
                _relationships => 
                Convert.ToString(_relationships.FromCardinality) 
                == 
                "One" 
                && 
                Convert.ToString(_relationships.ToCardinality) 
                == 
                "One").Count()) + "\n"

        + " │   └─ 非活动：" + 
            Convert.ToString(Model.Relationships.Where(
                _relationships => 
                Convert.ToString(_relationships.IsActive) 
                == 
                "False").Count()) + "\n"

        + " │\n"
        + " ├─ 计算组：" + 
            Convert.ToString(_calcgroups) + "\n"
        + " │   └─ 计算项：" + 
            Convert.ToString(_calcitems) + "\n" 
        + " │\n"
        + " ├─ 计算列：" + 
            Convert.ToString(Model.AllColumns.Where(
                _columns => 
                Convert.ToString(_columns.Type) 
                == 
                "Calculated").Count()) + "\n"

        + " │\n"
        + " └─ 度量值：" + 
            Convert.ToString(_measures) + "\n" 
        + "     └─ DAX 平均行数：" + 
            Convert.ToString(_numLines) + " 行 \n" 
        + "     └─ DAX 平均字符数：" + 
            Convert.ToString(_numChars) + " 个字符 \n\n" 
       
        + "-----------------------------------------\n"
        + "其他对象\n"
        + "-----------------------------------------\n"
        + " ├─ 数据安全角色：" + 
            Convert.ToString(Model.Roles.Count()) + "\n"
        + " ├─ 显式数据源：" + 
            Convert.ToString(Model.DataSources.Count()) + "\n"
        + " ├─ 透视图：" + 
            Convert.ToString(Model.Perspectives.Count()) + "\n"
        + " └─ 翻译：" + 
            Convert.ToString(Model.Cultures.Count()));
```

### 说明

这段代码会遍历模型并统计不同类型对象的数量，然后以手动构造的分层“节点树”格式展示出来。
你可以把不需要的部分注释掉。

## 示例输出

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-count-things-output.png" alt="Example of the dialog pop-up that informs the user of how many rows are in the selected table upon running the script." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong>Info 信息框输出示例。脚本执行后，会向用户显示模型中各类对象的数量。 如果对某些对象不感兴趣，用户可以在脚本中将其注释掉或删除，然后重新运行。</figcaption>
</figure>