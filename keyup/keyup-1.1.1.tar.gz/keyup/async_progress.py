#!/usr/bin/env python
"""
Styled similar to tqdm, another progress bar implementation in Python.

See: https://github.com/noamraph/tqdm
"""
#from __future__ import unicode_literals
import asyncio
import time
from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts.progress_bar import formatters
from keyup.cauth import report_complete


style = Style.from_dict({
    '': 'orange',
})


async def ptk_main(loop=True, title='    Querying Amazon STS'):
    custom_formatters = [
        formatters.Label(suffix=': '),
        formatters.Bar(start='|', end='|', sym_a='#', sym_b='#', sym_c='-'),
        formatters.Text(' '),
        formatters.Progress(),
        formatters.Text(' '),
        formatters.Percentage(),
        formatters.Text(' [elapsed: '),
        formatters.TimeElapsed(),
        formatters.Text(' left: '),
        formatters.TimeLeft(),
        formatters.Text(', '),
        formatters.IterationsPerSecond(),
        formatters.Text(' iters/sec]'),
        formatters.Text('  '),
    ]

    with ProgressBar(style=style, formatters=custom_formatters) as pb:
        for i in pb(range(1600), label=title):
            #time.sleep(.01)
            await asyncio.sleep(0.001)

            if report_complete():
                break
    return True


if __name__ == '__main__':
    ptk_main()
