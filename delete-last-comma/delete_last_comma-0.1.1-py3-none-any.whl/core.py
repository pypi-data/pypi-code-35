# -*- coding: utf-8 -*-
"""
json形式の不完全（いわゆるケツカンマを含む）なテキストファイルを、
完全なjson形式のオブジェクトとして読み込む
"""
import json

def get_json_dict_from_path(path):
    """ファイルのフルパスからjson形式の辞書を取得する。
    ファイルの中身が厳密なjsonでなくても、ケツカンマや不要な閉じかっこ程度なら修正して読み込む"""
    json_str = get_str_from_file(path)
    completed_reading = False
    while not completed_reading:
        try:
            json_dict = json.loads(json_str)
            completed_reading = True
        except json.decoder.JSONDecodeError:
            json_str = format_readable_json(json_str)

    return json_dict

def get_str_from_file(path):
    """ファイルの内容を文字列として読み込む"""
    with open(path, encoding="utf-8") as file:
        file_str = file.read()

    return file_str

def format_readable_json(unreadable_json_str) -> str:
    """種々の処理を行い、json形式として読み込み可能な文字列に整形する"""
    deleted_comma = delete_last_comma(unreadable_json_str)
    try:
        json.loads(deleted_comma)
        output = deleted_comma
    except json.decoder.JSONDecodeError:
        deleted_extra_bracket = delete_last_bracket(deleted_comma)
        output = deleted_extra_bracket
    return output

def delete_last_comma(including_last_comma_string: str) -> str:
    """
    入力文字列内に存在するケツカンマを削除し、削除した後の文字列を返す。
    ケツカンマを判定する条件は次の通り。
    ・カンマのあとに「'"' or 数字」が出現しないまま「']' or '}'」が登場する
    """
    last_comma_index = []
    doubt_last_comma_index = -1 # ただカンマを見つけただけではケツカンマかどうかわからないのでdoubt
    exists_comma_forward = False # 今ループで見ている文字より前にカンマが存在するかどうか
    for index, char in enumerate(including_last_comma_string):
        if char == ",":
            exists_comma_forward = True
            doubt_last_comma_index = index
        elif char in ['"', "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            exists_comma_forward = False
        elif char in ["]", "}"] and exists_comma_forward:
            last_comma_index.append(doubt_last_comma_index)
            exists_comma_forward = False
        else:
            pass

    output = ""
    if last_comma_index: # リストが空でないとき
        str_list = list(including_last_comma_string)

        # インデックスの後ろから処理していくことで、削除したときにインデックスが狂うことがなくなる
        for index in reversed(last_comma_index):
            del str_list[index]

        # 空文字列を区切り文字にして結合することで、ただの文字列への変換の代わりにする
        output = "".join(str_list)
    else:
        # 何も削除する必要がなかった場合
        output = including_last_comma_string

    return output

def delete_last_bracket(unreadable_json_str) -> str:
    """最後に余計な閉じかっこが存在する場合に削除する"""
    reversed_list = list(reversed(unreadable_json_str))
    for index, char in enumerate(reversed_list):
        if char == "}":
            del reversed_list[index]
            break # 削除する閉じかっこは一つだけ

    valid_order_list = reversed(reversed_list)
    output = "".join(valid_order_list)
    return output
