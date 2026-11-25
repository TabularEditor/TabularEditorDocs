---
uid: properties-view
title: Properties view
author: Morten Lønskov
updated: 2026-11-13
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
      note: "Property grid only, without the Basic and Advanced tabs"
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Using the Properties view in Tabular Editor

The Properties view shows the properties of the objects you select in the TOM Explorer and lets you edit them. In Tabular Editor 3, with the **Basic Properties view** public preview turned on, the view has two tabs at the bottom:

- **Basic**: a form with the fields Power BI Desktop shows in the **Properties** pane of its **Model view**, such as the name, description, display folder and format of a measure.
- **Advanced**: the property grid with every property of the object, a toolbar and a search box. It also lists the properties that Visual Studio and Power BI Desktop don't show.

> [!NOTE]
> The **Basic** and **Advanced** tabs are a public preview. Until you turn the preview on, the Properties view shows only the property grid described under [Advanced tab](#advanced-tab), as in Tabular Editor 2.

## Turn on the Basic tab

1. Go to **Tools > Preferences > Tabular Editor > Public Previews**.
2. Check **Basic Properties view**.
3. Click **OK**.

The Properties view shows the **Basic** and **Advanced** tabs. To go back to the property grid alone, clear **Basic Properties view**. See [Public Previews](xref:preferences#tabular-editor--public-previews).

## Choose a tab

Click **Basic** or **Advanced** at the bottom of the Properties view to switch tabs. The tab you click stays selected for every object and after a restart. **Show in Advanced**, **Show Advanced** and a jump to a property switch to **Advanced** without changing that choice, so after a restart the view opens on the tab you last clicked.

When you turn the preview on, the Properties view opens on **Basic**. If you turn the preview off and on again, it opens on the tab you had. To set the tab, change **Properties view tab** under **Basic Properties view** in **Tools > Preferences > Tabular Editor > Public Previews**.

## Basic tab

![Basic tab of the Properties view for a measure](~/content/assets/images/user-interface/properties-view-basic.png)

The **Basic** tab shows one field per property, with its label above it. A description gets a multi-line text box, an option such as **Is hidden** is a switch and a choice is a list. The lists use the names Power BI Desktop uses, such as **Date/time** for a data type or **Don't summarize** for a column's summarization. The **Basic** tab has no toolbar.

Single-line fields, such as lists and text boxes, are about 250 pixels wide at 100% scaling, so they line up. A field takes the width of the view when the value it shows is wider, and shrinks when the view is narrower. An open list can be wider than its field, so a long item doesn't widen the field. The **Description** box shows one line while its text is short, and grows to four lines as you type.

When the mouse pointer is over a list or the **Description** box, the mouse wheel scrolls the form. Click into **Description** to scroll its text.

A value you pick from an open list is applied at once. With the focus on a closed list, **Up**, **Down**, **Home**, **End** or a letter steps through the values without applying them. Press **Enter** or leave the field to apply the value, or press **Esc** to show the current value again. A list you can type into, such as **Data category** or **Compatibility level**, applies the value when you press **Enter**, leave the field or pick from the list, not while you type.

**Display folder** and a legacy data source's **Connection string** have a **...** button that opens the same dialog as on the **Advanced** tab: **Choose Folder** for a display folder, and the connection dialog for a connection string.

### Fields per object type

The fields depend on the type of the selected object:

| Object | Fields |
|---|---|
| Measure | **Name**, **Home table**, **Description**, **Display folder**, **Is hidden**, **Format**, **Expressions** |
| Column | **Name**, **Description**, **Display folder**, **Is hidden**, **Data type**, **Format**, **Sort by column**, **Data category**, **Summarize by**, **Is nullable**. An imported column also has **Source column**, first under **Data**. A calculated column has **Expressions**, before **Data**. |
| Table | **Name**, **Description**, **Is hidden**, **Key column**, **Data category**, **Storage mode**, **Expressions**, **Row level security**. A calculated table has **Expressions** before **Data**. |
| Calculation group | **Name**, **Description**, **Is hidden**, **Calculation items**, **Calculation group precedence** (with more than one calculation group), **Expressions** |
| Relationship | **From table**, **From column**, **Cardinality**, **To table**, **To column**, **Make this relationship active**, **Cross filter direction** |
| Hierarchy | **Name**, **Description**, **Display folder**, **Is hidden**, **Levels** |
| Level | **Name**, **Description**, **Column** |
| Calculation item | **Name**, **Description**, **Ordinal**, **Expressions** |
| KPI | **Description**, and a **Status**, **Target** and **Trend** section, each with its **Expression** box |
| Model | **Name**, **Description**, **Compatibility mode**, **Compatibility level**, **Cultures**, **Discourage implicit measures** |
| Role | **Name**, **Description**, **Model permission**, **Row level security** |
| Table permission | **Table** (read-only), **Expressions** |
| Partition | **Name**, **Description**, **Expressions** |
| Shared expression | **Name**, **Description**, **Expressions** |
| DAX User-Defined Function | **Name**, **Description**, **Is hidden**, **Expressions** |
| Calendar | **Name**, **Description**, **Column mappings** |
| Legacy data source | **Name**, **Description**, **Connection string** |
| Power Query data source | **Name**, **Description**, **Protocol**, the address fields that are set, such as **Server** and **Database**, **Authentication kind** |
| Perspective | **Name**, **Description**, **Edit in Perspective Editor** |
| Culture | **Language**, **Edit in Metadata Translation Editor** |
| Display folder, table group | **Name** |

Renaming a display folder moves its objects to the new folder, and renaming a table group moves its tables to the new group, as one undo step. This works the same way as renaming the folder or group in the TOM Explorer.

**Home table** moves a measure to another table, the same way as dragging it in the TOM Explorer. **Key column** sets the column that identifies the table's rows, and picking a column clears the flag from the column that had it. **Data category** sets the kind of data the table holds, such as **Time**. **Storage mode** sets the mode of the table's partitions to **Import**, **DirectQuery** or **Dual**. It's read-only for calculated, Direct Lake, push and policy range tables, and for tables whose partitions have different modes.

A field is read-only when the model doesn't allow the change. For example, while Tabular Editor is connected to a Power BI Desktop version that restricts the modeling operations external tools can make, **Home table**, **Levels** and **Calculation items** can be read-only. See [Supported modeling operations](xref:desktop-integration#supported-modeling-operations).

When the selected object has no fields on the **Basic** tab, such as a role member, the tab reads **This object has no basic properties.** Click **Show Advanced** to see its properties on the **Advanced** tab.

### Sections

When a form has more than one group of fields, the fields are in sections with a line between them:

- **General**: the name, description, display folder, visibility and the other fields of the object.
- **Formatting**: **Data type** and **Format**.
- **Data**: **Key column**, **Data category** and **Storage mode** on a table, and **Source column**, **Sort by column**, **Data category**, **Summarize by** and **Is nullable** on a column.
- **Connection**: the connection fields of a data source. See [Data sources](#data-sources).
- **Levels**: see [Hierarchy levels](#hierarchy-levels).
- **Calculation items**: see [Calculation items](#calculation-items).
- **Column mappings**: see [Calendar column mappings](#calendar-column-mappings).
- **Calculation group precedence**: see [Calculation group precedence](#calculation-group-precedence).
- **Status**, **Target** and **Trend**: see [KPIs](#kpis).
- **Expressions**: see [Expressions](#expressions).
- **Row level security**: see [Row level security](#row-level-security).

Click a section heading to fold the section, and click it again to unfold it. With the keyboard, press **Tab** to move to a heading and **Space** or **Enter** to fold it. A folded section stays folded for every object and after a restart. A form whose fields all belong to **General**, such as a relationship or the model, has no section headings.

The **Data**, **Levels**, **Calculation items**, **Column mappings**, **Calculation group precedence**, **Expressions** and **Row level security** headings have an info button. Click it, or press **F1** on the heading, to read what to do in the section. For most objects, the note also links to the documentation.

### Format

On a measure or column with a numeric or date/time data type, or a measure whose data type isn't known yet, **Format** lists the formats the **Advanced** tab offers, followed by **Custom**:

- for numbers: **General**, **Whole number**, **Decimal number**, **Currency**, **Percentage** and **Scientific**
- for dates: **General** and the date patterns

The text box under the list always shows the format string. Picking a number format keeps the decimals, thousands separator and negative number style of the current format string. To write your own format string, pick **Custom** or click the text box, type the format string and press **Enter** or leave the box. Press **Esc** to discard what you typed. The list shows the format that matches the format string, or **Custom** when no format matches.

A column with a text, true/false or binary data type has a text box for the format string, without the list. For the format string that **Currency** writes, see the **Localization** settings under @preferences.

### Relationships

A relationship's ends are **From table** and **From column**, and **To table** and **To column**. When you pick a table, its column list opens, so you can pick a column of that table. When you pick a **To table**, the column that matches the **From column** is picked for you, as in the **Edit Relationship** dialog. A column you pick is applied at once. A table without a column isn't applied, and leaving the end shows the relationship as it was. **Cardinality** sets both ends of the relationship, for example **Many to one (\*:1)**, and **Cross filter direction** offers **Single**, **Both** and **Automatic**.

A change is checked as in the **Edit Relationship** dialog, and the result shows as an icon beside the list:

- An error isn't applied. Picking the table at the other end is an error, because a relationship can't join a table to itself. The focus stays in the end until you correct it, or press **Esc** to show the relationship as it was.
- A warning is applied. A column of another data type, or a column that makes a second active relationship between the same two tables, gets a warning. Press **Ctrl+Z** to undo the change.

While Tabular Editor is connected to a model, the referential integrity check runs against the server only after you change a column, not when you select a relationship. On a Direct Lake model, it doesn't run.

### Hierarchy levels

The **Levels** section of a hierarchy lists its levels from the top, numbered. When a level's name differs from the name of its column, the column appears after the level's name. Edit the levels in the list:

| Action | Mouse | Keyboard |
|---|---|---|
| Move a level | Drag it to another position | **Alt+Up** or **Alt+Down** on the selected level |
| Rename a level | Double-click its name | **F2** on the selected level |
| Remove a level | Click the **x** on the level's row | **Delete** on the selected level |

To add a level, click **Add a level** and pick a column. The list shows the columns of the table that aren't in the hierarchy, and the column you pick becomes the lowest level. Each move, rename, removal or addition is one undo step.

See @object-properties-hierarchies for the properties of hierarchies and levels.

### Calculation items

The **Calculation items** section of a calculation group lists its calculation items in order, numbered. Move, rename and remove items the same way as hierarchy levels: drag an item or press **Alt+Up** or **Alt+Down**, double-click its name or press **F2**, and click its **x** or press **Delete**.

Click **Add a calculation item** to add an item at the end of the list. It opens in the Expression Editor, where you write its DAX. Each move, rename, removal or addition is one undo step.

A move numbers the **Ordinal** of every item from 0 in the new order, also when the ordinals started at 1 or had gaps. Expect every item's ordinal to show as changed in a diff of the model's files.

A calculation group has no **Key column**, **Storage mode** or **Row level security**, because the engine doesn't use them for calculation groups.

### Calculation group precedence

In a model with more than one calculation group, the form of a calculation group has a **Calculation group precedence** section, which lists every calculation group of the model from **Applied first** to **Applied last**. The group with the highest precedence is at the top, the selected group is in bold, and each group's precedence number is at the right. When more than one calculation group changes the same measure, the group higher in the list is applied first.

To change the order, drag a group to another position, or select it and press **Alt+Up** or **Alt+Down**. A move reassigns the precedence values the groups already have in the new order, so the groups outside the move keep theirs. When two groups share a precedence value, a move numbers every group instead, from 0 for the group applied last. Each move is one undo step.

See @object-properties-calculation-groups for the `Precedence` property.

### Calendar column mappings

The **Column mappings** section of a calendar shows one box with a line for each unit of time and its primary column. A unit with associated columns shows, for example, **+2 associated** after its column, and a **Time-related** line lists the time-related columns. Click the box to edit the mappings in the [Calendar Editor](xref:calendars). For a calendar without mappings, the box reads **No time units mapped. Click to map columns in the Calendar Editor.**

See @object-properties-calendars for the properties of calendars.

### Model

**Compatibility level** lists the model's current compatibility level and the higher levels Tabular Editor knows for the model's compatibility mode. For a Power BI model, that's the current level and the highest level Power BI supports. Pick a level from the list, or type one and press Enter or leave the box. If an object in the model needs a higher level than the one you enter, an error names the object and the level doesn't change. A change of compatibility level is one undo step. See @update-compatibility-level.

**Compatibility mode** is **Analysis Services** or **Power BI**. When you pick the other mode, **Compatibility level** lists the levels of that mode. If the model can't use the mode you pick, an error is shown and the mode doesn't change.

**Compatibility mode** and **Compatibility level** are read-only when the model doesn't allow the change.

**Cultures** is read-only and lists the model's cultures, with the model's own culture first, for example **en-US (model), da-DK**. A model without cultures shows **(none)**. To add or remove a culture, use the **Translations** node in the TOM Explorer. A culture's form has an **Edit in Metadata Translation Editor** button, and a perspective's form an **Edit in Perspective Editor** button, which open the editor on the selected culture or perspective.

### Data sources

A legacy data source shows its **Connection string**, with the password replaced by `********`. Edit the rest of the connection string and the data source keeps its password. Click **...** to build the connection string in the connection dialog.

A Power Query data source shows its **Protocol**, the parts of its address that are set, such as **Server** and **Database**, and its **Authentication kind**. A field you clear stays on the form, empty, until the model is saved, so you can type the new value. To set another part of the address, use the **Advanced** tab.

### KPIs

A KPI has a **Status**, a **Target** and a **Trend** section, each starting with its **Expression** box:

- **Status**: **Expression**, **Description** and **Graphic**
- **Target**: **Expression**, **Description** and **Format**
- **Trend**: **Expression**, **Description** and **Graphic**

Click an **Expression** box to write the expression in the Expression Editor. A section whose expression is empty is folded. A KPI has no **Expressions** section and no **Add an expression**.

### Expressions

The **Expressions** section shows the object's DAX, M and SQL expressions in boxes. Each box shows up to four lines of its expression and fades out when the expression is longer. A tag in the corner of the box names the language: **DAX**, **M** or **SQL**. An empty box has a dashed border. Click a box, or press **Enter** or **Space** when it has the focus, to open the expression in the **Expression Editor**. The cursor moves to the Expression Editor, so you can start typing at once.

The main expression of the object always has a box, for example a measure's **Expression** or a partition's query. When it's empty, the box reads, for example, **Not set. Click to write DAX in the Expression Editor.** The other expressions, such as **Format String Expression** and **Detail Rows Expression**, get a box when they're set.

To set another expression, click **Add an expression**. The list shows the expressions that aren't set yet, each with a line on what it's for. Some entries have a link to the page that explains them, for example **Detail rows expressions**, which opens [Detail Rows Expression](xref:detail-rows-expression). Pick an entry to add an empty box and open it in the Expression Editor. The empty box stays until you select another object.

The **Expressions** section appears when one object is selected, on every object type with expressions except a KPI. See [KPIs](#kpis).

### Row level security

Tables and roles have a **Row level security** section. On a table, it shows a box for each role that has a filter on the table. On a role, it shows a box for each table the role filters. Click a box to open the filter in the Expression Editor.

To add a filter, click **Add a filter for a role** on a table, or **Add a filter on a table** on a role, and pick the role or table. An empty filter is added and opens in the Expression Editor. The role's **Model permission** doesn't change. **Edit > Undo** removes the filter in one step.

See @data-security-setup-rls for how to write the filter.

### Select several objects

When you select several objects, the **Basic** tab shows the fields they have in common. The top of the form names how many objects are selected, for example **3 measures**, or **5 objects** when they have different types. A field whose value differs between the objects shows **(Multiple values)**. An edit sets the field on every selected object as one undo step, so **Ctrl+Z** reverts it on all of them.

These fields apply to one object at a time, and don't appear when several objects are selected:

- **Name** and **Key column**
- a level's **Column** and a calculation item's **Ordinal**
- a relationship's **From table**, **From column**, **To table** and **To column**
- a table permission's **Table**
- **Levels**, **Calculation items**, **Column mappings** and **Calculation group precedence**
- **Expressions**, the KPI **Expression** boxes and **Row level security**
- the **Edit in Perspective Editor** and **Edit in Metadata Translation Editor** buttons

### Properties on the Advanced tab

When the selected object has values in properties that only the **Advanced** tab shows, a line at the bottom of the form says how many, for example **3 advanced properties have values.** With several objects selected, the line counts the objects that have such values. Translations, perspective memberships, object-level security, custom annotations and options changed from their default count. Lineage tags, synonyms, read-only properties, values that Tabular Editor infers and the annotations that Power BI Desktop and Tabular Editor write don't count.

Click **Show in Advanced** to open the **Advanced** tab with **Only advanced properties with values** turned on, so the grid lists only those properties. To see every property again, turn off **Only advanced properties with values** on the toolbar, select another object or switch to **Basic**.

## Advanced tab

The **Advanced** tab is a property grid with every property of the selected object type, such as name, description, data type, format string, translations and annotations. For a description of each property, see @object-properties.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/properties-view.png" alt="Properties View" style="width: 500px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 1:</strong> Example of Properties for a table. Each object has different properties depending on its type </figcaption>
</figure>

On the **Advanced** tab, you can:

- view and modify the properties of any object in the model, such as tables, columns, measures, hierarchies, relationships, partitions, roles and perspectives.
- filter and sort the properties by name or category using the search box and the buttons at the top of the view.
- copy and paste property values between different objects using **Ctrl+C** and **Ctrl+V**.
- undo and redo property changes using **Ctrl+Z** and **Ctrl+Y**.
- navigate and edit properties with the keyboard. For example, press **Ctrl+Up** or **Ctrl+Down** to move between properties, **Enter** or **F2** to edit a property value and **Esc** to cancel editing.

> [!TIP]
> You can multi-select objects to see the properties they have in common and edit them in bulk. This can be useful for setting Format Strings, for example.

### Toolbar

The toolbar at the top of the **Advanced** tab contains the following buttons:

- **Categorized**: Groups the properties into categories such as *General*, *Metadata* and *Options*.
- **Alphabetical**: Lists all properties in a single, alphabetically sorted list.
- **Show changes**: Hides all properties that have not changed since the model was last saved, so that only the properties with [unsaved changes](xref:unsaved-changes) remain. While the filter is active, the title of the view reads **Properties (Changed)**.
- **Only advanced properties with values**: Lists only the properties that hold a value and don't appear on the **Basic** tab. The button shows only while the **Basic Properties view** preview is on. See [Properties on the Advanced tab](#properties-on-the-advanced-tab).
- **Property descriptions**: Shows or hides the description pane at the bottom of the view, which explains the currently selected property. For a full description of every property, see @object-properties.
- **Search box**: Filters the list of properties by name.

## Unsaved changes

On the **Advanced** tab, properties that differ from the last saved version of the model are drawn with a light orange row background. On the **Basic** tab, a changed field gets the same tint and a change icon after its label. A changed expression box gets the icon after its name. Changed rows in **Levels**, **Calculation items** and **Calculation group precedence** get the icon too. The **Levels**, **Calculation items**, **Column mappings**, **Calculation group precedence**, **Expressions** and **Row level security** headings get the icon when something in the section changed. When several objects are selected, a property is marked if any of the selected objects changed it.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/unsaved-changes/revert-property.png" alt="Properties view with unsaved changes" style="width: 500px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 2:</strong> A measure with unsaved changes to its Description and Format String. The <strong>Revert</strong> option puts a single property back to its saved value.</figcaption>
</figure>

On the **Advanced** tab, right-click a marked row and choose **Revert** to put that property back to the value it had at the last save, without touching any other unsaved changes. The revert is a single step on the undo stack, so **Ctrl+Z** brings the change back. See @unsaved-changes for details, including how to revert whole objects from the TOM Explorer, and how to turn the indicators off under **Tools > Preferences**.

## Docking

The Properties view is by default in the bottom right corner, but you can also open it by pressing F4 on your keyboard. You can also dock it to any side of the main window or undock it as a separate window.
