from .base_analyzer import BaseAnalyzer

class ToplamSatisAnalyzer(BaseAnalyzer):
    def _filter_data(self):
        # Tüm veri kullanılır
        return self._data

    def _generate_response(self, df):
        if df.empty:
            return "Satış verisi bulunamadı."
        toplam_satis = df['satis_miktari'].sum()
        return f"Toplam satış miktarı {toplam_satis}."
