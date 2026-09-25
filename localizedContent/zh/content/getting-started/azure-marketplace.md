---
uid: azure-marketplace
title: 通过 Azure Marketplace 购买
author: Peer Grønnerup
updated: 2026-01-05
---

# 通过 Azure Marketplace 购买 Tabular Editor 3

Tabular Editor 3 已作为公开产品在 Azure Marketplace 上架。 This document provides an overview of how to streamline your purchase by acquiring Tabular Editor 3 directly through the Azure Marketplace.

访问 [Azure Marketplace 上的 Tabular Editor 3 产品页](https://marketplace.microsoft.com/en-us/marketplace/apps?search=tabular%20editor%203) 即可开始。

## 要求

要通过 Azure Marketplace 购买 Tabular Editor，您需要：

- 一个 Azure 订阅（请确认您是否已有订阅，或创建新的订阅）
- 一个 Azure AD 账户，并且在该 Azure 订阅中至少拥有“参与者”角色

此外，在通过 Azure Marketplace 购买 Tabular Editor 3 之前，请确保已满足以下[先决条件](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/enable-marketplace-purchases)。

## 如何在 Azure Marketplace 上购买 Tabular Editor 3

按以下流程通过 Azure Marketplace 购买 Tabular Editor 3 许可证：

1. 登录 [Azure 门户](https://portal.azure.com/)

2. 直接进入 Marketplace 页面，或使用页面顶部的搜索框搜索“Marketplace”。

3. 在 Azure Marketplace 页面中搜索“Tabular Editor 3”，然后点击 Tabular Editor 3 产品条目。

4. 选择您的订阅和许可证计划，然后点击 **订阅**。

   ![Azure Marketplace 订阅产品](~/content/assets/images/azuremarketplace-offer-page.png)

   > [!TIP]> 在采购流程的后续步骤中，也可以更改订阅和计划。

5. 选择用于管理 Tabular Editor 3 订阅资源及其成本的订阅。 Assign the resource to an existing resource group or create a new group for this purpose.

6. 为资源命名，然后通过选择计划、合同期限、席位数量以及自动续订偏好来配置您的订阅。

   ![Azure Marketplace 购买详情](~/content/assets/images/azuremarketplace-setup-purchase.png)

   > [!IMPORTANT]> 如果不启用自动续订，你的订阅将在首个计费周期结束后自动取消。

7. 点击 **查看 + 订阅**。

8. 查看条款并核对购买详情，然后在页面底部点击 **订阅**。

   ![Azure Marketplace subscribe to offer](~/content/assets/images/azuremarketplace-subscribe.png)

9. Wait until the subscription creation is complete, then click **Configure account now** to complete your subscription. This will redirect you to the Tabular Editor self-service page.

   ![Azure Marketplace configure purchase](~/content/assets/images/azuremarketplace-configure-purchase.png)

> [!NOTE]
> Tabular Editor 3 的每个版本都必须单独购买。 You cannot combine different editions in a single Azure Marketplace transaction.

更多详情，请参阅：[在 Azure 门户中购买 SaaS 产品](https://learn.microsoft.com/en-us/marketplace/purchase-saas-offer-in-azure-portal#saas-subscription-and-configuration)

## 激活 Azure Marketplace 订阅

要最终完成购买，你需要在 Tabular Editor 自助服务门户中激活订阅。 Activating the subscription requires a Tabular Editor user account.

> [!IMPORTANT]
> 你必须使用 Azure 门户中的 **立即配置账户** 链接来完成激活。 This link contains essential subscription details required for activation. If you navigate away or close the page before signing in, return to the Azure Portal and click **Configure account now** again to ensure proper activation.

按以下步骤完成购买的激活：

1. 从 Azure 门户跳转后，系统会要求你使用现有账户登录 Tabular Editor 自助服务门户，或创建一个新账户。

   > [!IMPORTANT]> Tabular Editor 账户请使用与你在 Azure 门户购买时填写的购买者或受益人邮箱相同的电子邮件地址。 Mismatched emails will prevent the Azure Marketplace subscription from linking to your account.

   > [!TIP]> 在自助服务门户创建新账户时，你需要进行授权并接受权限请求。

   登录后，你会在“订阅”页面顶部的“待处理的 Azure Marketplace 订阅”部分看到新购买的订阅。

   ![Azure Marketplace pending subscription](~/content/assets/images/azuremarketplace-pending-subscription.png)

   > [!NOTE]> 如果未在列表中看到待处理订阅，请返回 Azure 门户并再次点击 **立即配置账户** 按钮，以便使用正确的订阅信息重新跳转。

2. 点击你要激活的订阅上的 **激活** 按钮。 This will display the subscription details.

   ![Azure Marketplace activate subscription](~/content/assets/images/azuremarketplace-activate-subscription.png)

3. Review the details one final time and click **Confirm Activation**.

4. 订阅将被激活，并创建所需的许可证。 Once activation is complete:
   - Azure 中的订阅状态将从“Pending account configuration”变为“Subscribed”
   - 你将收到一封包含许可证密钥（可能有多个）的电子邮件
   - 该订阅将显示在 Tabular Editor 自助服务门户的 **Subscriptions** 下。 Click the ellipsis menu (three dots) and select **View subscription details** to view subscription information including the subscription period.

     ![Azure Marketplace subscription activated](~/content/assets/images/azuremarketplace-subscription-activated.png)

## 安装并激活许可证

有关如何安装、激活和配置 Tabular Editor 3 许可证的更多信息，请参阅 @installation-activation-basic。

## 更改 Azure Marketplace 订阅

通过 Azure Marketplace 购买的 Tabular Editor 3 订阅，所有修改都必须在 Azure 门户中完成。

### 如何修改订阅

1. 登录到 [Azure 门户](https://portal.azure.com/)
2. 转到 **主页** > **SaaS**，或在搜索框中搜索“SaaS”
3. 在列表中找到并选择你的 Tabular Editor 3 订阅
4. 在订阅概览页面上，你可以执行以下操作：
   - **更改计划**：升级到更高级别的 Tabular Editor 3 版本
   - **更改用户数**：添加更多用户许可证
   - **编辑自动续订**：启用或禁用自动续订
   - **取消订阅**：终止订阅
   - **更改 Azure 订阅**：修改用于计费的 Azure 订阅
   - **更改资源组**：将订阅资源移动到其他资源组

> [!NOTE]
> **不支持降级**：在当前订阅周期内，你无法降级到更低版本，也无法减少用户数。 To move to a lower-tier plan or reduce seats, turn off **Auto-renew** for your current subscription and purchase a new subscription with your desired configuration before the current term ends.

> [!IMPORTANT]
> Canceling a subscription immediately revokes access to all licenses under that subscription and cannot be undone. To maintain access until the end of your current billing period, click **Edit Auto-renew** and turn off automatic renewal instead. Refunds are processed according to the refund policy. For more information, see [Refund policies](https://learn.microsoft.com/en-us/marketplace/refund-policies?WT.mc_id=Portal-Microsoft_Azure_Marketplace#software-as-a-service-saas-offers) for Microsoft Marketplace.

想了解在 Azure 中管理 SaaS 订阅的更多信息，可以查看：[SaaS 订阅生命周期管理](https://learn.microsoft.com/en-us/marketplace/saas-subscription-lifecycle-management)