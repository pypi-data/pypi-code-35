from functools import wraps

import numpy as np
import scipy.integrate
from derivative import derivative


def generate_ode_data(
    problem,
    x0,
    t,
    ode_params=None,
    noise_amplitude=0,
    noise_pdf=None,
    noise_params=None,
    noise_kind="additive",
    diff_params=None,
):
    """Generate a trajectory and estimate its derivate.

    Noise will be added as measurement noise before estimating the derivatives.

    Args:
        problem: ode generator
        x0: initial conditions
        t: timestamps of the output
        ode_params: kwargs for problem
        noise_kind: proportional or additive
        noise_amplitude: noise amplitude
        noise_pdf: function which generates noise
        noise_params: kwargs passed to noise_pdf
        derive_max_order: maximum order derivative

    Returns:
        x, dx: trajectory and derivative

    """
    dy = problem(**(ode_params or {}))
    x = scipy.integrate.odeint(dy, x0, t)

    x = add_measurement_noise(
        x,
        noise_amplitude=noise_amplitude,
        noise_pdf=noise_pdf,
        noise_params=noise_params,
        noise_kind=noise_kind,
    )
    dx = derivative(t, x, **(diff_params or {}))
    return x, dx


def add_measurement_noise(x, noise_amplitude=0, noise_pdf=None, noise_params=None, noise_kind="additive"):
    """Add measurement noise to a trajectory."""
    noise_pdf = noise_pdf or np.random.normal
    noise_params = noise_params or {}

    if noise_amplitude > 0:
        if noise_kind == "proportional":
            return x * (1 + noise_amplitude * noise_pdf(size=x.shape, **noise_params))
        return x + noise_amplitude * noise_pdf(size=x.shape, **noise_params)
    return x
