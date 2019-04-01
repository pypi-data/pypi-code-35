"""This is a test module for show text lines.

The text lines are read from input text file.
The text file needs to be encoded in UTF-8 or Shift-JIS.
This changes each control code (x00 - x1f) into '▲'.

Copyright 2019 K2UNIT
"""

import datetime
import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox

import regex


# one shot patelier
def patelier():
    """This reads the text file and show text lines.
    The text file needs to include text lines.
    This calls patisserie function to print text lines.
    """
    root = tkinter.Tk()
    root.withdraw()
    file_type = [('', '*.txt')]
    crnt_dir = os.getcwd()
    tkinter.messagebox.showinfo(
            'patelier',
            'テキストファイルを選択してください。')
    src_file_path = tkinter.filedialog.askopenfilename(
            filetypes=file_type,
            initialdir=crnt_dir)  # 初期Dir=カレントDir
    root.destroy()
    if not os.path.isfile(src_file_path):
        print(''.join((
                '■Error:処理対象ファイルが存在しません。',
                src_file_path)))
        print('■異常終了')
    else:
        strs = _read_file(src_file_path)
        if not strs:
            strs = _read_file_cp932(src_file_path)
        if not strs:
            strs = _read_file_utf8(src_file_path)
        if not strs:
            print('■異常終了')
        else:
            if not patisserie(strs, False, '', src_file_path):
                print('■異常終了')


# File読込
def _read_file(filepath):
    try:
        with open(filepath, mode='rt') as f:
            return f.read().splitlines()
    except OSError:
        print(''.join((
                '■Warning:ファイルOpen(標準文字コード)に'
                '失敗しました(Shift-JIS[CP932]指定で再試行します)。',
                filepath)))
        return []
    except Exception as e:
        print(''.join((
                '■Warning:ファイルOpen(標準文字コード)に'
                '失敗しました(Shift-JIS[CP932]指定で再試行します)。',
                filepath, ' ', str(e.args[0]))))
        return []


# CP932明示指定File読込
def _read_file_cp932(filepath):
    try:
        with open(filepath, mode='rt', encoding='cp932') as f:
            return f.read().splitlines()
    except OSError:
        print(''.join((
                '■Warning:ファイルOpen(Shift_JIS[CP932]指定)に'
                '失敗しました(UTF-8指定で再試行します)。', filepath)))
        return []
    except Exception as e:
        print(''.join((
                '■Warning:ファイルOpen(Shift_JIS[CP932]指定)に'
                '失敗しました(UTF-8指定で再試行します)。', filepath, ' ',
                str(e.args[0]))))
        return []


# UTF-8明示指定File読込
def _read_file_utf8(filepath):
    try:
        with open(filepath, mode='rt', encoding='utf-8') as f:
            return f.read().splitlines()
    except OSError:
        print(''.join((
                '■Error:ファイルOpen(UTF-8指定)に失敗しました。',
                filepath)))
        return []
    except Exception as e:
        print(''.join((
                '■Error:ファイルOpen(UTF-8指定)に失敗しました。',
                filepath, ' ', str(e.args[0]))))
        return []


# テキスト結果出力
# textlines:テキスト行list、zero_flg=False:called from patelier function、
# output_dir:不要、
# src_file_path:入力原文ファイルPath(patelier functionからの呼出しで必要)
# 戻り値(True:正常、False:異常)
def patisserie(textlines, zero_flg, output_dir, src_file_path):
    """This gets the text lines and outputs them.

    This changes each control code (x00 - x1f) into '▲'.
    Args:
        textlines (list): This is a list of line strings of text data.
        zero_flg (bool): False is set by patelier function.
        output_dir (string): This is needless when.
        src_file_path (string): This is a source file path.
    Returns:
        bool:
            True: OK
    """
    if not zero_flg:  # called from patelier function
        print(''.join(('■処理対象ファイル:', src_file_path)))
        start_time = datetime.datetime.now()
        print(''.join((
            '■テキスト出力開始:',
            start_time.strftime('%Y/%m/%d %H:%M'))))
        line_number = 1
        for each_text in textlines:
            new_text = each_text.rstrip()
            msg = regex.sub(r'[\x00-\x1f]', '▲', new_text)
            print(''.join((str(line_number), ':', msg, '\n')))
            line_number += 1
        end_time = datetime.datetime.now()
        delta_time = end_time - start_time
        print(''.join((
                '■テキスト出力終了:', end_time.strftime('%Y/%m/%d %H:%M'),
                ' (処理時間{0}sec)'.format(delta_time.seconds))))
        return True
    else:
        return False


if '__main__' == __name__:
    patelier()
