# !/usr/bin/env python
import datetime
import inspect
from task import models
import public
import task


@public.add
class Task:
    """base class for a Task model. attrs: `name`, `category`, `description`, `disabled`. methods: `complete()`, `update()`. properties: `completed_at`. not implemented: `todo()`, ..."""
    name = None
    category = None
    description = None
    disabled = False

    def __init__(self, **kwargs):
        self.started_at = datetime.datetime.now()
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def module_name(self):
        return self.__class__.__module__

    @property
    def class_name(self):
        return self.__class__.__name__

    def run(self):
        path = "%s.%s" % (self.module_name, self.class_name)
        raise NotImplementedError('%s.run() is not implemented' % path)

    def todo(self):
        path = "%s.%s" % (self.module_name, self.class_name)
        raise NotImplementedError('%s.todo() is not implemented' % path)

    def getobject(self):
        """return Task model object for this class"""
        kwargs = dict(
            name=self.name,
            module_name=self.module_name,
            class_name=self.class_name
        )
        try:
            return models.Task.objects.get(**kwargs)
        except models.Task.DoesNotExist:
            pass

    def update(self):
        """create/update model record fields: `name`, `category`, `disabled`, `todo`, `updated_at`"""
        kwargs = dict(
            name=self.name,
            module_name=self.module_name,
            class_name=self.class_name
        )
        record, created = models.Task.objects.get_or_create(**kwargs)
        todo = self.todo
        record.todo = bool(todo()) if todo and inspect.isroutine(todo) else bool(todo)
        record.name = self.name
        record.disabled = self.disabled
        record.category = self.category
        record.updated_at = datetime.datetime.now()
        record.save()

    @property
    def completed_at(self):
        task = self.getobject()
        if task:
            return task.completed_at

    def complete(self):
        task = self.getobject()
        now = datetime.datetime.now()
        if not hasattr(self, "started_at"):
            task.started_at = now
        task.updated_at = now
        task.completed_at = now
        task.todo = False
        task.save()

    def __str__(self):
        return '<Task name="%s">' % (self.name)


@public.add
def getclasses():
    """return a list of Task subclasses"""
    classes = []
    for module in task.getmodules():
        for k, v in module.__dict__.items():
            if inspect.isclass(v) and issubclass(v, Task):
                classes.append(v)
    return classes


@public.add
def update():
    """create/update all tasks"""
    for cls in getclasses():
        cls().update()
