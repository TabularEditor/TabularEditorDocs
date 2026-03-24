---
uid: composite-model-measure-formatting
title: Measure Format Properties in Composite Models
author: Support Team
updated: 2026-01-26
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

# Measure Format Properties in Composite Models

When working with composite models that use a Live connection to Analysis Services (SSAS/AAS), you may encounter validation errors or confusing behavior when editing measure formatting properties. A common error message is:

**"A measure is not allowed to have both FormatString and Format Expression."**

This article explains why this occurs and how to resolve it.

---

## Understanding the Issue

Composite models combine local Power BI tables with remote tables from an SSAS/AAS semantic model via a Live connection. In this architecture, measure formatting can be ambiguous:

- **FormatString**: A static format definition (e.g., "0.00" for currency).
- **Format String Expression**: A dynamic format string evaluated at query time.

The error occurs because the model ends up with both a static format and a dynamic format expression simultaneously—a state that is not allowed by the Tabular Object Model (TOM).

### Why this happens

In composite models:

1. **Ownership ambiguity**: Remote measures are owned by the remote SSAS/AAS model. When you edit formatting in Tabular Editor, you may be trying to override remote metadata, which creates conflicts.

2. **Metadata synchronization**: When a Format String Expression is present on a measure, the FormatString often appears as "Custom" to indicate dynamic formatting is active. If you then try to set a static FormatString simultaneously, both properties become populated, triggering the validation error.

3. **Persistence constraints**: Changes to remote measure metadata may not persist cleanly because the remote model retains authoritative control. This leaves the local composite model in an inconsistent state.

---

## Root Causes

### Remote measure formatting

If the problematic measure is defined in the remote SSAS/AAS model:

- Formatting should be managed in the source model, not in the Power BI composite model.
- Attempting to override remote measure formatting in Power BI can result in both FormatString and Format String Expression being populated, leading to the validation error.

### Script or automation setting both properties

- If you are using C# scripts, Power Query transformations, or BPA rules to apply formatting, ensure they target only one approach per measure (either static or dynamic, not both).

### Calculation groups with format expressions

- Calculation groups can define Format String Expressions that override measure formats. If a calc item's format expression is active, the UI may still display the measure's static FormatString, creating the appearance of both being set.

### Version or environment constraints

- Dynamic format strings for measures have limited availability and may not be fully supported in certain Power BI versions or deployment modes (Report Server).
- If you are on Power BI Desktop prior to 2025 or Power BI Report Server prior to January 2025, dynamic measure formats may not be supported.

---

## Resolution

The solution depends on whether the measure is **remote** (from SSAS/AAS) or **local** (created in the composite model).

### If the measure is remote (from SSAS/AAS)

This is the most common scenario. Remote measures are owned by the source semantic model.

**Recommended approach:**

1. **Manage formatting in the source model.** Open SSAS/AAS in SQL Server Management Studio or Tabular Editor connected to the source model, and set the formatting there.

2. **If report-specific formatting is required,** create a local "wrapper" measure in your Power BI composite model:

   - Define a new measure in the local model that references the remote measure.
   - Apply the desired format string to the wrapper measure.
   - Use the wrapper measure in your report instead of the remote measure.

   **Trade-off:** This approach creates duplicates and adds maintenance overhead, but it is the most reliable way to apply report-specific formatting in a Live connection scenario.

### If the measure is local (created in the composite model)

**For static formatting (most common):**

1. Select the measure in Tabular Editor.
2. Clear the **Format String Expression** field (set it to empty/null).
3. Set the measure's **Format String** to the desired static format (e.g., `"0.00%"` for percentage, `"$#,##0.00"` for currency).
4. Save the model.

**For dynamic formatting:**

1. Select the measure.
2. Keep or set the **Format String Expression** to your desired DAX expression (this is the only formatting property you should use).
3. Leave the **Format String** as "Custom" (do not attempt to also set a static format string).
4. Verify that your environment supports dynamic format strings (Power BI Desktop 2025 or later, or Power BI Report Server January 2025 or later).

---

## Quick Troubleshooting Checklist

- [ ] **Determine measure ownership**: Is the measure remote (SSAS/AAS) or local (composite model)?
- [ ] **Check Format String Expression**: Even if you didn't set it, verify whether it is populated. In the property grid, look for a non-empty "Format String Expression" field.
- [ ] **Review scripts and rules**: If you use C# scripts or BPA rules to set measure formats, ensure they do not set both FormatString and Format String Expression in the same pass.
- [ ] **Check calculation groups**: Confirm whether any calculation group items define a Format String Expression that might be overriding or conflicting with the measure's format.
- [ ] **Verify environment version**: Confirm your Power BI Desktop (2025 or later) or Power BI Report Server (January 2025 or later) version, especially if using dynamic formats.

