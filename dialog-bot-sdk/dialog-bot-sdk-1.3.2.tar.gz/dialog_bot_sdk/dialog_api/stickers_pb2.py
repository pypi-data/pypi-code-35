# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: stickers.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from . import definitions_pb2 as definitions__pb2
from . import miscellaneous_pb2 as miscellaneous__pb2
from . import media_and_files_pb2 as media__and__files__pb2
from .scalapb import scalapb_pb2 as scalapb_dot_scalapb__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='stickers.proto',
  package='dialog',
  syntax='proto3',
  serialized_options=_b('\342?\026\n\024im.dlg.grpc.services'),
  serialized_pb=_b('\n\x0estickers.proto\x12\x06\x64ialog\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x11\x64\x65\x66initions.proto\x1a\x13miscellaneous.proto\x1a\x15media_and_files.proto\x1a\x15scalapb/scalapb.proto\"\x95\x02\n\x11StickerDescriptor\x12\x19\n\x02id\x18\x01 \x01(\x05\x42\r\x8a\xea\x30\t\n\x07visible\x12:\n\x05\x65moji\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\r\x8a\xea\x30\t\n\x07visible\x12\x37\n\timage_128\x18\x03 \x01(\x0b\x32\x15.dialog.ImageLocationB\r\x8a\xea\x30\t\n\x07visible\x12\x37\n\timage_512\x18\x04 \x01(\x0b\x32\x15.dialog.ImageLocationB\r\x8a\xea\x30\t\n\x07visible\x12\x37\n\timage_256\x18\x05 \x01(\x0b\x32\x15.dialog.ImageLocationB\r\x8a\xea\x30\t\n\x07visible\"\xe6\x01\n\x11StickerCollection\x12\x19\n\x02id\x18\x01 \x01(\x05\x42\r\x8a\xea\x30\t\n\x07visible\x12:\n\x05title\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\r\x8a\xea\x30\t\n\x07visible\x12:\n\x08stickers\x18\x03 \x03(\x0b\x32\x19.dialog.StickerDescriptorB\r\x8a\xea\x30\t\n\x07visible\x12>\n\x0bowned_by_me\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.BoolValueB\r\x8a\xea\x30\t\n\x07visible\"\xb2\x01\n\x18ResponseStickersResponse\x12=\n\x0b\x63ollections\x18\x01 \x03(\x0b\x32\x19.dialog.StickerCollectionB\r\x8a\xea\x30\t\n\x07visible\x12\x1a\n\x03seq\x18\x02 \x01(\x05\x42\r\x8a\xea\x30\t\n\x07visible\x12\x1c\n\x05state\x18\x03 \x01(\x0c\x42\r\x8a\xea\x30\t\n\x07visible:\x1d\xe2?\x1a\n\x18im.dlg.grpc.GrpcResponse\"6\n\x16RequestLoadOwnStickers:\x1c\xe2?\x19\n\x17im.dlg.grpc.GrpcRequest\"i\n\x17ResponseLoadOwnStickers\x12/\n\x0cown_stickers\x18\x01 \x03(\x0b\x32\x19.dialog.StickerCollection:\x1d\xe2?\x1a\n\x18im.dlg.grpc.GrpcResponse\"=\n\x1dRequestLoadAcesssibleStickers:\x1c\xe2?\x19\n\x17im.dlg.grpc.GrpcRequest\"w\n\x1eResponseLoadAcesssibleStickers\x12\x36\n\x13\x61\x63\x63\x65ssible_stickers\x18\x01 \x03(\x0b\x32\x19.dialog.StickerCollection:\x1d\xe2?\x1a\n\x18im.dlg.grpc.GrpcResponse\"j\n\x1eRequestAddStickerPackReference\x12*\n\x13source_sticker_pack\x18\x01 \x01(\x05\x42\r\x8a\xea\x30\t\n\x07visible:\x1c\xe2?\x19\n\x17im.dlg.grpc.GrpcRequest\"m\n!RequestRemoveStickerPackReference\x12*\n\x13source_sticker_pack\x18\x01 \x01(\x05\x42\r\x8a\xea\x30\t\n\x07visible:\x1c\xe2?\x19\n\x17im.dlg.grpc.GrpcRequest\"h\n\x1fUpdateStickerCollectionsChanged\x12\x45\n\x13updated_collections\x18\x01 \x03(\x0b\x32\x19.dialog.StickerCollectionB\r\x8a\xea\x30\t\n\x07visible\":\n\x18UpdateStickerPackRemoved\x12\x1e\n\x07pack_id\x18\x01 \x01(\x05\x42\r\x8a\xea\x30\t\n\x07visible\"P\n\x16UpdateStickerPackAdded\x12\x36\n\x04pack\x18\x01 \x01(\x0b\x32\x19.dialog.StickerCollectionB\r\x8a\xea\x30\t\n\x07visible\"Y\n\x1bRequestAddStickerCollection\x12\x1c\n\x05title\x18\x01 \x01(\tB\r\x8a\xea\x30\t\n\x07visible:\x1c\xe2?\x19\n\x17im.dlg.grpc.GrpcRequest\"Y\n\x1eRequestRemoveStickerCollection\x12\x19\n\x02id\x18\x01 \x01(\x05\x42\r\x8a\xea\x30\t\n\x07visible:\x1c\xe2?\x19\n\x17im.dlg.grpc.GrpcRequest\"W\n\x1cRequestLoadStickerCollection\x12\x19\n\x02id\x18\x01 \x01(\x05\x42\r\x8a\xea\x30\t\n\x07visible:\x1c\xe2?\x19\n\x17im.dlg.grpc.GrpcRequest\"m\n\x1dResponseLoadStickerCollection\x12-\n\ncollection\x18\x01 \x01(\x0b\x32\x19.dialog.StickerCollection:\x1d\xe2?\x1a\n\x18im.dlg.grpc.GrpcResponse2\x83\x08\n\x08Stickers\x12\x80\x01\n\x0fLoadOwnStickers\x12\x1e.dialog.RequestLoadOwnStickers\x1a\x1f.dialog.ResponseLoadOwnStickers\",\x82\xd3\xe4\x93\x02&\"!/v1/grpc/Stickers/LoadOwnStickers:\x01*\x12\x9c\x01\n\x16LoadAcesssibleStickers\x12%.dialog.RequestLoadAcesssibleStickers\x1a&.dialog.ResponseLoadAcesssibleStickers\"3\x82\xd3\xe4\x93\x02-\"(/v1/grpc/Stickers/LoadAcesssibleStickers:\x01*\x12\x8c\x01\n\x17\x41\x64\x64StickerPackReference\x12&.dialog.RequestAddStickerPackReference\x1a\x13.dialog.ResponseSeq\"4\x82\xd3\xe4\x93\x02.\")/v1/grpc/Stickers/AddStickerPackReference:\x01*\x12\x95\x01\n\x1aRemoveStickerPackReference\x12).dialog.RequestRemoveStickerPackReference\x1a\x13.dialog.ResponseSeq\"7\x82\xd3\xe4\x93\x02\x31\",/v1/grpc/Stickers/RemoveStickerPackReference:\x01*\x12\x83\x01\n\x14\x41\x64\x64StickerCollection\x12#.dialog.RequestAddStickerCollection\x1a\x13.dialog.ResponseSeq\"1\x82\xd3\xe4\x93\x02+\"&/v1/grpc/Stickers/AddStickerCollection:\x01*\x12\x8c\x01\n\x17RemoveStickerCollection\x12&.dialog.RequestRemoveStickerCollection\x1a\x13.dialog.ResponseSeq\"4\x82\xd3\xe4\x93\x02.\")/v1/grpc/Stickers/RemoveStickerCollection:\x01*\x12\x98\x01\n\x15LoadStickerCollection\x12$.dialog.RequestLoadStickerCollection\x1a%.dialog.ResponseLoadStickerCollection\"2\x82\xd3\xe4\x93\x02,\"\'/v1/grpc/Stickers/LoadStickerCollection:\x01*B\x19\xe2?\x16\n\x14im.dlg.grpc.servicesb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,definitions__pb2.DESCRIPTOR,miscellaneous__pb2.DESCRIPTOR,media__and__files__pb2.DESCRIPTOR,scalapb_dot_scalapb__pb2.DESCRIPTOR,])




_STICKERDESCRIPTOR = _descriptor.Descriptor(
  name='StickerDescriptor',
  full_name='dialog.StickerDescriptor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='dialog.StickerDescriptor.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='emoji', full_name='dialog.StickerDescriptor.emoji', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='image_128', full_name='dialog.StickerDescriptor.image_128', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='image_512', full_name='dialog.StickerDescriptor.image_512', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='image_256', full_name='dialog.StickerDescriptor.image_256', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=175,
  serialized_end=452,
)


_STICKERCOLLECTION = _descriptor.Descriptor(
  name='StickerCollection',
  full_name='dialog.StickerCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='dialog.StickerCollection.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='title', full_name='dialog.StickerCollection.title', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stickers', full_name='dialog.StickerCollection.stickers', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='owned_by_me', full_name='dialog.StickerCollection.owned_by_me', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=455,
  serialized_end=685,
)


_RESPONSESTICKERSRESPONSE = _descriptor.Descriptor(
  name='ResponseStickersResponse',
  full_name='dialog.ResponseStickersResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='collections', full_name='dialog.ResponseStickersResponse.collections', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seq', full_name='dialog.ResponseStickersResponse.seq', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='state', full_name='dialog.ResponseStickersResponse.state', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\032\n\030im.dlg.grpc.GrpcResponse'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=688,
  serialized_end=866,
)


_REQUESTLOADOWNSTICKERS = _descriptor.Descriptor(
  name='RequestLoadOwnStickers',
  full_name='dialog.RequestLoadOwnStickers',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\031\n\027im.dlg.grpc.GrpcRequest'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=868,
  serialized_end=922,
)


_RESPONSELOADOWNSTICKERS = _descriptor.Descriptor(
  name='ResponseLoadOwnStickers',
  full_name='dialog.ResponseLoadOwnStickers',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='own_stickers', full_name='dialog.ResponseLoadOwnStickers.own_stickers', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\032\n\030im.dlg.grpc.GrpcResponse'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=924,
  serialized_end=1029,
)


_REQUESTLOADACESSSIBLESTICKERS = _descriptor.Descriptor(
  name='RequestLoadAcesssibleStickers',
  full_name='dialog.RequestLoadAcesssibleStickers',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\031\n\027im.dlg.grpc.GrpcRequest'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1031,
  serialized_end=1092,
)


_RESPONSELOADACESSSIBLESTICKERS = _descriptor.Descriptor(
  name='ResponseLoadAcesssibleStickers',
  full_name='dialog.ResponseLoadAcesssibleStickers',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='accessible_stickers', full_name='dialog.ResponseLoadAcesssibleStickers.accessible_stickers', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\032\n\030im.dlg.grpc.GrpcResponse'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1094,
  serialized_end=1213,
)


_REQUESTADDSTICKERPACKREFERENCE = _descriptor.Descriptor(
  name='RequestAddStickerPackReference',
  full_name='dialog.RequestAddStickerPackReference',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='source_sticker_pack', full_name='dialog.RequestAddStickerPackReference.source_sticker_pack', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\031\n\027im.dlg.grpc.GrpcRequest'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1215,
  serialized_end=1321,
)


_REQUESTREMOVESTICKERPACKREFERENCE = _descriptor.Descriptor(
  name='RequestRemoveStickerPackReference',
  full_name='dialog.RequestRemoveStickerPackReference',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='source_sticker_pack', full_name='dialog.RequestRemoveStickerPackReference.source_sticker_pack', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\031\n\027im.dlg.grpc.GrpcRequest'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1323,
  serialized_end=1432,
)


_UPDATESTICKERCOLLECTIONSCHANGED = _descriptor.Descriptor(
  name='UpdateStickerCollectionsChanged',
  full_name='dialog.UpdateStickerCollectionsChanged',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='updated_collections', full_name='dialog.UpdateStickerCollectionsChanged.updated_collections', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1434,
  serialized_end=1538,
)


_UPDATESTICKERPACKREMOVED = _descriptor.Descriptor(
  name='UpdateStickerPackRemoved',
  full_name='dialog.UpdateStickerPackRemoved',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pack_id', full_name='dialog.UpdateStickerPackRemoved.pack_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1540,
  serialized_end=1598,
)


_UPDATESTICKERPACKADDED = _descriptor.Descriptor(
  name='UpdateStickerPackAdded',
  full_name='dialog.UpdateStickerPackAdded',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pack', full_name='dialog.UpdateStickerPackAdded.pack', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1600,
  serialized_end=1680,
)


_REQUESTADDSTICKERCOLLECTION = _descriptor.Descriptor(
  name='RequestAddStickerCollection',
  full_name='dialog.RequestAddStickerCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='dialog.RequestAddStickerCollection.title', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\031\n\027im.dlg.grpc.GrpcRequest'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1682,
  serialized_end=1771,
)


_REQUESTREMOVESTICKERCOLLECTION = _descriptor.Descriptor(
  name='RequestRemoveStickerCollection',
  full_name='dialog.RequestRemoveStickerCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='dialog.RequestRemoveStickerCollection.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\031\n\027im.dlg.grpc.GrpcRequest'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1773,
  serialized_end=1862,
)


_REQUESTLOADSTICKERCOLLECTION = _descriptor.Descriptor(
  name='RequestLoadStickerCollection',
  full_name='dialog.RequestLoadStickerCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='dialog.RequestLoadStickerCollection.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\031\n\027im.dlg.grpc.GrpcRequest'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1864,
  serialized_end=1951,
)


_RESPONSELOADSTICKERCOLLECTION = _descriptor.Descriptor(
  name='ResponseLoadStickerCollection',
  full_name='dialog.ResponseLoadStickerCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='collection', full_name='dialog.ResponseLoadStickerCollection.collection', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\032\n\030im.dlg.grpc.GrpcResponse'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1953,
  serialized_end=2062,
)

_STICKERDESCRIPTOR.fields_by_name['emoji'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_STICKERDESCRIPTOR.fields_by_name['image_128'].message_type = media__and__files__pb2._IMAGELOCATION
_STICKERDESCRIPTOR.fields_by_name['image_512'].message_type = media__and__files__pb2._IMAGELOCATION
_STICKERDESCRIPTOR.fields_by_name['image_256'].message_type = media__and__files__pb2._IMAGELOCATION
_STICKERCOLLECTION.fields_by_name['title'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_STICKERCOLLECTION.fields_by_name['stickers'].message_type = _STICKERDESCRIPTOR
_STICKERCOLLECTION.fields_by_name['owned_by_me'].message_type = google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE
_RESPONSESTICKERSRESPONSE.fields_by_name['collections'].message_type = _STICKERCOLLECTION
_RESPONSELOADOWNSTICKERS.fields_by_name['own_stickers'].message_type = _STICKERCOLLECTION
_RESPONSELOADACESSSIBLESTICKERS.fields_by_name['accessible_stickers'].message_type = _STICKERCOLLECTION
_UPDATESTICKERCOLLECTIONSCHANGED.fields_by_name['updated_collections'].message_type = _STICKERCOLLECTION
_UPDATESTICKERPACKADDED.fields_by_name['pack'].message_type = _STICKERCOLLECTION
_RESPONSELOADSTICKERCOLLECTION.fields_by_name['collection'].message_type = _STICKERCOLLECTION
DESCRIPTOR.message_types_by_name['StickerDescriptor'] = _STICKERDESCRIPTOR
DESCRIPTOR.message_types_by_name['StickerCollection'] = _STICKERCOLLECTION
DESCRIPTOR.message_types_by_name['ResponseStickersResponse'] = _RESPONSESTICKERSRESPONSE
DESCRIPTOR.message_types_by_name['RequestLoadOwnStickers'] = _REQUESTLOADOWNSTICKERS
DESCRIPTOR.message_types_by_name['ResponseLoadOwnStickers'] = _RESPONSELOADOWNSTICKERS
DESCRIPTOR.message_types_by_name['RequestLoadAcesssibleStickers'] = _REQUESTLOADACESSSIBLESTICKERS
DESCRIPTOR.message_types_by_name['ResponseLoadAcesssibleStickers'] = _RESPONSELOADACESSSIBLESTICKERS
DESCRIPTOR.message_types_by_name['RequestAddStickerPackReference'] = _REQUESTADDSTICKERPACKREFERENCE
DESCRIPTOR.message_types_by_name['RequestRemoveStickerPackReference'] = _REQUESTREMOVESTICKERPACKREFERENCE
DESCRIPTOR.message_types_by_name['UpdateStickerCollectionsChanged'] = _UPDATESTICKERCOLLECTIONSCHANGED
DESCRIPTOR.message_types_by_name['UpdateStickerPackRemoved'] = _UPDATESTICKERPACKREMOVED
DESCRIPTOR.message_types_by_name['UpdateStickerPackAdded'] = _UPDATESTICKERPACKADDED
DESCRIPTOR.message_types_by_name['RequestAddStickerCollection'] = _REQUESTADDSTICKERCOLLECTION
DESCRIPTOR.message_types_by_name['RequestRemoveStickerCollection'] = _REQUESTREMOVESTICKERCOLLECTION
DESCRIPTOR.message_types_by_name['RequestLoadStickerCollection'] = _REQUESTLOADSTICKERCOLLECTION
DESCRIPTOR.message_types_by_name['ResponseLoadStickerCollection'] = _RESPONSELOADSTICKERCOLLECTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StickerDescriptor = _reflection.GeneratedProtocolMessageType('StickerDescriptor', (_message.Message,), dict(
  DESCRIPTOR = _STICKERDESCRIPTOR,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.StickerDescriptor)
  ))
_sym_db.RegisterMessage(StickerDescriptor)

StickerCollection = _reflection.GeneratedProtocolMessageType('StickerCollection', (_message.Message,), dict(
  DESCRIPTOR = _STICKERCOLLECTION,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.StickerCollection)
  ))
_sym_db.RegisterMessage(StickerCollection)

ResponseStickersResponse = _reflection.GeneratedProtocolMessageType('ResponseStickersResponse', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSESTICKERSRESPONSE,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.ResponseStickersResponse)
  ))
