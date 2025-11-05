---
uid: find-replace
title: Find/Replace
author: Morten Lønskov
updated: 2023-03-22
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# Find
In Tabular Editor, you can use the advanced Find functionality to search for specific expressions throughout your open documents and dataset. The Find dialog box is accessible through the keyboard shortcut Ctrl+F.


<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/find-dialog.png" alt="Find Dialog Box" style="width: 300px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 1:</strong> Find window in Tabular Editor. Ctrl+F opens the dialog box </figcaption>
</figure>

To perform a search, define the expression you want to search for, and use the Options to determine if certain criteria should be met. For example, you can choose whether the case should match between your find expression and the found text or use regular expressions to search with.

## Look in
Additionally, you can specify where to Look in, different areas of your Tabular Editor instance, to limit or expand the scope of your search. The Look in options include:

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/find-dialog-look-in.png" alt="Find and Replace Dialog Box" style="width: 200px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 2:</strong> Find/Replace window in Tabular Editor. Ctrl+F opens the dialog box </figcaption>
</figure>

* _Selection_: Search within the selection in the current open document (Cannot search through your dataset)
* _Current document_: Search through the entire document that you currently have open (Cannot search through your dataset)
* _All open documents_: Searches all open documents (Cannot search through your dataset)
* _Entire model_: Searches the TOM Explorer for matches in your dataset. 
  + Allows for searching within the individual parts of your dataset such as Names, Expressions, Annotations etc. 
  + You can also search using Dynamic LINQ in this mode to, for example, find all columns that do not have summarize set to none.

> [!TIP]
> You can also use the search field in the TOM Explorer to search your dataset instead of the Find dialog

## Replace

The Replace dialog allows you in the same way as Find to search for an expression and then replace it with a different expression. 

The Replace dialog does not require anything in the _Replace with_ field, but leaving it empty will replace your searched for expression with an empty expression.
You have the same options as in the Find dialog to determine search criteria, but the _Look in_ functionality is only for documents, i.e. you cannot search and replace within your dataset objects. 

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/find-dialog.png" alt="Replace Dialog Box" style="width: 300px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 3:</strong> Replace window in Tabular Editor. Ctrl+F opens the dialog box </figcaption>
</figure>

> [!TIP]
> If you are trying to rename variables in a DAX statement (Expression or Script), Ctrl+R will let you refactor a selected variable