---
uid: connect-snowflake
title: 连接到 Snowflake
author: Morten Lønskov
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 连接到 Snowflake

Snowflake 连接器可连接到 Snowflake Warehouse，并且仅可作为隐式数据源使用（参见 [旧版、结构化和隐式数据源](xref:connectivity#legacy-structured-and-implicit-data-sources)）。

选择 **模型 > 导入表...**，然后选择 Snowflake 数据源以打开对话框。

![“连接到 Snowflake”对话框：在“身份验证方式”列表中选择了“外部浏览器”，且“用户名”和“密码”字段已禁用](~/content/assets/images/features/connectivity/snowflake-connection.png)

## 连接字段

| 字段                      | 说明                                |
| ----------------------- | --------------------------------- |
| **服务器**                 | 你的 Snowflake 账户 URL。必需            |
| **Warehouse**           | 用于运行查询的 Warehouse。必需              |
| **数据库（可选）**             | 要导入的数据库                           |
| **身份验证方式**              | 身份验证选项。参见 [身份验证](#authentication) |
| **用户名**、**密码**和**私钥文件** | 所选身份验证方式的凭据。标签会随身份验证器而变化          |
| **附加连接字符串属性（可选）**       | 附加连接字符串设置                         |

## 身份验证

| 身份验证          | 你需要提供的内容                                              | 交互式登录 |
| ------------- | ----------------------------------------------------- | ----- |
| **Snowflake** | 用户名和密码                                                | 否     |
| **外部浏览器**     | 通过浏览器向你的身份提供程序登录                                      | 是的    |
| **OAuth**     | 在 **令牌** 字段中输入 OAuth 提供程序提供的 OAuth 访问令牌。令牌过期后，请输入新的令牌 | 否     |
| **密钥对**       | 用户名和 RSA 私钥文件；如果该密钥已加密，还需提供其密码短语                      | 否     |

Tabular Editor 会将连接设置和凭据保存在你的用户选项文件中（参见 [凭据的存储位置](xref:connectivity#where-credentials-are-stored)）。

## 密钥对身份验证

Snowflake 服务用户（`TYPE = SERVICE`）不能使用密码登录，因此应为此类用户选择 **密钥对**。参见 [单因素密码登录弃用规划](https://docs.snowflake.com/en/user-guide/security-mfa-rollout)。

1. 在 **身份验证器** 列表中选择 **密钥对**。**密码** 字段会变为 **密码短语**。
2. 输入用户名。
3. 浏览并选择私钥文件。
4. 如果密钥已加密，请输入对应的密码短语。

填写完 **服务器**、**Warehouse**、**用户名** 和 **私钥文件** 后，**确定** 按钮才会启用。私钥文件必须采用以下格式之一：

- 未加密的 PKCS#1
- 未加密的 PKCS#8
- 使用密码短语加密的 PKCS#8；这也是 [Snowflake 官方密钥对说明](https://docs.snowflake.com/en/user-guide/key-pair-auth) 生成的格式

当你在 **密钥对** 和其他 **身份验证器** 之间切换时，**密码** 或 **密码短语** 字段会被清空。只有在选择 **密钥对** 时，Tabular Editor 才会保存私钥文件路径。

> [!IMPORTANT]
> 不支持采用旧版 OpenSSL 方案加密的密钥：这类密钥以 `-----BEGIN RSA PRIVATE KEY-----` 开头，并包含 `Proc-Type` 和 `DEK-Info` 标头。可将这类密钥转换为加密的 PKCS#8：
>
> ```bash
> openssl pkcs8 -topk8 -v2 aes256 -in rsa_key.pem -out rsa_key.p8
> ```
>
> 转换不会改变密钥对，已为你的 Snowflake 用户注册的公钥仍然有效。

<!-- IMAGE NEEDED: connectivity/snowflake-key-pair.png
     The Snowflake connection dialog with Key pair selected, so the Private key file field
     and its browse button are visible and the password field reads Passphrase.
     House border, 100% DPI.
     Alt text: "The Snowflake connection dialog with Key pair authentication selected" -->

## 外部浏览器登录

Tabular Editor 会缓存浏览器登录状态。从 Tabular Editor 3.27.0 起，如果 Snowflake 拒绝使用已缓存的登录状态(例如你的身份提供商已使其过期或已将其撤销)，Tabular Editor 会丢弃该缓存，并重新打开浏览器登录窗口。如果你关闭浏览器登录窗口，或登录超时，操作将被取消。
