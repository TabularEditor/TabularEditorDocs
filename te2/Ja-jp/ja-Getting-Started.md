# Getting Started

## Installation

[リリースページ](https://github.com/otykier/TabularEditor/releases/latest)から.msiファイルをダウンロードし、.msiのインストールを実行するだけです。

## Prerequisites

なし。

> [!NOTE]
> Tabular Editor は [Tabular Object Model](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) を使用して Model.bim ファイルや既存のデータベースとの間でメタデータの読み込みと保存を行います。これは.msiインストーラーに含まれています。[Analysis Services Client Libraries](https://docs.microsoft.com/en-us/azure/analysis-services/analysis-services-data-providers)については、マイクロソフト社の公式ドキュメントをご覧ください。

## System requirements

- **Operating system:** Windows 7, Windows 8, Windows 10, Windows Server 2016, Windows Server 2019 or newer
- **.NET Framework:** [4.6](https://dotnet.microsoft.com/download/dotnet-framework)

## Working with Tabular Editor

推奨されるワークフローは、通常通りSSDTを使ってテーブルとリレーションシップを設定し、あとはTabular Editorで行うことです。つまり計算列、メジャー、階層、パースペクティブ、トランスレーション、表示フォルダー、その他あらゆる種類の微調整を行います。

Model.bim ファイルを読み込むには、File メニューから Open > From File... オプションを選択するか（CTRL+O）、既存のデータベースを Analysis Services のインスタンスから Open > From DB... オプションを選択します。後者の場合、サーバー名とオプションの認証情報を入力するよう求められます。

![既にデプロイされているTabularモデルへの接続](https://raw.githubusercontent.com/otykier/TabularEditor/master/Documentation/Connect.png)

これは、新しいAzure Analysis Services PaaSでも機能します。ローカルインスタンス」ドロップダウンを使用して、Power BI DesktopまたはVisual Studio Integrated Workspacesの実行中のインスタンスを参照および接続できます。**Tabular Editor は TOM を通して Power BI モデルに変更を加えることができますが、すべてのモデリング操作が Microsoft によってサポートされているわけではないことに注意してください。[詳細](/Power-BI-Desktop-Integration)**。

OK "をクリックすると、サーバー上のデータベースのリストが表示されます。

これが、モデルをTabular Editorにロードした後のUIの様子です。

![The main UI of Tabular Editor](https://raw.githubusercontent.com/otykier/TabularEditor/master/Documentation/Main%20UI.png)

画面の左側のツリーには、タブラ・モデル内のすべてのテーブルが表示されます。テーブルを展開すると、テーブル内のすべての列、メジャー、および階層が、表示フォルダーごとにグループ化されて表示されます。ツリーのすぐ上にあるボタンを使って、表示フォルダー、非表示オブジェクト、特定のタイプのオブジェクトを切り替えたり、名前でオブジェクトをフィルタリングしたりできます。ツリー内の任意の場所を右クリックすると、新しいメジャーの追加、オブジェクトの非表示、オブジェクトの複製、オブジェクトの削除など、一般的なアクションを含むコンテキストメニューが表示されます。F2キーを押して現在選択されているオブジェクトの名前を変更したり、複数選択して右クリックすることで複数のオブジェクトの名前を一括で変更できます。

![Batch Renaming lets you rename multiple objects simultaneously](https://raw.githubusercontent.com/otykier/TabularEditor/master/Documentation/BatchRename.png)

メインUIの右上には、DAXエディターがあり、モデル内の任意のメジャーまたは計算列のDAX式を編集するために使用できます。DAX Formatter」ボタンをクリックすると、www.daxformatter.comを通じてコードを自動的にフォーマットできます。

右下隅にあるプロパティ・グリッドを使用して、フォーマット文字列、説明、トランスレーション、パースペクティブ・メンバーシップなどのオブジェクトのプロパティを調べたり設定したりできます。表示フォルダーのプロパティもここで設定できますが、ツリー内のオブジェクトをドラッグ＆ドロップして表示フォルダーを更新する方が簡単です（CTRLまたはSHIFTで複数のオブジェクトを選択してみてください）。

パースペクティブやトランスレーション（カルチャ）を編集するには、ツリーで「モデル」オブジェクトを選択し、プロパティ・グリッドで「モデルのパースペクティブ」または「モデルのカルチャ」プロパティを見つけます。小さな楕円形のボタンをクリックすると、パースペクティブやカルチャを追加、削除、編集するためのコレクションエディターが開きます。

![Editing perspectives - click the elipsis button to the right](https://raw.githubusercontent.com/otykier/TabularEditor/master/Documentation/Edit%20Perspectives.png)

変更をModel.bimファイルに戻して保存するには、保存ボタンをクリックするか、CTRL+Sを押します。既存のTabularデータベースを開いている場合、変更は直接データベースに保存されます。データベースをTabular Editorに読み込んでから変更された場合は、プロンプトが表示されます。CTRL+Zを押せばいつでも変更を取り消すことができます。

モデルを別の場所にデプロイしたい場合、"Model" メニューから "Deploy" を選択してください。

## Deployment

Tabular Editorにはデプロイメントウィザードがあり、SSDTからデプロイする場合と比較して既存のデータベースにデプロイする場合、いくつかの利点があります。デプロイ先のサーバーとデータベースを選択した後、手元にあるデプロイ用の以下のオプションがあります。

![Deployment Wizard](https://raw.githubusercontent.com/otykier/TabularEditor/master/Documentation/Deployment.png)

" Deploy Connections "ボックスをオフにすると、ターゲットデータベース上のすべてのデータソースが変更されないことを確認します。モデルに、ターゲットデータベースに存在しないデータソースを持つテーブルが1つ以上含まれている場合、エラーが表示されます。

同様に、"Deploy Table Partitions "をオフにすると、テーブル上の既存のパーティションは変更されず、パーティション内のデータはそのまま残されます。

ロールのデプロイ "にチェックを入れると、ターゲットデータベース内のロールはロードしたモデルの内容に更新されますが、"ロールメンバーのデプロイ "にチェックを入れないと、各ロールのメンバーはターゲットデータベースで変更されません。

## Command Line usage

コマンド ラインを使用して、自動デプロイメントを行うことができます。GUI で利用可能なすべてのデプロイメントオプションは、コマンドラインでも利用可能です。

### Deployment Examples

`TabularEditor.exe c:\Projects\Model.bim`

Tabular Editor GUIを開き、指定されたModel.bimファイルをロードします（デプロイは行いません）。

`TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks`

指定されたModel.bimファイルをlocalhost上で動作するSSASインスタンスにデプロイし、AdventureWorksデータベースを上書きまたは作成します。GUIはロードされません。

デフォルトでは、パーティション、データソース、ロールはターゲットデータベースで上書きされません。この動作は、上記のコマンドに以下のスイッチを1つ以上追加することで変更可能です。

* `-P` Overwrite **p**artitions
* `-C` Overwrite **c**onnections (data sources)
* `-R` Overwrite **r**oles
* `-M` Overwrite role **m**embers

コマンドラインオプションの詳細については、[以下を参照してください。](/Command-line-Options)

> [!NOTE]
> TabularEditor.exe は Windows Forms アプリケーションなので、コマンドラインから実行するとアプリケーションが別のスレッドで実行され、呼び出し元にすぐに制御が戻されます。これは、バッチジョブの一部としてデプロイメントを実行する場合、ジョブを進める前にデプロイメントが成功するのを待つ必要があり、問題を引き起こす可能性があります。このような問題が発生した場合は、`start /wait` を使用して TabularEditor がその仕事を終えてから呼び出し元に制御を戻してください。
> 
> `start /wait TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks`

## Advanced Scripting

Tabular Editorでは、C#を使用してロードされたモデルへの変更をスクリプト化できます。これは、一度に多くのオブジェクトにいくつかの変更を適用したい場合に実用的です。アドバンスト・スクリプト・エディターは、2つのオブジェクトにアクセスできます。

* `Selected` は、エクスプローラツリーで現在選択されているすべてのオブジェクトを表します。
* `Model` で、Tabular Object Modelのツリー全体を表します。

アドバンスト・スクリプト・エディターには、使い始めに必要なインテリセンス機能がいくつか用意されています。

![IntelliSenseにより、Tabular Editorのスクリプトを作成することができます。](https://raw.githubusercontent.com/otykier/TabularEditor/master/Documentation/AdvancedEditor%20intellisense.png)

アドバンスト・スクリプティングに関する詳しい説明とサンプルは、[こちら](/Advanced-Scripting)を参照してください。
