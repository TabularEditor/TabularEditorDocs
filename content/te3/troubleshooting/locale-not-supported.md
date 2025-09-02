---
uid: locale-not-supported
title: Locale Not Supported
author: Morten Lønskov
updated: 2025-09-02
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# "Locale is not supported" Warning

You may encounter the warning message:

```
The XXXX locale is not supported
```
in the Tabular Editor 3 Message view

This issue usually occurs when your local machine uses a **regional configuration not supported by the Analysis Services (SSAS) engine**.  
In most cases, the error is triggered by another underlying issue or warning, but this message is shown as a result.

---

## Scenarios and Solutions

### 1. Connecting to a Local SSAS Instance
If you are running SQL Server Analysis Services (SSAS) locally on your machine:
- **Solution:** Change the **service account** used by the SSAS instance.  
  Updating the account often resolves unsupported locale mismatches.

---

### 2. Connecting to a Remote SSAS, Azure AS, or Power BI
When connecting to a remote instance, you have two possible solutions:

#### Option A: Specify Locale in the Connection String
Explicitly set a supported locale (e.g., English – 1033) by adding `LocaleIdentifier=1033` to your connection string.

**Example (Azure AS):**
```plaintext
Data Source=asazure://westeurope.asazure.windows.net/instance-name;LocaleIdentifier=1033
```

#### Option B: Change Regional Settings on Your Machine
Adjust your local system’s regional and language settings to match a supported locale.

- **Recommended settings:**  
  - **Regional format:** English (United States)  
  - **Windows Display Language:** English (United States)