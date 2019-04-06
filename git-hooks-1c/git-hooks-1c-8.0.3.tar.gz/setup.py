# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['git_hooks_1c']

package_data = \
{'': ['*']}

install_requires = \
['cjk-commons>=3.3,<4.0', 'parse-1c-build>=5.5,<6.0']

entry_points = \
{'console_scripts': ['gh1c = git_hooks_1c.__main__:run']}

setup_kwargs = {
    'name': 'git-hooks-1c',
    'version': '8.0.3',
    'description': 'Git hooks utilities for 1C:Enterprise',
    'long_description': 'РќР°Р±РѕСЂ СѓС‚РёР»РёС‚ РґР»СЏ РїРµСЂРµС…РІР°С‚С‡РёРєРѕРІ (hooks) Git РґР»СЏ СЂР°Р±РѕС‚С‹ СЃ 1РЎ\n===\n\nР§С‚Рѕ РґРµР»Р°РµС‚\n---\n\nРџСЂРё СѓСЃС‚Р°РЅРѕРІРєРµ РїР°РєРµС‚Р° РІ РєР°С‚Р°Р»РѕРіРµ СЃРєСЂРёРїС‚РѕРІ РёРЅС‚РµСЂРїСЂРµС‚Р°С‚РѕСЂР° Python СЃРѕР·РґР°С‘С‚СЃСЏ РёСЃРїРѕР»РЅСЏРµРјС‹Р№ С„Р°Р№Р» *gh1c.exe*. РЎРјРѕС‚СЂРё СЃРїРёСЃРѕРє \nРїРѕРґРґРµСЂР¶РёРІР°РµРјС‹С… РєРѕРјР°РЅРґ РІ СЃРѕСЃС‚Р°РІРµ.\n\nРўСЂРµР±РѕРІР°РЅРёСЏ\n---\n\n- Windows\n- Python 3.7 Рё РІС‹С€Рµ. РљР°С‚Р°Р»РѕРіРё РёРЅС‚РµСЂРїСЂРµС‚Р°С‚РѕСЂР° Рё СЃРєСЂРёРїС‚РѕРІ Python РґРѕР»Р¶РЅС‹ Р±С‹С‚СЊ РїСЂРѕРїРёСЃР°РЅС‹ РІ РїРµСЂРµРјРµРЅРЅРѕР№ РѕРєСЂСѓР¶РµРЅРёСЏ Path\n- РџР°РєРµС‚С‹ virtualenv Рё virtualenvwrapper-win\n- РџР°РєРµС‚ [parse-1c-build][1] СЃ РЅРµРѕР±С…РѕРґРёРјС‹РјРё РЅР°СЃС‚СЂРѕР№РєР°РјРё\n\nРЎРѕСЃС‚Р°РІ\n---\n\n- *install.py* вЂ” СЃРєСЂРёРїС‚, СЃРѕР·РґР°СЋС‰РёР№ С…СѓРєРё РІ *.git/hooks* РїСЂРѕРµРєС‚Р°. Р—Р°РїСѓСЃРєР°РµС‚СЃСЏ РєРѕРјР°РЅРґРѕР№ *install*.\n- *uninstall.py* вЂ” СЃРєСЂРёРїС‚, СѓРґР°Р»СЏСЋС‰РёР№ С…СѓРєРё РёР· *.git/hooks* РїСЂРѕРµРєС‚Р°. Р—Р°РїСѓСЃРєР°РµС‚СЃСЏ РєРѕРјР°РЅРґРѕР№ *uninstall*.\n- *pre-commit.sample* вЂ” РѕР±СЂР°Р·РµС† hook-СЃРєСЂРёРїС‚Р°, Р·Р°РїСѓСЃРєР°СЋС‰РµРіРѕ *pre-commit-1c.bat*\n- *pre_commit.py* вЂ” СЃРєСЂРёРїС‚ РґР»СЏ СЂР°Р·Р±РѕСЂРєРё *epf*-, *erf*-, *ert*- Рё *md*-С„Р°Р№Р»РѕРІ СЃ РїРѕРјРѕС‰СЊСЋ РїР°РєРµС‚Р° \n[parse-1c-build][1] РІ РєР°С‚Р°Р»РѕРіРё, РєРѕС‚РѕСЂС‹Рµ Р·Р°С‚РµРј РґРѕР±Р°РІР»СЏСЋС‚СЃСЏ РІ РёРЅРґРµРєСЃ Рё РїРѕРјРµС‰Р°СЋС‚СЃСЏ РІ git-СЂРµРїРѕР·РёС‚РѕСЂРёР№. Р—Р°РїСѓСЃРєР°РµС‚СЃСЏ РєРѕРјР°РЅРґРѕР№ \n*pre_commit*.\n\n[1]: https://github.com/Cujoko/parse-1c-build\n',
    'author': 'Cujoko',
    'author_email': 'cujoko@gmail.com',
    'url': 'https://github.com/Cujoko/git-hooks-1c',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
