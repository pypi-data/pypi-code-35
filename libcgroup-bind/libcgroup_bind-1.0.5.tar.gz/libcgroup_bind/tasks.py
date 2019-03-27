# coding: UTF-8

from ctypes import POINTER, Structure, c_char_p, c_int, c_uint

from . import _libcgroup
from .groups import CGroupPointer
from .init import c_char_pp

try:
    from enum import IntFlag
except ImportError:
    from enum import IntEnum as IntFlag


class CGFlags(IntFlag):
    USECACHE = 0b1
    USE_TEMPLATE_CACHE = 0b10

    @classmethod
    def from_param(cls, obj):
        return int(obj)


class DaemonType(IntFlag):
    UNCHANGE_CHILDREN = 0b1
    CANCEL_UNCHANGE_PROCESS = 0b10

    @classmethod
    def from_param(cls, obj):
        return int(obj)


cgroup_attach_task = _libcgroup.cgroup_attach_task
cgroup_attach_task.argtypes = (CGroupPointer,)
cgroup_attach_task.restype = c_int
# int cgroup_attach_task(struct cgroup *cgroup);

cgroup_attach_task_pid = _libcgroup.cgroup_attach_task_pid
cgroup_attach_task_pid.argtypes = (CGroupPointer, c_int)
cgroup_attach_task_pid.restype = c_int
# int cgroup_attach_task_pid(struct cgroup *cgroup, pid_t tid);

cgroup_change_cgroup_path = _libcgroup.cgroup_change_cgroup_path
cgroup_change_cgroup_path.argtypes = (c_char_p, c_int, c_char_pp)
cgroup_change_cgroup_path.restype = c_int
# int cgroup_change_cgroup_path(const char *path, pid_t pid, const char *const controllers[]);

cgroup_get_current_controller_path = _libcgroup.cgroup_get_current_controller_path
cgroup_get_current_controller_path.argtypes = (c_int, c_char_p, c_char_pp)
cgroup_get_current_controller_path.restype = c_int
# int cgroup_get_current_controller_path(pid_t pid, const char *controller, char **current_path);

cgroup_init_rules_cache = _libcgroup.cgroup_init_rules_cache
cgroup_init_rules_cache.argtypes = tuple()
cgroup_init_rules_cache.restype = c_int
# int cgroup_init_rules_cache(void);

cgroup_reload_cached_rules = _libcgroup.cgroup_reload_cached_rules
cgroup_reload_cached_rules.argtypes = tuple()
cgroup_reload_cached_rules.restype = c_int


# int cgroup_reload_cached_rules(void);


class FILE(Structure):
    pass


FILE_p = POINTER(FILE)

cgroup_print_rules_config = _libcgroup.cgroup_print_rules_config
cgroup_print_rules_config.argtypes = (FILE_p,)
cgroup_print_rules_config.restype = None
# void cgroup_print_rules_config(FILE *fp);

cgroup_change_all_cgroups = _libcgroup.cgroup_change_all_cgroups
cgroup_change_all_cgroups.argtypes = tuple()
cgroup_change_all_cgroups.restype = c_int
# int cgroup_change_all_cgroups(void);

cgroup_change_cgroup_flags = _libcgroup.cgroup_change_cgroup_flags
cgroup_change_cgroup_flags.argtypes = (c_uint, c_uint, c_char_p, c_int, c_int)
cgroup_change_cgroup_flags.restype = c_int
# int cgroup_change_cgroup_flags(uid_t uid, gid_t gid, const char *procname, pid_t pid, int flags);

cgroup_change_cgroup_uid_gid_flags = _libcgroup.cgroup_change_cgroup_uid_gid_flags
cgroup_change_cgroup_uid_gid_flags.argtypes = (c_uint, c_uint, c_int, c_int)
cgroup_change_cgroup_uid_gid_flags.restype = c_int
# int cgroup_change_cgroup_uid_gid_flags(uid_t uid, gid_t gid, pid_t pid, int flags);

cgroup_change_cgroup_uid_gid = _libcgroup.cgroup_change_cgroup_uid_gid
cgroup_change_cgroup_uid_gid.argtypes = (c_uint, c_uint, c_int)
cgroup_change_cgroup_uid_gid.restype = c_int
# int cgroup_change_cgroup_uid_gid(uid_t uid, gid_t gid, pid_t pid);

cgroup_register_unchanged_process = _libcgroup.cgroup_register_unchanged_process
cgroup_register_unchanged_process.argtypes = (c_int, c_int)
cgroup_register_unchanged_process.restype = c_int
# int cgroup_register_unchanged_process(pid_t pid, int flags);
