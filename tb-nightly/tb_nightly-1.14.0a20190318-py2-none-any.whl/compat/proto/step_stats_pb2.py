# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/compat/proto/step_stats.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorboard.compat.proto import allocation_description_pb2 as tensorboard_dot_compat_dot_proto_dot_allocation__description__pb2
from tensorboard.compat.proto import tensor_description_pb2 as tensorboard_dot_compat_dot_proto_dot_tensor__description__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorboard/compat/proto/step_stats.proto',
  package='tensorboard',
  syntax='proto3',
  serialized_options=_b('\n\030org.tensorflow.frameworkB\017StepStatsProtosP\001Z=github.com/tensorflow/tensorflow/tensorflow/go/core/framework\370\001\001'),
  serialized_pb=_b('\n)tensorboard/compat/proto/step_stats.proto\x12\x0btensorboard\x1a\x35tensorboard/compat/proto/allocation_description.proto\x1a\x31tensorboard/compat/proto/tensor_description.proto\"=\n\x10\x41llocationRecord\x12\x14\n\x0c\x61lloc_micros\x18\x01 \x01(\x03\x12\x13\n\x0b\x61lloc_bytes\x18\x02 \x01(\x03\"\xc5\x01\n\x13\x41llocatorMemoryUsed\x12\x16\n\x0e\x61llocator_name\x18\x01 \x01(\t\x12\x13\n\x0btotal_bytes\x18\x02 \x01(\x03\x12\x12\n\npeak_bytes\x18\x03 \x01(\x03\x12\x12\n\nlive_bytes\x18\x04 \x01(\x03\x12\x39\n\x12\x61llocation_records\x18\x06 \x03(\x0b\x32\x1d.tensorboard.AllocationRecord\x12\x1e\n\x16\x61llocator_bytes_in_use\x18\x05 \x01(\x03\"V\n\nNodeOutput\x12\x0c\n\x04slot\x18\x01 \x01(\x05\x12:\n\x12tensor_description\x18\x03 \x01(\x0b\x32\x1e.tensorboard.TensorDescription\"\xec\x01\n\x0bMemoryStats\x12\x18\n\x10temp_memory_size\x18\x01 \x01(\x03\x12\x1e\n\x16persistent_memory_size\x18\x03 \x01(\x03\x12#\n\x1bpersistent_tensor_alloc_ids\x18\x05 \x03(\x03\x12#\n\x17\x64\x65vice_temp_memory_size\x18\x02 \x01(\x03\x42\x02\x18\x01\x12)\n\x1d\x64\x65vice_persistent_memory_size\x18\x04 \x01(\x03\x42\x02\x18\x01\x12.\n\"device_persistent_tensor_alloc_ids\x18\x06 \x03(\x03\x42\x02\x18\x01\"\xa2\x04\n\rNodeExecStats\x12\x11\n\tnode_name\x18\x01 \x01(\t\x12\x18\n\x10\x61ll_start_micros\x18\x02 \x01(\x03\x12\x1b\n\x13op_start_rel_micros\x18\x03 \x01(\x03\x12\x19\n\x11op_end_rel_micros\x18\x04 \x01(\x03\x12\x1a\n\x12\x61ll_end_rel_micros\x18\x05 \x01(\x03\x12\x30\n\x06memory\x18\x06 \x03(\x0b\x32 .tensorboard.AllocatorMemoryUsed\x12\'\n\x06output\x18\x07 \x03(\x0b\x32\x17.tensorboard.NodeOutput\x12\x16\n\x0etimeline_label\x18\x08 \x01(\t\x12\x18\n\x10scheduled_micros\x18\t \x01(\x03\x12\x11\n\tthread_id\x18\n \x01(\r\x12=\n\x11referenced_tensor\x18\x0b \x03(\x0b\x32\".tensorboard.AllocationDescription\x12.\n\x0cmemory_stats\x18\x0c \x01(\x0b\x32\x18.tensorboard.MemoryStats\x12\x17\n\x0f\x61ll_start_nanos\x18\r \x01(\x03\x12\x1a\n\x12op_start_rel_nanos\x18\x0e \x01(\x03\x12\x18\n\x10op_end_rel_nanos\x18\x0f \x01(\x03\x12\x19\n\x11\x61ll_end_rel_nanos\x18\x10 \x01(\x03\x12\x17\n\x0fscheduled_nanos\x18\x11 \x01(\x03\"\xca\x01\n\x0f\x44\x65viceStepStats\x12\x0e\n\x06\x64\x65vice\x18\x01 \x01(\t\x12.\n\nnode_stats\x18\x02 \x03(\x0b\x32\x1a.tensorboard.NodeExecStats\x12\x43\n\x0cthread_names\x18\x03 \x03(\x0b\x32-.tensorboard.DeviceStepStats.ThreadNamesEntry\x1a\x32\n\x10ThreadNamesEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"<\n\tStepStats\x12/\n\tdev_stats\x18\x01 \x03(\x0b\x32\x1c.tensorboard.DeviceStepStatsBo\n\x18org.tensorflow.frameworkB\x0fStepStatsProtosP\x01Z=github.com/tensorflow/tensorflow/tensorflow/go/core/framework\xf8\x01\x01\x62\x06proto3')
  ,
  dependencies=[tensorboard_dot_compat_dot_proto_dot_allocation__description__pb2.DESCRIPTOR,tensorboard_dot_compat_dot_proto_dot_tensor__description__pb2.DESCRIPTOR,])




