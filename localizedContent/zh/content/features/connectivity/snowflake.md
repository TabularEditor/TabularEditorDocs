---
uid: connect-snowflake
title: 连接到 Snowflake
author: Morten Lønskov
updated: 2026-09-21
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

依次选择 **模型 > 导入表...**，然后选择 Snowflake 数据源。每种身份验证方式都需要服务器（你的账户 URL）和 Warehouse。

![“连接到 Snowflake”对话框：在“身份验证方式”列表中选择了“外部浏览器”，且“用户名”和“密码”字段已禁用](~/content/assets/images/features/connectivity/snowflake-connection.png)

## 身份验证方式

| 身份验证方式        | 你需要提供的内容                             | 可在无人值守时重连 |
| ------------- | ------------------------------------ | --------- |
| **Snowflake** | 用户名和密码                               | 是的        |
| **外部浏览器**     | 通过浏览器向你的身份提供程序登录                     | 否         |
| **OAuth**     | 来自你的 OAuth 提供程序的令牌                   | 是，只要令牌有效  |
| **密钥对**       | 用户名和 RSA 私钥文件；如果该密钥设置了密码短语，还需要提供密码短语 | 是的        |

## 密钥对身份验证

由于 Snowflake 现在对服务账户强制启用多重身份验证，因此用于无人值守工作时，应选择“密钥对”作为身份验证方式。它无需交互式登录，因此保存后的连接可自行重连。

选择 **密钥对**，输入用户名，然后浏览到你的私钥文件。选择此身份验证器后，密码字段会改名为 **密码短语**。**确定** 按钮会一直处于禁用状态，直到服务器、Warehouse、用户名都已填写，且已选择私钥文件。

支持的密钥格式包括未加密的 PKCS#1 和 PKCS#8，以及使用密码短语加密的 PKCS#8；这也是 [Snowflake 官方密钥对说明](https://docs.snowflake.com/en/user-guide/key-pair-auth) 生成的格式。

> [!IMPORTANT]
> 不支持使用旧版 OpenSSL 方案加密的密钥。这类密钥以 `-----BEGIN RSA PRIVATE KEY-----` 开头，并带有 `Proc-Type` 和 `DEK-Info` 标头。使用一条 `openssl pkcs8 -topk8` 命令即可完成转换。这不需要生成新的密钥对，因此已为你的 Snowflake 用户注册的公钥仍然有效。

<!-- IMAGE NEEDED: connectivity/snowflake-key-pair.png
     The Snowflake connection dialog with Key pair selected, so the Private key file field
     and its browse button are visible and the password field reads Passphrase.
     House border, 100% DPI.
     Alt text: "The Snowflake connection dialog with Key pair authentication selected" -->

## 外部浏览器登录

浏览器登录会被缓存，因此你不必在每次操作时都重新登录。从 Tabular Editor 3.27.0 开始，如果缓存的登录已过期或被你的身份提供程序撤销，也不会再阻止连接：一旦 Snowflake 拒绝该登录，Tabular Editor 就会将其丢弃，并重新打开浏览器登录流程。

以前如果不重新打开浏览器，之后的每项操作都会失败；向导不会显示错误，而是显示空的表和列；唯一的恢复办法就是重启 Tabular Editor。现在，若你中途放弃登录，或登录超时，系统会将其视为取消，而不是会阻塞后续工作的错误。

## 切换身份验证器

切换回 **Snowflake** 时，会清除私钥路径和密码短语，而不会把密码短语继续当作账户密码。

## 凭据的存储位置

你在此处输入的凭据会按用户、按模型保存在模型旁边的 [用户选项](xref:user-options) 文件 (`.tmuo`) 中，并经过加密，只有你的 Windows 账户可以读取。它们不属于模型元数据，因此不会提交到源代码管理；打开同一模型的同事需要提供他们自己的凭据。

生成的 M 表达式只包含服务器和对象的名称。其中绝不会包含密码、令牌或密钥。
