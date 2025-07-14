# main.py

import pandas as pd
import simulasyon_motoru as sm
import gorsellestirme as gorsel
import parametreler as p # Yeni: parametreler dosyasını içe aktarıyoruz

if __name__ == "__main__":
    print("--- Enerji Pozitif Metro Projesi - Dinamik Simülasyon Başlıyor ---")

    # Adım 1: Sabit Simülasyon Senaryolarını Excel dosyasından oku (eski yöntem, hala geçerli)
    try:
        excel_senaryolar_dosyasi = "senaryolar.xlsx"
        df_senaryolar = pd.read_excel(excel_senaryolar_dosyasi)
        print(f"\n--- '{excel_senaryolar_dosyasi}' dosyasından senaryolar yüklendi ---")
        # print(df_senaryolar) # Yüklenen senaryoları terminalde göster

    except FileNotFoundError:
        print(f"Hata: '{excel_senaryolar_dosyasi}' bulunamadı. Lütfen Excel dosyasının 'MetroProjesi' klasöründe olduğundan emin olun.")
        exit()

    # Adım 2: Dinamik Saatlik Veri Profillerini Excel dosyasından oku
    try:
        excel_dinamik_dosyasi = "dinamik_veriler.xlsx"
        df_dinamik_veriler = pd.read_excel(excel_dinamik_dosyasi)
        print(f"\n--- '{excel_dinamik_dosyasi}' dosyasından dinamik veriler yüklendi ---")
        # print(df_dinamik_veriler) # Yüklenen dinamik verileri terminalde göster

    except FileNotFoundError:
        print(f"Hata: '{excel_dinamik_dosyasi}' bulunamadı. Lütfen Excel dosyasının 'MetroProjesi' klasöründe olduğundan emin olun.")
        exit()

    # Adım 3: Her bir genel senaryo için simülasyonu çalıştır (eskisi gibi, günlük bazda)
    for index, row in df_senaryolar.iterrows():
        senaryo_adi = row['SenaryoAdı']
        print(f"\n\n--- Genel Senaryo Çalıştırılıyor: {senaryo_adi} ---")

        # Excel sütunlarından parametreleri al
        gunluk_sefer_sayisi_sabit = row['GunlukSeferSayisi']
        tren_basina_tuketim_kWh_sabit = row['TrenBasinaTuketimkWh']
        frenleme_geri_kazanim_orani_sabit = row['FrenlemeGeriKazanimOrani']
        istasyon_tuketimi_kWh_sabit = row['IstasyonTuketimikWh']
        gunes_paneli_uretimi_kWh_sabit = row['GunesPaneliUretimikWh']
        ruzgar_turbini_uretimi_kWh_sabit = row['RuzgarTurbiniUretimikWh']

        # Eskiden kullandığımız günlük hesaplama fonksiyonu (simulasyon_motoru.py'den silindiği için şimdilik devre dışı)
        # Bu kısım sadece genel bir özet içindi, şimdi daha dinamik bir yaklaşım kullanıyoruz.
        # Eğer bu tarz bir "statik günlük özet" istiyorsak, simulasyon_motoru.py'ye ayrı bir fonksiyon olarak tekrar eklemeliyiz.
        # Şimdilik, sadece dinamik sonuçların günlük toplamlarını kullanacağız.

    # Adım 4: Dinamik Simülasyonu Çalıştır (parametreler.py'den maksimum değerleri ve dinamik veriyi kullanarak)
    print(f"\n\n--- Dinamik (Saatlik) Simülasyon Çalıştırılıyor ---")

    dinamik_simulasyon_sonuclari = sm.hesapla_dinamik_enerji_dengesi(
        df_dinamik_veriler,
        p.TREN_BASINA_MAKS_TUKETIM_KWH,
        p.FRENLEME_GERI_KAZANIM_ORANI,
        p.MAKS_ISTASYON_TUKETIMI_KWH,
        p.MAKS_GUNES_PANELI_URETIMI_KWH,
        p.MAKS_RUZGAR_TURBINI_URETIMI_KWH,
        p.VARSAYILAN_GUNLUK_TOPLAM_SEFER
    )

    # Dinamik simülasyonun günlük toplamlarını göster
    print("\n--- Dinamik Simülasyon - Günlük Toplam Enerji Hesaplamaları ---")
    for key, value in dinamik_simulasyon_sonuclari["gunluk_toplamlar"].items():
        print(f"{key}: {value:.2f} kWh")

    print("\n--- Dinamik Simülasyon Yorumu ---")
    if dinamik_simulasyon_sonuclari["gunluk_toplamlar"]["Net Enerji Dengesi (kWh)"] < 0:
        print(f"Bu dinamik senaryoda metro sistemi günlük enerji fazlası vermektedir! (ENERJİ POZİTİF!)")
        print(f"Fazla enerji: {-dinamik_simulasyon_sonuclari['gunluk_toplamlar']['Net Enerji Dengesi (kWh)']:.2f} kWh")
    elif dinamik_simulasyon_sonuclari["gunluk_toplamlar"]["Net Enerji Dengesi (kWh)"] == 0:
        print("Bu dinamik senaryoda metro sistemi günlük enerji dengesindedir.")
    else:
        print(f"Bu dinamik senaryoda metro sistemi hala günlük enerji tüketmektedir. Enerji açığı: {dinamik_simulasyon_sonuclari['gunluk_toplamlar']['Net Enerji Dengesi (kWh)']:.2f} kWh")


    # Adım 5: Görselleştirmeleri Oluştur
    # Günlük toplamlar için çubuk grafik
    gorsel.enerji_dengesi_cubuk_grafigi_olustur(
        dinamik_simulasyon_sonuclari["gunluk_toplamlar"],
        grafik_adi="Dinamik Simülasyon - Günlük Toplam Enerji Dengesi"
    )

    # Saatlik veriler için çizgi grafik
    gorsel.enerji_dengesi_cizgi_grafigi_olustur(
        dinamik_simulasyon_sonuclari["saatlik_veri"],
        grafik_adi="Dinamik Simülasyon - Saatlik Enerji Akışı"
    )


    print("\n--- Dinamik Simülasyon ve Grafik Sonlandı ---")