_ALLOCATIONRECORD = _descriptor.Descriptor(
  name='AllocationRecord',
  full_name='tensorboard.AllocationRecord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='alloc_micros', full_name='tensorboard.AllocationRecord.alloc_micros', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='alloc_bytes', full_name='tensorboard.AllocationRecord.alloc_bytes', index=1,
      number=2, type=3, cpp_type=2, label=1,
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
  serialized_start=164,
  serialized_end=225,
)


_ALLOCATORMEMORYUSED = _descriptor.Descriptor(
  name='AllocatorMemoryUsed',
  full_name='tensorboard.AllocatorMemoryUsed',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='allocator_name', full_name='tensorboard.AllocatorMemoryUsed.allocator_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='total_bytes', full_name='tensorboard.AllocatorMemoryUsed.total_bytes', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='peak_bytes', full_name='tensorboard.AllocatorMemoryUsed.peak_bytes', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='live_bytes', full_name='tensorboard.AllocatorMemoryUsed.live_bytes', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='allocation_records', full_name='tensorboard.AllocatorMemoryUsed.allocation_records', index=4,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='allocator_bytes_in_use', full_name='tensorboard.AllocatorMemoryUsed.allocator_bytes_in_use', index=5,
      number=5, type=3, cpp_type=2, label=1,
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
  serialized_start=228,
  serialized_end=425,
)


_NODEOUTPUT = _descriptor.Descriptor(
  name='NodeOutput',
  full_name='tensorboard.NodeOutput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='slot', full_name='tensorboard.NodeOutput.slot', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tensor_description', full_name='tensorboard.NodeOutput.tensor_description', index=1,
      number=3, type=11, cpp_type=10, label=1,
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
  ],
  serialized_start=427,
  serialized_end=513,
)


_MEMORYSTATS = _descriptor.Descriptor(
  name='MemoryStats',
  full_name='tensorboard.MemoryStats',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='temp_memory_size', full_name='tensorboard.MemoryStats.temp_memory_size', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='persistent_memory_size', full_name='tensorboard.MemoryStats.persistent_memory_size', index=1,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='persistent_tensor_alloc_ids', full_name='tensorboard.MemoryStats.persistent_tensor_alloc_ids', index=2,
      number=5, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_temp_memory_size', full_name='tensorboard.MemoryStats.device_temp_memory_size', index=3,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\030\001'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_persistent_memory_size', full_name='tensorboard.MemoryStats.device_persistent_memory_size', index=4,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\030\001'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_persistent_tensor_alloc_ids', full_name='tensorboard.MemoryStats.device_persistent_tensor_alloc_ids', index=5,
      number=6, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\030\001'), file=DESCRIPTOR),
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
  serialized_start=516,
  serialized_end=752,
)