_sym_db.RegisterMessage(ResponseStickersResponse)

RequestLoadOwnStickers = _reflection.GeneratedProtocolMessageType('RequestLoadOwnStickers', (_message.Message,), dict(
  DESCRIPTOR = _REQUESTLOADOWNSTICKERS,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.RequestLoadOwnStickers)
  ))
_sym_db.RegisterMessage(RequestLoadOwnStickers)

ResponseLoadOwnStickers = _reflection.GeneratedProtocolMessageType('ResponseLoadOwnStickers', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSELOADOWNSTICKERS,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.ResponseLoadOwnStickers)
  ))
_sym_db.RegisterMessage(ResponseLoadOwnStickers)

RequestLoadAcesssibleStickers = _reflection.GeneratedProtocolMessageType('RequestLoadAcesssibleStickers', (_message.Message,), dict(
  DESCRIPTOR = _REQUESTLOADACESSSIBLESTICKERS,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.RequestLoadAcesssibleStickers)
  ))
_sym_db.RegisterMessage(RequestLoadAcesssibleStickers)

ResponseLoadAcesssibleStickers = _reflection.GeneratedProtocolMessageType('ResponseLoadAcesssibleStickers', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSELOADACESSSIBLESTICKERS,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.ResponseLoadAcesssibleStickers)
  ))
