---
uid: data-security-about
title: ¿Qué es la seguridad de los datos?
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

# ¿Qué es la seguridad de los datos?

![Resumen Visual de la seguridad de los datos](~/content/assets/images/data-security/data-security-visual-abstract.png)

---

Los Dataset publicados se pueden configurar con seguridad de datos mediante <span style="color:#01a99d">[seguridad a nivel de filas (RLS)](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls)</span> (para tablas) o <span style="color:#8d7bae">[seguridad a nivel de objetos (OLS)](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-ols?tabs=table)</span> (para tablas y columnas). **El objetivo de la seguridad de los datos es garantizar que los usuarios solo vean y usen los datos para los que tienen permiso, tanto en Report publicados como al crear sus propias soluciones de datos de autoservicio.** Para ello, a los usuarios se les asignan **roles** con reglas de <span style="color:#01a99d">**RLS**</span> u <span style="color:#8d7bae">**OLS**</span>, que <span style="color:#01a99d">**aplican FILTER (RLS)**</span> o <span style="color:#8d7bae">**restringen (OLS)**</span> las consultas generadas por Report y herramientas de cliente como Power BI Desktop o Excel.

Aunque [no es obligatoria](https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance#when-to-avoid-using-rls), [la seguridad de datos es una característica común de una solución de BI empresarial sólida, segura y conforme](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-security-report-consumer-planning#enforce-data-security-based-on-consumer-identity). Esta serie es una introducción práctica a la seguridad de datos, en lo que respecta al modelado tabular y Tabular Editor.

_Tanto RLS como OLS se pueden configurar, modificar y probar fácilmente desde Tabular Editor._

---

- **Acerca de la seguridad de datos y RLS/OLS (este artículo):** Una visión general funcional de <span style="color:#01a99d">RLS</span> y <span style="color:#8d7bae">OLS</span>.
- [**Modificar/configurar la configuración de RLS:**](data-security-setup-rls.md) Cómo configurar <span style="color:#01a99d">RLS</span> en un Dataset.
- [**Modificar/configurar la configuración de OLS:**](data-security-setup-ols.md) Cómo configurar <span style="color:#8d7bae">OLS</span> en un Dataset.
- [**Probar RLS/OLS con suplantación de identidad:**](data-security-testing.md) Cómo validar fácilmente la seguridad de los datos con Tabular Editor.

<div class="NOTE">
  <h5>¿POR QUÉ CONFIGURAR LA SEGURIDAD A NIVEL DE FILAS O LA SEGURIDAD A NIVEL DE OBJETOS?</h5>
  Configurar RLS u OLS puede ser beneficioso para su modelo y sus Reports:  
  <li> Reduce el riesgo y mejora la gobernanza, garantizando que los usuarios solo vean los datos a los que tienen acceso.
  <li> Configura RLS dinámico con tablas centrales de roles para mantener la consistencia y facilitar el mantenimiento.
  <li> Mantén un control granular sobre qué datos y objetos se pueden consultar.
</div>

---

### ¿Cómo funciona?

La seguridad de datos funciona a nivel de modelo. Se configura siguiendo los pasos que se indican a continuación:

#### 1. **Crear roles:**

Los _roles_ son grupos de usuarios que comparten los mismos permisos o la misma lógica de seguridad de datos. En este caso, los _usuarios_ se identifican por su correo electrónico, o por el correo electrónico de un [grupo de seguridad de Azure AD](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-security-tenant-level-planning#integration-with-azure-ad). Ejemplos de roles:

- Usuarios de la misma región, equipo o departamento (_EMEA_, _UA Sales Team_).
- Usuarios con el mismo rol, función o nivel de autorización de acceso (_Key Account Managers_, _SC Clearance_).
- Grupos definidos por otra lógica de negocio o por reglas arbitrarias (_Externals_, _Build Users_).

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-create-role.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> En Tabular Editor, los roles son uno de los tipos de objetos de nivel superior (como tablas, relaciones, etc.).</figcaption>
</figure>

> [!IMPORTANT]
> Después de crear un nuevo rol en Tabular Editor, primero debe establecer la propiedad `Model Permission` en `Read`.

#### 2. **Especificar reglas:**

Las _reglas_ se aplican para cada rol a uno o varios objetos, en función del tipo de seguridad:

- _<span style="color:#01a99d">Permisos de tabla para RLS:</span>_ Expresiones de tabla DAX: devuelven cada fila que evalúa como `True`. Estos permisos atraviesan relaciones; **el diseño del modelo es clave para definir buenas reglas de RLS.**

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-table-permissions.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 2:</strong> En Tabular Editor, los permisos de tabla para RLS son visibles bajo el rol. Se pueden crear nuevos permisos de tabla haciendo clic con el botón derecho en un rol y seleccionando <i>"Agregar partición de tabla..."</i></figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-table-permissions-dax.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 3:</strong> El DAX del permiso de tabla se muestra en el Editor de expresiones al seleccionar un permiso de tabla.</figcaption>
</figure>

- _<span style="color:#8d7bae">Permisos de objeto de OLS:</span>_ Estos permisos se aplican a los objetos principales, así como a todos los dependientes aguas abajo.
  - `Read` (Puede ver / consultar)
  - `None` (No puede ver / consultar)
  - `Default` (No hay ninguna directiva configurada; equivale a `Read`)

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-table-permissions-dax.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 4:</strong> En Tabular Editor, los permisos de objeto están disponibles en la ventana "Propiedades", en el encabezado "Traducciones, Perspectivas, Seguridad".</figcaption>
</figure>

#### 3. **Asignar usuarios a los roles:**

Una vez configurado el Dataset, debes asignar a los usuarios a sus roles correspondientes.

- _Power BI:_ Los roles se asignan mediante Tabular Editor o a través del **servicio de Power BI/Fabric**, [en la configuración del Dataset del Workspace](https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security#manage-security-on-your-model).
- _SSAS / AAS:_ Los roles se asignan mediante el objeto rol, haciendo clic con el botón derecho y seleccionando "Editar miembros..."
- _Power BI Embedded:_ Debes [generar un token de inserción](https://learn.microsoft.com/en-us/power-bi/developer/embedded/cloud-rls#generate-an-embed-token).

Puedes asignar y quitar usuarios/grupos de los roles en Tabular Editor de la siguiente manera:

1. Haz clic con el botón derecho en el **rol** y selecciona **Editar miembros**...

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-edit-members.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 7:</strong> Los usuarios pueden asignarse a los roles haciendo clic con el botón derecho en un rol y seleccionando <i>'Editar miembros...'.</i></figcaption>
</figure>

2. Haz clic en el **botón desplegable** de 'Agregar miembro de Windows AD' y elige **Miembro de Azure AD**:

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-edit-members-dialog.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 8:</strong> En modelos AAS/SSAS, los usuarios pueden agregarse mediante el cuadro de diálogo <i>'Editar miembros...'</i>.</figcaption>
</figure>

3. Especifica la identidad del usuario de Azure AD (normalmente, el correo electrónico del usuario) como la propiedad **Nombre del miembro**.
4. Haz clic en **Aceptar**.
5. **Guarda** el modelo.

> [!IMPORTANT]
> Si tu organización usa Active Directory local con SQL Server Analysis Services, tendrás que usar la opción **Miembro de Windows AD** en lugar de **Miembro de Azure AD**.

> [!NOTE]
> Se [recomienda](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-security-tenant-level-planning#strategy-for-using-groups) gestionar la seguridad de los datos y el acceso con [grupos de Azure Active Directory](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/how-to-manage-groups). <br>Se prefiere este enfoque, ya que puedes centralizar la administración de la seguridad y la segmentación de usuarios.

#### 4. **Conceder a los usuarios acceso al Dataset:**

_Power BI:_ Se debe conceder a los usuarios acceso al Dataset según el [escenario de uso](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-overview).

- _App Audience:_ Los usuarios o sus grupos de Azure AD se agregan a la [App Audience](https://data-goblins.com/power-bi/app-audiences) adecuada.
- _Workspace Viewer:_ Los usuarios o sus grupos de Azure AD se agregan como [visores del Workspace](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-workspaces-workspace-level-planning#workspace-access)
- _Dataset Readers:_ A los usuarios o a sus grupos de Azure AD se les conceden [permisos específicos del Dataset](https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-manage-access-permissions) mediante un Dataset o un elemento dependiente (es decir. Report).

> [!WARNING]
> A los usuarios a los que se les asignen los [roles de Workspace de Administrador, Miembro o Colaborador](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-roles-new-workspaces#workspace-roles) se les conceden **_permisos de escritura_** sobre un Dataset. Por lo tanto, la seguridad de datos, como RLS y OLS, no filtrará ni bloqueará datos para los usuarios con estos roles. <br><br>
> **_Si un usuario es Administrador, Miembro o Colaborador, podrá ver todos los datos_**. <br><br>
> En la medida de lo posible, procura distribuir y administrar los permisos mediante Power BI Apps.

#### 5. **Validación de seguridad:**

RLS y OLS solo se pueden probar mediante suplantación una vez que se hayan agregado los grupos de usuarios y se les haya concedido acceso. Valida la seguridad mediante:

- _Tabular Editor:_ Usando [Suplantación de usuario](data-security-testing.md).
- _Servicio de Power BI:_ en la [configuración de seguridad del Dataset](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls#validating-the-role-within-the-power-bi-service).

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-impersonation.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 5:</strong> La forma más sencilla de probar la seguridad de datos es mediante suplantación con Tabular Editor. La opción "Suplantación" está disponible en cualquier función de consulta de datos (Consultas DAX, Pivot Grid, Vista previa de datos).</figcaption>
</figure>

> [!NOTE]
> Para validar la seguridad de datos mediante suplantación, deben cumplirse todas las condiciones siguientes:
>
> - Al usuario se le debe asignar un rol.
> - El usuario debe tener permisos de lectura sobre el Dataset.
> - El usuario debe tener **permisos de compilación** sobre el Dataset.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-impersonation-demo.gif" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 6:</strong> Una demostración de pruebas de RLS en Tabular Editor mediante suplantación. Se muestran pruebas con (A) Vista previa de datos, (B) Consultas DAX y (C) Pivot Grid.</figcaption>
</figure>

> [!IMPORTANT]
> Las pruebas de seguridad de datos mediante suplantación con Tabular Editor 3 están limitadas a los Datasets alojados en el servicio Power BI Datasets. Las licencias de escritorio de TE3 no pueden aprovechar esta funcionalidad. Esto se debe a que los roles se asignan en el servicio de Power BI.

---

### ¿Qué aspecto tiene?

En función de cómo hayas diseñado y configurado la seguridad de datos, la experiencia puede variar para los usuarios.
A continuación se muestran ejemplos típicos de escenarios comunes de implementación de RLS y/o OLS en un Dataset

_Haz clic en una pestaña para ver el ejemplo y obtener una explicación de cada uno:_

---

# [Ninguno](#tab/nodatasecurity)

**Sin seguridad, cualquier persona con acceso al Dataset puede ver todos los datos.**

La única restricción es si tienen acceso a los Report o a los Dataset.

![Sin seguridad](~/content/assets/images/data-security/data-security-no-security.png)

_En el ejemplo, tanto Jack como Janet pueden ver todos los datos._

# [RLS estático](#tab/staticrls)

**Con RLS configurado, los datos se filtran para mostrar solo las filas que el usuario tiene permiso para ver.** Esto se hace según los _permisos de tabla_ configurados en el modelo para esa tabla y ese rol. Estos permisos de tabla son expresiones de tabla DAX configuradas para una tabla específica del modelo. Se devuelven las filas que se evalúan como `True`; las filas que devuelven `False` se filtran debido a RLS.

Los permisos de tabla más sencillos son _estáticos_:

```dax
// permiso de tabla para la tabla 'Regions' y el rol 'CTG'
'Regions'[Territory] = "Central Transit Gate"
```

![Configuración de RLS estático](~/content/assets/images/data-security/data-security-static-rls.png)

_En el ejemplo:_

1. _Jack solo puede ver las filas para las que 'Region'[Territory] = "Central Transit Gate", ya que pertenece al rol 'CTG'._
2. _Los directivos, que tienen permiso para ver todos los datos, se agregan a un rol sin permisos de tabla._
3. _Tommy, un usuario que puede acceder al Dataset pero no pertenece a ningún rol, no verá ningún dato. Todos los Visual y las consultas devolverán un «recuadro gris de la muerte»._

_Es necesario crear roles al usar la seguridad de datos, incluso cuando hay usuarios como los directivos, que tienen acceso a los datos sin restricciones._

# [RLS dinámico](#tab/dynamicrls)

**Con RLS configurado, los datos se filtran para mostrar solo las filas que el usuario tiene permiso para ver.**
Esto se hace según los _permisos de tabla_ configurados en el modelo para esa tabla y ese rol.

Estos permisos de tabla son expresiones de tabla DAX configuradas para una tabla específica del modelo.
Se devuelven las filas que se evalúan como `True`; las filas que devuelven `False` se filtran debido a RLS.

**El RLS _dinámico_ se basa en las funciones `USERPRINCIPALNAME()` o `USERNAME()` para compararlas con los valores de una tabla de seguridad.**
La tabla de seguridad devolverá entonces la lógica que aplica el filtro de tabla a esa u otra tabla del modelo.

A esto se le llama RLS _dinámico_ porque el resultado cambiará en función del usuario, es decir, su `USERPRINCIPALNAME()`.
A continuación se muestra un ejemplo de permiso de tabla de RLS dinámico:

```dax
// permiso de tabla para 'Regions' y el rol 'Territory Directors'.

// Obtener el usuario actual
VAR _CurrentUser = 
SELECTCOLUMNS (
	FILTER ( 
		'Employees',
		'Employees'[Employee Email] = USERPRINCIPALNAME ()
	), 
	"@Name", 'Employees'[Employee Name]
)
RETURN 
'Regions'[Territory Directors] IN _CurrentUser
```

El permiso de tabla anterior obtiene el alias de la columna Employee Name de la tabla 'Employees' y se aplica sin que exista una relación con la tabla 'Regions'.
El resultado para cualquier usuario agregado a este rol es que solo verá datos donde:

1. Su correo electrónico está en la columna 'Employees'[Employee Email]
2. Su alias en 'Employees'[Employee Name] coincide con uno en 'Regions'[Territory Directors]

![Configuración de RLS dinámica](~/content/assets/images/data-security/data-security-dynamic-rls.png)

_En el ejemplo, cada director de territorio solo ve los territorios de los que es responsable:_

1. _Jack ve "Central Transit Gate" y "Io"._
2. _Janet ve "Arcadia III"._
3. _Elisa ve todos los datos, ya que el rol Execs no tiene ningún permiso de tabla configurado._

_La RLS dinámica es la forma más común de proteger un Dataset empresarial. Normalmente requiere configurar y mantener una **Tabla de seguridad** central, utilizada en todos los Datasets empresariales._

# [RLS (Varios roles)](#tab/multipleroles)

**Cuando se asigna un usuario a varios roles, cada uno con permisos de tabla diferentes, verá los datos permitidos por cualquiera de esos roles.** Los usuarios verán datos cuando al menos una expresión DAX de permisos de tabla se evalúe como `True` para las filas de las tablas del modelo; se aplica el operador lógico `OR`.

Esto puede ser peligroso si no se espera; algunos desarrolladores pueden anticipar que se tome la intersección; es decir, mostrar solo las filas donde **ambos** permisos de tabla devuelven `True`. Esto solo ocurrirá si los permisos de tabla se configuran para varias tablas del modelo; **dentro de un rol**, se toma la intersección de todos los permisos de tabla del modelo.

![Los roles de RLS combinan los permisos de tabla mediante un OR lógico](~/content/assets/images/data-security/data-security-combining-rls-roles.png)

_En el ejemplo:_

1. _Jack está asignado a los roles 'CTG' y 'FTL'. Verá todas las filas en las que 'Products'[Type] = "FTL" **O** en las que 'Regions'[Territory] = "Central Transit Gate". Es probable que este no sea el comportamiento esperado; el desarrollador probablemente pretende obtener el resultado del rol 'CTG/FTL', que devuelve solo las filas donde ambas condiciones son verdaderas._
2. _Elijah tiene el rol 'FTL' y solo verá las filas en las que 'Products'[Type] = "FTL".
3. _Abdullah tiene el rol 'CTG/FTL' y solo verá las filas en las que **AMBAS** 'Products'[Type] = "FTL" **Y** 'Regions'[Territory] = "Central Transit Gate"._

_Situaciones como esta ilustran la importancia de diseñar una configuración de seguridad de datos clara durante el diseño del modelo, asegurando que se alinee con las políticas de la organización y las prácticas existentes de seguridad de datos y administración de accesos._

# [OLS](#tab/ols)

**Con OLS configurado como `None`, se impide que las consultas se evalúen; devuelven un error.** Esta es una diferencia importante respecto a RLS; RLS filtra los datos, pero OLS impide la evaluación. Si el permiso de OLS se establece en `Read`, no hay ningún efecto. Esto se hace según el nivel de permiso de OLS de la columna o la tabla, y **afecta a todos los elementos dependientes aguas abajo** como las relaciones y las medidas.

![OLS configurado para la columna Cost](~/content/assets/images/data-security/data-security-ols.png)

_En el ejemplo, la columna 'Territory Sales'[Cost] tiene un permiso de OLS de `None` para el rol 'Sales'. Esto se debe al siguiente requisito:_

`Los usuarios de 'Sales' pueden ver los datos de 'Sales', pero no los de Cost ni los de Margin.`

_Esto significa que un usuario que pertenezca al rol 'Sales', como Jack, no podrá ver:_

1. _Cualquier consulta o Visual que haga referencia directamente a la columna 'Territory Sales'[Cost]_
2. _Cualquier medida de DAX o elemento de cálculo que haga referencia directamente a la columna 'Territory Sales'[Cost], como [Margin %]_
3. _Cualquier medida de DAX o elemento de cálculo que haga referencia _indirectamente_ (aguas abajo) a la columna 'Territory Sales'[Cost]._
4. _Cualquier objeto que tenga una columna con una relación con 'Territory Sales'[Cost]_

_El resultado de 1-4 será un **error** durante la evaluación de la consulta. Un Visual de Power BI mostrará un **cuadro gris de la muerte**._

> [!WARNING]
> __Los usuarios de negocio a menudo percibirán los resultados esperados de OLS como si el Report, el Visual o la consulta estuvieran "rotos". __ <br>Si usas OLS y se espera que los usuarios se enfrenten a estas evaluaciones, prueba lo siguiente:<br>
>
> 1. Forma a los usuarios sobre la seguridad.
> 2. Intenta controlar el error y devolver un mensaje más significativo.
> 3. En escenarios de Build, considera ocultar el objeto.
> 4. Otra optimización que conviene probar es establecer `IsPrivate` en `True` o `IsAvailableInMDX` en `False`.

# [RLS+OLS (Un solo rol)](#tab/rlsols)

Con RLS y OLS configurados, hay dos posibles resultados:

1. **El usuario tiene _un rol_ con RLS y OLS:** La seguridad funcionará como se espera, siempre que esté configurada correctamente.
2. **El usuario tiene _varios roles_ en los que RLS y OLS están configurados por separado:** La combinación de roles no es compatible y el usuario recibirá un error.

Debido a #2, si esperas usar tanto RLS como OLS, esto debe considerarse cuidadosamente durante el diseño del modelo.

A continuación se muestra un ejemplo de #1:

![Combinar OLS y RLS en el mismo rol produce el resultado esperado](~/content/assets/images/data-security/data-security-ols-and-rls-functional.png)

_En el ejemplo:_

1. _Jack, que tiene asignado el rol 'CTG':_
   - _Solo puede ver los datos de "Central Transit Gate" debido al permiso de tabla RLS en 'Regions'._
   - _Solo puede ver datos de ventas; no puede ver [Margin %]. Esto se debe al permiso de objeto de OLS `None` en 'Territory Sales'[Cost], lo que afecta a la medida dependiente [Margin %]_
2. _Elisa, que tiene asignado el rol 'Execs', puede ver todos los datos. No se ha configurado ningún permiso de tabla de RLS ni permiso de objeto de OLS (establecido en `Default`) para 'Execs'._
3. _Tommy, que no tiene asignado ningún rol, no puede ver ningún dato._

> [!WARNING]
> Los escenarios que combinan RLS y OLS no son raros. <br>Los escenarios en los que se usan correctamente sí lo son. <br>Asegúrate de que, si tienes el requisito de usar RLS y OLS juntos, lo consideres cuidadosamente durante el diseño del modelo.

# [❌ RLS+OLS (Combinar roles)](#tab/rlsolscombined)

Con RLS y OLS configurados, hay dos resultados posibles:

1. **El usuario tiene _un rol_ con RLS y OLS:** La seguridad funcionará como se espera, siempre que esté configurada correctamente.
2. **El usuario tiene _varios roles_ en los que RLS y OLS están configurados por separado:** La combinación de roles no es compatible y el usuario recibirá un error.

Debido a #2, si prevés usar RLS y OLS, debes considerarlo cuidadosamente durante el diseño del modelo.

A continuación se muestra un ejemplo de #2:

![❌ Combinar OLS y RLS entre roles producirá un error](~/content/assets/images/data-security/data-security-ols-and-rls-dysfunctional.png)

_En el ejemplo anterior:_

1. _Jack, que tiene asignado el rol 'Read Users':_
   - _Solo puede ver los datos de "Central Transit Gate" debido al permiso de tabla RLS en 'Regions'._
   - _Solo puede ver datos de ventas; no puede ver [Margin %]. Esto se debe al permiso de objeto de OLS `None` en 'Territory Sales'[Cost], lo que afecta a la medida dependiente [Margin %]_
2. _Janet, a quien se le han asignado los roles "Read Users" y "Build Users":_
   - _No se puede ver ningún dato. La combinación de permisos de RLS/OLS entre los roles no es válida._

_Los usuarios a los que se conceden permisos de compilación en el Dataset se agregan al grupo de seguridad Build de Azure AD, que está asignado al rol "Build Users". Los usuarios de compilación pueden ver tablas que no están en los Report ya existentes, por lo que se configura el permiso OLS `None` para la tabla "Employees". Esto produce una combinación en la que los permisos de RLS y OLS no se pueden conciliar, lo que provoca un error._

> [!WARNING]
> Los escenarios que combinan RLS y OLS no son raros. <br>Los escenarios en los que se usan correctamente sí lo son. <br>Asegúrate de que, si necesitas RLS y OLS a la vez, lo consideres detenidamente durante el diseño del modelo.

# [❌ Sin roles](#tab/role)

**Ningún usuario podrá leer ningún dato hasta que se le agregue al rol**, siempre que la seguridad de datos esté configurada en el Dataset.

![Sin acceso o sin rol](~/content/assets/images/data-security/data-security-no-role.png)

> [!NOTE]
> No olvides dar a los usuarios acceso al Dataset y añadirlos al rol de seguridad.

# [❌ Sin acceso](#tab/access)

**Si añades a un usuario a un rol de seguridad, eso no le dará automáticamente acceso de lectura al Dataset.** Aun así, no podrá acceder a ningún Dataset ni a ningún Report.

![Sin acceso o sin rol](~/content/assets/images/data-security/data-security-no-access.png)

> [!NOTE]
> No olvides dar a los usuarios acceso al Dataset y añadirlos al rol de seguridad.

> [!WARNING]
> **Es una práctica recomendada evitar la distribución mediante roles de Workspace, siempre que sea posible.** <br> Si es necesario, asegúrate de aplicar el **Principio de mínimo privilegio**: los usuarios deben tener el acceso mínimo necesario para hacer lo que necesitan.

# [❌ Acceso mediante roles de Workspace](#tab/workspace)

**Si le das a un usuario acceso a un Dataset mediante los roles de Administrador, Miembro o Colaborador, podrá ver todos los datos, independientemente de la configuración de seguridad de datos y de los roles que tenga asignados.** Este es un error habitual al escalar o en ecosistemas de Power BI de autoservicio, y provoca filtraciones de datos e incumplimiento.

![Problemas con roles de Workspace](~/content/assets/images/data-security/data-security-workspace-roles.png)

> [!WARNING]
> **Es una práctica recomendada evitar la distribución mediante roles de Workspace, siempre que sea posible.** <br> Si es necesario, asegúrate de aplicar el **Principio de mínimo privilegio**: los usuarios deben tener el acceso mínimo necesario para hacer lo que necesitan.

---

---

### Limitaciones estrictas

Algunas características de Report o de Data model no funcionarán con una configuración de RLS u OLS. Algunos ejemplos son:

1. [Limitaciones de RLS](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls#considerations-and-limitations)
   - Entidades de servicio agregadas a los roles de RLS
   - Pruebas con modelos de DirectQuery usando SSO
   - [Publicar en la web en Power BI](https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance#when-to-avoid-using-rls)

2. [Limitaciones de OLS](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-ols?tabs=table#considerations-and-limitations)
   - Combinar roles de RLS y de OLS independientes (como se comentó arriba)
   - Funciones de preguntas y respuestas
   - Información rápida
   - Narrativa inteligente
   - Galería de tipos de datos de Excel

---

### Lecturas adicionales y referencias

Para obtener más información detallada sobre la seguridad de los datos, consulta las siguientes referencias:

1. [Documento técnico de seguridad de Power BI](https://learn.microsoft.com/en-us/power-bi/guidance/whitepaper-powerbi-security)
2. [Documentación de Power BI: seguridad](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-power-bi-security)
3. [Documentación de Analysis Services: seguridad a nivel de objetos](https://learn.microsoft.com/en-us/analysis-services/tabular-models/object-level-security?view=asallproducts-allversions)
4. [Planificación de la implementación de Power BI: seguridad del Report](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-security-report-consumer-planning)
5. [(Relacionado) Planificación de la implementación de Power BI: protección de la información y prevención de pérdida de datos (DLP)](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-info-protection-data-loss-prevention-overview)