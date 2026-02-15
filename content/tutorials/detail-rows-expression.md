---
uid: detail-rows-expression
title: Detail Rows Expression
author: Just Blindbæk
updated: 2026-02-15
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
# Implementing Detail Rows Expressions

## Overview
Introduce what a Detail Rows Expression is and why customizing drillthrough results improves the consumer experience.  
Explain that the walkthrough uses Tabular Editor 3, but everything shown can also be done in Tabular Editor 2.

## Prerequisites
Before you begin, you should have:
- Tabular Editor 3 (or 2)
- A model that contains at least one measure
- Basic familiarity with DAX table expressions
- Excel to test drillthrough

## What You Will Build
Briefly describe the end result.  
Example: selecting a measure and controlling exactly which columns and rows users see when they drill to details.

## Understanding Detail Rows Expressions
Explain:
- Measure-level vs table-level expressions
- What happens if nothing is defined
- How client tools use the expression

Keep it conceptual – implementation comes later.

## Where to Configure Detail Rows in Tabular Editor
Describe where the property is located.

### Measures
- Select a measure
- Locate the **Detail Rows Expression** property

### Tables
- Select a table
- Locate the default expression

Mention any UI differences between TE3 and TE2.

## Creating a Basic Detail Rows Expression
Step-by-step tutorial.

1. Select a measure.
2. Open the property.
3. Enter a simple DAX table expression.
4. Save the model.

Provide a minimal code example placeholder.

## Testing the Result
Explain how to:
- Deploy / save
- Open the report or PivotTable
- Trigger drillthrough
- Verify columns & filters

## Overriding a Table Default with a Measure Expression
Demonstrate precedence and when to use each.

## Using Existing Logic with the DETAILROWS Function
Show how one expression can reference another to avoid duplication.

## Practical Patterns
Short subsections with common real-world needs.

### Returning Only Business-Friendly Columns
### Adding Calculated Columns
### Filtering to Relevant Transactions

## Tips for Working Efficiently
Ideas such as:
- Use DAX formatting
- Store reusable snippets
- Keep expressions readable
- Prefer measure-level control when semantics differ

## Compatibility with Tabular Editor 2
Clarify what is identical and what differs in navigation or UX.

## Troubleshooting
Examples:
- Drillthrough returns unexpected columns
- Expression not picked up
- Errors due to row/context assumptions

## Summary
Reiterate the benefit: better governed, predictable drillthrough experiences, authored centrally in the model.

## Further Reading
Link to external deep dives and conceptual articles.
- [DAX Guide: DETAILROWS](https://dax.guide/detailrows/)
- [Microsoft Docs: Detail Rows Expressions](https://docs.microsoft.com/en-us/analysis-services/tabular-models/detail-rows-expressions)