_NODEEXECSTATS = _descriptor.Descriptor(
  name='NodeExecStats',
  full_name='tensorboard.NodeExecStats',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='node_name', full_name='tensorboard.NodeExecStats.node_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='all_start_micros', full_name='tensorboard.NodeExecStats.all_start_micros', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='op_start_rel_micros', full_name='tensorboard.NodeExecStats.op_start_rel_micros', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='op_end_rel_micros', full_name='tensorboard.NodeExecStats.op_end_rel_micros', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='all_end_rel_micros', full_name='tensorboard.NodeExecStats.all_end_rel_micros', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='memory', full_name='tensorboard.NodeExecStats.memory', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='output', full_name='tensorboard.NodeExecStats.output', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeline_label', full_name='tensorboard.NodeExecStats.timeline_label', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='scheduled_micros', full_name='tensorboard.NodeExecStats.scheduled_micros', index=8,
      number=9, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='thread_id', full_name='tensorboard.NodeExecStats.thread_id', index=9,
      number=10, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='referenced_tensor', full_name='tensorboard.NodeExecStats.referenced_tensor', index=10,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='memory_stats', full_name='tensorboard.NodeExecStats.memory_stats', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='all_start_nanos', full_name='tensorboard.NodeExecStats.all_start_nanos', index=12,
      number=13, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='op_start_rel_nanos', full_name='tensorboard.NodeExecStats.op_start_rel_nanos', index=13,
      number=14, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='op_end_rel_nanos', full_name='tensorboard.NodeExecStats.op_end_rel_nanos', index=14,
      number=15, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='all_end_rel_nanos', full_name='tensorboard.NodeExecStats.all_end_rel_nanos', index=15,
      number=16, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='scheduled_nanos', full_name='tensorboard.NodeExecStats.scheduled_nanos', index=16,
      number=17, type=3, cpp_type=2, label=1,
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
  serialized_start=755,
  serialized_end=1301,
)


_DEVICESTEPSTATS_THREADNAMESENTRY = _descriptor.Descriptor(
  name='ThreadNamesEntry',
  full_name='tensorboard.DeviceStepStats.ThreadNamesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='tensorboard.DeviceStepStats.ThreadNamesEntry.key', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='tensorboard.DeviceStepStats.ThreadNamesEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1456,
  serialized_end=1506,
)

_DEVICESTEPSTATS = _descriptor.Descriptor(
  name='DeviceStepStats',
  full_name='tensorboard.DeviceStepStats',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device', full_name='tensorboard.DeviceStepStats.device', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='node_stats', full_name='tensorboard.DeviceStepStats.node_stats', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='thread_names', full_name='tensorboard.DeviceStepStats.thread_names', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_DEVICESTEPSTATS_THREADNAMESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1304,
  serialized_end=1506,
)


_STEPSTATS = _descriptor.Descriptor(
  name='StepStats',
  full_name='tensorboard.StepStats',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dev_stats', full_name='tensorboard.StepStats.dev_stats', index=0,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1508,
  serialized_end=1568,
)

