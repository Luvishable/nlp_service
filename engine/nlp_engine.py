from engine.entity_extractor import EntityExtractor
from engine.request_resolver import RequestResolver
from engine.analyzer_registry import ANALYZER_MAPPING
from typing import Callable, Optional

class NLPEngine:
    def __init__(self) -> None:
        self.entity_extractor: EntityExtractor = EntityExtractor()
        self.request_resolver: RequestResolver = RequestResolver()

    def process_request(self, user_input: str) -> str:
        request_name = self.request_resolver.resolve(user_input)
        if not request_name:
            return "Sorry, I couldn't understand your request."

        month = self.entity_extractor.extract_month(user_input)
        if month is None:
            return "Please specify a month in your request."

        analyzer = ANALYZER_MAPPING.get(request_name)
        if not analyzer:
            return "Sorry, no analyzer found for this request."

        analyzer_method: Optional[Callable[[int], str]] = getattr(analyzer, request_name, None)

        if not analyzer_method:
            return "Sorry, I can't process this type of request."

        return analyzer_method(month)
