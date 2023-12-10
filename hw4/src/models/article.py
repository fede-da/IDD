import jsonfrom typing import Any# noinspection SpellCheckingInspectionclass Article:    pmcid: str    title: str    abstract: str    keywords: [str]    tables: [object]    figures: [object]    def __init__(self, pmcid: str, title: str, abstract: str, keywords: list, tables: list,figures: list):        self.pmcid = pmcid        self.title = title        self.abstract = abstract        self.keywords = keywords        self.tables = tables        self.figures = figures    @ classmethod    def from_dict(cls, data: dict):        pmcid = data.get('pmcid', '')        content = data.get('content', {})        title = content.get('title', '')        abstract = content.get('abstract', '')        keywords = content.get('keywords', [])        tables = content.get('tables', [])        figures = content.get('figures', [])        return cls(pmcid, title, abstract, keywords, tables, figures)    def to_dict(self):        return {"pmcid": self.pmcid,                "content": {"title": self.title,                "abstract": self.abstract,                "keywords": self.keywords,                "tables": [table.to_dict() if hasattr(table, 'to_dict') else table for table in self.tables],                "figures": [figure.to_dict() if hasattr(figure, 'to_dict') else figure for figure in self.figures]}}    def to_json(self):        return json.dumps(self.to_dict())