_ALLOCATORMEMORYUSED.fields_by_name['allocation_records'].message_type = _ALLOCATIONRECORD
_NODEOUTPUT.fields_by_name['tensor_description'].message_type = tensorboard_dot_compat_dot_proto_dot_tensor__description__pb2._TENSORDESCRIPTION
_NODEEXECSTATS.fields_by_name['memory'].message_type = _ALLOCATORMEMORYUSED
_NODEEXECSTATS.fields_by_name['output'].message_type = _NODEOUTPUT
_NODEEXECSTATS.fields_by_name['referenced_tensor'].message_type = tensorboard_dot_compat_dot_proto_dot_allocation__description__pb2._ALLOCATIONDESCRIPTION
_NODEEXECSTATS.fields_by_name['memory_stats'].message_type = _MEMORYSTATS
_DEVICESTEPSTATS_THREADNAMESENTRY.containing_type = _DEVICESTEPSTATS
_DEVICESTEPSTATS.fields_by_name['node_stats'].message_type = _NODEEXECSTATS
_DEVICESTEPSTATS.fields_by_name['thread_names'].message_type = _DEVICESTEPSTATS_THREADNAMESENTRY
_STEPSTATS.fields_by_name['dev_stats'].message_type = _DEVICESTEPSTATS
DESCRIPTOR.message_types_by_name['AllocationRecord'] = _ALLOCATIONRECORD
DESCRIPTOR.message_types_by_name['AllocatorMemoryUsed'] = _ALLOCATORMEMORYUSED
DESCRIPTOR.message_types_by_name['NodeOutput'] = _NODEOUTPUT
DESCRIPTOR.message_types_by_name['MemoryStats'] = _MEMORYSTATS
DESCRIPTOR.message_types_by_name['NodeExecStats'] = _NODEEXECSTATS
DESCRIPTOR.message_types_by_name['DeviceStepStats'] = _DEVICESTEPSTATS
DESCRIPTOR.message_types_by_name['StepStats'] = _STEPSTATS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AllocationRecord = _reflection.GeneratedProtocolMessageType('AllocationRecord', (_message.Message,), dict(
  DESCRIPTOR = _ALLOCATIONRECORD,
  __module__ = 'tensorboard.compat.proto.step_stats_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.AllocationRecord)
  ))
_sym_db.RegisterMessage(AllocationRecord)

AllocatorMemoryUsed = _reflection.GeneratedProtocolMessageType('AllocatorMemoryUsed', (_message.Message,), dict(
  DESCRIPTOR = _ALLOCATORMEMORYUSED,
  __module__ = 'tensorboard.compat.proto.step_stats_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.AllocatorMemoryUsed)
  ))
_sym_db.RegisterMessage(AllocatorMemoryUsed)

NodeOutput = _reflection.GeneratedProtocolMessageType('NodeOutput', (_message.Message,), dict(
  DESCRIPTOR = _NODEOUTPUT,
  __module__ = 'tensorboard.compat.proto.step_stats_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.NodeOutput)
  ))
_sym_db.RegisterMessage(NodeOutput)

MemoryStats = _reflection.GeneratedProtocolMessageType('MemoryStats', (_message.Message,), dict(
  DESCRIPTOR = _MEMORYSTATS,
  __module__ = 'tensorboard.compat.proto.step_stats_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.MemoryStats)
  ))
_sym_db.RegisterMessage(MemoryStats)

NodeExecStats = _reflection.GeneratedProtocolMessageType('NodeExecStats', (_message.Message,), dict(
  DESCRIPTOR = _NODEEXECSTATS,
  __module__ = 'tensorboard.compat.proto.step_stats_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.NodeExecStats)
  ))
_sym_db.RegisterMessage(NodeExecStats)

DeviceStepStats = _reflection.GeneratedProtocolMessageType('DeviceStepStats', (_message.Message,), dict(

  ThreadNamesEntry = _reflection.GeneratedProtocolMessageType('ThreadNamesEntry', (_message.Message,), dict(
    DESCRIPTOR = _DEVICESTEPSTATS_THREADNAMESENTRY,
    __module__ = 'tensorboard.compat.proto.step_stats_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.DeviceStepStats.ThreadNamesEntry)
    ))
  ,
  DESCRIPTOR = _DEVICESTEPSTATS,
  __module__ = 'tensorboard.compat.proto.step_stats_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.DeviceStepStats)
  ))
_sym_db.RegisterMessage(DeviceStepStats)
_sym_db.RegisterMessage(DeviceStepStats.ThreadNamesEntry)

StepStats = _reflection.GeneratedProtocolMessageType('StepStats', (_message.Message,), dict(
  DESCRIPTOR = _STEPSTATS,
  __module__ = 'tensorboard.compat.proto.step_stats_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.StepStats)
  ))
_sym_db.RegisterMessage(StepStats)


DESCRIPTOR._options = None
_MEMORYSTATS.fields_by_name['device_temp_memory_size']._options = None
_MEMORYSTATS.fields_by_name['device_persistent_memory_size']._options = None
_MEMORYSTATS.fields_by_name['device_persistent_tensor_alloc_ids']._options = None
_DEVICESTEPSTATS_THREADNAMESENTRY._options = None
# @@protoc_insertion_point(module_scope)
