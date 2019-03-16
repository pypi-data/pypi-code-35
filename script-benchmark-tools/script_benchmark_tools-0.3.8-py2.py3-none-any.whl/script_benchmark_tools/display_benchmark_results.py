
from ansi_colours import AnsiColours as Colour
from terminal_table import Table


def display_benchmark_results(results):
    headers, rows = make_benchmark_results(results)

    print(Table.create(rows, headers(), column_colours=[Colour.green, Colour.yellow, Colour.red]))


def benchmark_results(results):
    headers, rows = make_benchmark_results(results)

    return Table.create(rows, headers())


def make_benchmark_results(results):
    def headers():
        return 'min', 'avg', 'max', 'func', 'name'

    def row(result):
        return (
            "%.9f" % result.min(),
            "%.9f" % result.average(),
            "%.9f" % result.max(),
            result.name(),
            result.user()
        )

    results.sort(key=lambda r: r.min())
    rows = [row(result) for result in results]
    return headers, rows
