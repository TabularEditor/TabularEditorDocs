# よくある質問

## Tabular Editorとは何ですか？

基本的に、Tabular EditorはAnalysis Services Tabular Modelを構成するメタデータを編集するためのUIを提供します。モデルの編集にTabular Editorを使う場合とVisual Studioを使う場合の主な違いは、Tabular Editorは_data_をロードしないことです - _metadata_のみです。つまり、メジャーや表示フォルダーなどを作成および変更する際に、検証や計算が行われないということです。検証や計算は、ユーザーが変更をデータベースに保存することを選択したときにのみ実行されます。これは、Visual Studioでの作業が遅くなりがちな中型から大型のモデルに対して、より良い開発者体験を提供します。

さらに、Tabular Editorには多くの[Features](Features-at-a-glance.md)があり、一般的に生産性を高め、特定の作業を容易にできます。

## なぜSSAS Tabularにさらに別のツールが必要なのか？

Analysis Services Tabularで作業する場合、SQL Server Data Tools (Visual Studio), [DAX Editor](https://www.sqlbi.com/tools/dax-editor/), [DAX Studio](https://www.sqlbi.com/tools/dax-studio/), [BISM Normalizer](http://bism-normalizer.com/) and [BIDSHelper](https://bidshelper.codeplex.com/) にすでに慣れているかも知れません。これらはすべて優れたツールで、それぞれ独自の目的を持っています。Tabular Editorはこれらのツールに取って代わるものではなく、むしろこれらのツールを補足するものと考えるべきでしょう。なぜTabular Editorが正当化されるのか、[Features at a glance](Features-at-a-glance.md) articleをご覧ください。

## なぜTabular EditorはVisual Studioのプラグインとして利用できないのですか？

Visual Studio内でTabular Modelsを扱うためのより良いユーザー体験は間違いなく評価されますが、スタンドアロンツールはプラグインよりもいくつかの利点を提供します。まず第一に、Tabular Editorを使うのにVisual Studio/SSDTのインストールは**必要ありません**。Tabular EditorはAMOライブラリのみを必要とし、VSと比較して非常に小さなインストールで済みます。次に、TabularEditor.exeはデプロイ、スクリプトなどのコマンドラインオプションで実行可能で、これは.vsix（プラグイン）プロジェクトでは不可能なことです。

また、特筆すべきは、Tabular Editorは[standalone .zip file](https://github.com/otykier/TabularEditor/releases/latest/download/TabularEditor.Portable.zip)としてダウンロードできます。つまり、何もインストールする必要がないのです。言い換えれば、Windowsマシンの管理者権限がなくてもタブラーエディターを実行することができるのです。zipファイルをダウンロードし、解凍してTabularEditor.exeを実行するだけです。

## 今後のリリースではどのような機能が予定されていますか？

現在のロードマップは[こちら](Roadmap.md)でご覧になれます。
