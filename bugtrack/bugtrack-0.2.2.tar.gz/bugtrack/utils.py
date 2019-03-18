from django.conf import settings
from django.contrib.auth.models import User

from .models import Category
from .workflows import BUGTRACK_WORKFLOW

def get_next_statuses(bug, next_state=False):
    statuses = BUGTRACK_WORKFLOW
    state = bug.bugstatus.code
    print('1')
    if state in statuses:
        print('2')
        if next_state:
            print('3')
            return next_state in statuses[state]
        else:
            return [st for st in statuses[state]]
    else:
        return False


def get_accessible_categories(user):
    top_categories = Category.objects.filter(parent__isnull=True)
    categories = []
    for top_category in top_categories:
        categories.append(top_category)
        categories.extend(top_category.get_children_tree())
    return [cat.id for cat in categories if cat.has_access(user)]


def get_accessible_categories_ro(user):
    top_categories = Category.objects.filter(parent__isnull=True)
    categories = []
    for top_category in top_categories:
        categories.append(top_category)
        categories.extend(top_category.get_children_tree())
    return [cat.id for cat in categories if cat.has_access_ro(user)]


def get_user_list():
    try:
        user_selection_query = settings.BUGTRACK['user_selection_query']
        return User.objects.filter(**user_selection_query)
    except:
        return User.objects.filter()