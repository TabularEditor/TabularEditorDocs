---
uid: connect-oledb
title: 通过 OLE DB 连接
author: Morten Lønskov
updated: 2026-09-21
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

# 通过 OLE DB 连接

OLE DB 是另一种通用连接方式；如果某个数据源提供 OLE DB 提供程序，但没有可用的 ODBC 驱动程序，就应使用这种方式。

![“数据链接属性”对话框的“提供程序”选项卡，其中列出了此计算机上安装的 OLE DB 提供程序](~/content/assets/images/features/connectivity/oledb-connection.png)

## 身份验证方式

与 ODBC 一样，由提供程序而不是 Tabular Editor 决定登录方式。

| 字段               | 含义                    |
| ---------------- | --------------------- |
| **提供程序**         | 此计算机上安装的 OLE DB 提供程序  |
| **服务器**          | 用于标识数据源的内容，按提供程序的要求填写 |
| **用户名** 和 **密码** | 在需要时提供给提供程序           |
| **附加选项**         | 额外的连接字符串设置，会原样传递      |

提供程序列表是从本机读取的，因此只会显示已安装的提供程序，而不是所有可用的提供程序。如果列表中缺少某个提供程序，需要先安装它，并确保其体系结构与 Tabular Editor 相同。

> [!TIP]
> 如有专用对话框，优先使用；否则优先选择 ODBC，而不是 OLE DB。 Analysis Services 支持的 OLE DB 提供程序范围比 Windows 更窄，因此，即使某个数据源能在向导中连接成功，仍可能在服务器上刷新失败。

## 凭据存储位置

你在此处输入的凭据会按用户和模型分别保存在模型旁边的 [用户选项](xref:user-options) 文件 (`.tmuo`) 中，并经过加密，只有你的 Windows 帐户可以读取。它们不属于模型元数据，因此不会提交到源代码版本控制中；其他同事打开同一模型时需要提供各自的。

生成的 M 表达式仅包含服务器和对象名称。其中绝不会包含密码、令牌或密钥。
