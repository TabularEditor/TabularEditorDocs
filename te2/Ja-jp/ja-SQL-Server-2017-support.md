# SQL Server 2017対応

バージョン2.3から、Tabular EditorはSQL Server 2017 (Compatibility Level 1400)もサポートするようになりました。これは、Tabular EditorのUIが、[こちら](https://blogs.msdn.microsoft.com/analysisservices/2017/04/19/whats-new-in-sql-server-2017-ctp-2-0-for-analysis-services/) で説明されている新機能の一部を公開することを意味します。

ただし、これらの機能を使用するには、[Tabular Editor の適切なビルド](https://github.com/otykier/TabularEditor/releases/tag/2.5-CL1400) をダウンロードする必要があることに注意してください。これは、SQL Server 2017 / SSDT 17.0向けに新しいクライアントライブラリのセットがMicrosoftから提供されており、これらのライブラリはTabular EditorのSQL Server 2016-ビルドと互換性がないためです。新しいライブラリは、新しい[SSDTのバージョン](https://docs.microsoft.com/en-us/sql/ssdt/download-sql-server-data-tools-ssdt)から取得できます（Visual Studio 2015が必要です）。

互換性レベル1400の機能が必要ない場合は、SQL Server 2016-ビルドの[Tabular Editor](https://github.com/otykier/TabularEditor/releases/tag/2.5)を使用できます。

ここでは、Tabular Editorで新機能がどのように使用されるかを簡単に説明します。

## 日付リレーションシップ

すべてのリレーションシップで、プロパティ・グリッドの「Join on Date Behavior」プロパティが公開されるようになりました。

![image](https://cloud.githubusercontent.com/assets/8976200/25297821/9dd46be0-26f0-11e7-92bf-10a921ed20dc.png)

## バリエーション（列・階層再利用）

プロパティグリッドの「バリエーション」プロパティを展開することで、カラムにバリエーションを設定できます。

![image](https://cloud.githubusercontent.com/assets/8976200/25297845/c69ecc5a-26f0-11e7-93af-b7a2a0cc9310.png)

なお、**Object Level Security** はカラムレベルで指定することも可能です。

省略記号ボタンをクリックすると、バリエーションコレクションエディターが開き、ここからPower BIで列や階層を再浮上させる方法を設定できます。

![image](https://cloud.githubusercontent.com/assets/8976200/25297884/fd4faf58-26f0-11e7-9a1a-df7a1b05f663.png)

テーブルレベルで「バリエーションとしてのみ表示」プロパティを「True」に設定することを忘れないでください。

![image](https://cloud.githubusercontent.com/assets/8976200/25297917/2c1e4b64-26f1-11e7-8ce6-a62aef2b7d8a.png)

**詳細行式**は、テーブルおよびメジャーに直接設定できます。ただし、現時点では、構文の強調表示やインテリセンスは使用できません。

Hierarchyオブジェクトは、ラグドヒエラルキーに便利な新しい**Hide Members**プロパティを公開します。
