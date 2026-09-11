---
uid: te-cli-automation
title: 自动化和脚本
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

# 自动化和脚本

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

Tabular Editor CLI 具备可组合性；每个命令都支持结构化输出，可按需禁用交互式提示，并返回可预测的退出代码。 这些基础能力同样适用于 shell 管道、Python 脚本、PowerShell 自动化以及由代理驱动的工作流。

## 结构化输出

使用 `--output-format` 可将任意命令在文本（供人阅读）和机器可读格式之间切换：

| 格式               | 用途                                                                                                                         | 说明                                                                           |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `text`（默认）       | 人工阅读                                                                                                                       | 无论是连接到 TTY 还是通过管道传输，stdout 都输出纯文本。                                           |
| `json`           | 机器可读                                                                                                                       | 始终向 stdout 输出有效的 JSON。 如果还需要在 stderr 上输出机器可读的错误信息，请使用 `--error-format json`。 |
| `csv`            | 表格结果（`query`、`bpa run`、`bpa rules`、`vertipaq`、`validate`、`test`、`refresh`、`profile list`、`session list`、`find`、`get`、`ls`） | 采用 RFC 4180 转义。                                                              |
| `tmsl`（别名 `bim`） | 整个对象的 TMSL/BIM 序列化                                                                                                         | 此格式被 `te get` 和 `te list` 支持。                                                |
| `tmdl`           | 整个对象的 TMDL 序列化                                                                                                             | 仅 `te get` 支持（单个对象）。                                                         |

```bash
te list --output-format json
te query -q "EVALUATE VALUES('Date'[Year])" --output-format csv
te bpa run --output-format json
```

在 `--output-format json` 下，`te validate`、`te bpa run`、`te test run` 和 `te query` 共用同一种 JSON 文档结构，包含 `summary`、扁平的 `findings[]` 数组和 `durationMs`——解析时请参见 @te-cli-findings 中的结构定义。

> [!NOTE]
> `--output-format` 和 `--error-format` 相互独立。 设置 `--output-format json` _不会_ 将 stderr 切换为 JSON；若要这样做，请传入 `--error-format json`。 重定向 stdout 时不会自动切换格式；除非你另行指定，否则默认始终为 `text`。

## 非交互模式

为任意命令添加 `--non-interactive`，以禁用确认提示、凭据选择列表和引导式向导。 如果命令需要的输入无法通过参数、环境变量或配置确定，它会以非零状态退出，并返回可操作的错误信息，而不是一直挂起。

`te deploy` 和 `te refresh` 默认也会以 dry-run 方式运行——它们会打印将要发送的 TMSL，且不会改动任何内容。 `--execute` 会执行实际操作；在管道或 CI 运行中，`--execute` 还要求使用 `--force`（因为无法响应确认提示）。

```bash
te deploy --model ./model --target-server my-workspace --target-database my-model \
  --non-interactive --execute --force --ci github
```

## 退出代码

每个 `te` 命令都会使用可预测的状态代码退出，因此调用方无需解析 stdout，就能根据成功或失败执行分支逻辑。

| 退出代码 | 含义                                                                                                                                                                 |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `0`  | 成功。                                                                                                                                                                |
| `1`  | 通用失败——参数无效、命令失败、验证错误、身份验证失败、BPA 质量门在严重性 >= error 时未通过、某次 `te script` 运行中脚本调用了 `Error(...)`，或某次 `te deploy` 已被服务器接受但包含对象错误。 针对 `te diff`：发现差异（遵循 `diff`/`cmp` 的惯例）。 |
| `2`  | 仅适用于 `te diff`：比较过程中出错，因此差异状态未知。                                                                                                                                   |

将退出代码与 `--ci <vsts\|github>` 注释以及 `--trx <file>` 结合使用，可在 CI 中展示更丰富的失败信息——请参阅 @te-cli-cicd。

## 在 stderr 上的错误

错误、警告、进度和状态提示（旋转指示器、`Using active connection:`）、参数错误后的用法提示以及预览横幅都会写入 **stderr**；stdout 只输出结果。 因此，被拒绝的命令会使 stdout 为空，所以捕获到的 dry-run 要么是有效输出，要么什么都没有；你也可以安全地通过管道传递 JSON，而不会被进度指示器或诊断信息污染：

```bash
te list --output-format json | jq '.[] | .name'
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
    return json.loads(result.stdout)["rows"]

rows = query("Finance", "Revenue Model", "EVALUATE TOPN(10, 'Sales')")
for row in rows:
    print(row)
```

要从 stderr 捕获结构化错误：

