---
uid: user-options
title: User options (.tmuo) file
author: Daniel Otykier
updated: 2021-09-27
---
# Tabular Model User Options (.tmuo) File

Tabular Editor 3 introduces a new JSON based file, to store developer- and model-specific preferences. This file is called the **Tabular Model User Options** file and uses the **.tmuo** file extension.

When you open a Model.bim or Database.json file in Tabular Editor 3, the file will be created using the name of the file you loaded and your Windows user name. For example, if a user opens a file called `AdventureWorks.bim`, the user options file will be saved as `AdventureWorks.<UserName>.tmuo`, where `<UserName>` is the Windows user name of the current user. Tabular Editor searches for a file with such a name every time a model is loaded from disk.

> [!IMPORTANT]
> The **.tmuo** file contains user-specific preferences, and as such it should not be included in a shared version control environment. If you're using Git for version control, make sure to include the `.tmuo` extension in your `.gitignore` file.

## File content

Below is an example of the file content:

```json
{
  "UseWorkspace": true,
  "WorkspaceConnection": "provider=MSOLAP;data source=localhost",
  "WorkspaceDatabase": "WorkspaceDB_DanielOtykier_20210904_222118",
  "DataSourceOverrides": {
    "SQLDW": {
      "ConnectionString": {
        "Encryption": "UserKey",
        "EncryptedString": "..."
      },
      "PrivacySetting": "NA"
    }
  },
  "TableImportSettings": {
    "SQLDW": {
      "ServerType": "Sql",
      "UserId": "sqladmin",
      "Password": {
        "Encryption": "UserKey",
        "EncryptedString": "..."
      },
      "Server": "localhost",
      "Database": "AdventureWorksDW2019",
      "Authentication": 0
    }
  }
}
```

In this example, the JSON properties shown have the following meaning:

- `UseWorkspace`: Indicates whether Tabular Editor should connect to a workspace database upon loading the model. The workspace database will be overwritten with the metadata of the loaded file/folder structure. When this value is not present, Tabular Editor will prompt the user for whether they want to use a workspace database or not, upon model load.
- `WorkspaceConnection`: Server name of the Analysis Services instance or Power BI XMLA Endpoint to which the workspace database will be deployed.
- `WorkspaceDatabase`: Name of the workspace database to deploy. This should ideally be unique for each developer and model.
- `DataSourceOverrides`: This structure may be used to specify alternative data source properties and credentials which will be used every time the workspace database is deployed. This is useful if the Model.bim file contains data source connection details that you want to override for your workspace database, such as when you want Analysis Services to refresh data from a different source than what is specified in the Model.bim file.
- `TableImportSettings`: This structure is used whenever Tabular Editor's [Import Table or Schema Update](xref:importing-tables) feature is used. The credentials and settings specified here, are used by Tabular Editor when establishing a connection to the source for purposes of browsing available tables/views and updating the imported table schema, when changes have been made to the source.

All credentials and connection strings in the .tmuo file are encrypted with the Windows User Key. In other words, a .tmuo file containing encrypted data cannot be shared between multiple users.

## Next steps

- @workspace-mode