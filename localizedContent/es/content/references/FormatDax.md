---
uid: formatdax
title: Deprecación de FormatDax
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      none: true
---

# Deprecación de FormatDax

El método `FormatDax` (que es uno de los [métodos auxiliares](xref:advanced-scripting#helper-methods) disponibles en Tabular Editor) ha quedado obsoleto con el lanzamiento de Tabular Editor 2.13.0.

El motivo de esta deprecación es que el servicio web de https://www.daxformatter.com/ estaba empezando a recibir una carga elevada de múltiples solicitudes en rápida sucesión, lo que les estaba causando problemas. Esto se debe a que el método `FormatDax` realiza una solicitud web cada vez que se invoca en un script, y muchas personas han estado usando scripts como el siguiente:

**¡No hagas esto!**

```csharp
foreach(var m in Model.AllMeasures)
{
    // DON'T DO THIS
    m.Expression = FormatDax(m.Expression);
}
```

Esto está bien para modelos pequeños con unas pocas decenas de medidas, pero el tráfico en www.daxformatter.com indica que se está ejecutando un script como el anterior en varios modelos con miles de medidas, ¡incluso varias veces al día!

Para abordar este problema, Tabular Editor 2.13.0 mostrará una advertencia cuando se llame a `FormatDax` más de tres veces seguidas, usando la sintaxis anterior. Además, las llamadas posteriores se limitarán, con un retraso de 5 segundos entre cada una.

## Sintaxis alternativa

Tabular Editor 2.13.0 incorpora dos formas distintas de llamar a FormatDax. El script anterior se puede reescribir de cualquiera de las siguientes maneras:

```csharp
foreach(var m in Model.AllMeasures)
{
    m.FormatDax();
}
```

...o simplemente...:

```csharp
Model.AllMeasures.FormatDax();
```

Ambos enfoques agruparán todas las llamadas a www.daxformatter.com en una sola solicitud. También puedes usar la sintaxis de método global si lo prefieres:

```csharp
foreach(var m in Model.AllMeasures)
{
    FormatDax(m);
}
```

...o simplemente...:

```csharp
FormatDax(Model.AllMeasures);
```

## Más detalles

Técnicamente, `FormatDax` ahora se ha implementado como dos métodos de extensión sobrecargados:

1. `void FormatDax(this IDaxDependantObject obj)`
2. `void FormatDax(this IEnumerable<IDaxDependantObject> objects, bool shortFormat = false, bool? skipSpaceAfterFunctionName = null)`

La sobrecarga núm. 1 anterior pondrá en cola el objeto proporcionado para darle formato cuando finalice la ejecución del script o cuando se llame al nuevo método `void CallDaxFormatter()`. La sobrecarga n.º 2 llamará inmediatamente a www.daxformatter.com mediante una única solicitud web, que dará formato a todas las expresiones DAX de todos los objetos proporcionados en el enumerable. Puedes usar cualquiera de estos métodos según te convenga.

Ten en cuenta que el nuevo método no acepta ningún argumento de tipo cadena. Tiene en cuenta todas las propiedades DAX del objeto proporcionado para darles formato (en las medidas, son las propiedades Expression y DetailRowsExpression; en los KPI, son StatusExpression, TargetExpression y TrendExpression, etc.).
