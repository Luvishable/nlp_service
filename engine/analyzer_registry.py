from analyzers.purchase_analyzer import PurchaseAnalyzer
from analyzers.sales_analyzer import SalesAnalyzer

ANALYZER_MAPPING = {
    "get_total_sales_amount": SalesAnalyzer(),
    "get_total_purchase_amount": PurchaseAnalyzer(),
    "get_top_supplier_by_spending": PurchaseAnalyzer(),
    "get_supplier_purchase_count": PurchaseAnalyzer(),
    "get_top_purchased_product": PurchaseAnalyzer(),
}