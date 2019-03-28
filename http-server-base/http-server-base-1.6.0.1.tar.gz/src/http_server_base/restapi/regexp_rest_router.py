from typing import List, Union, Dict, Type, Tuple, Any, Pattern, Callable, TypeVar, Optional

import re

from . import ArgumentListType
from . import IInRequestRouter
from . import BaseInRequestRouter

from http_server_base.tools import RegExpType, ReDict

class RegexpRestRouter(BaseInRequestRouter):
    mapper_type = ReDict
    
    @classmethod
    def get_path_regular(cls, path: str, path_args: ArgumentListType = IInRequestRouter.DEFAULT_ARG, path_regular: Union[str,Pattern[str]] = None, **kwargs) -> Tuple[RegExpType, ArgumentListType]:
        if (path_regular is None):
            _regular, path_args = super().get_path_regular(path=path, path_args=path_args, **kwargs)
        else:
            if (isinstance(path_regular, str)):
                _regular = re.compile(path_regular, flags=re.IGNORECASE)
            
            elif (isinstance(path_regular, RegExpType)):
                _regular = path_regular
            
            else:
                raise TypeError(f"uri_regular must be either str, compiled regular or None; but not {type(path_regular)}")
            
            if (path_args == cls.DEFAULT_ARG):
                path_args = None
        
        return _regular, path_args
    
    @classmethod
    def get_path_key(cls, *, path: str, **kwargs):
        regexp, _ = cls.get_path_regular(path, **kwargs)
        return regexp
