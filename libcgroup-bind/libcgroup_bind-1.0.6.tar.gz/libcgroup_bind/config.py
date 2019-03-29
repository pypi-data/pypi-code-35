# coding: UTF-8

from ctypes import c_char_p, c_int

from . import _libcgroup
from .groups import CGroupPointer

cgroup_config_load_config = _libcgroup.cgroup_config_load_config
cgroup_config_load_config.argtypes = (c_char_p,)
cgroup_config_load_config.restype = c_int
# int cgroup_config_load_config(const char *pathname);

cgroup_unload_cgroups = _libcgroup.cgroup_unload_cgroups
cgroup_unload_cgroups.argtypes = tuple()
cgroup_unload_cgroups.restype = c_int
# int cgroup_unload_cgroups(void);

cgroup_config_unload_config = _libcgroup.cgroup_config_unload_config
cgroup_config_unload_config.argtypes = (c_char_p, c_int)
cgroup_config_unload_config.restype = c_int
# int cgroup_config_unload_config(const char *pathname, int flags);

cgroup_config_set_default = _libcgroup.cgroup_config_set_default
cgroup_config_set_default.argtypes = (CGroupPointer,)
cgroup_config_set_default.restype = c_int
# int cgroup_config_set_default(struct cgroup *new_default);

cgroup_init_templates_cache = _libcgroup.cgroup_init_templates_cache
cgroup_init_templates_cache.argtypes = (c_char_p,)
cgroup_init_templates_cache.restype = c_int
# int cgroup_init_templates_cache(char *pathname);

cgroup_reload_cached_templates = _libcgroup.cgroup_reload_cached_templates
cgroup_reload_cached_templates.argtypes = (c_char_p,)
cgroup_reload_cached_templates.restype = c_int
# int cgroup_reload_cached_templates(char *pathname);

cgroup_config_create_template_group = _libcgroup.cgroup_config_create_template_group
cgroup_config_create_template_group.argtypes = (CGroupPointer, c_char_p, c_int)
cgroup_config_create_template_group.restype = c_int
# int cgroup_config_create_template_group(struct cgroup *cgroup, char *template_name, int flags);
