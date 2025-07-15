# simulasyon_motoru.py dosyası

import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, PULP_CBC_CMD, LpStatus
import matplotlib.pyplot as plt # Sadece hata ayıklama veya geçici görselleştirme için kalabilir
import numpy as np

# --- 1. Sabit Tanımlamalar ---
# Bu sabitler, simülasyon motorunun doğrudan kullandığı parametrelerdir.
# Eğer bu değerler 'parametreler.py' dosyasından geliyorsa, o zaman buradaki tanımları kaldırıp
# 'hesapla_dinamik_enerji_dengesi' fonksiyonuna parametre olarak geçirmelisiniz.
# Ancak şimdilik main.py'den gelen kafa karışıklığını gidermek için burada tutuyorum
# ve p. dosyasındaki değerleri buradaki fonksiyonların parametresi olarak almayacağız.
# Bunun yerine, main.py'den gelen değerleri fonksiyon içinde kullanacağız.

# Dinamik veri yükleme fonksiyonu (main.py'de zaten çağrılıyor)
def dinamik_veri_yukle(dosya_yolu):
    try:
        df = pd.read_excel(dosya_yolu)
        # print(f"--- '{dosya_yolu}' dosyasından dinamik veriler yüklendi ---") # Main.py'de var
        return df
    except FileNotFoundError:
        print(f"Hata: '{dosya_yolu}' bulunamadı. Lütfen dosya yolunu kontrol edin.")
        return None

