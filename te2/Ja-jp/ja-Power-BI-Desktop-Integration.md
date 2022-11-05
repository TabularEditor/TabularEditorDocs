# Power BI Desktop Integration

2020年7月現在、[Power BI Desktop は External Tools のサポートを追加します](https://docs.microsoft.com/da-dk/power-bi/create-reports/desktop-external-tools)。これにより、DesktopでImportedまたはDirectQueryデータを扱う際に、Tabular Editorで特定のモデリング操作を実行できるようになります。

![image](https://user-images.githubusercontent.com/8976200/87296924-dcea3180-c507-11ea-9cf9-2f647d26a2a9.png)

## Prerequisites

- 2020年7月版[Power BI Desktop](https://www.microsoft.com/en-us/download/details.aspx?id=58494) (またはそれ以降）
- [最新版 Tabular Editor](https://github.com/otykier/TabularEditor/releases/latest)
- Power BI Desktopのプレビュー機能で [Enhanced Metadata](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-enhanced-dataset-metadata) を有効化する。

また、[automatic date/time](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-auto-date-time) は **disabled** にすることを強く推奨します（Power BI Desktopの「データ読み込み」での設定）。

## Supported Modeling Operations

デフォルトでは、Power BI Desktopモデルに接続すると、Tabular Editorは限られた数のオブジェクトとプロパティしか編集できなくなります。これらは以下の通りです。

- メジャー（任意のプロパティの追加・削除・編集）
- 計算グループと計算項目（任意のプロパティの追加/削除/編集）
- パースペクティブ（任意のプロパティの追加・削除・編集）
- 翻訳（追加・削除）
  - メタデータの変換は、モデル内のどのオブジェクトにも適用できますが、Power BI Desktopはデフォルトのモデル カルチャへの変換をまだサポートしていないことに注意してください。

**注意：** Tabular EditorのFile > Preferencesダイアログで "Allow unsupported Power BI features (experimental)" オプションを有効にすると、Tabular Editorは **any** オブジェクトとプロパティを編集できるようになり、Power BI Desktopがサポートしていないモデル変更を引き起こす可能性があり、クラッシュや破損した .pbixファイルを引き起こす可能性があるため、注意が必要です。この場合、Microsoftサポートは対応できませんので、自己責任で使用し、念のため.pbixファイルのバックアップをとっておいてください。