_sym_db.RegisterMessage(ResponseLoadAcesssibleStickers)

RequestAddStickerPackReference = _reflection.GeneratedProtocolMessageType('RequestAddStickerPackReference', (_message.Message,), dict(
  DESCRIPTOR = _REQUESTADDSTICKERPACKREFERENCE,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.RequestAddStickerPackReference)
  ))
_sym_db.RegisterMessage(RequestAddStickerPackReference)

RequestRemoveStickerPackReference = _reflection.GeneratedProtocolMessageType('RequestRemoveStickerPackReference', (_message.Message,), dict(
  DESCRIPTOR = _REQUESTREMOVESTICKERPACKREFERENCE,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.RequestRemoveStickerPackReference)
  ))
_sym_db.RegisterMessage(RequestRemoveStickerPackReference)

UpdateStickerCollectionsChanged = _reflection.GeneratedProtocolMessageType('UpdateStickerCollectionsChanged', (_message.Message,), dict(
  DESCRIPTOR = _UPDATESTICKERCOLLECTIONSCHANGED,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.UpdateStickerCollectionsChanged)
  ))
_sym_db.RegisterMessage(UpdateStickerCollectionsChanged)

UpdateStickerPackRemoved = _reflection.GeneratedProtocolMessageType('UpdateStickerPackRemoved', (_message.Message,), dict(
  DESCRIPTOR = _UPDATESTICKERPACKREMOVED,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.UpdateStickerPackRemoved)
  ))
