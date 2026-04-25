---
uid: references-application-language
title: 应用语言
author: Morten Lønskov
updated: 2026-01-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
description: 更改 Tabular Editor 3 界面的显示语言。
---

# 应用语言

Tabular Editor 3 支持多种 UI 语言。 你可以随时在不同语言之间切换。

> [!NOTE]
> Tabular Editor 3 目前仍未完全本地化。 具体来说，目前我们尚未对各个 TOM 属性进行本地化。

## 支持的语言

| 语言   | 状态   |
| ---- | ---- |
| 英语   | 完全支持 |
| 西班牙语 | 预览   |
| 中文   | 预览   |
| 法语   | Beta |
| 德语   | Beta |
| 日语   | Beta |

> [!NOTE]
> **预览**语言已翻译核心 UI 元素，但可能仍有部分内容未覆盖。 **Beta** 语言属于实验性支持，可能存在较多缺失或不一致。 请在 [GitHub](https://github.com/TabularEditor/TabularEditor3/issues) 上 Report 问题。

### 预览语言

处于 Beta 支持状态的语言表示其翻译已由人工译者校对，但 Tabular Editor 3 仍可能未完全本地化。 具体来说，我们目前尚未本地化各个 TOM 属性。

### Beta 语言

Beta 语言完全由 AI 翻译，尚未经人工译者校对。 我们计划在 2026 年第二季度将测试版语言引入 Preview。

## 更改语言

更改应用程序语言有两种方法：

### 通过“窗口”菜单

1. 点击 **窗口** > **语言**
2. 选择所需语言
3. 系统提示重启时，点击 **确定**
4. 手动重启 Tabular Editor 3

[通过窗口菜单更改语言](~/content/assets/images/user-interface/chaning-language-windows-ui.png)

### 通过偏好

1. 点击 **工具** > **偏好**
2. 转到 **UI** 部分
3. 在 **语言** 下拉列表中选择所需语言
4. 当系统提示重启时，点击 **确定**
5. 手动重启 Tabular Editor 3

[通过“窗口”菜单更改语言偏好](~/content/assets/images/user-interface/chaning-language-preferences.png)

## 需要重新启动

**你必须重启 Tabular Editor 3**，语言更改才会生效。 应用会提示你重启，但不会自动重启。 更改语言前，请先保存工作。

[通过“窗口”菜单更改语言](~/content/assets/images/user-interface/chaning-language-restart-pop-up.png)

## 安装语言

在安装过程中，安装程序会提示你选择一种语言（英语、西班牙语或中文）。 这会设置你的初始语言偏好，Tabular Editor 3 首次启动时将以该语言显示。

安装程序会将你的选择写入 LocalAppData 文件夹中的偏好设置文件。 你可以稍后使用上述任一方法进行更改。

## 语言设置持久化

你的语言偏好会存储在你的用户配置文件中的 `UiPreferences.json` 里。 该设置在应用更新和重启后仍会保留。

## 提供反馈

### 翻译问题

如果你发现翻译不正确或有文本缺失：

- 在 [GitHub](https://github.com/TabularEditor/TabularEditor3/issues) 上提交一个 Issue
- 请注明语言、错误文本，以及其在 UI 中出现的位置
- 如有可能，请提供正确的译文建议

## 另请参阅

- [偏好](xref:preferences)
- [用户界面概述](xref:user-interface)
