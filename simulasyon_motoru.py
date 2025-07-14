# simulasyon_motoru.py

# simulasyon_motoru.py
import pandas as pd
from pulp  import LpProblem, LpMinimize, LpVariable, lpSum, PULP_CBC_CMD, LpStatus

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
    batarya_bosaltma_esigi_oran,
    batarya_doldurma_esigi_oran,
    # Elektrik Fiyatları Parametresi
    elektrik_birim_fiyatlari_tl_kwh
):
    """
    Metro sistemi için saatlik enerji dengesi hesaplamalarını, batarya yönetimini
    ve maliyet/gelir hesaplamalarını matematiksel optimizasyon ile yapar.

    Parametreler:
    - dinamik_veriler_df (pd.DataFrame): Saatlik profil oranlarını içeren DataFrame.
    - diğerleri: parametreler.py'den gelen maksimum günlük değerler.
    - batarya_kapasitesi_kWh (float): Bataryanın maksimum kapasitesi.
    - sarj_verimliligi (float): Batarya şarj verimliliği (0-1).
    - desarj_verimliligi (float): Batarya deşarj verimliliği (0-1).
    - baslangic_batarya_doluluk_orani (float): Simülasyon başlangıcında batarya doluluk oranı (0-1).
    - batarya_bosaltma_esigi_oran (float): Bataryanın boşaltılacağı minimum oran (0-1).
    - batarya_doldurma_esigi_oran (float): Bataryanın doldurulacağı maksimum oran (0-1).
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
    # Optimizasyon modeli günlük bazda çalıştığı için, batarya seviyesi model içinde yönetilecek.
    # İlk saat için başlangıç değeri kullanılır.

    # Optimizasyon Modelini Oluştur
    prob = LpProblem("Metro_Enerji_Yonetimi", LpMinimize)

    # Değişkenleri Tanımla
    T = range(24) # Saat dilimleri (0'dan 23'e kadar)

    # Saatlik Şebekeden Alım (Net Alım)
    sebekeden_alim = LpVariable.dicts("sebekeden_alim", T, lowBound=0)
    # Saatlik Şebekeye Verme (Net Verme)
    sebekeye_verme = LpVariable.dicts("sebekeye_verme", T, lowBound=0)
    # Saatlik Batarya Şarj (Net Şarj)
    batarya_sarj = LpVariable.dicts("batarya_sarj", T, lowBound=0)
    # Saatlik Batarya Deşarj (Net Deşarj)
    batarya_desarj = LpVariable.dicts("batarya_desarj", T, lowBound=0)
    # Saatlik Batarya Doluluk Seviyesi
    batarya_doluluk = LpVariable.dicts("batarya_doluluk", T, lowBound=batarya_kapasitesi_kWh * batarya_bosaltma_esigi_oran, upBound=batarya_kapasitesi_kWh * batarya_doldurma_esigi_oran)

    # Amaç Fonksiyonu: Toplam Maliyeti Minimize Et
    # Şebekeden alım maliyeti - Şebekeye verme geliri
    prob += lpSum([sebekeden_alim[t] * elektrik_birim_fiyatlari_tl_kwh[t] - sebekeye_verme[t] * elektrik_birim_fiyatlari_tl_kwh[t] for t in T]), "Toplam_Maliyet"


    # Kısıtları Ekle
    for t in T:
        saat = int(dinamik_veriler_df.iloc[t]['Saat'])
        tren_sefer_yogunlugu_orani = dinamik_veriler_df.iloc[t]['TrenSeferYogunluguOrani']
        istasyon_tuketim_orani = dinamik_veriler_df.iloc[t]['IstasyonTuketimOrani']
        gunes_radyasyon_orani = dinamik_veriler_df.iloc[t]['GunesRadyasyonOrani']
        ruzgar_hizi_orani = dinamik_veriler_df.iloc[t]['RuzgarHiziOrani']

        # Saatlik enerji tüketimi ve üretimi hesaplamaları (Tahminler)
        saatlik_sefer_sayisi = (varsayilan_gunluk_toplam_sefer / 24.0) * tren_sefer_yogunlugu_orani
        saatlik_tren_tuketimi = saatlik_sefer_sayisi * tren_basina_maks_tuketim_kWh
        saatlik_geri_kazanilan_enerji = saatlik_tren_tuketimi * frenleme_geri_kazanim_orani
        saatlik_net_tren_tuketimi_gercek = saatlik_tren_tuketimi - saatlik_geri_kazanilan_enerji
        saatlik_istasyon_tuketimi_gercek = (maks_istasyon_tuketimi_kWh / 24.0) * istasyon_tuketim_orani
        saatlik_gunes_uretimi_gercek = (maks_gunes_paneli_uretimi_kWh / 24.0) * gunes_radyasyon_orani
        saatlik_ruzgar_turbini_uretimi_gercek = (maks_ruzgar_turbini_uretimi_kWh / 24.0) * ruzgar_hizi_orani

        # Toplam Sistem Net Tüketimi (Pozitif = Tüketim, Negatif = Fazlalık)
        sistem_net_ihtiyaci = (saatlik_net_tren_tuketimi_gercek + saatlik_istasyon_tuketimi_gercek) - \
                              (saatlik_gunes_uretimi_gercek + saatlik_ruzgar_turbini_uretimi_gercek)

        # Enerji Dengesi Kısıtı: Üretim + Şebekeden Alım + Bataryadan Deşarj = Tüketim + Şebekeye Verme + Batarya Şarj
        prob += (sebekeden_alim[t] + (batarya_desarj[t] * desarj_verimliligi) + saatlik_gunes_uretimi_gercek + saatlik_ruzgar_turbini_uretimi_gercek) == \
                (sistem_net_ihtiyaci + sebekeye_verme[t] + (batarya_sarj[t] / sarj_verimliligi)), f"Enerji_Dengesi_Saat_{t}"

        # Batarya Doluluk Kısıtları
        if t == 0:
            # Başlangıç batarya doluluğu
            prob += batarya_doluluk[t] == batarya_kapasitesi_kWh * baslangic_batarya_doluluk_orani + (batarya_sarj[t] * sarj_verimliligi) - (batarya_desarj[t] / desarj_verimliligi), f"Batarya_Baslangic_Doluluk_{t}"
        else:
            # Diğer saatler için batarya doluluğu (önceki saate bağlı)
            prob += batarya_doluluk[t] == batarya_doluluk[t-1] + (batarya_sarj[t] * sarj_verimliligi) - (batarya_desarj[t] / desarj_verimliligi), f"Batarya_Doluluk_Guncelleme_{t}"

        # Batarya Şarj/Deşarj Karşılıklı Dışlama Kısıtı (aynı anda hem şarj hem de deşarj olamaz)
        # Bu, PuLP ile doğrudan modellemekte biraz karmaşık olabilir, ancak genellikle batarya modellemesinde
        # şarj ve deşarj değişkenleri ayrı ayrı tanımlanıp birbirini dışlayacak şekilde kullanılır.
        # Basitlik adına, burada direkt enerji dengesi içinde ele alıyoruz ve negatif olmalarını engelliyoruz (lowBound=0).
        # Yani, batarya_sarj pozitifse batarya_desarj 0, batarya_desarj pozitifse batarya_sarj 0 olur.

        # Batarya Kapasite Kısıtları (değişken tanımında zaten upper/lower bound olarak belirlendi)
        # prob += batarya_doluluk[t] >= batarya_kapasitesi_kWh * batarya_bosaltma_esigi_oran
        # prob += batarya_doluluk[t] <= batarya_kapasitesi_kWh * batarya_doldurma_esigi_oran

        # Şebeke Alım/Verme Karşılıklı Dışlama Kısıtı
        # Şebekeden hem alıp hem veremeyiz, bu da varsayılan olarak lowBound=0 ile sağlanır.


    # Modeli Çöz
    prob.solve(PULP_CBC_CMD(msg=0)) # msg=0 ile çözümleyici çıktısını gizle

    # Çözüm durumunu kontrol et
    if LpStatus[prob.status] != "Optimal":
        print(f"Uyarı: Optimizasyon çözümü optimal değil. Durum: {LpStatus[prob.status]}")

    # Sonuçları Saatlik Veri Çerçevesine Kaydet
    for t in T:
        saat = int(dinamik_veriler_df.iloc[t]['Saat'])
        tren_sefer_yogunlugu_orani = dinamik_veriler_df.iloc[t]['TrenSeferYogunluguOrani']
        istasyon_tuketim_orani = dinamik_veriler_df.iloc[t]['IstasyonTuketimOrani']
        gunes_radyasyon_orani = dinamik_veriler_df.iloc[t]['GunesRadyasyonOrani']
        ruzgar_hizi_orani = dinamik_veriler_df.iloc[t]['RuzgarHiziOrani']

        saatlik_sefer_sayisi = (varsayilan_gunluk_toplam_sefer / 24.0) * tren_sefer_yogunlugu_orani
        saatlik_tren_tuketimi_gercek = saatlik_sefer_sayisi * tren_basina_maks_tuketim_kWh
        saatlik_geri_kazanilan_enerji_gercek = saatlik_tren_tuketimi_gercek * frenleme_geri_kazanim_orani
        saatlik_net_tren_tuketimi_gercek_hesap = saatlik_tren_tuketimi_gercek - saatlik_geri_kazanilan_enerji_gercek
        saatlik_istasyon_tuketimi_gercek_hesap = (maks_istasyon_tuketimi_kWh / 24.0) * istasyon_tuketim_orani

        saatlik_gunes_uretimi_gercek_hesap = (maks_gunes_paneli_uretimi_kWh / 24.0) * gunes_radyasyon_orani
        saatlik_ruzgar_turbini_uretimi_gercek_hesap = (maks_ruzgar_turbini_uretimi_kWh / 24.0) * ruzgar_hizi_orani

        saatlik_toplam_sistem_net_tuketimi_hesap = saatlik_net_tren_tuketimi_gercek_hesap + saatlik_istasyon_tuketimi_gercek_hesap
        saatlik_toplam_yenilenebilir_uretim_hesap = saatlik_gunes_uretimi_gercek_hesap + saatlik_ruzgar_turbini_uretimi_gercek_hesap

        # Anlık Net Enerji (Batarya/Şebeke Öncesi) - Bu değer artık optimizasyon çıktısına göre dengeye giriyor
        anlik_net_enerji_batt_sebeke_oncesi_hesap = saatlik_toplam_sistem_net_tuketimi_hesap - saatlik_toplam_yenilenebilir_uretim_hesap

        # Optimizasyon sonuçlarını al
        opt_sebekeden_alim = sebekeden_alim[t].varValue if sebekeden_alim[t].varValue is not None else 0.0
        opt_sebekeye_verme = sebekeye_verme[t].varValue if sebekeye_verme[t].varValue is not None else 0.0
        opt_batarya_sarj = batarya_sarj[t].varValue if batarya_sarj[t].varValue is not None else 0.0
        opt_batarya_desarj = batarya_desarj[t].varValue if batarya_desarj[t].varValue is not None else 0.0
        opt_batarya_doluluk = batarya_doluluk[t].varValue if batarya_doluluk[t].varValue is not None else 0.0

        saatlik_maliyet_hesap = (opt_sebekeden_alim * elektrik_birim_fiyatlari_tl_kwh[saat]) - (opt_sebekeye_verme * elektrik_birim_fiyatlari_tl_kwh[saat])

        saatlik_sonuclar.append({
            "Saat": saat,
            "Net Tren Tüketimi (kWh)": saatlik_net_tren_tuketimi_gercek_hesap,
            "İstasyon Tüketimi (kWh)": saatlik_istasyon_tuketimi_gercek_hesap,
            "Güneş Paneli Üretimi (kWh)": saatlik_gunes_uretimi_gercek_hesap,
            "Rüzgar Türbini Üretimi (kWh)": saatlik_ruzgar_turbini_uretimi_gercek_hesap,
            "Toplam Sistem Net Tüketimi (kWh)": saatlik_toplam_sistem_net_tuketimi_hesap,
            "Toplam Yenilenebilir Üretim (kWh)": saatlik_toplam_yenilenebilir_uretim_hesap,
            "Anlık Net Enerji (Batarya/Şebeke Öncesi) (kWh)": anlik_net_enerji_batt_sebeke_oncesi_hesap,
            "Bataryadan Çekilen (kWh)": opt_batarya_desarj,
            "Bataryaya Giden (kWh)": opt_batarya_sarj,
            "Şebekeden Alım (kWh)": opt_sebekeden_alim,
            "Şebekeye Verme (kWh)": opt_sebekeye_verme,
            "Batarya Doluluk (kWh)": opt_batarya_doluluk,
            "Batarya Doluluk Oranı (%)": (opt_batarya_doluluk / batarya_kapasitesi_kWh) * 100 if batarya_kapasitesi_kWh > 0 else 0,
            "Saatlik Maliyet (TL)": saatlik_maliyet_hesap
        })

        # Günlük toplamları güncelle
        gunluk_toplam_tren_tuketimi += saatlik_tren_tuketimi_gercek
        gunluk_geri_kazanilan_enerji += saatlik_geri_kazanilan_enerji_gercek
        gunluk_net_tren_tuketimi += saatlik_net_tren_tuketimi_gercek_hesap
        gunluk_istasyon_tuketimi += saatlik_istasyon_tuketimi_gercek_hesap
        gunluk_gunes_paneli_uretimi += saatlik_gunes_uretimi_gercek_hesap
        gunluk_ruzgar_turbini_uretimi += saatlik_ruzgar_turbini_uretimi_gercek_hesap
        gunluk_toplam_sistem_net_tuketimi += saatlik_toplam_sistem_net_tuketimi_hesap
        gunluk_toplam_yenilenebilir_uretim += saatlik_toplam_yenilenebilir_uretim_hesap
        gunluk_batarya_sarj_miktari += opt_batarya_sarj
        gunluk_batarya_desarj_miktari += opt_batarya_desarj
        gunluk_sebeke_alim_miktari += opt_sebekeden_alim
        gunluk_sebeke_verme_miktari += opt_sebekeye_verme
        gunluk_toplam_maliyet += saatlik_maliyet_hesap


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