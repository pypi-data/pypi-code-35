"""Middleware tests"""
import pytest


@pytest.mark.parametrize("is_enabled", [True, False])
@pytest.mark.parametrize("is_anonymous", [True, False])
@pytest.mark.parametrize(
    "path, allowed_regexes, denied_regexes, should_redirect",
    [
        ("/allowed", [], [], False),
        ("/allowed", [r"^/allowed"], [], False),
        ("/allowed/nested", [r"^/allowed"], [], False),
        ("/denied", [r"^/allowed"], [], True),
        ("/allowed", [], [r"^/allowed"], True),
        ("/allowed/nested", [], [r"^/allowed"], True),
        ("/denied", [], [r"^/allowed"], False),
        ("/allowed", [r"^/allowed"], [r"^/allowed/nested"], False),
        ("/allowed/nested", [r"^/allowed"], [r"^/allowed/nested"], True),
    ],
)
def test_redirect_middleware(
    settings,
    rf,
    mocker,
    is_enabled,
    is_anonymous,
    path,
    allowed_regexes,
    denied_regexes,
    should_redirect,
):  # pylint: disable=too-many-arguments
    """Test that the middleware redirects correctly"""
    settings.MITXPRO_CORE_REDIRECT_LOGIN_URL = "/login"
    settings.MITXPRO_CORE_REDIRECT_ENABLED = is_enabled
    settings.MITXPRO_CORE_REDIRECT_ALLOW_RE_LIST = allowed_regexes
    settings.MITXPRO_CORE_REDIRECT_DENY_RE_LIST = denied_regexes

    from mitxpro_core.middleware import RedirectAnonymousUsersToLoginMiddleware

    should_redirect = should_redirect and is_enabled and is_anonymous

    mock_get_response = mocker.Mock()

    middleware = RedirectAnonymousUsersToLoginMiddleware(mock_get_response)

    request = rf.get(path)
    request.user = mocker.Mock(is_anonymous=is_anonymous)
    response = middleware(request)

    if should_redirect:
        mock_get_response.assert_not_called()
        assert response.status_code == 302
        assert response.url == settings.MITXPRO_CORE_REDIRECT_LOGIN_URL
    else:
        mock_get_response.assert_called_once_with(request)
