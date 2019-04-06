import angr
from ...sim_type import parse_type

sysinfo_ty = parse_type("""
   struct sysinfo {
       long uptime;             /* Seconds since boot */
       unsigned long loads[3];  /* 1, 5, and 15 minute load averages */
       unsigned long totalram;  /* Total usable main memory size */
       unsigned long freeram;   /* Available memory size */
       unsigned long sharedram; /* Amount of shared memory */
       unsigned long bufferram; /* Memory used by buffers */
       unsigned long totalswap; /* Total swap space size */
       unsigned long freeswap;  /* Swap space still available */
       unsigned short procs;    /* Number of current processes */
       unsigned long totalhigh; /* Total high memory size */
       unsigned long freehigh;  /* Available high memory size */
       unsigned int mem_unit;   /* Memory unit size in bytes */
   }
""")

class sysinfo(angr.SimProcedure):
    def run(self, info):
        value = {
                'uptime': 0,
                'loads': [0,0,0],
                'totalram': 0,
                'freeram': 0,
                'sharedram': 0,
                'bufferram': 0,
                'totalswap': 0,
                'freeswap': 0,
                'procs': 0,
                'totalhigh': 0,
                'freehigh': 0,
                'mem_unit': 0,
        }
        sysinfo_ty.with_arch(self.arch).store(self.state, info, value)
        return 0
