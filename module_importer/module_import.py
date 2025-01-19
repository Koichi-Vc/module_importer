from importlib import import_module
from importlib.util import find_spec
import logging
from pathlib import Path
from re import sub, escape
from sys import exc_info
from traceback import print_exc


def create_module_import_path(file_path):
    ''' モジュールファイルディレクトリパスをインポートパスに変換 '''
    back_slash = escape('\\')#\\をエスケープ。
    rep = f"[/ | {back_slash}]"
    path = Path(file_path)
    path_dir = str(path.parent) 
    module = path.stem

    import_path = sub(rep, '.', path_dir)

    joined_import_path = import_path + '.' + module if import_path != '.' else import_path+module

    return joined_import_path


def split_module_path(module_path, split_place=None):
    ''' moduleインポートパスをfrom節とimport節に該当する様に分割する。'''
    module_name = None
    obj_name = None
    if not module_path or not isinstance(module_path, str):
        logging.warning(f'モジュールパスが無効か又は文字列ではありません。module_path: {module_name}. type: {type(module_name)}')
        return module_name, obj_name
    
    if split_place is None:
        split_place = module_path.count('.')-1#最後のドット節がimport節に来る様に調整。25/1/06/

    replace_path = module_path.replace('.', '-', split_place).split('.', 1)
    split_path = [ph.replace('-', '.') for ph in replace_path]

    if isinstance(split_path, str):
        split_path = [split_path]

    if len(split_path) >= 2:
        module_name, obj_name = split_path
    else:
        module_name = split_path[0]

    return module_name, obj_name


def get_module_attr(module, attr_path):
    #モジュールのメンバーを取得する。

    attr_names = attr_path.split('.')
    obj = None
    try:
        for attr in attr_names:
            if not obj:
                obj = getattr(module, attr)

            elif obj:
                obj = getattr(obj, attr)
    except AttributeError as a:
        logging.error(f'モジュールメンバーのインポート失敗。path: {attr_path}')
        print_exc()
    return obj


def error_message_valid(error_message, module_path):
    #モジュールパス名がエラーメッセージに含まれているか検査する。
    #真だった場合、エラーはモジュールパス由来、偽だった場合は、モジュールパス以外が理由の可能性があると解釈する。

    error_message = str(error_message).replace("'", '').replace('"',"")
    dot_length = module_path.count('.') if module_path.count('.') else 1
    included = False

    for i in reversed(range(dot_length)):

        split_module = split_module_path(module_path, i)
        module_name = split_module[0]
        
        if module_name in error_message and i != 0:
            #errorメッセージにモジュールパスが一部以上含まれていた場合、エラーの原因はモジュールパス由来と判断する。
            included = True
            break
        elif i == 0 and module_name in error_message.split():

            included = True
            break

    return included
        


def get_module(module_path, split_place=None):
    ''' moduleを動的にインポートする。'''
    obj = None
    module = None
    split_place = module_path.count('.')#モジュールパスドットの数を数える

    #モジュールパスをfromとimport部分に分割するが、始めは分割せず、module_nameのみでimportを試みる。
    module_name, obj_name = split_module_path(module_path, split_place)
    
    if module_name:

        for place in reversed(range(split_place)):

            try:
                if place == 0:
                    #placeが0になった場合、module_nameをトップレベルパスにしてブレークする。
                    module_name, obj_name = split_module_path(module_path, split_place=place)
                    break
                has_module = find_spec(module_name)#moduleのスペックを取得
                if has_module:
                    #モジュールが存在していればインポートを実行
                    module = import_module(module_name)#インポートに成功した時点でbreakする。
                    break
                else:
                    module_name, obj_name = split_module_path(module_path, split_place=place)
                   
            except ModuleNotFoundError:
                #モジュールを取得できなかった場合は、インポート出来る迄分割するドットを左へずらして行く。
                exc_type, exc_value, exc_traceback = exc_info()
                if not error_message_valid(str(exc_value), module_name):
                    #errorメッセージにインポートするモジュールやオブジェクト名が含まれていなかった場合、予期しないエラーが発生したと解釈する。
                    module = None
                    break
                module = None
                module_name, obj_name = split_module_path(module_path, split_place=place)

        #break又はfor終了時点でのmoduleインポート状況を評価
        if module is None:
            #Noneの場合、改めてmodule_nameでインポートを試みる。
            module = import_module(module_name)
    
    if module and obj_name:
        obj = get_module_attr(module, obj_name)
      
    if obj:
        return obj
    else:
        return module 



