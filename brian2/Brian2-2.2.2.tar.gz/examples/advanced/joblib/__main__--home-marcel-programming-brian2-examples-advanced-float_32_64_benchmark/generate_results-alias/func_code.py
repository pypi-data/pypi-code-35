# first line: 99
def generate_results(num_repeats):
    results = {}

    for name in ['CUBA', 'COBA']:
        for target in ['numpy', 'cython', 'weave']:
            for dtype in [float32, float64]:
                prefs.codegen.target = target
                prefs.core.default_float_dtype = dtype
                prefs.codegen.cpp.extra_compile_args_gcc += ['-std=c++11']
                times = [run_benchmark(name) for repeat in range(num_repeats)]
                results[name, target, dtype.__name__] = amin(times)

    for name in ['CUBA', 'COBA']:
        for dtype in [float32, float64]:
            times = []
            for _ in range(num_repeats):
                reset_device()
                reinit_devices()
                set_device('cpp_standalone', directory=None, with_output=False,
                           clean=True)
                prefs.codegen.cpp.extra_compile_args_gcc += ['-std=c++11']
                prefs.core.default_float_dtype = dtype
                times.append(run_benchmark(name))
            results[name, 'cpp_standalone', dtype.__name__] = amin(times)

    return results
