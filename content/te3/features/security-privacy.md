﻿---
uid: security-privacy
title: Security overview
author: Daniel Otykier
updated: 2024-10-30
---
# Tabular Editor 3 Security and Privacy

This document describes the security and privacy considerations of Tabular Editor 3 and its use. In the following, the phrase "Tabular Editor" can mean both the commercial tool Tabular Editor 3, as well as the open-source tool Tabular Editor 2.X. Whenever something considers only one of the tools, we will use their explicit names "Tabular Editor 3" or "Tabular Editor 2.X".

## Microsoft advice on third-party tools such as Tabular Editor

Microsoft supports the use of community third-party tools as communicated here: [Community and third-party tools for developing enterprise-level Power BI and Analysis Services models]( https://powerbi.microsoft.com/en-us/blog/community-tools-for-enterprise-powerbi-and-analysisservices)

Microsoft's Power BI implementation planning documentation specifically includes Tabular Editor in advanced data modeling scenarios and enterprise development: [Power BI usage scenarios: Advanced data model management](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-advanced-data-model-management#tabular-editor)

## Trust Center
At Tabular Editor, we are committed to transparency and strong security practices. Visit our [Trust Center](https://trust.tabulareditor.com/) to find details about our SOC 2 audit report, key policy documents, license terms, and our approach to infrastructure and organizational security. You’ll also find information about our sub-processors and how we work to keep your data safe.

## Metadata and Data Privacy

Tabular Editor is primarily an offline tool, meaning that all data and metadata reside locally in the client machine on which Tabular Editor is installed, and all user interactions are performed locally as well. An Internet connection is not required to run and use Tabular Editor.

That being said, there are scenarios in which Tabular Editor connects to remote services for various purposes. These are described in the following:

### Analysis Services XMLA Protocol

All communication with Analysis Services instances or Power BI Premium workspaces happens through the use of the [Microsoft Analysis Management Objects (AMO)](https://docs.microsoft.com/en-us/analysis-services/amo/developing-with-analysis-management-objects-amo?view=asallproducts-allversions) client libraries, or more specifically, the [Tabular Object Model (TOM) extension for AMO](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions). These client libraries are provided by Microsoft for redistribution in 3rd party applications such as Tabular Editor. For licensing details, please refer to the [AMO EULA](https://go.microsoft.com/fwlink/?linkid=852989).

When Tabular Editor connects to an instance of Analysis Services (local network or cloud) or a Power BI Premium workspace (cloud), this connection is performed through the client libraries mentioned above. By design, the AMO library handles the authentication and authorization of the user. Only users with administrative privileges on the Analysis Services instance or Power BI Premium workspace, are allowed to connect. This is no different than when using Microsoft tools such as SQL Server Management Studio or SQL Server Data Tools (which use the same client libraries for connectivity).

### Tabular Object Model metadata

Once the AMO/TOM client library establishes connection, Tabular Editor will request the full Tabular Object Model (TOM) metadata for the specific Analysis Services database or Power BI dataset that the user wants to connect to. The AMO/TOM client library then serves this metadata to the client application (Tabular Editor) in a programmatic approach, allowing the application to apply metadata changes, such as renaming an object, adding a description, modifying a DAX expression, etc. In addition, the AMO/TOM client library provides methods for serializing the TOM metadata into a JSON-based format. Tabular Editor uses this technique to allow users to save the model metadata as a local JSON file, for purposes of version control of the data model structure. **Note: The JSON file produced this way contains no actual data records. The file contains only model metadata, that is, information about the structure of the model in terms of tables, columns, measures, DAX expressions, etc.** While model metadata is generally not considered confidential information, it is the responsibility of the user of Tabular Editor to handle any file produced this way with the required confidentiality (i.e. not sharing the file with 3rd parties, etc.).

**Tabular Editor does not collect, publish, share, transfer or otherwise make public any model metadata obtained through the AMO/TOM client library unless the user specifically initiates an action to do so** (for example by saving the model metadata JSON file to a shared network location, or deploying the model metadata to another instance of Analysis Services or Power BI workspace).

### Model data content

In the following, "model data" refers to the actual data records stored within the Analysis Services database or Power BI dataset. Depending on the source database or dataset, it is very likely that the model data is confidential.

Because of the requirement for a user to have administrative privileges on the instance of Analysis Services or Power BI workspace that they are connecting to, the user will, by definition, also have access to all data content of the Analysis Services database or Power BI dataset. Tabular Editor only allows retrieval of data through the AMO client library mentioned above. Tabular Editor 3 provides features for browsing and querying model data. Regardless of which technique is used to access the data **Tabular Editor only stores retrieved data in local memory. Tabular Editor does not collect, publish, share, transfer or otherwise make public any model data obtained through the tool**. If a user chooses to copy or export query results obtained through Tabular Editor, it is their responsibility to treat the copied or exported data according to the confidentiality of the data. This is no different than a user connecting to the Analysis Services database or Power BI dataset using client tools such as Excel or Power BI, in which case they will also have the option to copy query results.

### Web requests

Tabular Editor may perform requests to online resources (web URLs) only in the following cases:

- **License activation\*.** When Tabular Editor 3 is first launched, and at periodic intervals thereafter, the tool may perform a request to our licensing service. This request contains encrypted information about the license key entered by the user, the e-mail address of the user (if provided), the local machine name and a one-way encoded hash identifying the current installation. No other data is transmitted in this request. The purpose of this request, is to activate and validate the license key used by the installation, enforce trial limitations, as well as allowing the user to manage their installations of Tabular Editor 3 through our licensing service.
- **Upgrade checks\*.** Each time Tabular Editor 3 is launched, it may perform a request to our application service, in order to determine if a newer version of Tabular Editor 3 is available. This request does not contain any data.
- **Usage telemetry\*.** By default, Tabular Editor 3 collects and transmits anonymous usage data as users interact with the tool. This data includes information about which UI objects a user interacts with and the timing of each. It also contains high-level information about the Tabular data model being edited through the tool. This information only relates to high-level properties like compatibility level and mode, number of tables, type of server (Analysis Services vs. Power BI vs. Power BI Desktop), etc. **No personally identifyable data is collected this way**, neither do we collect any information about names of objects or DAX expressions in the Tabular Object Model itself. A user may opt out of sending telemetry data to us at any point.
- **Error reports\*.** When an unexpected error occurs, we transmit the stack trace and (anonymized) error message, along with an optional description provided by the user. If a user opts out of sending telemetry data, error reports will also not be sent.
- **Using the DAX formatter.** (Tabular Editor 2.x only) A DAX expression may be formatted by clicking a button in Tabular Editor. In this case, the DAX expression (and nothing else) is sent to the www.daxformatter.com webservice. The first time a user clicks this button, an explicit warning message is shown, asking them to confirm their intent. Tabular Editor 3 does not perform web requests when formatting DAX code.
- **DAX Optimizer**. If a user has a [Tabular Tools account](https://tabulartools.com) with a [DAX Optimizer](https://daxoptimizer.com) subscription, they will be able to browse their DAX Optimizer workspace, view issues and suggestions, and upload new VPAX files directly from within Tabular Editor 3. VPAX files contains model metadata and statistics, but no actual model *data*. The DAX Optimizer Integration feature in Tabular Editor 3 causes various requests to one or more of the below endpoints (depending on authentication type and region specified when the Tabular Tools account was created).<br/>
  For more information, please consult the [DAX Optimizer documentation](https://docs.daxoptimizer.com/legal/data-processing).<br/>
  Endpoints used:
  - https://account.tabulartools.com
  - https://licensing.api.daxoptimizer.com/api
  - https://australiaeast.api.daxoptimizer.com/api
  - https://eastus.api.daxoptimizer.com/api
  - https://westeurope.api.daxoptimizer.com/api
- **Importing Best Practice Rules.** Tabular Editor has a feature that allows a user to specify an URL from which to retrieve a list of Best Practice rules in a JSON based format. This type of request only downloads the JSON data from the URL - no data is transmitted to the URL.
- **Using C# scripts.** Tabular Editor allows users to write and execute code written in C#, for purposes of automation. Such a script may potentially connect to online resources, using C# language features and the .NET runtime. The user is always responsible for ensuring that executed code does not cause any unintended sharing of data. Tabular Editor ApS cannot be held liable for any damages, losses or leaks caused by the use of the C# scripting feature in general. Tabular Editor will never execute C# scripts without the explicit action of the user.

\***Any information we obtain through the license activation service, the usage telemetry or the error reports, is kept confidential. We will not share, publish or distribute the data collected in any way, shape or form.**

**Firewall allowlist / acceptlist**
To allow traffic to the above mentioned web requests, you'll have to whitelist:
- License activation / upgrade checks: **https://api.tabulareditor.com**
- Usage telemetry / Error reports: **https://*.in.applicationinsights.azure.com**
- DAX Formatter (Tabular Editor 2.x only): **https://www.daxformatter.com**
- Import Best Practice Rules / C# Scripts: Depends on the context
- DAX Optimizer: Endpoints listed above.

> [!NOTE]
> A system administrator may enforce certain [policies](xref:policies), which can be used to disable some or all of the features shown on the list above.

## Application Security

Tabular Editor does not require any elevated privileges on the Windows machine in which it is installed, neither does it access any restricted resources on the machine. One exception from this rule, is if using the Tabular Editor installer file (.msi), in which case the executable and support files required by the tool, are by default copied to the `Program Files` folder, which typically requires elevated permission. Both the Tabular Editor binary files as well as the installer file, have been signed with a code signing certificate issued to Kapacity A/S, which is your guarantee that the code has not been tampered with by any 3rd party.

When the application is executing, all access to external resources are performed through the AMO/TOM client library or the web requests mentioned above.

The C# script feature allows Tabular Editor to execute arbitrary C# code within the .NET runtime. Such code is only compiled and executed on the explicit request of the user. C# scripts may also be saved as "macros", which makes it easier for the user to manage and execute multiple different scripts. The code is stored to the users own `%localappdata%` folder, ensuring that only they or a local machine administrator, can access the scripts. The user is always responsible for ensuring that executed code does not cause any unintended sideeffects. Under no circumstance can Tabular Editor ApS be held liable for any damages, losses or leaks caused by the use of the C# scripting or custom actions/macros features.
