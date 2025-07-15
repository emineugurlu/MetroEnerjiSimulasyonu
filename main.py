# main.py

import pandas as pd
import simulasyon_motoru as sm
import gorsellestirme as gorsel # Varsayılan olarak ayrı bir gorsellestirme.py dosyanız olduğunu varsayıyorum
import parametreler as p       # Varsayılan olarak ayrı bir parametreler.py dosyanız olduğunu varsayıyorum
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
        exit() # Dosya bulunamazsa programdan çık

    # Adım 2: Dinamik Simülasyonu Akıllı Batarya Entegrasyonu ile Çalıştır
    # simulasyon_motoru.py dosyanızdaki fonksiyon adını 'akilli_ems_simulasyon' yerine
    # 'hesapla_dinamik_enerji_dengesi' olarak adlandırdığınızı varsayıyorum
    print(f"\n\n--- Dinamik (Saatlik) Simülasyon Akıllı EMS ile Çalıştırılıyor ({len(df_dinamik_veriler) / 24:.1f} Günlük) ---") # Dinamik gün sayısı eklendi

    dinamik_simulasyon_sonuclari = sm.hesapla_dinamik_enerji_dengesi(
        df_dinamik_veriler,
        p.TREN_BASINA_MAKS_TUKETIM_KWH,
        p.FRENLEME_GERI_KAZANIM_ORANI,
        p.MAKS_ISTASYON_TUKETIMI_KWH,
        p.MAKS_GUNES_PANELI_URETIMI_KWH,
        p.MAKS_RUZGAR_TURBINI_URETIMI_KWH,
        # p.VARSAYILAN_GUNLUK_TOPLAM_SEFER, # Bu parametre dinamik veri ile genellikle kullanılmaz, gerekiyorsa simülasyon motorunda içsel olarak hesaplanmalı
        
        # Batarya Parametreleri
        p.BATARYA_KAPASITESI_KWH,
        p.SARJ_VERIMLILIGI,
        p.DESARJ_VERIMLILIGI,
        p.BASLANGIC_BATARYA_DOLULUK_ORANI,
        p.BATARYA_BOSALTMA_ESIGI_ORAN,
        p.BATARYA_DOLDURMA_ESIGI_ORAN,
        
        # Elektrik Fiyatları Parametresi
        p.ELEKTRIK_BIRIM_FIYATLARI_TL_KWH, # Tek bir değer yerine dictionary bekliyorsa sim. motorunda ayarlanmalı
        p.ELEKTRIK_BIRIM_FIYATLARI_TL_KWH_SATIS # Yeni: Satış fiyatını da parametrelerden almalı
    )

    # Simülasyon sonucu None ise hata mesajı verip çık
    if dinamik_simulasyon_sonuclari is None:
        print("Simülasyon sonuçları alınamadı. Lütfen 'simulasyon_motoru.py' dosyasındaki hataları kontrol edin.")
        exit()

    # Adım 3: Dinamik simülasyonun genel sonuçlarını göster
    # Artık 'gunluk_toplamlar' anahtarı altında toplu veriler var
    print("\n--- Dinamik Simülasyon - Toplam Enerji Hesaplamaları (Akıllı EMS Entegreli) ---")
    
    # 'gunluk_toplamlar' dictionary'sindeki her öğeyi yazdır
    for key, value in dinamik_simulasyon_sonuclari["gunluk_toplamlar"].items():
        if "Maliyet" in key or "Gelir" in key:
            print(f"{key}: {value:.2f} TL")
        elif "kg CO2e" in key: # Karbon ayak izi için yeni çıktı formatı
            print(f"{key}: {value:.2f} kg CO2e")
        else:
            print(f"{key}: {value:.2f} kWh")

    print("\n--- Dinamik Simülasyon Yorumu (Akıllı EMS Entegreli) ---")
    
    # Günlük toplamlar dictionary'sinden ilgili değerleri çek
    net_enerji_dengesi_sebeke = dinamik_simulasyon_sonuclari["gunluk_toplamlar"].get("Net Enerji Dengesi (Şebeke Etkisi ile) (kWh)", 0)
    toplam_maliyet = dinamik_simulasyon_sonuclari["gunluk_toplamlar"].get("Toplam Enerji Maliyeti (TL)", 0)
    toplam_karbon_ayak_izi = dinamik_simulasyon_sonuclari["gunluk_toplamlar"].get("Toplam Karbon Ayak İzi (Şebeke Alımından) (kg CO2e)", 0) # Yeni

    if net_enerji_dengesi_sebeke < 0:
        print(f"Bu {dinamik_simulasyon_sonuclari['simulasyon_suresi_gun']:.1f} günlük senaryoda metro sistemi net enerji fazlası vermektedir! (ENERJİ POZİTİF!)")
        print(f"Fazla enerji (şebekeye verilen): {-net_enerji_dengesi_sebeke:.2f} kWh")
    elif net_enerji_dengesi_sebeke == 0:
        print(f"Bu {dinamik_simulasyon_sonuclari['simulasyon_suresi_gun']:.1f} günlük senaryoda metro sistemi net enerji dengesindedir (şebekeden alım/verme yok).")
    else:
        print(f"Bu {dinamik_simulasyon_sonuclari['simulasyon_suresi_gun']:.1f} günlük senaryoda metro sistemi net enerji tüketmektedir. Enerji açığı (şebekeden alınan): {net_enerji_dengesi_sebeke:.2f} kWh")

    print(f"Toplam Enerji Maliyeti/Geliri: {toplam_maliyet:.2f} TL")
    if toplam_maliyet < 0:
        print(f"Sistem toplamda {abs(toplam_maliyet):.2f} TL gelir elde etmektedir (Enerji Satışı).")
    elif toplam_maliyet > 0:
        print(f"Sistem toplamda {toplam_maliyet:.2f} TL maliyet oluşturmaktadır (Enerji Alımı).")
    else:
        print(f"Sistem toplamda enerji maliyeti/geliri dengesindedir.")
    
    print(f"Şebekeden alım kaynaklı toplam karbon ayak izi: {toplam_karbon_ayak_izi:.2f} kg CO2e") # Karbon ayak izi çıktısı

   # main.py dosyasında, dinamik_simulasyon_sonuclari hesaplandıktan sonra ve
