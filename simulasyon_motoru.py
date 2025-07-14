# simulasyon_motoru.py

import pandas as pd

def hesapla_dinamik_enerji_dengesi(
    dinamik_veriler_df,
    tren_basina_maks_tuketim_kWh,
    frenleme_geri_kazanim_orani,
    maks_istasyon_tuketimi_kWh,
    maks_gunes_paneli_uretimi_kWh,
    maks_ruzgar_turbini_uretimi_kWh,
    varsayilan_gunluk_toplam_sefer,
    # Batarya Parametreleri
    batarya_kapasitesi_kWh,
    sarj_verimliligi,
    desarj_verimliligi,
    baslangic_batarya_doluluk_orani,
    # Hata Buradaydı: Fonksiyon parametre isimlerini düzelttim
    batarya_bosaltma_esigi_oran_param, # Parametre adını değiştirdim
    batarya_doldurma_esigi_oran_param, # Parametre adını değiştirdim
    # Elektrik Fiyatları Parametresi
    elektrik_birim_fiyatlari_tl_kwh
):
    """
    Metro sistemi için saatlik enerji dengesi hesaplamalarını, batarya yönetimini
    ve maliyet/gelir hesaplamalarını yapar.

    Parametreler:
    - dinamik_veriler_df (pd.DataFrame): Saatlik profil oranlarını içeren DataFrame.
    - diğerleri: parametreler.py'den gelen maksimum günlük değerler.
    - batarya_kapasitesi_kWh (float): Bataryanın maksimum kapasitesi.
    - sarj_verimliligi (float): Batarya şarj verimliliği (0-1).
    - desarj_verimliligi (float): Batarya deşarj verimliliği (0-1).
    - baslangic_batarya_doluluk_orani (float): Simülasyon başlangıcında batarya doluluk oranı (0-1).
    - batarya_bosaltma_esigi_oran_param (float): Bataryanın boşaltılacağı minimum oran (0-1). # Güncellendi
    - batarya_doldurma_esigi_oran_param (float): Bataryanın doldurulacağı maksimum oran (0-1). # Güncellendi
    - elektrik_birim_fiyatlari_tl_kwh (list): Her saat için elektrik birim fiyatlarını içeren liste.

    Dönüş:
    - dict: Saatlik ve günlük toplam detaylı enerji hesaplamalarını içeren bir sözlük.
    """

    saatlik_sonuclar = []

    # Günlük toplam değerleri hesaplamak için başlangıç
    gunluk_toplam_tren_tuketimi = 0.0
    gunluk_geri_kazanilan_enerji = 0.0
    gunluk_net_tren_tuketimi = 0.0
    gunluk_istasyon_tuketimi = 0.0
    gunluk_gunes_paneli_uretimi = 0.0
    gunluk_ruzgar_turbini_uretimi = 0.0
    gunluk_toplam_sistem_net_tuketimi = 0.0
    gunluk_toplam_yenilenebilir_uretim = 0.0
    gunluk_batarya_sarj_miktari = 0.0
    gunluk_batarya_desarj_miktari = 0.0
    gunluk_sebeke_alim_miktari = 0.0
    gunluk_sebeke_verme_miktari = 0.0
    gunluk_toplam_maliyet = 0.0

    # Batarya başlangıç doluluk seviyesi
    mevcut_batarya_doluluk_kWh = batarya_kapasitesi_kWh * baslangic_batarya_doluluk_orani

    # Her bir saat dilimi için hesaplama yap
    for index, row in dinamik_veriler_df.iterrows():
        saat = int(row['Saat'])
        tren_sefer_yogunlugu_orani = row['TrenSeferYogunluguOrani']
        istasyon_tuketim_orani = row['IstasyonTuketimOrani']
        gunes_radyasyon_orani = row['GunesRadyasyonOrani']
        ruzgar_hizi_orani = row['RuzgarHiziOrani']

        # Saatlik enerji tüketimi ve üretimi
        saatlik_sefer_sayisi = (varsayilan_gunluk_toplam_sefer / 24.0) * tren_sefer_yogunlugu_orani
        saatlik_tren_tuketimi = saatlik_sefer_sayisi * tren_basina_maks_tuketim_kWh
        saatlik_geri_kazanilan_enerji = saatlik_tren_tuketimi * frenleme_geri_kazanim_orani
        saatlik_net_tren_tuketimi = saatlik_tren_tuketimi - saatlik_geri_kazanilan_enerji
        saatlik_istasyon_tuketimi = (maks_istasyon_tuketimi_kWh / 24.0) * istasyon_tuketim_orani

        saatlik_gunes_uretimi = (maks_gunes_paneli_uretimi_kWh / 24.0) * gunes_radyasyon_orani
        saatlik_ruzgar_turbini_uretimi = (maks_ruzgar_turbini_uretimi_kWh / 24.0) * ruzgar_hizi_orani

        saatlik_toplam_sistem_net_tuketimi = saatlik_net_tren_tuketimi + saatlik_istasyon_tuketimi
        saatlik_toplam_yenilenebilir_uretim = saatlik_gunes_uretimi + saatlik_ruzgar_turbini_uretimi

        # Sistemdeki anlık net enerji (batarya ve şebeke hariç)
        anlik_net_enerji_batt_sebeke_oncesi = saatlik_toplam_sistem_net_tuketimi - saatlik_toplam_yenilenebilir_uretim

        # Güncel elektrik birim fiyatı
        mevcut_elektrik_fiyati = elektrik_birim_fiyatlari_tl_kwh[saat]

        bataryadan_cekilen = 0.0
        bataryaya_giden = 0.0
        sebekeden_alim = 0.0
        sebekeye_verme = 0.0
        saatlik_maliyet = 0.0

        if anlik_net_enerji_batt_sebeke_oncesi > 0: # Sistem enerji açığı veriyor (tüketim > üretim)
            # Önce bataryadan çekmeye çalış (eğer boşaltma eşiğinin üzerindeyse)
            # Hata Buradaydı: Fonksiyon parametresi kullanıldı
            if mevcut_batarya_doluluk_kWh > (batarya_kapasitesi_kWh * batarya_bosaltma_esigi_oran_param):
                # Hata Buradaydı: Fonksiyon parametresi kullanıldı
                cekilebilecek_batarya = mevcut_batarya_doluluk_kWh - (batarya_kapasitesi_kWh * batarya_bosaltma_esigi_oran_param)
                bataryadan_cekilen_potansiyel = anlik_net_enerji_batt_sebeke_oncesi / desarj_verimliligi
                bataryadan_cekilen = min(bataryadan_cekilen_potansiyel, cekilebilecek_batarya)

                mevcut_batarya_doluluk_kWh -= bataryadan_cekilen
                anlik_net_enerji_batt_sebeke_oncesi -= (bataryadan_cekilen * desarj_verimliligi)

            if anlik_net_enerji_batt_sebeke_oncesi > 0: # Hala açık varsa şebekeden al
                sebekeden_alim = anlik_net_enerji_batt_sebeke_oncesi
                saatlik_maliyet = sebekeden_alim * mevcut_elektrik_fiyati

        elif anlik_net_enerji_batt_sebeke_oncesi < 0: # Sistem enerji fazlası veriyor (üretim > tüketim)
            # Batarya şarj edilebilecek kapasitedeyse (doldurma eşiğinin altındaysa)
            # Hata Buradaydı: Fonksiyon parametresi kullanıldı
            if mevcut_batarya_doluluk_kWh < (batarya_kapasitesi_kWh * batarya_doldurma_esigi_oran_param):
                # Hata Buradaydı: Fonksiyon parametresi kullanıldı
                sarj_edilebilecek_bosluk = (batarya_kapasitesi_kWh * batarya_doldurma_esigi_oran_param) - mevcut_batarya_doluluk_kWh
                bataryaya_giden_potansiyel = abs(anlik_net_enerji_batt_sebeke_oncesi) * sarj_verimliligi
                bataryaya_giden = min(bataryaya_giden_potansiyel, sarj_edilebilecek_bosluk)

                mevcut_batarya_doluluk_kWh += bataryaya_giden
                anlik_net_enerji_batt_sebeke_oncesi += (bataryaya_giden / sarj_verimliligi) # Bataryaya giden enerjinin fazladan düşülen kısmı (ters işlem)

            if anlik_net_enerji_batt_sebeke_oncesi < 0: # Hala fazlalık varsa şebekeye ver (gelir)
                sebekeye_verme = abs(anlik_net_enerji_batt_sebeke_oncesi)
                saatlik_maliyet = -sebekeye_verme * mevcut_elektrik_fiyati # Gelir olduğu için negatif maliyet

        # Batarya doluluk seviyesini min/max değerler arasında tut (eşiklerden dolayı garanti olsun diye)
        # Hata Buradaydı: Fonksiyon parametreleri kullanıldı
        mevcut_batarya_doluluk_kWh = max(batarya_kapasitesi_kWh * batarya_bosaltma_esigi_oran_param,
                                         min(batarya_kapasitesi_kWh * batarya_doldurma_esigi_oran_param, mevcut_batarya_doluluk_kWh))


        # Saatlik sonuçları listeye ekle
        saatlik_sonuclar.append({
            "Saat": saat,
            "Net Tren Tüketimi (kWh)": saatlik_net_tren_tuketimi,
            "İstasyon Tüketimi (kWh)": saatlik_istasyon_tuketimi,
            "Güneş Paneli Üretimi (kWh)": saatlik_gunes_uretimi,
            "Rüzgar Türbini Üretimi (kWh)": saatlik_ruzgar_turbini_uretimi,
            "Toplam Sistem Net Tüketimi (kWh)": saatlik_toplam_sistem_net_tuketimi,
            "Toplam Yenilenebilir Üretim (kWh)": saatlik_toplam_yenilenebilir_uretim,
            "Anlık Net Enerji (Batarya/Şebeke Öncesi) (kWh)": anlik_net_enerji_batt_sebeke_oncesi,
            "Bataryadan Çekilen (kWh)": bataryadan_cekilen,
            "Bataryaya Giden (kWh)": bataryaya_giden,
            "Şebekeden Alım (kWh)": sebekeden_alim,
            "Şebekeye Verme (kWh)": sebekeye_verme,
            "Batarya Doluluk (kWh)": mevcut_batarya_doluluk_kWh,
            "Batarya Doluluk Oranı (%)": (mevcut_batarya_doluluk_kWh / batarya_kapasitesi_kWh) * 100,
            "Saatlik Maliyet (TL)": saatlik_maliyet
        })

        # Günlük toplamları güncelle
        gunluk_toplam_tren_tuketimi += saatlik_tren_tuketimi
        gunluk_geri_kazanilan_enerji += saatlik_geri_kazanilan_enerji
        gunluk_net_tren_tuketimi += saatlik_net_tren_tuketimi
        gunluk_istasyon_tuketimi += saatlik_istasyon_tuketimi
        gunluk_gunes_paneli_uretimi += saatlik_gunes_uretimi
        gunluk_ruzgar_turbini_uretimi += saatlik_ruzgar_turbini_uretimi
        gunluk_toplam_sistem_net_tuketimi += saatlik_toplam_sistem_net_tuketimi
        gunluk_toplam_yenilenebilir_uretim += saatlik_toplam_yenilenebilir_uretim
        gunluk_batarya_sarj_miktari += bataryaya_giden
        gunluk_batarya_desarj_miktari += bataryadan_cekilen
        gunluk_sebeke_alim_miktari += sebekeden_alim
        gunluk_sebeke_verme_miktari += sebekeye_verme
        gunluk_toplam_maliyet += saatlik_maliyet


    return {
        "saatlik_veri": pd.DataFrame(saatlik_sonuclar),
        "gunluk_toplamlar": {
            "Toplam Tren Tüketimi (kWh)": gunluk_toplam_tren_tuketimi,
            "Geri Kazanılan Enerji (kWh)": gunluk_geri_kazanilan_enerji,
            "Net Tren Tüketimi (kWh)": gunluk_net_tren_tuketimi,
            "İstasyon Tüketimi (kWh)": gunluk_istasyon_tuketimi,
            "Güneş Paneli Üretimi (kWh)": gunluk_gunes_paneli_uretimi,
            "Rüzgar Türbini Üretimi (kWh)": gunluk_ruzgar_turbini_uretimi,
            "Toplam Sistem Net Tüketimi (kWh)": gunluk_toplam_sistem_net_tuketimi,
            "Toplam Yenilenebilir Üretim (kWh)": gunluk_toplam_yenilenebilir_uretim,
            "Günlük Batarya Şarj Miktarı (kWh)": gunluk_batarya_sarj_miktari,
            "Günlük Batarya Deşarj Miktarı (kWh)": gunluk_batarya_desarj_miktari,
            "Günlük Şebekeden Alım (kWh)": gunluk_sebeke_alim_miktari,
            "Günlük Şebekeye Verme (kWh)": gunluk_sebeke_verme_miktari,
            "Net Enerji Dengesi (Şebeke Etkisi ile) (kWh)": (gunluk_sebeke_verme_miktari - gunluk_sebeke_alim_miktari),
            "Toplam Enerji Maliyeti (TL)": gunluk_toplam_maliyet
        }
    }