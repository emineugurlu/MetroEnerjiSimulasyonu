# parametreler.py

# Metro sistemi ve enerji simülasyonu için temel/maksimum parametreler

# Tren ve Hareket Parametreleri
# Bir trenin bir seferde tükettiği maksimum enerji (kWh)
TREN_BASINA_MAKS_TUKETIM_KWH = 50
# Frenleme enerjisinin ne kadarının geri kazanıldığı oranı (0 ile 1 arasında)
FRENLEME_GERI_KAZANIM_ORANI = 0.30
# Toplam günlük varsayılan sefer sayısı (dinamik modelde saatlik yoğunlukla çarpılacak)
VARSAYILAN_GUNLUK_TOPLAM_SEFER = 1000

# İstasyon ve Diğer Tüketim Parametreleri
# Bir günde istasyonların maksimum toplam enerji tüketimi (kWh)
MAKS_ISTASYON_TUKETIMI_KWH = 2000

# Yenilenebilir Enerji Üretim Parametreleri
# Güneş panellerinden günlük beklenen maksimum toplam enerji üretimi (kWh)
MAKS_GUNES_PANELI_URETIMI_KWH = 38000
# Rüzgar türbinlerinden günlük beklenen maksimum toplam enerji üretimi (kWh)
MAKS_RUZGAR_TURBINI_URETIMI_KWH = 3000

# Saatlik simülasyon için toplam saat sayısı
TOPLAM_SIMULASYON_SAATI = 24
# parametreler.py (Devamı)

# Batarya (Enerji Depolama) Parametreleri
# Bataryanın maksimum enerji depolama kapasitesi (kWh)
# parametreler.py içinde
BATARYA_KAPASITESI_KWH = 30000 # Örneğin, mevcut değerin iki katı
# Bataryanın şarj verimliliği (0 ile 1 arasında)
SARJ_VERIMLILIGI = 0.90 # %90 verimle şarj
# Bataryanın deşarj verimliliği (0 ile 1 arasında)
DESARJ_VERIMLILIGI = 0.90 # %90 verimle deşarj
# Simülasyon başlangıcında bataryanın doluluk oranı (0 ile 1 arasında)
BASLANGIC_BATARYA_DOLULUK_ORANI = 0.50 # %50 dolu başla
# parametreler.py (Devamı)

# Elektrik Birim Fiyatları (TL/kWh) - Örnek Fiyatlandırma
# Gündüz (08:00-18:00) ve Gece (18:00-08:00) gibi farklı tarifeler uygulanabilir.
# Basitlik için her saat için ayrı bir fiyat tanımlayabiliriz veya tarifelere bölebiliriz.
# Şimdilik basit bir günlük döngü için 24 saatlik fiyat listesi.

# NOT: Bu değerler piyasa koşullarına göre değiştirilebilir.
# Gündüz tarifesinin daha yüksek, gece tarifesinin daha düşük olduğu bir senaryo.
ELEKTRIK_BIRIM_FIYATLARI_TL_KWH = [
    0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.9, 1.0, # 00:00 - 07:00 (gece/sabah düşük)
    1.2, 1.3, 1.4, 1.5, 1.5, 1.4, 1.3, 1.2, # 08:00 - 15:00 (gündüz yüksek)
    1.1, 1.0, 0.9, 0.8, 0.8, 0.8, 0.8, 0.8  # 16:00 - 23:00 (akşam düşüşü, geceye geçiş)
]

# Batarya yönetiminde kullanılacak eşik değerler
# Batarya boşaltma eşiği: Bu oranın altına düşüldüğünde batarya deşarjı durdurulur. (örn. %20)
BATARYA_BOSALTMA_ESIGI_ORAN = 0.20
# Batarya doldurma eşiği: Bu oranın üzerine çıkıldığında batarya şarjı durdurulur. (örn. %95)
BATARYA_DOLDURMA_ESIGI_ORAN = 0.95
# parametreler.py (Devamı)

# Elektrik Birim Fiyatları (TL/kWh) - Örnek Fiyatlandırma
# Gündüz (08:00-18:00) ve Gece (18:00-08:00) gibi farklı tarifeler uygulanabilir.
# Basitlik için her saat için ayrı bir fiyat tanımlayabiliriz veya tarifelere bölebiliriz.
# Şimdilik basit bir günlük döngü için 24 saatlik fiyat listesi.

# NOT: Bu değerler piyasa koşullarına göre değiştirilebilir.
# Gündüz tarifesinin daha yüksek, gece tarifesinin daha düşük olduğu bir senaryo.
ELEKTRIK_BIRIM_FIYATLARI_TL_KWH = [
    0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.9, 1.0, # 00:00 - 07:00 (gece/sabah düşük)
    1.2, 1.3, 1.4, 1.5, 1.5, 1.4, 1.3, 1.2, # 08:00 - 15:00 (gündüz yüksek)
    1.1, 1.0, 0.9, 0.8, 0.8, 0.8, 0.8, 0.8  # 16:00 - 23:00 (akşam düşüşü, geceye geçiş)
]

# Batarya yönetiminde kullanılacak eşik değerler
# Batarya boşaltma eşiği: Bu oranın altına düşüldüğünde batarya deşarjı durdurulur. (örn. %20)
BATARYA_BOSALTMA_ESIGI_ORAN = 0.20
# Batarya doldurma eşiği: Bu oranın üzerine çıkıldığında batarya şarjı durdurulur. (örn. %95)
BATARYA_DOLDURMA_ESIGI_ORAN = 0.95
# parametreler.py
# ... diğer parametreler ...

# Elektrik Fiyatları
ELEKTRIK_BIRIM_FIYATLARI_TL_KWH = 2.0  # Şebekeden alım fiyatı (örnek)
ELEKTRIK_BIRIM_FIYATLARI_TL_KWH_SATIS = 1.0 # Şebekeye satış fiyatı (örnek) - YENİ EKLENEN SATIR

# ... diğer parametreler ...