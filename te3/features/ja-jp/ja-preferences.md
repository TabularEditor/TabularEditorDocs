# Tabular Editor 3 Preferences

タブラーデータモデルの開発プロセスやワークフローは組織によって大きく異なります。このツールをできるだけ多くのワークフローに適合させるため、Tabular Editor 3は高度なカスタマイズが可能です。ユーザーインターフェイスの外観だけでなく、ウェブプロキシ、アップデートとフィードバック、行数制限、タイムアウト、スキーマ比較の設定など、より高度なトピックについてもカスタマイズが可能です。

この記事では、Tabular Editor 3のPreferencesダイアログと、それを通してコントロールできる設定について説明します。

環境設定ダイアログにアクセスするには、**Tools > Preferences**に進みます。

> [!NOTE]
> すべてのTabular Editorの設定はWindowsユーザープロファイルごとに、`%localappdata%TabularEditor3`フォルダーに保存されます。このフォルダの内容をコピーするだけで、他のマシンに設定を移行することができます。

## Tabular Editor > Features

![image](https://user-images.githubusercontent.com/8976200/104600495-5ad6f300-5679-11eb-9572-af99f0895859.png)

### Power BI

- **Allow unsupported editing**: このオプションは、Tabular Editor 3をPower BI Desktopの外部ツールとして使用する場合にのみ関連します。チェックすると、Power BI Desktopのインスタンスに接続したとき、すべてのTOMデータ モデリング プロパティを編集できるようになります。Power BIファイルに誤ってPower BI Desktopでサポートされていない変更を加えないようにするため、一般に、このオプションはチェックしないことをオススメします（xref:desktop-limitations）。

### メタデータの同期

- **Warn when local metadata is out-of-sync with deployed model（ローカルメタデータがデプロイされたモデルと同期していない場合に警告を出す）**: チェックすると、Analysis Servicesにまだ保存されていないモデルへのローカルな変更を行った場合に、Tabular Editor内に情報バーが表示されます。たとえば、DAXクエリやピボットグリッドが期待した結果を生成しない場合、Analysis Servicesに変更を保存せずにTabular Editorでメジャー式を変更したことが原因です。保存（Ctrl+S）を押すとバーが消えます。情報バーを見るのが面倒な場合は、このチェックを外してください。
- **Track external model changes（外部モデル変更の追跡）**: Power BI Desktopが外部ツールによるデータモデルの変更を検知できるように、Tabular Editorも検知できるようになりました。つまり、これをチェックした状態で、他のユーザーやアプリケーションが *Analysis Servicesのローカルインスタンス* でモデルに変更を加えた場合、Tabular Editorは通知を受け取ります。
  - **Refresh local Tabular Object Model metadata automatically（ローカルのTabular Object Modelのメタデータを自動的に更新する）**: 上記の通知によって、Tabular Editor内のメタデータを実際に更新したい場合は、このチェックボックスをオンにします。

### ベストプラクティス・アナライザー

- **Scan for Best Practice violations in the background（ベストプラクティス違反のスキャンをバックグラウンドで実施）** チェックされていない場合、違反があるかどうかを確認するために、ベストプラクティス・アナライザー・ツールウィンドウ内から明示的にベストプラクティス分析を実行する必要があります。チェックした場合、変更が加えられるたびに、バックグラウンドスレッドで継続的にスキャンが行われます。非常に大きなモデルや、非常に複雑なベストプラクティスルールを持つモデルの場合、問題が発生します。

## Tabular Editor > Updated and Feedback

![image](https://user-images.githubusercontent.com/8976200/104601469-92926a80-567a-11eb-9499-1d1c8d967c72.png)

- **Check for updates on start-up（スタートアップ時に更新を確認）**:かなり自明です。パブリックプレビュー期間中にアップデート通知は行われず、下の「アップデートを確認する」ボタンも現時点では機能しません。
- **Help improve Tabular Editor by collecting anonymous usage data（匿名の使用データを収集し、Tabular Editorの改善に役立てる。）**: データには、個人を特定できるような情報や、お客様のデータモデルの構造や内容に関する情報は一切含まれません。それでもテレメトリーのオプトアウトを希望される場合は、このチェックを外してください。
- **Send error reports（エラーメッセージの送信）**: クラッシュした場合、Tabular Editorはこれをチェックすると、クラッシュレポートを送信するオプションを表示します。クラッシュレポートはデバッグの際に非常に役立ちますので、差し支えなければチェックしたままにしておいてください。

## Data Browsing > Pivot Grid / DAX Query

![image](https://user-images.githubusercontent.com/8976200/104601874-0df41c00-567b-11eb-8ba1-41a992e5664f.png)

この設定により、モデルの変更がAnalysis Servicesに保存されたとき、新しいピボットグリッドまたはDAXクエリウィンドウがデフォルトで自動的に更新されるかどうかを指定できます。以下のスクリーンショットにあるように、「Auto-execute」ボタンを切り替えることで、ウィンドウごとにこの動作を変更できます。

![image](https://user-images.githubusercontent.com/8976200/104602109-56abd500-567b-11eb-9e8f-32ab58390449.png)

この機能は、たとえば、メジャーのデバッグを行う際に非常に便利です。あるウィンドウでメジャー式を更新し、別のウィンドウでそのメジャーを使用するピボット・グリッドまたはDAXクエリを開いておきます。CTRL+Sを押すたびに、ピボット・グリッドまたはDAXクエリが自動的に更新され、行った変更の影響が即座に表示されます。

## DAX Editor > General

![image](https://user-images.githubusercontent.com/8976200/104602381-a7233280-567b-11eb-8151-cf810b7cb748.png)

さて、いよいよ本題に入ります。このページでは、DAXエディターの一般的な構成に関する設定を数多く提供しています。コードの折りたたみ」機能をぜひ試してみてください。

- **DAX function documentation（DAX関数ドキュメント）**: この設定は、DAX関数にカーソルがあるときにF12キーを押したときに、デフォルトのWebブラウザで起動するURLを指定するために使用します。私は https://dax.guide を使うことをオススメしますが、Microsoftの公式ドキュメント（ドロップダウンで利用可能）を好む人もいるようです。

## DAX Editor > Auto Formatting

![image](https://user-images.githubusercontent.com/8976200/104602767-084b0600-567c-11eb-88ea-018e3d436f68.png)

上のスクリーンショットからわかるように、新しいDAXエディターは非常に強力で、入力中に美しく読みやすいDAXコードを作成するのに役立ちます。また、何か期待通りに動作しない場合や、さらなる改善のためのアイデアがある場合は、[フィードバック](https://github.com/TabularEditor3/PublicPreview/issues/new)を提供することを忘れないでください。

## DAX Editor > Code Assist

![image](https://user-images.githubusercontent.com/8976200/104603313-90311000-567c-11eb-853d-6ca6e0f0ed07.png)

このページでは、コードアシストのもっとも重要な2つの機能であるコールチップ（別名「パラメーター情報」）とオートコンプリートを設定できます。設定は主に、コールチップとオートコンプリートのボックスがどのような状況で画面に表示されるかを制御します。ただし、オートコンプリートについてはどの項目を提案するか、テーブル名を常に引用するか、インクリメンタルサーチなどを制御するための機能があります。
