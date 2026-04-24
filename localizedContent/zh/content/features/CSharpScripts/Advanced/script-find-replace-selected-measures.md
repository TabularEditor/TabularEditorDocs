---
uid: script-find-replace
title: 查找/替换度量值 DAX
author: Kurt Buhler
updated: 2023-03-01
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 在度量值中查找并替换子字符串

## 脚本用途

在模型的度量值 DAX 表达式中查找并替换子字符串。 即 例如，你想在多个度量值中将 `'Customers'[Key Account]` 替换为 `'Products'[Type]`。
一个输入框让用户输入要查找的文本，另一个输入框让用户定义替换文本。

## 脚本

```csharp
#r "System.Drawing"

using System.Drawing;
using System.Text.RegularExpressions;
using System.Windows.Forms;

// 隐藏“正在运行宏”微调框
ScriptHelper.WaitFormVisible = false;

// 将 Selected.Measures 替换为 Model.AllMeasures 以扫描所有度量值
var _measures = Model.AllMeasures;
    // 可选：将 _m.Expression 替换为 _m.Name，以在名称中查找/替换。

// 初始化 _find 和 _replace 字符串变量
string _find = "查找";
string _replace = "替换";

// WinForms 提示以获取查找/替换输入
using (Form prompt = new Form())
{
    Font formFont = new Font("Segoe UI", 11); 

    // 提示框配置
    prompt.AutoSize = true;
    prompt.MinimumSize = new Size(350, 120);
    prompt.Text = "查找/替换对话框";
    prompt.StartPosition = FormStartPosition.CenterScreen;

    // 将 AutoScaleMode 属性设置为 Dpi
    prompt.AutoScaleMode = AutoScaleMode.Dpi;

    // 查找：标签
    Label findLabel = new Label() { Text = "查找:" };
    findLabel.Location = new Point(20, 20);
    findLabel.Width = 80;
    findLabel.Font = formFont;

    // 用于输入子字符串文本的文本框
    TextBox findBox = new TextBox();
    findBox.Width = 200;
    findBox.Location = new Point(findLabel.Location.X + findLabel.Width + 20, findLabel.Location.Y - 4);
    findBox.SelectedText = "查找此文本";
    findBox.Font = formFont;

    // 替换：标签
    Label replaceLabel = new Label() { Left = 20, Top = 60, Text = "替换:" };
    replaceLabel.Width = 80;
    replaceLabel.Font = formFont;

    // 用于输入子字符串文本的文本框
    TextBox replaceBox = new TextBox() { Left = replaceLabel.Right + 20, Top = replaceLabel.Location.Y - 4, Width = findBox.Width };
    replaceBox.SelectedText = "替换为此文本";
    replaceBox.Font = formFont;

    // 确定按钮
    Button okButton = new Button() { Text = "确定", Left = 20, Width = 75, Top = replaceBox.Location.Y + replaceBox.Height + 20 };
    okButton.MinimumSize = new Size(75, 25);
    okButton.AutoSize = true;
    okButton.Font = formFont;

    // 取消按钮
    Button cancelButton = new Button() { Text = "取消", Left = okButton.Location.X + okButton.Width + 10, Top = okButton.Location.Y };
    cancelButton.MinimumSize = new Size(75, 25);
    cancelButton.AutoSize = true;
    cancelButton.Font = formFont;

    // 按钮操作
    okButton.Click += (sender, e) => { _find = findBox.Text; _replace = replaceBox.Text; prompt.DialogResult = DialogResult.OK; };
    cancelButton.Click += (sender, e) => { prompt.DialogResult = DialogResult.Cancel; };

    prompt.AcceptButton = okButton;
    prompt.CancelButton = cancelButton;

    prompt.Controls.Add(findLabel);
    prompt.Controls.Add(findBox);
    prompt.Controls.Add(replaceLabel);
    prompt.Controls.Add(replaceBox);
    prompt.Controls.Add(okButton);
    prompt.Controls.Add(cancelButton);

    // 用户点击“确定”后，执行查找/替换逻辑
    if (prompt.ShowDialog() == DialogResult.OK)
        {
            
            int _occurrences = 0;
            var _ReplacedList = new List<string>();
    
            foreach (var _m in _measures)
                {
                    if (_m.Expression != _m.Expression.Replace(_find, _replace))
                        {
                            try
                                {
                                    // 统计字符串中 _find 子字符串出现的次数
                                    string _pattern = Regex.Escape(_find);
                                    _occurrences = Regex.Matches(_m.Expression, _pattern).Count;
                                }
                            catch
                                {
                                    // 如果未找到，则出现次数为 0
                                    _occurrences = 0;
                                }
            
                            // 执行查找/替换
                            _m.Expression = _m.Expression.Replace(_find, _replace);
                            _ReplacedList.Add(_m.DaxObjectName);
                        }
                }
    
            // 创建一个包含所有已替换度量值的列表
            string _Replaced = _ReplacedList.Count > 0
                ? "\\n\\n已替换的度量值:\\n • " + string.Join("\\n • ", _ReplacedList)
                : "";
    
            // 返回成功信息弹窗
            Info(
                "已将 " + 
                _occurrences + 
                " 处出现的 '" + 
                _find + 
                "' 替换为 '" + 
                _replace + 
                "'" + 
                _Replaced);
        }
    else
        {
            Error("查找/替换已取消！");
        }
}

```

### 说明

此代码片段会使用 WinForms 创建一个弹出对话框，让你输入要在所选度量值中搜索的子字符串，并将其替换为另一个子字符串。 成功提示框会告知你查找/替换已成功完成。 成功提示框会告知你查找/替换已成功完成。

### 示例输出

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-find-replace-dialogue.png" alt="An example of the pop-up Find/Replace dialog that allows the user to enter the sub-strings to be searched / replaced." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> 弹出的查找/替换对话框示例，允许用户输入要搜索/替换的子字符串。</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-find-replace-success.png" alt="An example of the info box dialog which informs the user that the Find/Replace was successful, and how many / which measures were affected by the script." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 2：</strong> 信息提示框示例：用于告知用户查找/替换已成功，并显示脚本影响了多少/哪些度量值。</figcaption>
</figure>