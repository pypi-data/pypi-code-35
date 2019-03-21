## @package mmsi
#  Python wrapper for Modifiable Multi-Scale Image (MMSI) library.

from ctypes import *
from enum import Enum
import numpy
import platform

MMSIPROP_VERSION        = "mmsi_version"
MMSIPROP_IMAGE_WIDTH    = "mmsi_width"
MMSIPROP_IMAGE_HEIGHT   = "mmsi_height"
MMSIPROP_TILE_WIDTH     = "mmsi_tile_width"
MMSIPROP_TILE_HEIGHT    = "mmsi_tile_height"
MMSIPROP_LEVEL_COUNT    = "mmsi_level_count"
MMSIPROP_PIXEL_SIZE     = "mmsi_pixel_size"
MMSIPROP_DESCRIPTION    = "mmsi_description"

if platform.system() == 'Darwin':
    _so = cdll.LoadLibrary('libmmsi.0.dylib')
elif platform.system() == 'Windows':
	_so = cdll.LoadLibrary('mmsi.dll')
else:
    _so = cdll.LoadLibrary('libmmsi.so.0')

## The main class of MMSI.
class _MMSI(object):
    def __init__(self, mmsi):
        self._mmsi = mmsi
        self._as_parameter_ = self._mmsi
        self._segm_ps = 0
    
    def __del__(self):
        _Destroy(self._mmsi)
        
    @classmethod
    def from_param(cls, obj):
        return obj
    
    ## Load file data or create file.
    #
    #  This function must be called after parameters assigned and before
    #  initializing regions when using a Writer, or be called at first
    #  when using an Accessor.
    def Open(self):
        _Open(self._mmsi)
    
    ## Save file data.
    #
    #  This function must be called at last when data needs to be saved.
    def Close(self):
        _Close(self._mmsi)
    
    ## Get image property value.
    #  @param key The property name.
    #  @return The property value.
    def GetPropertyValue(self, key):
        return _GetPropertyValue(self._mmsi, _to_c_char_p(key))
    
    ## Set image property value.
    #  @param key The property name.
    #  @param value The property value.
    def SetPropertyValue(self, key, value):
        _SetPropertyValue(self._mmsi, _to_c_char_p(key), _to_c_char_p(value))
        
    ## Remove the property from this image.
    #  @param key The property name.
    def RemoveProperty(self, key):
        _RemoveProperty(self._mmsi, _to_c_char_p(key))
       
    ## Does certain property exist in this image.
    #  @param key The property name.
    #  @return Existed or not.
    def IsPropertyExisted(self, key):
        return _IsPropertyExisted(self._mmsi, _to_c_char_p(key))
    
    ## Get all property names in this image.
    #  @return Property names list.
    def GetPropertyNames(self):
        return _GetPropertyNames(self._mmsi)
    
    ## Get the description of this image.
    #  @return The description.
    def GetDescription(self):
        return _GetDescription(self._mmsi)
    
    ## Set the description of this image.
    #  @param desc The description.
    def SetDescription(self, desc):
        _SetDescription(self._mmsi, _to_c_char_p(desc))
        
    ## Has any error occurred when processing.
    #
    #  This function does not need to be called manually since every error will
    #  raise an MMSIError exception automatically.
    #  @return Any error or not.
    def HasError(self):
        return _HasError(self._mmsi)
    
    ## Get the error string.
    #
    #  @return The error string.
    def GetError(self):
        return _GetError(self._mmsi)
    
    ## Set the data compression level (1 - 9).
    #
    #  Use 1 for fastest compression and use 9 for minimal file size.
    #  @param level The compression level range in [1, 9].
    def SetCompressLevel(self, level):
        _SetCompressLevel(self._mmsi, level)
        
    ## Set the image size. Must be called before Open in a Writer.
    #  @param size The tuple contains image size.
    def SetImageSize(self, size):
        _SetImageSize(self._mmsi, size[0], size[1])
        
    ## Set the tile size. Must be called before Open in a Writer.
    #  @param size The tuple contains tile size.
    def SetTileSize(self, size):
        _SetTileSize(self._mmsi, size[0], size[1])
        
    ## Set the pixel size. Must be one of (1, 2, 4, 8). Must be called before Open
    #  in a Writer.
    #  @param size The pixel size in bytes.
    def SetPixelSize(self, size):
        _SetPixelSize(self._mmsi, size)
        
    ## Set the number of levels. Must be called before Open in a Writer.
    #  @param count The number of levels.
    def SetLevelCount(self, count):
        _SetLevelCount(self._mmsi, count)
    
    ## Initialize region image data. Must be called After Open and before Close in
    #  a Writer.
    #  @param data The numpy array that holds image data. The size must be corresponding
    #  to @param size and the dtype must be corresponding to the image pixel size.
    #  @param mask The numpy array that holds mask data. The size must be corresponding
    #  to @param size and the dtype must be 1 byte. Can be None to ignore mask.
    #  @param pos The left-top corner of the region.
    #  @param size The size of the region.
    def InitRegion(self, data, mask, pos, size):
        if not data.flags['C_CONTIGUOUS']:
            data = numpy.ascontiguousarray(data)
        databuf = cast(data.ctypes.data, c_void_p)
        maskbuf = None
        if not mask is None:
            if not mask.flags['C_CONTIGUOUS']:
                mask = numpy.ascontiguousarray(mask)
            maskbuf = cast(mask.ctypes.data, c_void_p)
        _InitRegion(self._mmsi, databuf, maskbuf, pos[0], pos[1], size[0], size[1])
    
    ## Set current operating region. Indicate where to read or write in following operations.
    #  Must be called in an Accessor.
    #  @param pos The left-top corner of the region.
    #  @param size The size of the region.
    def SetCurrentRegion(self, pos, size):
        _SetCurrentRegion(self._mmsi, pos[0], pos[1], size[0], size[1])
        self._size = [size[1], size[0]]
        
    ## Get desired image size of WriteRegion function. Must be called in an Accessor after Open.
    #  @param level The level of layer.
    #  @return The width of image.
    def GetRegionWidthLevel(self, level):
        return _GetRegionWidthLevel(self._mmsi, level)
    
    ## Get desired image size of WriteRegion function. Must be called in an Accessor after Open.
    #  @param level The level of layer.
    #  @return The height of image.
    def GetRegionHeightLevel(self, level):
        return _GetRegionHeightLevel(self._mmsi, level)
    
    ## Get down sample ratio at certain layer. Must be called in an Accessor after Open.
    #  @param level The level of layer.
    #  @return The down sample ratio.
    def GetDownsample(self, level):
        return _GetDownsample(self._mmsi, level)
    
    ## Read image data in current region. Must be called after calling SetCurrentRegion.
    #  Must be called in an Accessor after Open.
    #  @param level The level of layer to read.
    #  @return Numpy array containing image data.
    def ReadRegion(self, level):
        if self._segm_ps == 0:
            self._segm_ps = _GetPixelSize(self._mmsi)
            if self._segm_ps == 1:
                self._dtype = numpy.uint8
            if self._segm_ps == 2:
                self._dtype = numpy.uint16
            if self._segm_ps == 4:
                self._dtype = numpy.uint32
            if self._segm_ps == 8:
                self._dtype = numpy.uint64
        
        width = _GetRegionWidthLevel(self._mmsi, level)
        height = _GetRegionHeightLevel(self._mmsi, level)
        arr = numpy.empty([height, width], dtype = self._dtype)
        buffer = cast(arr.ctypes.data, c_void_p)
        _ReadRegion(self._mmsi, level, buffer)
        return arr
        
    ## Write image data in current region. Must be called after calling SetCurrentRegion.
    #  Must be called in an Accessor after Open.
    #  @param level The level of layer to write.
    #  @param data The numpy array that holds image data. The size must be corresponding to
    #  GetRegionWidthLevel / GetRegionHeightLevel and dtype must be corresponding to the
    #  image pixel size.
    #  @param mask The numpy array that holds mask data. The size must be corresponding to
    #  GetRegionWidthLevel / GetRegionHeightLevel and dtype must be 1 byte. Can be None to
    #  ignore mask.
    def WriteRegion(self, level, data, mask):
        if not data.flags['C_CONTIGUOUS']:
            data = numpy.ascontiguousarray(data)
        databuf = cast(data.ctypes.data, c_void_p)
        maskbuf = None
        if not mask is None:
            if not mask.flags['C_CONTIGUOUS']:
                mask = numpy.ascontiguousarray(mask)
            maskbuf = cast(mask.ctypes.data, c_void_p)
        _WriteRegion(self._mmsi, level, databuf, maskbuf)
        
    ## Get the image width. Must be called in an Accessor after Open.
    #  @return The image width.
    def GetImageWidth(self):
        return _GetImageWidth(self._mmsi)
        
    ## Get the image height. Must be called in an Accessor after Open.
    #  @return The image height.
    def GetImageHeight(self):
        return _GetImageHeight(self._mmsi)
        
    ## Get the tile width. Must be called in an Accessor after Open.
    #  @return The tile width.
    def GetTileWidth(self):
        return _GetTileWidth(self._mmsi)
        
    ## Get the tile height. Must be called in an Accessor after Open.
    #  @return The tile height.
    def GetTileHeight(self):
        return _GetTileHeight(self._mmsi)
        
    ## Get the image pixel size. Must be called in an Accessor after Open.
    #  @return The pixel size.
    def GetPixelSize(self):
        return _GetPixelSize(self._mmsi)
        
    ## Get number of layers. Must be called in an Accessor after Open.
    #  @return Number of layers.
    def GetLevelCount(self):
        return _GetLevelCount(self._mmsi)
        
    ## Get processing cache size. Means how many tiles are kept in the memory.
    #  Must be called in an Accessor.
    #  @return Number of tiles.
    def GetCacheSize(self):
        return _GetCacheSize(self._mmsi)
    
    ## Set processing cache size. Must be called in an Accessor.
    #  @param size Number of tiles.
    def SetCacheSize(self, size):
        _SetCacheSize(self._mmsi, size)
        
    ## Enable / Disable secure mode. File data will not be corrupted once the
    #  program crushes, but caching will be disabled. Must be called in an Accessor.
    #  @param enable Enable or not.
    def SetSecureMode(self, enable):
        _SetSecureMode(self._mmsi, enable)
        
