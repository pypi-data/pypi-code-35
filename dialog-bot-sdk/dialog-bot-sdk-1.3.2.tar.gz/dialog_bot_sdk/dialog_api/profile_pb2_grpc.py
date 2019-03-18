# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import miscellaneous_pb2 as miscellaneous__pb2
from . import profile_pb2 as profile__pb2


class ProfileStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.EditName = channel.unary_unary(
        '/dialog.Profile/EditName',
        request_serializer=profile__pb2.RequestEditName.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeq.FromString,
        )
    self.EditNickName = channel.unary_unary(
        '/dialog.Profile/EditNickName',
        request_serializer=profile__pb2.RequestEditNickName.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeq.FromString,
        )
    self.CheckNickName = channel.unary_unary(
        '/dialog.Profile/CheckNickName',
        request_serializer=profile__pb2.RequestCheckNickName.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseBool.FromString,
        )
    self.EditAbout = channel.unary_unary(
        '/dialog.Profile/EditAbout',
        request_serializer=profile__pb2.RequestEditAbout.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeq.FromString,
        )
    self.EditAvatar = channel.unary_unary(
        '/dialog.Profile/EditAvatar',
        request_serializer=profile__pb2.RequestEditAvatar.SerializeToString,
        response_deserializer=profile__pb2.ResponseEditAvatar.FromString,
        )
    self.RemoveAvatar = channel.unary_unary(
        '/dialog.Profile/RemoveAvatar',
        request_serializer=profile__pb2.RequestRemoveAvatar.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeq.FromString,
        )
    self.EditMyTimeZone = channel.unary_unary(
        '/dialog.Profile/EditMyTimeZone',
        request_serializer=profile__pb2.RequestEditMyTimeZone.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeq.FromString,
        )
    self.EditMyPreferredLanguages = channel.unary_unary(
        '/dialog.Profile/EditMyPreferredLanguages',
        request_serializer=profile__pb2.RequestEditMyPreferredLanguages.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeq.FromString,
        )
    self.EditSex = channel.unary_unary(
        '/dialog.Profile/EditSex',
        request_serializer=profile__pb2.RequestEditSex.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeq.FromString,
        )
    self.EditCustomProfile = channel.unary_unary(
        '/dialog.Profile/EditCustomProfile',
        request_serializer=profile__pb2.RequestEditCustomProfile.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeq.FromString,
        )
    self.ChangeUserStatus = channel.unary_unary(
        '/dialog.Profile/ChangeUserStatus',
        request_serializer=profile__pb2.RequestChangeUserStatus.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeq.FromString,
        )


class ProfileServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def EditName(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def EditNickName(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CheckNickName(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def EditAbout(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def EditAvatar(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RemoveAvatar(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def EditMyTimeZone(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def EditMyPreferredLanguages(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def EditSex(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def EditCustomProfile(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ChangeUserStatus(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ProfileServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'EditName': grpc.unary_unary_rpc_method_handler(
          servicer.EditName,
          request_deserializer=profile__pb2.RequestEditName.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeq.SerializeToString,
      ),
      'EditNickName': grpc.unary_unary_rpc_method_handler(
          servicer.EditNickName,
          request_deserializer=profile__pb2.RequestEditNickName.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeq.SerializeToString,
      ),
      'CheckNickName': grpc.unary_unary_rpc_method_handler(
          servicer.CheckNickName,
          request_deserializer=profile__pb2.RequestCheckNickName.FromString,
          response_serializer=miscellaneous__pb2.ResponseBool.SerializeToString,
      ),
      'EditAbout': grpc.unary_unary_rpc_method_handler(
          servicer.EditAbout,
          request_deserializer=profile__pb2.RequestEditAbout.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeq.SerializeToString,
      ),
      'EditAvatar': grpc.unary_unary_rpc_method_handler(
          servicer.EditAvatar,
          request_deserializer=profile__pb2.RequestEditAvatar.FromString,
          response_serializer=profile__pb2.ResponseEditAvatar.SerializeToString,
      ),
      'RemoveAvatar': grpc.unary_unary_rpc_method_handler(
          servicer.RemoveAvatar,
          request_deserializer=profile__pb2.RequestRemoveAvatar.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeq.SerializeToString,
      ),
      'EditMyTimeZone': grpc.unary_unary_rpc_method_handler(
          servicer.EditMyTimeZone,
          request_deserializer=profile__pb2.RequestEditMyTimeZone.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeq.SerializeToString,
      ),
      'EditMyPreferredLanguages': grpc.unary_unary_rpc_method_handler(
          servicer.EditMyPreferredLanguages,
          request_deserializer=profile__pb2.RequestEditMyPreferredLanguages.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeq.SerializeToString,
      ),
      'EditSex': grpc.unary_unary_rpc_method_handler(
          servicer.EditSex,
          request_deserializer=profile__pb2.RequestEditSex.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeq.SerializeToString,
      ),
      'EditCustomProfile': grpc.unary_unary_rpc_method_handler(
          servicer.EditCustomProfile,
          request_deserializer=profile__pb2.RequestEditCustomProfile.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeq.SerializeToString,
      ),
      'ChangeUserStatus': grpc.unary_unary_rpc_method_handler(
          servicer.ChangeUserStatus,
          request_deserializer=profile__pb2.RequestChangeUserStatus.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeq.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'dialog.Profile', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
