#!/usr/bin/env python
import jsfiddle
import os
import public


@public.add
class Readme:
    """README.md class. methods: `render`, `save(path)`"""

    @property
    def details(path):
        return jsfiddle.details.load()

    @property
    def resources_table(self):
        resources = self.details.get("resources", [])
        if not resources:
            return ""
        lines = []
        for url in resources:
            lines.append("`%s`|[%s](%s)" % (os.path.basename(url), url, url))
        return """filename|url
-|-
%s""" % "\n".join(lines)

    def render(self):
        sections = ["""<!--
https://pypi.org/project/jsfiddle-readme/
-->
"""]
        url = jsfiddle.url()
        if url:
            sections.append("""###### Link
[%s](%s)""" % (url, url))
        else:
            sections.append("""###### Link
unknown (git remote required)""")
        if self.details:
            name = self.details.get("name", "unknown")
            description = self.details.get("description", "unknown")
            sections.append("""###### Details
name|value
-|-
name|%s
description|%s""" % (name, description))
        resources = self.resources_table
        if resources:
            sections.append("""###### Resources
%s""" % resources)
        return "\n\n".join(sections)

    def save(self, path=None):
        if not path:
            path = "README.md"
        dirname = os.path.dirname(path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        open(path, "w").write(str(self))

    def __str__(self):
        return self.render()
