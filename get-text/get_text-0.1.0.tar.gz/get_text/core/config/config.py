"""Дефолнтая настройка.

Полезная информация - текст

DEFAULT_CONFIG:
    width: Ширина строки
    file_type: Тип файла который на выход даст парсер (пока только txt)
    show_link: Показывать ли ссылки в тексте
    template: Шаблон на который "натянется" и сохранится полученные данные
    exclude_elements: Элементы которые должны будут удалиться до получение
                                                            данных со страницы
        class: список классов, если перечисленный класс есть у какого
                                            либо тега - этот тег парсер удалить
        tags: как и классы, но теперь тут название самих тегов - которые должны
                                                                  будут удалены
        id: список id тегов которые буду удалены
        css_selectors: css селекторы которые будут удалены
    general: общие для всех сайтов правилы на получении заголовка и текста
        title: Заголовок
            tags: список тегов потенциальные на звание заголовка
        content: Текст
            tags: теги которые будут считаться текстом
    sites: Список сайтов на которые были "хардкодно" указаны css селекторы
                        по которым можно получить заголовк и информации с сайта
        title: css селектор заголовка информации
        content: css селектор самого текста

"""

from .template import DEFAULT_TEMPLATE_NEWS

DEFAULT_CONFIG = {
    "width": 80,
    "file_type": 'txt',
    "show_link": False,
    "template": DEFAULT_TEMPLATE_NEWS,
    "exclude_elements": {
            'class': [
                'header',
                'footer',
                'nav',
                'menu',
                'push',
                'socials',
                'sharing',
                'topics',
                '^hidden$'
                'hidden',
                'banner',
                '^ad$',
                'sidebar',
                'footer',
                'sidebars',
            ],
            'css_selectors': [
                'div.hidden'
            ],
            'tags': [
                'nav',
                'footer',
                'iframe',
                'canvas',
                '^header$',
                'footer',
            ],
            'id': ['footer', '^header', 'header'],
        },
    "general": {
        'title': {
            'tags': ['h1'],
        },
        'content': {
            'tags': ['p', 'span'],
        },
    },
    'sites': {
        '1tv.ru': {
            'title': 'h1.title',
            'content': 'div.w_row>div>div',
        },
        'habr.com': {
            'title': 'h1.post__title.post__title_full',
            'content': 'div.post__text',
        },
    }

}




