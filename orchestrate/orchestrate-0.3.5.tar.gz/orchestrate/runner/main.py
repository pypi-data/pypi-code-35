from orchestrate.runner.optimizer import SigOptOptimizer
from orchestrate.runner.options import Options


def main():
  options = Options.from_env()
  optimizer = SigOptOptimizer(
    config=options.load_config(),
    log_path=options.log_path,
    suggestion_path=options.suggestion_path,
    pod_name=options.pod_name,
    experiment_id=options.experiment_id,
  )
  optimizer.optimization_loop()