# --- Akıllı EMS ile Simülasyon Fonksiyonu ---
# Bu fonksiyon şimdi dışarıdan tüm gerekli parametreleri alacak.
# Bu sayede simulasyon_motoru.py bağımsız olacak ve parametreler.py'ye bağımlı olmayacak.
def hesapla_dinamik_enerji_dengesi(
    dinamik_veriler_df,
    tren_basina_maks_tuketim_kwh,
    frenleme_geri_kazanim_orani,
    maks_istasyon_tuketimi_kwh,
    maks_gunes_paneli_uretimi_kwh,
    maks_ruzgar_turbini_uretimi_kwh,
    batarya_kapasitesi_kwh,
    sarj_verimliligi,
    desarj_verimliligi,
    baslangic_batarya_doluluk_orani,
    batarya_bosaltma_esigi_oran,
    batarya_doldurma_esigi_oran,
    elektrik_birim_fiyatlari_tl_kwh, # Şebekeden alım fiyatı
    elektrik_birim_fiyatlari_tl_kwh_satis # Şebekeye satış fiyatı
):
    if dinamik_veriler_df is None:
        return None

    # Toplam simülasyon süresi (saat cinsinden)
    toplam_saat = len(dinamik_veriler_df)
    simulasyon_suresi_gun = toplam_saat / 24

    print(f"\n--- Dinamik ({toplam_saat} Saatlik / {simulasyon_suresi_gun:.1f} Günlük) Simülasyon Akıllı EMS ile Çalıştırılıyor ---")

    # Sabitler (Fonksiyon parametrelerinden türetilenler veya içsel sabitler)
    # Maks ve min batarya doluluk seviyeleri (kWh cinsinden)
    maks_sarj_deposu_kwh = batarya_kapasitesi_kwh * batarya_doldurma_esigi_oran
    min_sarj_deposu_kwh = batarya_kapasitesi_kwh * batarya_bosaltma_esigi_oran
    
    # Batarya şarj/deşarj maksimum gücü (örneğin kapasitenin %20'si gibi, yoksa parametre olarak alınmalı)
    # Burada varsayılan olarak kapasitenin 1/5'i olarak belirlenmiştir.
    maks_sarj_gucu = batarya_kapasitesi_kwh / 5 
    maks_desarj_gucu = batarya_kapasitesi_kwh / 5

    # Karbon Emisyon Faktörü (bu değer p. dosyasından gelmeli, gelmiyorsa burada sabit kalsın)
    KARBON_EMISYON_FAKTORU_SEBEKE = 0.45 # kg CO2e/kWh (Örnek değer)

    # Sonuçları depolamak için listeler
    saatlik_tren_tuketimi_list = []
    saatlik_istasyon_tuketimi_list = []
    saatlik_gunes_uretimi_list = []
    saatlik_ruzgar_uretimi_list = []
    saatlik_net_tuketim_list = [] # Bu listede tüketim - üretim olacak
    saatlik_batarya_doluluk_list = [batarya_kapasitesi_kwh * baslangic_batarya_doluluk_orani] # Başlangıç doluluğu (kWh)
    saatlik_batarya_sarj_akisi_list = []
    saatlik_batarya_desarj_akisi_list = []
    saatlik_sebekeden_alim_list = []
    saatlik_sebekeye_verme_list = []
    saatlik_maliyet_list = [] # Her saatteki net enerji maliyeti/geliri

    # Simülasyon Döngüsü
  # Simülasyon Döngüsü
    for t in range(toplam_saat):
        # Dinamik Verileri Çek
        tren_sefer_yogunlugu = dinamik_veriler_df.loc[t, 'TrenSeferYogunluguOrani'] # <-- BURASI GÜNCELLENDİ!
        istasyon_tuketim_orani = dinamik_veriler_df.loc[t, 'IstasyonTuketimOrani']
        gunes_radyasyon_orani = dinamik_veriler_df.loc[t, 'GunesRadyasyonOrani'] # Excel sütun adını tekrar kontrol edin!
        ruzgar_hizi_orani = dinamik_veriler_df.loc[t, 'RuzgarHiziOrani']


        # Hesaplamalar
        # Not: Tren ve İstasyon tüketimleri doğrudan p. dosyasından gelen MAKS değerler ve oranlarla hesaplanır
        current_tren_tuketimi = tren_basina_maks_tuketim_kwh * tren_sefer_yogunlugu
        # Frenleme geri kazanımı burada düşülmeli
        current_net_tren_tuketimi = current_tren_tuketimi * (1 - frenleme_geri_kazanim_orani)
        
        current_istasyon_tuketimi = maks_istasyon_tuketimi_kwh * istasyon_tuketim_orani
        current_gunes_uretimi = maks_gunes_paneli_uretimi_kwh * gunes_radyasyon_orani
        current_ruzgar_uretimi = maks_ruzgar_turbini_uretimi_kwh * ruzgar_hizi_orani

        saatlik_tren_tuketimi_list.append(current_tren_tuketimi)
        saatlik_istasyon_tuketimi_list.append(current_istasyon_tuketimi)
        saatlik_gunes_uretimi_list.append(current_gunes_uretimi)
        saatlik_ruzgar_uretimi_list.append(current_ruzgar_uretimi)
        
        # Anlık net enerji ihtiyacı (pozitif ise ihtiyaç, negatif ise fazlalık)
        anlik_net_ihtiyac = (current_net_tren_tuketimi + current_istasyon_tuketimi) - \
                             (current_gunes_uretimi + current_ruzgar_uretimi)
        saatlik_net_tuketim_list.append(anlik_net_ihtiyac)


        # Optimizasyon Modeli (Pulp ile)
        prob = LpProblem("EnerjiYonetimi", LpMinimize)

        # Değişkenler
        batarya_sarj_kwh = LpVariable("BataryaSarjKWH", 0, maks_sarj_gucu)
        batarya_desarj_kwh = LpVariable("BataryaDesarjKWH", 0, maks_desarj_gucu)
        sebekeden_alim_kwh = LpVariable("SebekedenAlimKWH", 0)
        sebekeye_verme_kwh = LpVariable("SebekeyeVermeKWH", 0)

        # Amaç Fonksiyonu: Maliyeti Minimize Et (Alış maliyeti - Satış geliri)
        prob += (sebekeden_alim_kwh * elektrik_birim_fiyatlari_tl_kwh) - \
                (sebekeye_verme_kwh * elektrik_birim_fiyatlari_tl_kwh_satis)

        # Kısıtlar
        onceki_batarya_doluluk = saatlik_batarya_doluluk_list[-1]

        # Enerji Denge Kısıtı:
        # Net İhtiyaç = Şebekeden Alım - Şebekeye Verme + Batarya Şarj - Batarya Deşarj
        prob += anlik_net_ihtiyac == (sebekeden_alim_kwh - sebekeye_verme_kwh) + \
                                      (batarya_sarj_kwh / sarj_verimliligi) - \
                                      (batarya_desarj_kwh * desarj_verimliligi)

        # Batarya Doluluk Kısıtı (bir sonraki saatin başlangıç doluluğu)
        prob += (onceki_batarya_doluluk + batarya_sarj_kwh - batarya_desarj_kwh) >= min_sarj_deposu_kwh
        prob += (onceki_batarya_doluluk + batarya_sarj_kwh - batarya_desarj_kwh) <= maks_sarj_deposu_kwh
        
        # Batarya aynı anda hem şarj hem de deşarj olamaz (Pulp bunu optimize eder ancak bazen açık kısıt iyi olur)
        # lpSum ile batarya_sarj_kwh ve batarya_desarj_kwh'nın toplamı, 
        # sadece birinin pozitif olabileceği bir şekilde yönetilebilir.
        # Basitlik için Pulp'un optimal çözümü bulmasına izin veriyoruz.

        # Optimizasyonu Çalıştır
        prob.solve(PULP_CBC_CMD(msg=0)) # msg=0 ile Pulp'ın detaylı çıktılarını gizle

        # Sonuçları al
        current_batarya_sarj = batarya_sarj_kwh.varValue
        current_batarya_desarj = batarya_desarj_kwh.varValue
        current_sebekeden_alim = sebekeden_alim_kwh.varValue
        current_sebekeye_verme = sebekeye_verme_kwh.varValue
        
        # Null değer kontrolü (Pulp çözemezse None dönebilir)
        if current_batarya_sarj is None: current_batarya_sarj = 0.0
        if current_batarya_desarj is None: current_batarya_desarj = 0.0
        if current_sebekeden_alim is None: current_sebekeden_alim = 0.0
        if current_sebekeye_verme is None: current_sebekeye_verme = 0.0

        saatlik_batarya_sarj_akisi_list.append(current_batarya_sarj)
        saatlik_batarya_desarj_akisi_list.append(-current_batarya_desarj) # Deşarjı negatif olarak kaydet

        # Batarya doluluğunu güncelle ve listeye ekle
        yeni_batarya_doluluk = onceki_batarya_doluluk + current_batarya_sarj - current_batarya_desarj
        
        # Sınırları aşma kontrolü (kayan nokta hatalarına karşı)
        yeni_batarya_doluluk = max(min_sarj_deposu_kwh, min(maks_sarj_deposu_kwh, yeni_batarya_doluluk))
        saatlik_batarya_doluluk_list.append(yeni_batarya_doluluk)

        saatlik_sebekeden_alim_list.append(current_sebekeden_alim)
        saatlik_sebekeye_verme_list.append(current_sebekeye_verme)
        
        # Saatlik maliyet hesaplaması
        current_maliyet = (current_sebekeden_alim * elektrik_birim_fiyatlari_tl_kwh) - \
                          (current_sebekeye_verme * elektrik_birim_fiyatlari_tl_kwh_satis)
        saatlik_maliyet_list.append(current_maliyet)

    # Batarya doluluk listesindeki son elemanı çıkar (fazla eklenen)
    saatlik_batarya_doluluk_list.pop()


    # --- Toplam Enerji Hesaplamaları ---
    print(f"\n--- Dinamik Simülasyon - Toplam Enerji Hesaplamaları (Akıllı EMS Entegreli) - {simulasyon_suresi_gun:.1f} Günlük ---")

    toplam_tren_tuketimi = sum(saatlik_tren_tuketimi_list)
    geri_kazanilan_enerji = toplam_tren_tuketimi * frenleme_geri_kazanim_orani
    net_tren_tuketimi = toplam_tren_tuketimi - geri_kazanilan_enerji
    
    toplam_istasyon_tuketimi = sum(saatlik_istasyon_tuketimi_list)
    toplam_gunes_uretimi = sum(saatlik_gunes_uretimi_list)
    toplam_ruzgar_uretimi = sum(saatlik_ruzgar_uretimi_list)
    
    toplam_batarya_sarj = sum(saatlik_batarya_sarj_akisi_list) # Zaten pozitif değerler
    toplam_batarya_desarj = sum([abs(val) for val in saatlik_batarya_desarj_akisi_list]) # Negatifleri pozitif yap

    toplam_sebekeden_alim = sum(saatlik_sebekeden_alim_list)
    toplam_sebekeye_verme = sum(saatlik_sebekeye_verme_list)
    
    # Net Enerji Dengesi (Şebeke Etkisi ile): Pozitif = Şebekeden Net Alım, Negatif = Şebekeye Net Verim
    net_enerji_dengesi_sebeke = toplam_sebekeden_alim - toplam_sebekeye_verme
    
    toplam_enerji_maliyeti = sum(saatlik_maliyet_list)
    
    # Karbon Ayak İzi Hesaplaması (Şebekeden Alım kaynaklı)
    toplam_karbon_ayak_izi = toplam_sebekeden_alim * KARBON_EMISYON_FAKTORU_SEBEKE

    # Sonuçları dictionary olarak düzenle ve döndür
    sonuclar = {
        'saatlik_veri': { # Saatlik detaylı veriler
            'Saat': list(range(toplam_saat)),
            'Tren Tuketimi': saatlik_tren_tuketimi_list,
            'Istasyon Tuketimi': saatlik_istasyon_tuketimi_list,
            'Gunes Uretimi': saatlik_gunes_uretimi_list,
            'Ruzgar Uretimi': saatlik_ruzgar_uretimi_list,
            'Net Tuketim': saatlik_net_tuketim_list,
            'Batarya Doluluk': saatlik_batarya_doluluk_list,
            'Batarya Sarj Akisi': saatlik_batarya_sarj_akisi_list,
            'Batarya Desaj Akisi': saatlik_batarya_desarj_akisi_list,
            'Şebekeden Alım': saatlik_sebekeden_alim_list,
            'Şebekeye Verme': saatlik_sebekeye_verme_list,
            'Saatlik Maliyet': saatlik_maliyet_list
        },
        'gunluk_toplamlar': { # Toplam değerler (Simülasyon süresi boyunca)
            "Toplam Tren Tüketimi (kWh)": toplam_tren_tuketimi,
            "Geri Kazanılan Enerji (kWh)": geri_kazanilan_enerji,
            "Net Tren Tüketimi (kWh)": net_tren_tuketimi,
            "İstasyon Tüketimi (kWh)": toplam_istasyon_tuketimi,
            "Güneş Paneli Üretimi (kWh)": toplam_gunes_uretimi,
            "Rüzgar Türbini Üretimi (kWh)": toplam_ruzgar_uretimi,
            "Toplam Sistem Net Tüketimi (kWh)": net_tren_tuketimi + toplam_istasyon_tuketimi,
            "Toplam Yenilenebilir Üretim (kWh)": toplam_gunes_uretimi + toplam_ruzgar_uretimi,
            "Toplam Batarya Şarj Miktarı (kWh)": toplam_batarya_sarj,
            "Toplam Batarya Deşarj Miktarı (kWh)": toplam_batarya_desarj,
            "Şebekeden Toplam Alım (kWh)": toplam_sebekeden_alim,
            "Şebekeye Toplam Verme (kWh)": toplam_sebekeye_verme,
            "Net Enerji Dengesi (Şebeke Etkisi ile) (kWh)": net_enerji_dengesi_sebeke,
            "Toplam Enerji Maliyeti (TL)": toplam_enerji_maliyeti,
            "Toplam Karbon Ayak İzi (Şebeke Alımından) (kg CO2e)": toplam_karbon_ayak_izi
        },
        'toplam_saat': toplam_saat,
        'simulasyon_suresi_gun': simulasyon_suresi_gun,
        # Grafik fonksiyonları için gerekli bazı temel parametreleri de buraya ekleyelim
        'BATARYA_KAPASITESI_KWH': batarya_kapasitesi_kwh 
    }

    return sonuclar

# NOT: Grafik çizim fonksiyonları buradan silindi ve gorsellestirme.py dosyasına taşınması gerekiyor.
# Lütfen gorsellestirme.py dosyanızın güncellenmiş simulasyon_motoru çıktısı olan
# 'sonuclar' dictionary'sini kabul ettiğinden emin olun.
# Örnek gorsellestirme.py içeriğini bir önceki cevabımda vermiştim.