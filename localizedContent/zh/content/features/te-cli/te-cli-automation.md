---
uid: te-cli-automation
title: 自动化和脚本
author: Peer Grønnerup
updated: 2026-05-06
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# 自动化和脚本

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

Tabular Editor CLI 具备可组合性；每个命令都支持结构化输出，可按需禁用交互式提示，并返回可预测的退出代码。 这些基础能力同样适用于 shell 管道、Python 脚本、PowerShell 自动化以及由代理驱动的工作流。

## 结构化输出

使用 `--output-format` 可将任意命令在文本（供人阅读）和机器可读格式之间切换：

| 格式               | 用途                                                                                                                                   | 说明                                                                           |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| `text`（默认）       | 人工阅读                                                                                                                                 | 无论是连接到 TTY 还是通过管道传输，stdout 都输出纯文本。                                           |
| `json`           | 机器可读                                                                                                                                 | 始终向 stdout 输出有效的 JSON。 如果还需要在 stderr 上输出机器可读的错误信息，请使用 `--error-format json`。 |
| `csv`            | 表格结果（`query`、`bpa run`、`bpa rules`、`vertipaq`、`validate`、`test`、`refresh`、`profile list`、`session list`、`find`、`replace`、`get`、`ls`） | 采用 RFC 4180 转义。                                                              |
| `tmsl`（别名 `bim`） | 整个对象的 TMSL/BIM 序列化                                                                                                                   | `te get` 和 `te ls` 接受此格式。                                                    |
| `tmdl`           | 整个对象的 TMDL 序列化                                                                                                                       | 仅 `te get` 支持（单个对象）。                                                         |

```bash
te ls --output-format json
te query -q "EVALUATE VALUES('Date'[Year])" --output-format csv
te bpa run --output-format json
```

> [!NOTE]
> `--output-format` 和 `--error-format` 相互独立。 设置 `--output-format json` _不会_ 将 stderr 切换为 JSON；若要这样做，请传入 `--error-format json`。 重定向 stdout 时不会自动切换格式；除非你另行指定，否则默认始终为 `text`。

## 非交互模式

为任意命令添加 `--non-interactive`，以禁用确认提示、凭据选择列表和引导式向导。 如果命令需要的输入无法通过参数、环境变量或配置确定，它会以非零状态退出，并返回可操作的错误信息，而不是一直挂起。

```bash
te deploy ./model --non-interactive --force --ci github
```

## 退出代码

每个 `te` 命令都会使用可预测的状态代码退出，因此调用方无需解析 stdout，就能根据成功或失败执行分支逻辑。

| 退出代码 | 含义                                                     |
| ---- | ------------------------------------------------------ |
| `0`  | 成功。                                                    |
| `1`  | 通用失败：参数无效、命令失败、验证错误、身份验证失败，或 BPA 门禁在严重级别 ≥ error 时未通过。 |
| `2`  | `te diff` 使用该代码表示模型存在差异（区别于 `0` 表示相同，以及其他非零错误代码）。      |

将退出代码与 `--ci <vsts\|github>` 注释以及 `--trx <file>` 结合使用，可在 CI 中展示更丰富的失败信息——请参阅 @te-cli-cicd。

## 在 stderr 上的错误

错误、警告和预览横幅会写入 **stderr**；结构化数据会写入 **stdout**。 这意味着你可以安全地通过管道传递 JSON，而不用担心其中混入进度指示或诊断信息：

```bash
te ls --output-format json | jq '.[] | .name'
te vertipaq --output-format json > stats.json
```

## Python

在数据管道、笔记本或测试框架中编排 CLI 调用时，Python 是很自然的选择。 使用 `subprocess.run` 调用 `te`，请求 JSON 输出，并解析 stdout：

```python
import json
import subprocess

def query(server: str, database: str, dax: str) -> list[dict]:
    result = subprocess.run(
        ["te", "query",
         "-s", server,
         "-d", database,
         "-q", dax,
         "--output-format", "json",
         "--non-interactive"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)

rows = query("Finance", "Revenue Model", "EVALUATE TOPN(10, 'Sales')")
for row in rows:
    print(row)
```

要从 stderr 捕获结构化错误：

