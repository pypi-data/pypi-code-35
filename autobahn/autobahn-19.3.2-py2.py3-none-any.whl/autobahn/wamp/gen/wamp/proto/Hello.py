# automatically generated by the FlatBuffers compiler, do not modify

# namespace: proto

import flatbuffers

class Hello(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsHello(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Hello()
        x.Init(buf, n + offset)
        return x

    # Hello
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Hello
    def Roles(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from .ClientRoles import ClientRoles
            obj = ClientRoles()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Hello
    def Realm(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Hello
    def Authmethods(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Hello
    def AuthmethodsAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Hello
    def AuthmethodsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Hello
    def Authid(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Hello
    def Authrole(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Hello
    def Authextra(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from .Map import Map
            obj = Map()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Hello
    def Resumable(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # Hello
    def ResumeSession(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Hello
    def ResumeToken(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

def HelloStart(builder): builder.StartObject(9)
def HelloAddRoles(builder, roles): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(roles), 0)
def HelloAddRealm(builder, realm): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(realm), 0)
def HelloAddAuthmethods(builder, authmethods): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(authmethods), 0)
def HelloStartAuthmethodsVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def HelloAddAuthid(builder, authid): builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(authid), 0)
def HelloAddAuthrole(builder, authrole): builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(authrole), 0)
def HelloAddAuthextra(builder, authextra): builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(authextra), 0)
def HelloAddResumable(builder, resumable): builder.PrependBoolSlot(6, resumable, 0)
def HelloAddResumeSession(builder, resumeSession): builder.PrependUint64Slot(7, resumeSession, 0)
def HelloAddResumeToken(builder, resumeToken): builder.PrependUOffsetTRelativeSlot(8, flatbuffers.number_types.UOffsetTFlags.py_type(resumeToken), 0)
def HelloEnd(builder): return builder.EndObject()
