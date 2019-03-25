# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['gpu_utils', 'gpu_utils._scripts']

package_data = \
{'': ['*']}

install_requires = \
['colored>=1.3,<2.0', 'nvidia-ml-py3>=7.352,<8.0', 'psutil>=5.6,<6.0']

entry_points = \
{'console_scripts': ['gpu = gpu_utils._scripts.gpu:print_gpu_info',
                     'kill_interrupted_processes = '
                     'gpu_utils._scripts.kill_interrupted_processes:main',
                     'tmux_gpu_info = gpu_utils._scripts.tmux_gpu_info:main']}

setup_kwargs = {
    'name': 'gpu-utils',
    'version': '0.2.5',
    'description': 'Utility functions for working with GPUs.',
    'long_description': '# GPU Utils\n\nA few small functions/scripts for working with GPUs.\n\n## Requirements\n\n* Python 3.6+\n* Linux OS for full functionality (only tested on Ubuntu; I use `subprocess.run` for `kill` and `lsof`)\n  * Everything except `kill_interrupted_processes` should work on any OS\n\n## Installation\n\n```\npip install gpu-utils\n```\n\nThe PyPI page is [here][pypi page].\n\n## Usage\n\n```python\nfrom gpu_utils import gpu_init\n\n# sets GPU ids to use nvidia-smi ordering (CUDA_DEVICE_ORDER = PCI_BUS_ID)\n# finds the gpu with the most free utilization or memory\n# hides all other GPUs so you only use this one (CUDA_VISIBLE_DEVICES = <gpu_id>)\ngpu_id = gpu_init(best_gpu_metric="util") # could also use "mem"\n```\n\nIf you use TensorFlow or PyTorch, `gpu_init` can take care of another couple of steps for you:\n\n```python\n# a torch.device for the selected GPU\ndevice = gpu_init(ml_library="torch")\n```\n\n```python\nimport tensorflow as tf\n# a tf.ConfigProto to allow soft placement + GPU memory growth\nconfig = gpu_init(ml_library="tensorflow")\nsession = tf.Session(config=config)\n```\n\n## Command Line Scripts\n\n`gpu` is a more concise and prettier version of `nvidia-smi`. It is similar to [`gpustat`][gpustat] but with more control over the color configuration and the ability to show the full processes running on each GPU.\n\n`kill_interrupted_processes` is useful if you interrupt a process using a GPU but find that, even though `nvidia-smi` no longer shows the process, the memory is still being held. It will send `kill -9` to all such processes so you can reclaim your GPU memory.\n\n`tmux_gpu_info.py` just prints a list of the percent utilization of each GPU; you can, e.g., show this in the status bar of `tmux` to keep an eye on your GPUs.\n\n## Acknowledgements\n* Using `pynvml` instead of parsing `nvidia-smi` with regular expressions made this library a bit faster and much more robust than my previous regex parsing of `nivida-smi`\'s output; thanks to [`gpustat`][gpustat] for showing me this library and some ideas about the output format for the `gpu` script.\n\n[pypi page]: https://pypi.org/project/gpu-utils/\n[gpustat]: https://github.com/wookayin/gpustat\n',
    'author': 'Nathan Hunt',
    'author_email': 'neighthan.hunt@gmail.com',
    'url': 'https://github.com/neighthan/gpu-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
