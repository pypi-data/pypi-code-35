"""A Python implementation of the EMuLSion framework (Epidemiologic
MUlti-Level SImulatiONs).

Tools for performance assessment.
"""


# EMULSION (Epidemiological Multi-Level Simulation framework)
# ===========================================================
# 
# Contributors and contact:
# -------------------------
# 
#     - Sébastien Picault (sebastien.picault@inra.fr)
#     - Yu-Lin Huang
#     - Vianney Sicard
#     - Sandie Arnoux
#     - Gaël Beaunée
#     - Pauline Ezanno (pauline.ezanno@inra.fr)
# 
#     BIOEPAR, INRA, Oniris, Atlanpole La Chantrerie,
#     Nantes CS 44307 CEDEX, France
# 
# 
# How to cite:
# ------------
# 
#     S. Picault, Y.-L. Huang, V. Sicard, P. Ezanno (2017). "Enhancing
#     Sustainability of Complex Epidemiological Models through a Generic
#     Multilevel Agent-based Approach", in: C. Sierra (ed.), 26th
#     International Joint Conference on Artificial Intelligence (IJCAI),
#     AAAI, p. 374-380. DOI: 10.24963/ijcai.2017/53
# 
# 
# License:
# --------
# 
#    Copyright 2016 INRA and Univ. Lille
# 
#    Inter Deposit Digital Number: IDDN.FR.001.280043.000.R.P.2018.000.10000
# 
#    Agence pour la Protection des Programmes,
#    54 rue de Paradis, 75010 Paris, France
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


import time
from   functools                  import wraps

def timethis(times=None):
    """A decorator function for printing execution time."""
    def timefunc(func):
        """The actual decorator"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Decorate the specified function in order to measure its
            execution time. Execution times are stored in the TIMES
            dictionary.

            """
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            if times is None:
                print('{}.{} : {}'.format(func.__module__,
                                          func.__name__,
                                          end - start))
            else:
                if func.__name__ not in times:
                    times[func.__name__] = [end-start]
                else:
                    times[func.__name__].append(end-start)
            return result
        return wrapper
    return timefunc
