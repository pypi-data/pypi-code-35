import argparse
from collections import defaultdict
import json
from datetime import datetime
import glob
from pathlib import Path
from pprint import pprint
import re
from typing import List, DefaultDict

import filelock
import json_lines
import numpy as np


NAME = 'json-log-plots.log'


def write_event(root: Path, step: int, prefix: str = '', **data):
    data = {prefix + k: v for k, v in data.items()}
    data['step'] = step
    data['dt'] = datetime.now().isoformat()
    with filelock.FileLock(root / '.{NANE}.lock'):
        with (root / NAME).open('at') as log:
            log.write(json.dumps(data, sort_keys=True))
            log.write('\n')


def plot(*args, ymin=None, ymax=None, xmin=None, xmax=None,
         max_points=200, legend=True, title=None,
         print_keys=False, print_paths=False, plt=None, newfigure=True,
         x_scale=1, without_confidence_intervals=False):
    """
    Use in the notebook like this::

        %matplotlib inline
        import json_log_plots
        json_log_plots.plot('./runs/oc2', './runs/oc1', 'loss', 'valid_loss')

    """
    if plt is None:
        from matplotlib import pyplot as plt
    paths, keys = [], []
    for x in args:
        if x.startswith('.') or '/' in x:
            if '*' in x:
                paths.extend(glob.glob(x))
            else:
                paths.append(x)
        else:
            keys.append(x)
    if print_paths:
        print('Found paths: {}'.format(' '.join(sorted(paths))))
    if newfigure:
        plt.figure(figsize=(12, 8))
    keys = keys or ['loss', 'valid_loss']

    ylim_kw = {}
    if ymin is not None:
        ylim_kw['ymin'] = ymin
    if ymax is not None:
        ylim_kw['ymax'] = ymax
    if ylim_kw:
        plt.ylim(**ylim_kw)

    xlim_kw = {}
    if xmin is not None:
        xlim_kw['xmin'] = xmin
    if xmax is not None:
        xlim_kw['xmax'] = xmax
    if xlim_kw:
        plt.xlim(**xlim_kw)
    all_keys = set()
    for path in sorted(paths):
        path = Path(path)
        with json_lines.open(path / NAME, broken=True) as f:
            events = list(f)
        all_keys.update(k for e in events for k in e)
        for key in sorted(keys):
            xs, ys, ys_err = [], [], []
            for e in events:
                if key in e:
                    xs.append(e['step'] * x_scale)
                    ys.append(e[key])
                    std_key = key + '_std'
                    if std_key in e and not without_confidence_intervals:
                        ys_err.append(e[std_key])
            if xs:
                if np.isnan(ys).any():
                    print('Warning: NaN {} for {}'.format(key, path))
                if len(xs) > 2 * max_points:
                    indices = (np.arange(0, len(xs) - 1, len(xs) / max_points)
                               .astype(np.int32))
                    xs = np.array(xs)[indices[1:]]
                    ys = _smooth(ys, indices)
                    if ys_err:
                        ys_err = _smooth(ys_err, indices)
                label = '{}: {}'.format(path, key)
                if label.startswith('_'):
                    label = ' ' + label
                if ys_err:
                    ys_err = 1.96 * np.array(ys_err)
                    plt.errorbar(xs, ys, yerr=ys_err,
                                 fmt='-o', capsize=5, capthick=2,
                                 label=label)
                else:
                    plt.plot(xs, ys, label=label)
                plt.legend()
    if newfigure:
        plt.grid()
    if legend:
        plt.legend()
    if title:
        plt.title(title)
    if print_keys:
        print('Found keys: {}'
              .format(', '.join(sorted(all_keys - {'step', 'dt'}))))


def _smooth(ys, indices):
    return [np.mean(ys[idx: indices[i + 1]])
            for i, idx in enumerate(indices[:-1])]


def main():
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg('args', type=str, nargs='+')
    arg('--ymin', type=float)
    arg('--ymax', type=float)
    arg('--xmin', type=int)
    arg('--xmax', type=int)
    arg('--params', action='store_true')
    arg('--max-points', type=int, default=200)
    arg('--legend', type=int, default=1)
    arg('--title')
    arg('--print-keys', action='store_true')
    arg('--print-paths', action='store_true')
    arg('--x-scale', type=float, default=1.0)
    arg('--output', default='/dev/stdout')
    arg('--without-confidence-intervals', action='store_true')

    args = parser.parse_args()

    positional = args.args
    named = {k: v for k, v in vars(args).items() if k not in ['output', 'args']}

    if plt is None:
        from matplotlib import pyplot as plt
    plot(*positional, plt=plt, newfigure=True, **named)
    plt.savefig(args.output)


if __name__ == "__main__":
    main()
