import pytest
import pandas as pd
from engine.sales_analyzer import SalesAnalyzer
from adapters.sales_loader import SalesDataLoader

@pytest.fixture
def analyzer():
    df = SalesDataLoader().load()
    return SalesAnalyzer(df)

def test_get_top_selling_product_by_revenue(analyzer):
    result = analyzer.get_top_selling_product_by_revenue(7)
    assert isinstance(result, str)
    assert "amount of money" in result
    assert "the top selling product by revenue is" in result

def test_get_average_basket_value(analyzer):
    result = analyzer.get_average_basket_value(month=7)
    assert "average basket amount" in result.lower()
    assert "july" in result.lower() or "7" in result


def test_get_total_sales_amount(analyzer):
    result = analyzer.get_total_sales_amount(month=7)
    assert "total sales amount" in result.lower()
    assert "july" in result.lower() or "7" in result


def test_get_top_customers_by_revenue(analyzer):
    result = analyzer.get_top_customers_by_revenue(month=7)
    assert "top 5 customer" in result.lower()


def test_get_weekday_vs_weekend_sales_revenue(analyzer):
    result = analyzer.get_weekday_vs_weekend_sales_revenue(month=7)
    assert "weekday" in result.lower()
    assert "weekend" in result.lower()

