---
uid: data-security-setup-rls
title: Setup or Modify RLS
author: Kurt Buhler
updated: 2023-03-14
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
# Configure Row-Level Security (RLS)


![Data Security Visual Abstract](~/content/assets/images/data-security/data-security-configure-rls-visual-abstract.png)


---

__RLS is changed by adjusting the Roles or Table Permissions defined for Tables.__ This DAX _Filter Expression_ can be viewed in the Expression Editor window when selecting a Table Permission within a particular role. This Filter Expression is the most important piece of the RLS configuration that determines what data is seen by a user.

---

- [__About Data Security and RLS/OLS:__](data-security-about.md) A functional overview of <span style="color:#01a99d">RLS</span> & <span style="color:#8d7bae">OLS</span>.
- __Modify/Setup an RLS Configuration (This Article):__ How to configure <span style="color:#01a99d">RLS</span> in a dataset.
- [__Modify/Setup an OLS Configuration:__](data-security-setup-ols.md) How to configure <span style="color:#8d7bae">OLS</span> in a dataset.
- [__Testing RLS/OLS with Impersonation:__](data-security-testing.md) How to easily validate Data Security with Tabular Editor.

---

## Configuring RLS in Tabular Editor 3
_Below is an overview of common changes one might make to existing RLS:_

---

### 1. Remove a Role
To remove a Role from the model, you can simply delete the Role object with `Del` or by right-clicking and selecting 'Delete'. 

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-delete-role.png" alt="Data Security Create Role" style="width: 550px;"/>
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
  <img class="noscale" src="~/content/assets/images/data-security/data-security-create-role.png" alt="Data Security Create Role" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 2:</strong> Creating a new Role in the model.</figcaption>
</figure>


3. __Set the `Model Permission` Property to `Read`:__ This is necessary for any members of the role to be able to access the dataset at all.


<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-model-permission-read.png" alt="Data Security Create Role" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 3:</strong> Setting the Model Permission property is necessary.</figcaption>
</figure>


4. __Set Permissions:__ Set RLS Table Permissions and/or OLS Object Permissions, as described, below.

---

### 3. Remove RLS
To remove RLS from the model, all Table Permissions must be deleted. To remove Data Security from the model, all Roles must be deleted. 


> [!NOTE]
> Once all roles are deleted, all users will be able to see all data so long as they have _Read_ permissions on the dataset.

---

### 4. Modify a Table Permission
To modify an existing Table Permission for a specific role:


1. __Expand the Role:__ This will reveal the Table Permissions. 
2. __Select the Table Permission:__ This will reveal the DAX for the Filter Permission in the Expression Editor.


<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-table-permissions-dax.png" alt="Data Security Create Role" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 4:</strong> The DAX Filter Expression is visible in the Expression Editor when selecting a Table Permission.</figcaption>
</figure>

3. __Adjust the Filter Expression / RLS Table Permissions:__ It is recommended that you test / validate the DAX before using it:
  - Copy the Filter Expression to a new DAX Query window under an `EVALUATE` statement.
  - Add it as the Expression of an `ADDCOLUMNS` statement iterating over Table, or part of the table.
  - Execute it and observe the results.
  - Replace `USERNAME()` or `USERPRINCIPALNAME()` in dynamic RLS with a known value from the Security Table.
  - Re-run the DAX Query and validate that the results appear as expected. Repeat until satisfied.


<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-rls-validation.png" alt="Data Security Validation" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 5:</strong> An example of how RLS can be validated from the DAX query window by using the Filter Expression inside of an Iterator over the Table (or part of the table, like the user alias). In this example, the original RLS Filter Expression in the Table Permission has been modified (Yellow) where an explicit User Principal Name in the dataset is added instead, to test (Green). The RLS code is executed inside of the ADDCOLUMNS iterator over a relevant part of the table. The checkmark indicates any row that evaluates to TRUE. The test demonstrates that the RLS is - for this UPN - working as expected, since <i>Gal Aehad</i> is the only user returning TRUE when their UPN is given.</figcaption>
</figure>

```dax
EVALUATE

// Create a table to test your RLS
ADDCOLUMNS ( 
  VALUES ( 'Regions'[Territory Directors] ),
  "@RLS-Validation",

    // RLS Code
    VAR _CurrentUser = 
      SELECTCOLUMNS (
        FILTER ( 
          'Employees', 
          'Employees'[Employee Email]

            // Replace USERPRINCIPALNAME() with a user email to test
            = "gal.aehad@spaceparts.co" // USERPRINCIPALNAME ()
        ),
        "@Name", 'Employees'[Employee Name]
      )
    RETURN
      'Regions'[Territory Directors] IN _CurrentUser

)

// Order from TRUE() to FALSE()
// Where it is TRUE() the data will be visible
ORDER BY [@RLS-Validation] DESC
```

---

### 5. Add a New Table Permission to a Role
To add a new table permission:


1. __Right-Click the Role:__ Select 'Add table permission...'

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-table-permissions.png" alt="Data Security Create Role" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 6:</strong> In Tabular Editor, Table Permissions for RLS are visible under the role. New table permissions can be created by right-clicking a Role and selecting <i>'Add Table Partition...'</i></figcaption>
</figure>

2. __Select the Table and press 'OK':__ Select the table for which you want to create the permission.
3. __Write the Filter Expression / RLS Table Permissions:__ Write the DAX for the filter expression. As above, you want to validate this filter expression (See __Figure 5__):
  - Copy the Filter Expression to a new DAX Query window under an `EVALUATE` statement.
  - Add it as the Expression of an `ADDCOLUMNS` statement iterating over Table, or part of the table.
  - Execute it and observe the results.
  - Replace `USERNAME()` or `USERPRINCIPALNAME()` in dynamic RLS with a known value from the Security Table.
  - Re-run the DAX Query and validate that the results appear as expected. Repeat until satisfied.

---

### 6. Assign or Remove Users from a Role
You can assign and remove users/groups from roles through Tabular Editor.

  1. Right-Click the __Role__, select __Edit members__...
  
<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-edit-members.png" alt="Data Security Create Role" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 7:</strong>Users can be assigned to roles by right-clicking a Role and selecting <i>'Edit members...'.</i></figcaption>
</figure>

  2. Click the __dropdown button__ on the 'Add Windows AD Member' button and choose __Azure AD Member__:

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-edit-members-dialog.png" alt="Data Security Create Role" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 8:</strong> For AAS/SSAS models, users can be added via the <i>'Edit members...'</i> dialog box.</figcaption>
</figure>

  3. Specify the Azure AD user identity (typically, the user e-mail address) as the __Member Name__ property.
  4. Click __OK__.
  5. __Save__ the model.

> [!IMPORTANT]
> If your organisation is using on-premises Active Directory with SQL Server Analysis Services, you will need to use the __Windows AD Member__ option instead of __Azure AD Member__.

> [!NOTE]
> Once a Power BI dataset has been published to the Power BI Service, you can also manage role members through the [Dataset Security settings](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls#manage-security-on-your-model). Alternatively, you can manage role members through [SQL Server Management Studio](https://learn.microsoft.com/en-us/analysis-services/tabular-models/manage-roles-by-using-ssms-ssas-tabular?view=asallproducts-allversions) (this applies to AAS/SSAS models in addition to Power BI dataset).

---
