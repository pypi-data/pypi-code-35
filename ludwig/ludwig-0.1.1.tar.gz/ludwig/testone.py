import logging
import pandas as pd
from pprint import pprint

import ludwig

model = ludwig.LudwigModel(
    model_definition={
        "input_features": [{"name": "text", "level": "char", "type": "text", "encoder": "rnn"}],
        "output_features": [{"name": "is_name", "type": "binary"}],
        "training": {"epochs": 20}
    }
)

positive = ["james", "ruth"]
negative = ["house", "flower"]
dataset_df = pd.DataFrame({
    "text": positive + negative,
    "is_name": [True] * len(positive) + [False] * len(negative),
})

stats = model.train(
    data_df=dataset_df,
    logging_level=logging.DEBUG
)
pprint(stats)
