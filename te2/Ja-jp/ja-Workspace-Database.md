## Introducing Workspace Databases

Tabular Editor 3.0は、Analysis Servicesのインスタンスに展開されたデータベースへの同時接続で、ディスクからロードされたモデルのメタデータの編集をサポートします。このデータベースを_workspace database_と呼びます。今後、Tabular Editorでタブラーモデリングを行う場合は、この方法を推奨します。

Save (Ctrl+S) を1回押すだけで、ディスクへの変更の保存とワークスペースデータベースのメタデータの更新を同時に行うことができるため、開発ワークフローが非常にシンプルになります。また、Analysis Servicesから返されたエラーメッセージは、Saveを押すとすぐにTabular Editorに表示されるという利点もあります。ある意味、ワークスペース・データベースが更新されるタイミングをコントロールできることを除けば、SSDT / Visual StudioまたはPower BI Desktopが行う方法に似ています。

Model.bimファイルやフォルダー構造からモデルを読み込むと、次のようなプロンプトが表示されます。

![image](https://user-images.githubusercontent.com/8976200/58166683-a65db180-7c8a-11e9-9df3-be9a716b3ad1.png)

* **Yes**: モデルメタデータはディスクからロードされ、すぐにAnalysis Servicesのインスタンスにデプロイされます。その後、Tabular Editorは新しくデプロイされたデータベースに接続します。次に同じモデルをディスクからロードすると、Tabular Editorは自動的に再デプロイされ、データベースに接続されます。
* **No**: モデルのメタデータは、Analysis Servicesのインスタンスに接続することなく、通常通りディスクからTabular Editorに読み込まれます。
* **No, don't ask again**: 上記のオプションと同じですが、Tabular Editorは次に同じモデルをロードしたときに再度質問することはありません。

### Setting up a Workspace Database

上記のプロンプトで「Yes」オプションを選択すると、Analysis Servicesのインスタンスに対するサーバ名と（オプションの）資格情報の入力を求められます。OK "を押すと、インスタンス上にすでにあるデータベースのリストが表示されます。Tabular Editorは新しいデータベースをデプロイすることを想定しており、Windowsユーザー名と現在の日付と時刻に基づいて新しいデータベースのデフォルト名を提供します。

![image](https://user-images.githubusercontent.com/8976200/58179509-a10f5f80-7ca8-11e9-9764-4cb76b9d1a8b.png)

既存のデータベースをワークスペースのデータベースとして使用する場合は、リストで選択するだけです。**注意警告: 既存のデータベースを選択した場合、ディスクから読み込まれたモデルのメタデータで上書きされます。このため、本番インスタンスにワークスペース・データベースをセットアップすることは推奨されません！**。

### The User Options file (.tmuo)

ファイルシステム内の各モデルのワークスペース設定を追跡するために、Tabular Editor 3.0では.tmuo（Tabular Model User Optionsの略）タイプの新しいファイルを導入し、Model.bimまたはDatabase.jsonファイルの隣に配置されるようにしました。

.tmuoファイルは、以下の内容を持つ単なるjson文書である。

```json
{
  "UseWorkspace": true,
  "WorkspaceConnection": "Data Provider=MSOLAP;Data Source=localhost",
  "WorkspaceDatabase": "AdventureWorks_WS_Feature123"
}
```

ディスクからモデルのメタデータをロードする際、Tabular Editorはロードされたモデルファイルと同じディレクトリに .tmuo ファイルがあるかどうかを調べます。.tmuo ファイルの名前は次のパターンにしたがっている必要があります。

```
<modelfilename>.<windowsusername>.tmuo
```

このファイルにユーザー名が含まれているのは、複数の開発者が並行して開発するワークフローにおいて、お互いのワークスペース・データベースを不注意に上書きしてしまうことを防ぐためです。このファイルが存在し、ファイルの "UseWorkspace" フラグが "true" に設定されている場合、Tabular Editorはディスクからモデルをロードする際に次のステップを実行します。

1. .tmuoファイルで指定されたサーバー名とデータベース名を使用して、モデルのメタデータをワークスペース・データベースに配備します（既存のメタデータを上書きします）。
2. Connect to the newly deployed database in "workspace mode".

「ワークスペース・モード」では、Save (ctrl+s) を押すと、Tabular Editorは同時にモデルをディスクに保存し、ワークスペース・データベースを更新します。これにより、モデルのメタデータをディスクに保存する際、手動でデータベースをデプロイしたり、File > Save As... やFile > Save to Folder... を実行しなくても、新しいコードのテストやAnalysis Servicesが提供するエラーメッセージを迅速に確認することができるようになりました。
