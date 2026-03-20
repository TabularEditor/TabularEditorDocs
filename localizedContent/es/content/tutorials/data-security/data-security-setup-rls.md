---
uid: data-security-setup-rls
title: Configurar o modificar RLS
author: Kurt Buhler
updated: 2023-03-14
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

# Configurar la seguridad a nivel de filas (RLS)

![Resumen Visual de seguridad de datos](~/content/assets/images/data-security/data-security-configure-rls-visual-abstract.png)

---

**RLS se modifica ajustando los roles o los permisos de tabla definidos en las tablas.** Esta _expresión de filtro_ de DAX se puede ver en la ventana del Editor de expresiones al seleccionar un permiso de tabla dentro de un rol específico. Esta expresión de filtro es la parte más importante de la configuración de RLS, ya que determina qué datos ve un usuario.

---

- [**Acerca de la seguridad de datos y RLS/OLS:**](data-security-about.md) Una descripción general funcional de <span style="color:#01a99d">RLS</span> y <span style="color:#8d7bae">OLS</span>.
- **Configurar o modificar una configuración de RLS (este artículo):** Cómo configurar <span style="color:#01a99d">RLS</span> en un Dataset.
- [**Configurar o modificar una configuración de OLS:**](data-security-setup-ols.md) Cómo configurar <span style="color:#8d7bae">OLS</span> en un Dataset.
- [**Pruebas de RLS/OLS con suplantación:**](data-security-testing.md) Cómo validar fácilmente la seguridad de datos con Tabular Editor.

---

## Configuración de RLS en Tabular Editor 3

_A continuación se muestra un resumen de cambios habituales que podrías hacer en una configuración de RLS existente:_

---

### 1. Eliminar un rol

Para eliminar un rol del modelo, basta con eliminar el objeto de rol con `Del` o haciendo clic con el botón derecho y seleccionando "Delete".

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-delete-role.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Eliminación de un rol en el modelo.</figcaption>
</figure>

> [!NOTE]
> Todos los usuarios asignados a este rol ya no podrán ver los datos del modelo, siempre que exista al menos otro rol.

---

### 2. Agregar un nuevo rol

Para agregar un rol al modelo:

1. **Haz clic con el botón derecho en el tipo de objeto 'Roles':** Esto abrirá el cuadro de diálogo para que puedas crear un nuevo rol.
2. **Selecciona 'Crear' > 'rol':** Asigna un nombre al nuevo rol.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-create-role.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 2:</strong> Creación de un nuevo rol en el modelo.</figcaption>
</figure>

3. **Establece la propiedad `Model Permission` en `Read`:** Esto es necesario para que cualquier miembro del rol pueda acceder al Dataset.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-model-permission-read.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 3:</strong> Es necesario establecer la propiedad `Model Permission`.</figcaption>
</figure>

4. **Establece permisos:** Configura los permisos de tabla de RLS y/o los permisos de objeto de OLS, como se describe a continuación.

---

### 3. Eliminar RLS

Para quitar el RLS del modelo, se deben eliminar todos los permisos de tabla. Para quitar la seguridad de datos del modelo, se deben eliminar todos los roles.

> [!NOTE]
> Una vez eliminados todos los roles, todos los usuarios podrán ver todos los datos siempre que tengan permisos de _Read_ sobre el Dataset.

---

### 4. Modificar un permiso de tabla

Para modificar un permiso de tabla existente para un rol específico:

1. **Expande el rol:** Esto mostrará los permisos de tabla.
2. **Selecciona el permiso de tabla:** Esto mostrará el DAX del permiso de filtro en el Editor de expresiones.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-table-permissions-dax.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 4:</strong> La expresión de filtro de DAX se muestra en el Editor de expresiones al seleccionar un permiso de tabla.</figcaption>
</figure>

3. **Ajusta la expresión de filtro / los permisos de tabla de RLS:** Se recomienda probar o validar el DAX antes de usarlo:

- Copia la expresión de filtro en una nueva ventana de Consulta DAX, bajo una instrucción `EVALUATE`.
- Agrégala como la expresión de una instrucción `ADDCOLUMNS` que itere sobre la tabla, o sobre una parte de la tabla.
- Ejecútala y observa los resultados.
- Sustituye `USERNAME()` o `USERPRINCIPALNAME()` en el RLS dinámico por un valor conocido de la tabla de seguridad.
- Vuelve a ejecutar la Consulta DAX y valida que los resultados aparezcan como se espera. Repite hasta quedar conforme.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-rls-validation.png" alt="Data Security Validation" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 5:</strong> Un ejemplo de cómo se puede validar RLS desde la ventana de Consulta DAX mediante la expresión FILTER dentro de un iterador sobre la tabla (o parte de ella, como el alias de usuario). En este ejemplo, se ha modificado (amarillo) la expresión de filtro RLS original en el permiso de tabla y, en su lugar, se ha añadido un User Principal Name explícito al Dataset para hacer la prueba (verde). El código de RLS se ejecuta dentro del iterador ADDCOLUMNS sobre una parte relevante de la tabla. La marca de verificación indica cualquier fila que, al ejecutarse con EVALUATE, se evalúa como TRUE. La prueba demuestra que el RLS —para este UPN— funciona como se espera, ya que <i>Gal Aehad</i> es el único usuario para el que se hace RETURN de TRUE cuando se indica su UPN.</figcaption>
</figure>

