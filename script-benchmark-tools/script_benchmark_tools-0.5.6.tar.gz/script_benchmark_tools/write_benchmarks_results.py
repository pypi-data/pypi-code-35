import os
from copy import copy

from terminal_table import Table

from script_benchmark_tools.benchmark_results import benchmark_results
from script_benchmark_tools.charts.plot_visual import plot_results


def generate_benchmarks(
        title,
        proof_data,
        filename,
        n_steps,
        benchmark,
        scripts
):
    proof_copy = copy(proof_data)
    output = "#%s\n\n" % title
    output += 'Proofs\n------\n\n'
    output += Table.create(
        [(
            str(proof_copy),
            str(script(arr=proof_data)),
            script.name(),
            script.user()
        ) for script in scripts],
        ('Input', 'Output', 'Script', 'User'),
        use_ansi=False
    )
    output += '\nPlots\n-----\n\n'
    output += '![%s](%s.png)\n\n' % (title, filename)
    benchmarks = map(
        lambda n: benchmark(scripts, n),
        n_steps
    )
    results = [(n, result) for n, result in benchmarks]
    output += '%s\n----------\n\n' % title
    for n, result in results:
        output += 'N = %d\n------\n\n' % n
        output += benchmark_results(result) + '\n'
    if not os.path.isdir('results'):
        umask = os.umask(0)
        try:
            os.mkdir('results', 0o777)
        finally:
            os.umask(umask)
    with open('results/%s.md' % filename, 'w') as f:
        f.write(output)
    plot = plot_results(results, title, loglog=True)
    plot.savefig('results/%s.png' % filename)
