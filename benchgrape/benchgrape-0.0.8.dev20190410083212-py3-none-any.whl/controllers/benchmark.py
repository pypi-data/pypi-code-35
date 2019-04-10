from cement import Controller, ex
import subprocess


class Benchmark(Controller):
    class Meta:
        label = 'benchmark'
        stacked_type = 'nested'
        stacked_on = 'base'

    @ex(help='start the locust suit.')
    def start(self):
        subprocess.run([
            "locust",
            "--locustfile=./benchgrape/locust/locustfiles/stability.py",
            "--host=%s" % "https://staging.chatgrape.com/"
        ])
