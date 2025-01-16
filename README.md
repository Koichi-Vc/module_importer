# module_importer
importlibを用いて、インポートパスからモジュールやオブジェクトの動的インポートを行います。
パスは絶対パスを想定しており、相対パスは未検証です。

### 作成した経緯
pythonのモジュールインポートの仕組みとモジュール自体の設計を学習する目的で、"動的インポートが出来るモジュール"をテーマに作成をしました。

## 使い方
最も簡単な使い方はget_moduleにインポートパスを渡す事です。

### 例
module_path = 'mypackages.subpack.mymodule'
module = get_module(module_path)
