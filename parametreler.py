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

# ==============================================================================
# EKONOMİK PARAMETRELER
# ==============================================================================

# Enerji Alım/Satım Fiyatları (TL/kWh) - Gerçekçi piyasa fiyatlarına göre güncellenebilir
# Bu değerler, günün farklı saatlerinde değişen tarifeleri yansıtacak şekilde bir liste olarak tanımlanabilir.
# Şimdilik sabit birer değer olarak başlayalım, sonra daha detaylı hale getirebiliriz.
SEBEKE_ALIM_FIYATI_TL_KWH = 2.5  # Şebekeden enerji alım maliyeti (Örnek değer)
SEBEKE_SATIS_FIYATI_TL_KWH = 1.8  # Şebekeye enerji satış geliri (Örnek değer)

# Yatırım (CAPEX) Maliyetleri (TL) - Birim maliyetler üzerinden hesaplanabilir
GUNES_PANELI_KURULUM_MALIYETI_TL_KWp = 6000 # Güneş paneli kWp başına kurulum maliyeti (Örnek değer)
RUZGAR_TURBINI_KURULUM_MALIYETI_TL_KW = 10000 # Rüzgar türbini kW başına kurulum maliyeti (Örnek değer)
BATARYA_KURULUM_MALIYETI_TL_KWH = 7000 # Batarya kWh başına kurulum maliyeti (Örnek değer)
EMS_SISTEMI_KURULUM_MALIYETI_TL = 500000 # EMS sisteminin kurulum maliyeti (Sabit örnek değer)

# İşletme ve Bakım (OPEX) Maliyetleri (Yıllık Yüzde)
GUNES_PANELI_OM_ORANI = 0.015 # Yıllık O&M maliyeti (kurulum maliyetinin %'si)
RUZGAR_TURBINI_OM_ORANI = 0.02 # Yıllık O&M maliyeti (kurulum maliyetinin %'si)
BATARYA_OM_ORANI = 0.025 # Yıllık O&M maliyeti (kurulum maliyetinin %'si)
# parametreler.py

# ... (Diğer parametreleriniz) ...

# Örnek değerler, sizin projenizin ihtiyaçlarına göre bu değerleri ayarlayın
TREN_BASINA_MAKS_TUKETIM_KWH = 500
FRENLEME_GERI_KAZANIM_ORANI = 0.3
MAKS_ISTASYON_TUKETIMI_KWH = 200
MAKS_GUNES_PANELI_URETIMI_KWH = 1000
MAKS_RUZGAR_TURBINI_URETIMI_KWH = 500
BATARYA_KAPASITESI_KWH = 20000
BATARYA_SARJ_VERIMI = 0.95  # <-- BU SATIRI EKLEYİN VEYA KONTROL EDİN!
BATARYA_DESARJ_VERIMI = 0.95 # <-- BU SATIRI EKLEYİN VEYA KONTROL EDİN!
BATARYA_ILK_DOLULUK_ORANI = 0.7
BATARYA_BOSALTMA_ESIGI_ORAN = 0.2
BATARYA_DOLDURMA_ESIGI_ORAN = 0.95
SEBEKE_ALIM_FIYATI_TL_KWH = 3.0
SEBEKE_SATIS_FIYATI_TL_KWH = 1.0
KARBON_EMISYON_FAKTORU_SEBEKE = 0.4 # kg CO2e/kWh
GUNES_PANELI_KURULUM_MALIYETI_TL_KWP = 5000 # TL/kWp
RUZGAR_TURBINI_KURULUM_MALIYETI_TL_KW = 7000 # TL/kW
BATARYA_KURULUM_MALIYETI_TL_KWH = 2000 # TL/kWh
EMS_SISTEMI_KURULUM_MALIYETI_TL = 50000 # TL
GUNES_PANELI_OM_ORANI = 0.01 # Yüzde olarak (örneğin %1)
RUZGAR_TURBINI_OM_ORANI = 0.02 # Yüzde olarak (örneğin %2)
BATARYA_OM_ORANI = 0.03 # Yüzde olarak (örneğin %3)
GUNES_PANELI_KAPASITESI_KWP = 100000 # KWP cinsinden kurulu güç
RUZGAR_TURBINI_KAPASITESI_KW = 50000 # KW cinsinden kurulu güç

DINAMIK_VERI_DOSYA_YOLU = 'dinamik_veriler.xlsx' # Dosyanızın adını ve yolunu kontrol edin