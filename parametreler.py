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