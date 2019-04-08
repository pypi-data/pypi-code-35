"""
Functions for access control.
"""


def staff(request):
    """For employers and superusers."""
    user = request.user
    return user.is_staff or user.is_superuser


def superuser(request):
    """For superusers only."""
    return request.user.is_superuser
