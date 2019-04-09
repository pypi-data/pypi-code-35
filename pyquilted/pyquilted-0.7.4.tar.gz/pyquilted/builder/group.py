from pyquilted.quilted.group import Group


class GroupBuilder:
    def __init__(self, resume=None):
        self.resume = resume
        self.grouped = []

    def create(self):
        group = None
        for section in self.resume.sections:
            first = list(section.keys())[0]
            if section[first]['compact']:
                if self._last_section(section):
                    self.grouped.append(section)
                else:
                    if not group:
                        group = Group()
                    group.add_section(section)
            elif group:
                self.grouped.append(group.get_sections())
                self.grouped.append(section)
                group = None
            else:
                self.grouped.append(section)

        self._update_resume()
        return self.resume

    def _last_section(self, section):
        if(self.resume.sections.index(section)
                == len(self.resume.sections) - 1):
            return True
        return False

    def _update_resume(self):
        if len(self.grouped) < len(self.resume.sections):
            self.resume.sections = self.grouped
