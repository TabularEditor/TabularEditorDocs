---
uid: script-create-date-table
title: 创建日期表
author: Kurt Buhler
updated: 2023-02-28
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 创建日期表

## 脚本用途

你可以使用此脚本，基于模型中所选的 1-2 个日期列创建一张新的、结构清晰且已配置好的日期表。
第一个选中的列应包含最早日期，第二个选中的列应包含最晚日期。 运行脚本/宏之前，请先同时选中这两列。

此脚本将在模型中创建以下对象：

1. 一个度量值 `[RefDate]`，其值为模型范围内的最新日期；例如：最后一个销售日。 你可以手动调整该度量值，然后重新处理日期表，以便基于不同的参考日期重新生成（即如果你想将其改为 TODAY() 或添加筛选器）
2. `'Date'` 表——如果你有其他需求，可以在单独的 DAX 查询窗口中配置该表，然后将内容复制回脚本。
   - 所有列都会归入显示文件夹中
   - 将设置“排序依据”等列属性

此脚本目前不会在创建的日期表与模型中的日期字段之间创建关系。

## 脚本

### 创建日期表

```csharp
// 要使用此 C# Script：
//
// 1. 运行脚本
// 2. 选择包含最早日期的列
// 3. 选择包含最晚日期的列

// 模型中所有 DateTime 列的列表
var _dateColumns = Model.AllColumns.Where(c => c.DataType == DataType.DateTime ).ToList();

// 在模型中选择包含最早日期的列
try
{
    string _EarliestDate = 
        SelectColumn(
            _dateColumns, 
            null, 
            "请选择包含最早日期的列："
        ).DaxObjectFullName;
    
    try
    {
        // 在模型中选择包含最晚日期的列
        string _LatestDate = 
            SelectColumn(
                _dateColumns, 
                null, 
                "请选择包含最晚日期的列："
            ).DaxObjectFullName;
        
        
        // 创建参考日期度量值
        var _RefDateMeasure = _dateColumns[0].Table.AddMeasure(
            "RefDate",
            "CALCULATE ( MAX ( " + _LatestDate + " ), REMOVEFILTERS ( ) )"
        );
        
        
        // 格式化的日期表 DAX
        // 基于 https://www.sqlbi.com/topics/date-table/ 中的日期表
        // 如需调整，将 @" 之后的所有内容复制到 DAX 查询窗口并替换
        
        var _DateDaxExpression = @"-- Report 中最新日期的参考日期
        -- 业务希望在 Report 中查看数据的截止日期
        VAR _Refdate_Measure = [RefDate]
        VAR _Today = TODAY ( )
        
        -- 如果 [RefDate] 结果为空，则替换为 ""Today""
        VAR _Refdate = IF ( ISBLANK ( _Refdate_Measure ), _Today, _Refdate_Measure )
            VAR _RefYear        = YEAR ( _Refdate )
            VAR _RefQuarter     = _RefYear * 100 + QUARTER(_Refdate)
            VAR _RefMonth       = _RefYear * 100 + MONTH(_Refdate)
            VAR _RefWeek_EU     = _RefYear * 100 + WEEKNUM(_Refdate, 2)
        
        -- 模型范围内的最早日期
        VAR _EarliestDate       = DATE ( YEAR ( MIN ( " + _EarliestDate + @" ) ) - 2, 1, 1 )
        VAR _EarliestDate_Safe  = MIN ( _EarliestDate, DATE ( YEAR ( _Today ) + 1, 1, 1 ) )
        
        -- 模型范围内的最晚日期
        VAR _LatestDate_Safe    = DATE ( YEAR ( _Refdate ) + 2, 12, 1 )
        
        ------------------------------------------
        -- 基础日历表
        VAR _Base_Calendar      = CALENDAR ( _EarliestDate_Safe, _LatestDate_Safe )
        ------------------------------------------
        
        
        
        ------------------------------------------
        VAR _IntermediateResult = 
            ADDCOLUMNS ( _Base_Calendar,
        
                    ------------------------------------------
                ""Calendar Year Number (ie 2021)"",           --|
                    YEAR ([Date]),                          --|-- Year
                                                            --|
                ""Calendar Year (ie 2021)"",                  --|
                    FORMAT ([Date], ""YYYY""),                --|
                    ------------------------------------------
        
                    ------------------------------------------
                ""Calendar Quarter Year (ie Q1 2021)"",       --|
                    ""Q"" &                                   --|-- Quarter
                    CONVERT(QUARTER([Date]), STRING) &      --|
                    "" "" &                                   --|
                    CONVERT(YEAR([Date]), STRING),          --|
                                                            --|
                ""Calendar Year Quarter (ie 202101)"",        --|
                    YEAR([Date]) * 100 + QUARTER([Date]),   --|
                    ------------------------------------------
        
                    ------------------------------------------
                ""Calendar Month Year (ie Jan 21)"",          --|
                    FORMAT ( [Date], ""MMM YY"" ),            --|-- Month
                                                            --|
                ""Calendar Year Month (ie 202101)"",          --|
                    YEAR([Date]) * 100 + MONTH([Date]),     --|
                                                            --|
                ""Calendar Month (ie Jan)"",                  --|
                    FORMAT ( [Date], ""MMM"" ),               --|
                                                            --|
                ""Calendar Month # (ie 1)"",                  --|
                    MONTH ( [Date] ),                       --|
                    ------------------------------------------
                    
                    ------------------------------------------
                ""Calendar Week EU (ie WK25)"",               --|
                    ""WK"" & WEEKNUM( [Date], 2 ),            --|-- Week
                                                            --|
                ""Calendar Week Number EU (ie 25)"",          --|
                    WEEKNUM( [Date], 2 ),                   --|
                                                            --|
                ""Calendar Year Week Number EU (ie 202125)"", --|
                    YEAR ( [Date] ) * 100                   --|
                    +                                       --|
                    WEEKNUM( [Date], 2 ),                   --|
                                                            --|
                ""Calendar Week US (ie WK25)"",               --|
                    ""WK"" & WEEKNUM( [Date], 1 ),            --|
                                                            --|
                ""Calendar Week Number US (ie 25)"",          --|
                    WEEKNUM( [Date], 1 ),                   --|
                                                            --|
                ""Calendar Year Week Number US (ie 202125)"", --|
                    YEAR ( [Date] ) * 100                   --|
                    +                                       --|
                    WEEKNUM( [Date], 1 ),                   --|
                                                            --|
                ""Calendar Week ISO (ie WK25)"",              --|
                    ""WK"" & WEEKNUM( [Date], 21 ),           --|
                                                            --|
                ""Calendar Week Number ISO (ie 25)"",         --|
                    WEEKNUM( [Date], 21 ),                  --|
                                                            --|
                ""Calendar Year Week Number ISO (ie 202125)"",--|
                    YEAR ( [Date] ) * 100                   --|
                    +                                       --|
                    WEEKNUM( [Date], 21 ),                  --|
                    ------------------------------------------
        
                    ------------------------------------------
                ""Weekday Short (i.e. Mon)"",                 --|
                    FORMAT ( [Date], ""DDD"" ),               --|-- Weekday
                                                            --|
                ""Weekday Name (i.e. Monday)"",               --|
                    FORMAT ( [Date], ""DDDD"" ),              --|
                                                            --|
                ""Weekday Number EU (i.e. 1)"",               --|
                    WEEKDAY ( [Date], 2 ),                  --|
                    ------------------------------------------
                    
                    ------------------------------------------
                ""Calendar Month Day (i.e. Jan 05)"",         --|
                    FORMAT ( [Date], ""MMM DD"" ),            --|-- Day
                                                            --|
                ""Calendar Month Day (i.e. 0105)"",           --|
                    MONTH([Date]) * 100                     --|
                    +                                       --|
                    DAY([Date]),                            --|
                                                            --|
                ""YYYYMMDD"",                                 --|
                    YEAR ( [Date] ) * 10000                 --|
                    +                                       --|
                    MONTH ( [Date] ) * 100                  --|
                    +                                       --|
                    DAY ( [Date] ),                         --|
                    ------------------------------------------
        
        
                    ------------------------------------------
                ""IsDateInScope"",                            --|
                    [Date] <= _Refdate                      --|-- Boolean
                    &&                                      --|
                    YEAR([Date]) > YEAR(_EarliestDate),     --|
                                                            --|
                ""IsBeforeThisMonth"",                        --|
                    [Date] <= EOMONTH ( _Refdate, -1 ),     --|
                                                            --|
                ""IsLastMonth"",                              --|
                    [Date] <= EOMONTH ( _Refdate, 0 )       --|
                    &&                                      --|
                    [Date] > EOMONTH ( _Refdate, -1 ),      --|
                                                            --|
                ""IsYTD"",                                    --|
                    MONTH([Date])                           --|
                    <=                                      --|
                    MONTH(EOMONTH ( _Refdate, 0 )),         --|
                                                            --|
                ""IsActualToday"",                            --|
                    [Date] = _Today,                        --|
                                                            --|
                ""IsRefDate"",                                --|
                    [Date] = _Refdate,                      --|
                                                            --|
                ""IsHoliday"",                                --|
                    MONTH([Date]) * 100                     --|
                    +                                       --|
                    DAY([Date])                             --|
                        IN {0101, 0501, 1111, 1225},        --|
                                                            --|
                ""IsWeekday"",                                --|
                    WEEKDAY([Date], 2)                      --|
                        IN {1, 2, 3, 4, 5})                 --|
                    ------------------------------------------
        
        VAR _Result = 
            
                    --------------------------------------------
            ADDCOLUMNS (                                      --|
                _IntermediateResult,                          --|-- Boolean #2
                ""IsThisYear"",                                 --|
                    [Calendar Year Number (ie 2021)]          --|
                        = _RefYear,                           --|
                                                            --|
                ""IsThisMonth"",                                --|
                    [Calendar Year Month (ie 202101)]         --|
                        = _RefMonth,                          --|
                                                            --|
                ""IsThisQuarter"",                              --|
                    [Calendar Year Quarter (ie 202101)]       --|
                        = _RefQuarter,                        --|
                                                            --|
                ""IsThisWeek"",                                 --|
                    [Calendar Year Week Number EU (ie 202125)]--|
                        = _RefWeek_EU                         --|
            )                                                 --|
                    --------------------------------------------
                    
        RETURN 
            _Result";
        
        // 创建日期表
        var _date = Model.AddCalculatedTable(
            "Date",
            _DateDaxExpression
        );
        
        //-------------------------------------------------------------------------------------------//
        
        // 设置排序依据...
        
        // 排序：星期
        (_date.Columns["Weekday Name (i.e. Monday)"] as CalculatedTableColumn).SortByColumn = (_date.Columns["Weekday Number EU (i.e. 1)"] as CalculatedTableColumn);
        (_date.Columns["Weekday Short (i.e. Mon)"] as CalculatedTableColumn).SortByColumn = (_date.Columns["Weekday Number EU (i.e. 1)"] as CalculatedTableColumn);
        
        // 排序：周
        (_date.Columns["Calendar Week EU (ie WK25)"] as CalculatedTableColumn).SortByColumn = (_date.Columns["Calendar Week Number EU (ie 25)"] as CalculatedTableColumn);
        (_date.Columns["Calendar Week ISO (ie WK25)"] as CalculatedTableColumn).SortByColumn = (_date.Columns["Calendar Week Number ISO (ie 25)"] as CalculatedTableColumn);
        (_date.Columns["Calendar Week US (ie WK25)"] as CalculatedTableColumn).SortByColumn = (_date.Columns["Calendar Week Number US (ie 25)"] as CalculatedTableColumn);
        
        // 排序：月
        (_date.Columns["Calendar Month (ie Jan)"] as CalculatedTableColumn).SortByColumn = (_date.Columns["Calendar Month # (ie 1)"] as CalculatedTableColumn);
        (_date.Columns["Calendar Month Day (i.e. Jan 05)"] as CalculatedTableColumn).SortByColumn = (_date.Columns["Calendar Month Day (i.e. 0105)"] as CalculatedTableColumn);
        (_date.Columns["Calendar Month Year (ie Jan 21)"] as CalculatedTableColumn).SortByColumn = (_date.Columns["Calendar Year Month (ie 202101)"] as CalculatedTableColumn);
        
        // 排序：季度
        (_date.Columns["Calendar Quarter Year (ie Q1 2021)"] as CalculatedTableColumn).SortByColumn = (_date.Columns["Calendar Year Quarter (ie 202101)"] as CalculatedTableColumn);
        
        // 排序：年
        (_date.Columns["Calendar Year (ie 2021)"] as CalculatedTableColumn).SortByColumn = (_date.Columns["Calendar Year Number (ie 2021)"] as CalculatedTableColumn);
        
        
        //-------------------------------------------------------------------------------------------//
        
        
        // 针对日期表中的所有列：
        foreach (var c in _date.Columns )
        {
        c.DisplayFolder = "7. Boolean Fields";
        c.IsHidden = true;
        
        // 将日期表整理到文件夹中
            if ( ( c.DataType == DataType.DateTime & c.Name.Contains("Date") ) )
                {
                c.DisplayFolder = "6. Calendar Date";
                c.IsHidden = false;
                c.IsKey = true;
                }
        
            if ( c.Name == "YYMMDDDD" )
                {
                c.DisplayFolder = "6. Calendar Date";
                c.IsHidden = true;
                }
        
            if ( c.Name.Contains("Year") & c.DataType != DataType.Boolean )
                {
                c.DisplayFolder = "1. Year";
                c.IsHidden = false;
                }
        
            if ( c.Name.Contains("Week") & c.DataType != DataType.Boolean )
                {
                c.DisplayFolder = "4. Week";
                c.IsHidden = true;
                }
        
            if ( c.Name.Contains("day") & c.DataType != DataType.Boolean )
                {
                c.DisplayFolder = "5. Weekday / Workday\\Weekday";
                c.IsHidden = false;
                }
        
            if ( c.Name.Contains("Month") & c.DataType != DataType.Boolean )
                {
                c.DisplayFolder = "3. Month";
                c.IsHidden = false;
                }
        
            if ( c.Name.Contains("Quarter") & c.DataType != DataType.Boolean )
                {
                c.DisplayFolder = "2. Quarter";
                c.IsHidden = false;
                }
        
        }
        
        // 标记为日期表格
        _date.DataCategory = "Time";
        
        
        //-------------------------------------------------------------------------------------------//
        
        
        // 创建 Workdays MTD、QTD、YTD 的逻辑
        //      (拆分为度量值和计算列，便于维护)
        //
        // 添加 Workdays MTD、QTD、YTD 的计算列
        
        string _WorkdaysDax = @"VAR _Holidays =
            CALCULATETABLE (
                DISTINCT ('Date'[Date]),
                'Date'[IsHoliday] <> TRUE
            )
        VAR _WeekdayName = CALCULATE ( SELECTEDVALUE ( 'Date'[Weekday Short (i.e. Mon)] ) )
        VAR _WeekendDays = SWITCH (
                _WeekdayName,
                ""Sat"", 2,
                ""Sun"", 3,
                0
            )
        VAR _WorkdaysMTD =
            CALCULATE (
                NETWORKDAYS (
                    CALCULATE (
                        MIN ('Date'[Date]),
                        ALLEXCEPT ('Date', 'Date'[Calendar Month Year (ie Jan 21)])
                    ),
                    CALCULATE (MAX ('Date'[Date]) - _WeekendDays),
                    1,
                    _Holidays
                )
            )
                + 1
        RETURN
            IF (_WorkdaysMTD < 1, 1, _WorkdaysMTD)";
        
        _date.AddCalculatedColumn(
            "Workdays MTD",
            _WorkdaysDax,
            "5. Weekday / Workday\\Workdays"
        );
        
        _date.AddCalculatedColumn(
            "Workdays QTD",
            _WorkdaysDax.Replace("'Date'[Calendar Month Year (ie Jan 21)]", "'Date'[Calendar Quarter Year (ie Q1 2021)]"),
            "5. Weekday / Workday\\Workdays"
        );
        
        _date.AddCalculatedColumn(
            "Workdays YTD",
            _WorkdaysDax.Replace("'Date'[Calendar Month Year (ie Jan 21)]", "'Date'[Calendar Year (ie 2021)]"),
            "5. Weekday / Workday\\Workdays"
        );
        
        
        //-------------------------------------------------------------------------------------------//
        
        
        // 创建用于显示已过去多少个工作日的度量值
        _WorkdaysDax = @"CALCULATE(
            MAX( 'Date'[Workdays MTD] ),
            'Date'[IsDateInScope] = TRUE
        )";
        
        _date.AddMeasure(
            "# Workdays MTD",
            _WorkdaysDax,
            "5. Weekday / Workday\\Measures\\# Workdays"
        );
        
        _date.AddMeasure(
            "# Workdays QTD",
            _WorkdaysDax.Replace("MTD", "QTD"),
            "5. Weekday / Workday\\Measures\\# Workdays"
        );
        
        _date.AddMeasure(
            "# Workdays YTD",
            _WorkdaysDax.Replace("MTD", "YTD"),
            "5. Weekday / Workday\\Measures\\# Workdays"
        );
        
        // 创建用于显示所选期间内包含多少个工作日的度量值
        
        _WorkdaysDax = @"IF (
            HASONEVALUE ('Date'[Calendar Month Year (ie Jan 21)]),
            CALCULATE (
                MAX ('Date'[Workdays MTD]),
                VALUES ('Date'[Calendar Month Year (ie Jan 21)])
            )
        )";
        
        _date.AddMeasure(
            "# Workdays in Selected Month",
            _WorkdaysDax,
            "5. Weekday / Workday\\Measures\\# Workdays"
        );
        
        _date.AddMeasure(
            "# Workdays in Selected Quarter",
            _WorkdaysDax.Replace("MTD", "QTD").Replace("'Date'[Calendar Month Year (ie Jan 21)]", "'Date'[Calendar Quarter Year (ie Q1 2021)]"),
            "5. Weekday / Workday\\Measures\\# Workdays"
        );
        
        _date.AddMeasure(
            "# Workdays in Selected Year",
            _WorkdaysDax.Replace("MTD", "YTD").Replace("'Date'[Calendar Month Year (ie Jan 21)]", "'Date'[Calendar Year (ie 2021)]"),
            "5. Weekday / Workday\\Measures\\# Workdays"
        );
        
        
        // 创建用于显示已过去工作日占比的度量值
        
        _WorkdaysDax = @"IF (
            HASONEVALUE ('Date'[Calendar Month Year (ie Jan 21)]),
            MROUND (
                DIVIDE ([# Workdays MTD], [# Workdays in Selected Month]),
                0.01
            )
        )";
        
        _date.AddMeasure(
            "% Workdays MTD",
            _WorkdaysDax,
            "5. Weekday / Workday\\Measures\\# Workdays"
        );
        
        _date.AddMeasure(
            "% Workdays QTD",
            _WorkdaysDax.Replace("MTD", "QTD").Replace("'Date'[Calendar Month Year (ie Jan 21)]", "'Date'[Calendar Quarter Year (ie Q1 2021)]").Replace("Month", "Quarter"),
            "5. Weekday / Workday\\Measures\\# Workdays"
        );
        
        _date.AddMeasure(
            "% Workdays YTD",
            _WorkdaysDax.Replace("MTD", "YTD").Replace("'Date'[Calendar Month Year (ie Jan 21)]", "'Date'[Calendar Year (ie 2021)]").Replace("Month", "Year"),
            "5. Weekday / Workday\\Measures\\# Workdays"
        );
        
        
        //-------------------------------------------------------------------------------------------//
        
        
        // 将参考度量值移到新创建的 'Date' 表。
        _RefDateMeasure.Delete();
        _RefDateMeasure = Model.Tables["Date"].AddMeasure(
            "RefDate",
            "CALCULATE ( MAX ( " + _LatestDate + " ), REMOVEFILTERS ( ) )",
            "0. Measures"
        );
        
        _RefDateMeasure.IsHidden = true;
        
        Info ( "已根据 C# Script 中的模板创建并整理新的 'Date' 表。\n最早日期取自 " + _EarliestDate + "\n最晚日期取自 " + _LatestDate );
    
        }
        catch
        {
            Error( "未选择最晚日期列！脚本结束，不做任何更改。" );
        }
}
catch
{
    Error( "未选择最早日期列！脚本结束，不做任何更改。" );
}

```

### 说明

此代码段会获取你所选的列，并创建一个度量值，用于在 Report 中显示最大日期。 随后会创建一张格式化的 Date 表，其中包含用于制作 Report 的常用列。 该日期表仅包含日历日期，不包含财务期间。

## 示例输出

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-date-table-select-earliest-date.png" alt="Select Earliest date dialog" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图1：</strong>运行脚本时，会弹出一个对话框，提示您从模型中选择一个包含最早日期的 DateTime 列，以便配置日期表。</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-date-table-select-latest-date.png" alt="Select Latest date dialog" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图2：</strong>选择最早日期后，会弹出一个对话框，提示您从模型中选择一个包含最晚日期的 DateTime 列，以便配置日期表。</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-date-table-confirmation.png" alt="Confirmation of the date table being created" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图3：</strong>确认对话框将告知您，日期表已基于所选的两个日期成功配置。</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-date-table.png" alt="Resulting Date Table Template" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图4：</strong>使用此脚本一键创建的、结构清晰且已配置完成的日期表示例。</figcaption>
</figure>
