---
uid: data-security-testing
title: Testing RLS/OLS
author: Kurt Buhler
updated: 2023-03-02
applies_to:
  editions:
    - edition: Desktop
      none: x
    - edition: Business
    - edition: Enterprise
---

# Testing Data Security with Impersonation

![Data Security Visual Abstract](~/content/assets/images/data-security/data-security-testing-visual-abstract.png)

---

**DAX Queries**, **Pivot Grid**, or **Preview Data** enable testing of Data Security in Tabular Editor. It is recommended to _always_ test Data Security with any changes to configuration, to mitigate risk of incorrect RLS/OLS implementation and the consequences thereof.

> [!IMPORTANT]
> Testing Data Security with Impersonation using Tabular Editor 3 is limited to datasets hosted in an Analysis Services instance or the Power BI Service. Tabular Editor 3 Desktop Licenses cannot benefit from this feature.

---

- [**About Data Security and RLS/OLS:**](data-security-about.md) A functional overview of <span style="color:#01a99d">RLS</span> & <span style="color:#8d7bae">OLS</span>.
- [**Modify/Setup an RLS Configuration:**](data-security-setup-rls.md) How to configure <span style="color:#01a99d">RLS</span> in a dataset.
- [**Modify/Setup an OLS Configuration:**](data-security-setup-ols.md) How to configure <span style="color:#8d7bae">OLS</span> in a dataset.
- **Testing RLS/OLS with Impersonation (This Article):** How to easily validate Data Security with Tabular Editor.

---

## Testing with Impersonation

**Data Security can be easily tested using _Impersonation_ in Tabular Editor 3.** Impersonation is a feature that lets you view a query result as a model Role or User. It is similar to the _'View As Role...'_ feature in the Power BI service, with two key differences:

1. The End-User being impersonated requires **dataset Build permissions** in addition to Role assignment & Dataset Read access.
2. Any query can be executed within Tabular Editor 3; it is not limited to available report visuals, as in the Power BI Service.

This is valuable, as it lets the developer run defined tests to see how the result would be viewed by any end-user with Build permissions. This helps ensure that even for complex queries and DAX expressions, the Data Security works as expected, and users only see what they should see.

> [!IMPORTANT]
> Ensure that Build permissions are not provisioned by providing end-users Workspace Roles (Contributor, Member, Admin), as these roles have **Write** permissions to the dataset and thus bypass Data Security; the testing will appear to not work, even if it's configured correctly.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-impersonation-demo.gif" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 1:</strong> A demonstration of RLS testing in Tabular Editor using impersonation. Shown is testing with (A) Data Preview, (B) DAX Queries and (C) Pivot Grid.</figcaption>
</figure>

---

## How to Test with Impersonation

To test with impersonation, follow the below steps:

1. **Ensure that the Dataset Configuration & Access is correct:**
   End-users being impersonated...

- _...have been assigned to the appropriate **Roles**._
- _...have been provisioned **Dataset Read Access**._
- _...have been provisioned **Dataset Build Access**. (Power BI)_
- _...**are not** Workspace Contributors, Members or Admins (Power BI)_.

2. **Create a new DAX Query, Pivot Grid or Preview Data window:**

- It's recommended that you start with _Preview Data_ to observe the effect on model tables
- Thereafter, perform a second validation with a _DAX Query_. This is because DAX Queries can be saved for documentation and later reference, if a change occurs in the model requiring re-testing.

3. **Select 'Impersonation' and enter the User e-mail**: If you have implemented _Static RLS_, you can test the role, instead.

4. **Explore the data to validate that the results appear as expected:** (according to the Security Rules).

### Tips for Testing

1. **Test more than one user:** It's recommended you test at least 3-10 different users per Role. You can also automate the testing to iterate through each UPN in the Security Table (i.e. using C# Scripting and Macros).

2. **Test each Role & Table Permission:** Since each Table Permission represents a different DAX Filter Expression, they all have to be tested, separately. Ensure that each Role is tested, and that each test includes the relevant tables with configured Filter Expressions. For example, if a Role consists of table expressions on the 'Customers' and 'Products' table, ensure your query includes attributes from both tables for validation purposes.

3. **Test many Queries/Measures:** Try to find complex queries to test, particularly those which might be problematic in the context of Data Security. For example, if calculations require comparing to a total, unfiltered average (i.e. % of total) and it's expected that _that total_ is not filtered in RLS, the developer may need to re-think the Data Security implementation as a function of the model.