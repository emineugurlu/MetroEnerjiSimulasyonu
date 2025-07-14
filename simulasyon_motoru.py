# simulasyon_motoru.py

import pandas as pd

def hesapla_dinamik_enerji_dengesi(
    dinamik_veriler_df,
    tren_basina_maks_tuketim_kWh,
    frenleme_geri_kazanim_orani,
    maks_istasyon_tuketimi_kWh,
    maks_gunes_paneli_uretimi_kWh,
    maks_ruzgar_turbini_uretimi_kWh,
    varsayilan_gunluk_toplam_sefer
):
    """
    Metro sistemi için saatlik enerji dengesi hesaplamalarını yapar.

    Parametreler:
    - dinamik_veriler_df (pd.DataFrame): Saatlik profil oranlarını içeren DataFrame.
    - diğerleri: parametreler.py'den gelen maksimum günlük değerler.

    Dönüş:
    - dict: Saatlik ve günlük toplam detaylı enerji hesaplamalarını içeren bir sözlük.
    """

    saatlik_sonuclar = []

    # Günlük toplam değerleri hesaplamak için başlangıç
    gunluk_toplam_tren_tuketimi = 0.0
    gunluk_geri_kazanilan_enerji = 0.0 # Hata buradaydı, düzeltildi
    gunluk_net_tren_tuketimi = 0.0
    gunluk_istasyon_tuketimi = 0.0
    gunluk_gunes_paneli_uretimi = 0.0
    gunluk_ruzgar_turbini_uretimi = 0.0
    gunluk_toplam_sistem_net_tuketimi = 0.0
    gunluk_toplam_yenilenebilir_uretim = 0.0
    gunluk_net_enerji_dengesi = 0.0

    # Her bir saat dilimi için hesaplama yap
    for index, row in dinamik_veriler_df.iterrows():
        saat = row['Saat']
        tren_sefer_yogunlugu_orani = row['TrenSeferYogunluguOrani']
        istasyon_tuketim_orani = row['IstasyonTuketimOrani']
        gunes_radyasyon_orani = row['GunesRadyasyonOrani']
        ruzgar_hizi_orani = row['RuzgarHiziOrani']

        # Saatlik değerleri hesapla
        # Varsayılan günlük toplam sefer sayısını 24'e bölerek saatlik ortalama potansiyeli alalım,
        # sonra o saatteki yoğunluk oranıyla çarpalım.
        saatlik_sefer_sayisi = (varsayilan_gunluk_toplam_sefer / 24.0) * tren_sefer_yogunlugu_orani

        saatlik_tren_tuketimi = saatlik_sefer_sayisi * tren_basina_maks_tuketim_kWh
        saatlik_geri_kazanilan_enerji = saatlik_tren_tuketimi * frenleme_geri_kazanim_orani
        saatlik_net_tren_tuketimi = saatlik_tren_tuketimi - saatlik_geri_kazanilan_enerji
        saatlik_istasyon_tuketimi = (maks_istasyon_tuketimi_kWh / 24.0) * istasyon_tuketim_orani
        saatlik_gunes_uretimi = (maks_gunes_paneli_uretimi_kWh / 24.0) * gunes_radyasyon_orani
        saatlik_ruzgar_uretimi = (maks_ruzgar_turbini_uretimi_kWh / 24.0) * ruzgar_hizi_orani

        saatlik_toplam_sistem_net_tuketimi = saatlik_net_tren_tuketimi + saatlik_istasyon_tuketimi
        saatlik_toplam_yenilenebilir_uretim = saatlik_gunes_uretimi + saatlik_ruzgar_uretimi
        saatlik_net_enerji_dengesi = saatlik_toplam_sistem_net_tuketimi - saatlik_toplam_yenilenebilir_uretim

        saatlik_sonuclar.append({
            "Saat": saat,
            "Net Tren Tüketimi (kWh)": saatlik_net_tren_tuketimi,
            "İstasyon Tüketimi (kWh)": saatlik_istasyon_tuketimi,
            "Güneş Paneli Üretimi (kWh)": saatlik_gunes_uretimi,
            "Rüzgar Türbini Üretimi (kWh)": saatlik_ruzgar_uretimi,
            "Toplam Sistem Net Tüketimi (kWh)": saatlik_toplam_sistem_net_tuketimi,
            "Toplam Yenilenebilir Üretim (kWh)": saatlik_toplam_yenilenebilir_uretim,
            "Net Enerji Dengesi (kWh)": saatlik_net_enerji_dengesi
        })

        # Günlük toplamları güncelle
        gunluk_toplam_tren_tuketimi += saatlik_tren_tuketimi
        gunluk_geri_kazanilan_enerji += saatlik_geri_kazanilan_enerji # Hata buradaydı, düzeltildi
        gunluk_net_tren_tuketimi += saatlik_net_tren_tuketimi
        gunluk_istasyon_tuketimi += saatlik_istasyon_tuketimi
        gunluk_gunes_paneli_uretimi += saatlik_gunes_uretimi
        gunluk_ruzgar_turbini_uretimi += saatlik_ruzgar_uretimi
        gunluk_toplam_sistem_net_tuketimi += saatlik_toplam_sistem_net_tuketimi
        gunluk_toplam_yenilenebilir_uretim += saatlik_toplam_yenilenebilir_uretim
        gunluk_net_enerji_dengesi += saatlik_net_enerji_dengesi

    return {
        "saatlik_veri": pd.DataFrame(saatlik_sonuclar),
        "gunluk_toplamlar": {
            "Toplam Tren Tüketimi (kWh)": gunluk_toplam_tren_tuketimi,
            "Geri Kazanılan Enerji (kWh)": gunluk_geri_kazanilan_enerji, # Hata buradaydı, düzeltildi
            "Net Tren Tüketimi (kWh)": gunluk_net_tren_tuketimi,
            "İstasyon Tüketimi (kWh)": gunluk_istasyon_tuketimi,
            "Güneş Paneli Üretimi (kWh)": gunluk_gunes_paneli_uretimi,
            "Rüzgar Türbini Üretimi (kWh)": gunluk_ruzgar_turbini_uretimi,
            "Toplam Sistem Net Tüketimi (kWh)": gunluk_toplam_sistem_net_tuketimi,
            "Toplam Yenilenebilir Üretim (kWh)": gunluk_toplam_yenilenebilir_uretim,
            "Net Enerji Dengesi (kWh)": gunluk_net_enerji_dengesi
        }
    }