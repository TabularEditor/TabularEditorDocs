---
uid: connect-ssas
title: 连接并部署到 SSAS
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

## 连接/部署到 SSAS 表格数据库

按下 CTRL+SHIFT+O，即可直接从已部署的表格数据库中打开表格模型。 输入服务器地址，并（可选）提供用户名和密码。 点击“确定”后，会显示该服务器上的数据库列表。 选择要加载的数据库，然后再次点击“确定”。

![](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/Connect.png)

该对话框也支持连接到 Azure Analysis Services 实例：只要提供 Azure AS 实例的完整名称，并以“azureas://”开头即可。 “本地实例”下拉列表可用于浏览并连接到任何正在运行的 Power BI Desktop 或 Visual Studio 集成工作区实例。 **注意：尽管 Tabular Editor 可以通过 TOM 对 Power BI 模型进行更改，但这不受 Microsoft 支持，而且可能会损坏你的 .pbix 文件。 请自行承担风险！** “本地实例”下拉列表可用于浏览并连接到任何正在运行的 Power BI Desktop 或 Visual Studio 集成工作区实例。 **注意：尽管 Tabular Editor 可以通过 TOM 对 Power BI 模型进行更改，但这不受 Microsoft 支持，而且可能会损坏你的 .pbix 文件。 请自行承担风险！**

在数据库加载完成后，只要你按下 CTRL+S，Tabular Editor 就会将你所做的更改更新到数据库中。 客户端工具（Excel、Power BI、DAX Studio 等） 这些工具随后应能立即在数据库中看到这些更改。 注意：根据你做的更改，你可能需要手动重新计算模型中的对象，才能成功查询模型。

如果你想将连接模式下的模型保存为 Model.bim 文件，请在“文件”菜单中选择“另存为...”。