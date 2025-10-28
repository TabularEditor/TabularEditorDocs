---
uid: udfs
title: DAX User-Defined Functions
author: Daniel Otykier
updated: 2025-09-15
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# DAX User-Defined Functions

DAX User-Defined Functions (UDFs) is a new capability of semantic models introduced in Power BI Desktop with the September 2025 update.

The feature lets you create reusable DAX functions that you can invoke from within any DAX expression of your model, even other functions. This powerful feature helps you maintain consistency, reduce code duplication, and create more maintainable DAX expressions.

Tabular Editor 3 supports UDFs starting from version 3.23.0, although we recommend using [3.23.1](xref:release-3-23-1) (or newer) to benefit from various bug fixes and improvements.

For a more detailed introduction to UDFs in Tabular Editor 3, check out [this blog post](https://tabulareditor.com/blog/how-to-get-started-using-udfs-in-tabular-editor-3).

## Understanding UDFs

UDFs can be thought of as custom DAX functions that you define once and can use throughout your model. You define which parameters the function accepts, which can be both scalar- or table-valued, or even references to objects, and then you provide the DAX expression that uses those parameters to compute a result, which can also be scalar- or table-valued.

To learn more about how DAX UDFs work, we recommend [this article by SQLBI](https://www.sqlbi.com/articles/introducing-user-defined-functions-in-dax/).

## Prerequisites

Before you can create and use UDFs in Tabular Editor 3, ensure that:

- Your model compatibility level is **1702 or higher**

## Creating Your First UDF

### Step 1: Set Up the Model

First, verify your model's compatibility level is appropriate for UDFs:

1. Open your model in Tabular Editor 3
2. Select the root node ("Model") in the **TOM Explorer**
2. In the **Properties** panel, expand the **Database** property, then check that the **Compatibility Level** is set to **1702** or higher
3. If needed, update the compatibility level and save your model

![Setting Compatibility Level](~/content/assets/images/udfs-cl1702.png)

### Step 2: Add a New Function

1. In the **TOM Explorer**, locate the **Functions** folder under your model
2. Right-click on the **Functions** folder
3. Select **Create > User-Defined Function**
4. Give your function a descriptive name (spaces and special characters are not allowed; underscores and periods are permitted)

![Creating a UDF](~/content/assets/images/new-udf.png)

You can also add a UDFs through the **Model > Add User-Defined Function** menu option.

Alternatively, you can create UDFs directly from the **DEFINE** section of a DAX query, by hitting F7 (Apply) or using the **Query > Apply** menu option. If your query contains multiple query-scoped definitions, you can also select just a subset of them and hit F8 (Apply Selection).

![Creating a UDF from DAX Query](~/content/assets/images/udf-from-query.png)

### Step 3: Define Your Function

In the **Expression Editor**, define your function using proper UDF syntax.

Here's a basic example that adds two numbers together:

```dax
// Adds two numbers together
(
    x, // The first number
    y  // The second number
)
=> x + y
```

> [!TIP]
> Use the **"Use correct UDF syntax"** code action in the Expression Editor if you need help with the proper syntax structure.

## UDF Syntax and Structure

### Basic Syntax

UDFs follow this general structure:

```dax
FUNCTION FunctionName =
    // Optional comment describing the function
    (
        parameter1, // Parameter description
        parameter2, // Parameter description
        // ... more parameters
    )
    => expression_using_parameters
```

### Parameter Evaluation Mode

A key aspect of UDFs is that parameters can be defined in one of two modes, **pass-by-value** and **pass-by-reference**. By default, and unless you specify otherwise, a parameter will by **pass-by-value**. This essentially means that the parameter behaves just like a DAX variable (i.e. one that is defined using the `VAR` keyword) inside the UDF expression. In other words, when the UDF is called, the parameter values are "copied" into the function and any reference to that parameter inside the function will always return the same value.

In contrast, **pass-by-reference** parameters behave more like measures. That is, the result of evaluating the parameter *inside the function* may differ depending on the evaluation context.

To specify the evaluation mode, include a parameter specification after the parameter name, separated by a colon (`:`). The specification can be either `VAL` or `EXPR` for "pass-by-value" and "pass-by-reference", respectively. As mentioned above, "pass-by-value" is the default, so `VAL` is implicit if not specified. For example:

```dax
(
    x: VAL,   // Pass-by-value parameter - the DAX expression is evaluated once when the function is called, and the result is "copied" into the function
    y: EXPR   // Pass-by-reference parameter - can be any DAX expression which will observe whatever context the parameter is later referenced under
)
=>
ROW(
    "x", x,
    "x modified", CALCULATE(x, Product[Color] = "Red"),
    "y", y, 
    "y modified", CALCULATE(y, Product[Color] = "Red")
)
```

Calling the above function with a measure reference for each parameter, e.g. `MyFunction([Some Measure], [Some Measure])`, will yield different results for the `y` parameter depending on the current filter context, as shown in the screenshot below:

![Pass-by-value vs Pass-by-reference](~/content/assets/images/udf-pass-by-ref.png)

In addition to specifying the evaluation mode, you can also constrain the parameter type by specifying a data type before the evaluation mode, e.g. `x: INT64 VAL` or `y: TABLE EXPR`.

These type specifications are optional, but if specified they will perform an implicit type conversion on arguments passed to the function, and will also affect the autocomplete suggestions in Tabular Editor 3 when writing DAX code that calls the function.

Check the [Microsoft specification for UDFs](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions) for the complete list of available constraints.

## Using UDFs in Your Model

### In Object Expressions

Once you've created a UDF, you can use it in any DAX expression throughout your model. Tabular Editor 3's autocomplete will suggest your UDFs as you type.

### In DAX Scripts

UDFs are also available when working with DAX Scripts:

```dax
-- Function: MyFuncRenamed
FUNCTION MyFuncRenamed =
    // Adds two numbers together
    (
        x: INT64, // The first number
        y: INT64  // The second number
    )
    => x + y

-- Measure: [New Measure]
MEASURE 'Date'[New Measure] = MyFuncRenamed(1,2)
```

### In DAX Queries

Tabular Editor 3 adds powerful new features for working with UDFs in DAX queries. We already mentioned above how you can "apply" a UDF from the **DEFINE** section of a DAX query, to have it become a permanent part of your model. In addition, if using a UDF inside a DAX query, you can right-click on the function invocation and choose **Define Function** to automatically generate the function definition in the **DEFINE** section of your query:

![Define Function from Query](~/content/assets/images/udf-define.png)

As can be seen from the screen above, the following options are available when right-clicking on a UDF invocation:

- **Peek Definition** (Alt+F12): Opens a nested, read-only editor below the current cursor position, showing you the function definition
- **Go To Definition** (F12): Navigates to the function definition in the **Functions** folder of your model, or, if the function is defined in the current query or script, to the function definition inside the editor
- **Inline Function**: Replaces the function invocation with the actual function definition, substituting parameters with the actual arguments passed to the function
- **Define Function** (DAX scripts or DAX queries only): Generates the function definition in the **DEFINE** section of your query, if it doesn't already exist there
- **Define Function with dependencies** (DAX scripts or DAX queries only): Similar to the above, but also generates definitions for any other UDFs that the function depends on

## Advanced Features

### Formula Fixup

When you rename a UDF, Tabular Editor 3 automatically updates all references throughout your model, just like with measures and other objects.

### Peek Definition

The **Peek Definition** feature works with UDFs, allowing you to quickly view the function's implementation without navigating away from your current context.

![Peek Definition for UDFs](~/content/assets/images/udf-peek-definition.png)

### Dependencies View

UDFs appear in the **DAX Dependencies** (Shift+F12) view, showing both:
- **Objects that depend on the function**: Which measures, columns, etc. use the UDF
- **Objects the function depends on**: Which measures, columns, etc. the UDF references

### Batch Rename

When you select multiple UDFs in the TOM Explorer, you can use the **Batch Rename** (F2) option from the right-click context menu to rename them all at once, using search-and-replace patterns, and optionally regular expressions.

### Namespaces

The concept of "namespace" doesn't exist in DAX, yet the recommendation is to name UDFs in such a way that ambiguities are avoided and that the origin of the UDF is clear. For example `DaxLib.Convert.CelsiusToFahrenheit` (using '.' as namespace separators). When a UDF is named this way, the TOM Explorer will display the UDF in a hierarchy based on the names. You can toggle the display of UDFs by namespace using the **Group User-Defined Functions by namespace** tuggle button in the toolbar above the TOM Explorer (note, this button is only visible when working with a model using Compatibility Level 1702 or higher).

![DAX UDFs grouped by namespace](~/content/assets/images/udf-namespaces-tom-explorer.png)

In Tabular Editor, UDFs also have a "Namespace" *property*, allowing you to customize the namespace of each UDF individually, without changing the actual UDF object name. This is very similar to Display Folders for measures. Setting a different value for the "Namespace" property, than would could be inferred from the UDF name, is useful for example if you want to batch rename (F2) multiple UDFs to get rid of the namespaces in their names, but you still want to keep them nicely organized in the TOM Explorer.

> [!NOTE]
> This organizational feature in Tabular Editor doesn't affect DAX code. You still need to type out the full UDF name when calling a UDF, including any namespace parts.

## Best Practices

### Naming Conventions
- Use descriptive names that clearly indicate the function's purpose
- Consider prefixing UDFs with your organization's initials (e.g., `ACME.CalculateDiscount`)
- Avoid generic names that might conflict with future DAX functions

### Documentation
- Always include comments describing what the function does
- Document each parameter's purpose and expected data type
- Include usage examples in your comments

```dax
// Calculates the percentage change between two values
// Usage: PercentChange(100, 110) returns 0.10 (10% increase)
(
    oldValue: DOUBLE,    // The original value
    newValue: DOUBLE     // The new value to compare against
)
=> DIVIDE(newValue - oldValue, oldValue)
```

Tabular Editor 3 automatically picks up any comments and displays them appropriately in autocomplete suggestions and tooltips.

![UDF Autocomplete with Comments](~/content/assets/images/udf-comment-tooltips.png)

## Common Use Cases

### Mathematical Operations
```dax
// Calculate compound interest
(
    principal: DOUBLE,
    rate: DOUBLE,
    periods: INT64
)
=> principal * POWER(1 + rate, periods)
```

### String Manipulation
```dax
// Format a full name from first and last name components
(
    firstName: STRING,
    lastName: STRING
)
=> TRIM(firstName) & " " & TRIM(lastName)
```

### Date Calculations
```dax
// Get the fiscal year based on a date (fiscal year starts July 1)
(
    inputDate: DATETIME
)
=> IF(MONTH(inputDate) >= 7, YEAR(inputDate) + 1, YEAR(inputDate))
```

### Business Logic
```dax
// Apply tiered discount based on quantity
(
    quantity: INT64
)
=> SWITCH(
    TRUE(),
    quantity >= 100, 0.15,
    quantity >= 50,  0.10,
    quantity >= 25,  0.05,
    0
)
```

## Troubleshooting

### Common Issues

**Function not appearing in autocomplete**
- Verify the function was saved successfully
- Check that there are no syntax errors in the function definition
- Ensure you're using the function in a compatible context

**Parameter constraint errors**
- Review the parameter types you've specified
- Make sure you're passing compatible values to the function
- Check the Microsoft documentation for supported constraint types

**Function not working after deployment**
- Verify your target environment supports UDFs (compatibility level 1702+). As of September 16th, 2025, the Power BI Service does not yet support UDFs, nor does Azure Analysis Services or SQL Server Analysis Services.

## Limitations

- UDFs are currently a preview feature and may have limitations in certain deployment scenarios
- Not all Power BI environments support UDFs (requires specific builds)
- UDFs cannot be recursive (call themselves)
- UDFs do not support optional parameters, parameters with default values, or parameter overloading

---

UDFs in Tabular Editor 3 provide a powerful way to create reusable, maintainable DAX code. By following these guidelines and best practices, you can build a library of functions that will improve your model's consistency and reduce development time.