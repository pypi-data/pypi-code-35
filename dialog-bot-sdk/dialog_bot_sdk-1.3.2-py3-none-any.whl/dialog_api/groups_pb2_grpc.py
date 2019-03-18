# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import groups_pb2 as groups__pb2
from . import miscellaneous_pb2 as miscellaneous__pb2


class GroupsStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.LoadFullGroups = channel.unary_unary(
        '/dialog.Groups/LoadFullGroups',
        request_serializer=groups__pb2.RequestLoadFullGroups.SerializeToString,
        response_deserializer=groups__pb2.ResponseLoadFullGroups.FromString,
        )
    self.LoadMembers = channel.unary_unary(
        '/dialog.Groups/LoadMembers',
        request_serializer=groups__pb2.RequestLoadMembers.SerializeToString,
        response_deserializer=groups__pb2.ResponseLoadMembers.FromString,
        )
    self.CreateGroup = channel.unary_unary(
        '/dialog.Groups/CreateGroup',
        request_serializer=groups__pb2.RequestCreateGroup.SerializeToString,
        response_deserializer=groups__pb2.ResponseCreateGroup.FromString,
        )
    self.EditGroupTitle = channel.unary_unary(
        '/dialog.Groups/EditGroupTitle',
        request_serializer=groups__pb2.RequestEditGroupTitle.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeqDateMid.FromString,
        )
    self.SetGroupShortname = channel.unary_unary(
        '/dialog.Groups/SetGroupShortname',
        request_serializer=groups__pb2.RequestSetGroupShortname.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeq.FromString,
        )
    self.EditGroupAvatar = channel.unary_unary(
        '/dialog.Groups/EditGroupAvatar',
        request_serializer=groups__pb2.RequestEditGroupAvatar.SerializeToString,
        response_deserializer=groups__pb2.ResponseEditGroupAvatar.FromString,
        )
    self.RemoveGroupAvatar = channel.unary_unary(
        '/dialog.Groups/RemoveGroupAvatar',
        request_serializer=groups__pb2.RequestRemoveGroupAvatar.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeqDateMid.FromString,
        )
    self.EditGroupTopic = channel.unary_unary(
        '/dialog.Groups/EditGroupTopic',
        request_serializer=groups__pb2.RequestEditGroupTopic.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeqDate.FromString,
        )
    self.EditGroupAbout = channel.unary_unary(
        '/dialog.Groups/EditGroupAbout',
        request_serializer=groups__pb2.RequestEditGroupAbout.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeqDate.FromString,
        )
    self.InviteUser = channel.unary_unary(
        '/dialog.Groups/InviteUser',
        request_serializer=groups__pb2.RequestInviteUser.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeqDateMid.FromString,
        )
    self.LeaveGroup = channel.unary_unary(
        '/dialog.Groups/LeaveGroup',
        request_serializer=groups__pb2.RequestLeaveGroup.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeqDateMid.FromString,
        )
    self.KickUser = channel.unary_unary(
        '/dialog.Groups/KickUser',
        request_serializer=groups__pb2.RequestKickUser.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeqDateMid.FromString,
        )
    self.MakeUserAdmin = channel.unary_unary(
        '/dialog.Groups/MakeUserAdmin',
        request_serializer=groups__pb2.RequestMakeUserAdmin.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeqDate.FromString,
        )
    self.GetGroupMemberPermissions = channel.unary_unary(
        '/dialog.Groups/GetGroupMemberPermissions',
        request_serializer=groups__pb2.RequestGetGroupMemberPermissions.SerializeToString,
        response_deserializer=groups__pb2.ResponseGetGroupMemberPermissions.FromString,
        )
    self.TransferOwnership = channel.unary_unary(
        '/dialog.Groups/TransferOwnership',
        request_serializer=groups__pb2.RequestTransferOwnership.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseSeqDate.FromString,
        )
    self.GetGroupInviteUrl = channel.unary_unary(
        '/dialog.Groups/GetGroupInviteUrl',
        request_serializer=groups__pb2.RequestGetGroupInviteUrl.SerializeToString,
        response_deserializer=groups__pb2.ResponseInviteUrl.FromString,
        )
    self.GetGroupInviteUrlBase = channel.unary_unary(
        '/dialog.Groups/GetGroupInviteUrlBase',
        request_serializer=groups__pb2.RequestGetGroupInviteUrlBase.SerializeToString,
        response_deserializer=groups__pb2.ResponseGetGroupInviteUrlBase.FromString,
        )
    self.RevokeInviteUrl = channel.unary_unary(
        '/dialog.Groups/RevokeInviteUrl',
        request_serializer=groups__pb2.RequestRevokeInviteUrl.SerializeToString,
        response_deserializer=groups__pb2.ResponseInviteUrl.FromString,
        )
    self.JoinGroup = channel.unary_unary(
        '/dialog.Groups/JoinGroup',
        request_serializer=groups__pb2.RequestJoinGroup.SerializeToString,
        response_deserializer=groups__pb2.ResponseJoinGroup.FromString,
        )
    self.JoinGroupByPeer = channel.unary_unary(
        '/dialog.Groups/JoinGroupByPeer',
        request_serializer=groups__pb2.RequestJoinGroupByPeer.SerializeToString,
        response_deserializer=miscellaneous__pb2.ResponseVoid.FromString,
        )
    self.MakeUserAdminObsolete = channel.unary_unary(
        '/dialog.Groups/MakeUserAdminObsolete',
        request_serializer=groups__pb2.RequestMakeUserAdminObsolete.SerializeToString,
        response_deserializer=groups__pb2.ResponseMakeUserAdminObsolete.FromString,
        )


class GroupsServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def LoadFullGroups(self, request, context):
    """/ deprecated
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def LoadMembers(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CreateGroup(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def EditGroupTitle(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetGroupShortname(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def EditGroupAvatar(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RemoveGroupAvatar(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def EditGroupTopic(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def EditGroupAbout(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def InviteUser(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def LeaveGroup(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def KickUser(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def MakeUserAdmin(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetGroupMemberPermissions(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def TransferOwnership(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetGroupInviteUrl(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetGroupInviteUrlBase(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RevokeInviteUrl(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def JoinGroup(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def JoinGroupByPeer(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def MakeUserAdminObsolete(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_GroupsServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'LoadFullGroups': grpc.unary_unary_rpc_method_handler(
          servicer.LoadFullGroups,
          request_deserializer=groups__pb2.RequestLoadFullGroups.FromString,
          response_serializer=groups__pb2.ResponseLoadFullGroups.SerializeToString,
      ),
      'LoadMembers': grpc.unary_unary_rpc_method_handler(
          servicer.LoadMembers,
          request_deserializer=groups__pb2.RequestLoadMembers.FromString,
          response_serializer=groups__pb2.ResponseLoadMembers.SerializeToString,
      ),
      'CreateGroup': grpc.unary_unary_rpc_method_handler(
          servicer.CreateGroup,
          request_deserializer=groups__pb2.RequestCreateGroup.FromString,
          response_serializer=groups__pb2.ResponseCreateGroup.SerializeToString,
      ),
      'EditGroupTitle': grpc.unary_unary_rpc_method_handler(
          servicer.EditGroupTitle,
          request_deserializer=groups__pb2.RequestEditGroupTitle.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeqDateMid.SerializeToString,
      ),
      'SetGroupShortname': grpc.unary_unary_rpc_method_handler(
          servicer.SetGroupShortname,
          request_deserializer=groups__pb2.RequestSetGroupShortname.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeq.SerializeToString,
      ),
      'EditGroupAvatar': grpc.unary_unary_rpc_method_handler(
          servicer.EditGroupAvatar,
          request_deserializer=groups__pb2.RequestEditGroupAvatar.FromString,
          response_serializer=groups__pb2.ResponseEditGroupAvatar.SerializeToString,
      ),
      'RemoveGroupAvatar': grpc.unary_unary_rpc_method_handler(
          servicer.RemoveGroupAvatar,
          request_deserializer=groups__pb2.RequestRemoveGroupAvatar.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeqDateMid.SerializeToString,
      ),
      'EditGroupTopic': grpc.unary_unary_rpc_method_handler(
          servicer.EditGroupTopic,
          request_deserializer=groups__pb2.RequestEditGroupTopic.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeqDate.SerializeToString,
      ),
      'EditGroupAbout': grpc.unary_unary_rpc_method_handler(
          servicer.EditGroupAbout,
          request_deserializer=groups__pb2.RequestEditGroupAbout.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeqDate.SerializeToString,
      ),
      'InviteUser': grpc.unary_unary_rpc_method_handler(
          servicer.InviteUser,
          request_deserializer=groups__pb2.RequestInviteUser.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeqDateMid.SerializeToString,
      ),
      'LeaveGroup': grpc.unary_unary_rpc_method_handler(
          servicer.LeaveGroup,
          request_deserializer=groups__pb2.RequestLeaveGroup.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeqDateMid.SerializeToString,
      ),
      'KickUser': grpc.unary_unary_rpc_method_handler(
          servicer.KickUser,
          request_deserializer=groups__pb2.RequestKickUser.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeqDateMid.SerializeToString,
      ),
      'MakeUserAdmin': grpc.unary_unary_rpc_method_handler(
          servicer.MakeUserAdmin,
          request_deserializer=groups__pb2.RequestMakeUserAdmin.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeqDate.SerializeToString,
      ),
      'GetGroupMemberPermissions': grpc.unary_unary_rpc_method_handler(
          servicer.GetGroupMemberPermissions,
          request_deserializer=groups__pb2.RequestGetGroupMemberPermissions.FromString,
          response_serializer=groups__pb2.ResponseGetGroupMemberPermissions.SerializeToString,
      ),
      'TransferOwnership': grpc.unary_unary_rpc_method_handler(
          servicer.TransferOwnership,
          request_deserializer=groups__pb2.RequestTransferOwnership.FromString,
          response_serializer=miscellaneous__pb2.ResponseSeqDate.SerializeToString,
      ),
      'GetGroupInviteUrl': grpc.unary_unary_rpc_method_handler(
          servicer.GetGroupInviteUrl,
          request_deserializer=groups__pb2.RequestGetGroupInviteUrl.FromString,
          response_serializer=groups__pb2.ResponseInviteUrl.SerializeToString,
      ),
      'GetGroupInviteUrlBase': grpc.unary_unary_rpc_method_handler(
          servicer.GetGroupInviteUrlBase,
          request_deserializer=groups__pb2.RequestGetGroupInviteUrlBase.FromString,
          response_serializer=groups__pb2.ResponseGetGroupInviteUrlBase.SerializeToString,
      ),
      'RevokeInviteUrl': grpc.unary_unary_rpc_method_handler(
          servicer.RevokeInviteUrl,
          request_deserializer=groups__pb2.RequestRevokeInviteUrl.FromString,
          response_serializer=groups__pb2.ResponseInviteUrl.SerializeToString,
      ),
      'JoinGroup': grpc.unary_unary_rpc_method_handler(
          servicer.JoinGroup,
          request_deserializer=groups__pb2.RequestJoinGroup.FromString,
          response_serializer=groups__pb2.ResponseJoinGroup.SerializeToString,
      ),
      'JoinGroupByPeer': grpc.unary_unary_rpc_method_handler(
          servicer.JoinGroupByPeer,
          request_deserializer=groups__pb2.RequestJoinGroupByPeer.FromString,
          response_serializer=miscellaneous__pb2.ResponseVoid.SerializeToString,
      ),
      'MakeUserAdminObsolete': grpc.unary_unary_rpc_method_handler(
          servicer.MakeUserAdminObsolete,
          request_deserializer=groups__pb2.RequestMakeUserAdminObsolete.FromString,
          response_serializer=groups__pb2.ResponseMakeUserAdminObsolete.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'dialog.Groups', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
