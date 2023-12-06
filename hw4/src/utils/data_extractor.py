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
    def _get_table_paragraphs(self, root, table_id):
        paragraph_reference_nodes = root.xpath(f"//p[xref[@ref-type='table' and @rid='{table_id}']]")
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

    def _get_cell_contents(self, node):
        # returns list of numbers as string
        td_content = node.xpath('.//td/text()')
        cells = []
        for string in td_content:
            paragraphs_containing_string = node.xpath(f".//p[contains(text(), \"{string}\")]")
            cells.append({
                "content": string,
                "cited_in": self._map_nodes_as_strings_list(paragraphs_containing_string)
            })
        return cells

    def _extract_figures(self, root, pmc_id):
        namespaces = {'xlink': 'http://www.w3.org/1999/xlink'}
        fig_elements = root.xpath('//fig')

        figures = []
        for fig in fig_elements:
            fig_id = fig.get('id')  # Get the 'id' attribute of 'fig'
            # Find the first caption_paragraph '<p>' inside 'fig' -> 'caption'
            caption_paragraph = fig.findtext('.//caption/p')
            source = fig.xpath('.//graphic/@xlink:href', namespaces=namespaces)[0]
            source = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/bin/{source}.jpg"
            # TODO: Completare estrazione citations slide 14
            paragraph = {}
            cited_in_paragraph_nodes = root.xpath(f"//p[xref[@ref-type='fig' and @rid='{fig_id}']]")
            citations_paragraphs = []
            for node in cited_in_paragraph_nodes:
                bibr_tags = node.xpath(".//xref[@ref-type='bibr']/@rid")
                if bibr_tags:
                    for bibr_tag in bibr_tags:
                        ref = root.xpath(f'//ref[@id="{bibr_tag}"]')
                        if ref:
                            ref_content = self._map_node_as_string(ref[0])
                            citations_paragraphs.append(ref_content)
            paragraph["cited_in"] = self._map_nodes_as_strings_list(cited_in_paragraph_nodes)
            paragraph["citations"] = citations_paragraphs
            figures.append({"id": fig_id, "src": source, "caption": caption_paragraph.strip(), "paragraph": paragraph})
        return figures



    def _get_tables(self, root):
        ret = []
        tables_wrap = root.xpath('//table-wrap')
        for table in tables_wrap:
            table_id = table.get('id')
            caption_node = table.xpath('.//caption/p')[0]
            foots_node = table.xpath('.//table-wrap-foot/p')
            # complete below
            table_node = table.xpath('.//thead | .//tbody')
            paragraphs = self._get_table_paragraphs(root, table_id)
            ret.append({
                    "table_id": table_id,
                    "body": self._map_nodes_as_strings_list(table_node),
                    "caption": self._map_node_as_string(caption_node),
                    "foots": self._map_nodes_as_strings_list(foots_node),
                    "paragraphs": paragraphs,
                    "cells": self._get_cell_contents(table)
            })
        return ret

    def extract_data(self) -> dict:
        # XPath
        root = etree.fromstring(self.file_red)
        pmc_id_node = root.xpath('//article-id[@pub-id-type="pmc"]')[0]
        title_node = root.xpath('//article-title')[0]
        abstract_node = root.xpath('//abstract/*/p')[0]
        # This is a list!
        keywords_nodes = root.xpath('//kwd-group/kwd')
        return {
            "pmcid": pmc_id_node.text,
            "content": {
                "title": title_node.text,
                # tostring method adds a string, trimmed with "replace" function
                "abstract": self._map_node_as_string(abstract_node),
                "keywords": list(map(lambda node: node.text, keywords_nodes)),
                "tables": self._get_tables(root),
                "figures": self._extract_figures(root, pmc_id_node.text)
                    #[
                     #   {
                      #      "fig_id": "",
                      #      "src": "",
                       #     "caption": "",
                       #     "paragraph":
                       #     [
                        #        {
                         #           "cited_in": [],
                          #          "citations": []
                          #      }
                           # ]
                        #},
                    #]
            }
        }

