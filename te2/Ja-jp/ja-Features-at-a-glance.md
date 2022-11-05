# Basic Features

以下の記事では、Tabular Editorの最も重要な機能の概要を説明します。

## Load/save Model.bim files

CTRL+Oを押すと、ファイルを開くダイアログが表示され、Tabular Editorに読み込むModel.bimファイルを選択できます。このファイルは互換性レベル1200以上でなければなりません（JSON形式）。CTRL+SはTabular Editorで行った変更をファイルに戻して保存します（Tabular Editorを使用する前にModel.bimファイルをバックアップしておくことをおすすめします）。ロードしたモデルをAnalysis Servicesサーバーインスタンスにデプロイする場合は、以下の[デプロイメント](/Features-at-a-glance#deployment)をご覧ください。

## Connect/deploy to SSAS Tabular Databases

CTRL+SHIFT+Oを押すと、すでにデプロイされているTabular DatabaseからTabular Modelを直接開くことができます。サーバーのアドレスを入力し、（オプションで）ユーザー名とパスワードを指定します。OK" を押すと、データベースとサーバーのリストが表示されます。ロードしたいものを選択し、再度 "OK" をクリックします。

![](https://github.com/otykier/TabularEditor/blob/master/Documentation/Connect.png)

このダイアログでは、Azure ASインスタンスの完全な名前 (「azureas://」で始まる) を指定すると、Azure Analysis Servicesインスタンスに接続することもできます。ローカルインスタンス」ドロップダウンを使用して、Power BI DesktopまたはVisual Studio Integrated Workspacesの実行中のインスタンスを参照および接続できます。**Tabular EditorはTOMを通してPower BIモデルに変更を加えることができますが、これはMicrosoftによってサポートされておらず、.pbixファイルを破損する可能性があることに注意してください。自己責任で進めてください！**。

データベースがロードされた後、CTRL+Sを押すといつでも、データベースはTabular Editorで行った変更が更新されます。クライアントツール（Excel、Power BI、DAX Studioなど）は、この後すぐにデータベースの変更を見ることができるはずです。モデルへのクエリーを成功させるために、変更内容によってはモデル内のオブジェクトを手動で再計算する必要があることに注意してください。

接続したモデルをModel.bimファイルに保存したい場合は、「File」メニューから「Save As...」を選択します。

## Deployment

現在ロードされているモデルを新しいデータベースにデプロイしたい場合、またはモデルの変更で既存のデータベースを上書きしたい場合（たとえばModel.bimファイルからロードする場合）、 "Model" > "Deploy..." にあるデプロイメント・ウィザードを使用します。ウィザードは、デプロイメントプロセスをガイドし、デプロイするモデルの領域を選択できます。[詳細はこちら](/Advanced-features#deployment-wizard)を参照してください。

## Hierarchical display

ロードされたモデルのオブジェクトは、画面左側のエクスプローラツリーに表示されます。デフォルトでは、すべてのオブジェクト・タイプ (可視テーブル、ロール、リレーションシップなど) が表示されます。テーブル、メジャー、カラム、階層のみを表示したい場合は、「表示」メニューから「すべてのオブジェクト・タイプを表示」をオフにします。

![image](https://raw.githubusercontent.com/otykier/TabularEditor/master/Documentation/AllObjectTypes.png)

"テーブル" グループでテーブルを展開すると、デフォルトでは、テーブルに含まれるメジャー、列、および階層がそれぞれの表示フォ ルダに表示されます。このように、エンドユーザがクライアントツールで見るのと同じようにオブジェクトが配置されます。

![image2](https://raw.githubusercontent.com/otykier/TabularEditor/master/Documentation/DisplayFolders.png)

エクスプローラツリーのすぐ上にあるボタンを使って、不可視オブジェクトの切り替え、フォルダー、メジャー、カラム、階層の表示、名前によるオブジェクトのフィルタリングを行うことができます。オブジェクトを選択し、F2キーを押すことで、オブジェクトの名前を変更できます。これは、表示フォルダーの場合も同じです。メジャーまたは計算列をダブルクリックすると、その [DAX式](/Advanced-features#dax-expression-editor) を編集できます。右クリックするとコンテキストメニューが表示され、可視性の設定、パースペクティブインクルージョン、階層への列の追加などの操作に便利なショートカットを利用できます。

## Editing properties

画面右下のプロパティグリッドは、エクスプローラツリーで選択されたオブジェクトのプロパティのほとんどを表示します。複数のオブジェクトを同時に選択した場合、Property Gridでは、選択したオブジェクトのプロパティを同時に編集すできます。これは、たとえば、Format Stringプロパティを設定する際に便利です。Property Gridで設定可能なプロパティの例。

* Name（エクスプローラツリーでF2を押すことにより、オブジェクトの名前を直接変更できます）
* Description（説明）
* Display Folder（エクスプローラツリーで直接名前を変更することもできます。)

選択されたオブジェクトの種類によって、異なるプロパティが存在します。

## Duplicate objects and batch renamings

エクスプローラツリーの右クリック コンテキスト メニューを使用すると、メジャーや列を複製できます。複製されたオブジェクトには、名前の末尾に "copy "が付きます。さらに、複数のオブジェクトを選択してエクスプローラツリーで右クリックすると、一括で名前を変更できます。

![](https://github.com/otykier/TabularEditor/blob/master/Documentation/BatchRename.png)

名前の変更にRegExを使用し、オプションで翻訳も同様に名前を変更するかどうかを選択できます。

## Drag and drop objects

表示フォルダーに整理された多くのメジャー/カラムを持つモデルで作業する場合、Tabular Editorのもっとも便利な機能です。以下のアニメーションをご覧ください。

![](https://github.com/otykier/TabularEditor/blob/master/Documentation/DragDropFolders.gif)

フォルダー全体がドラッグされると、フォルダーの下にあるすべてのオブジェクトの表示フォルダーのプロパティがどのように変更されるかに注目してください。表示フォルダーの構造を変更するために、メジャーや列を1つ1つ確認する必要はありません。見たままが手に入るのです。

(これは、翻訳にも有効です）

## Working with Perspectives and Translations

既存のパースペクティブやトランスレーション（カルチャ）を追加/編集するには、エクスプローラツリーでモデル ノードをクリックし、プロパティ グリッドの一番下にある関連プロパティを探します。また、エクスプローラツリーが[すべてのオブジェクトタイプを表示](/Features-at-a-glance#hierarchical-display)の場合、ツリーの中で直接パースペクティブ、カルチャー、ロールを表示、編集することも可能です。

![](https://raw.githubusercontent.com/otykier/TabularEditor/master/Documentation/RolesPerspectivesTranslations.png)

既存のパースペクティブ、ロール、翻訳を複製するには、右クリックメニューを開き、「複製」を選択します。この操作により、オブジェクトの完全なコピーが作成され、必要に応じて変更できます。

パースペクティブや翻訳を「実行中」に表示するには、画面上部のツールバーにある2つのドロップダウンリストを使用します。パースペクティブを選択すると、そのパースペクティブに含まれていないすべてのオブジェクトが非表示になり、翻訳を選択すると、翻訳された名前と表示フォルダーを使用してツリー内のすべてのオブジェクトが表示されます。F2キーを押してオブジェクトや表示フォルダーの名前を変更したり、ツリー内でオブジェクトをドラッグしたりすると、その変更は選択した翻訳にのみ適用されます。

## Perspectives/Translations within object context

ツリーで1つ以上のオブジェクトを選択すると、Property Grid 内に 4 つの特別なプロパティコレクションが表示されます。

* **Captions**, **Descriptions** and **Display Folders** は、モデル内のすべてのカルチャーのリストと、各カルチャーで選択されたオブジェクトの翻訳名、説明、表示フォルダーを表示します。 **Perspectives** は、モデル内のすべてのパースペクティブと、選択オブジェクトが各パースペクティブに属しているかどうかが表示されるリストを表示します。

これらのコレクションをProperty Gridで使用すると、1つまたは複数のオブジェクトの翻訳とパースペクティブの包含を一度に変更できます。

## Undo/Redo support

Tabular Editorで行った変更は、CTRL+Zで取り消し、その後CTRL+Yでやり直すことができます。取り消せる操作の数に制限はありませんが、Model.bim ファイルを開いたり、データベースからモデルをロードすると、スタックがリセットされます。

モデルからオブジェクトを削除すると、削除されたオブジェクトを参照しているすべてのトランスレーション、パースペクティブ、リレーションシップも自動的に削除されます（通常 Visual Studioでは、オブジェクトを削除できないというエラーメッセージが表示されます）。間違って削除した場合は、Undo機能を使用して削除したオブジェクトを復元することができ、削除された翻訳、パースペクティブ、リレーションシップも復元されます。Tabular Editorは[DAX式の依存関係]()を検出できますが、別のメジャーまたは計算された列のDAX式で使用されているメジャーまたは列を削除した場合、Tabular Editorは警告を表示しないことに注意してください。
