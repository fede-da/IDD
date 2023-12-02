
from lxml import etree


class DataExtractor:
    file_red: str

    def __init__(self, input_string: str):
        self.file_red = input_string

    def extract_data(self) -> dict:
        # XPath
        root = etree.fromstring(self.file_red)
        pmc_id_node = root.xpath('//article-id[@pub-id-type="pmc"]')[0]
        title_node = root.xpath('//article-title')[0]
        abstract_node = root.xpath('//abstract/*/p')[0]
        # This is a list!
        keywords_nodes = root.xpath('//kwd-group/kwd')
        table_wrap_id = root.xpath('//table-wrap/@id')[0]
        return {
            "pmcid": pmc_id_node.text,
            "title": title_node.text,
            # tostring method adds a string, trimmed with "replace" function
            "abstract": str(etree.tostring(abstract_node, pretty_print=True, method="xml").decode()).replace(' xmlns:xlink="http://www.w3.org/1999/xlink"', ''),
            "keywords": list(map(lambda node: node.text, keywords_nodes)),
            "tables": [
                {
                    "table_id": table_wrap_id,
                    "body": "",
                    "caption": "",
                    "caption_citations": [],
                    # foots is a list of texts
                    "foots": [],
                    "paragraph":
                    [
                        {
                            # here goes the text of the paragraph where the table was cited
                            "text": "",
                            # bibliography refence if a paper was cited in extracted text
                            "citations": []
                        }
                    ],
                    "cells":
                    [
                        {
                            # text contained in a cell
                            "content": "",
                            # text of the paragraph where the text of the cell was mentioned –if the content is repeated in more than one cell, still use one element to report them
                            "cited_in": []
                        }
                    ]

                 }
            ],
            "figures":
                [
                    {
                        "fig_id": "",
                        "src": "",
                        "caption": "",
                        "paragraph":
                        [
                            {
                                "cited_in": [],
                                "citations": []
                            }
                        ]

                    },
                ]
        }


