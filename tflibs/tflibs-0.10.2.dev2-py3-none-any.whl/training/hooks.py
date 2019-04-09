"""
    Session Run Hooks
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import threading
import os
import collections

import tensorflow as tf
from tflibs.image import encode


class BestModelExporterArgs(collections.namedtuple('BestModelExporterArgs',
                                                   ['metric_name', 'save_max'])):
    def __new__(cls, metric_name, save_max=True):
        return super(BestModelExporterArgs, cls).__new__(cls, metric_name, save_max)

    @property
    def __dict__(self):
        return super(BestModelExporterArgs, self)._asdict()


class EvaluationRunHook(tf.train.SessionRunHook):
    def __init__(self, estimator: tf.estimator.Estimator, input_fn, eval_steps: int, summary=True,
                 best_model_exporter_args: BestModelExporterArgs = None):
        self.estimator = estimator
        self.input_fn = input_fn
        self.eval_steps = eval_steps
        self.summary = summary
        self._lock = threading.Lock()
        self._best_model_exporter_args = best_model_exporter_args

    def before_run(self, run_context: tf.train.SessionRunContext):
        return tf.train.SessionRunArgs({'global_step': tf.train.get_or_create_global_step()})

    def after_run(self,
                  run_context: tf.train.SessionRunContext,  # pylint: disable=unused-argument
                  run_values: tf.train.SessionRunValues):
        global_step = run_values.results['global_step']
        if (global_step + 1) % self.eval_steps == 0:
            # Start new thread for evaluation
            t = threading.Thread(target=self._run_evaluation, args=(run_context,))
            t.start()

    def _run_evaluation(self, run_context: tf.train.SessionRunContext):
        if self._lock.acquire(False):
            hooks = []

            if self.summary:
                hooks.append(EvalSummaryHook(os.path.join(self.estimator.model_dir, 'eval')))

            if self._best_model_exporter_args is not None:
                hooks.append(BestModelExporterHook(**vars(self._best_model_exporter_args)))

            try:
                self.estimator.evaluate(self.input_fn, hooks=hooks)
            except Exception as e:
                tf.logging.info('Evaluation went wrong...')
                run_context.request_stop()
                raise e
            finally:
                self._lock.release()


class EvalSummaryHook(tf.train.SessionRunHook):
    def __init__(self,
                 summary_dir: str,
                 summary_op=None):
        self._summary_dir = summary_dir
        self._summary_op = summary_op
        self._summary_writer = None  # type: tf.summary.FileWriter
        self._finished = False

    def begin(self):
        self._summary_op = self._summary_op or tf.summary.merge_all()
        self._summary_writer = tf.summary.FileWriterCache.get(self._summary_dir)  # type: tf.summary.FileWriter

    def before_run(self, run_context: tf.train.SessionRunContext):
        return tf.train.SessionRunArgs({
            'summary': self._summary_op,
            'global_step': tf.train.get_or_create_global_step()
        }) if not self._finished and self._summary_op is not None else None

    def after_run(self,
                  run_context: tf.train.SessionRunContext,  # pylint: disable=unused-argument
                  run_values: tf.train.SessionRunValues):
        if not self._finished:
            self._summary_writer.add_summary(run_values.results['summary'], run_values.results['global_step'])
            self._finished = True


class BestModelExporterHook(tf.train.SessionRunHook):
    def __init__(self, metric_name: str, save_max=True):
        self._metric_name = metric_name
        self._metric = None

    @property
    def metric_name(self):
        return self._metric_name

    @property
    def metric(self):
        return self._metric

    def begin(self):
        metric_vars = tf.get_collection(tf.GraphKeys.METRIC_VARIABLES)
        tf.logging.info(metric_vars)

        self._metric = next((var for var in metric_vars if var.name == self.metric_name), None)

        if self.metric is None:
            raise ValueError('Metric variable named `{}` is not found'.format(self.metric_name))

    def before_run(self, run_context: tf.train.SessionRunContext):
        return tf.train.SessionRunArgs({
            'metric': self.metric,
        })

    def after_run(self,
                  run_context: tf.train.SessionRunContext,  # pylint: disable=unused-argument
                  run_values: tf.train.SessionRunValues):
        metric_val = run_values.results['metric']


class ImageSaverHook(tf.train.SessionRunHook):
    def __init__(self,
                 images,
                 image_dir):
        self.run_args = dict(
            map(lambda item: (item[0], tf.image.convert_image_dtype(item[1], tf.uint8)), images.items()))
        self.image_dir = image_dir
        self.iter = 0

        if not tf.gfile.Exists(self.image_dir):
            tf.gfile.MakeDirs(self.image_dir)

        tf.logging.info('ImageSaverHook: {}'.format(self.run_args))

    def before_run(self, run_context: tf.train.SessionRunContext):
        run_args = dict(self.run_args)
        run_args.update({'global_step': tf.train.get_or_create_global_step()})
        return tf.train.SessionRunArgs(run_args)

    def after_run(self,
                  run_context: tf.train.SessionRunContext,  # pylint: disable=unused-argument
                  run_values: tf.train.SessionRunValues):
        global_step = run_values.results['global_step']
        for k in self.run_args.keys():
            images = run_values.results[k]
            encoded = encode(images)
            with open(os.path.join(self.image_dir,
                                   '{key}_{gs:07d}_{iter:03d}.jpg'.format(
                                       key=k, gs=global_step, iter=self.iter)), 'wb') as f:
                f.write(encoded)

        self.iter += 1
