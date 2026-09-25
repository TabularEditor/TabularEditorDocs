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

Tabular Editor CLI 具备可组合性；每个命令都支持结构化输出，可按需禁用交互式提示，并返回可预测的退出代码。 The same primitives work equally well for shell pipelines, Python scripts, PowerShell automation, and agent-driven workflows.

## 结构化输出

使用 `--output-format` 可将任意命令在文本（供人阅读）和机器可读格式之间切换：

| 格式               | 用途                                                                                                                                                                   | 说明                                                                                                                   |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `text`（默认）       | Human-readable use                                                                                                                                                   | 无论是连接到 TTY 还是通过管道传输，stdout 都输出纯文本。                                                                                   |
| `json`           | 机器可读                                                                                                                                                                 | 始终向 stdout 输出有效的 JSON。 Use `--error-format json` if you also want machine-readable errors on stderr. |
| `csv`            | Tabular results (`query`, `bpa run`, `bpa rules`, `vertipaq`, `validate`, `test`, `refresh`, `profile list`, `session list`, `find`, `get`, `ls`) | 采用 RFC 4180 转义。                                                                                                      |
| `tmsl`（别名 `bim`） | 整个对象的 TMSL/BIM 序列化                                                                                                                                                   | Accepted by `te get` and `te list`.                                                                  |
| `tmdl`           | 整个对象的 TMDL 序列化                                                                                                                                                       | 仅 `te get` 支持（单个对象）。                                                                                                 |

```bash
te list --output-format json
te query -q "EVALUATE VALUES('Date'[Year])" --output-format csv
te bpa run --output-format json
```

Under `--output-format json`, `te validate`, `te bpa run`, `te test run`, and `te query` share one JSON document shape with a `summary`, a flat `findings[]` array, and `durationMs` - see @te-cli-findings for the shape to parse.

> [!NOTE]
> `--output-format` and `--error-format` are independent. 设置 `--output-format json` _不会_ 将 stderr 切换为 JSON；若要这样做，请传入 `--error-format json`。 There is no automatic format switching when stdout is redirected - the default is always `text` unless you ask otherwise.

## 非交互模式

Add `--non-interactive` to any command to disable confirmation prompts, credential picklists, and guided wizards. If the command needs input it cannot resolve from flags, environment, or config, it exits non-zero with an actionable error instead of hanging.

`te deploy` and `te refresh` are additionally dry-run by default - they print the TMSL they would send and touch nothing. `--execute` performs the action, and in piped or CI runs `--execute` requires `--force` (the confirmation prompt cannot be answered).

```bash
te deploy --model ./model --target-server my-workspace --target-database my-model \
  --non-interactive --execute --force --ci github
```

## 退出代码

每个 `te` 命令都会使用可预测的状态代码退出，因此调用方无需解析 stdout，就能根据成功或失败执行分支逻辑。

| 退出  | 含义                                                                                                                                                                                                                                                                                                                                                                                 |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0` | 成功。                                                                                                                                                                                                                                                                                                                                                                                |
| `1` | Generic failure - invalid arguments, command failed, validation errors, auth failure, BPA gate failed at severity >= error, a `te script` run in which a script called `Error(...)`, a `te deploy` the server accepted with object errors. For `te diff`: differences found (like the `diff`/`cmp` convention). |
| `2` | `te diff` only: an error occurred while comparing, so the difference status is unknown.                                                                                                                                                                                                                                                            |

将退出代码与 `--ci <vsts\|github>` 注释以及 `--trx <file>` 结合使用，可在 CI 中展示更丰富的失败信息——请参阅 @te-cli-cicd。

## 在 stderr 上的错误

Errors, warnings, progress and status notices (the spinner, `Using active connection:`), the usage reminder that follows an argument error, and the preview banner are written to **stderr**; stdout carries only the result. A rejected command therefore leaves stdout empty, so a captured dry run is either valid output or nothing at all, and you can pipe JSON safely without it being contaminated by progress indicators or diagnostic messages:

```bash
te list --output-format json | jq '.[] | .name'
te vertipaq --output-format json > stats.json
```

## Python

Python is a natural host for orchestrating CLI calls from data pipelines, notebooks, or test harnesses. 使用 `subprocess.run` 调用 `te`，请求 JSON 输出，并解析 stdout：

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

PowerShell handles JSON natively. `te` 是一个普通的控制台可执行文件，可直接在 PowerShell 管道中使用（如果你正从较旧的 `TabularEditor.exe` CLI 迁移，请参阅 @te-cli-migrate）：

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

Read secrets from the environment rather than passing them as plaintext:

```powershell
$env:AZURE_CLIENT_ID     = "your-app-id"
$env:AZURE_CLIENT_SECRET = "your-client-secret"
$env:AZURE_TENANT_ID     = "your-tenant-id"

