## @package libmi
#  Python wrapper for libMI the histopathological image annotating library.

from ctypes import *
from enum import Enum
import numpy
import platform

if platform.system() == 'Darwin':
    _so = cdll.LoadLibrary('libmi.0.dylib')
elif platform.system() == 'Windows':
    _so = cdll.LoadLibrary('libmi.dll')
else:
    _so = cdll.LoadLibrary('libmi.so.0')

## The type of image.
class SlideType(Enum):
    OPENSLIDE = 0
    DICOM = 1
    UNKNOWN = 2

## The main class of libmi
class Slide(object):
    ## The constructor
    #  @param projdir The project directory.
    def __init__(self, projdir):
        self._slide = _Create(_to_c_char_p(projdir))
        self._as_parameter_ = self._slide
        
    def __del__(self):
        _Destroy(self._slide)
        
    @classmethod
    def from_param(cls, obj):
        return obj
    
    ## Load project data.
    #
    #  This function must be called first before any other actions.
    def LoadProject(self):
        _LoadProject(self._slide)
        self._segm_ps = _GetSegmPixelSize(self._slide)
        if self._segm_ps == 1:
            self._dtype = numpy.int8
        if self._segm_ps == 2:
            self._dtype = numpy.int16
        if self._segm_ps == 4:
            self._dtype = numpy.int32
        if self._segm_ps == 8:
            self._dtype = numpy.int64
        
    ## Save project data.
    #
    #  This function must be called at last to ensure the data is saved.
    def SaveProject(self):
        _SaveProject(self._slide)
        
    ## Get image width.
    #  @return Image Width.
    def GetWidth(self):
        return _GetWidth(self._slide)
    
    ## Get image height.
    #  @return Image height.
    def GetHeight(self):
        return _GetHeight(self._slide)
    
    ## Get image type.
    #  @return Enum SlideType object.
    def GetType(self):
        return SlideType(_GetType(self._slide))
    
    ## Set current operating region. Indicate where to read or write in following operations.
    #  @param pos The left-top corner of the region.
    #  @param size The size of the region.
    def SetCurrentRegion(self, pos, size):
        _SetCurrentRegion(self._slide, pos[0], pos[1], size[0], size[1])
    
    ## Set the reading or writing buffer size.
    #  @param size The size of the data buffer.
    def SetRegionSize(self, size):
        _SetRegionSize(self._slide, size[0], size[1])
        self._ssize = [size[1], size[0]]
        self._rsize = [size[1], size[0], 4]
        
    ## Read image data in current region.
    #  @return Numpy array containing image data.
    def ReadRegion(self):
        arr = numpy.empty(self._rsize, dtype = numpy.uint8)
        buffer = cast(arr.ctypes.data, c_void_p)
        _ReadRegion(self._slide, buffer)
        return arr
    
    ## Read segmentation data in current region.
    #  @return Numpy array containing segmentation data.
    def ReadSegm(self):
        arr = numpy.empty(self._ssize, dtype = self._dtype)
        buffer = cast(arr.ctypes.data, c_void_p)
        _ReadSegm(self._slide, buffer)
        return arr
    
    ## Write segmentation data to current region.
    #  @param data The numpy array that holds segmentation data. The size must be corresponding
    #  to region size and dtype must be corresponding to the image pixel size.
    #  @param mask The numpy array that holds mask data. The size must be corresponding to region
    #  size and dtype must be 1 byte. Can be None to ignore this parameter.
    def WriteSegm(self, data, mask):
        if not data.flags['C_CONTIGUOUS']:
            data = numpy.ascontiguousarray(data)
        databuf = cast(data.ctypes.data, c_void_p)
        maskbuf = None
        if not mask is None:
            if not mask.flags['C_CONTIGUOUS']:
                mask = numpy.ascontiguousarray(mask)
            maskbuf = cast(mask.ctypes.data, c_void_p)
        _WriteSegm(self._slide, databuf, maskbuf)
        
    ## Add an ellipse annotation.
    #  @param pos The center position.
    #  @param radius The two radiuses.
    #  @return The annotation object.
    def AddAnnoEllipse(self, pos, radius):
        return Anno(_AddAnnoEllipse(self._slide, pos[0], pos[1], radius[0], radius[1]))
    
    ## Add an rectangle annotation.
    #  @param pos The left-top corner.
    #  @param size The size of the rectangle.
    #  @return The annotation object.
    def AddAnnoRect(self, pos, size):
        return Anno(_AddAnnoRect(self._slide, pos[0], pos[1], size[0], size[1]))
    
    ## Add an polygon annotation.
    #  @param xpos The x position numpy array. Must be 8 bytes.
    #  @param ypos The y posision numpy array. Must be 8 bytes.
    def AddAnnoPolygon(self, xpos, ypos):
        if not xpos.flags['C_CONTIGUOUS']:
            xpos = numpy.ascontiguousarray(xpos)
        if not ypos.flags['C_CONTIGUOUS']:
            ypos = numpy.ascontiguousarray(ypos)
        xbuf = cast(xpos.ctypes.data, POINTER(c_int64))
        ybuf = cast(ypos.ctypes.data, POINTER(c_int64))
        return Anno(_AddAnnoPolygon(self._slide, xbuf, ybuf, min(xpos.size, ypos.size)))
    
    ## Get all annotation objects.
    #  @return Anno object list.
    def GetAnnos(self):
        return _GetAnnos(self._slide)
    
    ## Remove certain annotation.
    #  @param anno The annotation to remove.
    def RemoveAnno(self, anno):
        _RemoveAnno(self._slide, anno._anno)
        
    ## Set segmentation processing cache size. Means how many tiles are kept in the memory.
    #  @param size The cache size.
    def SetSegmCacheSize(self, size):
        _SetSegmCacheSize(self._slide, size)
    
    ## Enable / Disable secure mode. File data will not be corrupted once the
    #  program crushes, but caching will be disabled.
    #  @param enable Enable or not.
    def SetSecureMode(self, enable):
        _SetSecureMode(self._slide, enable)
    
    ## Set the data compression level (1 - 9).
    #
    #  Use 1 for fastest compression and use 9 for minimal file size.
    #  @param level The compression level range in [1, 9].
    def SetCompressLevel(self, level):
        _SetCompressLevel(self._slide, level)
    
    ## Get all property names in this image.
    #  @return Property names list.
    def GetPropertyNames(self):
        return _GetPropertyNames(self._slide)
    
    ## Get image property value.
    #  @param key The property name.
    #  @return The property value.
    def GetPropertyValue(self, key):
        return _GetPropertyValue(self._slide, _to_c_char_p(key))
    
    ## Set image property value.
    #  @param key The property name.
    #  @param value The property value.
    def SetPropertyValue(self, key, value):
        _SetPropertyValue(self._slide, _to_c_char_p(key), _to_c_char_p(value))
    
    ## Remove the property from this image.
    #  @param key The property name.
    def RemoveProperty(self, key):
        _RemoveProperty(self._slide, _to_c_char_p(key))
    
    ## Get grading data for certain segmentation id.
    #  @param segm_id The segmentation id.
    #  @return The grade.
    def GetGrade(self, segm_id):
        return _GetGrade(self._slide, segm_id)
    
    ## Get grading data for an array of segmentation ids.
    #  @param segm_ids Numpy array of segmentation ids. Must be 8 bytes in size.
    #  @return Numpy array of grading data.
    def GetGrades(self, segm_ids):
        if not segm_ids.flags['C_CONTIGUOUS']:
            segm_ids = numpy.ascontiguousarray(segm_ids)
        buffer = cast(segm_ids.ctypes.data, POINTER(c_int64))
        grades = numpy.empty([segm_ids.size], dtype = numpy.uint8)
        gbuf = cast(grades.ctypes.data, POINTER(c_int8))
        _GetGrades(self._slide, segm_ids.size, buffer, gbuf)
        return grades
    
    ## Set grading data for certain segmentation id.
    #  @param segm_id The segmentation id.
    #  @param grade The grade.
    def SetGrade(self, segm_id, grade):
        _SetGrade(self._slide, segm_id, grade)
        
    ## Set grading data for an array of segmentation ids.
    #  @param segm_ids Numpy array of segmentation ids. Must be 8 bytes in size.
    #  @param grades Numpy array of grading data. Must be 1 byte in size.
    def SetGrades(self, segm_ids, grades):
        if not segm_ids.flags['C_CONTIGUOUS']:
            segm_ids = numpy.ascontiguousarray(segm_ids)
        if not grades.flags['C_CONTIGUOUS']:
            grades = numpy.ascontiguousarray(grades)
        buffer = cast(segm_ids.ctypes.data, POINTER(c_int64))
        gbuf = cast(grades.ctypes.data, POINTER(c_int8))
        _SetGrades(self._slide, segm_ids.size, buffer, gbuf)
    
    ## Get segmentation data tile size.
    #  @return Tile size.
    def GetSegmTileSize(self):
        return _GetSegmTileSize(self._slide)
    
    ## Get segmentation data pixel size.
    #  @return Pixel size.
    def GetSegmPixelSize(self):
        return _GetSegmPixelSize(self._slide)
    
    ## Get grading data tile size.
    #  @return Tile size.
    def GetGradeTileSize(self):
        return _GetGradeTileSize(self._slide)
    
