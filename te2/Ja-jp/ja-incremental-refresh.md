# 増分更新

Power BI Serviceでホストされているデータセットでは、1つ以上のテーブルで [Incremental Refresh](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview) を設定できます。Power BIデータセットでIncremental Refreshを設定・変更するには、[Power BIサービスのXMLAエンドポイントを直接使用する](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla)か、後述のようにXMLAエンドポイントに接続したTabular Editorを使用することが可能です。

## Tabular Editorでゼロから増分更新を設定する

1. ワークスペースのPower BI XMLA R/Wエンドポイントに接続し、増分更新を設定するデータセットを開きます。
2. 増分更新には `RangeStart` と `RangeEnd` パラメーターを作成する必要があります ([追加情報](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-configure#create-parameters)) ので、まずTabular Editorで新しいShared Expressionsを2つ追加してみましょう。
  ![Add shared expressions](https://user-images.githubusercontent.com/8976200/121341006-8906e900-c920-11eb-97af-ee683ff40609.png)
3. それぞれ `RangeStart` と `RangeEnd` という名前を付け、`Kind` プロパティを "M" に設定し、式を以下のように設定します（実際に指定する日時の値は、データ更新の開始時にPBIサービスによって設定されるため、重要ではありません）。

  ```M
  #datetime(2021, 6, 9, 0, 0, 0) meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]
  ```

  ![Set kind property](https://user-images.githubusercontent.com/8976200/121342389-dc2d6b80-c921-11eb-8848-b67950e55e36.png)

4. 次に、増分更新を有効にするテーブルを選択します。
5. テーブルの`EnableRefreshPolicy`プロパティを "true "に設定します。
  ![Enable Refresh Policy](https://user-images.githubusercontent.com/8976200/121339872-3842c080-c91f-11eb-8e63-a051b34fb36f.png)
6. 残りのプロパティは、必要なインクリメンタルリフレッシュポリシーにしたがって設定します。`SourceExpression` プロパティにM式を指定することを忘れないでください (これは、増分更新ポリシーによって作成されるパーティションに追加される式です。ソースのデータをフィルターするために `RangeStart` と `RangeEnd` パラメーターを使用する必要があります)。データ重複をする可能性があるため、= 演算子は`RangeStart`または`RangeEnd`のいずれかにのみ適用し、両方には適用しないでください。
  ![Configure Properties](https://user-images.githubusercontent.com/45298358/170603450-8232ad55-0b4a-4ead-b113-786a781f94ad.png)
7. モデルの保存 (Ctrl+S).
8. テーブルを右クリックし"Apply Refresh Policy"を選択します。
  ![Apply Refresh Policy](https://user-images.githubusercontent.com/8976200/121342947-78577280-c922-11eb-82b5-a517fbe86c3e.png)

これで完了です。この時点で、Power BI Serviceが、指定したポリシーに基づいてテーブルのパーティションを自動的に生成していることが確認できるはずです。

![Generated Partitions](https://user-images.githubusercontent.com/8976200/121343417-eef47000-c922-11eb-8731-1ac4dde916ef.png)

次に、パーティション内のデータのリフレッシュを行います。これにはPower BIのサービスを利用することもできますし、[SQL Server Management StudioによるXMLA/TMSL](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla#refresh-management-with-sql-server-management-studio-ssms)や、[Tabular Editorのスクリプト](https://www.elegantbi.com/post/datarefreshintabulareditor)を使ってパーティションを一括でリフレッシュすることも可能です。

## Modifying existing refresh policies

Power BI Desktopで設定した既存のリフレッシュポリシーをTabular Editorで変更することもできます。この場合は、上記のステップ6-8を実行するだけです。

## Applying refresh policies with `EffectiveDate`

現在の日付を上書きしながらパーティションを生成したい場合（異なるローリングウィンドウ範囲を生成する目的で）、Tabular Editorの小さなスクリプトを使用して、[EffectiveDate](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#optional-parameters) パラメーターでリフレッシュポリシーを適用できます。

増分更新テーブルを選択した状態で、上記のステップ8の代わりに、Tabular Editorの「アドバンススクリプト」ペインで以下のスクリプトを実行します。

```csharp
var effectiveDate = new DateTime(2020, 1, 1);  // Todo: replace with your effective date
Selected.Table.ApplyRefreshPolicy(effectiveDate);
```

![Use scripts to apply refresh policy](https://user-images.githubusercontent.com/8976200/121344362-f9633980-c923-11eb-916c-44a35cf03a36.png)
