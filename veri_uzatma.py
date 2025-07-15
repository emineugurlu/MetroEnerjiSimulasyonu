import pandas as pd

# Dinamik verilerinizin bulunduğu dosyanın yolu
dosya_yolu = 'dinamik_veriler.xlsx'

# Hedeflenen toplam saat sayısı (1 ay = 30 gün * 24 saat)
hedef_toplam_saat = 720

try:
    # Mevcut veriyi oku
    df_orijinal = pd.read_excel(dosya_yolu)
    print(f"'{dosya_yolu}' dosyasından {len(df_orijinal)} saatlik orijinal veri okundu.")

    # Orijinal 24 saatlik döngüyü al
    # Emin olmak için ilk 24 saati alalım (eğer dosyanızda daha fazla veri varsa)
    df_24_saat = df_orijinal.iloc[0:24].copy()

    # Yeni DataFrame oluşturmak için orijinal 24 saatlik veriyi tekrarlı olarak birleştir
    # Kaç kez tekrarlayacağımızı hesapla (hedef_toplam_saat / 24)
    tekrar_sayisi = hedef_toplam_saat // 24 # Tam bölme

    # Veriyi çoğalt
    df_uzatılmış = pd.concat([df_24_saat] * tekrar_sayisi, ignore_index=True)

    # 'Saat' sütununu 0'dan hedef_toplam_saat-1'e kadar yeniden oluştur
    df_uzatılmış['Saat'] = range(hedef_toplam_saat)

    # Uzatılmış veriyi aynı Excel dosyasına kaydet
    df_uzatılmış.to_excel(dosya_yolu, index=False)
    print(f"'{dosya_yolu}' dosyası {len(df_uzatılmış)} saate ({hedef_toplam_saat / 24:.0f} güne) uzatılarak güncellendi.")

except FileNotFoundError:
    print(f"Hata: '{dosya_yolu}' bulunamadı. Lütfen dosya yolunu kontrol edin.")
except Exception as e:
    print(f"Bir hata oluştu: {e}")