## The Exception type of MMSI library.
class MMSIError(Exception):
    pass

def _check_error(result, func, args):
    if _HasError(args[0]):
        raise MMSIError(_GetError(args[0]))
    return result

def _check_bool(result, func, args):
    if not result:
        raise MMSIError(_GetError(args[0]))
    return result

def _check_string(result, func, _args):
    return result.decode('UTF-8')

def _check_string_error(result, func, args):
    if _HasError(args[0]):
        raise MMSIError(_GetError(args[0]))
    return result.decode('UTF-8')
    
def _check_strings(result, func, args):
    res = []
    i = 0
    while result[i]:
        res.append(result[i].decode('UTF-8'))
        i = i + 1
    return res

def _check_strings_error(result, func, args):
    if _HasError(args[0]):
        raise MMSIError(_GetError(args[0]))
    res = []
    i = 0
    while result[i]:
        res.append(result[i].decode('UTF-8'))
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

## Get version string of MMSI library.
Version = _get_func('mmsi_Version', c_char_p, [], _check_string)

_Writer = _get_func('mmsi_Writer', c_void_p, [c_char_p], None)

## Create a Writer object. Used to generate new MMSI files.
#  @param filename The image file name.
def Writer(filename):
    return _MMSI(_Writer(_to_c_char_p(filename)))
