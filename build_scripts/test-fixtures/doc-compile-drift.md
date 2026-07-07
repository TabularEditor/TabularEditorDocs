# Compile drift

Good compile block:

```csharp {compile}
var view = SemanticBridge.MetricView.Model;
```

Run block that calls a nonexistent API (compile FAIL):

```csharp {run id=bad setup=none after=none output=false}
SemanticBridge.MetricView.NoSuchMethod();
```
