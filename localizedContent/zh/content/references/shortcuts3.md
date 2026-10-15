---
uid: shortcuts3
title: Tabular Editor 3 键盘快捷键
author: Daniel Otykier
updated: 2026-10-13
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 键盘快捷键

## 常规

| 命令                | 快捷键          |
| ----------------- | ------------ |
| 新建模型              | Ctrl+N       |
| 打开文件              | Ctrl+O       |
| 从数据库加载模型          | Ctrl+Shift+O |
| 保存当前项             | Ctrl+S       |
| 全部保存              | Ctrl+Shift+S |
| 关闭文档              | Ctrl+W       |
| 退出                | Alt+F4       |
| Deployment Wizard | Ctrl+Shift+D |
| 切换焦点窗口            | Ctrl+Tab     |

## 编辑

| 命令 | 快捷键    |
| -- | ------ |
| 全选 | Ctrl+A |
| 复制 | Ctrl+C |
| 剪切 | Ctrl+X |
| 粘贴 | Ctrl+V |
| 撤销 | Ctrl+Z |
| 重做 | Ctrl+Y |
| 查找 | Ctrl+F |
| 替换 | Ctrl+H |

## 与焦点位置相关的快捷键

某些快捷键会根据窗口中当前有焦点的部分执行不同的命令。文本控件包括文档编辑器、**表达式编辑器**，或在 **属性**视图中正在编辑的单元格。

| 快捷键                                  | 焦点在文本控件上   | 焦点在 TOM Explorer 上 |
| ------------------------------------ | ---------- | ------------------ |
| **Ctrl+Z** / **Ctrl+Y**              | 撤销或重做键入内容  | 撤销或重做上一次模型更改       |
| **Ctrl+X** / **Ctrl+C** / **Ctrl+V** | 剪切、复制或粘贴文本 | 剪切、复制或粘贴所选对象       |
| **Delete**                           | 删除所选文本     | 删除所选对象             |
| **Ctrl+A**                           | 全选文本       | 选择当前层级的所有对象        |
| **Ctrl+D**                           | 复制当前行      | 复制所选对象             |
| **Ctrl+U**                           | 取消注释文档中的各行 | 使所选对象可见            |

**Ctrl+S** 会保存当前有焦点的文档，例如 DAX 查询或关系图。当 TOM Explorer 获得焦点时，按下 **Ctrl+S** 即可保存模型。若要撤销通过文本控件对模型所做的更改，请参阅 @undo-redo。

## Data model 建模

| 命令           | 快捷键       |
| ------------ | --------- |
| 属性           | F4        |
| 编辑对象名称/批量重命名 | F2        |
| 批量重命名子项      | Shift+F2  |
| 查看依赖项        | Shift+F12 |
| 设为不可见        | Ctrl+I    |
| 设为可见         | Ctrl+U    |
| 创建度量值        | Alt+1     |
| 创建计算列        | Alt+2     |
| 创建层次结构       | Alt+3     |
| 创建数据列        | Alt+4     |
| 创建表          | Alt+5     |
| 创建计算表格       | Alt+6     |
| 创建计算组        | Alt+7     |
| 确认表达式更改      | F5        |

## TOM Explorer

| 命令               | 快捷键               |
| ---------------- | ----------------- |
| 向上/向下移动          | 上/下方向键            |
| 展开/折叠当前节点        | 右/左方向键            |
| 展开/折叠当前节点及其所有子节点 | Ctrl+右/左方向键       |
| 展开/折叠整棵树         | Ctrl+Shift+右/左方向键 |
| 切换度量值            | Ctrl+1            |
| 切换列              | Ctrl+2            |
| 切换层次结构           | Ctrl+3            |
| 显示/隐藏分区          | Ctrl+4            |
| 显示/隐藏显示文件夹       | Ctrl+5            |
| 显示/隐藏隐藏对象        | Ctrl+6            |
| 显示/隐藏信息列         | Ctrl+7            |
| 后退               | Alt+左箭头           |
| 前进               | Alt+右箭头           |

## 文本/代码编辑（通用）

| 命令     | 快捷键          |
| ------ | ------------ |
| 剪切行    | Ctrl+L       |
| 删除行    | Ctrl+Shift+L |
| 复制行    | Ctrl+Shift+T |
| 交换行    | Ctrl+T       |
| 重复当前行  | Ctrl+D       |
| 将行转为大写 | Ctrl+Shift+U |
| 向上移动行  | Alt+上箭头      |
| 向下移动行  | Alt+向下箭头     |

## DAX 代码

| 命令             | 快捷键                                    |
| -------------- | -------------------------------------- |
| 转到定义           | F12                                    |
| 窥视定义           | Alt+F12                                |
| 重构             | Ctrl+R                                 |
| 显示自动补全         | Ctrl+Space                             |
| 显示参数提示         | Ctrl+Shift+Space                       |
| 格式化 DAX        | F6                                     |
| 格式化 DAX（短行）    | Shift+F6                               |
| 注释行            | Ctrl+K                                 |
| 取消注释行          | Ctrl+U                                 |
| 切换注释           | Ctrl+/                                 |
| 折叠所有可折叠区域      | Ctrl+Alt+[   |
| 展开所有可折叠区域      | Ctrl+Alt+]   |
| 切换所有可折叠区域的折叠状态 | Ctrl+Alt+;                             |
| 折叠可折叠区域        | Ctrl+Shift+[ |
| 展开可折叠区域        | Ctrl+Shift+] |
| 切换可折叠区域的折叠状态   | Ctrl+Shift+;                           |
| 删除引用或词语        | Ctrl+Backspace 或 Ctrl+Delete           |
| 扩展选区           | Ctrl+Shift+E                           |

## DAX 查询

| 命令        | 快捷键                    |
| --------- | ---------------------- |
| 执行查询      | F5                     |
| 执行所选内容    | Shift+F5               |
| 应用        | F7                     |
| 应用并同步     | Shift+F7               |
| 应用所选内容    | F8                     |
| 应用所选内容并同步 | Shift+F8               |
| 显示代码操作    | Ctrl+. |

## DAX脚本

| 命令          | 快捷键      |
| ----------- | -------- |
| 应用脚本        | F5       |
| 应用所选内容      | F8       |
| 应用脚本并保存模型   | Shift+F5 |
| 应用所选内容并保存模型 | Shift+F8 |

## DAX 调试器

| 命令          | 快捷键       |
| ----------- | --------- |
| 单步跳过        | F10       |
| 单步回退        | Shift+F10 |
| 单步进入        | F11       |
| 单步跳出        | Shift+F11 |
| 下一行（最内层行语境） | F9        |
| 上一行（最内层行语境） | Shift+F9  |

## C# Script

| 命令   | 快捷键 |
| ---- | --- |
| 运行脚本 | F5  |

# 自定义快捷键

Tabular Editor 3 支持通过重新绑定现有快捷键或添加新快捷键来自定义快捷键。

可在 **工具 -> 偏好 -> 键盘** 中设置快捷键：找到需要绑定快捷键的命令，然后在菜单中指定按键组合。
Tabular Editor 3 的许多部分都可以设置快捷键，包括 [宏](xref:creating-macros)，让 C# Script 触手可及。

![Dax 脚本](~/content/assets/images/SetShortcuts.png)

1. 偏好设置中的“键盘”菜单
2. 找到需要设置快捷键的命令
3. 按住要设置的快捷键组合，然后使用 "Assign Shortcut" 进行分配