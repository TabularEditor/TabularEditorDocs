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
<br>
<img src="~/images/Cscripts/script-create-new-m-parameter.png" alt="Image description" id="create-new-m-parameter">
<script>
    var img = document.getElementById("create-new-m-parameter");
    img.style.width = "600px";
</script>