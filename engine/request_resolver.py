import spacy
from spacy.matcher import PhraseMatcher
from typing import Optional, Dict, List


class RequestResolver:
    def __init__(self, nlp: Optional[spacy.language.Language] = None) -> None:
        self.nlp = nlp or spacy.blank("en")
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        self.request_patterns: Dict[str, List[str]] = {}
        self._load_patterns()
        self._build_matcher()

    def _load_patterns(self) -> None:
        self.request_patterns = {
            "get_total_sales_amount": ["total sales", "sales amount"],
            "get_total_purchase_amount": ["total purchase", "purchase amount"],
        }

    def _build_matcher(self) -> None:
        for request_name, patterns in self.request_patterns.items():
            phrase_patterns = [self.nlp.make_doc(p) for p in patterns]
            self.matcher.add(request_name, phrase_patterns)

    def resolve(self, text: str) -> Optional[str]:
        doc = self.nlp(text)
        matches = self.matcher(doc)
        if not matches:
            return None
        match_id, _, _ = matches[0]
        return self.nlp.vocab.strings[match_id]
