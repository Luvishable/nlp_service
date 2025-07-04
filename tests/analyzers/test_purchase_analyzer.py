import pytest
from analyzers.purchase_analyzer import PurchaseAnalyzer


@pytest.fixture
def purchase_analyzer() -> PurchaseAnalyzer:
    """
    PurchaseAnalyzer fixture → Her testte yeni bir örnek döner.
    """
    return PurchaseAnalyzer()


def test_get_total_purchase_amount(purchase_analyzer: PurchaseAnalyzer) -> None:
    result = purchase_analyzer.get_total_purchase_amount(month=7)
    assert isinstance(result, str)
    assert "total purchase amount" in result.lower()
    assert "tl" in result.lower()


def test_get_top_supplier_by_spending(purchase_analyzer: PurchaseAnalyzer) -> None:
    result = purchase_analyzer.get_top_supplier_by_spending(month=7)
    assert isinstance(result, str)
    assert "top supplier" in result.lower()
    assert "tl" in result.lower()


def test_get_supplier_purchase_count(purchase_analyzer: PurchaseAnalyzer) -> None:
    result = purchase_analyzer.get_supplier_purchase_count(month=7)
    assert isinstance(result, str)
    assert "most purchase transactions" in result.lower()
    assert any(char.isdigit() for char in result)


def test_get_top_purchased_product(purchase_analyzer: PurchaseAnalyzer) -> None:
    result = purchase_analyzer.get_top_purchased_product(month=7)
    assert isinstance(result, str)
    assert "most purchased product" in result.lower()
    assert any(char.isdigit() for char in result)
