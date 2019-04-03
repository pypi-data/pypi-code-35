class NamespaceMiddleware(object):
    def before(self, ctx):
        ctx.ns = ctx.request.env.get('HTTP_DRONGO_NAMESPACE')
