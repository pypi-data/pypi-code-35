#!/usr/bin/env python
import pyleiades as eia
import os
from matplotlib import pyplot as plt

# Create a visual
visual = eia.Visual(['coal', 'nuclear'])
visual.include_energy('renewable')
visual.linegraph(subject='totals', freq='yearly', start_date='1970')
# Save and display the visual
fig_path = os.path.join(os.path.dirname(eia.__file__), 'fig', 'demo-plot.png')
plt.savefig(fig_path, dpi=300)
plt.show()
