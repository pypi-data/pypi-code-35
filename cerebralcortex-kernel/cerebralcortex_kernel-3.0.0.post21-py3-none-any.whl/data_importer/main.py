# from cerebralcortex.data_importer.data_parsers import mcerebrum_data_parser
# from cerebralcortex.data_importer.metadata_parsers import mcerebrum_metadata_parser
# from cerebralcortex.data_importer import import_dir
#
# import_dir(
#     cc_config="/home/ali/IdeaProjects/CerebralCortex-2.0/conf/",
#     input_data_dir="/home/ali/IdeaProjects/MD2K_DATA/rice_data/te/",
#     #batch_size=200,
#     compression='gzip',
#     header=None,
#     data_file_extension=[".gz"],
#     # allowed_filename_pattern="REGEX PATTERN",
#     data_parser=mcerebrum_data_parser,
#     metadata_parser=mcerebrum_metadata_parser,
#     gen_report=True
# )

# import scipy.io
# import pandas as pd
# import numpy as np
#
# mat = scipy.io.loadmat('/home/ali/IdeaProjects/MD2K_DATA/matlab_data/p02_s02.mat')
# mat = {k:v for k, v in mat.items() if k[0] != '_'}
# data = pd.DataFrame({k: pd.Series(v[0]) for k, v in mat.items()})
# data.to_csv("/home/ali/IdeaProjects/MD2K_DATA/matlab_data/example.csv")
# print("done")

# import gzip
# print("ddd")
# pass
# print("xxx")
# with gzip.open('/home/ali/IdeaProjects/MD2K_DATA/rice_data/raw/f7c1b540-cf9b-4d44-8196-372594b9a194/20180808/953c1f8a-fa30-3d5f-86c2-cdb128f1a619/e3ea8cd6-b7b3-4f7b-ae1f-dd8d28236ec5.gz','rt') as f:
#     try:
#         for line in f:
#             print('got line', line)
#     except:
#         pass
#

import re
word = 'fubar'
regexp = re.compile(r'uba')
if regexp.search(word):
    print('matched')