_sym_db.RegisterMessage(UpdateStickerPackRemoved)

UpdateStickerPackAdded = _reflection.GeneratedProtocolMessageType('UpdateStickerPackAdded', (_message.Message,), dict(
  DESCRIPTOR = _UPDATESTICKERPACKADDED,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.UpdateStickerPackAdded)
  ))
_sym_db.RegisterMessage(UpdateStickerPackAdded)

RequestAddStickerCollection = _reflection.GeneratedProtocolMessageType('RequestAddStickerCollection', (_message.Message,), dict(
  DESCRIPTOR = _REQUESTADDSTICKERCOLLECTION,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.RequestAddStickerCollection)
  ))
_sym_db.RegisterMessage(RequestAddStickerCollection)

RequestRemoveStickerCollection = _reflection.GeneratedProtocolMessageType('RequestRemoveStickerCollection', (_message.Message,), dict(
  DESCRIPTOR = _REQUESTREMOVESTICKERCOLLECTION,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.RequestRemoveStickerCollection)
  ))
_sym_db.RegisterMessage(RequestRemoveStickerCollection)

RequestLoadStickerCollection = _reflection.GeneratedProtocolMessageType('RequestLoadStickerCollection', (_message.Message,), dict(
  DESCRIPTOR = _REQUESTLOADSTICKERCOLLECTION,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.RequestLoadStickerCollection)
  ))
