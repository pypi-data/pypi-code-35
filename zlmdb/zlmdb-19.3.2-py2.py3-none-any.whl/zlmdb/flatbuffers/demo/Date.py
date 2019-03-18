# automatically generated by the FlatBuffers compiler, do not modify

# namespace: demo

import flatbuffers

class Date(object):
    __slots__ = ['_tab']

    # Date
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Date
    def Year(self): return self._tab.Get(flatbuffers.number_types.Uint16Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # Date
    def Month(self): return self._tab.Get(flatbuffers.number_types.Uint8Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(2))
    # Date
    def Day(self): return self._tab.Get(flatbuffers.number_types.Uint8Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(3))

def CreateDate(builder, year, month, day):
    builder.Prep(2, 4)
    builder.PrependUint8(day)
    builder.PrependUint8(month)
    builder.PrependUint16(year)
    return builder.Offset()
