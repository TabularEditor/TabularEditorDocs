---
uid: semantic-bridge-metric-view-fields-and-dimensions
title: Fields and Dimensions in Metric Views
author: Greg Baldini
updated: 2026-06-25
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.26.2
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---
# Fields and Dimensions in Metric Views

<!--
SUMMARY: Explains the Databricks Metric View `dimensions` -> `fields` keyword rename and the
matching Semantic Bridge C# API rename (Dimension -> Field): what changed, that the old names
still work, migration guidance, and what Tabular Editor emits on round-trip.
-->

In spring 2026, the Metric View spec redefined a canonical top-level key in the Metric View YAML specification from `dimensions` (now legacy) to `fields`.
These both refer to the collection of columns—whether direct references to source columns or defined by a SQL expression—that is available to query in the Metric View.
[The documentation indicates that, `fields` is to be preferred, but both terms remain valid](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#dimensions).
We have updated the Metric View object model in the Semantic Bridge to align with this.
Serialization and deserialization continue to work with either key in conformance with the Metric View spec.
We offer backward-compatibility shims in the object model for the old "dimension"-associated names.
Users of the object model in C# scripts should migrate to "field"-associated names when they can.

**Who this affects**: anyone writing Metric View YAML by hand, anyone using the Metric View object model in C# scripts in Tabular Editor.

## Versioning

This change came after the v1.1 spec was published, and with no new spec version.
As such, we take a conservative approach in the Semantic Bridge.
We treat `dimensions` as the default for v0.1 and v1.1 Metric Views.
In the future, we will treat `fields` as the default for any newer-versioned Metric Views.
This is out of caution and a desire to offer the most interoperability with any other tools that may not be up to date with the latest published Metric View spec.

## Serialization and deserialization

Per [Metric View documentation](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#dimensions), both keys remain valid for serialization.

We emit a warning upon deserialization when a Metric View's top-level keyword is not what was documented for that version.
The canonical keyword is `dimensions` before v1.1 and `fields` from v1.1 onward.
So we warn when a pre-v1.1 (v0.1) Metric View uses `fields`, and when a v1.1 or later Metric View uses `dimensions`.
The canonical pairings, `dimensions` before v1.1 and `fields` at v1.1 and later, deserialize without a warning.
Emitting `dimensions` by default at v1.1 while also warning about it upon deserialization is deliberate:
we emit based on the earliest documented v1.1 spec to avoid breaking any other tooling that is not up to date with the latest spec,
and we warn because the latest spec now prefers `fields`.
These warnings do not affect any operations you might want to perform with the Semantic Bridge or the Metric View object model.

When we read a Metric View definition, we track the keyword used in the YAML, so that we can preserve the same keyword upon re-serializing the definition.
This guarantees that Metric View definitions have round-trip fidelity in our deserializer and serializer; e.g., if you have a v0.1 Metric View using `fields`, we will serialize it using the same keyword so you get the same YAML back out.

The Semantic Bridge default of `dimensions` for v0.1 and v1.1 comes into play if you deserialize a Metric View with neither of `dimensions` or `fields` defined.
In this case, we apply our default logic if you add fields to the Metric View via a C# script and then later serialize the Metric View to YAML.

We will continue to support both keywords in all Metric View versions unless a future spec update indicates otherwise.
You can continue to freely use either as you prefer, with notes about the warnings and defaults above for serialization and deserialization.

We treat the case of both keys in a definition as an error and will fail to deserialize such a Metric View.
We are aware of no way to generate such a case other than by hand-editing YAML; certainly you cannot accidentally do this via the Semantic Bridge or any operations we expose.
Such a Metric View definition, which uses both `dimensions` and `fields`, will need manual remediation.

An important note on the `materialization` block of the Metric View YAML definition: this section of YAML continues to use only `dimensions` regardless of the top-level key used.
[See the documentation for authoritative guidance on materialization](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#materialization).

Finally, there is no behavior or semantic difference in using either of `dimensions` or `fields`.
These keywords are simply synonyms, with guidance that `fields` is to be preferred.

## Metric View object model API change: `Dimension` to `Field`

In light of guidance that `fields` is to be preferred, we have aligned to this throughout the Semantic Bridge.
We ship a [Metric View object model for programmatic interaction with a Metric View](xref:semantic-bridge-metric-view-object-model), necessary for implementing the translations in the Semantic Bridge.
We have deprecated the `Dimension` object, and all associated methods and properties that used "dimension" or "dimensions" in their name.
We have created a new `Field` object, and new "field"-named methods and properties.
The `Dimension` object and associated methods and properties will now give you a warning about their obsolete state.
All `Dimension`-based code will continue to work, but we may remove these after a suitable amount of time has passed.
Like Databricks, we recommend that you use `Field` and associated methods for all new work.

In terms of implementation, all `Dimension`-based code passes through or mirrors the implementation of the `Field`-based code.
While we recommend using `Field`, you can use both interchangeably.
In general, migrating from `Dimension` to `Field` should be transparent.

A technical note, [`Dimension`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Dimension) is a subclass of `Field`.
As such, there are a few ways in which you might observe differences between `Field` and `Dimension` code, and there are reasonable workarounds.
To write code that survives `Dimension`'s removal, branch and declare against `Field`; never name or test the concrete `Dimension` type. Given a field `f`:

| Avoid                                                            | Use instead                                            | Why it breaks when `Dimension` is removed                                 |
|------------------------------------------------------------------|--------------------------------------------------------|---------------------------------------------------------------------------|
| `f is Dimension`                                                 | `f is Field`                                           | `Dimension` stops compiling; `is Field` is true in both eras              |
| `f is Dimension x`                                               | `f is Field x`                                         | same                                                                      |
| `case Dimension x:`                                              | `case Field x:`                                        | same                                                                      |
| `(Dimension)f`, `f as Dimension`                                 | use `f` directly as a `Field` (no cast)                | the cast target disappears; `f` already is a `Field`                      |
| `f.GetType() == typeof(Dimension)`                               | `f is Field`                                           | `typeof(Dimension)` stops compiling                                       |
| `f.GetType() == typeof(Field)`                                   | `f is Field`                                           | false now (runtime type is `Dimension`), true later, so it silently flips |
| `f.GetType().Name == "Dimension"` (or `== "Field"`)              | `f is Field`; for a label, `f.ToString()` or `f.Name`  | the type-name string is `"Dimension"` now, `"Field"` later                |
| `Dimension x = ...`, `List<Dimension>`, `IEnumerable<Dimension>` | `Field x = ...`, `view.Fields`, `IReadOnlyList<Field>` | the `Dimension` type name goes away                                       |
| `typeof(Dimension)`, `nameof(Dimension)`                         | `typeof(Field)`, `nameof(Field)`                       | the `Dimension` symbol is removed                                         |
| `MakeValidationRule<MetricView.Dimension>(...)`                  | `MakeValidationRule<MetricView.Field>(...)`            | the type argument references a removed type                               |

> [!NOTE]
> The object model deprecation of the `Dimension` type and any future removal of this type and associated methods will have no effect on serializing or deserializing with either YAML keyword.

## Name reference: `Dimension` to `Field`

The following table lists each deprecated `Dimension`-based name and its canonical `Field`-based replacement. The legacy names still compile (with an obsolete warning) and behave identically; prefer the canonical names in new scripts.

| Legacy name (obsolete)                                          | Canonical name                                              | Where                                                                  |
|-----------------------------------------------------------------|-------------------------------------------------------------|------------------------------------------------------------------------|
| `MetricView.Dimension` (type)                                   | `MetricView.Field` (type)                                   | Object model                                                           |
| `view.Dimensions`                                               | `view.Fields`                                               | `View` collection                                                      |
| `view.Dimensions["name"]`                                       | `view.Fields["name"]`                                       | Name-based indexing into the collection                                |
| `view.AddDimension(name, expr)`                                 | `view.AddField(name, expr)`                                 | `View` method                                                          |
| `SemanticBridge.MetricView.MakeValidationRuleForDimension(...)` | `SemanticBridge.MetricView.MakeValidationRuleForField(...)` | Validation rule helper (both overloads, with and without `minVersion`) |
| `context.DimensionNames`                                        | `context.FieldNames`                                        | Context passed to a validation rule                                    |

## Related

- @semantic-bridge
- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-validation
- [Metric View API](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
