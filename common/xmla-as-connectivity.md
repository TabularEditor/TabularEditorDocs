---
uid: xmla-as-connectivity
title: XMLA / Analysis Services connectivity
author: Daniel Otykier
updated: 2024-05-01
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
  editions:
    - edition: Business
    - edition: Enterprise
---

# XMLA / Analysis Services connectivity

Tabular Editor uses the [AMO client library](https://learn.microsoft.com/en-us/analysis-services/amo/developing-with-analysis-management-objects-amo?view=asallproducts-allversions) to connect to the Power BI / Fabric XMLA endpoint, or instances of SQL Server or Azure Analysis Services (Tabular). Authentication and authorization is handled by the AMO client library, which means that Tabular Editor does not store any credentials or tokens. Moreover, users will need sufficient permissions to connect to the XMLA endpoint or Analysis Services instance. In most cases, this means that the user must be a member of the Analysis Services server administrator role, or have administrative permissions on the Power BI workspace.

In the following article, we will use the term "semantic model server" to mean the service accessed through the Power BI / Fabric XMLA endpoint, or any instance of SQL Server Analysis Services Tabular (SSAS) or Azure Analysis Services (AAS).

# Connection dialog

To connect to the semantic model server, go to **File** > **Open** > **Model from DB...**, or press **Ctrl+Shift+O**.

This will open the **Load Semantic Model from Database** dialog, where you can specify the server name or pick a local SSAS instance from a dropdown. Moreover, you can specify the type of authentication to use.

> [!NOTE]
> In Tabular Editor 2.x, the **Advanced Options** (for specifying read/write mode and a custom status bar color) are not available.

![Connect Dialog](~/images/connect-dialog.png)

# Select database

After you click "OK", Tabular Editor will connect to the semantic model server and retrieve a list of databases that you have access to. Select the database you want to work with, and click "OK".

# Advanced Connection String Properties

In all versions of Tabular Editor, you can specify an OLAP connection string in the **Server** textbox, rather than just the server name.

A typical OLAP connection string looks like this:

```
Provider=MSOLAP;Data Source=servername;Initial Catalog=databasename;Integrated Security=SSPI;
```

> [!NOTE]
> If the `Initial Catalog` property is specified in the connection string, the **Select Database** dialog will not be shown, and Tabular Editor will connect directly to the specified database.

OLAP connection strings support many properties in addition to the ones shown above. For a full list of properties, see the [Microsoft documentation](https://learn.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions).

In addition to the properties listed in the documentation, AMO connection strings also supports the following properties:

## Locale Identifier

You can specify the language to use for the connection by setting the `Locale Identifier` property. The value is a number that corresponds to a specific language. For example, `1033` corresponds to English (United States).

```
Provider=MSOLAP;Data Source=servername;Initial Catalog=databasename;Integrated Security=SSPI;Locale Identifier=1033;
```

This is useful if you want error messages and other server messages to be in a specific language. If the `Locale Identifier` property is not specified, the language of the client operating system is used.

Most Analysis Services instances supports several languages. See [this page for a full list of locale identifiers (LCID)](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-fulltext-languages-transact-sql?view=sql-server-ver16).