_Accessor = _get_func('mmsi_Accessor', c_void_p, [c_char_p], None)

## Create an Accessor object. Used to read and write MMSI files.
#  @param filename The image file name.
def Accessor(filename):
    return _MMSI(_Accessor(_to_c_char_p(filename)))
_Destroy = _get_func('mmsi_Destroy', None, [c_void_p], None)

_Open = _get_func('mmsi_Open', c_bool, [c_void_p], _check_bool)
_Close = _get_func('mmsi_Close', c_bool, [c_void_p], _check_bool)

_GetPropertyValue = _get_func('mmsi_GetPropertyValue', c_char_p, [c_void_p, c_char_p], _check_string_error)
_SetPropertyValue = _get_func('mmsi_SetPropertyValue', None, [c_void_p, c_char_p, c_char_p], _check_error)
_RemoveProperty = _get_func('mmsi_RemoveProperty', None, [c_void_p, c_char_p], _check_error)
_IsPropertyExisted = _get_func('mmsi_IsPropertyExisted', c_bool, [c_void_p, c_char_p], _check_error)
_GetPropertyNames = _get_func('mmsi_GetPropertyNames', POINTER(c_char_p), [c_void_p], _check_strings_error)

_GetDescription = _get_func('mmsi_GetDescription', c_char_p, [c_void_p], _check_string_error)
_SetDescription = _get_func('mmsi_SetDescription', None, [c_void_p, c_char_p], _check_error)

