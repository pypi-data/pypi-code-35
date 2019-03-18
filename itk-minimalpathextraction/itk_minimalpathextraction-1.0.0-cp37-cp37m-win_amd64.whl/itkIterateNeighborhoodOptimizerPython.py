# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.8
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (3, 0, 0):
    new_instancemethod = lambda func, inst, cls: _itkIterateNeighborhoodOptimizerPython.SWIG_PyInstanceMethod_New(func)
else:
    from new import instancemethod as new_instancemethod
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_itkIterateNeighborhoodOptimizerPython', [dirname(__file__)])
        except ImportError:
            import _itkIterateNeighborhoodOptimizerPython
            return _itkIterateNeighborhoodOptimizerPython
        if fp is not None:
            try:
                _mod = imp.load_module('_itkIterateNeighborhoodOptimizerPython', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _itkIterateNeighborhoodOptimizerPython = swig_import_helper()
    del swig_import_helper
else:
    import _itkIterateNeighborhoodOptimizerPython
del version_info
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.


def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        object.__setattr__(self, name, value)
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr_nondynamic(self, class_type, name, static=1):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    if (not static):
        return object.__getattr__(self, name)
    else:
        raise AttributeError(name)

def _swig_getattr(self, class_type, name):
    return _swig_getattr_nondynamic(self, class_type, name, 0)


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object:
        pass
    _newclass = 0



def _swig_setattr_nondynamic_method(set):
    def set_attr(self, name, value):
        if (name == "thisown"):
            return self.this.own(value)
        if hasattr(self, name) or (name == "this"):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add attributes to %s" % self)
    return set_attr


import ITKOptimizersBasePython
import ITKCommonBasePython
import pyBasePython
import ITKCostFunctionsPython
import vnl_least_squares_functionPython
import vnl_matrixPython
import stdcomplexPython
import vnl_vectorPython
import itkCostFunctionPython
import vnl_cost_functionPython
import vnl_unary_functionPython
import itkArrayPython
import itkOptimizerParametersPython
import itkArray2DPython

def itkIterateNeighborhoodOptimizer_New():
  return itkIterateNeighborhoodOptimizer.New()

class itkIterateNeighborhoodOptimizer(ITKOptimizersBasePython.itkSingleValuedNonLinearOptimizer):
    """Proxy of C++ itkIterateNeighborhoodOptimizer class."""

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    def __New_orig__() -> "itkIterateNeighborhoodOptimizer_Pointer":
        """__New_orig__() -> itkIterateNeighborhoodOptimizer_Pointer"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer___New_orig__()

    __New_orig__ = staticmethod(__New_orig__)

    def Clone(self) -> "itkIterateNeighborhoodOptimizer_Pointer":
        """Clone(itkIterateNeighborhoodOptimizer self) -> itkIterateNeighborhoodOptimizer_Pointer"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_Clone(self)


    def GetMaximize(self) -> "bool const &":
        """GetMaximize(itkIterateNeighborhoodOptimizer self) -> bool const &"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_GetMaximize(self)


    def SetMaximize(self, _arg: 'bool const') -> "void":
        """SetMaximize(itkIterateNeighborhoodOptimizer self, bool const _arg)"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_SetMaximize(self, _arg)


    def MaximizeOn(self) -> "void":
        """MaximizeOn(itkIterateNeighborhoodOptimizer self)"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_MaximizeOn(self)


    def MaximizeOff(self) -> "void":
        """MaximizeOff(itkIterateNeighborhoodOptimizer self)"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_MaximizeOff(self)


    def GetMinimize(self) -> "bool":
        """GetMinimize(itkIterateNeighborhoodOptimizer self) -> bool"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_GetMinimize(self)


    def SetMinimize(self, v: 'bool') -> "void":
        """SetMinimize(itkIterateNeighborhoodOptimizer self, bool v)"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_SetMinimize(self, v)


    def MinimizeOn(self) -> "void":
        """MinimizeOn(itkIterateNeighborhoodOptimizer self)"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_MinimizeOn(self)


    def MinimizeOff(self) -> "void":
        """MinimizeOff(itkIterateNeighborhoodOptimizer self)"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_MinimizeOff(self)


    def AdvanceOneStep(self) -> "void":
        """AdvanceOneStep(itkIterateNeighborhoodOptimizer self)"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_AdvanceOneStep(self)


    def ResumeOptimization(self) -> "void":
        """ResumeOptimization(itkIterateNeighborhoodOptimizer self)"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_ResumeOptimization(self)


    def StopOptimization(self) -> "void":
        """StopOptimization(itkIterateNeighborhoodOptimizer self)"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_StopOptimization(self)


    def SetFullyConnected(self, _arg: 'bool const') -> "void":
        """SetFullyConnected(itkIterateNeighborhoodOptimizer self, bool const _arg)"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_SetFullyConnected(self, _arg)


    def GetFullyConnected(self) -> "bool const &":
        """GetFullyConnected(itkIterateNeighborhoodOptimizer self) -> bool const &"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_GetFullyConnected(self)


    def FullyConnectedOn(self) -> "void":
        """FullyConnectedOn(itkIterateNeighborhoodOptimizer self)"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_FullyConnectedOn(self)


    def FullyConnectedOff(self) -> "void":
        """FullyConnectedOff(itkIterateNeighborhoodOptimizer self)"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_FullyConnectedOff(self)


    def SetNeighborhoodSize(self, _arg: 'itkArrayD') -> "void":
        """SetNeighborhoodSize(itkIterateNeighborhoodOptimizer self, itkArrayD _arg)"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_SetNeighborhoodSize(self, _arg)


    def GetNeighborhoodSize(self) -> "itkArrayD const &":
        """GetNeighborhoodSize(itkIterateNeighborhoodOptimizer self) -> itkArrayD"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_GetNeighborhoodSize(self)


    def GetCurrentIteration(self) -> "unsigned int":
        """GetCurrentIteration(itkIterateNeighborhoodOptimizer self) -> unsigned int"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_GetCurrentIteration(self)


    def GetCurrentValue(self) -> "double const &":
        """GetCurrentValue(itkIterateNeighborhoodOptimizer self) -> double const &"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_GetCurrentValue(self)

    __swig_destroy__ = _itkIterateNeighborhoodOptimizerPython.delete_itkIterateNeighborhoodOptimizer

    def cast(obj: 'itkLightObject') -> "itkIterateNeighborhoodOptimizer *":
        """cast(itkLightObject obj) -> itkIterateNeighborhoodOptimizer"""
        return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_cast(obj)

    cast = staticmethod(cast)

    def New(*args, **kargs):
        """New() -> itkIterateNeighborhoodOptimizer

        Create a new object of the class itkIterateNeighborhoodOptimizer and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkIterateNeighborhoodOptimizer.New( reader, Threshold=10 )

        is (most of the time) equivalent to:

          obj = itkIterateNeighborhoodOptimizer.New()
          obj.SetInput( 0, reader.GetOutput() )
          obj.SetThreshold( 10 )
        """
        obj = itkIterateNeighborhoodOptimizer.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)

itkIterateNeighborhoodOptimizer.Clone = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_Clone, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.GetMaximize = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_GetMaximize, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.SetMaximize = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_SetMaximize, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.MaximizeOn = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_MaximizeOn, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.MaximizeOff = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_MaximizeOff, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.GetMinimize = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_GetMinimize, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.SetMinimize = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_SetMinimize, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.MinimizeOn = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_MinimizeOn, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.MinimizeOff = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_MinimizeOff, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.AdvanceOneStep = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_AdvanceOneStep, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.ResumeOptimization = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_ResumeOptimization, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.StopOptimization = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_StopOptimization, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.SetFullyConnected = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_SetFullyConnected, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.GetFullyConnected = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_GetFullyConnected, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.FullyConnectedOn = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_FullyConnectedOn, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.FullyConnectedOff = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_FullyConnectedOff, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.SetNeighborhoodSize = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_SetNeighborhoodSize, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.GetNeighborhoodSize = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_GetNeighborhoodSize, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.GetCurrentIteration = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_GetCurrentIteration, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer.GetCurrentValue = new_instancemethod(_itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_GetCurrentValue, None, itkIterateNeighborhoodOptimizer)
itkIterateNeighborhoodOptimizer_swigregister = _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_swigregister
itkIterateNeighborhoodOptimizer_swigregister(itkIterateNeighborhoodOptimizer)

def itkIterateNeighborhoodOptimizer___New_orig__() -> "itkIterateNeighborhoodOptimizer_Pointer":
    """itkIterateNeighborhoodOptimizer___New_orig__() -> itkIterateNeighborhoodOptimizer_Pointer"""
    return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer___New_orig__()

def itkIterateNeighborhoodOptimizer_cast(obj: 'itkLightObject') -> "itkIterateNeighborhoodOptimizer *":
    """itkIterateNeighborhoodOptimizer_cast(itkLightObject obj) -> itkIterateNeighborhoodOptimizer"""
    return _itkIterateNeighborhoodOptimizerPython.itkIterateNeighborhoodOptimizer_cast(obj)



