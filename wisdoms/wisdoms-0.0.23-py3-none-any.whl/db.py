# Created by Q-ays.
# whosqays@gmail.com

# Have to install sqlalchemy

from sqlalchemy.exc import SQLAlchemyError
import traceback


def session_exception(session, is_raise=True):
    def wrapper(func):

        def catch(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except SQLAlchemyError as e:
                # print(e)
                print('~~~~~~~~~~~~~~~~session error~~~~~~~~~~~~~~~~~~')
                traceback.print_exc()
                session.rollback()
                if is_raise:
                    raise e

        return catch

    return wrapper


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


def o2d(obj):
    """
    把对象(支持单个对象、list、set)转换成字典
    :param obj: obj, list, set
    :return:
    """
    is_list = isinstance(obj, list)
    is_set = isinstance(obj, set)

    if is_list or is_set:
        obj_arr = []
        for o in obj:
            if o:
                obj_arr.append(o.to_dict())
        return obj_arr
    else:
        return obj.to_dict()


def repo_ref(session0):
    class RepoBase:
        def __init__(self, Model=None):
            self.session = session0
            self.Model = Model

        def add(self, data):
            model0 = self.Model(**data)

            self.session.add(model0)
            self.session.commit()

            return model0

        def delete(self, did):
            repo = self.session.query(self.Model).get(did)

            self.session.delete(repo)
            self.session.commit()

            return repo

        def update(self, did, data):
            model0 = self.get(did)

            columns = model0.__table__.columns

            for col in columns:
                name = col.name
                value = data.get(name, None)

                if value and not col.primary_key:
                    print(name)
                    setattr(model0, name, value)

            self.session.commit()

            return model0

        def get(self, did=None, **kwargs):
            if did:
                repos = self.session.query(self.Model).get(did)
            elif kwargs:
                repos = self.session.query(self.Model).filter_by(**kwargs).all()
            else:
                repos = self.session.query(self.Model).all()

            return repos

    return RepoBase