## The type of annotation.
class AnnoType(Enum):
    NONE = 0
    ELLIPSE = 1
    RECTANGLE = 2
    POLYGON = 3
    
## The annotation class.
class Anno(object):
    def __init__(self, annoobj):
        self._anno = annoobj
        self._as_parameter = self._anno
        
    @classmethod
    def from_param(cls, obj):
        return obj
    
    ## Get annotation type.
    #  @return Enum AnnoType.
    def GetAnnoType(self):
        return AnnoType(_GetAnnoType(self._anno))
    
    ## Get annotation color.
    #  @return Tuple of color.
    def GetAnnoColor(self):
        r, g, b = c_uint8(), c_uint8(), c_uint8()
        _GetAnnoColor(self._anno, byref(r), byref(g), byref(b))
        return (r, g, b)
    
    ## Set annotation color.
    #  @param color Tuple of color.
    def SetAnnoColor(self, color):
        _SetAnnoColor(self._anno, color[0], color[1], color[2])
        
    ## Get rectangle annotation parameters.
    #  @return Position and size of the annotation.
    def GetAnnoRectParam(self):
        x, y, w, h = c_int64(), c_int64(), c_int64(), c_int64()
        _GetAnnoRectParam(self._anno, byref(x), byref(y), byref(w), byref(h))
        return (x, y), (w, h)
    
    ## Set rectangle annotation parameters.
    #  @param pos The left-top corner of the rectangle.
    #  @param size The size of the rectangle.
    def SetAnnoRectParam(self, pos, size):
        _SetAnnoRectParam(self._anno, pos[0], pos[1], size[0], size[1])
        
    ## Get ellipse annotation parameters.
    #  @return Position and radius of the annotation.
    def GetAnnoElliParam(self):
        x, y, a, b = c_int64(), c_int64(), c_int64(), c_int64()
        _GetAnnoElliParam(self._anno, byref(x), byref(y), byref(a), byref(b))
        return (x, y), (a, b)
    
    ## Set ellipse annotation parameters.
    #  @param pos The center of the ellipse.
    #  @param radius The radiuses of the ellipse.
    def SetAnnoElliParam(self, pos, radius):
        _SetAnnoElliParam(self._anno, pos[0], pos[1], radius[0], radius[1])
        
    ## Get polygon annotation parameters.
    #  @return Numpy arrays of point positions.
    def GetAnnoPolyParam(self):
        size = _GetAnnoPolyPointCount(self._anno)
        xpos = numpy.empty([size], dtype = numpy.int64)
        ypos = numpy.empty([size], dtype = numpy.int64)
        xbuf = cast(xpos.ctypes.data, POINTER(c_int64))
        ybuf = cast(ypos.ctypes.data, POINTER(c_int64))
        _GetAnnoPolyParam(self._anno, xbuf, ybuf)
        return xpos, ypos
    
    ## Set polygon annotation parameters.
    #  @param xpos Numpy array of point x coordinations. Must be 8 bytes in size.
    #  @param ypos Numpy array of point y coordinations. Must be 8 bytes in size.
    def SetAnnoPolyParam(self, xpos, ypos):
        if not xpos.flags['C_CONTIGUOUS']:
            xpos = numpy.ascontiguousarray(xpos)
        if not ypos.flags['C_CONTIGUOUS']:
            ypos = numpy.ascontiguousarray(ypos)
        xbuf = cast(xpos.ctypes.data, POINTER(c_int64))
        ybuf = cast(ypos.ctypes.data, POINTER(c_int64))
        return _SetAnnoPolyParam(self._anno, xbuf, ybuf, min(xpos.size, ypos.size))

