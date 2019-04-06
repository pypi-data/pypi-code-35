"""
This module implements all 53 benchmark problems of
"GP Needs Better Benchmarks" by McDermott et. al.
DOI: 10.1145/2330163.2330273
"""
from .keijzer import all_problems as keijzer_all
from .korns import all_problems as korns_all
from .koza import all_problems as koza_all
from .nguyen import all_problems as nguyen_all
from .pagie import all_problems as pagie_all
from .vladislavleva import all_problems as vladislavleva_all

all_problems = {
    **koza_all,
    **nguyen_all,
    **nguyen_all,
    **pagie_all,
    **korns_all,
    **keijzer_all,
    **vladislavleva_all,
}
