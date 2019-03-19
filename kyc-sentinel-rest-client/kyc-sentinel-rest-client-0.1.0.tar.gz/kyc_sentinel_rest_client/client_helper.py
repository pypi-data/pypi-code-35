class BearerAuth():
    """Attaches HTTP Bearer Authentication to the given Request object."""

    def __init__(self, auth_token):
        self.auth_token = auth_token

    def __call__(self, r):
        r.headers['Authorization'] = f"Bearer {self.auth_token}"
        return r


def post_update_logs_payload(category = 'individual', datetime_format = None, **kwargs):
    
    updated_at = kwargs.get('updated_at')
    if updated_at is not None:
        updated_at = updated_at.strftime(datetime_format)
    ids = kwargs.get("ids")
    return { 'update_logs': [
              {
                  'category': category,
                  'updated_at': updated_at,
                  'ids': ids
              }
              ]
            }