```python
import json
import subprocess

result = subprocess.run(
    ["te", "deploy", "./model",
     "-s", "Finance", "-d", "Revenue",
     "--output-format", "json", "--non-interactive", "--force"],
    capture_output=True, text=True,
)

if result.returncode != 0:
    try:
        err = json.loads(result.stderr.strip().splitlines()[-1])
        print("Deploy failed:", err.get("error"), "- hint:", err.get("hint"))
    except json.JSONDecodeError:
        print("Deploy failed:\n", result.stderr)
```

## PowerShell

PowerShell 原生支持 JSON。 `te` 是一个普通的控制台可执行文件，可直接在 PowerShell 管道中使用（如果你正从较旧的 `TabularEditor.exe` CLI 迁移，请参阅 @te-cli-migrate）：

```powershell
$rows = te query -s Finance -d Revenue -q "EVALUATE TOPN(10, 'Sales')" --output-format json --non-interactive
  | ConvertFrom-Json

$rows | Format-Table

# Check exit code after the pipeline
if ($LASTEXITCODE -ne 0) {
    Write-Error "Query failed with exit $LASTEXITCODE"
    exit $LASTEXITCODE
}
```

从环境变量中读取密钥，而不是以明文传递：

```powershell
$env:AZURE_CLIENT_ID     = "your-app-id"
$env:AZURE_CLIENT_SECRET = "your-client-secret"
$env:AZURE_TENANT_ID     = "your-tenant-id"

te deploy ./model `
  -s my-workspace -d my-model `
  --auth env --non-interactive --force --ci vsts
```

## Bash

使用管道和 `jq` 组合命令。 CLI 的文本输出带有颜色，便于阅读；但切换到 `--output-format json` 后，你会得到一个干净、便于处理的结构：

```bash
# Count measures per table
te ls --type measure --output-format json \
  | jq -r '.[] | .table' \
  | sort | uniq -c | sort -rn
```

```bash
# Fail the shell script if BPA finds any errors
te bpa run --fail-on error --output-format json > bpa.json \
  || { echo "BPA gate failed"; jq '.violations' bpa.json; exit 1; }
```

## 可组合性示例

生成刷新 TMSL 脚本并将其纳入版本控制，只需三条命令：

```bash
te connect MyWorkspace MyModel
te refresh --type full --dry-run > refresh.tmsl
cat refresh.tmsl
```

生成的 TMSL 可在 Pull Request 中审查、提交到版本库、由 CLI 执行（`te refresh --type full`）、交给 DBA，或用任何兼容 XMLA 的工具应用。 CLI 不再是黑盒，而是可组合的组件。

## 常用模式

下面这些小技巧，是在脚本或管道中组合 `te` 命令时经常会用到的：

- **幂等的创建与删除。** `te add Sales/Marker -t Measure -i "0" --if-not-exists --save` 用于创建度量值，`te rm Sales/OldMeasure --if-exists --save` 用于删除度量值；无论对象是否存在，两者都会以 `0` 退出——可在 CI 中安全地重复运行。
- **试运行查看差异。** `te replace` 默认会先试运行；只有在你对预览结果满意时才添加 `--save`。
- **输出供审查的 TMSL。** `te deploy ./model --xmla deploy.tmsl` 会生成部署脚本，而不会更改服务器——适合 DBA 审查或手动应用。
- **仅输出路径。** `te ls --paths-only` 和 `te find --paths-only` 每行输出一个对象路径，非常适合通过管道传给 `xargs`、`te get` 或 `te set`。 模型级容器（`te ls Measures`、`te ls Columns`）与此配合良好，适合对整个模型进行一次全面扫描。
- **查询基准测试。** `te query --trace --cold --runs 5` 会在冷缓存下运行 DAX 查询，迭代五次，并捕获 FE/SE 跟踪事件。
- **CI 日志中的步骤耗时。** 长时间运行的命令（`te deploy`、`te refresh`、`te script`、`te validate`）会在 JSON 输出中包含 `durationMs` 字段——便于在管道摘要中展示各步骤耗时。

## 相关页面

- @te-cli-cicd - 面向流水线的模式和 YAML 示例。
- @te-cli-commands - 完整命令参考。
- @te-cli-interactive - 在哪些情况下交互模式比编写脚本更合适。