## The exception type of OpenHIL.
class OpenHILError(Exception):
    pass

def _check_error(result, func, args):
    if _HasError(args[0]):
        raise OpenHILError(_GetErrorStr(args[0]))
    return result

def _check_string(result, func, _args):
        return result.decode('UTF-8')
    
def _check_strings(result, func, args):
    res = []
    i = 0
    while result[i]:
        res.append(result[i].decode('UTF-8'))
        i = i + 1
    return res

def _check_pointers(result, func, args):
    res = []
    i = 0
    while result[i]:
        res.append(Anno(result[i]))
        i = i + 1
    return res

def _get_func(name, res, args, errchk = _check_error):
    func = getattr(_so, name)
    func.restype = res
    func.argtypes = args
    if errchk is not None:
        func.errcheck = errchk
    return func

def _to_c_char_p(string):
    return string.encode('UTF-8')

## Get version string of OpenHIL.
Version = _get_func('ohil_Version', c_char_p, [], _check_string)

_Create = _get_func('ohil_Create', c_void_p, [c_char_p], None)
_Destroy = _get_func('ohil_Destroy', None, [c_void_p], None)

_HasError = _get_func('ohil_HasError', c_bool, [c_void_p], None)
_GetErrorStr = _get_func('ohil_GetErrorStr', c_char_p, [c_void_p], _check_string)

