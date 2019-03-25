from nlpyper.module import Module
from nlpyper.batch_source_module import BatchSourceModule
import sys
import os
import traceback
import time
import logging
import json
from logging.handlers import RotatingFileHandler


class Pipeline:

    def __init__(self, source_mod, pipeline_mods):
        # check types
        if not isinstance(source_mod, BatchSourceModule):
            msg = "Source {} is not of type SourceModule".format(source_mod.__class__.__name__)
            raise TypeError(msg)
        for i, mod in enumerate(pipeline_mods):
            if not isinstance(mod, Module):
                msg = "Module {} is not of type Module".format(mod.__class__.__name__)
                raise TypeError(msg)
        # init members
        self.docs = []
        self.source = source_mod
        self.pipeline = pipeline_mods
        self._set_module_ids()
        # init empty members
        self.context = {
            'conf': {
                'loglvl': logging.INFO,
                'logpath': '/tmp/log.txt',
            },
        }
        self.time_stats = {
            'tot': {
                'tot': -1,
                'ini': -1,
                'src': -1,
                'pip': -1,
            },
            'mod': {},
            'doc': {},
        }

        
    def setconf(self, conf):
        # check conf is a dict
        if not isinstance(conf, dict):
            raise TypeError("conf must be a dict")
        # overwrite given config parameters
        for k, v in conf.items():
            self.context['conf'][k] = v

            
    def process(self, doc, _id):
        # check doc is a dict
        if not isinstance(doc, dict):
            raise TypeError("Document must be a dict")
        # set ID to doc
        doc['id'] = _id
        # insert doc into doc list
        self.docs.append(doc)

        
    def run_batch(self, data):

        # start time
        start = time.perf_counter()

        # init log
        self._init_log()
        
        # init modules
        self._init_modules()

        # fetch documents
        self._fetch_documents(data)

        # create execution context
        self._refresh_execution_context()
        
        # process each document through the pipeline
        pipe_start = time.perf_counter()
        for module in self.pipeline:
            self._run_module(module)
        self.time_stats['tot']['pip'] = time.perf_counter() - pipe_start

        # ack successfuly processed docs
        result = []
        for doc in self.docs:
            try:
                doc_result = self.source.on_success(doc)
                result.append(doc_result)
            except NotImplementedError as e:
                self.log.warn(e)
            self.log.info("Finished processing doc {}".format(doc['id']))

        # register total time
        self.time_stats['tot']['tot'] = time.perf_counter() - start

        # log time statistics
        self.log.info("Time statistics:\n{}".format(self._generate_stats_report()))

        # build JSON (python list of objects) to return, containing all the docs in a list
        return result

        
    def _init_modules(self):
        try:
            init_start = time.perf_counter()
            try:
                self.log.debug("Initializing source module {}".format(self.source.get_id()))
                self.source.init(self.context, self.log)
                self.log.debug("Source module {} initialized".format(self.source.get_id()))
            except NotImplementedError as e:
                self.log.warn(e)

            for module in self.pipeline:
                try:
                    self.log.debug("Initializing module {}".format(module.get_id()))
                    module.init(self.context, self.log)
                    self.log.debug("Module {} initialized".format(module.get_id()))
                except NotImplementedError as e:
                    self.log.warn(e)
            self.time_stats['tot']['ini'] = time.perf_counter() - init_start
                    
        except Exception as e:
            module_id = module.get_id() if 'module' in locals() else self.source.get_id()
            self.log.error("Error initializing module {}: {}".format(module_id, e))
            self.log.error(traceback.format_exc())
            raise e

    def _fetch_documents(self, data):
        try:
            src_start = time.perf_counter()
            self.log.debug("Running source module {}".format(self.source.get_id()))
            self.source.run(self, data)
            self.log.debug("Source module {} finished".format(self.source.get_id()))
            self.time_stats['tot']['src'] = time.perf_counter() - src_start
            self.time_stats['mod'][self.source.get_id()] = self.time_stats['tot']['src']
        except NotImplementedError as e:
            self.log.warn(e)

    def _refresh_execution_context(self):
        self.context['n_docs'] = len(self.docs)

    def _run_module(self, module):
        self.log.debug("Running module {}".format(module.get_id()))
        error_docs = []
        for i, doc in enumerate(self.docs):
            self.log.debug("Processing doc {}".format(doc['id']))
            try:
                try:
                    mod_doc_start = time.perf_counter()
                    module.run_prev(doc, self.context)
                    mod_doc_time = time.perf_counter() - mod_doc_start
                    self._register_exec_time(module.get_id(), doc['id'], mod_doc_time)
                except NotImplementedError as e:
                    self.log.warn(e)
            except Exception as e:
                try:
                    self.source.on_error(doc)
                except NotImplementedError as e_:
                    self.log.warn(e_)
                error_docs.append(doc)
                self.log.error("Error processing doc {}: {}".format(doc['id'], e))
                self.log.error(traceback.format_exc())
        for doc in error_docs:
            self.docs.remove(doc)
        self.log.debug("Module {} finished".format(module.get_id()))
        self._refresh_execution_context()

    def _init_log(self):
        logdir = os.path.dirname(self.context['conf']['logpath'])
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        handler = RotatingFileHandler(self.context['conf']['logpath'], mode='a', maxBytes=5*1024*1024, backupCount=2, encoding='utf-8', delay=0)
        date_format = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', date_format)
        handler.setFormatter(formatter)
        self.log = logging.getLogger()
        self.log.setLevel(self.context['conf']['loglvl'])
        self.log.addHandler(handler)

    def _set_module_ids(self):
        module_names = []
        modules = [self.source] + self.pipeline
        for module in modules:
            name = module.__class__.__name__
            module_names.append(name)
            ind = module_names.count(name)
            module.set_id('{}_{}'.format(name, ind))

    def _register_exec_time(self, module_id, doc_id, exec_time):
        # add time to module stats
        if module_id not in self.time_stats['mod']:
            self.time_stats['mod'][module_id] = 0
        self.time_stats['mod'][module_id] += exec_time
        # add time to doc stats
        if doc_id not in self.time_stats['doc']:
            self.time_stats['doc'][doc_id] = 0
        self.time_stats['doc'][doc_id] += exec_time

    def _generate_stats_report(self):
        report = "TOTAL"
        report += "\nTotal\t{}".format(self._format_time(self.time_stats['tot']['tot']))
        report += "\nInitializing\t{}".format(self._format_time(self.time_stats['tot']['ini']))
        report += "\nFetching\t{}".format(self._format_time(self.time_stats['tot']['src']))
        report += "\nProcessing\t{}".format(self._format_time(self.time_stats['tot']['pip']))
        report += "\nMODULES"
        modules = self.time_stats['mod'].items()
        for module_id, exec_time in modules:
            report += '\n{}\t{}'.format(module_id, self._format_time(exec_time))
        report += '\nDOCUMENTS'
        docs = self.time_stats['doc'].items()
        if len(docs) > 0:
            report += '\nAVG\t{}'.format(self._format_time(sum([ doc[1] for doc in docs ]) / len(docs)))
            report += '\nMAX\t{}'.format(self._format_time(max([ doc[1] for doc in docs ])))
            report += '\nMIN\t{}'.format(self._format_time(min([ doc[1] for doc in docs ])))
        else:
            report += '\nAVG\t-'
            report += '\nMAX\t-'
            report += '\nMIN\t-'
        return report

    @staticmethod
    def _format_time(seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return '{:d}:{:02d}:{:02d}'.format(int(h), int(m), int(s))
