import copy
import importlib
import operator
import os
import six

VALID_SECTIONS = ['default', 'development', 'test', 'homolog', 'staging', 'production']


class SettingsMeta(type):

    def __new__(meta, name, bases, attrs):

        _declared_options = {}

        base_options = meta.fetch_base_options(bases)

        # subclass declared options
        _explicit_options = {key: value for key, value in attrs.items() if key.isupper()}

        _declared_options.update(base_options)

        _declared_options.update(_explicit_options)

        API_ENV = _declared_options.get('API_ENV')

        #  Subclass config files  has higher priority
        config_files = attrs.get('_config_files', [])

        # configuration options from configuration files
        file_options = meta.load_config_from_files(API_ENV, config_files)

        # build current class's all declared configuration options including all superclass
        # base_options.update(attrs)

        # override class's declared options with file configuration with validation also
        for key, value in file_options.items():
            print('file options:', key, value, '\n')
            setting_key = key.upper()
            if setting_key not in _declared_options:
                raise Exception('Configuration field {} should be declared in {} class'.format(setting_key, name))

            if value.startswith('$'):
                value = os.environ.get(value[1:], None)

            if value.isnumeric():
                value = int(value)
            else:
                try:
                    value = float(value)
                except ValueError:
                    pass

            _explicit_options[setting_key] = value

        _declared_options.update(_explicit_options)

        # If subclass overload superclass's attribute, update super class
        for key, value in _declared_options.items():
            if not key.isupper():
                continue
            for base in bases:
                setattr(base, key, value)

        print(_declared_options)
        attrs.update(_declared_options)

        return super(SettingsMeta, meta).__new__(meta, name, bases, attrs)

    @classmethod
    def is_overload(cls, setting: str = None, base_settings: dict = None):
        return setting in base_settings

    @classmethod
    def fetch_base_options(cls, bases):
        base_config_attributes = {}
        for base in bases:
            base_config_attributes.update({key: value for key, value in base.__dict__.items() if key.isupper()})
        return base_config_attributes

    @classmethod
    def load_config_from_files(cls, env_name, files):
        from configparser import ConfigParser
        global_config = {}
        config = ConfigParser()
        for filename in files:
            config.read(filename)
            for section in config.sections():
                if section not in VALID_SECTIONS:
                    raise Exception('Invalid section {} in  {}'.format(section, filename))

            default_section = dict(config.items('default')) if config.has_section('default') else {}
            env_name_section = dict(config.items(env_name)) if config.has_section(env_name) else {}
            global_config.update(default_section)
            global_config.update(env_name_section)
        return global_config


class DefaultSettings(six.with_metaclass(SettingsMeta)):
    """
    Default project global scope
    """
    _config_files = []

    API_ENV = os.environ.get('API_ENV', 'development')

    # API return data related configuration
    API_DEFAULT_LIMIT = 20
    API_MAXIMUM_LIMIT = 100

    ############################################################
    # Mongo Database configuration template
    ############################################################
    MONGODB_URI = 'localhost:27017'
    DB_NAME = 'default_db'
    COLLECTION_NAME = 'default'

    @classmethod
    def mongo_config_for_collection(cls, collection_name: str = None):
        """
        Return a configuration object of MongoDBManager for given collection_name
        If collection_name in any configuration file then use the configured collection_name
        Else use the given collection_name instead
        """
        if collection_name is None:
            collection_name = cls.COLLECTION_NAME

        if not getattr(cls, collection_name, False):
            collection_name = collection_name
        else:
            collection_name = getattr(cls, collection_name)
        return {
            'MONGODB_URI': cls.MONGODB_URI,
            'DB_NAME': cls.DB_NAME,
            'COLLECTION_NAME': collection_name
        }

    ############################################################
    # AWS service configuration
    ############################################################
    AWS_REGION = 'us-west-2'
    BUCKET_NAME = None

    @classmethod
    def aws_config(cls):
        """
        Return aws's configuration from environment variable 'API_ENV'
        """
        return {
            'AWS_REGION': cls.AWS_REGION,
            'BUCKET_NAME': cls.BUCKET_NAME
        }


############################################################
# Lazy Settings style adapted from  Django
############################################################

API_SETTINGS_MODULE_ENVIRONMENT_VARIABLE = 'API_SETTINGS_MODULE'
empty = object()


def new_method_proxy(func):
    def inner(self, *args):
        if self._wrapped is empty:
            self._setup()
        return func(self._wrapped, *args)

    return inner


def unpickle_lazyobject(wrapped):
    """
    Used to unpickle lazy objects. Just return its argument, which will be the
    wrapped object.
    """
    return wrapped


