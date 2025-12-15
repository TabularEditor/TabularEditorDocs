# Applies To Examples

This document shows examples of the new `applies_to` front matter structure.

## Example 1: TE3 only, available since a specific version

```yaml
---
uid: example-feature
title: New Feature
author: Your Name
updated: 2025-11-04
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
      note: "Not available in TE2. Use TE3 for this feature."
    - product: Tabular Editor 3
      full: true
      since: 3.18.0
---
```

**Renders as:**
- **TE2** ❌ Not supported - Not available in TE2. Use TE3 for this feature.
- **TE3** ✅ Supported (Available since 3.18.0)

---

## Example 2: TE3 with edition-specific support

```yaml
---
uid: example-enterprise-feature
title: Enterprise Feature
author: Your Name
updated: 2025-11-04
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.15.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: "Limited to 10 objects"
        - edition: Enterprise
          full: true
---
```

**Renders as:**
- **TE2** ❌ Not supported
- **TE3** (Available since 3.15.0)
  - ❌ Desktop Edition
  - ⚠️ Business Edition (Limited to 10 objects)
  - ✅ Enterprise Edition

**Important:** When you have `editions`, do NOT set `full`, `partial`, or `none` at the product level. The support status is determined by the individual editions.

---

## Example 3: Feature available in both TE2 and TE3

```yaml
---
uid: example-basic-feature
title: Basic Feature
author: Your Name
updated: 2025-11-04
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
```

**Renders as:**
- **TE2** ✅ Supported
- **TE3** ✅ Supported

---

## Example 4: Feature deprecated in later versions

```yaml
---
uid: example-deprecated-feature
title: Deprecated Feature
author: Your Name
updated: 2025-11-04
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
      since: 3.0.0
      until: 3.22.0
      note: "Deprecated in 3.23.0. Use the new API instead."
---
```

**Renders as:**
- **TE2** ✅ Supported
- **TE3** ✅ Supported (Available in 3.0.0–3.22.0) - Deprecated in 3.23.0. Use the new API instead.

---

## Example 5: TE3 only, all editions

```yaml
---
uid: example-te3-only
title: TE3 Exclusive Feature
author: Your Name
updated: 2025-11-04
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
      note: "Upgrade to TE3 for this feature"
    - product: Tabular Editor 3
      full: true
      since: 3.0.0
---
```

**Renders as:**
- **TE2** ❌ Not supported - Upgrade to TE3 for this feature
- **TE3** ✅ Supported (Available since 3.0.0)

---

## Example 6: Complex scenario with partial support

```yaml
---
uid: example-complex
title: Complex Feature
author: Your Name
updated: 2025-11-04
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "Requires manual scripting workaround"
    - product: Tabular Editor 3
      since: 3.12.0
      editions:
        - edition: Desktop
          partial: true
          note: "Read-only mode"
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
```

**Renders as:**
- **TE2** ⚠️ Partially supported - Requires manual scripting workaround
- **TE3** (Available since 3.12.0)
  - ⚠️ Desktop Edition (Read-only mode)
  - ✅ Business Edition
  - ✅ Enterprise Edition

---

## Migration Guide from Old Format

### Old Format:
```yaml
applies_to:
  editions:
    - edition: Desktop
      none: x
    - edition: Business
    - edition: Enterprise
  versions:
    - version: "3.x"
```

### New Format:
```yaml
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.15.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
```

## Key Differences

1. **Product-first approach**: Start with `products` array containing `TE2` and `TE3`
2. **Boolean flags**: Use `full: true`, `partial: true`, or `none: true` instead of presence/absence
3. **Version tracking**: Use `since` and `until` fields for version tracking (TE3 only)
4. **Notes**: Add explanatory `note` field at any level for tooltips/additional context
5. **Nested editions**: Editions are now nested under each product, allowing different edition support per product
6. **Important**: When a product has `editions`, do NOT set `full`/`partial`/`none` at the product level - only at the edition level