_LoadProject = _get_func('ohil_LoadProject', None, [c_void_p])
_SaveProject = _get_func('ohil_SaveProject', None, [c_void_p])

_GetWidth = _get_func('ohil_GetWidth', c_int64, [c_void_p], None)
_GetHeight = _get_func('ohil_GetHeight', c_int64, [c_void_p], None)
_GetType = _get_func('ohil_GetType', c_int32, [c_void_p], None)

_SetCurrentRegion = _get_func('ohil_SetCurrentRegion', None, [c_void_p, c_int64, c_int64, c_int64, c_int64], None)
_SetRegionSize = _get_func('ohil_SetRegionSize', None, [c_void_p, c_int64, c_int64], None)
_ReadRegion = _get_func('ohil_ReadRegion', None, [c_void_p, c_void_p])
_ReadSegm = _get_func('ohil_ReadSegm', None, [c_void_p, c_void_p])
_WriteSegm = _get_func('ohil_WriteSegm', None, [c_void_p, c_void_p, c_void_p])

_AddAnnoEllipse = _get_func('ohil_AddAnnoEllipse', c_void_p, [c_void_p, c_int64, c_int64, c_int64, c_int64], None)
_AddAnnoRect = _get_func('ohil_AddAnnoRect', c_void_p, [c_void_p, c_int64, c_int64, c_int64, c_int64], None)
_AddAnnoPolygon = _get_func('ohil_AddAnnoPolygon', c_void_p, [c_void_p, POINTER(c_int64), POINTER(c_int64), c_int32], None)
_GetAnnos = _get_func('ohil_GetAnnos', POINTER(c_void_p), [c_void_p], _check_pointers)
_RemoveAnno = _get_func('ohil_RemoveAnno', None, [c_void_p, c_void_p], None)

