# Compiling with Roslyn

Visual Studio 2017で導入された新しいRoslynコンパイラーを使用してスクリプトをコンパイルしたい場合は、**Tools > Preferences > Tabular Editor > C# SCripts and Maros**で設定できます。これにより、文字列補間などの新しいC#言語の機能を利用できます。コンパイラの実行ファイル（`csc.exe`）を格納するディレクトリのパスを指定し、コンパイラのオプションとして言語バージョンを指定するだけで、簡単に設定できます。

![Custom Compiler Te3](../../../images/custom-compiler-te3.png)

## Visual Studio 2017

一般的なVisual Studio 2017 Enterpriseのインストールでは、Roslynコンパイラはここに配置されています。

```
c:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\MSBuild\15.0\Bin\Roslyn
```

これには、C# 6.0の言語機能がデフォルトで含まれています。

![image](https://user-images.githubusercontent.com/8976200/92464584-a52cfc80-f1cd-11ea-9b66-3b47ac36f6c6.png)

## Visual Studio 2019

一般的なVisual Studio 2019 Communityインストールの場合、Roslynコンパイラはここにあります。

```
c:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\Roslyn
```

VS2019に同梱されているコンパイラは、C#8.0の言語機能をサポートしており、コンパイラオプションとして以下を指定することで有効にできます。

```
-langversion:8.0
```
