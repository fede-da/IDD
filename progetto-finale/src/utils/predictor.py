import pandas as pd
import flexmatcher
from flexmatcher import FlexMatcher

from src.dataset.dataset import Dataset


class Predictor:
    schema_list: [pd.DataFrame]
    mapping_list: [dict]
    fm: FlexMatcher

    def __init__(self, datasets: [Dataset]):
        self.schema_list = []
        self.mapping_list = []
        for dataset in datasets:
            self.schema_list.append(dataset.to_dataframe())
            self.mapping_list.append(dataset.get_mapping())
        self.fm = flexmatcher.FlexMatcher(self.schema_list, self.mapping_list, sample_size=100)
        self.fm.train()

    def predict_mapping(self, dataframe_to_predict: pd.DataFrame):
        return self.fm.make_prediction(dataframe_to_predict)
