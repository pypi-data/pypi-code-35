import ludwig
import pandas as pd

model_definition = {
    'input_features':[{
        'name': 'l1',
        'type': 'text',
        'encoder': 'rnn',
        'cell_type': 'lstm',
        'reduce_output': 'None'}],
    'output_features':[{
        'name': 'l2',
        'type': 'text',
        'decoder': 'generator',
        'cell_type': 'lstm',
        'attention': 'bahdanau',
        'loss':{
            'type': 'sampled_softmax_cross_entropy'}}]}

model = ludwig.LudwigModel(model_definition=model_definition)

data_df = pd.DataFrame({
    'l1':['aa ab ac', 'ad ae af'],
    'l2':['za zb zc', 'zd ze zf']})

model_stats = model.train(data_df=data_df)

preds = model.predict(data_df=data_df)