import asyncio
import inspect
import functools
import typing

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

PropagatePredicate = typing.Optional[typing.Callable[[typing.Type], bool]]


class SubscriptionWrapper:

    __slots__ = ('pre_hooks', 'post_hooks')

    def __init__(self) -> None:
        self.pre_hooks: typing.Tuple[typing.Callable[..., typing.Any], ...] = ()
        self.post_hooks: typing.Tuple[typing.Callable[..., typing.Any], ...] = ()

    def add_pre_hook(self, hook: typing.Callable) -> None:
        self.pre_hooks += (hook,)

    def add_post_hook(self, hook: typing.Callable) -> None:
        self.post_hooks += (hook,)

    @classmethod
    def wrap_func(cls, class_function):
        if hasattr(class_function, '_sub_wrapper'):
            return class_function
        if asyncio.iscoroutinefunction(class_function):
            return cls._async_wrap(class_function)
        return cls._sync_wrap(class_function)

    @classmethod
    def _sync_wrap(cls, class_function):
        sub_wrapper = SubscriptionWrapper()

        @functools.wraps(class_function)
        def hook_function(*args, **kwargs):
            for pre_hook in sub_wrapper.pre_hooks:
                pre_hook(*args, **kwargs)
            result = class_function(*args, **kwargs)
            for post_hook in sub_wrapper.post_hooks:
                post_hook(*args, **kwargs)
            return result

        hook_function._sub_wrapper = sub_wrapper
        return hook_function

    @classmethod
    def _async_wrap(cls, class_function):
        sub_wrapper = SubscriptionWrapper()

        @functools.wraps(class_function)
        async def hook_function(*args, **kwargs):
            for pre_hook in sub_wrapper.pre_hooks:
                if asyncio.iscoroutinefunction(pre_hook):
                    await pre_hook(*args, **kwargs)
                else:
                    pre_hook(*args, **kwargs)
            result = await class_function(*args, **kwargs)
            for post_hook in sub_wrapper.post_hooks:
                if asyncio.iscoroutinefunction(post_hook):
                    await post_hook(*args, **kwargs)
                else:
                    post_hook(*args, **kwargs)
            return result

        hook_function._sub_wrapper = sub_wrapper
        return hook_function


class SubscribableMixinMeta(type):

    def __new__(mcs, name, bases, namespace):
        namespace['__childs__'] = []
        return super().__new__(mcs, name, bases, namespace)


class SubscribableMixin(metaclass=SubscribableMixinMeta):

    @classmethod
    def _convert_to_hooked(cls, class_function) -> None:
        if not inspect.isfunction(class_function):
            raise TypeError("You should use class funtion")
        function_name = class_function.__name__
        if not hasattr(cls, function_name):
            raise TypeError("You should use class function, that belong to this class")

        class_function = getattr(cls, function_name)
        if hasattr(class_function, '_sub_wrapper') and function_name not in cls.__dict__:
            class_function = class_function.__wrapped__
        hooked_function = SubscriptionWrapper.wrap_func(class_function)
        setattr(cls, function_name, hooked_function)
        return hooked_function

    @classmethod
    def _propagate_logic(
            cls, class_function, hook: typing.Callable,
            propagate_predicate: PropagatePredicate, propagate_method: str) -> None:
        for subclass in cls.__subclasses__():
            getattr(subclass, propagate_method)(class_function, hook, propagate_predicate)

    @classmethod
    def pre_hook(cls, class_function, hook: typing.Callable, propagate_predicate: PropagatePredicate = None) -> None:
        if propagate_predicate is None or propagate_predicate(cls):
            hooked_function = cls._convert_to_hooked(class_function)
            hooked_function._sub_wrapper.add_pre_hook(hook)  # type: ignore
        if propagate_predicate is not None:
            cls._propagate_logic(class_function, hook, propagate_predicate, 'pre_hook')

    @classmethod
    def post_hook(cls, class_function, hook: typing.Callable, propagate_predicate: PropagatePredicate = None) -> None:
        if propagate_predicate is None or propagate_predicate(cls):
            hooked_function = cls._convert_to_hooked(class_function)
            hooked_function._sub_wrapper.add_post_hook(hook)  # type: ignore
        if propagate_predicate is not None:
            cls._propagate_logic(class_function, hook, propagate_predicate, 'post_hook')
