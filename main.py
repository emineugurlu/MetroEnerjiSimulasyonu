# main.py

import pandas as pd
import simulasyon_motoru as sm
import gorsellestirme as gorsel
import parametreler
import matplotlib.pyplot as plt # Bu import olmalı

if __name__ == "__main__":
    print("--- Enerji Pozitif Metro Projesi - Akıllı EMS Entegreli Dinamik Simülasyon Başlıyor ---")

    # Adım 1: Dinamik Saatlik Veri Profillerini Excel dosyasından oku
    try:
        excel_dinamik_dosyasi = "dinamik_veriler.xlsx"
        df_dinamik_veriler = pd.read_excel(excel_dinamik_dosyasi) # Bu satır veriyi df_dinamik_veriler'e yüklüyor
        print(f"\n--- '{excel_dinamik_dosyasi}' dosyasından dinamik veriler yüklendi ---")

    except FileNotFoundError:
        print(f"Hata: '{excel_dinamik_dosyasi}' bulunamadı. Lütfen Excel dosyasının 'MetroProjesi' klasöründe olduğundan emin olun.")
        exit() # Dosya bulunamazsa programdan çık

    # Adım 2: Dinamik Simülasyonu Akıllı Batarya Entegrasyonu ile Çalıştır
    print(f"\n\n--- Dinamik (Saatlik) Simülasyon Akıllı EMS ile Çalıştırılıyor ({len(df_dinamik_veriler) / 24:.1f} Günlük) ---")

    # main.py dosyasının ilgili kısmı
# ...
    dinamik_simulasyon_sonuclari = sm.hesapla_dinamik_enerji_dengesi(
        dinamik_veriler_df=df_dinamik_veriler,
        tren_basina_maks_tuketim_kwh=parametreler.TREN_BASINA_MAKS_TUKETIM_KWH,
        frenleme_geri_kazanim_orani=parametreler.FRENLEME_GERI_KAZANIM_ORANI,
        maks_istasyon_tuketimi_kwh=parametreler.MAKS_ISTASYON_TUKETIMI_KWH,
        maks_gunes_paneli_uretimi_kwh=parametreler.MAKS_GUNES_PANELI_URETIMI_KWH,
        maks_ruzgar_turbini_uretimi_kwh=parametreler.MAKS_RUZGAR_TURBINI_URETIMI_KWH,
        batarya_kapasitesi_kwh=parametreler.BATARYA_KAPASITESI_KWH,
        sarj_verimliligi=parametreler.BATARYA_SARJ_VERIMI,
        desarj_verimliligi=parametreler.BATARYA_DESARJ_VERIMI,
        baslangic_batarya_doluluk_orani=parametreler.BATARYA_ILK_DOLULUK_ORANI,
        batarya_bosaltma_esigi_oran=parametreler.BATARYA_BOSALTMA_ESIGI_ORAN,
        batarya_doldurma_esigi_oran=parametreler.BATARYA_DOLDURMA_ESIGI_ORAN,
        sebeke_alim_fiyati_tl_kwh=parametreler.SEBEKE_ALIM_FIYATI_TL_KWH,
        sebeke_satis_fiyati_tl_kwh=parametreler.SEBEKE_SATIS_FIYATI_TL_KWH,
        # BURADA DÜZELTME YAPIN: "emision" yerine "emisyon" olmalı
        karbon_emisyon_faktoru_sebeke=parametreler.KARBON_EMISYON_FAKTORU_SEBEKE, # <-- BU SATIRI KONTROL ET
        gunes_paneli_kurulum_maliyeti_tl_kwp=parametreler.GUNES_PANELI_KURULUM_MALIYETI_TL_KWP,
        ruzgar_turbini_kurulum_maliyeti_tl_kw=parametreler.RUZGAR_TURBINI_KURULUM_MALIYETI_TL_KW,
        batarya_kurulum_maliyeti_tl_kwh=parametreler.BATARYA_KURULUM_MALIYETI_TL_KWH,
        ems_sistemi_kurulum_maliyeti_tl=parametreler.EMS_SISTEMI_KURULUM_MALIYETI_TL,
        gunes_paneli_om_orani=parametreler.GUNES_PANELI_OM_ORANI,
        ruzgar_turbini_om_orani=parametreler.RUZGAR_TURBINI_OM_ORANI,
        batarya_om_orani=parametreler.BATARYA_OM_ORANI,
        gunes_paneli_kapasitesi_kwp=parametreler.GUNES_PANELI_KAPASITESI_KWP,
        ruzgar_turbini_kapasitesi_kw=parametreler.RUZGAR_TURBINI_KAPASITESI_KW
    )
# ...

    if dinamik_simulasyon_sonuclari:
        saatlik_veri_df = pd.DataFrame(dinamik_simulasyon_sonuclari['saatlik_veri'])
        gunluk_toplamlar_dict = dinamik_simulasyon_sonuclari['gunluk_toplamlar']

        print(f"\n--- Dinamik (24 Saatlik / {dinamik_simulasyon_sonuclari['simulasyon_suresi_gun']:.1f} Günlük) Simülasyon Akıllı EMS ile Çalıştırılıyor ---")

        # Adım 3: Sonuçları Yazdır
        print("\n--- Dinamik Simülasyon Sonuçları (Akıllı EMS Entegreli) ---")
        for key, value in gunluk_toplamlar_dict.items():
            if isinstance(value, (int, float)):
                print(f"- {key}: {value:,.2f}")
            else:
                print(f"- {key}: {value}")
        
        # Adım 4: Görselleştirmeleri Oluştur
        gorsel.enerji_dengesi_cubuk_grafigi_olustur(gunluk_toplamlar_dict)
        gorsel.enerji_dengesi_cizgi_grafigi_olustur(saatlik_veri_df)
        gorsel.batarya_doluluk_grafigi_olustur(saatlik_veri_df)
        gorsel.batarya_akim_grafigi_olustur(saatlik_veri_df)
        gorsel.saatlik_maliyet_grafigi_olustur(saatlik_veri_df)

        plt.show() # Tüm grafik pencerelerini göster