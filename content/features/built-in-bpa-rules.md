---
uid: built-in-bpa-rules
title: Built-in BPA Rules
author: Morten Lønskov
updated: 2026-11-13
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
description: 36 curated best practice rules hardcoded into Tabular Editor 3 with knowledge base integration.
---

# Built-in BPA Rules

## Overview

Tabular Editor 3 includes 36 built-in best practice rules. These rules cover common issues in semantic model development and are updated automatically with each release.

Unlike custom rules stored in JSON files, built-in rules:
- Are integrated directly into the application
- Update automatically with new releases
- Link to knowledge base documentation
- Are read-only to ensure consistency across teams
- Work immediately without configuration

## Key Features

### Rule Categories

The **Best Practice Analyzer** groups the built-in rules by category:
- **Error Prevention**: invalid characters, missing expressions and source columns, data type mismatches, MDX availability, user-defined function names
- **Performance**: MDX availability, date tables, many-to-many relationships, connection string application names
- **Maintenance**: descriptions, empty calculation groups and perspectives, unused data sources
- **Naming Conventions**: leading and trailing spaces in names
- **Formatting**: format strings, summarization of numeric columns, foreign key visibility
- **Model Layout**: translations
- **Governance**: Power BI compatibility level
- **Security**: role permissions and combinations of row-level and object-level security

### Global and Per-Rule Control
![Manage Best Practice Rules dialog with the Built-in Best Practices collection selected and its rules grouped by category, each with a checkbox](~/content/assets/images/features/bpa-built-in-rules-preferences.png)
You can enable or disable built-in rules globally or individually. Settings persist across sessions and work independently from your custom rules.

To manage built-in rules:
1. Go to **Tools > Preferences > Tabular Editor > Miscellaneous**.
2. Under **Best Practice Analyzer**, select or clear **Enable built-in best practice rules** to turn the entire collection on or off.
3. To enable or disable individual rules, open **Tools > Manage BPA rules...**, select the **Built-in Best Practices** collection and select or clear the checkbox of each rule.

### First-Run Notification
![Screenshot of first-run notification dialog introducing built-in BPA rules](~/content/assets/images/features/bpa-built-in-rules-notification.png)

The first time you open a model after upgrading to a version with built-in rules, you'll see a notification explaining the feature with a link to preferences. This notification only appears once.

### Knowledge Base Integration


![Best Practice Analyzer window with the tooltip of a rule open and the Learn more link highlighted](~/content/assets/images/features/bpa-built-in-rules-kb-link.png)

Every built-in rule links to a knowledge base article. Each article explains what the rule checks, why it matters and how to fix violations.

To open the article, hover over a rule in the **Best Practice Analyzer** window and click **Learn more** in the tooltip.

### Read-Only Protection

Built-in rules can't be edited, cloned, or deleted. This ensures all users have the same rule definitions. You can disable individual rules, but the rule definitions themselves remain unchanged.

![Screenshot showing built-in rule with read-only badge/icon in BPA window](~/content/assets/images/features/bpa-built-in-rules-readonly.png)

### ID Collision Prevention

Built-in rules use reserved ID prefixes. When you create a custom rule, Tabular Editor validates that your ID doesn't conflict with built-in rules and shows an error if it does.

## Built-in Rules Catalog

Each entry links to the rule's knowledge base article. The severity is shown in parentheses.

### Error Prevention Rules
- [Data Column Must Have Source](xref:kb.bpa-data-column-source) (3)
- [Expression Required for Calculated Objects](xref:kb.bpa-expression-required) (3)
- [Avoid Provider Partitions with Structured Data Sources](xref:kb.bpa-avoid-provider-partitions-structured) (2)
- [Relationship Columns Must Have Same Data Type](xref:kb.bpa-relationship-same-datatype) (3)
- [Avoid Invalid Characters in Object Names](xref:kb.bpa-avoid-invalid-characters-names) (3)
- [Avoid Invalid Characters in Descriptions](xref:kb.bpa-avoid-invalid-characters-descriptions) (3)
- [Set IsAvailableInMDX to True When Necessary](xref:kb.bpa-set-isavailableinmdx-true-necessary) (3)
- [Use Compound Names for User-Defined Functions](xref:kb.bpa-udf-use-compound-names) (1)

