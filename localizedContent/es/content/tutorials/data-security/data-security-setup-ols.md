---
uid: data-security-setup-ols
title: Configurar o modificar OLS
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

# Configurar o modificar la seguridad a nivel de objetos (OLS)

![Resumen Visual de seguridad de datos](~/content/assets/images/data-security/data-security-configure-ols-visual-abstract.png)

---

**La OLS se modifica ajustando los roles o los permisos de objeto definidos para tablas o columnas.** Los permisos de objeto son propiedades TOM visibles en la propiedad `Object Level Security`, que puede ser `Default` (sin OLS; funcionalmente similar a `Read`), `Read` o `None`. La OLS se diferencia de la RLS en que no filtra los datos, sino que impide la ejecución del objeto **y de todos sus dependientes.** Esto significa que cualquier relación o medida que haga referencia al objeto donde `Object Level Security` esté establecido en `None` devolverá un error al evaluarse.

---

- [**Acerca de la seguridad de datos y RLS/OLS:**](data-security-about.md) Una visión general funcional de <span style="color:#01a99d">RLS</span> y <span style="color:#8d7bae">OLS</span>.
- [**Modificar/configurar una configuración de RLS:**](data-security-setup-rls.md) Cómo configurar <span style="color:#01a99d">RLS</span> en un Dataset.
- **Modificar/configurar la configuración de OLS (este artículo):** Cómo configurar <span style="color:#8d7bae">OLS</span> en un Dataset.
- [**Probar RLS/OLS con suplantación:**](data-security-testing.md) Cómo validar fácilmente la seguridad de datos con Tabular Editor.

---

## Configurar OLS en Tabular Editor 3

_A continuación se ofrece una visión general de los cambios habituales que se pueden realizar en una configuración de OLS existente. Además, a continuación se describen estrategias para configurar OLS en objetos no habituales (medidas, grupos de cálculo):_

---

### 1. Eliminar un rol

Para quitar un rol del modelo, basta con eliminar el objeto de rol pulsando `Del` o haciendo clic con el botón derecho y seleccionando "Eliminar".

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-delete-role.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Eliminación de un rol del modelo.</figcaption>
</figure>

> [!NOTE]
> Los usuarios asignados a este rol ya no podrán ver los datos del modelo, mientras exista al menos otro rol.

---

### 2. Agregar un nuevo rol

Para agregar un rol al modelo:

1. **Haz clic con el botón derecho en el tipo de objeto "Roles":** Se abrirá el cuadro de diálogo para crear un nuevo rol.
2. **Selecciona "Crear" > "Rol":** Asigna un nombre al nuevo rol.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-create-role.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 2:</strong> Creación de un nuevo rol en el modelo.</figcaption>
</figure>

3. **Establece la propiedad `Model Permission` en `Read`:** Esto es necesario para los Datasets de Power BI.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-create-role.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 3:</strong> Establecer la propiedad Model Permission es necesario para Power BI.</figcaption>
</figure>

4. **Configura los permisos:** Establece los permisos de tabla de RLS y/o los permisos de objeto de OLS, como se describe a continuación.

---

### 3. Eliminar OLS

Para eliminar OLS del modelo, todas las columnas y tablas deben tener la propiedad `Object Level Security` configurada en `Default` para todos los roles. Para quitar la seguridad de datos del modelo, tienes que eliminar todos los roles.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-ols-default.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 4:</strong> La propiedad de seguridad a nivel de objetos se encuentra en el panel de <i>Propiedades</i> al seleccionar una columna o tabla. La propiedad no existe para medidas, relaciones y otros tipos de objetos.</figcaption>
</figure>

> [!NOTE]
> Una vez que hayas eliminado todos los roles, todos los usuarios podrán ver todos los datos siempre que tengan permisos de _Read_ en el Dataset.

---

### 4. Configurar o cambiar OLS

Configurar o modificar OLS es muy fácil para columnas y tablas. Solo tienes que seleccionar el objeto y navegar hasta la propiedad `Object Level Security`, usando el desplegable para cambiarla al valor deseado.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-ols-change.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 4:</strong> La propiedad de seguridad a nivel de objetos se puede cambiar mediante el menú desplegable adyacente, que permite seleccionar <i>Default</i>, <i>None</i> o <i>Read</i>.</figcaption>
</figure>

---&#x20;

### 5. Combinar OLS con RLS

Combinar RLS con OLS con éxito requiere diseñar un modelo y una estrategia de seguridad de datos / gestión de acceso que estén alineados. Dado que RLS y OLS no se pueden combinar entre roles, esto significa que, si planeas implementar tanto RLS como OLS, los usuarios quedan limitados a un único rol.

---

### 6. Configurar OLS para las medidas

De forma nativa, OLS solo funciona con columnas, tablas y sus dependencias; no existe ninguna propiedad `seguridad a nivel de objetos` para las medidas. Sin embargo, como OLS también se aplica a las dependencias, es posible diseñar OLS que funcione con las medidas mediante tablas desconectadas o grupos de cálculo. Para ello, el DAX de la medida debe modificarse para evaluar una columna o un grupo de cálculo configurado con RLS. Si la propiedad `seguridad a nivel de objetos` de ese objeto es `None`, la medida no se evaluará.

Consulta también [este artículo de SQLBI](https://www.sqlbi.com/articles/hiding-measures-by-using-object-level-security-in-power-bi/), que explica en detalle este enfoque para ocultar medidas.