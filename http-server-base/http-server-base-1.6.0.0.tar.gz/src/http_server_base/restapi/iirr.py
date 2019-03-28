from typing import List, Union, Dict, Type, Tuple, Any, Pattern, Callable, TypeVar, Optional, Generic, Collection, Iterator

from http_server_base.tools import RegExpType

from . import ArgumentType, ArgumentListType, CanonicalArgumentListType, CanonicalArgumentType, MapperFuncType
from . import IRest_RequestHandler

class IInRequestRouter():
    
    T = TypeVar('T')
    mapper_type: Generic[T] = Collection
    DEFAULT_ARG = object()
    
    @classmethod
    def remove_base_path(cls, path: str, base_path: str) -> str:
        pass
    
    @classmethod
    def get_class_mapper(cls, x: Union[Type[IRest_RequestHandler], str]) -> Dict[str, mapper_type[Any]]:
        pass
    @classmethod
    def get_mapper_func(cls, x: Union[Type[IRest_RequestHandler], str]) -> MapperFuncType:
        pass
    @classmethod
    def get_class_endpoints(cls, x: Union[Type[IRest_RequestHandler], str]) -> Iterator[Tuple[str, str]]:
        pass
    
    @classmethod
    def get_canonical_form_of_argument(cls, arg: ArgumentType) -> CanonicalArgumentType:
        """
        Extracts the argument info from the free argument description form
        :param arg:
        Either str or tuple
        Str: argument_name. Any type. No default. Mandatory
        
        Tuple:
            (argument_name): the same
            (argument_name, argument_type): No default. Mandatory.
            (argument_name, argument_types, argument_default): Optional.
        
        Where:
            argument_name: str. Can have leading '?', marking argument as an optional (None will be returned if no default). Can have '=', making everything behind it the argument_default.
            argument_types: Type or Tuple of Types. Types used for strict type checks. 'None' is any type.
            argument_default: any legal type. The default value is returned if the argument itself is missing.
        :return:
        
        Tuple:
            (argument_name:str, argument_types:Tuple[Type+], argument_default, mandatory:bool)
        
        Where:
            mandatory: True if argument is mandatory, False if optional.
        """
        
        pass
    @classmethod
    def get_canonical_form_of_argument_list(cls, args: ArgumentListType) -> CanonicalArgumentListType:
        pass
    
    @classmethod
    def get_path_regular(cls, path: str, path_args: ArgumentListType = DEFAULT_ARG, **kwargs) -> Tuple[RegExpType, ArgumentListType]:
        pass
    
    @classmethod
    def get_path_key(cls, *, path: str, **kwargs) -> str:
        pass
    
    @classmethod
    def rest_method \
    (
        cls,
        path: str = '/',
        method: Union[str, List[str], Tuple[str]] = 'GET',
        *, 
        path_args: ArgumentListType = DEFAULT_ARG,
        body_args: ArgumentListType = None,
        query_args: ArgumentListType = None,
        header_args: ArgumentListType = None,
        support_arguments_capitalization_style_switch: bool = False,
        simple_return: bool = False,
        
        class_name: str = None,
        return_method_info: bool = False,
        **kwargs,
    ):
        pass
    
    @classmethod
    def extract_args \
    (
        cls,
        *,
        body_args: ArgumentListType = None,
        query_args: ArgumentListType = None,
        header_args: ArgumentListType = None,
        support_arguments_capitalization_style_switch: bool = False,
        
        class_name: str = None,
        **kwargs
    ):
        pass