# görselleştirme fonksiyonlarını çağırmadan hemen önce bu satırı ekleyin:

    # Saatlik veriyi Pandas DataFrame'e dönüştür
    saatlik_veri_df_gorsellestirme = pd.DataFrame(dinamik_simulasyon_sonuclari['saatlik_veri'])

    # Adım 4: Görselleştirmeleri Oluştur
    # ...
    # Aşağıdaki fonksiyon çağrılarında da simulasyon_sonuclari['saatlik_veri'] yerine
    # saatlik_veri_df_gorsellestirme değişkenini kullanacağız.

# Günlük Toplam Enerji Dengesi Çubuk Grafiği (Burada saatlik veri_df kullanılmıyor, olduğu gibi kalabilir)
gorsel.enerji_dengesi_cubuk_grafigi_olustur(
    sonuclar_dict={ 
        "Toplam Sistem Net Tüketimi (kWh)": dinamik_simulasyon_sonuclari['gunluk_toplamlar']["Toplam Sistem Net Tüketimi (kWh)"],
        "Güneş Paneli Üretimi (kWh)": dinamik_simulasyon_sonuclari['gunluk_toplamlar']["Güneş Paneli Üretimi (kWh)"],
        "Rüzgar Türbini Üretimi (kWh)": dinamik_simulasyon_sonuclari['gunluk_toplamlar']["Rüzgar Türbini Üretimi (kWh)"],
        "Günlük Şebekeden Alım (kWh)": dinamik_simulasyon_sonuclari['gunluk_toplamlar']["Şebekeden Toplam Alım (kWh)"],
        "Günlük Şebekeye Verme (kWh)": dinamik_simulasyon_sonuclari['gunluk_toplamlar']["Şebekeye Toplam Verme (kWh)"]
    },
    grafik_adi="Dinamik Simülasyon - Günlük Toplam Enerji Dengesi (Akıllı EMS ile)"
)

# Saatlik Enerji Akışı Çizgi Grafiği (Şebeke ile)
gorsel.enerji_dengesi_cizgi_grafigi_olustur(
    saatlik_veri_df=saatlik_veri_df_gorsellestirme, # <-- BURASI DEĞİŞTİ!
    grafik_adi="Dinamik Simülasyon - Saatlik Enerji Akışı (Akıllı EMS ile)"
)

# Saatlik Batarya Doluluk Seviyesi Grafiği
gorsel.batarya_doluluk_grafigi_olustur(
    saatlik_veri_df=saatlik_veri_df_gorsellestirme, # <-- BURASI DEĞİŞTİ!
    grafik_adi="Dinamik Simülasyon - Saatlik Batarya Doluluk Seviyesi (Akıllı EMS ile)"
)

# Saatlik Batarya Şarj/Deşarj Akışı Grafiği
gorsel.batarya_akim_grafigi_olustur(
    saatlik_veri_df=saatlik_veri_df_gorsellestirme, # <-- BURASI DEĞİŞTİ!
    grafik_adi="Dinamik Simülasyon - Saatlik Batarya Şarj/Deşarj Akışı (Akıllı EMS ile)"
)

# Saatlik Enerji Maliyeti/Geliri Grafiği
gorsel.saatlik_maliyet_grafigi_olustur(
    saatlik_veri_df=saatlik_veri_df_gorsellestirme, # <-- BURASI DEĞİŞTİ!
    grafik_adi="Dinamik Simülasyon - Saatlik Enerji Maliyeti/Geliri (Akıllı EMS ile)"
)

plt.show()