_sym_db.RegisterMessage(RequestLoadStickerCollection)

ResponseLoadStickerCollection = _reflection.GeneratedProtocolMessageType('ResponseLoadStickerCollection', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSELOADSTICKERCOLLECTION,
  __module__ = 'stickers_pb2'
  # @@protoc_insertion_point(class_scope:dialog.ResponseLoadStickerCollection)
  ))
_sym_db.RegisterMessage(ResponseLoadStickerCollection)


DESCRIPTOR._options = None
_STICKERDESCRIPTOR.fields_by_name['id']._options = None
_STICKERDESCRIPTOR.fields_by_name['emoji']._options = None
_STICKERDESCRIPTOR.fields_by_name['image_128']._options = None
_STICKERDESCRIPTOR.fields_by_name['image_512']._options = None
_STICKERDESCRIPTOR.fields_by_name['image_256']._options = None
_STICKERCOLLECTION.fields_by_name['id']._options = None
_STICKERCOLLECTION.fields_by_name['title']._options = None
_STICKERCOLLECTION.fields_by_name['stickers']._options = None
_STICKERCOLLECTION.fields_by_name['owned_by_me']._options = None
_RESPONSESTICKERSRESPONSE.fields_by_name['collections']._options = None
_RESPONSESTICKERSRESPONSE.fields_by_name['seq']._options = None
_RESPONSESTICKERSRESPONSE.fields_by_name['state']._options = None
_RESPONSESTICKERSRESPONSE._options = None
_REQUESTLOADOWNSTICKERS._options = None
_RESPONSELOADOWNSTICKERS._options = None
_REQUESTLOADACESSSIBLESTICKERS._options = None
_RESPONSELOADACESSSIBLESTICKERS._options = None
_REQUESTADDSTICKERPACKREFERENCE.fields_by_name['source_sticker_pack']._options = None
_REQUESTADDSTICKERPACKREFERENCE._options = None
_REQUESTREMOVESTICKERPACKREFERENCE.fields_by_name['source_sticker_pack']._options = None
_REQUESTREMOVESTICKERPACKREFERENCE._options = None
_UPDATESTICKERCOLLECTIONSCHANGED.fields_by_name['updated_collections']._options = None
_UPDATESTICKERPACKREMOVED.fields_by_name['pack_id']._options = None
_UPDATESTICKERPACKADDED.fields_by_name['pack']._options = None
_REQUESTADDSTICKERCOLLECTION.fields_by_name['title']._options = None
_REQUESTADDSTICKERCOLLECTION._options = None
_REQUESTREMOVESTICKERCOLLECTION.fields_by_name['id']._options = None
_REQUESTREMOVESTICKERCOLLECTION._options = None
_REQUESTLOADSTICKERCOLLECTION.fields_by_name['id']._options = None
_REQUESTLOADSTICKERCOLLECTION._options = None
_RESPONSELOADSTICKERCOLLECTION._options = None