class LazyObject:
    _wrapped = None

    def __init__(self):
        self._wrapped = empty

    __getattr__ = new_method_proxy(getattr)

    def __setattr__(self, name, value):
        if name == '_wrapped':
            self.__dict__['_wrapped'] = value
        else:
            if self._wrapped is empty:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == '_wrapped':
            raise TypeError("can't delete _wrapped")
        if self._wrapped is empty:
            self._setup()

        delattr(self._wrapped, name)

    def _setup(self):
        raise NotImplementedError('subclass of LazyObject must provide a _setup() method')

    def __reduce__(self):
        if self._wrapped is empty:
            self._setup()
        return (unpickle_lazyobject, (self._wrapped))

    def __copy__(self):
        if self._wrapped is empty:
            return type(self)()
        else:
            return copy.copy(self._wrapped)

    def __deepcopy__(self, memodict=None):
        if self._wrapped is empty:
            result = type(self)()
            memodict[id(self)] = result
            return result
        return copy.deepcopy(self._wrapped, memodict)

    # Introspection support
    __dir__ = new_method_proxy(dir)

    # Need to pretend to be the wrapped class, for the sake of objects that
    # care about this (especially in equality tests)
    __class__ = property(new_method_proxy(operator.attrgetter("__class__")))
    __eq__ = new_method_proxy(operator.eq)
    __ne__ = new_method_proxy(operator.ne)
    __hash__ = new_method_proxy(hash)

    # List/Tuple/Dictionary methods support
    __getitem__ = new_method_proxy(operator.getitem)
    __setitem__ = new_method_proxy(operator.setitem)
    __delitem__ = new_method_proxy(operator.delitem)
    __iter__ = new_method_proxy(iter)
    __len__ = new_method_proxy(len)
    __contains__ = new_method_proxy(operator.contains)


class Settings:
    def __init__(self, settings_module):

        # Configuration from Default settings
        for setting in dir(DefaultSettings):
            if setting.isupper():
                self.__dict__[setting] = getattr(DefaultSettings, setting)
                setattr(self, setting, getattr(DefaultSettings, setting))

        self.SETTINGS_MODULE = settings_module

        setting_module = importlib.import_module(self.SETTINGS_MODULE)
        setting_class = getattr(setting_module, 'Settings')

        self._explicit_settings = set()
        for setting in dir(setting_class):
            if setting.isupper():
                setting_value = getattr(setting_class, setting)
                setattr(self, setting, setting_value)
                self._explicit_settings.add(setting)

    def __repr__(self):
        return '<{cls} {setting_module} >'.format(
            **{'cls': self.__class__.__name__, 'setting_module': self.SETTINGS_MODULE})


class UserSettingsHolder:
    SETTINGS_MODULE = None

    def __init__(self, default_settings_class):
        self.__dict__['_deleted'] = set()
        self.default_settings_class = default_settings_class

    def __getattr__(self, name):
        if name in self._deleted:
            raise AttributeError
        return getattr(self.default_settings_class, name)

    def __delattr__(self, name):
        self._deleted.add(name)
        if hasattr(self, name):
            super().__delattr__(name)

    def __dir__(self):
        return sorted(
            s for s in list(self.__dict__) + dir(self.default_settings_class) if s not in self._delete
        )

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)


class LazySettings(LazyObject):

    def _setup(self, name=None):
        settings_model = os.environ.get(API_SETTINGS_MODULE_ENVIRONMENT_VARIABLE)
        if not settings_model:
            desc = ('setting {}'.format(name if name else 'settings'))
            raise Exception(
                "Requested {}, but settings are not configured. "
                "You must either define the environment variable {} "
                "or call settings.configure() before access settings".format(desc,
                                                                             API_SETTINGS_MODULE_ENVIRONMENT_VARIABLE)
            )
        self._wrapped = Settings(settings_model)

    def __repr__(self):
        if self._wrapped is empty:
            return '<LazySettings [Unevaluated]>'
        return '<LazySettings "{}" >'.format(self._wrapped.SETTINGS_MODULE)

    def __getattr__(self, name):
        if self._wrapped is empty:
            self._setup(name)
        val = getattr(self._wrapped, name)
        self.__dict__[name] = val
        return val

    def __setattr__(self, name, value):
        if name == '_wrapped':
            self.__dict__.clear()
        else:
            self.__dict__.pop(name, None)
        super().__setattr__(name, value)

    def __delattr__(self, name):
        super().__delattr__(name)
        self.__dict__.pop(name, None)

    # def __dir__(self):
    #     return sorted(s for s in list(self.__dict__) + dir(self._wrapped))

    def configure(self, default_settings_class=DefaultSettings, **options):
        if self._wrapped is empty:
            raise RuntimeError('Settings already configured.')
        holder = UserSettingsHolder(default_settings_class)
        for name, value in options.items():
            setattr(holder, name, value)
        self._wrapped = holder

    @property
    def configured(self):
        return self._wrapped is not empty

# settings = LazySettings()
