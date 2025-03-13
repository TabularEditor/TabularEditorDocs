---
uid: messages-view
title: Messages view
author: Daniel Otykier
updated: 2021-09-08
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# Messages view

The Messages view in Tabular Editor 3 is a tool window that displays various types of messages related to the current dataset. 

> [!TIP]
> You can double-click on a message to jump to the source of the error in the model tree or script editor.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/assets/images/user-interface/messages-view.png" alt="Message View" style="width: 500px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 1:</strong> Messages window in Tabular Editor. Provides an overview of all warnings and errors in your dataset </figcaption>
</figure>


The Messages view will tell you the Source and the object from which the message is being generated. 

There are two types of messages displayed Errors and Warnings
- Errors: This tab shows any errors that prevent your model from being deployed or saved. For example, if you have an invalid expression in a calculation item or a circular dependency in a relationship. 
- Warnings: This tab shows any warnings that does not concur with standards but does not prevent your model from being usable. This is for example having fully qualified measure references.