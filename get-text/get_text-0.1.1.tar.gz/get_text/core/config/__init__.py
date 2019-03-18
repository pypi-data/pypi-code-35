"""Класс Config - дает доспуп к настройкам (юзера/по умолчаниии) для парсера."""

from get_text.core.config.config import DEFAULT_CONFIG
from get_text.core.config.template import DEFAULT_TEMPLATE_NEWS


class Config:
    settings = DEFAULT_CONFIG
    site_host = ''

    def __init__(self, site_host, settings=None):
        self.site_host = site_host
        if isinstance(settings, dict):
            sites = settings.pop('sites', {})
            self.settings.update(**settings)
            self.settings['sites'].update(**sites)

    @property
    def sites(self):
        return self.settings['sites']

    def __getitem__(self, item):
        if self.site_host in self.sites:
            if item in self.sites[self.site_host]:
                return self.sites[self.site_host][item]

        return self.settings.get(item)
