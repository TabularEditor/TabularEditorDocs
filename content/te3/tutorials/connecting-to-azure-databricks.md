---
uid: connecting-to-azure-databricks
title: Connecting to Azure Databricks
author: David Bojsen
updated: 2025-08-05
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# (Tutorial) Connecting to Azure Databricks

Tabular Editor 3 supports connecting to Azure Databricks as a data source for your semantic models. This tutorial will guide you through the process of setting up a connection to Azure Databricks and importing data from it.

## Prerequisites

Before you begin, ensure you have the following:

- A valid Azure Databricks workspace
- Appropriate permissions to access the Databricks data
- Tabular Editor 3 (Desktop, Business, or Enterprise edition)

## Authentication Methods

When connecting to Azure Databricks, you have two main authentication methods:

### 1. Microsoft Entra ID (formerly Azure AD) Authentication

This is the recommended approach for connecting to Azure Databricks when your organization uses Microsoft Entra ID. This method provides seamless single sign-on and better security through managed identities.

#### About the Tabular Editor Enterprise Application

When you connect to Azure Databricks using Microsoft Entra ID authentication, Tabular Editor uses a registered enterprise application named "Tabular Editor 3 - User Delegated Access to Azure Databricks" with the Application (client) ID: `ea7fad17-a4d8-4bfe-9e2f-8bb09dc6daad`.

This enterprise application requires the following API permissions:

- **Microsoft Graph** (`00000003-0000-0000-c000-000000000000`)
  - `offline_access` (Delegated) - This permission allows Tabular Editor to maintain access to the data you've given it permission to access, even when you're not actively using the application. This is needed for maintaining a persistent connection to Databricks.
  - `openid` (Delegated) - Allows users to sign in to the app with their work or school accounts and allows the app to see basic user profile information.
  - `profile` (Delegated) - Allows the app to see basic profile information such as name, email, picture, username.
  - `User.Read` (Delegated) - Allows the app to read your profile, and to identify you when accessing the Databricks API.

- **Azure Databricks API** (`2ff814a6-3304-4ab8-85cb-cd0e6f879c1d`)
  - `user_impersonation` (Delegated) - Access Azure Databricks on behalf of the signed-in user. This allows Tabular Editor to connect to your Databricks workspace using your credentials.

