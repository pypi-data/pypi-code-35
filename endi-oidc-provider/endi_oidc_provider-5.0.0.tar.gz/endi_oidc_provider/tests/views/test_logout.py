# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def test_logout_view():
    from autonomie_oidc_provider.views.logout import logout_view
    # TODO : test redirect_uri + no redirect
