""".. module:: emulsion.tools.state

Tools aimed at handling state variables, either using a special
dictionary (``StateVarDict``), or using a special descriptor
(StateVar) in association with a decorator (@statevar).

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


from   enum                       import Enum
from   functools                  import total_ordering


class StateVarDict(dict):
    """A special dictionary aimed at handling the 'State Variables' of
    agents in Emulsion models. In addition to the classical dict
    key-based access, it provides an attribute-like access syntax.

    Example::

        s = StateVarDict(age=10, sick=True)
        s['age'] += 1
        s.sick = False
        s.new_property = 'Wow !'

    This class is used in Emulsion to store individual agent
    properties. Such properties include those defined automatically
    and used by the Emulsion engine, such as the values of the states
    for each state machine, the current time step, or "hidden" values
    such as the time spent in the current state for each state
    machine. They also include user-defined attributes (e.g. age,
    weight...).

    When searching for a model ``statevar``, the engine tries first to
    find a classical instance variable (which can be mimicked by a
    Python ``@property``-decored function), then looks inside the
    agent's ``statevar`` attribute; finally, the search continues in
    the agent's host (if any).

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # make self its own attributes dictionary (nice, hey ?)
        self.__dict__ = self


@total_ordering
class EmulsionEnum(Enum):
    """This class represents enumerations for Emulsion. They are endowed
    with some special features:

     #. They provide total ordering between items (based on ``__lt__``
       and ``__eq__`` methods).
     #. A comparison with ``None`` is provided (always greater than ``None``).
     #. Other features will be developed soon.

    """
    def __lt__(self, other):
        """Return a less-than comparison for enumeration items. An enum item
        is always greater than ``None``and than any other item of
        another enumeration. Then, the ``value`` attribute of the item
        is used.

        """
        return False if other is None or other.__class__ != self.__class__\
          else self.value < other.value

    def __eq__(self, other):
        """Return a equality comparison for enumeration items. An enum item is
        always greater than ``None``and than any other item of another
        enumeration. Then, the ``value`` attribute of the item is
        used.

        """
        return False if other is None or other.__class__ != self.__class__\
          else self.value == other.value

    def __int__(self):
        """Return the *int* value mapped to this item."""
        return self.value

    def __repr__(self):
        """Return a string representation of the instances of the enumeration,
        hiding associated numerical value.

        """
        return f'<{self.__class__.__name__}.{self.name}>'

    def __hash__(self):
        """Use the value as hashcode."""
        return self.value
