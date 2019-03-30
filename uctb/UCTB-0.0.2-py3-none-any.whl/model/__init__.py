
from .HM import HM
from .ARIMA import ARIMA
try:
    from .HMM import HMM
except:
    print('HMM not set')
from .XGBoost import XGBoost

from .DeepST import DeepST
from .ST_ResNet import ST_ResNet

from .AMulti_GCLSTM import AMulti_GCLSTM
