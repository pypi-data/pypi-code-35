from pyquilted.quilted.detail import *


class DetailFactory:
    """Detail factory creates detail objects"""
    @staticmethod
    def create(key, data):
        detail = None
        if key == 'title':
            detail = Title(**data)
        elif key == 'location':
            detail = Location(**data)
        elif key == 'objective':
            detail = Objective(**data)
        elif key == 'flair':
            detail = Flair(**data)

        return detail
