# 便利なスクリプトスニペット

ここでは、Tabular Editorの[Advanced Scripting機能](/Advanced-Scripting)を使い始めるための小さなスクリプトスニペットを集めています。これらのスクリプトの多くは[Custom Actions](/Custom-Actions)として保存すると、コンテキストメニューから簡単に再利用できるので便利です'。

他のスクリプトを調べたり、自分のスクリプトを投稿したい場合は、[Tabular Editor Scripts repository](https://github.com/TabularEditor/Scripts) に行ってください。

***

## カラムからメジャーを作成する

```csharp
// Creates a SUM measure for every currently selected column and hide the column.
foreach(var c in Selected.Columns)
{
    var newMeasure = c.Table.AddMeasure(
        "Sum of " + c.Name,                    // Name
        "SUM(" + c.DaxObjectFullName + ")",    // DAX expression
        c.DisplayFolder                        // Display Folder
    );
    
    // Set the format string on the new measure:
    newMeasure.FormatString = "0.00";

    // Provide some documentation:
    newMeasure.Description = "This measure is the sum of column " + c.DaxObjectFullName;

    // Hide the base column:
    c.IsHidden = true;
}
```

このスニペットでは、`<Table>.AddMeasure(<name>, <expression>, <displayFolder>)` 関数を使用して、テーブル上に新しいメジャーを作成します。DAX 式で使用する列の完全修飾名を取得するために、`DaxObjectFullName` プロパティを使用しています: `'TableName'[ColumnName]`.

***

## タイムインテリジェンスメジャーの生成

まず、個々のTime Intelligence集計のためのカスタムアクションを作成します。たとえば、次のようになります。

```csharp
// Creates a TOTALYTD measure for every selected measure.
foreach(var m in Selected.Measures) {
    m.Table.AddMeasure(
        m.Name + " YTD",                                       // Name
        "TOTALYTD(" + m.DaxObjectName + ", 'Date'[Date])",     // DAX expression
        m.DisplayFolder                                        // Display Folder
    );
}
```

ここでは、`DaxObjectName` プロパティを使用して、DAX式で使用する非限定的な参照を生成します。これを、メジャーに適用する "Time IntelligenceCreate YTD measure" という名前のカスタム・アクションとして保存します。MTD、LY、およびその他必要なものに対して同様のアクションを作成します。次に、新しいアクションとして以下を作成します。

```csharp
// Invoke all Time Intelligence Custom Actions:
CustomAction(@"Time Intelligence\Create YTD measure");
CustomAction(@"Time Intelligence\Create MTD measure");
CustomAction(@"Time Intelligence\Create LY measure");
```

これは、1つ（または複数）のカスタムアクションを別のアクション内から実行する方法を示しています（循環参照に注意 - Tabular Editorがクラッシュする原因になります）。これを新しいカスタムアクション「Time Intelligence All of the above」として保存すると、1回のクリックですべてのTime Intelligenceメジャーを簡単に生成できるようになります。

![image](https://user-images.githubusercontent.com/8976200/36632257-5565c8ca-197c-11e8-8498-82667b6e1049.png)

もちろん、以下のようにタイムインテリジェンスの計算をすべて1つのスクリプトにまとめてもよい。

```csharp
var dateColumn = "'Date'[Date]";

// Creates time intelligence measures for every selected measure:
foreach(var m in Selected.Measures) {
    // Year-to-date:
    m.Table.AddMeasure(
        m.Name + " YTD",                                       // Name
        "TOTALYTD(" + m.DaxObjectName + ", " + dateColumn + ")",     // DAX expression
        m.DisplayFolder                                        // Display Folder
    );
    
    // Previous year:
    m.Table.AddMeasure(
        m.Name + " PY",                                       // Name
        "CALCULATE(" + m.DaxObjectName + ", SAMEPERIODLASTYEAR(" + dateColumn + "))",     // DAX expression
        m.DisplayFolder                                        // Display Folder
    );    
    
    // Year-over-year
    m.Table.AddMeasure(
        m.Name + " YoY",                                       // Name
        m.DaxObjectName + " - [" + m.Name + " PY]",            // DAX expression
        m.DisplayFolder                                        // Display Folder
    );
    
    // Year-over-year %:
    m.Table.AddMeasure(
        m.Name + " YoY%",                                       // Name
        "DIVIDE([" + m.Name + " YoY], [" + m.Name + " PY])",    // DAX expression
        m.DisplayFolder                                         // Display Folder
    ).FormatString = "0.0 %";                                   // Set format string as percentage
    
    // Quarter-to-date:
    m.Table.AddMeasure(
        m.Name + " QTD",                                            // Name
        "TOTALQTD(" + m.DaxObjectName + ", " + dateColumn + ")",    // DAX expression
        m.DisplayFolder                                             // Display Folder
    );
    
    // Month-to-date:
    m.Table.AddMeasure(
        m.Name + " MTD",                                       // Name
        "TOTALMTD(" + m.DaxObjectName + ", " + dateColumn + ")",     // DAX expression
        m.DisplayFolder                                        // Display Folder
    );
}
```

### 追加プロパティを含む

新しく作成されたメジャーに追加のプロパティを設定したい場合は、上記のスクリプトを次のように修正します。

```csharp
// Creates a TOTALYTD measure for every selected measure.
foreach(var m in Selected.Measures) {
    var newMeasure = m.Table.AddMeasure(
        m.Name + " YTD",                                       // Name
        "TOTALYTD(" + m.DaxObjectName + ", 'Date'[Date])",     // DAX expression
        m.DisplayFolder                                        // Display Folder
    );
    newMeasure.FormatString = m.FormatString;               // Copy format string from original measure
    foreach(var c in Model.Cultures) {
        newMeasure.TranslatedNames[c] = m.TranslatedNames[c] + " YTD"; // Copy translated names for every culture
        newMeasure.TranslatedDisplayFolders[c] = m.TranslatedDisplayFolders[c]; // Copy translated display folders
    }
}
```

***

## デフォルトの翻訳を設定する

すべての（目に見える）オブジェクトにデフォルトの翻訳を適用しておくと便利な場合があります。この場合、デフォルトの翻訳は、オブジェクトのオリジナルの名前/説明/表示フォルダだけです。この利点は、JSON 形式で翻訳をエクスポートするときに、すべての翻訳オブジェクトを含めることができることです。

以下のスクリプトは、モデル内のすべてのカルチャをループし、まだ翻訳がないすべての可視オブジェクトに対して、デフォルト値を割り当てます。

```csharp
// Apply default translations to all (visible) translatable objects, across all cultures in the model:
foreach(var culture in Model.Cultures)
{
    ApplyDefaultTranslation(Model, culture);
    foreach(var perspective in Model.Perspectives)
        ApplyDefaultTranslation(perspective, culture);
    foreach(var table in Model.Tables.Where(t => t.IsVisible))
        ApplyDefaultTranslation(table, culture);
    foreach(var measure in Model.AllMeasures.Where(m => m.IsVisible))
        ApplyDefaultTranslation(measure, culture);
    foreach(var column in Model.AllColumns.Where(c => c.IsVisible))
        ApplyDefaultTranslation(column, culture);
    foreach(var hierarchy in Model.AllHierarchies.Where(h => h.IsVisible))
        ApplyDefaultTranslation(hierarchy, culture);
    foreach(var level in Model.AllLevels.Where(l => l.Hierarchy.IsVisible))
        ApplyDefaultTranslation(level, culture);
}

void ApplyDefaultTranslation(ITranslatableObject obj, Culture culture)
{
    // Only apply the default translation when a translation does not already exist:
    if(string.IsNullOrEmpty(obj.TranslatedNames[culture]))
    {
        // Default name translation:
        obj.TranslatedNames[culture] = obj.Name;

        // Default description translation:
        var dObj = obj as IDescriptionObject;
        if(dObj != null && string.IsNullOrEmpty(obj.TranslatedDescriptions[culture])
            && !string.IsNullOrEmpty(dObj.Description))
        {
            obj.TranslatedDescriptions[culture] = dObj.Description;
        }

        // Default display folder translation:
        var fObj = obj as IFolderObject;
        if(fObj != null && string.IsNullOrEmpty(fObj.TranslatedDisplayFolders[culture])
            && !string.IsNullOrEmpty(fObj.DisplayFolder))
        {
            fObj.TranslatedDisplayFolders[culture] = fObj.DisplayFolder;
        }
    }
}
```

***

## ハンドリング・パースペクティブ

このプロパティは、モデル内のすべてのパースペクティブに対してTrue/False値を保持し、指定されたオブジェクトがそのパースペクティブのメンバーであるかどうかを示します。

```csharp
foreach(var measure in Selected.Measures)
{
    measure.InPerspective["Inventory"] = true;
    measure.InPerspective["Reseller Operation"] = false;
}
```

上記のスクリプトでは、選択されたすべてのメジャーが「インベントリ」パースペクティブで表示され、「リセラー業務」パースペクティブで非表示になるようにします。

個々のパースペクティブでのメンバーシップの取得/設定に加えて、`InPerspective` プロパティは以下のメソッドもサポートします。

* `<<object>>.InPerspective.None()` - すべてのパースペクティブからオブジェクトを削除します。
* `<<object>>.InPerspective.All()` - すべてのパースペクティブにオブジェクトを含めます。
* `<<object>>.CopyFrom(string[] perspectives)` - 指定したすべてのパースペクティブ (パースペクティブの名前を含む文字列の配列) にオブジェクトを含めます。
* `<<object>>.CopyFrom(perspectiveIndexer perspectives)` - 別の `InPerspective` プロパティからパースペクティブインクルージョンをコピーします。

後者は、あるオブジェクトから別のオブジェクトにパースペクティブ・メンバシップをコピーするために使用されます。たとえば、ベース・メジャー["Reseller Sales"]があり、現在選択されているすべてのメジャーがこのベース・メジャーと同じパースペクティブに表示されるようにする必要があるとします。以下のスクリプトを実行します。

```csharp
var baseMeasure = Model.Tables["Reseller Sales"].Measures["Reseller Total Sales"];

foreach(var measure in Selected.Measures)
{
    /* Uncomment the line below, if you want 'measure' to be hidden
       from perspectives that 'baseMeasure' is hidden in: */
    // measure.InPerspective.None();

    measure.InPerspective.CopyFrom(baseMeasure.InPerspective);
}
```

この手法は、コードから新しいオブジェクトを生成する場合にも使用できます。たとえば、自動生成されたタイム・インテリジェンス・メジャーが、そのベース・メジャーと同じパースペクティブにのみ表示されるようにしたい場合、前のセクションのスクリプトを以下のように拡張します。

```csharp
// Creates a TOTALYTD measure for every selected measure.
foreach(var m in Selected.Measures) {
    var newMeasure = m.Table.AddMeasure(
        m.Name + " YTD",                                       // Name
        "TOTALYTD(" + m.DaxObjectName + ", 'Date'[Date])",     // DAX expression
        m.DisplayFolder                                        // Display Folder
    );
    newMeasure.InPerspective.CopyFrom(m.InPerspective);        // Apply perspectives from the base measure
}
```

***

## オブジェクトのプロパティをファイルに書き出す

ワークフローによっては、Excelを使って複数のオブジェクトプロパティを一括して編集することがあります。次のスニペットを使って、プロパティの標準的なセットを.TSVファイルにエクスポートし、その後、インポートできます（下記を参照）。

```csharp
// Export properties for the currently selected objects:
var tsv = ExportProperties(Selected);
SaveFile("Exported Properties 1.tsv", tsv);
```

でき上がった.TSVファイルをExcelで開くと、このようになります。

![image](https://user-images.githubusercontent.com/8976200/36632472-e8e96ef6-197e-11e8-8285-6816b09ad036.png)

最初の列の内容（Object）は、オブジェクトへの参照です。この列の内容が変更されると、その後のプロパティのインポートが正しく行われない場合があります。オブジェクトの名前を変更する場合は、2列目の値（Name）だけを変更します。

デフォルトでは、ファイルは TabularEditor.exe が置かれているのと同じフォルダーに保存されます。デフォルトでは、以下のプロパティのみがエクスポートされます（エクスポートされるオブジェクトの種類によって、該当するものがあります）。

* Name
* Description
* SourceColumn
* Expression
* FormatString
* DataType

異なるプロパティをエクスポートするには、`ExportProperties`の2番目の引数として、エクスポートするプロパティ名をカンマで区切ったリストを指定します。

```csharp
// Export the names and Detail Rows Expressions for all measures on the currently selected table:
var tsv = ExportProperties(Selected.Table.Measures, "Name,DetailRowsExpression");
SaveFile("Exported Properties 2.tsv", tsv);
```

利用可能なプロパティ名は [TOM API ドキュメント](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.aspx) で見ることができます。これらは、CamelCaseのTabular Editorのプロパティグリッドに表示される名前とほとんど同じで、スペースが取り除かれています（いくつかの例外を除いて、例えば、"Hidden "プロパティはTOM APIでは `IsHidden` と呼ばれています）。

プロパティをインポートするには、以下のスニペットを使用します。

```csharp
// 指定されたファイルのプロパティをインポートして適用する。
var tsv = ReadFile("Exported Properties 1.tsv");
ImportProperties(tsv);
```

### インデックス付きプロパティのエクスポート

Tabular Editor 2.11.0から、`ExportProperties` と `ImportProperties` メソッドがインデックス付きプロパティに対応しました。インデックス付きプロパティとは、プロパティ名に加え、キーを取るプロパティです。一例として、`myMeasure.TranslatedNames`があります。このプロパティは `myMeasure` の名前の翻訳として適用されるすべての文字列のコレクションを表します。C# では、インデックス演算子を使用して、特定のカルチャーの翻訳されたキャプションにアクセスできます。

長くなりましたが、Tabularモデル内のオブジェクトの翻訳、パースペクティブ情報、アノテーション、拡張プロパティ、行レベルおよびオブジェクトレベルのセキュリティ情報をすべてエクスポートできるようになりました。

たとえば、次のスクリプトは、すべてのモデル・メジャーと、それぞれがどのパースペクティブで表示されるかについての情報を含むTSVファイルを作成します。

```csharp
var tsv = ExportProperties(Model.AllMeasures, "Name,InPerspective");
SaveFile(@"c:\Project\MeasurePerspectives.tsv", tsv);
```

TSVファイルをExcelで開くと、このようになります。

![image](https://user-images.githubusercontent.com/8976200/85208532-956dec80-b331-11ea-8568-32dbd4cc5516.png)

そして、上に示したようにExcelで変更を行い、保存を押して、更新された値を `ImportProperties` を使ってTabular Editorにロードし直すことができます。

もし、特定のパースペクティブのみをリストアップしたい場合は、`ExportProperties`の呼び出しの第2引数でそれらを指定できます。

```csharp
var tsv = ExportProperties(Model.AllMeasures, "Name,InPerspective[Inventory]");
SaveFile(@"c:\Project\MeasurePerspectiveInventory.tsv", tsv);
```

同様に、翻訳、注釈などについても同様です。たとえば、テーブル、カラム、階層、レベル、メジャーに適用されたデンマーク語の翻訳をすべて確認したい場合。

```csharp
// Construct a list of objects:
var objects = new List<TabularNamedObject>();
objects.AddRange(Model.Tables);
objects.AddRange(Model.AllColumns);
objects.AddRange(Model.AllHierarchies);
objects.AddRange(Model.AllLevels);
objects.AddRange(Model.AllMeasures);

var tsv = ExportProperties(objects, "Name,TranslatedNames[da-DK],TranslatedDescriptions[da-DK],TranslatedDisplayFolders[da-DK]");
SaveFile(@"c:\Project\ObjectTranslations.tsv", tsv);
```

***

## ドキュメントの作成

上記の `ExportProperties` メソッドは、モデルのすべてまたは一部をドキュメント化する場合にも使用できます。以下のスニペットは、タブラーモデルのすべての可視メジャーまたは列からプロパティのセットを抽出し、それをTSVファイルとして保存します。

```csharp
// Construct a list of all visible columns and measures:
var objects = Model.AllMeasures.Where(m => !m.IsHidden && !m.Table.IsHidden).Cast<ITabularNamedObject>()
      .Concat(Model.AllColumns.Where(c => !c.IsHidden && !c.Table.IsHidden));

// Get their properties in TSV format (tabulator-separated):
var tsv = ExportProperties(objects,"Name,ObjectType,Parent,Description,FormatString,DataType,Expression");

// (Optional) Output to screen (can then be copy-pasted into Excel):
// tsv.Output();

// ...or save the TSV to a file:
SaveFile("documentation.tsv", tsv);
```

***

## ファイルからメジャーを生成する

上記のプロパティのエクスポート/インポートの手法は、モデル内の *既存の* オブジェクトのオブジェクト・プロパティを一括して編集する場合に便利です。一方、まだ存在しないメジャーのリストをインポートする場合はどうでしょうか。

既存のタブラー・モデルにインポートするメジャーの名前、説明、およびDAX式を含むTSV (タブ区切りの値）ファイルがあるとします。以下のスクリプトを使用して、ファイルを読み込み、それを行と列に分割し、メジャーを生成できます。また、このスクリプトでは各メジャーに特別なアノテーションが割り当てられ、同じスクリプトを使用して以前に作成されたメジャーを削除できます。

```csharp
var targetTable = Model.Tables["Program"];  // Name of the table that should hold the measures
var measureMetadata = ReadFile(@"c:\Test\MyMeasures.tsv");   // c:\Test\MyMeasures.tsv is a tab-separated file with a header row and 3 columns: Name, Description, Expression

// Delete all measures from the target table that have an "AUTOGEN" annotation with the value "1":
foreach(var m in targetTable.Measures.Where(m => m.GetAnnotation("AUTOGEN") == "1").ToList())
{
    m.Delete();
}

// Split the file into rows by CR and LF characters:
var tsvRows = measureMetadata.Split(new[] {'\r','\n'},StringSplitOptions.RemoveEmptyEntries);

// Loop through all rows but skip the first one:
foreach(var row in tsvRows.Skip(1))
{
    var tsvColumns = row.Split('\t');     // Assume file uses tabs as column separator
    var name = tsvColumns[0];             // 1st column contains measure name
    var description = tsvColumns[1];      // 2nd column contains measure description
    var expression = tsvColumns[2];       // 3rd column contains measure expression

    // This assumes that the model does not already contain a measure with the same name (if it does, the new measure will get a numeric suffix):
    var measure = targetTable.AddMeasure(name);
    measure.Description = description;
    measure.Expression = expression;
    measure.SetAnnotation("AUTOGEN", "1");  // Set a special annotation on the measure, so we can find it and delete it the next time the script is executed.
}
```

この処理を自動化する必要がある場合は、上記のスクリプトをファイルに保存し、以下のように[Tabular Editor CLI](/Command-line-Options) を使用してください。

```
start /wait TabularEditor.exe "<path to bim file>" -S "<path to script file>" -B "<path to modified bim file>"
```

例えば

```
start /wait TabularEditor.exe "c:\Projects\AdventureWorks\Model.bim" -S "c:\Projects\AutogenMeasures.cs" -B "c:\Projects\AdventureWorks\Build\Model.bim"
```

...または、すでにデプロイされたデータベースに対してスクリプトを実行したい場合。

```
start /wait TabularEditor.exe "localhost" "AdventureWorks" -S "c:\Projects\AutogenMeasures.cs" -D "localhost" "AdventureWorks" -O
```

***

## パーティションソースのメタデータからデータカラムを作成する

**注：** バージョン2.7.2またはそれ以降を使用している場合は、新しい "テーブルのインポート" 機能を必ず試してください。

テーブルがOLE DBプロバイダーデータソースに基づくQueryパーティションを使用している場合、以下のスニペットを実行することにより、そのテーブルの列メタデータを自動的にリフレッシュできます。

```csharp
Model.Tables["Reseller Sales"].RefreshDataColumns();
```

これは、モデルに新しいテーブルを追加するときに、テーブル上のすべてのデータ・カラムを手動で作成することを避けるために便利です。上記のスニペットは、'Reseller Sales' テーブルのパーティションソースの既存の接続文字列を使用して、パーティションソースがローカルにアクセスできることを想定しています。上記のスニペットは、パーティション・クエリからスキーマを抽出し、ソース・クエリ内の各カラムに対してテーブルにデータ・カラムを追加します。

この操作に別の接続文字列を指定する必要がある場合は、このスニペットで指定できます。

```csharp
var source = Model.DataSources["DWH"] as ProviderDataSource;
var oldConnectionString = source.ConnectionString;
source.ConnectionString = "...";   // Enter the connection string you want to use for metadata refresh
Model.Tables["Reseller Sales"].RefreshDataColumns();
source.ConnectionString = oldConnectionString;
```

これは、'Reseller Sales' テーブルのパーティションが "DWH" という名前のプロバイダデータソースを使用していると仮定している。

***

## DAX式のフォーマット

詳しくは、[FormatDax](/FormatDax)をご覧ください。

```csharp
// Works in Tabular Editor version 2.13.0 or newer:
Selected.Measures.FormatDax();
```

代替構文。

```csharp
// Works in Tabular Editor version 2.13.0 or newer:
foreach(var m in Selected.Measures)
    m.FormatDax();
```

***

## テーブルのソースカラムのリストを生成する

次のスクリプトは、現在選択されているテーブルのソースカラムのリストをきれいにフォーマットして出力します。これは、`SELECT *` を使用するパーティションクエリを明示的なカラムで置き換えたい場合に便利です。

```csharp
string.Join(",\r\n", 
    Selected.Table.DataColumns
        .OrderBy(c => c.SourceColumn)
        .Select(c => "[" + c.SourceColumn + "]")
    ).Output();
```

***

## リレーションの自動生成

チーム内で特定の命名規則を一貫して使用している場合、スクリプトを使用するとさらに強力な効果を得られることがすぐにわかります。

次のスクリプトを1つ以上のファクト・テーブルで実行すると、列名に基づいてすべての関連するディメンジョン・テーブルへのリレーションシップが自動的に作成されます。このスクリプトは、名前パターン `xxxyyyKey` を持つファクト・テーブル列を検索します。ここで xxx はロールプレイで使用するためのオプションの修飾子で、yyyはディメンジョン・テーブル名です。ディメンジョン・テーブルには、`yyyKey` という名前の列が存在し、ファクト・テーブルの列と同じデータ型である必要があります。たとえば、"ProductKey" という名前の列は、Productテーブルの "ProductKey "列と関連付けられます。Key" の代わりに使用する別の列名サフィックスを指定できます。

ファクト・テーブルとディメンジョン・テーブルの間にすでにリレーションシップが存在する場合、スクリプトは非アクティブとして新しいリレーションシップを作成します。

```csharp
var keySuffix = "Key";

// Loop through all currently selected tables (assumed to be fact tables):
foreach(var fact in Selected.Tables)
{
    // Loop through all SK columns on the current table:
    foreach(var factColumn in fact.Columns.Where(c => c.Name.EndsWith(keySuffix)))
    {
        // Find the dimension table corresponding to the current SK column:
        var dim = Model.Tables.FirstOrDefault(t => factColumn.Name.EndsWith(t.Name + keySuffix));
        if(dim != null)
        {
            // Find the key column on the dimension table:
            var dimColumn = dim.Columns.FirstOrDefault(c => factColumn.Name.EndsWith(c.Name));
            if(dimColumn != null)
            {
                // Check whether a relationship already exists between the two columns:
                if(!Model.Relationships.Any(r => r.FromColumn == factColumn && r.ToColumn == dimColumn))
                {
                    // If relationships already exists between the two tables, new relationships will be created as inactive:
                    var makeInactive = Model.Relationships.Any(r => r.FromTable == fact && r.ToTable == dim);

                    // Add the new relationship:
                    var rel = Model.AddRelationship();
                    rel.FromColumn = factColumn;
                    rel.ToColumn = dimColumn;
                    factColumn.IsHidden = true;
                    if(makeInactive) rel.IsActive = false;
                }
            }
        }
    }
}
```

***

## DumpFilters メジャーの作成

[この記事](https://www.sqlbi.com/articles/displaying-filter-context-in-power-bi-tooltips/)に触発されて、現在選択されているテーブルに対して[DumpFilters]メジャーを作成するスクリプトを紹介します。

```csharp
var dax = "VAR MaxFilters = 3 RETURN ";
var dumpFilterDax = @"IF (
    ISFILTERED ( {0} ), 
    VAR ___f = FILTERS ( {0} )
    VAR ___r = COUNTROWS ( ___f )
    VAR ___t = TOPN ( MaxFilters, ___f, {0} )
    VAR ___d = CONCATENATEX ( ___t, {0}, "", "" )
    VAR ___x = ""{0} = "" & ___d 
        & IF(___r > MaxFilters, "", ... ["" & ___r & "" items selected]"") & "" ""
    RETURN ___x & UNICHAR(13) & UNICHAR(10)
)";

// Loop through all columns of the model to construct the complete DAX expression:
bool first = true;
foreach(var column in Model.AllColumns)
{
    if(!first) dax += " & ";
    dax += string.Format(dumpFilterDax, column.DaxObjectFullName);
    if(first) first = false;
}

// Add the measure to the currently selected table:
Selected.Table.AddMeasure("DumpFilters", dax);
```

***

## キャメルケースからプロパーケースへ

リレーションデータベースのカラムとテーブルの一般的な命名規則は、キャメルケースです。つまり、名前にはスペースを含まず、個々の単語は大文字で始めます。Tabularモデルでは、テーブルやカラムは隠されることなくビジネスユーザーに見えるので、「より美しい」命名法を使用することが望ましい。次のスクリプトは、CamelCaseの名前をProper Caseに変換します。大文字の連続はそのままにする（頭文字をとる）。たとえば、このスクリプトは次のように変換する。

* `CustomerWorkZipcode` to `Customer Work Zipcode`
* `CustomerAccountID` to `Customer Account ID`
* `NSASecurityID` to `NSA Security ID`

このスクリプトは、すべてのオブジェクト タイプに適用されるカスタム アクションとして保存することを強くオススメします（Relationship、KPI、Table Permissions、Translationsは編集可能な "Name" プロパティがないため、これを除く）。

```csharp
foreach(var obj in Selected.OfType<ITabularNamedObject>()) {
    var oldName = obj.Name;
    var newName = new System.Text.StringBuilder();
    for(int i = 0; i < oldName.Length; i++) {
        // First letter should always be capitalized:
        if(i == 0) newName.Append(Char.ToUpper(oldName[i]));

        // A sequence of two uppercase letters followed by a lowercase letter should have a space inserted
        // after the first letter:
        else if(i + 2 < oldName.Length && char.IsLower(oldName[i + 2]) && char.IsUpper(oldName[i + 1]) && char.IsUpper(oldName[i]))
        {
            newName.Append(oldName[i]);
            newName.Append(" ");
        }

        // All other sequences of a lowercase letter followed by an uppercase letter, should have a space
        // inserted after the first letter:
        else if(i + 1 < oldName.Length && char.IsLower(oldName[i]) && char.IsUpper(oldName[i+1]))
        {
            newName.Append(oldName[i]);
            newName.Append(" ");
        }
        else
        {
            newName.Append(oldName[i]);
        }
    }
    obj.Name = newName.ToString();
}
```

***

## テーブルとメジャーの依存関係をエクスポートする

大規模で複雑なモデルがあり、基礎データの変更によって影響を受ける可能性があるメジャーを知りたいとします。

以下のスクリプトは、モデルのすべてのメジャーをループし、各メジャーに対して、そのメジャーが直接的および間接的に依存しているテーブルのリストを出力します。このリストは、Tab区切りのファイルとして出力されます。

```csharp
string tsv = "Measure\tDependsOnTable"; // TSV file header row

// Loop through all measures:
foreach(var m in Model.AllMeasures) {

    // Get a list of ALL objects referenced by this measure (both directly and indirectly through other measures):
    var allReferences = m.DependsOn.Deep();

    // Filter the previous list of references to table references only. For column references, let's get th
    // table that each column belongs to. Finally, keep only distinct tables:
    var allTableReferences = allReferences.OfType<Table>()
        .Concat(allReferences.OfType<Column>().Select(c => c.Table)).Distinct();

    // Output TSV rows - one for each table reference:
    foreach(var t in allTableReferences)
        tsv += string.Format("\r\n{0}\t{1}", m.Name, t.Name);
}
    
tsv.Output();   
// SaveFile("c:\\MyProjects\\SSAS\\MeasureTableDependencies.tsv", tsv); // Uncomment this line to save output to a file
```

***

## 集計の設定（Power BI Datasetのみ）

[Tabular Editor 2.11.3](https://github.com/otykier/TabularEditor/releases/tag/2.11.3) では、カラムに `AlternateOf` プロパティを設定できるようになり、モデル上で集計テーブルを定義することができるようになりました。この機能は、Power BI Service XMLAエンドポイントを通じて、Power BI Datasets （Compatibility Level 1460以上）で有効です。

列の範囲を選択し、以下のスクリプトを実行して、列の `AlternateOf` プロパティを開始させます。

```csharp
foreach(var col in Selected.Columns) col.AddAlternateOf();
```

カラムをひとつずつ調べて、ベースカラムに対応させ、それに応じた集計方法（Sum/Min/Max/GroupBy)を設定します。また、この作業を自動化したい場合、集計テーブルのカラムがベーステーブルのカラムと同じ名前であれば、以下のスクリプトを使用することで、カラムのマッピングを行うことができます。

```csharp
// ツリーで 2 つのテーブルを選択します (ctrl+click) 。集計テーブルは、カラム数が最も少ないテーブルと仮定する。 
// このスクリプトは、集計テーブルのすべてのカラムに AlternateOf プロパティを設定する。このスクリプトが動作するためには、集約テーブルのカラムはベーステーブルのカラムと同じ名前である必要があります。

var aggTable = Selected.Tables.OrderBy(t => t.Columns.Count).First();
var baseTable = Selected.Tables.OrderByDescending(t => t.Columns.Count).First();

foreach(var col in aggTable.Columns)
{
    // スクリプトは、列のデータ型が decimal/double でない限り、要約のタイプを "Group By" に設定する。    
    var summarization = SummarizationType.GroupBy;
    if(col.DataType == DataType.Double || col.DataType == DataType.Decimal)
        summarization = SummarizationType.Sum;
    
    col.AddAlternateOf(baseTable.Columns[col.Name], summarization);
}
```

スクリプトを実行すると、aggテーブルのすべてのカラムに `AlternateOf` プロパティが割り当てられます（以下のスクリーンショットを参照ください）。集約を行うには、ベースとなるテーブルパーティションでDirectQueryを使用しなければならないことに注意してください。

![image](https://user-images.githubusercontent.com/8976200/85851134-6ed70800-b7ae-11ea-82eb-37fcaa2ca9c4.png)

***

## アナリシスサービスのクエリ

バージョン[2.12.1](https://github.com/otykier/TabularEditor/releases/tag/2.12.1)より、Tabular Editorはモデルに対してDAXクエリーを実行したりDAX式を評価するためのヘルパーメソッドを多数提供するようになりました。これらのメソッドは、モデルメタデータがAnalysis Servicesのインスタンスから直接ロードされた場合、たとえば「ファイル > 開く > DBから」オプションを使用した場合、あるいはTabular EditorのPower BI外部ツール統合を使用した場合のみ動作します。

以下の方法があります。

| Method | Description |
| ------ | ----------- |
| `void ExecuteCommand(string tmslOrXmla, bool isXmla = false)` | このメソッドは、指定されたTMSLまたはXMLAスクリプトを、接続されているAnalysis Servicesのインスタンスに渡します。これは、ASインスタンス上のテーブルのデータをリフレッシュする場合に便利です。このメソッドを使用してモデルのメタデータを変更すると、ローカルモデルのメタデータがASインスタンスのメタデータと同期しなくなり、次にモデルのメタデータを保存しようとしたときにバージョンの衝突の警告が表示される可能性があることに注意してください。XMLAスクリプトを送信する場合は、`isXmla` パラメーターを `true` に設定してください。 |
| `IDataReader ExecuteReader(string dax)` | 接続中の AS データベースに対して、指定された DAX *クエリ* を実行し、結果の [AmoDataReader](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.amodatareader?view=analysisservices-dotnet) オブジェクトを返します。DAX クエリには、1 つ以上の [`EVALUATE`](https://dax.guide/EVALUATE) ステートメントが含まれます。一度に複数のデータリーダーを開くことはできないことに注意してください。万が一、明示的にリーダーを閉じたり処分したりするのを忘れた場合、Tabular Editorが自動的にそれらを閉じます。 |
| `DataSet ExecuteDax(string dax)` | 接続された AS データベースに対して指定された DAX *クエリ* を実行し、クエリから返されたデータを含む [DataSet](https://docs.microsoft.com/en-us/dotnet/api/system.data.dataset?view=netframework-4.6) オブジェクトを返します。DAXクエリは、1つ以上の[`EVALUATE`](https://dax.guide/EVALUATE)ステートメントを含んでいます。結果として得られる DataSet オブジェクトは、 `EVALUATE` ステートメントごとに 1 つの DataTable を含んでいます。非常に大きなデータテーブルを返すことは、メモリ不足などの安定性の問題を引き起こす可能性があるため、推奨されません。 |
| `object EvaluateDax(string dax)` | 接続中の AS データベースに対して指定された DAX *式* を実行し、その結果を表すオブジェクトを返します。DAX式がスカラーの場合、関連する型のオブジェクトが返されます（string、long、decimal、double、DateTime）。DAX式がテーブル値の場合、[DataTable](https://docs.microsoft.com/en-us/dotnet/api/system.data.datatable?view=netframework-4.6)が返されます。|

このメソッドは `Model.Database` オブジェクトにスコープされていますが、プレフィックスなしで直接実行することも可能です。

Darren Gosbellは `ExecuteDax` メソッドを使用してデータ駆動型のメジャーを生成する興味深いユースケースを紹介しています [こちら](https://darren.gosbell.com/2020/08/the-best-way-to-generate-data-driven-measures-in-power-bi-using-tabular-editor/)。

もう1つの方法は、テーブルを更新するための再利用可能なスクリプトを作成することです。たとえば、再計算を行うには、次のようにします。

```csharp
var type = "calculate";
var database = Model.Database.Name;
var table = Selected.Table.Name;
var tmsl = "{ \"refresh\": { \"type\": \"%type%\", \"objects\": [ { \"database\": \"%db%\", \"table\": \"%table%\" } ] } }"
    .Replace("%type%", type)
    .Replace("%db%", database)
    .Replace("%table%", table);

ExecuteCommand(tmsl);
```

### Analysis Services エンジンのキャッシュをクリアする

Tabular Editor 2.16.6またはTabular Editor3.2.3では、次の構文を使用して生のXMLAコマンドをAnalysis Servicesに送信できます。以下の例では、これを使用してASエンジン・キャッシュをクリアする方法を示しています。

```csharp
var clearCacheXmla = string.Format(@"<ClearCache xmlns=""http://schemas.microsoft.com/analysisservices/2003/engine"">  
  <Object>
    <DatabaseID>{0}</DatabaseID>
  </Object>
</ClearCache>", Model.Database.ID);

ExecuteCommand(clearCacheXmla, isXmla: true);
```

### クエリ結果の可視化

また、`Output`ヘルパーメソッドを使用すると、`EvaluateDax`から返されたDAX式の結果を直接視覚化できます。

```csharp
EvaluateDax("1 + 2").Output(); // An integer
EvaluateDax("\"Hello from AS\"").Output(); // A string
EvaluateDax("{ (1, 2, 3) }").Output(); // A table
```

![image](https://user-images.githubusercontent.com/8976200/91638299-bbd59580-ea0e-11ea-882b-55bff73c30fb.png)

...または、現在選択されているメジャーの値を返したい場合。

```csharp
EvaluateDax(Selected.Measure.DaxObjectFullName).Output();
```

![image](https://user-images.githubusercontent.com/8976200/91638367-6f3e8a00-ea0f-11ea-90cd-7d2e4cff6e31.png)

そして、より高度な例として、複数のメジャーを一度に選択し評価する方法をご紹介します。

```csharp
var dax = "ROW(" + string.Join(",", Selected.Measures.Select(m => "\"" + m.Name + "\", " + m.DaxObjectFullName).ToArray()) + ")";
EvaluateDax(dax).Output();
```

![image](https://user-images.githubusercontent.com/8976200/91638356-546c1580-ea0f-11ea-8302-3e40829e00dd.png)

本当に上級者であれば、SUMMARIZECOLUMNSやその他のDAX関数を使って、選択したメジャーをある列でスライスして視覚化できます。

```csharp
var dax = "SUMMARIZECOLUMNS('Product'[Color], " + string.Join(",", Selected.Measures.Select(m => "\"" + m.Name + "\", " + m.DaxObjectFullName).ToArray()) + ")";
EvaluateDax(dax).Output();
```

![image](https://user-images.githubusercontent.com/8976200/91638389-9b5a0b00-ea0f-11ea-819f-d3eee3ddfa71.png)

スクリプトエディターの上にある「+」アイコンをクリックすると、これらのスクリプトをカスタムアクションとして保存できます。このようにして、Tabular Editorのコンテキストメニューから直接実行したり視覚化したりできる、再利用しやすいDAXクエリのコレクションを手に入れることができます。

![image](https://user-images.githubusercontent.com/8976200/91638790-305e0380-ea12-11ea-9d84-313f4388496f.png)

### データの書き出し

以下のスクリプトを使用して、DAXクエリを評価し、その結果をファイルにストリームできます（スクリプトはタブ区切りのファイル形式を使用します）。

```csharp
using System.IO;

// This script evaluates a DAX query and writes the results to file using a tab-separated format:

var dax = "EVALUATE 'Customer'";
var file = @"c:\temp\file.csv";
var columnSeparator = "\t";

using(var daxReader = ExecuteReader(dax))
using(var fileWriter = new StreamWriter(file))
{
    // Write column headers:
    fileWriter.WriteLine(string.Join(columnSeparator, Enumerable.Range(0, daxReader.FieldCount - 1).Select(f => daxReader.GetName(f))));

    while(daxReader.Read())
    {
        var rowValues = new object[daxReader.FieldCount];
        daxReader.GetValues(rowValues);
        var row = string.Join(columnSeparator, rowValues.Select(v => v == null ? "" : v.ToString()));
        fileWriter.WriteLine(row);
    }
}
```

他にも面白い使い方を思いついたら、ぜひ [community scripts repository](https://github.com/TabularEditor/Scripts) で共有することを検討してみてください。ありがとうございました。

***

## Power Queryのサーバー名とデータベース名の置き換え

SQL ServerベースのデータソースからデータをインポートするPower BIデータセットには、しばしば次のようなM式が含まれます。Tabular Editorには残念ながらこのような式を「解析」するメカニズムはありませんが、この式のサーバー名とデータベース名を元の値を知らずに別のものに置き換えたい場合、値が二重引用符で囲まれているという事実を利用できます。

```M
let
    Source = Sql.Databases("devsql.database.windows.net"),
    AdventureWorksDW2017 = Source{[Name="AdventureWorks"]}[Data],
    dbo_DimProduct = AdventureWorksDW2017{[Schema="dbo",Item="DimProduct"]}[Data]
in
    dbo_DimProduct
```

次のスクリプトは、二重引用符で囲まれた値の最初の出現箇所をサーバー名で、二重引用符で囲まれた値の2番目の出現箇所をデータベース名で置き換えるものです。どちらの置換値も環境変数から読み込まれる。

```csharp
// This script is used to replace the server and database names across
// all power query partitions, with the ones provided through environment
// variables:
var server = "\"" + Environment.GetEnvironmentVariable("SQLServerName") + "\"";
var database = "\"" + Environment.GetEnvironmentVariable("SQLDatabaseName") + "\"";

// This function will extract all quoted values from the M expression, returning a list of strings
// with the values extracted (in order), but ignoring any quoted values where a hashtag (#) precedes
// the quotation mark:
var split = new Func<string, List<string>>(m => { 
    var result = new List<string>();
    var i = 0;
    foreach(var s in m.Split('"')) {
        if(s.EndsWith("#") && i % 2 == 0) i = -2;
        if(i >= 0 && i % 2 == 1) result.Add(s);
        i++;
    }
    return result;
});
var GetServer = new Func<string, string>(m => split(m)[0]);    // Server name is usually the 1st encountered string
var GetDatabase = new Func<string, string>(m => split(m)[1]);  // Database name is usually the 2nd encountered string

// Loop through all partitions on the model, replacing the server and database names from the partitions
// with the ones specified in environment variables:
foreach(var p in Model.AllPartitions.OfType<MPartition>())
{
    var oldServer = "\"" + GetServer(p.Expression) + "\"";
    var oldDatabase = "\"" + GetDatabase(p.Expression) + "\"";
    p.Expression = p.Expression.Replace(oldServer, server).Replace(oldDatabase, database);
}
```

***

## Power QueryのデータソースとパーティションをLegacyに置き換える

SQL Serverベースのデータソースに対してパーティションにPower Query（M）式を使用するPower BIベースのモデルを使用している場合、残念ながらTabular Editorのデータインポートウィザードの使用やスキーマチェック（インポートしたカラムとデータソースのカラムの比較など）の実行ができなくなります。

この問題を解決するには、モデル上で以下のスクリプトを実行し、パワークエリパーティションを対応するネイティブSQLクエリパーティションに置き換え、モデル上にレガシー（プロバイダー）データソースを作成してTabular Editorのデータインポートウィザードで機能させることが可能です。

このスクリプトには2つのバージョンがあります。最初のものは、作成されたレガシーデータソース用のMSOLEDBSQLプロバイダーと、ハードコードされたクレデンシャルを使用します。これはローカルで開発する場合に便利です。2つ目は、Azure DevOps上のMicrosoftがホストするビルドエージェントで利用できるSQLNCLIプロバイダーを使用し、環境変数から資格情報とサーバー/データベース名を読み取るもので、Azure Pipeliensへの統合に便利なスクリプトとなっています。

Mパーティションから接続情報を読み込み、Azure ADを通じてユーザー名とパスワードの入力を促すMSOLEDBSQL版。

```csharp
#r "Microsoft.VisualBasic"

// This script replaces all Power Query partitions on this model with a
// legacy partition using the provided connection string with INTERACTIVE
// AAD authentication. The script assumes that all Power Query partitions
// load data from the same SQL Server-based data source.

// Provide the following information:
var authMode = "ActiveDirectoryInteractive";
var userId = Microsoft.VisualBasic.Interaction.InputBox("Type your AAD user name", "User name", "name@domain.com", 0, 0);
if(userId == "") return;
var password = ""; // Leave blank when using ActiveDirectoryInteractive authentication

// This function will extract all quoted values from the M expression, returning a list of strings
// with the values extracted (in order), but ignoring any quoted values where a hashtag (#) precedes
// the quotation mark:
var split = new Func<string, List<string>>(m => { 
    var result = new List<string>();
    var i = 0;
    foreach(var s in m.Split('"')) {
        if(s.EndsWith("#") && i % 2 == 0) i = -2;
        if(i >= 0 && i % 2 == 1) result.Add(s);
        i++;
    }
    return result;
});
var GetServer = new Func<string, string>(m => split(m)[0]);    // Server name is usually the 1st encountered string
var GetDatabase = new Func<string, string>(m => split(m)[1]);  // Database name is usually the 2nd encountered string
var GetSchema = new Func<string, string>(m => split(m)[2]);    // Schema name is usually the 3rd encountered string
var GetTable = new Func<string, string>(m => split(m)[3]);     // Table name is usually the 4th encountered string

var server = GetServer(Model.AllPartitions.OfType<MPartition>().First().Expression);
var database = GetDatabase(Model.AllPartitions.OfType<MPartition>().First().Expression);

// Add a legacy data source to the model:
var ds = Model.AddDataSource("AzureSQL");
ds.Provider = "System.Data.OleDb";
ds.ConnectionString = string.Format(
    "Provider=MSOLEDBSQL;Data Source={0};Initial Catalog={1};Authentication={2};User ID={3};Password={4}",
    server,
    database,
    authMode,
    userId,
    password);

// Remove Power Query partitions from all tables and replace them with a single Legacy partition:
foreach(var t in Model.Tables.Where(t => t.Partitions.OfType<MPartition>().Any()))
{
    var mPartitions = t.Partitions.OfType<MPartition>();
    if(!mPartitions.Any()) continue;
    var schema = GetSchema(mPartitions.First().Expression);
    var table = GetTable(mPartitions.First().Expression);
    t.AddPartition(t.Name, string.Format("SELECT * FROM [{0}].[{1}]", schema, table));
    foreach(var p in mPartitions.ToList()) p.Delete();
}
```

環境変数から接続情報を読み取るSQLNCLIバージョン。

```csharp
// このスクリプトは、このモデル上のすべてのPower Queryパーティションをレガシーパーティションに置き換え、SQLサーバー名、データベース名、ユーザー名、パスワードを対応する環境変数から読み込みます。このスクリプトは、すべての Power Query パーティションが同じ SQL Server ベースのデータソースからデータをロードすることを想定しています。

var server = Environment.GetEnvironmentVariable("SQLServerName");
var database = Environment.GetEnvironmentVariable("SQLDatabaseName");
var userId = Environment.GetEnvironmentVariable("SQLUserName");
var password = Environment.GetEnvironmentVariable("SQLUserPassword");

// This function will extract all quoted values from the M expression, returning a list of strings
// with the values extracted (in order), but ignoring any quoted values where a hashtag (#) precedes
// the quotation mark:
var split = new Func<string, List<string>>(m => { 
    var result = new List<string>();
    var i = 0;
    foreach(var s in m.Split('"')) {
        if(s.EndsWith("#") && i % 2 == 0) i = -2;
        if(i >= 0 && i % 2 == 1) result.Add(s);
        i++;
    }
    return result;
});
var GetServer = new Func<string, string>(m => split(m)[0]);    // Server name is usually the 1st encountered string
var GetDatabase = new Func<string, string>(m => split(m)[1]);  // Database name is usually the 2nd encountered string
var GetSchema = new Func<string, string>(m => split(m)[2]);    // Schema name is usually the 3rd encountered string
var GetTable = new Func<string, string>(m => split(m)[3]);     // Table name is usually the 4th encountered string

// Add a legacy data source to the model:
var ds = Model.AddDataSource("AzureSQL");
ds.Provider = "System.Data.SqlClient";
ds.ConnectionString = string.Format(
    "Server={0};Initial Catalog={1};Persist Security Info=False;User ID={2};Password={3}",
    server,
    database,
    userId,
    password);

// Remove Power Query partitions from all tables and replace them with a single Legacy partition:
foreach(var t in Model.Tables.Where(t => t.Partitions.OfType<MPartition>().Any()))
{
    var mPartitions = t.Partitions.OfType<MPartition>();
    if(!mPartitions.Any()) continue;
    var schema = GetSchema(mPartitions.First().Expression);
    var table = GetTable(mPartitions.First().Expression);
    t.AddPartition(t.Name, string.Format("SELECT * FROM [{0}].[{1}]", schema, table));
    foreach(var p in mPartitions.ToList()) p.Delete();
}
```
