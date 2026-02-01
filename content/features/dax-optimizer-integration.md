---
uid: dax-optimizer-integration
title: DAX Optimizer Integration
author: Daniel Otykier
updated: 2024-10-30
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
# DAX Optimizer Integration

> [!NOTE]
> Tabular Editor 3 **Enterprise Edition** users are eligible for free DAX Optimizer access. [Learn more](https://blog.tabulareditor.com/2024/10/31/free-dax-optimizer-access-in-tabular-editor-3/)

Tabular Editor 3.18.0 introduces **DAX Optimizer** as an integrated experience. [DAX Optimizer](https://daxoptimizer.com) is a service that helps you optimize your SSAS/Azure AS tabular models and Power BI/Fabric semantic models. The tool combines [VertiPaq Analyzer statistics](https://www.sqlbi.com/tools/vertipaq-analyzer/) with a static analysis of your DAX code, thus providing a prioritized list of recommendations, to help you quickly identify potential performance bottlenecks.

> [!IMPORTANT]
> DAX Optimizer is a paid third-party service. In order to use the **DAX Optimizer** feature in Tabular Editor 3, you will need an [account for DAX Optimizer](https://www.daxoptimizer.com/free-tour/).

## Video introduction

Watch Marco Russo from [SQLBI](https://www.sqlbi.com) introduce the DAX Optimizer integration in Tabular Editor 3:

<iframe width="640" height="360" src="https://www.youtube.com/embed/Z5lZdI79tF8" title="Detect and Fix Issues with Tabular Editor 3 and DAX Optimizer Integration" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Getting started

To access this feature, go to the **View** menu and choose **DAX Optimizer**.

![Dax Optimizer](~/content/assets/images/features/dax-optimizer-view-menu.png)

You will be presented with a new view similar to the figure below:

![Dax Optimizer View](~/content/assets/images/features/dax-optimizer-view.png)

To connect Tabular Editor 3 to the DAX Optimizer service, click **Connect...** through the **Options** menu. You will be prompted to enter your Tabular Tools (DAX Optimizer) credentials.

If you wish to **disconnect** or **connect using a different account**, go to the **Options** menu again, and choose the **Reconnect...** option. Cancelling the dialog will disconnect the current session.

If you want Tabular Editor 3 to automatically connect the next time the application is launched, you can check the **Connect automatically** option within the **Options** menu. If you have a DAX Optimizer account with workspaces in multiple regions, you can also choose which region to connect to through the **Options** menu.

Lastly, the **Options** menu also lets you switch to a different account in [group scenarios](https://docs.daxoptimizer.com/how-to-guides/managing-groups).

## Browsing workspaces and models

Once connected, the dropdowns at the top of the view will be populated with your existing workspaces, models and model versions. Make your selections from left to right (i.e. choose the **Workspace** first, then the **Model**, then the **Version**). The view will display a summary of the currently selected model version, with information such as model size, number of tables, number of measures, etc.

![Model Overview](~/content/assets/images/model-overview.png)

> [!NOTE]
> Tabular Editor 3 lets you upload VPAX files in order to create new models or model versions in the DAX Optimizer service. If, however, you need to create or manage workspaces, move or share models, etc. you will need to do this through the [DAX Optimizer web interface](https://app.daxoptimizer.com).

If a model version has not yet been analyzed, you will have an option to start the analysis. Note that, depending on your account plan, you may have a limited number of "runs" available.

Once the analysis is complete, you will be presented with a summary showing the number of issues detected. The information shown is similar to what you would see in the DAX Optimizer web interface.

Go to the **Issues** or **Measures** tab to view detailed results. Use the column headers to sort and filter the results.

![Dax Optimizer Issues](~/content/assets/images/features/dax-optimizer-issues.png)

## Navigating issues and measures

When you double-click on an issue or measure in the detailed view shown above, you will be taken to the **DAX Optimizer Results** view, where the original DAX expression of the measure is shown, along with highlights of the problematic areas. The list on the left side of the screen lets you toggle which issues to highlight. Moreover, you can mark issues as **Fixed** or **Ignored** using the checkboxes within the list.

![Dax Optimizer Results](~/content/assets/images/features/dax-optimizer-results.png)

Click on the **Find in TOM Explorer...** button in the top-right area of the view, to navigate to the corresponding measure in the currently loaded model.

Tick the **Track TOM Explorer** checkbox to keep the TOM Explorer in sync with the currently selected measure in the DAX Optimizer Results view.

When you click on a measure reference in the DAX code panel within the **DAX Optimizer Results** view, the view will navigate to that measure. You can then use the **Back** (Alt+Left) and **Forward** (Alt+Right) buttons to navigate back and forth between the measures you have visited.

## Upload models and model versions

To upload VPAX statistics to DAX Optimizer, make sure Tabular Editor is currently connected to an instance of Analysis Services (SSAS, Azure AS, Power BI Desktop or Power BI/Fabric XMLA endpoint). Then, select the workspace in the top-left dropdown on the **DAX Optimizer** view. Click on **Upload...** within the **Options** menu.

You will be presented with a dialog similar to the one shown below:

![Upload Vpax](~/content/assets/images/upload-vpax.png)

Here, you can choose whether the VPAX should be uploaded as a new model within the workspace, or whether the VPAX contains updated statistics for an existing model.

- For a **new model**, you must supply a name and choose whether or not the VPAX should be [obfuscated](https://www.sqlbi.com/blog/marco/2024/03/15/vpax-obfuscator-a-library-to-obfuscate-vpax-files/) (see below for more details on obfuscation). You must also choose which [contract](https://docs.daxoptimizer.com/glossary/contract) the model should be uploaded under. This impacts the number and frequency of DAX Optimizer [*runs*](https://docs.daxoptimizer.com/glossary/run) you can subsequently perform on the model.
- For a **new model version**, you must select the existing model to update.

Once you click the **OK** button, the VPAX file will be uploaded to DAX Optimizer, and you will be able to start analyzing the model.

> [!NOTE]
> If no VertiPaq Analyzer statistics are available in Tabular Editor 3, these statistics will be collected for the current model before the VPAX file is uploaded. We will also automatically re-collect statistics if the last statistics collection is older than or equal to the statistics of the last VPAX file upload, for the specific model.

### Obfuscation

By default, VPAX files uploaded using Tabular Editor 3 will be obfuscated. In the **Upload Model** you may toggle obfuscation on/off for new model uploads. Subsequent model version uploads will be obfuscated or not depending on the first version upload. You can also export an obfuscated VPAX file locally without uploading to DAX Optimizer through the **VertiPaq Analyzer** view. In this case, a dictionary file is generated and stored on your local machine, next to the exported .ovpax file. This dictionary file is used to deobfuscate the contents of the .ovpax file.

When obfuscated VPAX data is uploaded to the DAX Optimizer service through the **DAX Optimizer** view, Tabular Editor automatically keeps track of obfuscation dictionaries by storing them in the `%LocalAppData%\TabularEditor3\DaxOptimizer` folder on your local machine. As such, when browsing models using the **DAX Optimizer** feature in Tabular Editor 3, models are automatically deobfuscated if a suitable dictionary is found in this folder, providing a more seamless experience when using obfuscation.

If the dictionary is not found, you will have an option to manually specify a dictionary file.

![Obfuscated Model](~/content/assets/images/obfuscated-model.png)

If no dictionary file is provided, you will only be able to browse the obfuscated model and DAX Optimizer results, meaning you will not be able to view the original DAX expressions or navigate to the corresponding measures in the TOM Explorer.

[Learn more about DAX Optimizer obfuscation](https://docs.daxoptimizer.com/how-to-guides/obfuscating-files).

> [!TIP]
> If you want to browse an obfuscated model through the DAX Optimizer web interface, you can specify a dictionary from the `%LocalAppData%\TabularEditor3\DaxOptimizer` location. The DAX Optimizer web interface performs the deobfuscation on the client side, so your dictionary is never uploaded to the DAX Optimizer service.

### Analyze a model

Once a VPAX file has been uploaded, please allow a few seconds for the file to be "verified" by the DAX Optimizer service. Once verified, you can perform a DAX Optimizer "run" by checking the "You agree to **consume 1 run** to analyze this model." checkbox, and then clicking the **Analyze** button in the **DAX Optimizer** view:

![Dax Optimizer Analyze](~/content/assets/images/features/dax-optimizer-analyze.png)

The analysis will take a few minutes to complete, depending on the size of the model and the number of measures. Once the analysis is complete, you will be presented with a summary of the issues detected.

## Known issues and limitations

The following are known issues and limitations with the **DAX Optimizer** feature, which we expect to address in future releases:

- The **DAX Optimizer** view does not display how many "runs" are left on any given contract. As a workaround, sign in to https://app.daxoptimizer.com and click the "lightning" icon in the top-right corner, to view how many "runs" you have left per contract.