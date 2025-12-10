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

Tabular Editor uses the [AMO client library](https://learn.microsoft.com/en-us/analysis-services/amo/developing-with-analysis-management-objects-amo?view=asallproducts-allversions) to connect to the Power BI / Fabric XMLA endpoint or instances of SQL Server or Azure Analysis Services (Tabular). Authentication and authorization is handled by the AMO client library, which means that Tabular Editor does not store any credentials or tokens. Moreover, users will need sufficient permissions to connect to the XMLA endpoint or Analysis Services instance. In most cases, the user must be a member of the Analysis Services server administrator role or have administrative permissions in the Power BI workspace.

In the following article, we will use the term "semantic model server" to mean the service accessed through the Power BI / Fabric XMLA endpoint or any instance of SQL Server Analysis Services Tabular (SSAS) or Azure Analysis Services (AAS).

## Connection dialog

To connect to the semantic model server, go to **File** > **Open** > **Model from DB...**, or press **Ctrl+Shift+O**.

This will open the **Load Semantic Model from Database** dialog, where you can specify the server name, an XMLA connection string or pick a local SSAS instance from a dropdown. Moreover, you can specify the type of authentication to use.

> [!NOTE]
> In Tabular Editor 2.x, the **Advanced Options** (for specifying read/write mode and a custom status bar color) are not available.

![Connect Dialog](~/content/assets/images/connect-dialog.png)

## Select database

After you click "OK", Tabular Editor will connect to the semantic model server and retrieve a list of databases that you have access to. Select the database you want to work with, and click "OK".

## Advanced Connection String Properties

In all versions of Tabular Editor, you can specify an OLAP connection string in the **Server** textbox, rather than just the server name.

A typical OLAP connection string looks like this:

```
Provider=MSOLAP;Data Source=servername;Initial Catalog=databasename;Integrated Security=SSPI;
```

> [!NOTE]
> If the `Initial Catalog` property is specified in the connection string, the **Select Database** dialog will not be shown, and Tabular Editor will connect directly to the specified database.

OLAP connection strings support many properties in addition to the ones shown above. For a full list of properties, see the [Microsoft documentation](https://learn.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions).

In addition to the properties listed in the documentation, AMO connection strings also supports the following properties:

### Locale Identifier

You can specify the language to use for the connection by setting the `Locale Identifier` property. The value is a number that corresponds to a specific language. For example, `1033` corresponds to English (United States).

```
Provider=MSOLAP;Data Source=servername;Initial Catalog=databasename;Integrated Security=SSPI;Locale Identifier=1033;
```

This is useful if you want error messages and other server messages to be in a specific language. If the `Locale Identifier` property is not specified, the language of the client operating system is used.

Most Analysis Services instances support several languages. See [this page for a full list of locale identifiers (LCID)](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-fulltext-languages-transact-sql?view=sql-server-ver16).

## Fabric/Power BI XMLA Settings

Two admin settings must be switched on to enable the XMLA endpoint in Fabric/Power BI. 

### Enable Tennant XMLA Endpoint 

In the Fabric/Power BI admin portal, the integration setting "Allow XMLA endpoints and Analyze in Excel with on-premises semantic models" must be enabled

At the tenant level, the setting may be restricted to only certain users. If the setting is restricted in your organization, ensure all required users are allowed to use the XMLA endpoint at the tenant level.

![Tennant Admin Setting](~/content/assets/images/common/XMLASettings/TennantAdminSetting.png)

### Enable XMLA Read Write on Capacity

To use the XMLA endpoint, the workspace that hosts a semantic model must be assigned to a capacity (FSku or Power BI Premium Per User), and the capacity must have XMLA ["Read Write" enabled in the capacity settings.](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#enable-xmla-read-write)

![Tennant Admin Setting](~/content/assets/images/common/XMLASettings/CapacityAdminSetting.png)

Read Write is enabled in the Admin Portal by navigating to 
1. Capacity Settings
1. Choosing the type of capacity
3. Selecting the relevant Capacity
4. Navigating to Power BI Workloads and scrolling down to find the XMLA Endpoint setting choosing "Read Write"

### Workspace Level User Rights
To edit models using the XMLA endpoint the user's account needs to have access to the workspace as either **Contributor**, **Member** or **Admin**. In the workspace choose 'Manage Access' and add the user account or a Entra ID group that the user belongs to with the required role. For more information on roles in workspaces please see Microsoft's Documentation: [Roles in Workspaces](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces)

### Read/Write on Semantic Model
Ensure that the user's account has Write permission to the semantic model. This can be required even if the user is an admin on the workspace as mentioned above.

To check that your account has the necessary permissions start by locating the model in the Fabric/Power BI workspace and first click on the hamburger symbol (3 vertical dots) and go to the "Manage permissions" page.

![Manage Permissions on Semantic Model](~/content/assets/images/common/XMLASettings/ManagePermissionsonSemanticModel.png)

Validate or give the user's account or the Entra ID group that they belong to either **Workspace Admin**, **Workspace Contributor**, or **Write permission** on the semantic model. For example, in the screenshot below, only the 3 users highlighted in Blue would be able to access the model through Tabular Editor:

![User Permissions on Semantic Model](~/content/assets/images/common/XMLASettings/UserPermissionsonSemanticModel.png)

### Set workspace to large semantic models
To ensure the best experience while editing models using the XMLA endpoint the workspace should have its semantic storage format set to **Large Semantic model storage format**. Go to 'Workspace Settings' in the top right corner of the Fabric/Power BI workspace. First navigate to the 'License info', secondly validate if the storage format is set to large and if not choose 'Edit' to change the storage format. 

![Large Semantic Model Storage Format](~/content/assets/images/common/XMLASettings/LargeSemanticModelStorageFormat.png)


## Additional Fabric/Power BI settings.

### Disable Package Refresh

If another user, other than the semantic model's owner, needs to edit the model through the XMLA endpoint, the security admin setting in Fabric/Power BI called "Block republish and disable package refresh" must be disabled.

![Tennant Admin Setting](~/content/assets/images/common/XMLASettings/DisablePackageRefresh.png)


## Unsupported model types
Several types of models do not support XMLA connections, [listed below](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#unsupported-semantic-models). 
 
The following semantic models aren't accessible by using the XMLA endpoint. These semantic models won't appear under the workspace in Tabular Editor or any other tool.

- Semantic models based on a live connection to an Azure Analysis Services or SQL Server Analysis Services model.
- Semantic models based on a live connection to a Power BI semantic model in another workspace. 
- Semantic models with Push data by using the REST API.
- Semantic models in My Workspace.
- Excel workbook semantic models

In Fabric, the default semantic model of a lakehouse or warehouse can be opened/connected to in Tabular Editor, but [not edited](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#considerations-and-limitations). Moreover, some operations that require read access to certain [DMVs](https://learn.microsoft.com/en-us/analysis-services/instances/use-dynamic-management-views-dmvs-to-monitor-analysis-services?view=asallproducts-allversions), such as collecting VertiPaq Analyzer statistics, may not be supported on default semantic models.

## Troubleshooting XMLA connections

### Testing a simple connection

These steps show how to most reliably connect to a Fabric/Power BI semantic model from Tabular Editor. 

1. Connecting to a semantic model in Fabric is through the 'File' > 'Open' > 'Model from DB' (default shortcut Ctrl+Shift+O)

2. You'll be presented with a dialogue (see below), and you need to put the Power BI connection string into the text box labeled 'Server'. Leave the rest of the options as configured in the screenshot (these are defaults). The connection string is in the form shown below. You can find this connection string in the Service (more details here in this [Microsoft doc in the sections 'Connecting to a Premium Workspace' and 'To get the workspace connection URL'](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#connecting-to-a-premium-workspace)

![Load Model From Database](~/content/assets/images/common/XMLASettings/LoadModelFromDatabase.png)

Please copy and paste the connection string directly from the workspace rather than copying from somewhere/someone else or modifying it in any way.

3. Depending on your machine (if your Windows login is linked to Entra ID or your identity provider) you may be prompted to log in. It's important that the account you use is the one with permission to the workspace. If your organization has multiple tenants or if you have multiple logins, this might not match your Windows login. You should use the exact credential that is shown in the Fabric web UI for your user.

![Authenticate to FabricPowerBI](~/content/assets/images/common/XMLASettings/AuthenticateToFabricPowerBI.png)

4. After successful authentication, you'll be presented with a 'Choose database' dialog. Select one and click 'Ok'.

![Choose Database](~/content/assets/images/common/XMLASettings/ChooseDatabase.png)

### Set Authentication Type to Microsoft Entra ID
In some cases the 'Integrated' security option could be different from the user account that should be used for authenticating against the Fabric/Power BI service. The next step to take is to choose the **Microsoft Entra MFA** option in the open model dialog box.

![Microsoft Entra MFA](~/content/assets/images/common/XMLASettings/LoadModelFromDatabaseMicrosoftEntraID.png)

Choosing the 'Microsoft Entra MFA' option forces the multifactor authentication and allows for choosing the specific account that is needed to connect to the workspace. 

### Multiple tenants
If you've double-checked the user name and connection string as above and are still having issues, the next thing to check is whether adding the tenant GUID to the connection string helps. This might be an issue if you belong to multiple tenants.
 
The tenant ID can be found directly in Power BI by clicking the top-right question mark and selecting 'About Power BI'. The tenant ID is shown as part of the 'Tenant URL'. Be careful, as the text box is typically too small to display the whole thing in the window in Power BI. Double-click on the URL shown, which will highlight the entire thing, that you can copy and paste.
 
The whole URL is not the tenant ID. The tenant ID is the GUID at the end of the string, after "ctid=". So in the screenshot below, my tenant ID starts with "ddec", but yours will be different. Once you have the tenant ID, you can change the connection string that you used above: replace the part of the path that says "myorg" with your tenant ID. 

An example is below. Your tenant ID and your workspace name will be different than those shown.
 
- Old: `powerbi://api.powerbi.com/v1.0/myorg/WorkspaceName`
- New: `powerbi://api.powerbi.com/v1.0/eeds65sv-kl25-4d12-990a-770ca3eb6226/WorkspaceName`

You can also use the tenant name (e.g. `fabrikam.com`) as shown in [this article](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools#connecting-to-a-premium-workspace).
 
Then, attempt connecting precisely as the instructions in the [Testing a simple connection section](#testing-a-simple-connection)

### Duplicate names

There can be issues connecting to a model if the workspace name is a duplicate of another workspace or if the model name is a duplicate name of another model.
 
If there are duplicate names, please refer to Microsoft's documentation in the sections ["Duplicate workspace names" and "Duplicate semantic model name"](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#duplicate-workspace-names) to learn how to modify the connection string to address these issues

### Proxy handling

Another common cause of connectivity issues is proxies. For more information about this, please review [this article](xref:proxy-settings).

### Testing connectivity using PowerShell

If connectivity issues persist even after attempting the troubleshooting steps mentioned above, it is also possible to connect directly to the XMLA endpoint using the [Microsoft-provided Analysis Services client libraries](https://www.nuget.org/packages/Microsoft.AnalysisServices/), *without* using Tabular Editor. We can do this using a simple PowerShell script as shown below. If this connection also fails, it is a clear indication that the issue is unrelated to Tabular Editor; in this case, you should consider raising a support ticket with Microsoft. When contacting Microsoft, inform them of which version of the **Microsoft.AnalysisServices.Tabular.dll** and **Microsoft.Identity.Client.dll** you're using, and also include the PowerShell script. Also, inform them whether you're using the .NET Core (Tabular Editor 3) or .NET Framework (Tabular Editor 2) versions of the DLLs. Avoid mentioning Tabular Editor directly in your support request, as this may confuse their 1st-level support. After creating the support ticket, please also notify us via support@tabulareditor.com, as we are interested in tracking the frequency of these issues.

To use the script:

1. Navigate to the Tabular Editor 3 installation folder through Windows Explorer
2. Right-click somewhere in the folder and choose "Open in Terminal". This should open a PowerShell window. You can also open a regular command window and type `pwsh` to launch PowerShell.
3. Check that the PowerShell version is at least 6.2.0. If the constrained language mode is restricted, try to open the terminal as an administrator or request assistance from your IT admin team to run the script.
4. In notepad, adjust the XMLA URL in the script below to match the endpoint you're trying to connect to. Then, copy the modified script into the PowerShell window and hit [Enter] to run it.

```powershell
# Config (TODO: Update workspace name below)
$xmla = "powerbi://api.powerbi.com/v1.0/myorg/workspace-name"

# Load DLLs
Add-Type -Path "Microsoft.AnalysisServices.Tabular.dll"

# Create Microsoft.AnalysisServices.Tabular.Server object:
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$connectionString = "Provider=MSOLAP;Data Source=$xmla;Interactive Login=Always;Identity Mode=Connection"

try {
	# Connect
	$server.Connect($connectionString)

	Write-Host "Connection succeeded." -ForegroundColor Green
	Write-Host "Connected to: $($server.Name)"
}
catch {
	Write-Host "Connection failed:" -ForegroundColor Red
	Write-Host $_.Exception.Message -ForegroundColor Red
}
```

If the script **succeeds**, it means that your machine is able to connect to the XMLA endpoint using the Microsoft client libraries. If, simultaneously, you're **not** able to connect using Tabular Editor, please post a ticket on our [Tabular Editor 2](https://github.com/TabularEditor/TabularEditor/issues) or [Tabular Editor 3](https://github.com/TabularEditor/TabularEditor3/issues) support page, or send an email to support@tabulareditor.com (**Tabular Editor 3 Enterprise Edition customers only**).

If the script **fails**, something on your environment is blocking XMLA endpoint connectivity, and so Tabular Editor will also not be able to connect. In this case, please reach out to your IT department for troubleshooting firewalls/proxies, before contacting Microsoft support.

If the script **succeeds** using Tabular Editor 2 DLLs, but **fails** using Tabular Editor 3 DLLs (or vice versa), please reach out to Microsoft support, since the issue in this case would be a discrepancy between the .NET Framework version of the DLLs (used by Tabular Editor 2) and the .NET Core version of the DLLs (used by Tabular Editor 3).
