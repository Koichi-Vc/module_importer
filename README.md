# module_importer
importlibを用いて、インポートパスからモジュールやオブジェクトの動的インポートを行います。
パスは絶対パスを想定しており、相対パスは未検証です。

### 作成した経緯
pythonのモジュールインポートの仕組みとモジュール自体の設計を学習する目的で、"動的インポートが出来るモジュール"をテーマに作成をしました。

## 使い方
最も簡単な使い方はget_moduleにインポートパスを渡す事です。

### 例
```
module_path = 'mypackages.subpack.mymodule'
module = get_module(module_path)
```

## メソッド
#### `get_module(module_path_name, split_place=None)`
メインのメソッドで、モジュールパスから動的インポートを行う。文字列の絶対パスを想定しており、相対パスはサポートしていません。
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

