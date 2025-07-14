# main.py

import pandas as pd # Yeni: Pandas kütüphanesini içe aktarıyoruz
import simulasyon_motoru as sm
import gorsellestirme as gorsel # parametreler.py artık doğrudan kullanılmayacak

if __name__ == "__main__":
    print("--- Enerji Pozitif Metro Projesi - Gelişmiş Simülasyon Başlıyor ---")

    # Adım 1: Senaryoları Excel dosyasından oku
    try:
        # Excel dosyasının adını ve yolunu belirt
        excel_dosyasi = "senaryolar.xlsx"
        df_senaryolar = pd.read_excel(excel_dosyasi)
        print(f"\n--- '{excel_dosyasi}' dosyasından senaryolar yüklendi ---")
        print(df_senaryolar) # Yüklenen senaryoları terminalde göster

    except FileNotFoundError:
        print(f"Hata: '{excel_dosyasi}' bulunamadı. Lütfen Excel dosyasının 'MetroProjesi' klasöründe olduğundan emin olun.")
        exit() # Dosya bulunamazsa programı sonlandır

    # Adım 2: Her bir senaryo için simülasyonu çalıştır
    for index, row in df_senaryolar.iterrows():
        senaryo_adi = row['SenaryoAdı']
        print(f"\n\n--- Senaryo Çalıştırılıyor: {senaryo_adi} ---")

        # Excel sütunlarından parametreleri al
        gunluk_sefer_sayisi = row['GunlukSeferSayisi']
        tren_basina_tuketim_kWh = row['TrenBasinaTuketimkWh']
        frenleme_geri_kazanim_orani = row['FrenlemeGeriKazanimOrani']
        istasyon_tuketimi_kWh = row['IstasyonTuketimikWh']
        gunes_paneli_uretimi_kWh = row['GunesPaneliUretimikWh']
        ruzgar_turbini_uretimi_kWh = row['RuzgarTurbiniUretimikWh']

        # Simülasyon motorunu çalıştır
        sonuclar = sm.hesapla_enerji_dengesi(
            gunluk_sefer_sayisi,
            tren_basina_tuketim_kWh,
            frenleme_geri_kazanim_orani,
            istasyon_tuketimi_kWh,
            gunes_paneli_uretimi_kWh,
            ruzgar_turbini_uretimi_kWh
        )

        print("\n--- Günlük Enerji Hesaplamaları ---")
        for key, value in sonuclar.items():
            print(f"{key}: {value:.2f} kWh")

        print("\n--- Simülasyon Yorumu ---")
        if sonuclar["Net Enerji Dengesi (kWh)"] < 0:
            print(f"Bu senaryoda metro sistemi enerji fazlası vermektedir! (ENERJİ POZİTİF!)")
            print(f"Fazla enerji: {-sonuclar['Net Enerji Dengesi (kWh)']:.2f} kWh")
        elif sonuclar["Net Enerji Dengesi (kWh)"] == 0:
            print("Bu senaryoda metro sistemi enerji dengesindedir. Ne tüketiyor ne de fazlası var.")
        else:
            print(f"Bu senaryoda metro sistemi hala enerji tüketmektedir. Enerji pozitif olmak için daha fazla enerji üretimi veya daha az tüketim gerekli.")
            print(f"Enerji açığı: {sonuclar['Net Enerji Dengesi (kWh)']:.2f} kWh")

        # Görselleştirme fonksiyonunu çağır
        gorsel.enerji_dengesi_grafigi_olustur(sonuclar)

    print("\n--- Tüm Senaryolar Tamamlandı ---")