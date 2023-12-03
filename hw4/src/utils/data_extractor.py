from lxml import etree


class DataExtractor:
    file_red: str

    def __init__(self, input_string: str):
        self.file_red = input_string

    def _map_nodes_as_strings_list(self, nodes):
        return list(map(lambda node: str(etree.tostring(node, pretty_print=True, method="xml").decode()).strip().replace(' xmlns:xlink="http://www.w3.org/1999/xlink"', '').strip(), nodes))

    def _map_node_as_string(self, node):
        return str(etree.tostring(node, pretty_print=True, method="xml").decode()).strip().replace(' xmlns:xlink="http://www.w3.org/1999/xlink"', '')

    # must return a list of dictionaries
    def _get_table_paragraphs(self, root):
        paragraph_reference_nodes = root.xpath('//p[xref[@ref-type="table"]]')
        paragraph_list = []

        for paragraph in paragraph_reference_nodes:
            para_to_add = {}
            full_text = [paragraph.text or ""]

            # Including text from immediate children (ignoring nested tags)
            for child in paragraph:
                if child.tail:
                    full_text.append(child.tail)

            para_to_add["text"] = ''.join(full_text).strip()

            # Find all <xref> elements with an 'rid' attribute within the paragraph
            xrefs = paragraph.xpath('.//xref[@rid]')
            refs = []

            # Extract corresponding <ref> elements
            for xref in xrefs:
                rid = xref.get('rid')
                ref = root.xpath(f'//ref[@id="{rid}"]')
                if ref:
                    ref_content = self._map_node_as_string(ref[0])
                    refs.append(ref_content)

            # Add refs to the paragraph dictionary if any are found
            if refs:
                para_to_add["citation"] = refs

            paragraph_list.append(para_to_add)

        return paragraph_list

    def _get_cell_contents(self, root):
        # returns list of numbers as string
        colspan_content_as_strings = root.xpath('//thead/tr/td/@colspan')
        cells = []
        for string in colspan_content_as_strings:
            paragraphs_containing_string = root.xpath(f"//p[contains(text(), '{string}')]")
            cells.append({
                "content": string,
                "cited_in": self._map_nodes_as_strings_list(paragraphs_containing_string)
            })
        return cells


    def extract_data(self) -> dict:
        # XPath
        root = etree.fromstring(self.file_red)
        pmc_id_node = root.xpath('//article-id[@pub-id-type="pmc"]')[0]
        title_node = root.xpath('//article-title')[0]
        abstract_node = root.xpath('//abstract/*/p')[0]
        # This is a list!
        keywords_nodes = root.xpath('//kwd-group/kwd')
        table_wrap_id = root.xpath('//table-wrap/@id')[0]
        caption_node = root.xpath('//caption/p')[0]
        foots_node = root.xpath('//table-wrap-foot/p')
        # complete below
        table_node = root.xpath('//thead | //tbody')
        paragraphs = self._get_table_paragraphs(root)
        colspan_nodes = self._get_cell_contents(root)
        return {
            "pmcid": pmc_id_node.text,
            "content": {
                "title": title_node.text,
                # tostring method adds a string, trimmed with "replace" function
                "abstract": self._map_node_as_string(abstract_node),
                "keywords": self._map_nodes_as_strings_list(keywords_nodes),
                "tables": [
                    {
                        "table_id": table_wrap_id,
                        "body": self._map_nodes_as_strings_list(table_node),
                        "caption": self._map_node_as_string(caption_node),
                        "caption_citations": [],
                        # foots is a list of texts
                        "foots": self._map_nodes_as_strings_list(foots_node),
                        "paragraph": paragraphs,
                        "cells":colspan_nodes
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
        }

