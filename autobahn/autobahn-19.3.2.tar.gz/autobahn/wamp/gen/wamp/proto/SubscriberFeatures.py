# automatically generated by the FlatBuffers compiler, do not modify

# namespace: proto

import flatbuffers

class SubscriberFeatures(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsSubscriberFeatures(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = SubscriberFeatures()
        x.Init(buf, n + offset)
        return x

    # SubscriberFeatures
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # SubscriberFeatures
    def PublisherIdentification(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # SubscriberFeatures
    def PatternBasedSubscription(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # SubscriberFeatures
    def PublicationTrustlevels(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # SubscriberFeatures
    def SubscriptionRevocation(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # SubscriberFeatures
    def EventHistory(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # SubscriberFeatures
    def AcknowledgeSubscriberReceived(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # SubscriberFeatures
    def PayloadTransparency(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # SubscriberFeatures
    def PayloadEncryptionCryptobox(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

def SubscriberFeaturesStart(builder): builder.StartObject(8)
def SubscriberFeaturesAddPublisherIdentification(builder, publisherIdentification): builder.PrependBoolSlot(0, publisherIdentification, 0)
def SubscriberFeaturesAddPatternBasedSubscription(builder, patternBasedSubscription): builder.PrependBoolSlot(1, patternBasedSubscription, 0)
def SubscriberFeaturesAddPublicationTrustlevels(builder, publicationTrustlevels): builder.PrependBoolSlot(2, publicationTrustlevels, 0)
def SubscriberFeaturesAddSubscriptionRevocation(builder, subscriptionRevocation): builder.PrependBoolSlot(3, subscriptionRevocation, 0)
def SubscriberFeaturesAddEventHistory(builder, eventHistory): builder.PrependBoolSlot(4, eventHistory, 0)
def SubscriberFeaturesAddAcknowledgeSubscriberReceived(builder, acknowledgeSubscriberReceived): builder.PrependBoolSlot(5, acknowledgeSubscriberReceived, 0)
def SubscriberFeaturesAddPayloadTransparency(builder, payloadTransparency): builder.PrependBoolSlot(6, payloadTransparency, 0)
def SubscriberFeaturesAddPayloadEncryptionCryptobox(builder, payloadEncryptionCryptobox): builder.PrependBoolSlot(7, payloadEncryptionCryptobox, 0)
def SubscriberFeaturesEnd(builder): return builder.EndObject()