_SetSegmCacheSize = _get_func('ohil_SetSegmCacheSize', None, [c_void_p, c_int32], None)
_SetSecureMode = _get_func('ohil_SetSecureMode', None, [c_void_p, c_bool], None)
_SetCompressLevel = _get_func('ohil_SetCompressLevel', None, [c_void_p, c_int32], None)

_GetPropertyNames = _get_func('ohil_GetPropertyNames', POINTER(c_char_p), [c_void_p], _check_strings)
_GetPropertyValue = _get_func('ohil_GetPropertyValue', c_char_p, [c_void_p, c_char_p], _check_string)
_SetPropertyValue = _get_func('ohil_SetPropertyValue', None, [c_void_p, c_char_p, c_char_p], None)
_RemoveProperty = _get_func('ohil_RemoveProperty', None, [c_void_p, c_char_p], None)

_GetGrade = _get_func('ohil_GetGrade', c_int8, [c_void_p, c_int64])
_GetGrades = _get_func('ohil_GetGrades', None, [c_void_p, c_int32, POINTER(c_int64), POINTER(c_int8)])
_SetGrade = _get_func('ohil_SetGrade', None, [c_void_p, c_int64, c_int8])
_SetGrades = _get_func('ohil_SetGrades', None, [c_void_p, c_int32, POINTER(c_int64), POINTER(c_int8)])

_GetSegmTileSize = _get_func('ohil_GetSegmTileSize', c_int32, [c_void_p], None)
_GetSegmPixelSize = _get_func('ohil_GetSegmPixelSize', c_int32, [c_void_p], None)
_GetGradeTileSize = _get_func('ohil_GetGradeTileSize', c_int32, [c_void_p], None)

_GetAnnoType = _get_func('ohil_GetAnnoType', c_int32, [c_void_p], None)
_GetAnnoColor = _get_func('ohil_GetAnnoColor', None, [c_void_p, POINTER(c_uint8), POINTER(c_uint8), POINTER(c_uint8)], None)
_SetAnnoColor = _get_func('ohil_SetAnnoColor', None, [c_void_p, c_uint8, c_uint8, c_uint8], None)

_GetAnnoRectParam = _get_func('ohil_GetAnnoRectParam', None, [c_void_p, POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64)], None)
_SetAnnoRectParam = _get_func('ohil_SetAnnoRectParam', None, [c_void_p, c_int64, c_int64, c_int64, c_int64], None)
_GetAnnoElliParam = _get_func('ohil_GetAnnoElliParam', None, [c_void_p, POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64)], None)
_SetAnnoElliParam = _get_func('ohil_SetAnnoElliParam', None, [c_void_p, c_int64, c_int64, c_int64, c_int64], None)
_GetAnnoPolyPointCount = _get_func('ohil_GetAnnoPolyPointCount', c_int32, [c_void_p], None)
_GetAnnoPolyParam = _get_func('ohil_GetAnnoPolyParam', None, [c_void_p, POINTER(c_int64), POINTER(c_int64)], None)
_SetAnnoPolyParam = _get_func('ohil_SetAnnoPolyParam', None, [c_void_p, POINTER(c_int64), POINTER(c_int64), c_int32], None)
