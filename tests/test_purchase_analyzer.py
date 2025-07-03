import pytest
from adapters.purchase_loader import PurchaseDataLoader
from engine.purchase_analyzer import PurchaseAnalyzer


@pytest.fixture
def purchase_analyzer():
    df = PurchaseDataLoader().load()
    return PurchaseAnalyzer(df)


def test_get_total_purchase_amount(purchase_analyzer):
    result = purchase_analyzer.get_total_purchase_amount(7)
    assert isinstance(result, str)
    assert "Total purchase amount" in result
    assert "TL" in result


def test_get_top_supplier_by_spending(purchase_analyzer):
    result = purchase_analyzer.get_top_supplier_by_spending(7)
    assert isinstance(result, str)
    assert "top supplier" in result
    assert "TL" in result


def test_get_supplier_purchase_count(purchase_analyzer):
    result = purchase_analyzer.get_supplier_purchase_count(7)
    assert isinstance(result, str)
    assert "most purchase transactions" in result
    assert any(char.isdigit() for char in result)


def test_get_top_purchased_product(purchase_analyzer):
    result = purchase_analyzer.get_top_purchased_product(7)
    assert isinstance(result, str)
    assert "most purchased product" in result
    assert any(char.isdigit() for char in result)
