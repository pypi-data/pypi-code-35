#!/usr/bin/env python
import pyleiades as eia
import os
from matplotlib import pyplot as plt

# Create a visual
visual = eia.Visual(['coal', 'nuclear'])
visual.include_energy('renewable')

# Demo single visual
visual.linegraph(freq='yearly', start_date='1970')
fig_path = os.path.join(os.path.dirname(eia.__file__), 'fig', 'demo-plot.png')
plt.savefig(fig_path, dpi=300)
plt.close()

# Demo double visual
fig, axs = plt.subplots(2, 1, figsize=(8, 6))
axs[0] = visual.linegraph(ax=axs[0], freq='yearly', start_date='1970')
axs[1] = visual.linegraph(ax=axs[1], freq='monthly',
                          start_date='1980', end_date='2000')
plt.tight_layout()
plt.show()
