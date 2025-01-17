# module_importer
importlibを用いて、インポートパスからモジュールやオブジェクトの動的インポートを行います。
絶対パスでのインポートを想定しており、現状相対パスはサポートしていません。

### 作成した経緯
このモジュールは、モジュールインポートの仕組み理解を深める事と、動的インポートの導入を目標にして作成しました。

### 概要
主にimportlibを用いており、モジュールに加えて、クラスなどのオブジェクトのインポートも出来る様になっています。

#### 成果
パッケージ構造やモジュールインポートの仕組み等について理解を深める事が出来た。

#### 課題
importlibの理解が不足しており、今後はモジュールのリロードを始め、将来的にはMetaPathFinderを応用した機能の実装に取り組んで行きたい。

## 使用している主要なライブラリ
- importlib
- pathlib
- re
  
## 使い方
最も簡単な使い方はget_moduleにインポートパスを渡す事です。

### 例
```
module_path = 'mypackages.subpack.mymodule'
module = get_module(module_path)
```

## メソッドの紹介
#### `get_module(module_path_name, split_place=None)`
メインのメソッドで、モジュールのインポートを行います。絶対パスを想定しており、相対パスはサポートしていません。
##### `get_module`の使用例
```
import_path = "myproject.mypackage.subpack.submodule"
module = get_module(import_path)
```

#### `split_module_path(module_path, split_place=None)`
モジュールのインポートパスを、二つに分割します。

args:
- module_path:モジュールのインポートパスを受け取る。
- split_place: 分割する箇所をint型で指定する。


##### `split_module_path`の使用例

```
import_path = "myproject.mypackage.subpack.submodule"
from_path, import_path = split_module_path(import_path)
print(from_path, import_path)
#('myproject.mypackage.subpack', 'submodule')
```
#### `get_module_attr(module, attr_path)`
インポートしたモジュールからオブジェクトを取得する。get_moduleメソッドでは、モジュールがインポートされた時点で残りのインポートパスをたどる為に使われる。

args:
- module: インポートされたモジュール
- attr_path: オブジェクトのインポートパス


