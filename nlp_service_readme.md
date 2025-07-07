# nlp\_service

## 📚 Proje Amacı

`nlp_service`, kullanıcıdan alınan doğal dildeki promptlara yanıt vererek arka planda bulunan veri kaynakları üzerinde çeşitli analizler yapan bir motor geliştirme amacıyla tasarlanmıştır. Kullanıcı dostu, modüler, geliştirilebilir ve test edilebilir bir mimari hedeflenmektedir.

---

## 🔧 Klasör Yapısı ve Açıklamaları

```
nlp_service/
├── adapters/                # Veri kaynaklarından (CSV) veri yüklenmesini sağlar
├── analyzers/               # Satış ve alış analizlerini yapar
├── engine/                  # Doğal dil işleme ve prompt çözümlemesini yönetir
├── data/                    # Girdi verilerinin saklandığı CSV dosyaları
├── tests/                   # Tüm birim testlerini içerir
├── pyproject.toml           # Proje ayarları, linter ve formatlama konfigürasyonu
└── README.md                # Proje dökümanı
```

- `adapters/`  → Verilerin pandas DataFrame'e yüklenmesini sağlayan **loader** sınıfları
- `analyzers/` → Satış ve alış veri analizlerini yapan **analyzer** sınıfları
- `engine/`     → Promptu analiz edip doğru analiz fonksiyonunu çağıran motor
- `tests/`      → Her katman için **pytest** testleri
- `data/`       → Örnek veri dosyaları (CSV)

---

## 🔄 Şu Ana Kadar Yapılanlar

1. 🔎 **Proje Mimarisi Kuruldu** (Adapters, Analyzers, Engine)
2. 🔹 **SalesAnalyzer** ve **PurchaseAnalyzer** geliştirildi ve test edildi.
3. 🔹 **RequestResolver**, **EntityExtractor**, **NLPEngine** yazıldı.
4. 🔹 Promptlar ve ay isimleri için enum yapısı tanımlandı.
5. 🔹 **pytest** testleri %100 başarı ile çalıştı.
6. 🔹 **mypy**, **ruff**, **black** entegre edildi ve kod temizliği sağlandı.

---

## 🔢 Bu Haftaki Hedefler

1. 🔹 Farklı analyzer scriptlerinin oluşturulması
2. 🔹 Uygulamayı terminal üzerinden kullanırken daha iyi çıktı görüntüleri alabilmek için Rich library ile CLI katmanının yazılması
3. 🔹 Yazılan birimlerin teslerinin yapılması

---

## 🔀 Geliştirilmeye Açık Alanlar

- Engine şu anda default promptları analiz edip response dönebiliyor. Fakat ilerleyen süreçte kullanıcıdan gelen daha 
spontane şekilde yazılmış promptlar analiz edilip response dönülebilir. 
- Pandas Dataframe'ler yerine gerçek bir veritabanından çekilen veriler işlenecek.
- 

---

## 📚 Kullanılan Kütüphaneler

| Kütüphane  | Amaç                                     |
| ---------- | ---------------------------------------- |
| **spaCy**  | Doğal Dil İşleme (tokenizasyon, matcher) |
| **pandas** | Veri yükleme ve analiz                   |
| **pytest** | Birim testleri                           |
| **mypy**   | Tip denetimi                             |
| **black**  | Kod formatlama                           |
| **ruff**   | Linter                                   |
| **Rich**   | CLI için estetik terminal çıktısı        |

---



