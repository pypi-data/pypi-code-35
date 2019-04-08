from testing import benchmark

def run_tests():
    Logger.log("running tests...")
    #run_benchmarks
    benchmark.do_benchmarks()

    #run_voice tests

if __name__ == "__main__":
    run_tests()