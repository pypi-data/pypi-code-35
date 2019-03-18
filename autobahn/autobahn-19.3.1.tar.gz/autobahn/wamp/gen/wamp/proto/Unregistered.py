# automatically generated by the FlatBuffers compiler, do not modify

# namespace: proto

import flatbuffers

class Unregistered(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsUnregistered(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Unregistered()
        x.Init(buf, n + offset)
        return x

    # Unregistered
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Unregistered
    def Request(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Unregistered
    def Registration(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Unregistered
    def Reason(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

def UnregisteredStart(builder): builder.StartObject(3)
def UnregisteredAddRequest(builder, request): builder.PrependUint64Slot(0, request, 0)
def UnregisteredAddRegistration(builder, registration): builder.PrependUint64Slot(1, registration, 0)
def UnregisteredAddReason(builder, reason): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(reason), 0)
def UnregisteredEnd(builder): return builder.EndObject()
