# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ava_engine/ava/service_api.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ava_engine.ava import engine_api_pb2 as ava__engine_dot_ava_dot_engine__api__pb2
from ava_engine.ava import images_api_pb2 as ava__engine_dot_ava_dot_images__api__pb2
from ava_engine.ava import feature_classification_pb2 as ava__engine_dot_ava_dot_feature__classification__pb2
from ava_engine.ava import feature_detection_pb2 as ava__engine_dot_ava_dot_feature__detection__pb2
from ava_engine.ava import feature_face_recognition_pb2 as ava__engine_dot_ava_dot_feature__face__recognition__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ava_engine/ava/service_api.proto',
  package='ava_engine',
  syntax='proto3',
  serialized_pb=_b('\n ava_engine/ava/service_api.proto\x12\nava_engine\x1a\x1f\x61va_engine/ava/engine_api.proto\x1a\x1f\x61va_engine/ava/images_api.proto\x1a+ava_engine/ava/feature_classification.proto\x1a&ava_engine/ava/feature_detection.proto\x1a-ava_engine/ava/feature_face_recognition.proto2\xab\x01\n\x0c\x45ngineApiDef\x12?\n\x06Status\x12\x19.ava_engine.StatusRequest\x1a\x1a.ava_engine.StatusResponse\x12Z\n\x0fPerformanceTest\x12\".ava_engine.PerformanceTestRequest\x1a#.ava_engine.PerformanceTestResponse2\xf9\x01\n\x0cImagesApiDef\x12\x45\n\x08GetImage\x12\x1b.ava_engine.GetImageRequest\x1a\x1c.ava_engine.GetImageResponse\x12O\n\rGetImageBytes\x12\x1b.ava_engine.GetImageRequest\x1a!.ava_engine.GetImageBytesResponse\x12Q\n\x0cSearchImages\x12\x1f.ava_engine.SearchImagesRequest\x1a .ava_engine.SearchImagesResponse2[\n\x14\x43lassificationApiDef\x12\x43\n\x06\x44\x65tect\x12\x1b.ava_engine.ClassifyRequest\x1a\x1c.ava_engine.ClassifyResponse2R\n\x0f\x44\x65tectionApiDef\x12?\n\x06\x44\x65tect\x12\x19.ava_engine.DetectRequest\x1a\x1a.ava_engine.DetectResponse2i\n\x15\x46\x61\x63\x65RecognitionApiDef\x12P\n\tRecognize\x12 .ava_engine.RecognizeFaceRequest\x1a!.ava_engine.RecognizeFaceResponseB#\n!com.imageintelligence.engine.grpcb\x06proto3')
  ,
  dependencies=[ava__engine_dot_ava_dot_engine__api__pb2.DESCRIPTOR,ava__engine_dot_ava_dot_images__api__pb2.DESCRIPTOR,ava__engine_dot_ava_dot_feature__classification__pb2.DESCRIPTOR,ava__engine_dot_ava_dot_feature__detection__pb2.DESCRIPTOR,ava__engine_dot_ava_dot_feature__face__recognition__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n!com.imageintelligence.engine.grpc'))

_ENGINEAPIDEF = _descriptor.ServiceDescriptor(
  name='EngineApiDef',
  full_name='ava_engine.EngineApiDef',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=247,
  serialized_end=418,
  methods=[
  _descriptor.MethodDescriptor(
    name='Status',
    full_name='ava_engine.EngineApiDef.Status',
    index=0,
    containing_service=None,
    input_type=ava__engine_dot_ava_dot_engine__api__pb2._STATUSREQUEST,
    output_type=ava__engine_dot_ava_dot_engine__api__pb2._STATUSRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='PerformanceTest',
    full_name='ava_engine.EngineApiDef.PerformanceTest',
    index=1,
    containing_service=None,
    input_type=ava__engine_dot_ava_dot_engine__api__pb2._PERFORMANCETESTREQUEST,
    output_type=ava__engine_dot_ava_dot_engine__api__pb2._PERFORMANCETESTRESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_ENGINEAPIDEF)

DESCRIPTOR.services_by_name['EngineApiDef'] = _ENGINEAPIDEF


_IMAGESAPIDEF = _descriptor.ServiceDescriptor(
  name='ImagesApiDef',
  full_name='ava_engine.ImagesApiDef',
  file=DESCRIPTOR,
  index=1,
  options=None,
  serialized_start=421,
  serialized_end=670,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetImage',
    full_name='ava_engine.ImagesApiDef.GetImage',
    index=0,
    containing_service=None,
    input_type=ava__engine_dot_ava_dot_images__api__pb2._GETIMAGEREQUEST,
    output_type=ava__engine_dot_ava_dot_images__api__pb2._GETIMAGERESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetImageBytes',
    full_name='ava_engine.ImagesApiDef.GetImageBytes',
    index=1,
    containing_service=None,
    input_type=ava__engine_dot_ava_dot_images__api__pb2._GETIMAGEREQUEST,
    output_type=ava__engine_dot_ava_dot_images__api__pb2._GETIMAGEBYTESRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SearchImages',
    full_name='ava_engine.ImagesApiDef.SearchImages',
    index=2,
    containing_service=None,
    input_type=ava__engine_dot_ava_dot_images__api__pb2._SEARCHIMAGESREQUEST,
    output_type=ava__engine_dot_ava_dot_images__api__pb2._SEARCHIMAGESRESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_IMAGESAPIDEF)

DESCRIPTOR.services_by_name['ImagesApiDef'] = _IMAGESAPIDEF


_CLASSIFICATIONAPIDEF = _descriptor.ServiceDescriptor(
  name='ClassificationApiDef',
  full_name='ava_engine.ClassificationApiDef',
  file=DESCRIPTOR,
  index=2,
  options=None,
  serialized_start=672,
  serialized_end=763,
  methods=[
  _descriptor.MethodDescriptor(
    name='Detect',
    full_name='ava_engine.ClassificationApiDef.Detect',
    index=0,
    containing_service=None,
    input_type=ava__engine_dot_ava_dot_feature__classification__pb2._CLASSIFYREQUEST,
    output_type=ava__engine_dot_ava_dot_feature__classification__pb2._CLASSIFYRESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CLASSIFICATIONAPIDEF)

DESCRIPTOR.services_by_name['ClassificationApiDef'] = _CLASSIFICATIONAPIDEF


_DETECTIONAPIDEF = _descriptor.ServiceDescriptor(
  name='DetectionApiDef',
  full_name='ava_engine.DetectionApiDef',
  file=DESCRIPTOR,
  index=3,
  options=None,
  serialized_start=765,
  serialized_end=847,
  methods=[
  _descriptor.MethodDescriptor(
    name='Detect',
    full_name='ava_engine.DetectionApiDef.Detect',
    index=0,
    containing_service=None,
    input_type=ava__engine_dot_ava_dot_feature__detection__pb2._DETECTREQUEST,
    output_type=ava__engine_dot_ava_dot_feature__detection__pb2._DETECTRESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_DETECTIONAPIDEF)

DESCRIPTOR.services_by_name['DetectionApiDef'] = _DETECTIONAPIDEF


_FACERECOGNITIONAPIDEF = _descriptor.ServiceDescriptor(
  name='FaceRecognitionApiDef',
  full_name='ava_engine.FaceRecognitionApiDef',
  file=DESCRIPTOR,
  index=4,
  options=None,
  serialized_start=849,
  serialized_end=954,
  methods=[
  _descriptor.MethodDescriptor(
    name='Recognize',
    full_name='ava_engine.FaceRecognitionApiDef.Recognize',
    index=0,
    containing_service=None,
    input_type=ava__engine_dot_ava_dot_feature__face__recognition__pb2._RECOGNIZEFACEREQUEST,
    output_type=ava__engine_dot_ava_dot_feature__face__recognition__pb2._RECOGNIZEFACERESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_FACERECOGNITIONAPIDEF)

DESCRIPTOR.services_by_name['FaceRecognitionApiDef'] = _FACERECOGNITIONAPIDEF

# @@protoc_insertion_point(module_scope)
