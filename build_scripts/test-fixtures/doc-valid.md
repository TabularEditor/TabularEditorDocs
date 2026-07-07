# Valid doc

Untagged csharp block is skipped:

```csharp
Output("ignored by the harness");
```

Compile-only block:

```csharp {compile}
var view = SemanticBridge.MetricView.Model;
```

Run block with expected output:

```csharp {run id=first setup=mv-sample after=none output=true}
Output("hello from a run block");
```
**Output:**
```
hello from a run block
```

Chained run block, no output assertion:

```csharp {run id=second setup=none after=first output=false}
Output("chained after first");
```

A non-csharp block is ignored:

```yaml
version: 1.1
```
