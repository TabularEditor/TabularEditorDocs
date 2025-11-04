---
uid: dax-package-manager
title: DAX Package Manager
author: Daniel Otykier
updated: 2025-11-03
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---

# DAX Package Manager

## Overview

The **DAX Package Manager** (DPM) in Tabular Editor allows users to easily discover, install, update, and manage [DAX User-Defined Function (UDF)](xref:udfs) libraries (called DAX Packages), directly within the application.  
These libraries extend your DAX capabilities with reusable functions, making it easier to build consistent and maintainable Power BI semantic models.

As the name suggests, this feature acts like a package manager similar to how NuGet or npm manage code libraries for developers. The source of the DAX packages is https://daxlib.org, which is an open-source, non-profit project by [SQLBI](https://sqlbi.com).

You can use the DAX Package Manager with any model that supports DAX User-Defined Functions, that is, the Compatibility Level of the model must be 1702 or higher.

> [!WARNING]
> DAX User-Defined Functions is currently (as of November 2025) a preview feature of Power BI. Consider their [limitations](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions#considerations-and-limitations) before use.

---

![DAX Package Manager](~/content/assets/images/dax-package-manager-overview.png)

## Interface Layout

### 1. Launching the DAX Package Manager
You can open the DPM panel through the **View** menu. It is also possible to assign a custom shortcut to the `View.DaxPackageManager` command, through **Tools > Preferences > Keyboard**.

- **Menu:** `View → DAX Package Manager`
- **Shortcut:** *(if assigned in Preferences)*

---

### 2. Package lists

On the left of the screen, you'll find the following three tabs. Each tab is accompanied by a list of packages relevant to its context:

| Tab | Description |
|-----|--------------|
| **Browse** | Discover available DAX packages from the provider (e.g., `api.daxlib.org`). |
| **Installed** | View all currently installed packages and their versions. |
| **Updates** | See packages for which newer versions are available. |

Each package entry includes:
- **Name and short description**
- **Version number**
- **Authors or owners**
- **Provider URL**
- **Install / Remove / Update buttons**
- **Popularity indicator (downloads count)**

---

### 3. Search bar

Enter your search keywords or the (partial) name of the package, to filter the list of items to only those that match the search terms. This feature applies to all three tabs, i.e., **Browse**, **Installed**, and **Updates**.

> [!NOTE]
> We currently only show the top 20 packages matching the search criteria. There is no pagination feature yet - this will come in a future update. If you need to browse all available packages, go to the source, e.g. https://daxlib.org.

---

### 4. Package Detail Pane

Selecting a package displays detailed information:

| Field | Description |
|--------|--------------|
| **Installed / Version** | Current version and available updates. |
| **Description** | Summary of what the library provides. |
| **Release Notes** | Information about new features or changes in the latest version. |
| **Provider / Owners / Authors** | Attribution metadata. |
| **Tags** | Helpful for categorization and search. |
| **URLs** | Direct links to the project’s documentation, API, and GitHub repository. |
| **Publish Date** | Timestamp of the current release. |
| **Downloads** | Total installs from all users. |

A package that is not installed, will show an **“Install”** button. Clicking this button will instantly add the UDFs in the package to your model.

Packages that are already installed will show a **“Remove”** button.

Packages for which newer versions are available, will show an **“Update”** button.

> [!WARNING]
> If you remove or update a package in which you have made modifications to the DAX expression of one or more UDFs, you will see a warning message indicating that your changes will be lost.

---

### 5. Update notifications

When opening a model that uses a package for which an update is available, you will see an update notification at the bottom of the **TOM Explorer**.

Click on the update notification or open the DAX Package Manager view, to view and install the update.

---

## Installing Packages

1. Open **DAX Package Manager**.
1. In the **Browse** tab, select a package (e.g., `DaxLib.SVG`). Use the search bar to refine the search as needed.
2. Click **Install**.
3. Once installed, the package and its functions will appear in the TOM Explorer.

You can also select specific **versions** before installing — useful for regression testing or ensuring compatibility with older models.

---

## Updating Packages

- Navigate to the **Updates** tab or select a package with a newer version available.
- Click **Update All** to update all installed packages, or **Update** on a specific one.
- DPM fetches the latest definitions and replaces existing functions automatically.

---

## Removing Packages

- Go to the **Installed** tab.
- Select the package you wish to remove.
- Click **Remove**.

All associated UDFs will be removed from the model.

> [!CAUTION]
> Removing UDFs may cause DAX expressions in other areas of the model (measures, calculation columns, etc.) to become invalid. If this happens, you can always hit **Undo** (Ctrl+Z) to undo the package removal. Use the **Show dependencies** (Shift+F12) feature to identify where the UDFs are used before removing a package.

---

## Technical considerations

The DAX Package Manager uses [extended properties](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.extendedproperty?view=analysisservices-dotnet) to keep track of installed packages. Extended properties are similar to annotations, but are better suited for storing custom metadata in JSON format.

The DAX Package Manager creates the following extended properties on the **Model** object:

| Property Name                     | Description                                      |
|-----------------------------------|--------------------------------------------------|
| `TabularEditor_ModelDaxPkgTable` | A JSON dictionary with one entry for each installed package. The key is a sequential integer, while the value contains information about the package provider, package ID within the provider, and package version. |
| `TabularEditor_ModelDaxPkgSeq` | An integer value that is incremented each time a package is installed. This is used to generate unique keys for the `TabularEditor_ModelDaxPkgTable` property. |

Moreover, each UDFs imported through the DAX Package Manager will have the following extended properties assigned:

| Property Name                     | Description                                      |
|-----------------------------------|--------------------------------------------------|
| `TabularEditor_ObjDaxPkgHandle`   | An integer value that corresponds to the key in the `TabularEditor_ModelDaxPkgTable` property on the model. This allows Tabular Editor to identify which package a UDF belongs to. |
| `TabularEditor_ObjDaxPkgContentHash` | A hash value computed from the DAX expression of the UDF at the time of installation. This is used to detect if a UDF has been modified since installation, which is important when updating or removing packages. |

> [!CAUTION]
> Modifying or deleting these extended properties manually may lead to unexpected behavior in the DAX Package Manager.

## Handling conflicts

### Modifying UDFs from packages

If you modify the DAX expression of a UDF imported from a DAX package, you will see the following prompt upon upgrading or removing the package:

![Update modified UDF](~/content/assets/images/dax-package-manager-update-modified.png)

You have the following options:

- **Yes**: The update will proceed, overwriting the changes you made to the UDF with its definition from the DAX Package Manager source.
- **No**: The update will proceed, but the modified UDF(s) will remain untouched, which may potentially cause issues if the package update included breaking changes.
- **Cancel**: Cancels the update.

> [!TIP]
> If you wish to "unlink" existing UDFs from the DAX Package Manager, remove the extended properties `TabularEditor_ObjDaxPkgHandle` and `TabularEditor_ObjDaxPkgContentHash` from the UDF objects. This way, the DAX Package Manager will no longer track these UDFs, and they will not be affected by future package updates or removals. However, you still need to be aware of name conflicts.

### Installing a package with name conflicts

If you attempt to install a package containing a UDF that has the same name as an existing UDF in the model (regardless of whether it was imported from another package or created manually), you will see the following prompt:

![Install package name conflict](~/content/assets/images/dax-package-manager-install-conflict.png)

You have the following options:

- **Yes**: The installation will proceed, and the UDF from the package will overwrite the existing UDF in the model.
- **No**: The installation will proceed, but the conflicting UDF(s) from the package will be skipped.
- **Cancel**: Cancels the installation.

---

## Additional Resources

- [DaxLib Project Site](https://daxlib.org)
- [DaxLib GitHub Repository](https://github.com/daxlib/daxlib)
- [DAX User-Defined Functions (Microsoft Learn)](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions)
- [User-Defined Functions in Tabular Editor 3](xref:udfs)