For more information about Microsoft Entra ID permissions, please refer to the [Microsoft documentation on permission types](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-permissions-and-consent) and [application consent experience](https://learn.microsoft.com/en-us/azure/active-directory/develop/application-consent-experience).

> [!IMPORTANT]
> These permissions are required for Tabular Editor to access your Azure Databricks data securely through your Microsoft Entra ID credentials. Without these permissions, Tabular Editor cannot authenticate to your Azure Databricks workspace properly.

#### Consent Process for Microsoft Entra ID Authentication

When you first attempt to connect to Azure Databricks using Microsoft Entra ID authentication, you may be prompted to consent to the required permissions. The consent process depends on your organization's Microsoft Entra ID policies:

##### User Consent
If your organization allows user consent for applications:
1. You will see a consent prompt from Microsoft asking for permission to allow Tabular Editor to access Azure Databricks on your behalf
2. Review the permissions being requested
3. Click **Accept** to grant consent

> [!NOTE]
> Whether admin consent is required depends on your organization's Microsoft Entra ID policies, not necessarily the specific API permissions being requested. Many organizations allow users to consent to delegated permissions themselves, while others require administrator approval for all third-party applications regardless of permission level.

##### Admin Consent Required
If your organization restricts user consent (common in enterprise environments):
1. You will receive an error message indicating that admin consent is required
2. You'll need to contact your IT department or Microsoft Entra ID administrator
3. Provide them with:
   - Application Name: "Tabular Editor 3 - User Delegated Access to Azure Databricks"
   - Application ID: `ea7fad17-a4d8-4bfe-9e2f-8bb09dc6daad`
   - Required Permissions: Microsoft Graph (offline_access, openid, profile, User.Read) and Azure Databricks API (user_impersonation)

Your administrator can grant organization-wide consent in one of two ways:

**Option 1: Through the Microsoft Entra ID Admin Portal**
1. Navigate to Microsoft Entra ID > Enterprise Applications
2. Search for "Tabular Editor 3 - User Delegated Access to Azure Databricks"
3. Select the application and go to Permissions
4. Click "Grant admin consent for [Organization]"

**Option 2: Using the Direct Admin Consent URL**
Administrators can use the following direct link to grant consent:
```
https://login.microsoftonline.com/organizations/v2.0/adminconsent?client_id=ea0fc0fe-ed02-40d7-a29a-cc0a59d8b42c&scope=https://graph.microsoft.com/offline_access%20https://graph.microsoft.com/openid%20https://graph.microsoft.com/profile%20https://graph.microsoft.com/User.Read%202ff814a6-3304-4ab8-85cb-cd0e6f879c1d/user_impersonation&redirect_uri=https://tabulareditor.com
```

For more information about admin consent, see Microsoft's documentation on [Configure how users consent to applications](https://learn.microsoft.com/en-us/azure/active-directory/manage-apps/configure-user-consent).

#### Steps for Microsoft Entra ID Authentication:

1. In Tabular Editor 3, go to **Model** > **Import tables...**
2. Select **New Source** > **Databricks**
3. In the connection dialog:
   - Enter your Databricks workspace URL (format: `https://<region>.azuredatabricks.net`)
   - Select **Microsoft Entra ID** as the authentication method
   - For HTTP Path, specify the path to your Databricks cluster (e.g., `/sql/1.0/warehouses/<warehouse-id>`)

> [!NOTE]
> Your Databricks workspace URL should be in the format `https://<region>.azuredatabricks.net` - for example, `https://westeurope.azuredatabricks.net`.

### 2. Personal Access Token (PAT) Authentication

If Microsoft Entra ID integration is not available or if you prefer token-based authentication, you can use a Personal Access Token.

#### Steps for PAT Authentication:

1. Generate a Personal Access Token in your Azure Databricks workspace:
   - Go to your Databricks workspace
   - Click on your user profile icon in the top-right corner
   - Select **User Settings**
   - Go to the **Access Tokens** tab
   - Click **Generate New Token**
   - Provide a name and optionally set an expiration time
   - Click **Generate** and copy the token value

2. In Tabular Editor 3, go to **Model** > **Import tables...**
3. Select **New Source** > **Databricks**
4. In the connection dialog:
   - Enter your Databricks workspace URL
   - Select **Personal Access Token** as the authentication method
   - Paste your token into the Token field
   - For HTTP Path, specify the path to your Databricks cluster (e.g., `/sql/1.0/warehouses/<warehouse-id>`)

## Finding Your HTTP Path

The HTTP Path parameter is essential for connecting to your Databricks SQL warehouse. To find this value:

1. Go to your Databricks workspace
2. Navigate to **SQL** > **SQL Warehouses**
3. Select the SQL warehouse you want to connect to
4. Look for the **Connection Details** section
5. Copy the HTTP Path value which should be in the format: `/sql/1.0/warehouses/<warehouse-id>`

## Importing Tables from Databricks

Once you've configured your connection:

1. Click **Test Connection** to verify your credentials and connection settings
2. If the connection is successful, click **Next**
3. Select whether to import specific tables/views or use a custom SQL query
4. If selecting tables/views:
   - Browse through the available catalogs, schemas, and tables
   - Select the tables you wish to import
   - Optionally preview and filter columns
5. Review your selections and click **Import** to finalize

## Troubleshooting Connection Issues

If you encounter issues connecting to Azure Databricks:

- Verify your workspace URL is correct and accessible
- Ensure your Personal Access Token hasn't expired (if using PAT authentication)
- Check that your user account has the necessary permissions in Databricks
- Verify the HTTP Path points to an active SQL warehouse
- Ensure your network allows connections to the Databricks service

### Resolving Microsoft Entra ID Authentication Issues

If you're using Microsoft Entra ID authentication and encounter errors:

#### "AADSTS65001: The user or administrator has not consented to use the application"

This error occurs when the required permissions haven't been granted:

1. If you have sufficient privileges:
   - Click the consent link in the error message
   - Review and accept the permissions request

2. If you don't have sufficient privileges:
   - Contact your IT administrator
   - Provide them with the application ID: `ea7fad17-a4d8-4bfe-9e2f-8bb09dc6daad`
   - Request they grant organizational consent for the Tabular Editor enterprise application

#### "AADSTS700016: Application with identifier was not found in the directory"

This may occur if your organization uses a restricted application policy:

1. Contact your Microsoft Entra ID administrator
2. Request that they add the Tabular Editor enterprise application (ID: `ea7fad17-a4d8-4bfe-9e2f-8bb09dc6daad`) to your organization's allowed application list

> [!TIP]
> In some organizations, IT departments may require a formal request or security review before approving new enterprise applications. Be prepared to explain that this application is used by Tabular Editor 3 to securely connect to Azure Databricks resources using the organization's existing Microsoft Entra ID authentication infrastructure.

## Using Update Table Schema with Databricks

After importing tables from Azure Databricks, you can use Tabular Editor's **Update Table Schema** feature to keep your model in sync with changes in the Databricks tables.

To update the schema:

1. Right-click on the imported table in the TOM Explorer
2. Select **Update Table Schema**
3. Review any detected changes and apply them as needed

For complex queries or if you encounter issues with schema detection, consider enabling the **Use Analysis Services for change detection** option under **Tools** > **Preferences** > **Schema Compare** as described in the [Updating Table Schema](xref:importing-tables#updating-table-schema-through-analysis-services) documentation.

