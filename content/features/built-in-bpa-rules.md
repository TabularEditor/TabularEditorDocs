---
uid: built-in-bpa-rules
title: Built-in BPA Rules
author: Morten Lønskov
updated: 2026-01-09
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.24.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
description: Enterprise Edition feature providing 27 curated best practice rules hardcoded into Tabular Editor 3 with knowledge base integration.
---

# Built-in BPA Rules

## Overview

Tabular Editor 3 Enterprise Edition includes 27 built-in best practice rules. These rules cover common issues in semantic model development and are updated automatically with each release.

Unlike custom rules stored in JSON files, built-in rules:
- Are integrated directly into the application
- Update automatically with new releases
- Link to knowledge base documentation
- Are read-only to ensure consistency across teams
- Work immediately without configuration

## Key Features

### Rule Categories

The 27 built-in rules cover four areas:
- **Error Prevention**: Invalid characters, missing expressions, data type mismatches
- **Performance**: Relationships, partitions, aggregations
- **Formatting**: Format strings, visibility, naming conventions
- **Maintenance**: Descriptions, calculation groups, unused objects

### Global and Per-Rule Control
![Screenshot showing BPA preferences with global enable/disable toggle and per-rule checkboxes](~/content/assets/images/features/bpa-built-in-rules-preferences.png)
You can enable or disable built-in rules globally or individually. Settings persist across sessions and work independently from your custom rules.

To manage built-in rules:
1. Go to **Tools** > **Preferences** > **Best Practice Analyzer**
2. Find the **Built-in Rules** section
3. Toggle **Enable Built-in Rules** to turn the entire collection on or off
4. Use the BPA Manager to enable or disable individual rules

### First-Run Notification
![Screenshot of first-run notification dialog introducing built-in BPA rules](~/content/assets/images/features/bpa-built-in-rules-notification.png)

The first time you open a model after upgrading to a version with built-in rules, you'll see a notification explaining the feature with a link to preferences. This notification only appears once.

### Knowledge Base Integration


![Screenshot showing BPA window with rule selected and "View Documentation" button highlighted](~/content/assets/images/features/bpa-built-in-rules-kb-link.png)

Every built-in rule links to a knowledge base article through the `KnowledgeBaseArticle` property. Each article explains what the rule checks, why it matters, and how to fix violations.

To view documentation, select a rule in the Best Practice Analyzer window.

### Read-Only Protection

Built-in rules can't be edited, cloned, or deleted. This ensures all users have the same rule definitions. You can disable individual rules, but the rule definitions themselves remain unchanged.

![Screenshot showing built-in rule with read-only badge/icon in BPA window](~/content/assets/images/features/bpa-built-in-rules-readonly.png)

### ID Collision Prevention

Built-in rules use reserved ID prefixes. When you create a custom rule, Tabular Editor validates that your ID doesn't conflict with built-in rules and shows an error if it does.

## Built-in Rules Catalog

The initial release includes the following rules:


### Error Prevention Rules
- [Avoid Invalid Characters in Object Names](xref:kb.bpa-avoid-invalid-characters-names)
- [Avoid Invalid Characters in Descriptions](xref:kb.bpa-avoid-invalid-characters-descriptions)
- [Expression Required for Calculated Objects](xref:kb.bpa-expression-required)
- [Data Column Must Have Source](xref:kb.bpa-data-column-source)
- [Relationship Columns Must Have Same Data Type](xref:kb.bpa-relationship-same-datatype)
- [Avoid Provider Partitions with Structured Data Sources](xref:kb.bpa-avoid-provider-partitions-structured)

### Performance Rules
- [Many-to-Many Relationships Should Use Single Direction](xref:kb.bpa-many-to-many-single-direction)
- [Hide Foreign Key Columns](xref:kb.bpa-hide-foreign-keys)
- [Set SummarizeBy to None for Numeric Columns](xref:kb.bpa-do-not-summarize-numeric)
- [Remove Auto Date Tables](xref:kb.bpa-remove-auto-date-table)
- [Remove Unused Data Sources](xref:kb.bpa-remove-unused-data-sources)

### Formatting Rules
- [Provide Format String for Measures](xref:kb.bpa-format-string-measures)
- [Provide Format String for Numeric and Date Columns](xref:kb.bpa-format-string-columns)
- [Visible Objects Should Have Descriptions](xref:kb.bpa-visible-objects-no-description)
- [Trim Object Names](xref:kb.bpa-trim-object-names)
- [Date Table Should Exist](xref:kb.bpa-date-table-exists)

### Maintenance Rules
- [Calculation Groups Should Contain Items](xref:kb.bpa-calculation-groups-no-items)
- [Perspectives Should Contain Objects](xref:kb.bpa-perspectives-no-objects)
- [Use Latest Power BI Compatibility Level](xref:kb.bpa-powerbi-latest-compatibility)


## Working with Built-in and Custom Rules

Built-in and custom rules work side by side:

| Feature | Built-in Rules | Custom Rules |
|---------|---------------|--------------|
| **Storage** | Hardcoded in application | JSON files or model annotations |
| **Updates** | Automatic with releases | Manual editing required |
| **Modification** | Read-only | Fully editable |
| **Documentation** | Integrated KB articles | User-provided descriptions |
| **Availability** | Enterprise Edition only | All editions |
| **Sharing** | Consistent across teams | Requires manual distribution |

### Recommended Workflow

1. Enable built-in rules for immediate coverage
2. Review violations and apply fixes
3. Disable rules that don't apply to your conventions
4. Add custom rules for organization-specific requirements
5. Use the "Ignore" feature for intentional violations

## Best Practices

### Onboarding Teams

When rolling out built-in rules to your team:
- Start with all rules enabled to establish a baseline
- Review violations together and agree on which rules apply
- Document why specific rules are disabled
- Add custom rules for organization-specific requirements

### Model Maintenance

- Run BPA before committing changes to version control
- Fix high-severity violations immediately
- Review medium and low-severity issues regularly
- Use automatic fixes where available

### Custom Rules

- Don't duplicate built-in rule functionality
- Use different ID prefixes to avoid conflicts
- Document your custom rules
- Share rule collections within your team

## Troubleshooting

### Built-in Rules Not Appearing

If built-in rules don't show in the BPA window:
1. Check that you're using Tabular Editor 3 Enterprise Edition
2. Verify that built-in rules are enabled in **Tools** > **Preferences** > **Best Practice Analyzer**
3. Restart Tabular Editor if you just changed preferences
4. Confirm your license is active

### Cannot Modify Built-in Rule

This is expected. Built-in rules are read-only. If you need different logic, create a custom rule with your expression and disable the corresponding built-in rule.

### ID Collision Error

Built-in rules reserve certain ID prefixes. Choose a different ID that doesn't start with `TE3_BUILT_IN`.

## Compatibility

- Requires Tabular Editor 3.24.0 or later
- Enterprise Edition only
- Works with all compatibility levels (1200+)

## Next Steps

- [Using the Best Practice Analyzer](xref:using-bpa)
- [BPA sample rules and expressions](xref:using-bpa-sample-rules-expressions)
- [Custom BPA rules](xref:best-practice-analyzer)