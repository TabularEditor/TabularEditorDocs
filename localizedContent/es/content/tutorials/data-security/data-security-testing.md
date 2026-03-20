---
uid: data-security-testing
title: Pruebas de RLS/OLS
author: Kurt Buhler
updated: 2023-03-02
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Probar la seguridad de los datos mediante suplantación

![Resumen Visual de la seguridad de datos](~/content/assets/images/data-security/data-security-testing-visual-abstract.png)

---

Las **Consultas DAX**, el **Pivot Grid** o la **Vista previa de datos** permiten poner a prueba la seguridad de los datos en Tabular Editor. Se recomienda _siempre_ probar la seguridad de los datos ante cualquier cambio en la configuración, para mitigar el riesgo de una implementación incorrecta de RLS/OLS y sus consecuencias.

> [!IMPORTANT]
> Las pruebas de seguridad de datos con suplantación en Tabular Editor 3 están limitadas a Datasets alojados en una instancia de Analysis Services o en Power BI Service. Las licencias de Tabular Editor 3 Desktop no pueden aprovechar esta funcionalidad.

---

- [**Acerca de la seguridad de datos y RLS/OLS:**](data-security-about.md) Una descripción general funcional de <span style="color:#01a99d">RLS</span> y <span style="color:#8d7bae">OLS</span>.
- [**Modificar/Configurar una configuración de RLS:**](data-security-setup-rls.md) Cómo configurar <span style="color:#01a99d">RLS</span> en un Dataset.
- [**Modificar/Configurar una configuración de OLS:**](data-security-setup-ols.md) Cómo configurar <span style="color:#8d7bae">OLS</span> en un Dataset.
- **Probar RLS/OLS mediante suplantación (este artículo):** Cómo validar fácilmente la seguridad de los datos con Tabular Editor.

---

## Pruebas con suplantación

**La seguridad de los datos se puede probar fácilmente mediante la _suplantación_ en Tabular Editor 3.** La suplantación es una funcionalidad que te permite ver el resultado de una consulta como si fueras un rol o un usuario del modelo. Es similar a la funcionalidad _"Ver como rol..."_ del servicio de Power BI, con dos diferencias clave:

1. El usuario final suplantado necesita **permisos de compilación del Dataset**, además de la asignación de rol y el acceso de lectura al Dataset.
2. Puedes ejecutar cualquier consulta dentro de Tabular Editor 3; no está limitado a los Visuales disponibles del Report, como ocurre en el servicio de Power BI.

Esto es valioso, ya que permite al desarrollador ejecutar pruebas predefinidas para ver cómo vería el resultado cualquier usuario final con permisos de compilación. Esto ayuda a garantizar que, incluso con consultas complejas y expresiones DAX, la seguridad de datos funcione como se espera y que los usuarios solo vean lo que deben.

> [!IMPORTANT]
> Asegúrate de que no se concedan permisos de compilación al asignar a los usuarios finales roles del Workspace (Contributor, Member, Admin), ya que estos roles tienen permisos de **Write** sobre el Dataset y, por tanto, eluden la seguridad de datos; parecerá que las pruebas no funcionan, aunque esté configurado correctamente.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-impersonation-demo.gif" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Demostración de pruebas de RLS en Tabular Editor mediante suplantación. Se muestran las pruebas con (A) Vista previa de datos, (B) Consultas DAX y (C) Pivot Grid.</figcaption>
</figure>

---

## Cómo probar con suplantación

Para probar con suplantación, sigue estos pasos:

1. **Asegúrate de que la configuración y el acceso al Dataset sean correctos:**
   Los usuarios finales que se van a suplantar...

- _...estén asignados a los **roles** adecuados._
- _...tengan concedido el **Acceso de lectura al Dataset**._
- _...tengan concedido el **Acceso de compilación al Dataset**. (Power BI)_
- _...**no sean** Contributor, Member ni Admin del Workspace (Power BI)_.

2. **Crea una nueva Consulta DAX, un Pivot Grid o una ventana de Vista previa de datos:**

- Se recomienda empezar con _Vista previa de datos_ para observar el efecto en las tablas del modelo
- Después, realiza una segunda validación con una _DAX Query_. Esto se debe a que las consultas DAX se pueden guardar como documentación y para consultarlas más adelante si se produce un cambio en el modelo que requiera volver a probar.

3. **Selecciona 'Suplantación' e introduce el correo electrónico del usuario**: Si has implementado _RLS estático_, puedes probar el rol en su lugar.

4. **Explora los datos para validar que los resultados se muestran como se espera:** (según las reglas de seguridad).

### Consejos para las pruebas

1. **Prueba con más de un usuario:** Se recomienda probar al menos 3-10 usuarios distintos por rol. También puedes automatizar las pruebas para recorrer cada UPN de la tabla de seguridad (por ejemplo, usando C# Scripts y macros).

2. **Prueba cada rol y permiso de tabla:** Dado que cada permiso de tabla representa una expresión de filtro DAX diferente, hay que probarlos todos por separado. Asegúrate de que se prueba cada rol y de que cada prueba incluye las tablas pertinentes con las expresiones de filtro configuradas. Por ejemplo, si un rol incluye expresiones de filtro en las tablas 'Customers' y 'Products', asegúrate de que la consulta incluya atributos de ambas tablas para la validación.

3. **Prueba muchas consultas/medidas:** Intenta encontrar consultas complejas para probar, especialmente las que puedan resultar problemáticas en el contexto de la seguridad de datos. Por ejemplo, si los cálculos requieren comparar con un promedio total sin filtrar (es decir, el % del total) y se espera que _ese total_ no esté filtrado en RLS, es posible que el desarrollador tenga que replantearse la implementación de la seguridad de datos en función del modelo.