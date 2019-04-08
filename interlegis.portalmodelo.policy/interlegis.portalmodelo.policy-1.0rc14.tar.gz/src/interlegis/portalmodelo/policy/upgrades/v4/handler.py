# -*- coding:utf-8 -*-
from interlegis.portalmodelo.policy.config import CREATORS
from interlegis.portalmodelo.policy.config import PROJECTNAME
from interlegis.portalmodelo.policy.utils import _add_id
from plone.app.upgrade.utils import loadMigrationProfile
from plone import api

import logging

PROFILE_ID = 'interlegis.portalmodelo.policy:default'

def apply_configurations(context):
    """Atualiza perfil para versao 4."""
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-interlegis.portalmodelo.policy.upgrades.v4:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 4')

    site = api.portal.getSite()

    SITE_STRUCTURE = [
        dict(
            type='Link',
            title=u'Caderno de Exercícios',
            description=u'Link para o arquivo PDF do Caderno de Exercícios do Portal Modelo 3, utilizado nas oficinas. (este link é apenas uma referência, está privado e pode ser removido)',
            remoteUrl='http://ftp.interlegis.leg.br/interlegis/produtos/portalmodelo/versao3.0/docs/Caderno%20de%20exercicios%20PORTAL%20MODELO%203%C2%AA%20edi%C3%A7%C3%A3o-%20Colab.pdf',
            _transition=None,
        ),
    ]
    SITE_STRUCTURE = _add_id(SITE_STRUCTURE)
    for item in SITE_STRUCTURE:
        id = item['id']
        title = item['title']
        description = item.get('description', u'')
        if id not in site:
            if 'creators' not in item:
                item['creators'] = CREATORS
            obj = api.content.create(site, **item)
            obj.setTitle(title)
            obj.setDescription(description)
            obj.reindexObject()
            logger.debug(u'    {0} criado e publicado'.format(title))
        else:
            logger.debug(u'    pulando {0}; conteúdo existente'.format(title))


