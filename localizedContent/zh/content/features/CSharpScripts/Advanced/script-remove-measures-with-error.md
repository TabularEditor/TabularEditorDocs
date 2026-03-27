---
uid: script-remove-measures-with-error
title: 查看/删除有错误的度量值
author: Kurt Buhler
updated: 2023-02-28
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---

# 查看/删除有错误的度量值

## 脚本用途

如果你想查看所有包含错误的度量值，并可选择将其从模型中删除，同时将被删除的度量值备份为 .tsv 文件并保存到你选定的目录（以便之后需要时再添加回来）。

## 脚本

### 查看并删除有错误的度量值

```csharp
// 此脚本会扫描模型并显示所有包含错误的度量值，同时提供删除选项。
//
// .GetCachedSemantics(...) 方法仅在 TE3 中可用
using System.Windows.Forms;

// 隐藏“运行宏”微调框
ScriptHelper.WaitFormVisible = false;

// 获取所有包含错误的度量值
var measuresWithError = Model.AllMeasures.Where(m => m.GetCachedSemantics(ExpressionProperty.Expression).HasError).ToList();
// 在 Tabular Editor 3.12.0 之前，必须使用 GetSemantics 方法。
//var measuresWithError = Model.AllMeasures.Where(m => m.GetSemantics(ExpressionProperty.Expression).HasError).ToList();

// 如果没有包含错误的度量值，则以错误结束脚本。
if ( measuresWithError.Count == 0 )
{ 
Info ( "没有包含错误的度量值！ 👍" );
}

// 处理有问题的度量值
else 
{

// 查看包含错误的度量值列表
measuresWithError.Output();

//   你可以从列表中选择 1 个或多个度量值进行删除
var _ToDelete = SelectObjects(measuresWithError, measuresWithError, "选择要删除的度量值。\n稍后你可以导出备份。");

    // 删除所选度量值
    try
    {
        foreach ( var _m in _ToDelete ) 
            {
                _m.Delete();
            }
    
        Info ( 
            "已删除 " + 
            Convert.ToString(_ToDelete.Count()) + 
            " 个包含错误的度量值。" 
        );
    
        // 创建 FolderBrowserDialog 类的实例
        FolderBrowserDialog folderBrowserDialog = new FolderBrowserDialog();
        
        // 设置对话框标题
        folderBrowserDialog.Description = "选择一个目录，用于输出已删除度量值的备份。";
        
        // 设置对话框的根文件夹
        folderBrowserDialog.RootFolder = Environment.SpecialFolder.MyComputer;
        
        // 显示对话框并获取结果
        DialogResult result = folderBrowserDialog.ShowDialog();
        
        // 检查用户是否单击“确定”按钮并获取所选路径
        if (result == DialogResult.OK && !string.IsNullOrWhiteSpace(folderBrowserDialog.SelectedPath))
            {
                // 将输出路径作为字符串获取
                string _outputPath = folderBrowserDialog.SelectedPath;
                
                // 获取已删除度量值的属性
                var _backup = ExportProperties( _ToDelete );
    
                // 保存已删除度量值的备份
                SaveFile( _outputPath + "/DeletedMeasures-" + Model.Name + DateTime.Today.ToString("-yyyy-MM-dd") + ".tsv", _backup);
    
                Info ( 
                    "已导出 " + 
                    Convert.ToString(_ToDelete.Count()) +
                    " 个度量值的备份到 " + 
                    _outputPath
                );
            }
    }
    catch
    // 如果未选择任何度量值，则显示信息框
    {
    Info ( "未选择任何度量值。" );
    }
}

```

### 说明

此代码片段会根据 Tabular Editor 的语义分析，获取所有包含错误的度量值。 随后会在输出框中显示这些度量值，你可以手动浏览它们或进行修改。 之后，你可以选择要删除的度量值。 被删除的度量值可以保存为 .tsv 备份文件，方便你之后需要时再导入。

## 示例输出

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-view-error-measures.png" alt="An output dialog that lets the user view and edit any measures with errors in Tabular Editor" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong>该输出对话框允许你查看并编辑根据 Analysis Services 语义分析判定为“有错误”的度量值。</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-delete-error-measures.png" alt="A selection dialog that lets the user select measures to delete" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 2：</strong>可选择有错误的度量值并将其删除。</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-delete-error-measures-success.png" alt="A confirmation dialog that informs the user the deletion was successful" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 3：</strong>确认对话框会提示度量值已成功删除。</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-delete-error-measures-backup.png" alt="A dialog that lets the user select a directory to save a .tsv back-up of the deleted measure metadata" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 4：</strong>还可以选择将度量值的属性和定义备份为 .tsv 文件并保存到本地目录，以便日后需要时重新添加。</figcaption>
</figure>
