# -*- coding: utf-8 -*-


def test_user_info_view(app, oidc_client, oidc_token, user):
    headers = [
        [
            'Authorization',
            'Bearer %s' % oidc_token.access_token,
        ]
    ]
    resp = app.post('/userinfo', headers=headers)
    assert resp.status_int == 200
    assert resp.json['email'] == user.email
    assert resp.json['user_id'] == user.id
    assert resp.json['sub'] == user.id
