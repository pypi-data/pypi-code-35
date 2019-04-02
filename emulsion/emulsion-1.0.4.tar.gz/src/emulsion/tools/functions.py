""".. module:: emulsion.tools.functions

Additional functions for symbolic computing in YAML model definition files.

All functions in this module can be used in Emulsion models.
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


import numpy as np

def IfThenElse(condition, val_if_true, val_if_false):
    """Ternary conditional function: return either *val_if_true* or
    *val_if_false* depending on *condition*.

    Args:
        condition: a boolean expression
        val_if_true: value to return if the expression is True
        val_if_false: value to return if the expression is False

    Returns:
        One of the two values, depending on *condition*.
    """
    return val_if_true if condition else val_if_false

IfThenElse.__USER_FUNCTION__ = ['Functions Available for Models']


# BEWARE: using lambdify, by default And and Or fall back to numpy's
# *binary* operators, so that more than 3 conditions linked by And or
# Or trigger a TypeError ('return arrays must be of ArrayType')
# see topic addressed there:
# https://stackoverflow.com/questions/42045906/typeerror-return-arrays-must-be-of-arraytype-using-lambdify-of-sympy-in-python

# To avoid problems, please use AND / OR (fully in UPPERCASE) instead
# of And / Or (Capitalized) in the conditions of Emulsion models
def AND(*values):
    """Return a logical AND (conjunction) between all the values.

    Args:
        *values: a list of boolean values

    Returns:
        True if all values are True, False otherwise.
    """
    return all(values)

AND.__USER_FUNCTION__ = ['Functions Available for Models']


def OR(*values):
    """Return a logical OR (disjunction) between all the values.

    Args:
        *values: a list of boolean values

    Returns:
        True if one of the values is True, False otherwise.
    """
    return any(values)

OR.__USER_FUNCTION__ = ['Functions Available for Models']

def random_bool(proba_success: float) -> int:
    """Return a random boolean value (actually, 0 or 1) depending on
    *proba_success*.

    Args:
        proba_success: probability of returning 1 (True)

    Returns:
        Either 1 with probability *proba_success*, or 0 with
        probability 1-*proba_success*

    """
    return np.random.binomial(1, proba_success)

def random_choice(*values):
    """Return a value chosen randomly.

    Args:
        *values: the possible values

    Returns:
        Either one of the values (equiprobable choice)

    """
    return np.random.choice(values)

random_choice.__USER_FUNCTION__ = ['Functions Available for Models']


## shortcuts for numpy.random distributions
random_uniform = np.random.uniform
random_integers = np.random.random_integers
random_exponential = np.random.exponential
random_beta = np.random.beta
random_normal = np.random.normal
random_poisson = np.random.poisson
random_gamma = np.random.gamma


# def random_beta(alpha: float, beta: float) -> float:
#     """Return a random value from a Beta distribution depending on shape
#     parameters *alpha* and *beta*.

#     Args:
#         alpha: 1st shape parameter of a Beta distribution
#         beta: 2nd shape parameter of a Beta distribution

#     Returns:
#         A random sample of the specified Beta distribution.

#     See also:
#         ``np.random.beta``

#     """
#     return np.random.beta(alpha, beta)

# random_beta.__USER_FUNCTION__ = ['Functions Available for Models']

# def random_normal(avg: float, sd: float) -> float:
#     """Return a random value from a normal distribution with specified
#     mean (*avg*) and standard deviation (*sd*).

#     Args:
#         avg: mean of the normal distribution
#         sd: standard deviation of the normal distribution

#     Returns:
#         A random sample of the specified normal distribution.

#     See also:
#         ``np.random.normal``

#     """
#     return np.random.normal(avg, sd)

# random_normal.__USER_FUNCTION__ = ['Functions Available for Models']

# def random_poisson(avg: float) -> float:
#     """Return a random value from a Poisson distribution of mean *avg*.

#     Args:
#         avg: the mean of the Poisson distribution

#     Returns:
#         A random sample of the specified Poisson distribution.

#     See also:
#         ``np.random.poisson``

#     """
#     return np.random.poisson(avg)

# random_poisson.__USER_FUNCTION__ = ['Functions Available for Models']
