
from lxml import etree


class DataExtractor:
    file_red: str

    def __init__(self, input_string: str):
        self.file_red = input_string

    def extract_data(self) -> dict:
        # XPath
        root = etree.fromstring(self.file_red)
        pmc_element = root.xpath('//article-id[@pub-id-type="pmc"]')[0]
        return {
            #"pmcid": pmc_element
            "pmcid": pmc_element.text,
            #"title": "",
            #"abstract": "",
            #"keywords": "",
            #"tables": [],
            #"figures": []
        }


