import pytest
from analyzers.sales_analyzer import SalesAnalyzer


@pytest.fixture
def analyzer() -> SalesAnalyzer:
    """
    SalesAnalyzer fixture → Her test için yeni bir örnek döner.
    """
    return SalesAnalyzer()


def test_get_total_sales_amount(analyzer: SalesAnalyzer) -> None:
    result = analyzer.get_total_sales_amount(month=7)
    assert isinstance(result, str)
    assert "total sales amount" in result.lower()
    assert "7" in result or "july" in result.lower()


def test_get_top_selling_product_by_quantity(analyzer: SalesAnalyzer) -> None:
    result = analyzer.get_top_selling_product_by_quantity(month=7)
    assert isinstance(result, str)
    assert "top selling product" in result.lower()
    assert "quantity" in result.lower()


def test_get_top_selling_product_by_revenue(analyzer: SalesAnalyzer) -> None:
    result = analyzer.get_top_selling_product_by_revenue(month=7)
    assert isinstance(result, str)
    assert "top selling product by revenue" in result.lower()
    assert "amount of money" in result.lower()


def test_get_average_basket_value(analyzer: SalesAnalyzer) -> None:
    result = analyzer.get_average_basket_value(month=7)
    assert isinstance(result, str)
    assert "average basket amount" in result.lower()
    assert "7" in result or "july" in result.lower()


def test_get_top_customers_by_revenue(analyzer: SalesAnalyzer) -> None:
    result = analyzer.get_top_customers_by_revenue(month=7)
    assert isinstance(result, str)
    assert "top 5 customers" in result.lower() or "top 5 customer" in result.lower()


def test_get_weekday_vs_weekend_sales_revenue(analyzer: SalesAnalyzer) -> None:
    result = analyzer.get_weekday_vs_weekend_sales_revenue(month=7)
    assert isinstance(result, str)
    assert "weekday" in result.lower()
    assert "weekend" in result.lower()
