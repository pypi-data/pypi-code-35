from dateutil.parser import parse as parse_date
from delbot.webhooks import handlers
from django.utils.text import slugify
from django.utils.timezone import utc


@handlers.register('pingdom')
def pingdom(data, db):
    service = data['check_name']
    state = data['current_state']
    importance_level = data['importance_level']

    db.create(
        'blog.post',
        {
            'title': '%s is %s' % (
                service,
                state.lower()
            ),
            'body': data['long_description'],
            'level': {
                'DOWN': 'danger',
                'UP': 'success'
            }[state],
            'published': parse_date(
                data['state_changed_utc_time']
            ).replace(tzinfo=utc),
            'categories': db.create(
                'blog.category',
                {
                    'name': service,
                    'slug': slugify(service)
                },
                update_on='slug'
            ),
            'tags': [
                db.create(
                    'blog.tag',
                    {
                        'name': 'Outages',
                        'slug': 'outages'
                    },
                    update_on='slug'
                ),
                db.create(
                    'blog.tag',
                    {
                        'name': importance_level.capitalize(),
                        'slug': slugify(importance_level)
                    },
                    update_on='slug'
                )
            ]
        }
    )