te deploy --model ./model `
  --target-server my-workspace --target-database my-model `
  --auth env --non-interactive --execute --force --ci vsts
```

## Bash

Compose commands with pipes and `jq`. CLI 的文本输出带有颜色，便于阅读；但切换到 `--output-format json` 后，你会得到一个干净、便于处理的结构：

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

The resulting TMSL can be reviewed in a pull request, committed, executed by the CLI (`te refresh --type full --execute`), handed to a DBA, or applied by any XMLA-compatible tool. The CLI becomes a building block rather than a black box.

## 常用模式

下面这些小技巧，是在脚本或管道中组合 `te` 命令时经常会用到的：

- **Idempotent creates and removes.** `te add Sales/Marker -t Measure -p Expression="0" --if-not-exists --save` and `te remove Sales/OldMeasure --if-exists --save` both exit `0` whether or not the object existed - safe to re-run in CI.
- **Nothing persists without `--save`.** Mutating commands (`te add`, `te set`, `te move`, `te remove`, `te script`, `te macro run`) apply the change in memory, report what they did, and then print `Dry run - nothing saved. Add --save to persist.` Run one bare to confirm it resolves the objects you expect, then re-run with `--save`. `te remove --dry-run` goes further and reports what would be removed without applying anything.
- **Emit TMSL for review.** `te deploy --model ./model --target-server my-workspace --target-database my-model > deploy.tmsl` - deploy is dry-run by default and prints the exact target-aware TMSL to stdout, so redirecting it produces the deployment script without touching the server. Useful for DBA review or manual apply.
- **Piped values via `-`.** Every value-taking option reads piped stdin through `-` (trailing newline removed, byte-order mark stripped; errors immediately when nothing is piped): `cat query.dax | te query -q -` (bare piped stdin with no `-q` also works), `te set Sales/Amount -p Expression=- < expr.dax --save`, `cat fix.csx | te script --inline - --save`, `cat messy.dax | te util format-dax -`. A piped value is taken verbatim - piping the text `null` stores the word `null`, where `-p Name=null` or `--unset Name` clears the property.
- **Discover property names.** `te get <path> --properties --output-format json` returns every name `-p` accepts on that object with its type, writability, and allowed values - the list to consult before generating `te set` calls.
- **Parseable change sets.** Mutating commands (`set`, `add`, `remove`, `move`, `script`, `bpa run --fix`) render a diff by default; `--stat` and `--name-only` give compact text alternatives, and `te config set mutationOutput diff|stat|name-only|none` sets a standing default. JSON output always carries the full `changes` array (one entry per changed object with `objectPath`, `objectType`, `changeKind`, and before/after property pairs) regardless of these flags - the stable shape to parse in scripts. `te diff` reports its differences in the same shape.
- **Path-only output.** `te list --paths-only` and `te find --paths-only` emit one object path per line, ideal for piping to `xargs`, `te get`, or `te set`. The model-level containers (`te list Measures`, `te list Columns`) compose well with this for whole-model sweeps.
- **查询基准测试。** `te query --trace --cold --runs 5` 会在冷缓存下运行 DAX 查询，迭代五次，并捕获 FE/SE 跟踪事件。
- **Step timings in CI logs.** Long-running commands (`te deploy`, `te refresh`, `te script`, `te validate`, `te query`) include a `durationMs` field in JSON output - useful for surfacing per-step timings in pipeline summaries.

## 相关页面

- @te-cli-cicd - 面向流水线的模式和 YAML 示例。
- @te-cli-commands - 完整的命令参考。
- @te-cli-interactive - 在哪些情况下交互模式比编写脚本更合适。
