class Account:
    def __init__(self, username, skills):
        self.name = username
        self.skills = skills

    def get_skill(self, skill_name):
        try:
            return self.skills[skill_name]
        except KeyError:
            return None

    def get_total(self):
        try:
            return self.skills['total']
        except KeyError:
            return None

    def get_level(self, skill_name):
        try:
            return self.skills[skill_name].level
        except KeyError:
            return None

    def get_xp(self, skill_name):
        try:
            return self.skills[skill_name].experience
        except KeyError:
            return None

    def get_rank(self, skill_name):
        try:
            return self.skills[skill_name].rank
        except KeyError:
            return None
