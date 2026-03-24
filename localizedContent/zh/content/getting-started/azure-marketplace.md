---
uid: azure-marketplace
title: 通过 Azure Marketplace 购买
author: Peer Grønnerup
updated: 2026-01-05
---

# 通过 Azure Marketplace 购买 Tabular Editor 3

Tabular Editor 3 已作为公开产品在 Azure Marketplace 上架。 本文档概述了如何直接通过 Azure Marketplace 获取 Tabular Editor 3，从而简化您的采购流程。

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

   > [!TIP]
   > 在采购流程的后续步骤中，也可以更改订阅和计划。

5. 选择用于管理 Tabular Editor 3 订阅资源及其成本的订阅。 将该资源分配到现有资源组，或为此创建新的资源组。

6. 为资源命名，然后通过选择计划、合同期限、席位数量以及自动续订偏好来配置您的订阅。

   ![Azure Marketplace 购买详情](~/content/assets/images/azuremarketplace-setup-purchase.png)

   > [!IMPORTANT]
   > 如果不启用自动续订，你的订阅将在首个计费周期结束后自动取消。

7. 点击 **查看 + 订阅**。

8. 查看条款并核对购买详情，然后在页面底部点击 **订阅**。

   ![Azure Marketplace subscribe to offer](~/content/assets/images/azuremarketplace-subscribe.png)

9. 等待订阅创建完成，然后点击 **立即配置账户** 以完成订阅。 这将把你重定向到 Tabular Editor 自助服务页面。

   ![Azure Marketplace configure purchase](~/content/assets/images/azuremarketplace-configure-purchase.png)

> [!NOTE]
> Tabular Editor 3 的每个版本都必须单独购买。 你无法在单笔 Azure Marketplace 交易中组合购买不同版本。

更多详情，请参阅：[在 Azure 门户中购买 SaaS 产品](https://learn.microsoft.com/en-us/marketplace/purchase-saas-offer-in-azure-portal#saas-subscription-and-configuration)

## 激活 Azure Marketplace 订阅

要最终完成购买，你需要在 Tabular Editor 自助服务门户中激活订阅。 激活订阅需要一个 Tabular Editor 用户账户。

> [!IMPORTANT]
> 你必须使用 Azure 门户中的 **立即配置账户** 链接来完成激活。 该链接包含激活所需的关键订阅详细信息。 如果你在登录前离开或关闭页面，请返回 Azure 门户并再次点击 **立即配置账户**，以确保正确激活。

按以下步骤完成购买的激活：

1. 从 Azure 门户跳转后，系统会要求你使用现有账户登录 Tabular Editor 自助服务门户，或创建一个新账户。

   > [!IMPORTANT]
   > Tabular Editor 账户请使用与你在 Azure 门户购买时填写的购买者或受益人邮箱相同的电子邮件地址。 邮箱不一致会导致 Azure Marketplace 订阅无法关联到你的账户。

   > [!TIP]
   > 在自助服务门户创建新账户时，你需要进行授权并接受权限请求。

   登录后，你会在“订阅”页面顶部的“待处理的 Azure Marketplace 订阅”部分看到新购买的订阅。

   ![Azure Marketplace pending subscription](~/content/assets/images/azuremarketplace-pending-subscription.png)

   > [!NOTE]
   > 如果未在列表中看到待处理订阅，请返回 Azure 门户并再次点击 **立即配置账户** 按钮，以便使用正确的订阅信息重新跳转。

2. 点击你要激活的订阅上的 **激活** 按钮。 这将显示订阅的详细信息。

   ![Azure Marketplace activate subscription](~/content/assets/images/azuremarketplace-activate-subscription.png)

3. 最后再核对一遍详细信息，然后点击 **确认激活**。

4. 订阅将被激活，并创建所需的许可证。 激活完成后：
   - Azure 中的订阅状态将从“Pending account configuration”变为“Subscribed”
   - 你将收到一封包含许可证密钥（可能有多个）的电子邮件
   - 该订阅将显示在 Tabular Editor 自助服务门户的 **Subscriptions** 下。 点击省略号菜单（三个点），然后选择 **查看订阅详细信息**，就能查看包括订阅期限在内的订阅信息。

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
> **不支持降级**：在当前订阅周期内，你无法降级到更低版本，也无法减少用户数。 要切换到更低级别的计划或减少席位，请先关闭当前订阅的 **自动续订**，然后在当前期限结束前按所需配置购买新的订阅。

> [!IMPORTANT]
> 取消订阅会立即撤销该订阅下所有许可证的使用权限，且此操作无法撤销。 若要将访问权限保留到当前计费周期结束，请点击 **编辑自动续订**，然后关闭自动续订。 退款将按退款政策处理。 想了解更多信息，可以查看 Microsoft Marketplace 的 [退款政策](https://learn.microsoft.com/en-us/marketplace/refund-policies?WT.mc_id=Portal-Microsoft_Azure_Marketplace#software-as-a-service-saas-offers)。

想了解在 Azure 中管理 SaaS 订阅的更多信息，可以查看：[SaaS 订阅生命周期管理](https://learn.microsoft.com/en-us/marketplace/saas-subscription-lifecycle-management)