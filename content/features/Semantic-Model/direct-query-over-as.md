---
uid: dq-over-as-limitations
title: Direct Query over Analysis Services
author: Morten Lønskov
updated: 2025-07-14
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

## Overview

Tabular Editor 3 can **connect** to composite models that leverage **DirectQuery over Analysis Services (DQ‑over‑AS)**, but full modeling support is **not yet available**.  Most authoring tasks work as expected; however, operations that rely on synchronising metadata with the remote semantic model—such as *Update table schema*—are currently limited.

>[!IMPORTANT]
> Until full DQ‑over‑AS support ships, model metadata edited in Tabular Editor 3 **is not automatically kept in sync** with the source dataset. You must apply one of the work‑arounds listed below whenever columns or measures are added to the underlying Analysis Services model.

## Current limitations

| Feature                     | Status in TE3   | Notes                                                                                      |
| --------------------------- | --------------- | ------------------------------------------------------------------------------------------ |
| **Update table schema**     | ❌ Not supported | Attempting to run **Model > Update table schema** on a DQ‑over‑AS table has no effect.     |
| **Measure synchronisation** | ❌ Not supported | Measures created in the source dataset do not appear automatically in the composite model. |

## Work‑arounds

### 1. Manually add missing columns

1. In **TOM Explorer**, select the table that requires the new column.
2. Choose **Add > Data Column**.
3. In the *Properties* window, set:

   * **SourceColumnName** – *exactly* match the **Name** of the column in the remote table.
   * **SourceLineageTag** – copy the **LineageTag** value from the source column.
4. Save and deploy the model.

>[!NOTE]
> Column names and lineage tags must match *character‑for‑character*.  Any mismatch will cause deployment errors.

### 2. Use the “Import tables from remote model” C# script

Daniel Otykier’s article on LinkedIn provides a [ready‑made C# automation script](https://www.linkedin.com/pulse/composite-models-tabular-editor-daniel-otykier/) that:

1. Temporarily imports full copies of tables from the remote model.
2. Lets you copy columns (and other metadata) into existing tables.
3. Deletes the temporary tables after the copy is complete.

This approach is faster when several tables require updates.

### 3. One‑click macro to pull new measures

[rem-bou's](https://github.com/rem-bou) GitHub repository contains an advanced macro that scans the source dataset for measures that are **missing** in the composite model and adds them automatically: [Create-Update DQ over AS model connection](https://github.com/rem-bou/TabularEditor-Scripts/blob/main/Advanced/One-Click%20Macros/Create-Update%20DQ%20over%20AS%20model%20connection.csx)
