from .base_analyzer import BaseAnalyzer

class TemmuzSatisAnalyzer(BaseAnalyzer):
    def _filter_data(self):
        return self._data[self._data['ay'].str.lower() == 'temmuz']

    def _generate_response(self, df):
        if df.empty:
            return "Temmuz için veri yok."
        en_cok_satan = df.groupby('personel')['satis_miktari'].sum().idxmax()
        toplam_satis = df['satis_miktari'].sum()
        return f"Temmuz ayının en çok satış yapan personeli {en_cok_satan}, toplam satış {toplam_satis}."
