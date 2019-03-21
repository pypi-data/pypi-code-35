# coding: UTF-8

from ctypes import POINTER, Structure, c_bool, c_char_p, c_int, c_int64, c_uint, c_uint64

from . import _libcgroup
from .init import c_char_pp
from .iterators import c_int_p

try:
    from enum import IntFlag
except ImportError:
    from enum import IntEnum as IntFlag


class DeleteFlag(IntFlag):
    NONE = 0b000
    IGNORE_MIGRATION = 0b001
    RECURSIVE = 0b010
    EMPTY_ONLY = 0b100

    @classmethod
    def from_param(cls, obj):
        return int(obj)


class CGroup(Structure):
    pass


CGroupPointer = POINTER(CGroup)
CGroupDoublePointer = POINTER(CGroupPointer)


class CGroupController(Structure):
    pass


CGroupControllerPointer = POINTER(CGroupController)

cgroup_new_cgroup = _libcgroup.cgroup_new_cgroup
cgroup_new_cgroup.argtypes = (c_char_p,)
cgroup_new_cgroup.restype = CGroupPointer
# struct cgroup *cgroup_new_cgroup(const char *name);

cgroup_add_controller = _libcgroup.cgroup_add_controller
cgroup_add_controller.argtypes = (CGroupPointer, c_char_p)
cgroup_add_controller.restype = CGroupControllerPointer
# struct cgroup_controller *cgroup_add_controller(struct cgroup *cgroup, const char *name);

cgroup_get_controller = _libcgroup.cgroup_get_controller
cgroup_get_controller.argtypes = (CGroupPointer, c_char_p)
cgroup_get_controller.restype = CGroupControllerPointer
# struct cgroup_controller *cgroup_get_controller(struct cgroup *cgroup, const char *name);

cgroup_free = _libcgroup.cgroup_free
cgroup_free.argtypes = (CGroupDoublePointer,)
cgroup_free.restype = None
# void cgroup_free(struct cgroup **cgroup);

cgroup_free_controllers = _libcgroup.cgroup_free_controllers
cgroup_free_controllers.argtypes = (CGroupPointer,)
cgroup_free_controllers.restype = None
# void cgroup_free_controllers(struct cgroup *cgroup);


cgroup_create_cgroup = _libcgroup.cgroup_create_cgroup
cgroup_create_cgroup.argtypes = (CGroupPointer, c_int)
cgroup_create_cgroup.restype = c_int
# int cgroup_create_cgroup(struct cgroup *cgroup, int ignore_ownership);


cgroup_create_cgroup_from_parent = _libcgroup.cgroup_create_cgroup_from_parent
cgroup_create_cgroup_from_parent.argtypes = (CGroupPointer, c_int)
cgroup_create_cgroup_from_parent.restype = c_int
# int cgroup_create_cgroup_from_parent(struct cgroup *cgroup, int ignore_ownership);


cgroup_modify_cgroup = _libcgroup.cgroup_modify_cgroup
cgroup_modify_cgroup.argtypes = (CGroupPointer,)
cgroup_modify_cgroup.restype = c_int
# int cgroup_modify_cgroup(struct cgroup *cgroup);


cgroup_delete_cgroup = _libcgroup.cgroup_delete_cgroup
cgroup_delete_cgroup.argtypes = (CGroupPointer, c_int)
cgroup_delete_cgroup.restype = c_int
# int cgroup_delete_cgroup(struct cgroup *cgroup, int ignore_migration);


cgroup_delete_cgroup_ext = _libcgroup.cgroup_delete_cgroup_ext
cgroup_delete_cgroup_ext.argtypes = (CGroupPointer, c_int)
cgroup_delete_cgroup_ext.restype = c_int
# int cgroup_delete_cgroup_ext(struct cgroup *cgroup, int flags);


cgroup_get_cgroup = _libcgroup.cgroup_get_cgroup
cgroup_get_cgroup.argtypes = (CGroupPointer,)
cgroup_get_cgroup.restype = c_int
# int cgroup_get_cgroup(struct cgroup *cgroup);