_HasError = _get_func('mmsi_HasError', c_bool, [c_void_p], None)
_GetError = _get_func('mmsi_GetError', c_char_p, [c_void_p], _check_string)

_SetCompressLevel = _get_func('mmsi_SetCompressLevel', None, [c_void_p, c_int32], None)

_SetImageSize = _get_func('mmsi_SetImageSize', None, [c_void_p, c_int64, c_int64], None)
_SetTileSize = _get_func('mmsi_SetTileSize', None, [c_void_p, c_int64, c_int64], None)
_SetPixelSize = _get_func('mmsi_SetPixelSize', None, [c_void_p, c_int32], None)
_SetLevelCount = _get_func('mmsi_SetLevelCount', None, [c_void_p, c_int32], None)

_InitRegion = _get_func('mmsi_InitRegion', None, [c_void_p, c_void_p, c_void_p, c_int64, c_int64, c_int64, c_int64], _check_error)

_SetCurrentRegion = _get_func('mmsi_SetCurrentRegion', None, [c_void_p, c_int64, c_int64, c_int64, c_int64], None)

_GetRegionWidthLevel = _get_func('mmsi_GetRegionWidthLevel', c_int64, [c_void_p, c_int32], None)
_GetRegionHeightLevel = _get_func('mmsi_GetRegionHeightLevel', c_int64, [c_void_p, c_int32], None)
_GetDownsample = _get_func('mmsi_GetDownsample', c_int64, [c_void_p, c_int32], None)

_ReadRegion = _get_func('mmsi_ReadRegion', None, [c_void_p, c_int32, c_void_p], _check_error)
_WriteRegion = _get_func('mmsi_WriteRegion', None, [c_void_p, c_int32, c_void_p, c_void_p], _check_error)

_GetImageWidth = _get_func('mmsi_GetImageWidth', c_int64, [c_void_p], None)
_GetImageHeight = _get_func('mmsi_GetImageHeight', c_int64, [c_void_p], None)
_GetTileWidth = _get_func('mmsi_GetTileWidth', c_int64, [c_void_p], None)
_GetTileHeight = _get_func('mmsi_GetTileHeight', c_int64, [c_void_p], None)
_GetPixelSize = _get_func('mmsi_GetPixelSize', c_int32, [c_void_p], None)
_GetLevelCount = _get_func('mmsi_GetLevelCount', c_int32, [c_void_p], None)

_GetCacheSize = _get_func('mmsi_GetCacheSize', c_int32, [c_void_p], None)
_SetCacheSize = _get_func('mmsi_SetCacheSize', None, [c_void_p, c_int32], None)
_SetSecureMode = _get_func('mmsi_SetSecureMode', None, [c_void_p, c_bool], None)