### Performance Rules
- [Set IsAvailableInMDX to False](xref:kb.bpa-set-isavailableinmdx-false) (3)
- [Date Table Should Exist](xref:kb.bpa-date-table-exists) (2)
- [Remove Auto Date Tables](xref:kb.bpa-remove-auto-date-table) (2)
- [Many-to-Many Relationships Should Use Single Direction](xref:kb.bpa-many-to-many-single-direction) (2)
- [Specify Application Name in Connection Strings](xref:kb.bpa-specify-application-name) (1)

### Maintenance Rules
- [Remove Unused Data Sources](xref:kb.bpa-remove-unused-data-sources) (1)
- [Visible Objects Should Have Descriptions](xref:kb.bpa-visible-objects-no-description) (1): five rules, for tables, columns, measures, calculation groups and user-defined functions
- [Perspectives Should Contain Objects](xref:kb.bpa-perspectives-no-objects) (1)
- [Calculation Groups Should Contain Items](xref:kb.bpa-calculation-groups-no-items) (2)

### Naming Conventions Rules
- [Trim Object Names](xref:kb.bpa-trim-object-names) (1)

### Formatting Rules
- [Set SummarizeBy to None for Numeric Columns](xref:kb.bpa-do-not-summarize-numeric) (3)
- [Hide Foreign Key Columns](xref:kb.bpa-hide-foreign-keys) (2)
- [Provide Format String for Numeric and Date Columns](xref:kb.bpa-format-string-columns) (2)
- [Provide Format String for Measures](xref:kb.bpa-format-string-measures) (2)

### Model Layout Rules
- [Translate Display Folders for All Cultures](xref:kb.bpa-translate-display-folders) (1)
- [Translate Descriptions for All Cultures](xref:kb.bpa-translate-descriptions) (1)
- [Translate Visible Object Names for All Cultures](xref:kb.bpa-translate-visible-names) (1)
- [Translate Hierarchy Level Names for All Cultures](xref:kb.bpa-translate-hierarchy-levels) (1)
- [Translate Perspective Names for All Cultures](xref:kb.bpa-translate-perspectives) (1)

### Governance Rules
- [Use Latest Compatibility Level for Power BI Models](xref:kb.bpa-powerbi-latest-compatibility) (3)

### Security Rules
- [Row-Level and Object-Level Security Require Read Permission](xref:kb.bpa-role-security-not-enforced) (3)
- [Power BI Roles Must Have Read Permission](xref:kb.bpa-powerbi-role-read-permission) (3)
- [Roles Without Security Override Secured Roles](xref:kb.bpa-role-unrestricted-read) (2)
- [Avoid Members in Both an RLS Role and an OLS Role](xref:kb.bpa-role-mixed-rls-ols-members) (3)

The security rules have no automatic fix.

## Working with Built-in and Custom Rules

Built-in and custom rules work side by side:

| Feature | Built-in Rules | Custom Rules |
|---------|---------------|--------------|
| **Storage** | Hardcoded in application | JSON files or model annotations |
| **Updates** | Automatic with releases | Manual editing required |
| **Modification** | Read-only | Fully editable |
| **Documentation** | Integrated KB articles | User-provided descriptions |
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
1. Verify that **Enable built-in best practice rules** is selected in **Tools > Preferences > Tabular Editor > Miscellaneous**
2. Restart Tabular Editor if you just changed preferences
3. Confirm your license is active

### Cannot Modify Built-in Rule

This is expected. Built-in rules are read-only. If you need different logic, create a custom rule with your expression and disable the corresponding built-in rule.

### ID Collision Error

Built-in rules reserve certain ID prefixes. Choose a different ID that doesn't start with `TE3_BUILT_IN`.

## Compatibility

Built-in rules apply to models with compatibility level 1200 and higher. Some rules require a higher level: the rule for members in both a row-level security role and an object-level security role requires 1400, and the two rules for user-defined functions require 1702. Each knowledge base article states the rule's compatibility level.

## Next Steps

- [Using the Best Practice Analyzer](xref:using-bpa)
- [BPA sample rules and expressions](xref:using-bpa-sample-rules-expressions)
- [Custom BPA rules](xref:best-practice-analyzer)