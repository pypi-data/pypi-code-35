#!/usr/bin/env python
import jsfiddle
import markdown_table
import os
import public


@public.add
class Readme:
    """README.md class. methods: `render`, `save(path)`"""

    @property
    def details(path):
        return jsfiddle.details.load()

    def resources_table(self):
        resources = self.details.get("resources", [])
        if not resources:
            return ""
        matrix = []
        for url in resources:
            left = "`%s`" % os.path.basename(url)
            right = "[%s](%s)" % (url, url)
            matrix.append([left, right])
        return markdown_table.render(["filename", "url"], matrix)

    def details_table(self):
        matrix = []
        name = self.details.get("name", os.path.basename(os.getcwd()))
        matrix = [['name', name]]
        description = self.details.get("description", "").strip()
        if len(description) > 1:
            matrix.append(['description', description])
        return markdown_table.render(["key", "value"], matrix)

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
            self.details_table()
            sections.append("""###### Details
%s""" % self.details_table())
        resources_table = self.resources_table()
        if resources_table:
            sections.append("""###### Resources
%s""" % resources_table)
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
