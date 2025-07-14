# parametreler.py

# Metro sistemi ve enerji simülasyonu için varsayılan parametreler

# Tren ve Hareket Parametreleri
GUNLUK_SEFER_SAYISI = 1000
TREN_BASINA_TUKETIM_KWH = 50
FRENLEME_GERI_KAZANIM_ORANI = 0.30

# İstasyon ve Diğer Tüketim Parametreleri
ISTASYON_TUKETIMI_KWH = 2000

# Yenilenebilir Enerji Üretim Parametreleri
# Güneş panellerinden günlük beklenen üretim
GUNES_PANELI_URETIMI_KWH = 38000 # Güneş enerjisi üretimini 38000 kWh'ye yükseltiyoruz (örnek)
# Rüzgar türbinlerinden günlük beklenen üretim
RUZGAR_TURBINI_URETIMI_KWH = 3000