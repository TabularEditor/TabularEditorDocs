---
uid: te-cli-findings
title: 机器可读结果（JSON）
author: Peer Grønnerup
updated: 2026-09-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# 机器可读结果（JSON）

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

`te validate`、`te bpa run`、`te test run` 和 `te query` 会使用统一的 JSON 结构来 Report 问题。 使用 `--output-format json` 时，这些命令都会输出 **单个文档**，不会出现没有任何内容可供解析的情况。

> [!NOTE]
> `te query` 仅在执行前的 DAX 验证产生至少一个错误时，才会使用此 JSON 结构。 查询成功时，会改为输出查询结果：`{columns, rows, rowCount, truncated, durationMs, trace?}`。

## JSON 文档

```json
{
  "command": "validate",
  "durationMs": 412,
  "summary": { "errors": 1, "warnings": 2, "info": 0, "total": 3 },
  "findings": [
    {
      "severity": "error",
      "source": "validate",
      "code": "TE0001",
      "message": "Unknown column 'Sales'[Amt]",
      "object": "Revenue",
      "objectType": "Measure",
      "objectPath": "Sales/Revenue",
      "expressionPosition": { "property": "Expression", "lineNumber": 3, "column": 9 },
      "fixable": false
    }
  ],
  "valid": false
}
```

- `command`：生成该文档的命令。
- `durationMs`：总运行时长。
- `summary`：严重性统计：`errors`、`warnings`、`info`、`total`。
- `findings`：一个扁平数组，通过 `severity` 区分。

## 每个发现项的键名

每个发现项都包含：

| 键            | 值/含义                                                                            |
| ------------ | ------------------------------------------------------------------------------- |
| `severity`   | `error`、`warning` 或 `info`。                                                     |
| `source`     | `validate`、`bpa`、`test` 或 `query`。                                              |
| `code`       | 稳定的发现代码（验证信息 ID、BPA 规则 ID、`TEST_FAIL` / `TEST_ERROR` / `TEST_SUITE_INVALID` 等）。 |
| `信息`         | 便于理解的描述。                                                                        |
| `object`     | 该发现所涉及对象的基本名称。                                                                  |
| `objectType` | 预定义值之一——见下文。                                                                    |
| `fixable`    | 仅当 BPA 违规项的规则定义了修复表达式时，值才为 `true`。                                              |

**仅在 CLI 已知这些值时**才会出现——未设置时，这些键&#x4F1A;_&#x7F3A;失_，而不是 `null`：

| 键                      | 填充自                          | 含义                                                                                                                                                                       |
| ---------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `objectPath`           | 仅适用于 `validate` 和 `bpa` 的违规项 | 规范对象路径，可由 `te get` 或 `te set` 直接按原样解析。 测试发现项、查询发现项以及 BPA 规则错误中没有此字段。                                                                                                     |
| `expressionPosition`   | 仅限 `validate` 和 `query`      | Named Expression 属性中的 `{property, lineNumber, column}`。 **在所有来源中，包括 validate 和 query，都是可选的** - 只要分析器未报告任何可用位置，此字段就不存在；并且要么完整提供，要么完全不提供(绝不会只提供部分位置信息)。 |
| `ruleName`, `category` | 仅限 `bpa`                     | 所违反规则的名称和类别。                                                                                                                                                             |

### objectType 取值表

`objectType` 的取值是一个封闭集合（使用路径语法中各容器的单数形式，而不是 TOM 枚举）：

`Measure`, `Column`, `Hierarchy`, `Level`, `Partition`, `CalculationItem`, `Table`, `Role`, `TablePermission`, `Perspective`, `Culture`, `DataSource`, `Expression`, `Function`, `Relationship`, `KPI`, `RefreshPolicy`, `Member`, `Calendar`, `Variation`, `Model`, `BpaRule`, `Test`, `TestSuite`, `Query`。

## 各命令专有字段

每个命令都会在文档顶层带有少量自身专有的键：

| 命令                 | 额外键                                                                                                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `te validate`      | `valid`（布尔值）。                                                                                                                                                             |
| `te bpa run`       | `model`、`rulesEvaluated`、`violations`、`ruleErrors`、`ignoredRules`。 规则评估错误会以严重性 `error`、`objectType: "BpaRule"` 的形式出现在 `findings` 中；`violations` 和 `ruleErrors` 分别统计这两类数量。 |
| `te bpa run --fix` | 在同一个文档内新增一个 `fix` 键：`changes`、`fixed`、`fixErrors`、`skipped`、`fixedItems`、`fixErrorItems`。 如果修复步骤本身失败，仍会生成文档，并将原因写入 `fix.error`。 不带 `--fix` 时不会出现。                         |
| `te test run`      | `suites`、`invalidSuites`、`testSummary`（按状态汇总测试数量；`summary` 仍为共享的严重性汇总）。                                                                                                   |
| `te query`         | 没有——而且只会在验证错误时出现；见上文说明。                                                                                                                                                   |

## CI 注释

这四个命令共用同一个注释写入器，用于 `--ci vsts` / `--ci github`（接受 `azdo`、`azure-devops` 和 `gh` 作为别名；`none` 会禁用注释；其他任何值都会在命令运行前被拒绝）。 注释会输出到 stderr；stdout 保持可解析：

- 注释会带上发现项的代码：在 Azure DevOps 中使用 `code=`，在 GitHub 中使用 `title=`。
- 信息级 Info 发现项不是警告：在 GitHub 上会输出 `::notice::`，在 Azure DevOps 上则是一条普通日志行。 如果某次 Azure DevOps 运行的发现项只有信息类 Report，则该运行会显示为 **Succeeded**。
- 多行信息会被转义为单行注释，因此规则说明不会破坏日志格式。

## 相关页面

- @te-cli-commands#exit-codes - 退出代码不受输出格式影响。
- @te-cli-cicd - 使用这种输出结构的管道模式。
- @te-cli-automation - 在脚本中解析结构化输出。
