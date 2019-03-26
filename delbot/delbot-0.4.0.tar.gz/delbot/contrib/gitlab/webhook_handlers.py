from dateutil.parser import parse as parse_date
from delbot.webhooks import handlers
from django.utils.text import slugify


def create_issue(attrs, project, labels, db):
    if attrs.get('confidential'):
        return

    db.create(
        'blog.post',
        {
            'source': 'gitlab',
            'title': attrs['title'],
            'remote_id': attrs['id'],
            'published': parse_date(attrs['created_at']),
            'body': attrs['description'],
            'level': 'warning',
            'categories': db.create(
                'blog.category',
                {
                    'name': project['name'],
                    'slug': project['path_with_namespace'].split('/')[-1]
                },
                update_on='slug'
            ),
            'tags': [
                db.create(
                    'blog.tag',
                    {
                        'name': label['title'].capitalize(),
                        'slug': slugify(label['title'])
                    },
                    update_on='slug'
                ) for label in labels
            ]
        }
    )


def update_issue(attrs, project, labels, db):
    if not attrs.get('confidential'):
        add_child = False

        try:
            post = db.latest(
                'blog.post',
                source='gitlab',
                remote_id=attrs['id']
            )
        except db.ObjectNotFound:
            return

        already_closed = post['level'] == 'success'
        current_state = attrs['state']

        if current_state == 'closed' and not already_closed:
            add_child = True
        elif current_state == 'opened' and already_closed:
            add_child = True

        db.update(
            'blog.post',
            {
                'level': attrs['state'] == 'closed' and 'success' or 'warning',
                'tags': [
                    db.create(
                        'blog.tag',
                        {
                            'name': label['title'].capitalize(),
                            'slug': slugify(label['title'])
                        },
                        update_on='slug'
                    ) for label in labels
                ]
            },
            source='gitlab',
            remote_id=attrs['id']
        )

        if add_child:
            db.create(
                'blog.post',
                {
                    'source': 'gitlab',
                    'title': 'Status set to %(state)s' % attrs,
                    'published': parse_date(attrs['updated_at']),
                    'parent': db.ref(
                        'blog.post',
                        source='gitlab',
                        remote_id=attrs['id']
                    )
                }
            )


def create_comment(attrs, issue, db):
    if not issue.get('confidential'):
        return db.create(
            'blog.post',
            {
                'source': 'gitlab',
                'title': attrs['note'],
                'remote_id': attrs['id'],
                'body': attrs.get('description'),
                'published': parse_date(attrs['created_at']),
                'parent': db.ref(
                    'blog.post',
                    source='gitlab',
                    remote_id=issue['id']
                )
            }
        )


@handlers.register('gitlab')
def gitlab(data, db):
    kind = data.get('object_kind')
    attrs = data.get('object_attributes', {})
    project = data.get('project', {})
    labels = data.get('labels', [])
    action = attrs.get('action')

    if kind == 'issue':
        if action == 'update':
            update_issue(attrs, project, labels, db)
        elif action == 'open':
            create_issue(attrs, project, labels, db)
    elif kind == 'note':
        issue = data.get('issue', {})
        create_comment(attrs, issue, db)
