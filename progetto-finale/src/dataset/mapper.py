from src.dataset.dataset import Dataset
from src.utils.predictor import Predictor


class Mapper:
    _mediated_schema: [str]
    _predicted_mapping: [dict]

    def __init__(self, mediated_schema: [str]):
        self._mediated_schema = mediated_schema
        self._predicted_mapping = []

    def map(self, datasets_for_training: [Dataset], datasets_to_predict: [Dataset]):
        predictor = Predictor(datasets_for_training)
        for dataset in datasets_to_predict:
            self._predicted_mapping.append(
                predictor.predict_mapping(dataset.to_dataframe())
            )

    def print_mapping(self):
        for mapping in self._predicted_mapping:
            print(mapping)
