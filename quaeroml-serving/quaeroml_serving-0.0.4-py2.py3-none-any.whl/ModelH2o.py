from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import zipfile
import json
import csv
import subprocess

import pandas as pd
import h2o

def csv_dump(path, data):
    fh          = open(path, 'w+')
    csv_writer  = csv.writer(fh, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    csv_writer.writerow( data['keys'] )
    for line in data['data']:
        csv_writer.writerow(line)

class ModelH2o(object):
    def __init__(self, opts):
        self.opts       = opts
        self.is_mojo    = False
        self.name       = opts['name'] + '_' + opts['version']
        #mojo or mojo pipeline
        if opts['model']['path'].endswith('.zip'):
            self.is_mojo = True

        h2o.init()
        
        if self.is_mojo:
            if not os.path.isdir('models'):
                os.makedirs('models')

            zip_ref = zipfile.ZipFile(opts['model']['path'], 'r')
            zip_ref.extractall( os.path.join('models', self.name ) )
            zip_ref.close()
            
            # if not os.path.exists( os.path.join('models', self.name, 'mojo-pipeline', 'pipeline.mojo') ):
                # raise Exception('H2o mojo not yet supported. Supported is Driverless AI pipeline scoring mojo')

        if not self.is_mojo:
            self.model  = h2o.load_model( opts['model']['path'] )

    def inference(self, input):
        if self.is_mojo:
            in_path     = os.path.join('models', self.name, 'input.csv')
            out_path    = os.path.join('models', self.name, 'out.csv')
            mojo_path   = os.path.join('models', self.name, 'mojo-pipeline', 'pipeline.mojo')
            mojor_path  = os.path.join('models', self.name, 'mojo-pipeline', 'mojo2-runtime.jar')
            
            csv_dump(in_path, input)
            
            fh          = open('procout', "w")
            proc_args   = ['java', '-Dai.h2o.mojos.runtime.license.key='+self.opts['model']['key'], '-cp', mojor_path, 'ai.h2o.mojos.ExecuteMojo', mojo_path, in_path, out_path]
            proc        = subprocess.call(proc_args, stdout = fh, stderr = fh)
            fh.close()
            
            # stdout      = proc.communicate()[0]
            # stderr      = proc.communicate()[1]
    
            predictions = h2o.import_file(out_path)

        if not self.is_mojo:
            df          = h2o.H2OFrame(input['data'], column_names=input['keys'])
            predictions = self.model.predict(df)

        result_df   = predictions.as_data_frame()
        values      = result_df.to_json(orient='split')

        result          = json.loads(values)
        result['keys']  = result['columns']
        del result['columns']
        del result['index']

        return result
