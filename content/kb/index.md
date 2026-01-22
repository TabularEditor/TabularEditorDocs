# Knowledge Base

This section contains articles about best practices, code analysis rules, and DAX optimization patterns for Tabular Editor and Power BI models.

## In this section

### Best Practice Rules (BPA)

Comprehensive guidelines for building high-quality, maintainable Power BI and Analysis Services models.

- @kb.bpa-avoid-invalid-characters-descriptions - Prevent metadata corruption by removing control characters from descriptions
- @kb.bpa-avoid-invalid-characters-names - Ensure object names contain only valid characters
- @kb.bpa-data-column-source - Verify all data columns have proper source mappings
- @kb.bpa-relationship-same-datatype - Enforce data type consistency in relationships
- @kb.bpa-visible-objects-no-description - Ensure all visible objects have meaningful descriptions
- @kb.bpa-trim-object-names - Remove leading and trailing spaces from names
- @kb.bpa-expression-required - Validate that calculated objects have expressions
- @kb.bpa-format-string-columns - Apply consistent formatting to numeric and date columns
- @kb.bpa-format-string-measures - Provide format strings for all measures
- @kb.bpa-do-not-summarize-numeric - Prevent inappropriate summarization of numeric columns
- @kb.bpa-date-table-exists - Ensure proper date table configuration
- @kb.bpa-hide-foreign-keys - Hide foreign key columns from end users
- @kb.bpa-many-to-many-single-direction - Enforce single-direction filtering in many-to-many relationships
- @kb.bpa-avoid-provider-partitions-structured - Use proper partition sources for structured data
- @kb.bpa-translate-descriptions - Support multi-language descriptions
- @kb.bpa-translate-display-folders - Localize display folder names
- @kb.bpa-translate-hierarchy-levels - Translate hierarchy level captions
- @kb.bpa-translate-perspectives - Localize perspective names
- @kb.bpa-translate-visible-names - Translate visible object names for all cultures
- @kb.bpa-perspectives-no-objects - Ensure perspectives contain relevant objects
- @kb.bpa-calculation-groups-no-items - Validate calculation group definitions
- @kb.bpa-set-isavailableinmdx-false - Control MDX availability of objects
- @kb.bpa-set-isavailableinmdx-true-necessary - Enable MDX availability when required
- @kb.bpa-remove-auto-date-table - Clean up auto-generated date tables
- @kb.bpa-remove-unused-data-sources - Eliminate unused data source definitions
- @kb.bpa-specify-application-name - Set application names in connection strings for monitoring
- @kb.bpa-powerbi-latest-compatibility - Maintain compatibility with latest Power BI features

## Code Actions
### DAX Code Analysis (DI)

Improvement suggestions for DAX code structure and efficiency. These rules identify opportunities to simplify and optimize your expressions.

- @DI001 - Remove unused variable
- @DI002 - Remove unused variable
- @DI003 - Remove table name
- @DI004 - Add table name
- @DI005 - Rewrite table filter as scalar predicate
- @DI006 - Split multi-column filter into multiple filters
- @DI007 - Simplify SWITCH statement
- @DI008 - Remove superfluous CALCULATE
- @DI009 - Avoid calculate shortcut syntax
- @DI010 - Use MIN/MAX instead of IF
- @DI011 - Use ISEMPTY instead of COUNTROWS
- @DI012 - Use DIVIDE instead of division
- @DI013 - Use division instead of DIVIDE
- @DI014 - Replace IFERROR with DIVIDE
- @DI015 - Replace IF with DIVIDE

### DAX Refactoring (DR)

Refactoring suggestions for complex or inefficient DAX patterns. These rules help modernize and improve readability of your DAX code.

- @DR001 - Convert to scalar predicate
- @DR002 - Use aggregator instead of iterator
- @DR003 - Use VALUES instead of SUMMARIZE
- @DR004 - Prefix variable
- @DR005 - Prefix temporary column
- @DR006 - Move constant aggregation to variable
- @DR007 - Simplify 1-variable block
- @DR008 - Simplify multi-variable block
- @DR009 - Rewrite using DISTINCTCOUNT
- @DR010 - Rewrite using COALESCE
- @DR011 - Rewrite using ISBLANK
- @DR012 - Remove unnecessary BLANK
- @DR013 - Simplify negated logic
- @DR014 - Simplify using IN

### DAX Rewrites (RW)

Suggested rewrites for specific DAX patterns that can be expressed more effectively using alternative syntax.

- @RW001 - Rewrite TOTALxTD using CALCULATE
- @RW002 - Rewrite using FILTER
- @RW003 - Invert IF

---
