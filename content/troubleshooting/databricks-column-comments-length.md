---
uid: databricks-column-comments-length
title: Databricks Column Comment Length Error
author: Support Team
updated: 2026-04-08
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

# Databricks Column Comment Length Error

> [!TIP]
> Databricks has released a new ODBC driver that replaces the legacy Simba Spark ODBC Driver. The new [Databricks ODBC Driver](https://www.databricks.com/spark/odbc-drivers-download) may not have the `MaxCommentLen` limitation described below. If you experience this issue, consider switching to the new driver, which Tabular Editor 3.26.0 and later supports.

When using the Import Table Wizard to import tables from Databricks, you may encounter a connection error if column comments (descriptions) exceed 512 characters. This limitation exists in the Simba Spark ODBC Driver, even though Databricks Unity Catalog allows longer column comments.

A typical error message looks like:

**"Unable to connect to database 'database_name' on 'adb-xxxx.azuredatabricks.net/sql/1.0/warehouses/xxxx': Exception has been thrown by the target of an invocation."**

This article explains why this occurs and provides two workarounds to resolve the issue.

---

## Understanding the Issue

The Simba Spark ODBC Driver, which Tabular Editor uses to connect to Databricks, has a default limit of 512 characters for column comments. This limit is enforced regardless of what Databricks Unity Catalog allows.

### Why this happens

1. **Default driver limitation**: The Simba Spark ODBC Driver is configured with a default `MaxCommentLen` parameter of 512 characters.

2. **Unity Catalog allows longer comments**: Databricks Unity Catalog permits column descriptions longer than 512 characters, which can exceed the driver's limit.

3. **Import wizard retrieval**: When the Import Table Wizard queries table metadata, it attempts to retrieve all column comments. If any comment exceeds the driver's limit, the connection fails with an invocation exception.

---

## Resolution

There are two approaches to resolve this issue:

### Option 1: Limit column comments in Databricks (Recommended for simplicity)

The simplest approach is to ensure that all column descriptions in your Databricks Unity Catalog tables do not exceed 512 characters.

**Steps:**

1. Review column comments in your Databricks tables.
2. Identify any comments that exceed 512 characters.
3. Edit those comments to be 512 characters or fewer.
4. Save the changes in Databricks.
5. Retry the import in Tabular Editor.

**Benefits:**
- Simple to implement
- No configuration changes required
- Works across all tools connecting to Databricks

**Trade-offs:**
- Requires modification of source metadata
- May lose information if descriptions are truncated
- Not suitable if longer descriptions are required

### Option 2: Increase the MaxCommentLen parameter in Simba Driver

If you need to preserve column comments longer than 512 characters, you can configure the Simba Spark ODBC Driver to accommodate larger comments.

> [!NOTE]
> Before proceeding, ensure you have the latest version of the Simba Spark ODBC Driver for Databricks installed. You can download it from the [Microsoft Azure Databricks ODBC download page](https://learn.microsoft.com/azure/databricks/integrations/odbc/download).

**Steps:**

1. **Locate the Simba Spark ODBC Driver installation folder.**

   The default installation location for the 64-bit driver is:
   ```
   C:\Program Files\Simba Spark ODBC Driver\
   ```

   If you installed the driver to a custom location, navigate to that folder instead.

2. **Create or edit the microsoft.sparkodbc.ini file.**

   In the driver installation folder, create a new file named **microsoft.sparkodbc.ini** (if it doesn't already exist).

   > [!NOTE]
   > The Simba Spark ODBC Driver installer does not create this .ini file by default, so you will likely need to create it manually.

3. **Add the MaxCommentLen configuration.**

   Open the **microsoft.sparkodbc.ini** file in a text editor (such as Notepad) and add the following content:

   ```ini
   [Driver]
   MaxCommentLen=2048
   ```

   Adjust the value (2048 in this example) to accommodate the maximum comment length you need.

4. **Save the file.**

   Ensure the file is saved as **microsoft.sparkodbc.ini** (not microsoft.sparkodbc.ini.txt) in the driver installation folder.

5. **Restart Tabular Editor.**

   Close all instances of Tabular Editor and reopen the application for the configuration change to take effect.

6. **Retry the import.**

   Use the Import Table Wizard again to import your Databricks tables. The connection should now succeed with the increased comment length limit.

**Benefits:**
- Preserves full column descriptions
- No need to modify source metadata
- Applies to all Databricks connections using this driver

**Trade-offs:**
- Requires file system access to the driver installation folder
- Configuration file must be created manually
- Changes apply machine-wide, affecting other applications using the same driver

---

## Step-by-Step Example: Creating the microsoft.sparkodbc.ini File

If you've never created an .ini file before, follow these detailed steps:

1. **Open Notepad** (or your preferred text editor).

2. **Type the following content:**

   ```ini
   [Driver]
   MaxCommentLen=2048
   ```

3. **Save the file:**
   - Click **File > Save As**
   - Navigate to `C:\Program Files\Simba Spark ODBC Driver\`
   - In the **Save as type** dropdown, select **All Files (*.*)** (important!)
   - In the **File name** field, type exactly: **microsoft.sparkodbc.ini**
   - Click **Save**

   > [!IMPORTANT]
   > Make sure to select "All Files" as the file type, otherwise Notepad will save it as microsoft.sparkodbc.ini.txt, which will not work.

4. **Verify the file was created correctly:**
   - Open File Explorer and navigate to `C:\Program Files\Simba Spark ODBC Driver\`
   - Confirm that you see a file named **microsoft.sparkodbc.ini** (not microsoft.sparkodbc.ini.txt)

5. **Close and restart Tabular Editor** for the changes to take effect.

---

## Quick Troubleshooting Checklist

- [ ] **Confirm the error message**: Verify that the connection error occurs during the Import Table Wizard when connecting to Databricks.
- [ ] **Check column comment lengths**: Query your Databricks tables to identify any column comments exceeding 512 characters.
- [ ] **Verify driver installation**: Confirm that the Simba Spark ODBC Driver is installed and locate its installation folder.
- [ ] **Check .ini file location**: Ensure the **microsoft.sparkodbc.ini** file is in the correct folder (the driver installation directory, not a subdirectory).
- [ ] **Verify file extension**: Confirm the file is named **microsoft.sparkodbc.ini** and not **microsoft.sparkodbc.ini.txt**.
- [ ] **Restart Tabular Editor**: Configuration changes only take effect after restarting the application.

---

## Prevention Best Practices

1. **Establish comment length guidelines**: If you're managing Databricks metadata, consider establishing guidelines to keep column comments under 512 characters for maximum compatibility.

2. **Test imports early**: When setting up a new Databricks environment, test table imports in Tabular Editor early in the development process to identify any metadata issues.

3. **Document driver configuration**: If you modify the **microsoft.sparkodbc.ini** file, document the change in your team's runbook so others are aware of the customization.

4. **Review after driver updates**: When updating the Simba Spark ODBC Driver, verify that your **microsoft.sparkodbc.ini** file is still present, as driver updates may overwrite or remove custom configuration files.

---

## Additional Resources

- **[Databricks Knowledge Base - Unity Catalog Metadata Error](https://kb.databricks.com/unity-catalog/error-when-trying-to-load-a-dataset-after-integrating-unity-catalog-metadata-with-power-bi)**: Official Databricks documentation covering this issue and the MaxCommentLen parameter.
- **[Simba Spark ODBC Driver for Azure Databricks](https://learn.microsoft.com/azure/databricks/integrations/odbc/download)**: Download the latest version of the Simba Spark ODBC Driver for Databricks.
- **[Import Table Wizard](xref:importing-tables)**: Learn more about using the Import Table Wizard in Tabular Editor.

---

## Still Need Help?

If the steps above don't resolve your issue:

1. **Verify ODBC driver version**: Ensure you have the latest version of the Simba Spark ODBC Driver installed. You can download it from the [Microsoft Azure Databricks ODBC download page](https://learn.microsoft.com/azure/databricks/integrations/odbc/download).

2. **Check ODBC Data Source configuration**: Open the Windows ODBC Data Source Administrator (odbcad32.exe) and verify that your Databricks connection is configured correctly.

3. **Test with a simpler table**: Try importing a Databricks table that you know has short column comments (or no comments) to confirm the connection works in general.

4. **Review ODBC driver logs**: The Simba Spark ODBC Driver can generate detailed logs. Refer to the driver documentation for instructions on enabling logging, which may provide additional diagnostic information.

5. **Contact support**: Reach out to Tabular Editor support with:
   - The full error message text
   - Your Databricks connection details (excluding credentials)
   - The Simba Spark ODBC Driver version
   - Whether you have created the microsoft.sparkodbc.ini file and its contents
