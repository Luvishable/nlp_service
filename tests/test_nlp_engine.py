import pytest
from engine.nlp_engine import NLPEngine

@pytest.fixture
def nlp_engine() -> NLPEngine:
    return NLPEngine()


def test_unknown_request(nlp_engine: NLPEngine) -> None:
    result = nlp_engine.process_request("What is the weather today?")
    assert "couldn't understand" in result.lower()


def test_missing_month(nlp_engine: NLPEngine) -> None:
    result = nlp_engine.process_request("Show me total sales")
    assert "specify a month" in result.lower()


def test_sales_request(nlp_engine: NLPEngine) -> None:
    result = nlp_engine.process_request("Show me total sales for July")
    assert "total sales amount" in result.lower()


def test_purchase_request(nlp_engine: NLPEngine) -> None:
    result = nlp_engine.process_request("Show me total purchase for July")
    assert "total purchase amount" in result.lower()
