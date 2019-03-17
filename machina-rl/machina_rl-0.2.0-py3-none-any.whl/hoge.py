import numpy as np
import torch
from time import time

start = time()
x = np.random.uniform(-1, 1, (20, 1000, 6))
#x = torch.tensor(x, dtype=torch.float)
print('numpy1:', time()-start)

start = time()
x = np.random.uniform(-1, 1, (20, 1000, 6)).astype(np.float32)
#x = torch.from_numpy(x)
print('numpy2:', time()-start)

# case 2
start = time()
x = torch.rand(20, 1000, 6, dtype=torch.float)*2-1.
print('pytorch 1:', time()-start)

# case 3
start = time()
x = torch.empty(20, 1000, 6, dtype=torch.float).uniform_(-1,1)
print('pytorch 2:', time()-start)
