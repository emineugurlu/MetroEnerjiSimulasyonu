# main.py

import pandas as pd
import simulasyon_motoru as sm
import gorsellestirme as gorsel
import parametreler as p
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("--- Enerji Pozitif Metro Projesi - Akıllı EMS Entegreli Dinamik Simülasyon Başlıyor ---")

    # Adım 1: Dinamik Saatlik Veri Profillerini Excel dosyasından oku
    try:
        excel_dinamik_dosyasi = "dinamik_veriler.xlsx"
        df_dinamik_veriler = pd.read_excel(excel_dinamik_dosyasi)
        print(f"\n--- '{excel_dinamik_dosyasi}' dosyasından dinamik veriler yüklendi ---")

    except FileNotFoundError:
        print(f"Hata: '{excel_dinamik_dosyasi}' bulunamadı. Lütfen Excel dosyasının 'MetroProjesi' klasöründe olduğundan emin olun.")
        exit()

    # Adım 2: Dinamik Simülasyonu Akıllı Batarya Entegrasyonu ile Çalıştır
    print(f"\n\n--- Dinamik (Saatlik) Simülasyon Akıllı EMS ile Çalıştırılıyor ---")

    dinamik_simulasyon_sonuclari = sm.hesapla_dinamik_enerji_dengesi(
        df_dinamik_veriler,
        p.TREN_BASINA_MAKS_TUKETIM_KWH,
        p.FRENLEME_GERI_KAZANIM_ORANI,
        p.MAKS_ISTASYON_TUKETIMI_KWH,
        p.MAKS_GUNES_PANELI_URETIMI_KWH,
        p.MAKS_RUZGAR_TURBINI_URETIMI_KWH,
        p.VARSAYILAN_GUNLUK_TOPLAM_SEFER,
        # Batarya Parametreleri
        p.BATARYA_KAPASITESI_KWH,
        p.SARJ_VERIMLILIGI,
        p.DESARJ_VERIMLILIGI,
        p.BASLANGIC_BATARYA_DOLULUK_ORANI,
        p.BATARYA_BOSALTMA_ESIGI_ORAN, # Yeni: Batarya Boşaltma Eşiği
        p.BATARYA_DOLDURMA_ESIGI_ORAN, # Yeni: Batarya Doldurma Eşiği
        # Elektrik Fiyatları Parametresi
        p.ELEKTRIK_BIRIM_FIYATLARI_TL_KWH # Yeni: Elektrik Birim Fiyatları
    )

    # Dinamik simülasyonun günlük toplamlarını göster
    print("\n--- Dinamik Simülasyon - Günlük Toplam Enerji Hesaplamaları (Akıllı EMS Entegreli) ---")
    for key, value in dinamik_simulasyon_sonuclari["gunluk_toplamlar"].items():
        print(f"{key}: {value:.2f} kWh" if "kWh" in key else f"{key}: {value:.2f} TL") # Maliyeti TL olarak göster

    print("\n--- Dinamik Simülasyon Yorumu (Akıllı EMS Entegreli) ---")
    net_enerji_dengesi_sebeke = dinamik_simulasyon_sonuclari["gunluk_toplamlar"]["Net Enerji Dengesi (Şebeke Etkisi ile) (kWh)"]
    toplam_maliyet = dinamik_simulasyon_sonuclari["gunluk_toplamlar"]["Toplam Enerji Maliyeti (TL)"]

    if net_enerji_dengesi_sebeke < 0:
        print(f"Bu dinamik senaryoda metro sistemi günlük enerji fazlası vermektedir! (ENERJİ POZİTİF!)")
        print(f"Fazla enerji (şebekeye verilen): {-net_enerji_dengesi_sebeke:.2f} kWh")
    elif net_enerji_dengesi_sebeke == 0:
        print("Bu dinamik senaryoda metro sistemi günlük enerji dengesindedir (şebekeden alım/verme yok).")
    else:
        print(f"Bu dinamik senaryoda metro sistemi günlük enerji tüketmektedir. Enerji açığı (şebekeden alınan): {net_enerji_dengesi_sebeke:.2f} kWh")

    print(f"Günlük Toplam Enerji Maliyeti/Geliri: {toplam_maliyet:.2f} TL")
    if toplam_maliyet < 0:
        print(f"Sistem günlük olarak {abs(toplam_maliyet):.2f} TL gelir elde etmektedir (Enerji Satışı).")
    elif toplam_maliyet > 0:
        print(f"Sistem günlük olarak {toplam_maliyet:.2f} TL maliyet oluşturmaktadır (Enerji Alımı).")
    else:
        print(f"Sistem günlük olarak enerji maliyeti/geliri dengesindedir.")


    # Adım 4: Görselleştirmeleri Oluştur
    # Günlük toplamlar için çubuk grafik (Şebeke Alım/Verme dahil)
    gorsel.enerji_dengesi_cubuk_grafigi_olustur(
        dinamik_simulasyon_sonuclari["gunluk_toplamlar"],
        grafik_adi="Dinamik Simülasyon - Günlük Toplam Enerji Dengesi (Akıllı EMS ile)"
    )

    # Saatlik veriler için çizgi grafik (Şebeke Alım/Verme gösteren)
    gorsel.enerji_dengesi_cizgi_grafigi_olustur(
        dinamik_simulasyon_sonuclari["saatlik_veri"],
        grafik_adi="Dinamik Simülasyon - Saatlik Enerji Akışı (Akıllı EMS ile)"
    )

    # Saatlik Batarya Doluluk Grafiği
    gorsel.batarya_doluluk_grafigi_olustur(
        dinamik_simulasyon_sonuclari["saatlik_veri"],
        grafik_adi="Dinamik Simülasyon - Saatlik Batarya Doluluk Seviyesi (Akıllı EMS ile)"
    )

    # Saatlik Batarya Şarj/Deşarj Akım Grafiği
    gorsel.batarya_akim_grafigi_olustur(
        dinamik_simulasyon_sonuclari["saatlik_veri"],
        grafik_adi="Dinamik Simülasyon - Saatlik Batarya Şarj/Deşarj Akışı (Akıllı EMS ile)"
    )

    # Yeni: Saatlik Enerji Maliyeti/Geliri Grafiği
    gorsel.saatlik_maliyet_grafigi_olustur(
        dinamik_simulasyon_sonuclari["saatlik_veri"],
        grafik_adi="Dinamik Simülasyon - Saatlik Enerji Maliyeti/Geliri (Akıllı EMS ile)"
    )

    print("\n--- Dinamik Simülasyon ve Tüm Grafikler Sonlandı ---")
    plt.show() # Tüm grafik pencerelerinin açık kalmasını sağlar