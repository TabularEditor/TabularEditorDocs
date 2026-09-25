---
uid: deploy-current-model
title: Deploy the loaded model
author: Morten Lønskov
updated: 2026-09-15
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Deploy the loaded model

Deployment pushes the model you have open to a server, either creating a new database or overwriting an existing one. It's how you get a model held in a `.bim` file or a folder onto a server, and how you promote a model from one environment to the next.

Open the wizard with **Model > Deploy...**, choose the destination server and database, then choose how much of the model to send.

## What each option controls

The wizard's value is in what it lets you _leave alone_ on the destination. Each option is a decision about whether the destination keeps its own version of something:

- **Deploy Model Structure** sends the model metadata. This is the deployment itself; clearing it leaves nothing to do.
- **Deploy Data Sources** sends explicit data sources. Clear it to keep the destination's own connection strings and credentials, which is usually what you want when promoting from development to test.
- **Deploy Table Partitions** synchronizes partitions with the model metadata. Clear it to leave existing partitions, and the data in them, untouched. With it enabled, partitions on the destination that aren't in the model are removed along with their data.
  - **Deploy partitions governed by Incremental Refresh Policies** appears when the option above is enabled, and lets you deploy every partition _except_ those an incremental refresh policy generates.
- **Deploy Model Roles** sends the roles defined in the model. Clear it to keep the destination's roles as they are.
  - **Deploy Model Role Members** sends role membership. Role members are commonly managed on the server rather than in the metadata, so clearing this is normal.

@deployment covers all of this in detail, along with the TMSL script the wizard generates, what a deployment does to data already in the destination, and how to deploy from the command line or a pipeline.

> [!NOTE]
> Deploying is not the same as saving. If you opened the model from a server, **File > Save** writes back to _that_ database, as described in @connect-ssas. Use deployment when the destination is somewhere else.
