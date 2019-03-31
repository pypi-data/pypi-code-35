from schevo.schema import *
schevo.schema.prep(locals())

from notmm.utils.decorators import permalink
from markdown2 import markdown, MarkdownError

class SchevoIcon(E.Entity):

    _hidden = True

    name = f.string()
    data = f.image()

    _key(name)

class Category(E.Entity):
    name = f.string()
    description = f.string(required=False)
    slug = f.string(required=False)

    _key(name)
    _plural = "Categories"

    def x_as_slug(self):
        
        if self.slug:
            slug = self.slug
        else:
            slug = self.name.replace(' ', '-').lower()

        return str(slug)

class Comment(E.Entity):
    author = f.entity('Author')
    #TODO support more flexible content/object types...
    blogentry = f.entity('BlogEntry')
    message = f.string(multiline=True)
    published = f.boolean(required=False, default=False)
    pub_date = f.datetime()

    _key(author, blogentry)

class Author(E.Entity):
    name = f.string()
    # TODO: add a emailstring() method to support e-mail bytestrings in utf8
    email = f.string(required=False)
    homepage = f.string(required=False)
    twitter_username = f.string(required=False)

    _key(name)

    #def x_blogentries(self):
    #    return [casting.movie
    #            for casting in self.m.movie_castings()]

class Tag(E.Entity):

    name = f.string()
    blogentry = f.entity('BlogEntry')
    #description = f.string(required=False)

    _key(name, blogentry)

class BlogEntry(E.Entity):

    title = f.string()
    pub_date = f.datetime()
    author = f.entity('Author')
    category = f.entity('Category', required=False)
    short_description = f.string(multiline=False, required=False, default='')
    
    # TODO: add markdown or textile support here
    body = f.string(multiline=True)
    # /path/to/filename.rst 
    source = f.path(required=False)
    
    #Need a f.multiplechoices field type!
    #source_type = f.string(
    #    preferred_values=('rest', 'html', 'text'),
    #    required=False)
    
    published = f.boolean(required=False, default=False)
    slug = f.string(required=False)

    _key(title)
    _plural = "Blog Entries"

    def x_comments(self):
        return [(comment.author, 
        comment.message) for comment in self.m.comments()]

    def x_tags(self):
        return [tag for tag in self.m.tags()]

    def __unicode__(self):
        return '%s: %s' % (self.author, self.title)

    #### public methods

    @permalink
    def get_absolute_url(self):
        # returns the canonical URL representation for this post
        
        category_slug = self.category.x.as_slug()
        return ('blogengine.views.details', (), dict(
            category=category_slug, 
            slug=self.slug))
    
    def convert_to_html(self, name='body'):
        """ convert to html with markdown """
        # XXX: support other wiki-like converters
        try:
            s = getattr(self, name)
            # Can only convert strings, not _UNASSIGNED or None fields.. 
            if isinstance(s, str):
                html = markdown(s)
            else:
                html = ''
        except (MarkdownError, AttributeError) as e:
            # Error converting the document to html
            raise e

        return html
