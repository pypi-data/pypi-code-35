from interlegis.portalmodelo.policy.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile
from plone import api

import logging

PROFILE_ID = 'interlegis.portalmodelo.policy:default'
PRODUCTS = ('sc.social.like')

def apply_configurations(context):
    """Atualiza perfil para versao 5."""
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-interlegis.portalmodelo.policy.upgrades.v5:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 5')

    q_i = api.portal.get_tool(name='portal_quickinstaller')

    for up in PRODUCTS:
        if q_i.isProductInstalled(up):
            q_i.uninstallProducts([up])
    logger.info('Desinstalando produto de Social Like para evitar conflitos')

    if not q_i.isProductInstalled('sc.social.like'):
        q_i.installProduct('sc.social.like')
    logger.info('Instalado produto de Social Like.')
