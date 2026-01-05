---
uid: tmdl
title: Tabular Model Definition Language (TMDL)
author: Daniel Otykier
updated: 2023-05-22
applies_to:
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Tabular Model Definition Language (TMDL)

**TMDL** is a model metadata file format [announced by Microsoft in April 2023](https://powerbi.microsoft.com/en-ie/blog/announcing-public-preview-of-the-tabular-model-definition-language-tmdl/). It aims to provide a human-readable, text-based alternative to the JSON-based model.bim file format. TMDL is inspired by YAML, and as such, is easy to read and write, with minimal use of string quotes and escape characters. It also serializes a model as several smaller files in a folder structure, and is therefore also better suited for version control integration.

## Enabling TMDL in Tabular Editor 3

To enable TMDL in Tabular Editor 3, go to **Tools > Preferences > File Formats > Save-to-folder**, and select "TMDL" in the **Serialization mode** dropdown. The legacy "save-to-folder" functionality will continue to exist side by side with TMDL, but is not a Microsoft supported format.

After doing so, Tabular Editor 3 will use the TMDL format when saving a model as a folder (**File > Save to folder...**).

> [!NOTE]
> When you load a model from a legacy Tabular Editor folder structure, it will still get saved into that same format when using **File > Save** (Ctrl+S). Only when you explicitly use the **File > Save to folder...** command, will the model be saved in the new TMDL format.

## New models

When saving a new model for the first time, Tabular Editor (since v. 3.7.0), will now provide an option for saving the model as TMDL, even when the default serialization mode is not set to TMDL, as described in the previous section.

![New Model Tmdl](~/content/assets/images/new-model-tmdl.png)

# Next steps

- [TMDL overview (Microsoft Learn)](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview).
- [Get started with TMDL (Microsoft Learn)](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-how-to)
