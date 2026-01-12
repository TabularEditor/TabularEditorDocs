---
uid: save-with-supporting-files
title: Save with supporting files
author: Peer Grønnerup
updated: 2026-01-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Save with supporting files

Save with supporting files is a feature that enables saving of semantic models with additional supporting files that follow the source code format required for Git Integration in Microsoft Fabric. This feature ensures that your Tabular Editor models are fully compatible with Fabric's Git integration capabilities, allowing seamless version control and deployment workflows.

When you save a semantic model with supporting files, Tabular Editor creates a folder structure that includes all necessary metadata files required by Microsoft Fabric's Git integration. This allows you to use Fabric Git integration to synchronize your semantic models between Fabric workspaces and Git repositories.

> [!NOTE]
> Saving with supporting files is only available when saving to .bim (TMSL) or when Save to Folder is set to TMDL as serialization mode.

## File structure and model properties

Semantic models saved with supporting files are stored in a folder with the **.SemanticModel** suffix. This suffix is required by Microsoft Fabric to recognize the folder as a semantic model item. If the parent folder does not have the .SemanticModel suffix, you will be prompted with a confirmation dialog to rename the folder.

> [!IMPORTANT]
> Model properties such as **name** and **description** are maintained through the **Name** and **Description** properties of the Database object in the TOM Explorer. These properties are automatically synchronized to the .platform metadata file. The folder name itself has no impact on the semantic model properties when deployed to Microsoft Fabric.

### Files included

Every saved model includes these core files:
- **.platform** - Metadata about the item including its type, display name, and description. Also contains a logicalId property, an automatically generated cross-workspace identifier.
- **definition.pbism** - Overall definition and core settings of the semantic model.

The complete folder structure depends on your serialization format:

| Format | Model storage |
|--------|------------------|
| **TMDL** | `\definition` folder containing TMDL files with the model metadata |
| **TMSL (.bim)** | `model.bim` file (automatically saved with a fixed filename) |

## How to save with supporting files

To save your model with supporting files:

1. Create a new or open an existing semantic model in Tabular Editor 3
2. Ensure your serialization mode is set to either TMDL or that you're saving as a .bim file
   - Go to **Tools > Preferences > File Formats** to configure serialization settings
3. Click on **File > Save As** or **File > Save to Folder**
4. Choose a folder where you want to save your model
   - Check the checkbox **Save with supporting files**
   ![Save with supporting files dialog](~/content/assets/images/common/SaveWithSupportingFilesDialog.png)
5. Click **Save**
    - If the folder name doesn't end with .SemanticModel, you'll be prompted to confirm the folder renaming

Tabular Editor will create the folder structure with all necessary files in the format compatible with Microsoft Fabric Git integration.

> [!IMPORTANT]
> The model culture must be present when synchronizing the model from Git to Microsoft Fabric. If the culture is not set, Fabric will apply its default culture, which can result in uncommitted changes appearing after the initial synchronization. To prevent this, Tabular Editor automatically sets the model culture to **en-US** when saving with supporting files.

## Git Integration in Microsoft Fabric

The **Save with supporting files** feature is designed to work seamlessly with Microsoft Fabric's Git integration capabilities.

> [!NOTE]
> Git Integration is available on workspaces assigned to:
> - Microsoft Fabric F-SKU capacity
> - Power BI Premium capacity
> - Power BI Premium Per User (PPU)

### Workflow with Fabric Git integration

1. **Save your model** using the Save with supporting files option in Tabular Editor 3
2. **Commit the changes** to your Git repository
3. **Connect your Fabric workspace** to the Git repository
4. **Synchronize** your model between Fabric and Git using the **Update all** button in the workspace source control pane.
   ![Synchronize workspace with Git](~/content/assets/images/common/WorkspaceGitSync.png)

For more information about working with Git integration in Fabric, see the following resources:
- [Microsoft Fabric Git integration documentation](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration?tabs=azure-devops)
- [Tabular Editor and Fabric Git Integration blog post](https://tabulareditor.com/blog/tabular-editor-and-fabric-git-integration)

## Comparing serialization formats

When using Save with supporting files, you can choose between two serialization formats:

### TMDL (Tabular Model Definition Language)
- Human-readable text format
- Easier to review changes in Git diffs
- Better for code reviews and collaboration
- Learn more: [TMDL documentation](tmdl.md)

### TMSL/JSON (.bim)
- JSON-based format
- Single file representation
- Compatible with older tools and workflows

Both formats are supported by Microsoft Fabric Git integration, and the choice depends on your team's preferences and workflow requirements.

## See also

- [Save to folder](save-to-folder.md)
- [TMDL - Tabular Model Definition Language](tmdl.md)
