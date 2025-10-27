---
uid: script-create-m-parameter
title: Create M Parameter
author: Kurt Buhler
updated: 2023-02-28
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---

# Create M Partition

## Script Purpose

If you want to create a new dynamic M Parameter to use in Power Query queries (M Partitions or Shared Expressions).

## Script

### Create a new M Partition

```csharp
// This script creates a new M parameter in the 'Shared Expressions' of a model.
//
// Create a new shared expression called "New Parameter"
Model.AddExpression( 
    "New Parameter", 
    @"
""Parameter Text"" meta
[
	IsParameterQuery = true,
	IsParameterQueryRequired = true,
	Type = type text
]"
);

// Provides an output informing how to configure and use the parameter
Info ( 
    "Created a new Shared Expression called 'New Parameter', which is an M Parameter template." + 
    "\n------------------------------------------------------\n" + 
    "To configure:" +
    "\n------------------------------------------------------\n    " + 
    "1. Replace the text 'New Parameter' with the desired parameter value\n    " +
    "2. Set the data type appropriately\n    " +
    "3. Replace any values found in the M partitions with the parameter reference." );
```

### Explanation

This snippet creates a new M parameter in 'Shared Expressions' which you can refer to from within your M Partitions Power Query.

## Example Output

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-new-m-parameter.png" alt="An example of the Info box that appears to inform the user that the M Parameter was successfully created, and recommending next steps to configure / use it in the M Partitions." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 1:</strong> An example of the Info box that appears to inform the user that the M Parameter was successfully created, and recommending next steps to configure / use it in the M Partitions.</figcaption>
</figure>