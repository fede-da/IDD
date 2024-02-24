import pandas as pd


class Dataset:
    _val: dict
    _header: [str]
    _mapping: dict

    def __init__(self, header: [str], mapping: dict, val: [any]):
        self._header = header
        self._mapping = mapping
        self._val = val

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self._val, columns=self._header)

    def get_mapping(self):
        return self._mapping
