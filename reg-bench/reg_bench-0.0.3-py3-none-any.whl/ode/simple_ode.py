import functools
import inspect
import sys

import numpy as np
from sklearn.datasets.base import Bunch

from ..utils import make_register
from .integrate import generate_ode_data


all_ode = {}
register_ode = make_register(all_ode)


@register_ode(2, "linear", "polynomial")
def harmonic_oscillator(omega=1.0):
    @functools.wraps(harmonic_oscillator)
    def dy(y, t):
        dy0 = y[1]
        dy1 = -omega ** 2 * y[0]
        return [dy0, dy1]

    return dy


@register_ode(2, "polynomial")
def anharmonic_oscillator(omega=1.0, c=1.0, l=1.0):
    @functools.wraps(anharmonic_oscillator)
    def dy(y, t):
        dy0 = y[1]
        dy1 = -omega ** 2 * y[0] - l * y[0] ** 2 - c * y[1]
        return [dy0, dy1]

    return dy


@register_ode(3, "polynomial")
def lorenz(s=10.0, r=28.0, b=8.0 / 3.0):
    @functools.wraps(lorenz)
    def dy(y, t):
        dy0 = s * (y[1] - y[0])
        dy1 = r * y[0] - y[1] - y[0] * y[2]
        dy2 = y[0] * y[1] - b * y[2]
        return [dy0, dy1, dy2]

    return dy


@register_ode(2, "polynomial")
def van_der_pol(omega=1.0, a=0.1, b=0.01):
    @functools.wraps(van_der_pol)
    def dy(y, t):
        y0, y1 = y
        dy0 = y1
        dy1 = -omega ** 2 * y0 + a * y1 * (1 - b * y0 ** 2)
        return dy0, dy1

    return dy


@register_ode(2)
def michaelis_menten(vmax=0.25, Km=0.1, rho=1.0):
    @functools.wraps(michaelis_menten)
    def dy(y, t):
        s, p = y
        dp = vmax * s ** rho / (Km + s ** rho)
        ds = -dp
        return [ds, dp]

    return dy


@register_ode(3, "polynomial")
def rössler(a=0.15, b=0.20, c=10.0):
    @functools.wraps(rössler)
    def dy_(state, t):
        x, y, z = state
        dx = -y - z
        dy = x + a * y
        dz = b + (x - c) * z
        return [dx, dy, dz]

    return dy_


@register_ode(2, "polynomial")
def brusselator(a=1.0, b=3.0):
    @functools.wraps(brusselator)
    def dy_(state, t):
        x, y = state
        dx = a + x ** 2 * y - (b + 1) * x
        dy = b * x - x ** 2 * y
        return dx, dy

    return dy_


@register_ode(2)
def magnets(K=0.25):
    @functools.wraps(magnets)
    def dy(state, t):
        theta1, theta2 = state
        dtheta1 = K * np.sin(theta1 - theta2) - np.sin(theta1)
        dtheta2 = K * np.sin(theta2 - theta1) - np.sin(theta2)
        return dtheta1, dtheta2

    return dy


@register_ode(2)
def predator_prey(a=0.5, b=0.5):
    @functools.wraps(predator_prey)
    def dy_(state, t):
        x, y = state
        dx = x * (b - x - y / (1.0 + x))
        dy = y * (x / (1 + x) - a * y)
        return dx, dy

    return dy_


@register_ode(2)
def bacterial_respiration(a=0.1, b=0.2, q=1.0):
    @functools.wraps(bacterial_respiration)
    def dy_(state, t):
        x, y = state
        temp = x * y / (1 + q * x ** 2)
        dx = b - x - temp
        dy = a - temp
        return dx, dy

    return dy_


@register_ode(2)
def glider(d=1.0):
    @functools.wraps(glider)
    def dy(state, t):
        v, theta = state
        dv = -np.sin(theta) - d * v ** 2
        dtheta = -np.cos(theta) / v + v
        return dv, dtheta

    return dy


@register_ode(2)
def shear_flow(a=0.3):
    @functools.wraps(shear_flow)
    def dy(state, t):
        theta, phi = state
        dtheta = np.tan(phi) ** (-1) * np.cos(theta)
        dphi = (np.cos(phi) ** 2 + a * np.sin(phi) ** 2) * np.sin(theta)
        return dtheta, dphi

    return dy


def make_bunch(data_config):
    default_params = lambda: {
        p.name: p.default for p in inspect.signature(data_config["problem"]).parameters.values()
    }
    data_config["ode_params"] = data_config.get("ode_params", default_params())
    x, dx = generate_ode_data(**data_config)
    return Bunch(data=x, target=dx, x0=data_config["x0"], params=data_config["ode_params"], t=data_config["t"])


def make_load(ode, t=np.linspace(0, 100, 10001, endpoint=True), x0=1):
    arity = all_ode[ode]["arity"]
    data_config = dict(problem=ode, x0=np.ones(arity) * x0, t=t)

    def loader():
        return make_bunch(data_config)

    loader.__name__ = "load_" + all_ode[ode]["name"]

    # register loader to the simple_ode module
    caller = inspect.getframeinfo(inspect.stack()[1][0])  # find current_module by looking up caller in stack
    name = inspect.getmodulename(caller.filename)
    current_module = [mod for mname, mod in sys.modules.items() if name == mname.split(".")[-1]][0]
    if loader.__name__ not in dir(current_module):
        setattr(current_module, loader.__name__, loader)

    return loader


all_loaders = {all_ode[ode]["name"]: make_load(ode) for ode in all_ode}
