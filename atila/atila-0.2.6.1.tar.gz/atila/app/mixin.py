from functools import wraps
import os
from importlib import reload
from skitai import was as the_was
import time, threading
from ..storage import Storage
import atila
from . import decorators, auth, template_engine, router, events
    
class MixIn (
        decorators.Decorators,
        router.Router, 
        events.Events,
        auth.Auth,        
        template_engine.TemplateEngine
    ):    
    use_reloader = False
    debug = False
    auto_mount = True
    contrib_devel = False # make reloadable
    
    securekey = None
    session_timeout = None

    access_control_allow_origin = None
    access_control_max_age = 0
    authenticate = None
    
    def __init__ (self):
        decorators.Decorators.__init__ (self)
        router.Router.__init__ (self)
        events.Events.__init__ (self)        
        auth.Auth.__init__ (self)         
        template_engine.TemplateEngine.__init__ (self)

        self.module = None
        self.packagename = None
        self.wasc = None
        self.logger = None
        self.store = Storage ()
        self.lock = threading.RLock ()
        
        self.mount_p = "/"
        self.path_suffix_len = 0
        self.mount_params = {}
        self.reloadables = {}
        self.last_reloaded = time.time ()        
        self.init_time = time.time ()
        
        self._maintern_funcs = {}  
        self._package_dirs = []           
        self._mount_option = {}
        self._started = False        
        
        self._salt = None        
        
        self.store ["__last_maintern"] = 0.0
        self.store ["__maintern_count"] = 0
    
    def maintern (self):
        if not self._maintern_funcs:
            return
        now = time.time ()
        if (now - self.store ["__last_maintern"]) < self.config.get ("maintain_interval", 60):
            return
        
        was = the_was._get ()
        with self.lock:
            for func in self._maintern_funcs.values ():
                func (was, now, self.store ["__maintern_count"])
        self.store ["__last_maintern"] = now
        self.store ["__maintern_count"] += 1
            
    def get_resource (self, *args):
        return self.joinpath ("resources", *args)
    
    def joinpath (self, *args):
        return os.path.normpath (os.path.join (self.home, *args))

    def set_mount_point (self, mount):
        if not mount:
            self.mount_p = "/"
        elif mount [-1] != "/":
            self.mount_p = mount + "/"
        else:
            self.mount_p = mount
        self.path_suffix_len = len (self.mount_p) - 1
                
    def init (self, module, packagename = "app", mount = "/"):
        self.module = module    
        self.packagename = packagename
        self.set_mount_point (mount)
        
        if self.module:
            self.abspath = self.module.__file__
            if self.abspath [-3:] != ".py":
                self.abspath = self.abspath [:-1]
            self.update_file_info    ()
        
    def __getitem__ (self, k):
        return self.route_map [k]
    
    def get_file_info (self, module):        
        stat = os.stat (module.__file__)
        return stat.st_mtime, stat.st_size
       
    def update_file_info (self):
        stat = os.stat (self.abspath)
        self.file_info = (stat.st_mtime, stat.st_size)
        
    #------------------------------------------------------    
    @property
    def salt (self):
        if self._salt:
            return self._salt
        if not self.securekey:
            self._salt = None
        else:            
            self._salt = self.securekey.encode ("utf8")
        return self._salt
    
    def set_default_session_timeout (self, timeout):
        self.session_timeout = timeout
                 
    def set_devel (self, debug = True, use_reloader = True):
        self.debug = debug
        self.use_reloader = use_reloader
    
    # services management ----------------------------------------------
    PACKAGE_DIRS = ["services", "decorative"]
    CONTRIB_DIR = os.path.join (os.path.dirname (atila.__spec__.origin), 'contrib', 'services')
                
    def add_package (self, *names):
        for name in names:
            self.PACKAGE_DIRS.append (name)
    
    def _mount (self, module):
        mount_func = None
        if hasattr (module, "mount"):
            mount_func = module.mount
        elif hasattr (module, "decorate"): # for old ver
            mount_func = module.decorate
                        
        if mount_func:
            if not self.auto_mount and module not in self.mount_params:            
                return        
            params = self.mount_params.get (module, {})
            if params.get ("debug_only") and not self.debug:
                return
            # for app
            setattr (module, "__options__", params)
            setattr (module, "_mount__", params)
            # for app initialzing and reloading
            self._mount_option = params
            try:
                mount_func (self)
                self.log ("- {} mounted".format (module.__name__), "info")
            finally:    
                self._mount_option = {}
                
        try:
            self.reloadables [module] = self.get_file_info (module)
        except FileNotFoundError:
            del self.reloadables [module]
            return        
        # find recursively
        self.find_mountables (module)
        
    def find_mountables (self, module):
        for attr in dir (module):
            v = getattr (module, attr)
            try:
                modpath = v.__spec__.origin
            except AttributeError:
                continue
            if not modpath:
                continue            
            if v in self.reloadables:
                continue
            if self.contrib_devel:
                if modpath.startswith (self.CONTRIB_DIR):
                    self._mount (v)
                    continue
            for package_dir in self._package_dirs:
                if modpath.startswith (package_dir):
                    self._mount (v)
                    break
    
    def add_package_dir (self, path):
        if path not in self._package_dirs:
            self._package_dirs.append (path)
            
    def mount_externals (self):
        for module in self.mount_params:            
            if module in self.reloadables:
                continue
            self._mount (module)
        
    def mount (self, maybe_point = None, *modules, **kargs):
        if maybe_point:
            if isinstance (maybe_point, str):                
                kargs ["point"] = maybe_point
            else:
                modules = (maybe_point,) + modules
        for module in modules:
            assert hasattr (module, "mount") or hasattr (module, "decorate")            
            self.add_package_dir (os.path.dirname (module.__spec__.origin))
            self.mount_params [module] = (kargs)
    mount_with = decorate_with = mount    
    
    def umount (self, *modules):
        for module in modules:
            umount_func = None
            if hasattr (module, "umount"):
                umount_func = module.umount
            elif hasattr (module, "dettach"): # for old ver
                umount_func = module.dettach 
            umount_func and umount_func (self)
            self.log ("- %s umounted" % module.__name__, "info")
         
    def  umount_all (self):
        self.umount (*tuple (self.reloadables.keys ()))
    dettach_all = umount_all
    
    def maybe_reload (self):
        if time.time () - self.last_reloaded < 1.0:
            return
        
        self._reloading = True
        for module in list (self.reloadables.keys ()):
            try:
                fi = self.get_file_info (module)
            except FileNotFoundError:
                del self.reloadables [module]
                continue
                
            if self.reloadables [module] != fi:
                self.log ("- reloading service, %s" % module.__name__, "info")
                self._current_function_specs = {}
                if hasattr (module, "dettach"):
                    module.dettach (self)
                with self.lock:
                    newmodule = reload (module)
                    del self.reloadables [module]
                    self._mount (newmodule)
                    
        self.load_jinja_filters ()
        self.last_reloaded = time.time ()        
        self._reloading = False
    
    # logger ----------------------------------------------------------
    def set_logger (self, logger):
        self.logger = logger 
        
    def log (self, msg, type = "info"):
        self.logger (msg, type)
    
    def trace (self):
        self.logger.trace ()
   
    PHASES = {
        'before_mount': 0,
        'mounted': 3,
        'before_reload': 5,
        'reloaded': 1,
        'before_umount': 4,
        'umounted': 2,
        'mounted_or_reloaded': 6
    }
    def life_cycle (self, phase, obj):
        if phase in ("umounted", "before_reload"):
            self.dettach_all ()
        index = self.PHASES.get (phase)
        func = self._binds_server [index]
        if not func:
            return        
        
        obj.app = self
        try:
            func (obj)
        except:
            if self.logger:
                self.logger.trace ()
            else:
                raise                             
    
    # Error handling ------------------------------------------------------        
    def render_error (self, error, was = None):
        handler = self.handlers.get (error ['code'], self.handlers.get (0))
        if not handler:
            return
        was = was or the_was._get ()
        if not hasattr (was, "response") or was.response is None:
            return
        # reset was.app for rendering
        was.app = self
        content =  handler [0] (was, error)
        was.app = None
        return content
    

    # app startup and shutdown --------------------------------------------    
    def cleanup (self):   
        pass
            
    def _start (self, wasc, route, reload = False):
        self.wasc = wasc
        if not route:
            self.basepath = "/"
        elif not route.endswith ("/"):            
            self.basepath = route + "/"
        else:
            self.basepath = route
        
    def start (self, wasc, route):
        self.bus.emit ("app:starting", wasc)
        self._start (wasc, route)
        self.bus.emit ("app:started", wasc)
        self._started = True
        
    def restart (self, wasc, route):        
        self._reloading = True
        self.bus.emit ("app:restarting", wasc)    
        self._start (wasc, route, True)
        self.bus.emit ("app:restarted", wasc)    
        self._reloading = False
    
    