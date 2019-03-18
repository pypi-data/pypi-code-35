import numpy as np
from scipy.stats import kstest
from typing import Union

import cocos.numerics as cn


def perform_ks_test(x: Union[np.ndarray, cn.ndarray],
                    alpha: float,
                    distribution,
                    args=None,
                    verbose: bool=False) -> bool:
    D, p_value = kstest(x, distribution, args=args)
    if verbose:
        print(f"D={D}, p-value={p_value}")

    alpha = 0.01
    reject = p_value < alpha
    if verbose:
        print(f"D={D}, p-value={p_value}")
        print(f"reject = {reject}")

    return reject
