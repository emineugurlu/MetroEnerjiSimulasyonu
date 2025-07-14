# simulasyon_motoru.py

def hesapla_enerji_dengesi(sefer_sayisi, tren_tuketim, frenleme_oran,
                         istasyon_tuketim, gunes_uretim, ruzgar_uretim): # Parametre adları burada doğru
    """
    Metro sistemi için temel enerji dengesi hesaplamalarını yapar.
    Parametre adları Excel sütun adlarıyla eşleşecek şekilde ayarlandı.

    Dönüş:
    - dict: Detaylı enerji hesaplamalarını içeren bir sözlük.
    """

    toplam_tren_tuketimi = sefer_sayisi * tren_tuketim
    geri_kazanilan_enerji = toplam_tren_tuketimi * frenleme_oran
    net_tren_tuketimi = toplam_tren_tuketimi - geri_kazanilan_enerji
    toplam_sistem_net_tuketimi = net_tren_tuketimi + istasyon_tuketim # Hata buradaydı, 'istasyon_tuketimi' yerine 'istasyon_tuketim' olmalı
    toplam_yenilenebilir_uretim = gunes_uretim + ruzgar_uretim
    net_enerji_dengesi = toplam_sistem_net_tuketimi - toplam_yenilenebilir_uretim

    return {
        "Toplam Tren Tüketimi (kWh)": toplam_tren_tuketimi,
        "Geri Kazanılan Enerji (kWh)": geri_kazanilan_enerji,
        "İstasyon Tüketimi (kWh)": istasyon_tuketim, # Burada da düzeltmeyi yapalım, tutarlı olması için
        "Güneş Paneli Üretimi (kWh)": gunes_uretim,
        "Rüzgar Türbini Üretimi (kWh)": ruzgar_uretim,
        "Toplam Sistem Net Tüketimi (kWh)": toplam_sistem_net_tuketimi,
        "Toplam Yenilenebilir Üretim (kWh)": toplam_yenilenebilir_uretim,
        "Net Enerji Dengesi (kWh)": net_enerji_dengesi
    }