cgroup_copy_cgroup = _libcgroup.cgroup_copy_cgroup
cgroup_copy_cgroup.argtypes = (CGroupPointer, CGroupPointer)
cgroup_copy_cgroup.restype = c_int
# int cgroup_copy_cgroup(struct cgroup *dst, struct cgroup *src);


cgroup_compare_cgroup = _libcgroup.cgroup_compare_cgroup
cgroup_compare_cgroup.argtypes = (CGroupPointer, CGroupPointer)
cgroup_compare_cgroup.restype = c_int
# int cgroup_compare_cgroup(struct cgroup *cgroup_a, struct cgroup *cgroup_b);


cgroup_compare_controllers = _libcgroup.cgroup_compare_controllers
cgroup_compare_controllers.argtypes = (CGroupControllerPointer, CGroupControllerPointer)
cgroup_compare_controllers.restype = c_int
# int cgroup_compare_controllers(struct cgroup_controller *cgca, struct cgroup_controller *cgcb);


cgroup_set_uid_gid = _libcgroup.cgroup_set_uid_gid
cgroup_set_uid_gid.argtypes = (CGroupPointer, c_uint, c_uint, c_uint, c_uint)
cgroup_set_uid_gid.restype = c_int
# int cgroup_set_uid_gid(struct cgroup *cgroup, uid_t tasks_uid, gid_t tasks_gid, uid_t control_uid, gid_t control_gid);

c_uint_p = POINTER(c_uint)

cgroup_get_uid_gid = _libcgroup.cgroup_get_uid_gid
cgroup_get_uid_gid.argtypes = (CGroupPointer, c_uint_p, c_uint_p, c_uint_p, c_uint_p)
cgroup_get_uid_gid.restype = c_int
# int cgroup_get_uid_gid(struct cgroup *cgroup, uid_t *tasks_uid, gid_t *tasks_gid,
#                        uid_t *control_uid, gid_t *control_gid);


cgroup_set_permissions = _libcgroup.cgroup_set_permissions
cgroup_set_permissions.argtypes = (CGroupPointer, c_uint, c_uint, c_uint)
cgroup_set_permissions.restype = None
# void cgroup_set_permissions(struct cgroup *cgroup, mode_t control_dperm, mode_t control_fperm, mode_t task_fperm);


cgroup_add_value_string = _libcgroup.cgroup_add_value_string
cgroup_add_value_string.argtypes = (CGroupControllerPointer, c_char_p, c_char_p)
cgroup_add_value_string.restype = c_int
# int cgroup_add_value_string(struct cgroup_controller *controller, const char *name, const char *value);


cgroup_add_value_int64 = _libcgroup.cgroup_add_value_int64
cgroup_add_value_int64.argtypes = (CGroupControllerPointer, c_char_p, c_int64)
cgroup_add_value_int64.restype = c_int
# int cgroup_add_value_int64(struct cgroup_controller *controller, const char *name, int64_t value);


cgroup_add_value_uint64 = _libcgroup.cgroup_add_value_uint64
cgroup_add_value_uint64.argtypes = (CGroupControllerPointer, c_char_p, c_uint64)
cgroup_add_value_uint64.restype = c_int
# int cgroup_add_value_uint64(struct cgroup_controller *controller, const char *name, u_int64_t value);


cgroup_add_value_bool = _libcgroup.cgroup_add_value_bool
cgroup_add_value_bool.argtypes = (CGroupControllerPointer, c_char_p, c_bool)
cgroup_add_value_bool.restype = c_int
# int cgroup_add_value_bool(struct cgroup_controller *controller, const char *name, bool value);


cgroup_get_value_string = _libcgroup.cgroup_get_value_string
cgroup_get_value_string.argtypes = (CGroupControllerPointer, c_char_p, c_char_pp)
cgroup_get_value_string.restype = c_int
# int cgroup_get_value_string(struct cgroup_controller *controller, const char *name, char **value);

c_int64_p = POINTER(c_int64)

