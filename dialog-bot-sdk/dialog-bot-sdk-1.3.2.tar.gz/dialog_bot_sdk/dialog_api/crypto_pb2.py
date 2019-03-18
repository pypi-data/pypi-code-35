# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: crypto.proto

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
from .scalapb import scalapb_pb2 as scalapb_dot_scalapb__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='crypto.proto',
  package='dialog',
  syntax='proto3',
  serialized_options=_b('\342?\026\n\024im.dlg.grpc.services'),
  serialized_pb=_b('\n\x0c\x63rypto.proto\x12\x06\x64ialog\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x11\x64\x65\x66initions.proto\x1a\x15scalapb/scalapb.proto\"r\n\x12RequestKeyExchange\x12>\n\nclient_key\x18\x01 \x01(\x0b\x32\x1b.google.protobuf.BytesValueB\r\x8a\xea\x30\t\n\x07\x63ompact:\x1c\xe2?\x19\n\x17im.dlg.grpc.GrpcRequest\"e\n\x13ResponseKeyExchange\x12/\n\nserver_key\x18\x01 \x01(\x0b\x32\x1b.google.protobuf.BytesValue:\x1d\xe2?\x1a\n\x18im.dlg.grpc.GrpcResponse2x\n\x06\x43rypto\x12n\n\x0bKeyExchange\x12\x1a.dialog.RequestKeyExchange\x1a\x1b.dialog.ResponseKeyExchange\"&\x82\xd3\xe4\x93\x02 \"\x1b/v1/grpc/Crypto/KeyExchange:\x01*B\x19\xe2?\x16\n\x14im.dlg.grpc.servicesb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,definitions__pb2.DESCRIPTOR,scalapb_dot_scalapb__pb2.DESCRIPTOR,])




_REQUESTKEYEXCHANGE = _descriptor.Descriptor(
  name='RequestKeyExchange',
  full_name='dialog.RequestKeyExchange',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='client_key', full_name='dialog.RequestKeyExchange.client_key', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007compact'), file=DESCRIPTOR),
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
  serialized_start=128,
  serialized_end=242,
)


_RESPONSEKEYEXCHANGE = _descriptor.Descriptor(
  name='ResponseKeyExchange',
  full_name='dialog.ResponseKeyExchange',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='server_key', full_name='dialog.ResponseKeyExchange.server_key', index=0,
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
  serialized_start=244,
  serialized_end=345,
)

_REQUESTKEYEXCHANGE.fields_by_name['client_key'].message_type = google_dot_protobuf_dot_wrappers__pb2._BYTESVALUE
_RESPONSEKEYEXCHANGE.fields_by_name['server_key'].message_type = google_dot_protobuf_dot_wrappers__pb2._BYTESVALUE
DESCRIPTOR.message_types_by_name['RequestKeyExchange'] = _REQUESTKEYEXCHANGE
DESCRIPTOR.message_types_by_name['ResponseKeyExchange'] = _RESPONSEKEYEXCHANGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RequestKeyExchange = _reflection.GeneratedProtocolMessageType('RequestKeyExchange', (_message.Message,), dict(
  DESCRIPTOR = _REQUESTKEYEXCHANGE,
  __module__ = 'crypto_pb2'
  # @@protoc_insertion_point(class_scope:dialog.RequestKeyExchange)
  ))
_sym_db.RegisterMessage(RequestKeyExchange)

ResponseKeyExchange = _reflection.GeneratedProtocolMessageType('ResponseKeyExchange', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSEKEYEXCHANGE,
  __module__ = 'crypto_pb2'
  # @@protoc_insertion_point(class_scope:dialog.ResponseKeyExchange)
  ))
_sym_db.RegisterMessage(ResponseKeyExchange)


DESCRIPTOR._options = None
_REQUESTKEYEXCHANGE.fields_by_name['client_key']._options = None
_REQUESTKEYEXCHANGE._options = None
_RESPONSEKEYEXCHANGE._options = None

_CRYPTO = _descriptor.ServiceDescriptor(
  name='Crypto',
  full_name='dialog.Crypto',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=347,
  serialized_end=467,
  methods=[
  _descriptor.MethodDescriptor(
    name='KeyExchange',
    full_name='dialog.Crypto.KeyExchange',
    index=0,
    containing_service=None,
    input_type=_REQUESTKEYEXCHANGE,
    output_type=_RESPONSEKEYEXCHANGE,
    serialized_options=_b('\202\323\344\223\002 \"\033/v1/grpc/Crypto/KeyExchange:\001*'),
  ),
])
_sym_db.RegisterServiceDescriptor(_CRYPTO)

DESCRIPTOR.services_by_name['Crypto'] = _CRYPTO

# @@protoc_insertion_point(module_scope)
