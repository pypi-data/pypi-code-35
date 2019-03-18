# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gateway_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import obsolete_pb2 as obsolete__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='gateway_service.proto',
  package='dialog',
  syntax='proto3',
  serialized_options=_b('\242\002\003API\272\002\003API'),
  serialized_pb=_b('\n\x15gateway_service.proto\x12\x06\x64ialog\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x0eobsolete.proto\"c\n\x14GetDifferenceCommand\x12(\n\x03seq\x18\x01 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\r\n\x05state\x18\x02 \x01(\x0c\x12\x12\n\nconfigHash\x18\x03 \x01(\x03\"P\n\rServiceUpdate\x12\x35\n\x0eobsoleteUpdate\x18\x01 \x01(\x0b\x32\x1b.google.protobuf.BytesValueH\x00\x42\x08\n\x06updateB\x0c\xa2\x02\x03\x41PI\xba\x02\x03\x41PIb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,obsolete__pb2.DESCRIPTOR,])




_GETDIFFERENCECOMMAND = _descriptor.Descriptor(
  name='GetDifferenceCommand',
  full_name='dialog.GetDifferenceCommand',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='seq', full_name='dialog.GetDifferenceCommand.seq', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='state', full_name='dialog.GetDifferenceCommand.state', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='configHash', full_name='dialog.GetDifferenceCommand.configHash', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=110,
  serialized_end=209,
)


_SERVICEUPDATE = _descriptor.Descriptor(
  name='ServiceUpdate',
  full_name='dialog.ServiceUpdate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='obsoleteUpdate', full_name='dialog.ServiceUpdate.obsoleteUpdate', index=0,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='update', full_name='dialog.ServiceUpdate.update',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=211,
  serialized_end=291,
)

_GETDIFFERENCECOMMAND.fields_by_name['seq'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT32VALUE
_SERVICEUPDATE.fields_by_name['obsoleteUpdate'].message_type = google_dot_protobuf_dot_wrappers__pb2._BYTESVALUE
_SERVICEUPDATE.oneofs_by_name['update'].fields.append(
  _SERVICEUPDATE.fields_by_name['obsoleteUpdate'])
_SERVICEUPDATE.fields_by_name['obsoleteUpdate'].containing_oneof = _SERVICEUPDATE.oneofs_by_name['update']
DESCRIPTOR.message_types_by_name['GetDifferenceCommand'] = _GETDIFFERENCECOMMAND
DESCRIPTOR.message_types_by_name['ServiceUpdate'] = _SERVICEUPDATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetDifferenceCommand = _reflection.GeneratedProtocolMessageType('GetDifferenceCommand', (_message.Message,), dict(
  DESCRIPTOR = _GETDIFFERENCECOMMAND,
  __module__ = 'gateway_service_pb2'
  # @@protoc_insertion_point(class_scope:dialog.GetDifferenceCommand)
  ))
_sym_db.RegisterMessage(GetDifferenceCommand)

ServiceUpdate = _reflection.GeneratedProtocolMessageType('ServiceUpdate', (_message.Message,), dict(
  DESCRIPTOR = _SERVICEUPDATE,
  __module__ = 'gateway_service_pb2'
  # @@protoc_insertion_point(class_scope:dialog.ServiceUpdate)
  ))
_sym_db.RegisterMessage(ServiceUpdate)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