_STICKERS = _descriptor.ServiceDescriptor(
  name='Stickers',
  full_name='dialog.Stickers',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=2065,
  serialized_end=3092,
  methods=[
  _descriptor.MethodDescriptor(
    name='LoadOwnStickers',
    full_name='dialog.Stickers.LoadOwnStickers',
    index=0,
    containing_service=None,
    input_type=_REQUESTLOADOWNSTICKERS,
    output_type=_RESPONSELOADOWNSTICKERS,
    serialized_options=_b('\202\323\344\223\002&\"!/v1/grpc/Stickers/LoadOwnStickers:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='LoadAcesssibleStickers',
    full_name='dialog.Stickers.LoadAcesssibleStickers',
    index=1,
    containing_service=None,
    input_type=_REQUESTLOADACESSSIBLESTICKERS,
    output_type=_RESPONSELOADACESSSIBLESTICKERS,
    serialized_options=_b('\202\323\344\223\002-\"(/v1/grpc/Stickers/LoadAcesssibleStickers:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='AddStickerPackReference',
    full_name='dialog.Stickers.AddStickerPackReference',
    index=2,
    containing_service=None,
    input_type=_REQUESTADDSTICKERPACKREFERENCE,
    output_type=miscellaneous__pb2._RESPONSESEQ,
    serialized_options=_b('\202\323\344\223\002.\")/v1/grpc/Stickers/AddStickerPackReference:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='RemoveStickerPackReference',
    full_name='dialog.Stickers.RemoveStickerPackReference',
    index=3,
    containing_service=None,
    input_type=_REQUESTREMOVESTICKERPACKREFERENCE,
    output_type=miscellaneous__pb2._RESPONSESEQ,
    serialized_options=_b('\202\323\344\223\0021\",/v1/grpc/Stickers/RemoveStickerPackReference:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='AddStickerCollection',
    full_name='dialog.Stickers.AddStickerCollection',
    index=4,
    containing_service=None,
    input_type=_REQUESTADDSTICKERCOLLECTION,
    output_type=miscellaneous__pb2._RESPONSESEQ,
    serialized_options=_b('\202\323\344\223\002+\"&/v1/grpc/Stickers/AddStickerCollection:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='RemoveStickerCollection',
    full_name='dialog.Stickers.RemoveStickerCollection',
    index=5,
    containing_service=None,
    input_type=_REQUESTREMOVESTICKERCOLLECTION,
    output_type=miscellaneous__pb2._RESPONSESEQ,
    serialized_options=_b('\202\323\344\223\002.\")/v1/grpc/Stickers/RemoveStickerCollection:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='LoadStickerCollection',
    full_name='dialog.Stickers.LoadStickerCollection',
    index=6,
    containing_service=None,
    input_type=_REQUESTLOADSTICKERCOLLECTION,
    output_type=_RESPONSELOADSTICKERCOLLECTION,
    serialized_options=_b('\202\323\344\223\002,\"\'/v1/grpc/Stickers/LoadStickerCollection:\001*'),
  ),
])
_sym_db.RegisterServiceDescriptor(_STICKERS)

DESCRIPTOR.services_by_name['Stickers'] = _STICKERS

# @@protoc_insertion_point(module_scope)
