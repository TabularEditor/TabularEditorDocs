---
uid: roslyn
title: Compiling with Roslyn
author: Daniel Otykier
updated: 2021-09-28
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
## Compiling with Roslyn

If you prefer to compile your scripts using the new Roslyn compiler introduced with Visual Studio 2017, you can set this up under **Tools > Preferences > Tabular Editor > C# SCripts and Maros**. This allows you to use newer C# language features such as string interpolation. Simply specify the path to the directory that holds the compiler executable (`csc.exe`) and specify the language version as an option for the compiler:

![Custom Compiler Te3](~/content/assets/images/custom-compiler-te3.png)

### Visual Studio 2017

For a typical Visual Studio 2017 Enterprise installation, the Roslyn compiler is located here:

```
c:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\MSBuild\15.0\Bin\Roslyn
```

This includes the C# 6.0 language features by default.

![image](https://user-images.githubusercontent.com/8976200/92464584-a52cfc80-f1cd-11ea-9b66-3b47ac36f6c6.png)

### Visual Studio 2019

For a typical Visual Studio 2019 Community installation, the Roslyn compiler is located here:

```
c:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\Roslyn
```

The compiler that ships with VS2019 supports C# 8.0 language features, which can be enabled by specifying the following as compiler options:

```
-langversion:8.0
```
