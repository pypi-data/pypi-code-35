# pylint: disable=missing-docstring,invalid-name
# %%
__all__ = ['setup_logger']
import fn_reflection._external as _e


def setup_logger(logger: _e.logging.Logger,
                 log_path: str,
                 fmt: str = 't:%(asctime)s\tlv:%(levelname)s\tn:%(name)s\tm:%(message)s')->None:
    if _e.os.path.exists(log_path):
        print(f'log file not found, log_path:{log_path}', file=_e.sys.stderr)
        return
    if not logger.handlers:
        fmtr = _e.logging.Formatter(fmt)
        sh = _e.logging.StreamHandler()
        sh.setFormatter(fmtr)
        fh = _e.logging.FileHandler(filename=log_path)
        fh.setFormatter(fmtr)
        logger.addHandler(sh)
        logger.addHandler(fh)
    return logger