---

## Step-by-Step Examples

### Example 1: Fixing a remote measure with static formatting

**Scenario:** You have a "Sales Amount" measure in the remote SSAS model, and you want it formatted as currency in your Power BI report.

**Steps:**

1. In Tabular Editor, connect directly to the SSAS/AAS model (not to the Power BI composite model).
2. Navigate to the "Sales Amount" measure.
3. Set its **Format String** to `"$#,##0.00"`.
4. Save the model back to SSAS/AAS.
5. Return to Tabular Editor connected to the Power BI composite model; the formatting should now be inherited.

If formatting still does not appear correct in the report, create a local wrapper measure (see below).

### Example 2: Creating a wrapper measure for report-specific formatting

**Scenario:** You need the Sales Amount measure from SSAS formatted differently in this specific report.

**Steps:**

1. In Tabular Editor, connect to the Power BI composite model.
2. Create a new measure in a local table (or in the measure table if you have one):
   ```
   Sales Amount (Formatted) = [Sales Amount]
   ```
3. Set the **Format String** of the new measure to your desired format (e.g., `"$#,##0.00"`).
4. Save the model.
5. Update your report visuals to use the wrapper measure instead of the original remote measure.

### Example 3: Setting local measure with dynamic formatting

**Scenario:** You have a local measure in the composite model and want to apply conditional formatting based on a threshold.

**Steps:**

1. Select the measure in Tabular Editor.
2. Ensure **Format String** is empty (do not set a static format).
3. Set **Format String Expression** to your conditional expression:
   ```dax
   IF(
       [YourMeasure] > 1000,
       "#,##0.00",
       "0.00"
   )
   ```
4. Do **not** also set a static FormatString.
5. Save the model.
6. Verify your Power BI version supports dynamic format strings (Desktop 2025+ or PBIRS Jan 2025+).

---

## Prevention Best Practices

1. **Decide on formatting strategy early**: Determine whether each measure should use static or dynamic formatting and stick to one approach per measure.

2. **Audit remote measures**: Before editing formatting in a composite model, check whether the measure is remote. If so, manage formatting in the source SSAS/AAS model.

3. **Use version-appropriate features**: If you're using dynamic format strings, ensure all relevant environments (Desktop, Report Server, Analysis Services) support them for your Power BI version.

4. **Script defensively**: If you write C# scripts or BPA rules to format measures, separate the logic so you only set one for mat property per measure, and include a guard to check whether the other property is already populated.

5. **Clear Format String Expression when switching to static**: If a measure previously used dynamic formatting, always clear the Format String Expression before attempting to set a static FormatString.

---

## Additional Resources

- **[Microsoft Docs - Measure Format Strings](https://learn.microsoft.com/en-us/analysis-services/tmsl/measures-object-tmsl)**: Official documentation on measure formatting in the Tabular Object Model.
- **[Composite Models in Power BI](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-composite-models)**: Understanding Live connections and composite model architecture.
- **[Dynamic Format Strings](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-dynamic-format-strings)**: Feature availability and usage guidance.

---

## Still Need Help?

If the steps above don't resolve your issue:

1. **Verify the measure is local**: Connect directly to your Power BI file (.pbix) in Tabular Editor to confirm the measure is defined locally, not remotely.

2. **Export diagnostic information**: Run the following Tabular Editor script to audit all measures:
   ```csharp
   var measures = Model.AllMeasures;
   foreach (var m in measures)
   {
       var hasStaticFormat = !string.IsNullOrEmpty(m.FormatString);
       var hasDynamicFormat = !string.IsNullOrEmpty(m.FormatStringExpression);
       if (hasStaticFormat && hasDynamicFormat)
       {
           Output($"CONFLICT - {m.Name}: FormatString='{m.FormatString}', Expression='{m.FormatStringExpression}'");
       }
       else if (hasStaticFormat)
       {
           Output($"STATIC - {m.Name}: '{m.FormatString}'");
       }
       else if (hasDynamicFormat)
       {
           Output($"DYNAMIC - {m.Name}: '{m.FormatStringExpression}'");
       }
   }
   ```

3. **Contact support**: Reach out with the diagnostic output and your Power BI and Tabular Editor version numbers.