cgroup_get_value_int64 = _libcgroup.cgroup_get_value_int64
cgroup_get_value_int64.argtypes = (CGroupControllerPointer, c_char_p, c_int64_p)
cgroup_get_value_int64.restype = c_int
# int cgroup_get_value_int64(struct cgroup_controller *controller, const char *name, int64_t *value);

c_uint64_p = POINTER(c_uint64)

cgroup_get_value_uint64 = _libcgroup.cgroup_get_value_uint64
cgroup_get_value_uint64.argtypes = (CGroupControllerPointer, c_char_p, c_uint64_p)
cgroup_get_value_uint64.restype = c_int
# int cgroup_get_value_uint64(struct cgroup_controller *controller, const char *name, u_int64_t *value);

c_bool_p = POINTER(c_bool)

cgroup_get_value_bool = _libcgroup.cgroup_get_value_bool
cgroup_get_value_bool.argtypes = (CGroupControllerPointer, c_char_p, c_bool_p)
cgroup_get_value_bool.restype = c_int
# int cgroup_get_value_bool(struct cgroup_controller *controller, const char *name, bool *value);

cgroup_set_value_string = _libcgroup.cgroup_set_value_string
cgroup_set_value_string.argtypes = (CGroupControllerPointer, c_char_p, c_char_p)
cgroup_set_value_string.restype = c_int
# int cgroup_set_value_string(struct cgroup_controller *controller, const char *name, const char *value);

cgroup_set_value_int64 = _libcgroup.cgroup_set_value_int64
cgroup_set_value_int64.argtypes = (CGroupControllerPointer, c_char_p, c_int64)
cgroup_set_value_int64.restype = c_int
# int cgroup_set_value_int64(struct cgroup_controller *controller, const char *name, int64_t value);

cgroup_set_value_uint64 = _libcgroup.cgroup_set_value_uint64
cgroup_set_value_uint64.argtypes = (CGroupControllerPointer, c_char_p, c_uint64)
cgroup_set_value_uint64.restype = c_int
# int cgroup_set_value_uint64(struct cgroup_controller *controller, const char *name, u_int64_t value);

cgroup_set_value_bool = _libcgroup.cgroup_set_value_bool
cgroup_set_value_bool.argtypes = (CGroupControllerPointer, c_char_p, c_bool)
cgroup_set_value_bool.restype = c_int
# int cgroup_set_value_bool(struct cgroup_controller *controller, const char *name, bool value);

cgroup_get_value_name_count = _libcgroup.cgroup_get_value_name_count
cgroup_get_value_name_count.argtypes = (CGroupControllerPointer,)
cgroup_get_value_name_count.restype = c_int
# int cgroup_get_value_name_count(struct cgroup_controller *controller);

cgroup_get_value_name = _libcgroup.cgroup_get_value_name
cgroup_get_value_name.argtypes = (CGroupControllerPointer, c_int)
cgroup_get_value_name.restype = c_char_p
# char *cgroup_get_value_name(struct cgroup_controller *controller, int index);

c_int_pp = POINTER(c_int_p)

cgroup_get_procs = _libcgroup.cgroup_get_procs
cgroup_get_procs.argtypes = (c_char_p, c_char_p, c_int_pp, c_int_p)
cgroup_get_procs.restype = c_int
# int cgroup_get_procs(char *name, char *controller, pid_t **pids, int *size);

cg_chmod_recursive = _libcgroup.cg_chmod_recursive
cg_chmod_recursive.argtypes = (CGroupPointer, c_uint, c_int, c_uint, c_int)
cg_chmod_recursive.restype = c_int
# int cg_chmod_recursive(struct cgroup *cgroup, mode_t dir_mode, int dirm_change, mode_t file_mode, int filem_change);

# TODO: undefined
# cgroup_get_cgroup_name = _libcgroup.cgroup_get_cgroup_name
# cgroup_get_cgroup_name.argtypes = (CGroupPointer,)
# cgroup_get_cgroup_name.restype = c_char_p
# # char *cgroup_get_cgroup_name(struct cgroup *cgroup);