```dax
EVALUATE

// Crea una tabla para probar tu RLS
ADDCOLUMNS ( 
  VALUES ( 'Regions'[Territory Directors] ),
  "@RLS-Validation",

    // Código de RLS
    VAR _CurrentUser = 
      SELECTCOLUMNS (
        FILTER ( 
          'Employees', 
          'Employees'[Employee Email]

            // Reemplaza USERPRINCIPALNAME() por el correo de un usuario para probar
            = "gal.aehad@spaceparts.co" // USERPRINCIPALNAME ()
        ),
        "@Name", 'Employees'[Employee Name]
      )
    RETURN
      'Regions'[Territory Directors] IN _CurrentUser

)

// Ordena de TRUE() a FALSE()
// Cuando sea TRUE(), los datos serán visibles
ORDER BY [@RLS-Validation] DESC
```

---

### 5. Agregar un nuevo permiso de tabla a un rol

Para agregar un nuevo permiso de tabla:

1. **Haz clic con el botón derecho en el rol:** Selecciona 'Agregar permiso de tabla...'

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-table-permissions.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 6:</strong> En Tabular Editor, los permisos de tabla para RLS son visibles bajo el rol. Los nuevos permisos de tabla se pueden crear haciendo clic con el botón derecho en un rol y seleccionando <i>'Agregar partición de tabla...'</i></figcaption>
</figure>

2. **Selecciona la tabla y pulsa 'Aceptar':** Selecciona la tabla para la que quieras crear el permiso.
3. **Escribe la expresión FILTER / permisos de tabla de RLS:** Redacta el DAX de la expresión FILTER. Como antes, quieres validar esta expresión de filtro (Ver la **Figura 5**):

- Copia la expresión FILTER en una nueva ventana de Consulta DAX, debajo de una instrucción `EVALUATE`.
- Añádela como la expresión de una instrucción `ADDCOLUMNS` que itere sobre la tabla o sobre una parte de ella.
- Ejecútala y observa los resultados.
- Sustituye `USERNAME()` o `USERPRINCIPALNAME()` en el RLS dinámico por un valor conocido de la tabla de seguridad.
- Vuelve a ejecutar la Consulta DAX y valida que los resultados aparezcan como se espera. Repite hasta quedar conforme.

---

### 6. Asignar o quitar usuarios de un rol

Puedes asignar y quitar usuarios o grupos de los roles desde Tabular Editor.

1. Haz clic con el botón derecho en el **rol** y selecciona **Editar miembros**...

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-edit-members.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 7:</strong> Los usuarios pueden asignarse a roles haciendo clic con el botón derecho en un rol y seleccionando <i>'Editar miembros...'.</i></figcaption>
</figure>

2. Haz clic en el **botón desplegable** del botón 'Agregar miembro de Windows AD' y selecciona **Miembro de Azure AD**:

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-edit-members-dialog.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 8:</strong> Para modelos AAS/SSAS, los usuarios se pueden agregar mediante el cuadro de diálogo <i>'Editar miembros...'</i>.</figcaption>
</figure>

3. Especifica la identidad del usuario de Azure AD (normalmente, la dirección de correo electrónico del usuario) en la propiedad **Nombre de miembro**.
4. Haz clic en **Aceptar**.
5. **Guarda** el modelo.

> [!IMPORTANT]
> Si tu organización usa Active Directory local con SQL Server Analysis Services, tendrás que usar la opción **Miembro de Windows AD** en lugar de **Miembro de Azure AD**.

> [!NOTE]
> Una vez que hayas publicado un Dataset de Power BI en el servicio Power BI, también puedes administrar los miembros del rol desde la [configuración de seguridad del Dataset](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls#manage-security-on-your-model). Como alternativa, puedes administrar los miembros del rol desde [SQL Server Management Studio](https://learn.microsoft.com/en-us/analysis-services/tabular-models/manage-roles-by-using-ssms-ssas-tabular?view=asallproducts-allversions) (esto se aplica a los modelos AAS/SSAS, además del Dataset de Power BI).

---