```python
import json
import subprocess

result = subprocess.run(
    ["te", "deploy", "--model", "./model",
     "--target-server", "Finance", "--target-database", "Revenue",
     "--output-format", "json", "--error-format", "json",
     "--non-interactive", "--execute", "--force"],
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
$result = te query -s Finance -d Revenue -q "EVALUATE TOPN(10, 'Sales')" --output-format json --non-interactive
  | ConvertFrom-Json

$result.rows | Format-Table

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

te deploy --model ./model `
  --target-server my-workspace --target-database my-model `
  --auth env --non-interactive --execute --force --ci vsts
```

## Bash

使用管道和 `jq` 组合命令。 CLI 的文本输出带有颜色，便于阅读；但切换到 `--output-format json` 后，你会得到一个干净、便于处理的结构：

```bash
# Count measures per table
te list --type measure --output-format json \
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
te refresh --type full > refresh.tmsl
cat refresh.tmsl
```

生成的 TMSL 可在 Pull Request 中审查、提交到版本库、由 CLI 执行（`te refresh --type full --execute`）、交给 DBA，或用任何兼容 XMLA 的工具应用。 CLI 不再是黑盒，而是可组合的组件。

## 常用模式

下面这些小技巧，是在脚本或管道中组合 `te` 命令时经常会用到的：

- **幂等的创建与删除。** `te add Sales/Marker -t Measure -p Expression="0" --if-not-exists --save` 用于创建度量值，`te remove Sales/OldMeasure --if-exists --save` 用于删除度量值；无论对象是否存在，两者都会以 `0` 退出——可在 CI 中安全地重复运行。
- **没有 `--save` 就不会持久化任何更改。** 会修改内容的命令（`te add`、`te set`、`te move`、`te remove`、`te script`、`te macro run`）会在内存中应用更改，输出 Report 说明它们执行了哪些操作，然后打印 `Dry run - nothing saved.`。 添加 --save 以持久化保存。`先不带`--save`运行一次，确认它解析到的是你期望的对象，然后再加上`--save`重新运行。`te remove --dry-run\` 还会更进一步：在不实际应用任何更改的情况下，输出 Report 说明将会删除哪些内容。
- **输出供审查的 TMSL。** `te deploy --model ./model --target-server my-workspace --target-database my-model > deploy.tmsl`——`deploy` 默认以 dry-run 方式运行，并将精确、已针对目标环境生成的 TMSL 打印到 stdout，因此将其重定向即可生成部署脚本，而不会触及服务器。 适合供 DBA 审查或手动应用。
- **通过 `-` 传入管道值。** 所有接受值的选项都可以通过 `-` 读取管道传入的 stdin（会移除末尾换行、剥离字节顺序标记；如果没有管道输入则立即报错）：`cat query.dax | te query -q -`（直接通过管道传入 stdin 而不加 `-q` 也可用）、`te set Sales/Amount -p Expression=- < expr.dax --save`、`cat fix.csx | te script --inline - --save`、`cat messy.dax | te util format-dax -`。 管道传入的值会按原样处理——如果管道传入文本 `null`，存储的就是单词 `null`；而 `-p Name=null` 或 `--unset Name` 则会清除该属性。
- **查找属性名。** `te get <path> --properties --output-format json` 会返回该对象上 `-p` 可接受的每个名称及其类型、是否可写和允许值——在生成 `te set` 调用前，应先查阅这份列表。
- **可解析的变更集。** 变更类命令（`set`、`add`、`remove`、`move`、`script`、`bpa run --fix`）默认会输出 diff；`--stat` 和 `--name-only` 提供更紧凑的文本替代形式，而 `te config set mutationOutput diff|stat|name-only|none` 可设置固定默认值。 无论是否使用这些标志，JSON 输出始终都会包含完整的 `changes` 数组（每个已更改对象一项，带有 `objectPath`、`objectType`、`changeKind` 以及属性变更前/后的配对值）——这是脚本中可稳定解析的结构。 `te diff` 也会以同样的结构输出 Report 来呈现差异。
- **仅输出路径。** `te list --paths-only` 和 `te find --paths-only` 每行输出一个对象路径，非常适合通过管道传给 `xargs`、`te get` 或 `te set`。 模型级容器（`te list Measures`、`te list Columns`）与此配合良好，可用于对整个模型进行全面扫描。
- **查询基准测试。** `te query --trace --cold --runs 5` 会在冷缓存下运行 DAX 查询，迭代五次，并捕获 FE/SE 跟踪事件。
- **CI 日志中的步骤耗时。** 长时间运行的命令（`te deploy`、`te refresh`、`te script`、`te validate`、`te query`）会在 JSON 输出中包含 `durationMs` 字段——便于在管道摘要中展示各步骤耗时。

## 相关页面

- @te-cli-cicd - 面向流水线的模式和 YAML 示例。
- @te-cli-commands - 完整命令参考。
- @te-cli-interactive - 在哪些情况下交互模式比编写脚本更合适。
