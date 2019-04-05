# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['diff_1c']

package_data = \
{'': ['*']}

install_requires = \
['cjk-commons>=3.3,<4.0', 'parse-1c-build>=5.5,<6.0']

entry_points = \
{'console_scripts': ['diff1c = diff_1c.__main__:run']}

setup_kwargs = {
    'name': 'diff-1c',
    'version': '6.2.3',
    'description': 'Diff utility for 1C:Enterprise',
    'long_description': 'РЈС‚РёР»РёС‚Р° РґР»СЏ СЃСЂР°РІРЅРµРЅРёСЏ *epf*-, *erf*-, *ert*- Рё *md*-С„Р°Р№Р»РѕРІ\n===\n\nР§С‚Рѕ РґРµР»Р°РµС‚\n---\n\nР¤Р°Р№Р»С‹ СЂР°Р·Р±РёСЂР°СЋС‚СЃСЏ СЃ РїРѕРјРѕС‰СЊСЋ РїР°РєРµС‚Р° [parse-1c-build][1] РІ РєР°С‚Р°Р»РѕРіРё, РєРѕС‚РѕСЂС‹Рµ Р·Р°С‚РµРј СЃСЂР°РІРЅРёРІР°СЋС‚СЃСЏ СѓРєР°Р·Р°РЅРЅРѕР№ РІ Р°СЂРіСѓРјРµРЅС‚Р°С… \nРєРѕРјР°РЅРґРЅРѕР№ СЃС‚СЂРѕРєРё СѓС‚РёР»РёС‚РѕР№ СЃСЂР°РІРЅРµРЅРёСЏ. РџРѕРґРґРµСЂР¶РёРІР°СЋС‚СЃСЏ AraxisMerge, ExamDiff, KDiff3, WinMerge.\n\nРџСЂРё СѓСЃС‚Р°РЅРѕРІРєРµ РїР°РєРµС‚Р° РІ РєР°С‚Р°Р»РѕРіРµ СЃРєСЂРёРїС‚РѕРІ РёРЅС‚РµСЂРїСЂРµС‚Р°С‚РѕСЂР° Python СЃРѕР·РґР°С‘С‚СЃСЏ РёСЃРїРѕР»РЅСЏРµРјС‹Р№ С„Р°Р№Р» *diff1c.exe*.\n\nРўСЂРµР±РѕРІР°РЅРёСЏ\n---\n\n- Windows\n- Python 3.7 Рё РІС‹С€Рµ. РљР°С‚Р°Р»РѕРіРё РёРЅС‚РµСЂРїСЂРµС‚Р°С‚РѕСЂР° Рё СЃРєСЂРёРїС‚РѕРІ Python РґРѕР»Р¶РЅС‹ Р±С‹С‚СЊ РїСЂРѕРїРёСЃР°РЅС‹ РІ РїРµСЂРµРјРµРЅРЅРѕР№ РѕРєСЂСѓР¶РµРЅРёСЏ Path\n- РџР°РєРµС‚ [parse-1c-build][1] СЃ РЅРµРѕР±С…РѕРґРёРјС‹РјРё РЅР°СЃС‚СЂРѕР№РєР°РјРё\n\n[1]: https://github.com/Cujoko/parse-1c-build\n',
    'author': 'Cujoko',
    'author_email': 'cujoko@gmail.com',
    'url': 'https://github.com/Cujoko/diff-1c',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
