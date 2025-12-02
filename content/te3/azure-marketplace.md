---
uid: azure-marketplace
title: Purchase via Azure Marketplace
author: Peer Grønnerup
updated: 2025-12-02
---
# Purchase Tabular Editor 3 through the Azure Marketplace

Tabular Editor 3 is available on the Azure Marketplace as a public offer. This document provides an overview of how to streamline your purchase by acquiring Tabular Editor 3 directly through the Azure Marketplace.

## Requirements
To purchase Tabular Editor via the Azure Marketplace, you need:
- An Azure subscription (verify if you already have a subscription or create a new subscription)
- An Azure AD account with at least Contributor role for the Azure subscription

Also ensure these [prerequisites](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/enable-marketplace-purchases) are met before proceeding with the purchase of Tabular Editor 3 through the Azure Marketplace.

## How to purchase Tabular Editor 3 in the Azure Marketplace

Follow this procedure to purchase Tabular Editor 3 licenses through the Azure Marketplace:

1. Sign in to the [Azure Portal](https://portal.azure.com/)
2. Navigate directly to the Marketplace page or search for "Marketplace" using the search box at the top of the page.
3. On the Azure Marketplace page, search for "Tabular Editor 3" and click on the Tabular Editor 3 offering.
4. Select your subscription and license plan, then click **Subscribe**.
    
   ![Azure Marketplace Subscribe to offer](~/content/assets/images/azuremarketplace-offer-page.png)

   > [!TIP]
   > The subscription and plan can be changed later in the purchasing process.

5. Select the subscription to manage the Tabular Editor 3 subscription resource and costs. Assign the resource to an existing resource group or create a new group for this purpose.

6. Provide a name for the resource and configure your subscription by selecting the plan, contract duration, number of seats, and auto-renewal preference.
  
   ![Azure Marketplace purchase details](~/content/assets/images/azuremarketplace-setup-purchase.png)

   > [!IMPORTANT]
   > If you do not enable auto-renew, your subscription will be cancelled after the first billing term.

7. Click **Review + Subscribe**.

8. Review the terms and verify the purchase details, then click **Subscribe** at the bottom of the page.
   
   ![Azure Marketplace subscribe to offer](~/content/assets/images/azuremarketplace-subscribe.png)

9. Wait until the subscription creation is complete, then click **Configure account now** to complete your subscription. This will redirect you to the Tabular Editor self-service page.
   
   ![Azure Marketplace configure purchase](~/content/assets/images/azuremarketplace-configure-purchase.png)

> [!NOTE]
> Each edition of Tabular Editor 3 must be purchased separately. You cannot combine different editions in a single Azure Marketplace transaction.

For more details, see: [Purchase a SaaS offer in Azure Portal](https://learn.microsoft.com/en-us/marketplace/purchase-saas-offer-in-azure-portal#saas-subscription-and-configuration)

## Activating your Azure Marketplace subscription

Final completion of your purchase requires you to activate the subscription on the Tabular Editor self-service portal. Activating the subscription requires a Tabular Editor user account.

> [!IMPORTANT]
> You must use the **Configure account now** link from the Azure Portal to complete activation. This link contains essential subscription details required for activation. If you navigate away or close the page before signing in, return to the Azure Portal and click **Configure account now** again to ensure proper activation.

Follow the procedure below to finalize the activation of your purchase:

1. Once redirected from the Azure Portal, you are requested to sign in to the Tabular Editor Self-service portal using an existing account or by creating a new one.
   
   > [!IMPORTANT]
   > Use the same email address for your Tabular Editor account as the purchaser or beneficiary email from your Azure Portal purchase. Mismatched emails will prevent the Azure Marketplace subscription from linking to your account.
   
   > [!TIP]
   > You will need to give consent and accept the permission request when creating a new account for the self-service portal.

   Once signed in, you will see the newly purchased subscription at the top of the subscriptions page under the section "Pending Azure Marketplace subscriptions".

   ![Azure Marketplace pending subscription](~/content/assets/images/azuremarketplace-pending-subscription.png)

   > [!NOTE]
   > If you don't see your pending subscription listed, return to the Azure Portal and click the **Configure account now** button again to be redirected with the correct subscription information.
   
2. Click the **Activate** button for the subscription you wish to activate. This will display the subscription details.

   ![Azure Marketplace activate subscription](~/content/assets/images/azuremarketplace-activate-subscription.png)

3. Review the details one final time and click **Confirm Activation**.

4. The subscription will now be activated and the required licenses will be created. Once activation is complete:
   - Your subscription status in Azure will change from "Pending account configuration" to "Subscribed"
   - You will receive an email containing your license key(s)
   - The subscription will appear under **Subscriptions** in the Tabular Editor self-service portal. Click the ellipsis menu (three dots) and select **View subscription details** to view subscription information including the subscription period.
   
      ![Azure Marketplace subscription activated](~/content/assets/images/azuremarketplace-subscription-activated.png)

## Installing and activating licenses

Please read @installation-activation-basic for more details on how to install, activate, and configure your Tabular Editor 3 licenses.

## Changing Azure Marketplace subscriptions

All modifications to Tabular Editor 3 subscriptions purchased through the Azure Marketplace must be made in the Azure Portal. The Tabular Editor self-service portal does not currently support these operations.

You can manage the following subscription changes through the Azure Portal:

- **Change plan**: Upgrade or downgrade between different Tabular Editor 3 editions
- **Adjust number of seats**: Add or remove user licenses
- **Modify renewal preferences**: Enable or disable auto-renewal
- **Change Azure subscription**: Change Azure subscription or resource group managing the Tabular Editor subscription resource.
- **Cancel subscription**: Terminate your subscription at the end of the billing period

### How to modify your subscription

1. Sign in to the [Azure Portal](https://portal.azure.com/)
2. Navigate to **Home** > **SaaS** or search for "SaaS" in the search box
3. Locate and select your Tabular Editor 3 subscription from the list
4. On the subscription overview page, you can:
   - Click **Change plan** to switch between editions
   - Click **Change No. of users** to adjust the number of seats/licenses
   - Click **Edit Auto-renew** to adjust the auto-renewal settings
   - Click **Cancel subscription** to terminate the subscription
   - Click **Change Azure subscription** to change the Azure subscription used for billing
   - Click **Change resource group** to move the subscription resource to a different resource group

> [!IMPORTANT]
> Canceling a subscription immediately revokes access to all licenses under that subscription and cannot be undone. To maintain access until the end of your current billing period, click **Edit Auto-renew** and turn off automatic renewal instead.

For more information about managing SaaS subscriptions in Azure, see: [SaaS subscription lifecycle management](https://learn.microsoft.com/en-us/marketplace/saas-subscription-lifecycle-management)