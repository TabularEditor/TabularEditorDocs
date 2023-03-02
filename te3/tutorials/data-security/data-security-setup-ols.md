---
uid: data-security-setup-ols
title: Setup or Modify OLS
author: Kurt Buhler
updated: 2023-03-02
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# Setup or Modify Object-Level Security (OLS)


![Data Security Visual Abstract](~/images/data-security/data-security-configure-ols-visual-abstract.png)


---

__OLS is changed by adjusting the Roles or Object Permissions defined for Tables or Columns.__ Object Permissions are TOM Properties visible with the `Object Level Security` property that can be either `Default` (no OLS; functionally similar to `Read`), `Read`, or `None`. OLS differs from RLS in that it does not filter data, but prevents execution of the object __and all dependents.__ This means any relationship or measure that references the object where `Object Level Security` is set to `None` will return an error upon evaluation.

---

- [__About Data Security and RLS/OLS:__](data-security-about.md) A functional overview of <span style="color:#01a99d">RLS</span> & <span style="color:#8d7bae">OLS</span>.
- [__Modify/Setup an RLS Configuration:__](data-security-setup-rls.md) How to configure <span style="color:#01a99d">RLS</span> in a dataset.
- __Modify/Setup an OLS Configuration (This Article):__ How to configure <span style="color:#8d7bae">OLS</span> in a dataset.
- [__Testing RLS/OLS with Impersonation:__](data-security-testing.md) How to easily validate Data Security with Tabular Editor.

---

## Configuring OLS in Tabular Editor 3
_Below is an overview of common changes one might make to existing OLS. Additionally, strategies for configuring OLS for atypical objects (Measures, Calculation Groups) are described, below:_

---

### 1. Remove a Role
To remove a Role from the model, you can simply delete the Role object with `Del` or by right-clicking and selecting 'Delete'. 

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/images/data-security/data-security-delete-role.png" alt="Data Security Create Role" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 1:</strong> Deleting a Role in the model.</figcaption>
</figure>

> [!NOTE]
> All users assigned to this role will no longer be able to see model data, so long as at least one other Role exists. 

---

### 2. Add a New Role
To add a Role to the model: 
1. __Right-Click the 'Roles' Object Type:__ This will open the dialogue to let you create a new Role.
2. __Select 'Create' > 'Role':__ Name the new role.


<figure style="padding-top: 15px;">
  <img class="noscale" src="~/images/data-security/data-security-create-role.png" alt="Data Security Create Role" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 2:</strong> Creating a new Role in the model.</figcaption>
</figure>


3. __Set the `Model Permission` Property to `Read`:__ This is necessary for Power BI datasets.


<figure style="padding-top: 15px;">
  <img class="noscale" src="~/images/data-security/data-security-create-role.png" alt="Data Security Create Role" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 3:</strong> Setting the Model Permission property is necessary for Power BI.</figcaption>
</figure>


4. __Set Permissions:__ Set RLS Table Permissions and/or OLS Object Permissions, as described, below.

---

### 3. Remove OLS
To remove OLS from the model, all Columns and Tables must have their `Object Level Security` property configured to `Default` for all roles. To remove Data Security from the model, all Roles must be deleted.


<figure style="padding-top: 15px;">
  <img class="noscale" src="~/images/data-security/data-security-ols-default.png" alt="Data Security Create Role" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 4:</strong> The Object-Level Security property can be found in the <i>Properties</i> pane when selecting a Column or Table. The property does not exist for Measures, Relationships and other Object Types.</figcaption>
</figure>


> [!NOTE]
> Once all roles are deleted, all users will be able to see all data so long as they have _Read_ permissions on the dataset.

---

### 4. Setup or Change OLS
Setup or Modification of OLS is trivial for Columns and Table. You just have to select the object and navigate to the `Object Level Security` property, using the dropdown to change the property to the desired value.


<figure style="padding-top: 15px;">
  <img class="noscale" src="~/images/data-security/data-security-ols-change.png" alt="Data Security Create Role" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 4:</strong> The Object-Level Security property can be changed with an adjacent drop-down, allowing selection of <i>Default</i>, <i>None</i> or <i>Read</i>.</figcaption>
</figure>

--- 

### 5. Combine OLS with RLS
Successfully combining RLS with OLS requires designing a model and Data Security / Access Management strategy that align. Since RLS and OLS cannot combine across roles, this means if you plan on implementing both RLS and OLS, users are limited to a single role. 

---

### 6. Configure OLS for Measures
Natively, OLS works only on Columns, Tables and their dependents; there is no `Object-Level Security` property for measures. However, since OLS also applies to dependents, it is possible to design OLS that works on measures via disconnected tables or calculation groups. To do this, the measure DAX has to be altered to evaluate a column or calculation group configured with RLS. If the `Object-Level Security` property of that object is `None`, then the Measure will not evaluate. 