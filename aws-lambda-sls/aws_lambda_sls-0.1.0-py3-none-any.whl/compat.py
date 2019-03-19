import socket
import six
import os


def pip_import_string():
    import pip
    pip_major_version = pip.__version__.split('.')[0]
    # Pip moved its internals to an _internal module in version 10.
    # In order to be compatible with version 9 which has it at at the
    # top level we need to figure out the correct import path here.
    if pip_major_version == '9':
        return 'from pip import main'
    else:
        return 'from pip._internal import main'


if os.name == 'nt':
    # windows
    # This is the actual patch used on windows to prevent distutils from
    # compiling C extensions. The msvc compiler base class has its compile
    # method overridden to raise a CompileError. This can be caught by
    # setup.py code which can then fallback to making a pure python
    # package if possible.
    # We need mypy to ignore these since they are never actually called from
    # within our process they do not need to be a part of our typechecking
    # pass.
    def prevent_msvc_compiling_patch():  # type: ignore
        import distutils
        import distutils._msvccompiler
        import distutils.msvc9compiler
        import distutils.msvccompiler

        from distutils.errors import CompileError

        def raise_compile_error(*args, **kwargs):  # type: ignore
            raise CompileError('Pysls blocked C extension compiling.')
        distutils._msvccompiler.MSVCCompiler.compile = raise_compile_error
        distutils.msvc9compiler.MSVCCompiler.compile = raise_compile_error
        distutils.msvccompiler.MSVCCompiler.compile = raise_compile_error

    # This is the setuptools shim used to execute setup.py by pip.
    # Lines 2 and 3 have been added to call the above function
    # `prevent_msvc_compiling_patch` and extra escapes have been added on line
    # 5 because it is passed through another layer of string parsing before it
    # is executed.
    _SETUPTOOLS_SHIM = (
        r"import setuptools, tokenize;__file__=%r;"
        r"from aws_lambda_sls.compat import prevent_msvc_compiling_patch;"
        r"prevent_msvc_compiling_patch();"
        r"f=getattr(tokenize, 'open', open)(__file__);"
        r"code=f.read().replace('\\r\\n', '\\n');"
        r"f.close();"
        r"exec(compile(code, __file__, 'exec'))"
    )
    pip_no_compile_c_shim = (
        'import pip;'
        'pip.wheel.SETUPTOOLS_SHIM = """%s""";'
    ) % _SETUPTOOLS_SHIM
    pip_no_compile_c_env_vars = {}
else:
    pip_no_compile_c_shim = ''
    pip_no_compile_c_env_vars = {
        'CC': '/var/false'
    }


if six.PY3:
    from urllib.parse import urlparse, parse_qs
    lambda_abi = 'cp36m'

    def is_broken_pipe_error(error):
        return isinstance(error, BrokenPipeError)  # noqa
else:
    from urlparse import urlparse, parse_qs
    lambda_abi = 'cp27mu'

    def is_broken_pipe_error(error):
        # type: (Exception) -> bool

        # In python3, this is a BrokenPipeError. However in python2, this
        # is a socket.error that has the message 'Broken pipe' in it. So we
        # don't want to be assuming all socket.error are broken pipes so just
        # check if the message has 'Broken pipe' in it.
        return isinstance(error, socket.error) and 'Broken pipe' in str(error)


def to_unicode(s, encoding='utf-8', errors='strict'):
    if six.PY2:
        return s if isinstance(s, unicode)\
               else s.decode(encoding, errors=errors)
    else:
        return s if isinstance(s, six.string_types)\
               else s.decode(encoding, errors=errors)


def to_byte(s, encoding='utf-8', errors='strict'):
    if six.PY2:
        return s.encode(encoding, errors=errors)\
               if isinstance(s, unicode) else s
    else:
        return s.encode(encoding, errors=errors)\
               if isinstance(s, six.string_types) else s
