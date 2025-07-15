# gorsellestirme.py
import matplotlib.pyplot as plt
import pandas as pd

def enerji_dengesi_cubuk_grafigi_olustur(sonuclar_dict, grafik_adi="Günlük Metro Enerji Dengesi"):
    """
    Simülasyonun günlük toplam sonuçlarını çubuk grafik olarak görselleştirir.
    """
    print(f"\n--- Çubuk Grafik Oluşturuluyor: {grafik_adi} ---")

    etiketler = ['Toplam Net Tüketim', 'Güneş Üretimi', 'Rüzgar Üretimi']
    degerler = [
        sonuclar_dict["Toplam Sistem Net Tüketimi (kWh)"],
        sonuclar_dict["Güneş Paneli Üretimi (kWh)"],
        sonuclar_dict["Rüzgar Türbini Üretimi (kWh)"]
    ]
    renkler = ['red', 'green', 'green']

    if sonuclar_dict.get("Günlük Şebekeden Alım (kWh)", 0) > 0:
        etiketler.append('Şebekeden Alım')
        degerler.append(sonuclar_dict["Günlük Şebekeden Alım (kWh)"])
        renkler.append('purple')
    if sonuclar_dict.get("Günlük Şebekeye Verme (kWh)", 0) > 0:
        etiketler.append('Şebekeye Verme')
        degerler.append(sonuclar_dict["Günlük Şebekeye Verme (kWh)"])
        renkler.append('orange')

    plt.figure(figsize=(12, 7))
    plt.bar(etiketler, degerler, color=renkler)

    plt.ylabel('Enerji Miktarı (kWh)')
    plt.title(grafik_adi)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.axhline(0, color='black', linewidth=0.8)

    for i, v in enumerate(degerler):
        plt.text(i, v + (v * 0.05 if v != 0 else 100), f'{v:.0f}', ha='center', va='bottom')

    plt.tight_layout()
    # plt.show(block=False) # BU SATIR SİLİNDİ!

def enerji_dengesi_cizgi_grafigi_olustur(saatlik_veri_df, grafik_adi="Saatlik Metro Enerji Akışı"):
    """
    Saatlik simülasyon sonuçlarını çizgi grafik olarak görselleştirir.
    Toplam sistem net tüketimi, toplam yenilenebilir üretim ve şebeke etkileri sonrası net enerji dengesini gösterir.
    """
    print(f"\n--- Çizgi Grafik Oluşturuluyor: {grafik_adi} ---")

    plt.figure(figsize=(14, 8))

    plt.plot(saatlik_veri_df['Saat'], saatlik_veri_df['Toplam Sistem Net Tüketimi (kWh)'],
             label='Toplam Sistem Net Tüketimi', color='red', marker='o', linestyle='-')
    plt.plot(saatlik_veri_df['Saat'], saatlik_veri_df['Toplam Yenilenebilir Üretim (kWh)'],
             label='Toplam Yenilenebilir Üretim', color='green', marker='o', linestyle='-')
    plt.plot(saatlik_veri_df['Saat'], saatlik_veri_df['Şebekeden Alım (kWh)'],
             label='Şebekeden Alım', color='purple', linestyle=':', marker='^')
    plt.plot(saatlik_veri_df['Saat'], -saatlik_veri_df['Şebekeye Verme (kWh)'],
             label='Şebekeye Verme', color='orange', linestyle=':', marker='v')

    plt.xlabel('Saat')
    plt.ylabel('Enerji Miktarı (kWh)')
    plt.title(grafik_adi)
    plt.xticks(saatlik_veri_df['Saat'])
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.axhline(0, color='black', linewidth=0.8, linestyle='-')
    plt.legend()
    plt.tight_layout()
    # plt.show(block=False) # BU SATIR SİLİNDİ!

def batarya_doluluk_grafigi_olustur(saatlik_veri_df, grafik_adi="Saatlik Batarya Doluluk Seviyesi"):
    """
    Saatlik batarya doluluk seviyesini ve oranını gösteren çizgi grafik oluşturur.
    """
    print(f"\n--- Batarya Doluluk Grafiği Oluşturuluyor: {grafik_adi} ---")

    fig, ax1 = plt.subplots(figsize=(14, 7))

    color = 'blue'
    ax1.set_xlabel('Saat')
    ax1.set_ylabel('Batarya Doluluk (kWh)', color=color)
    ax1.plot(saatlik_veri_df['Saat'], saatlik_veri_df['Batarya Doluluk (kWh)'],
             label='Batarya Doluluk (kWh)', color=color, marker='o', linestyle='-')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle='--', alpha=0.6)

    ax2 = ax1.twinx()
    color = 'cyan'
    ax2.set_ylabel('Batarya Doluluk Oranı (%)', color=color)
    ax2.plot(saatlik_veri_df['Saat'], saatlik_veri_df['Batarya Doluluk Oranı (%)'],
             label='Batarya Doluluk Oranı (%)', color=color, linestyle='--')
    ax2.tick_params(axis='y', labelcolor=color)

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.title(grafik_adi)
    plt.xticks(saatlik_veri_df['Saat'])
    plt.tight_layout()
    # plt.show(block=False) # BU SATIR SİLİNDİ!

def batarya_akim_grafigi_olustur(saatlik_veri_df, grafik_adi="Saatlik Batarya Şarj/Deşarj Akışı"):
    """
    Saatlik batarya şarj ve deşarj akışını gösteren çubuk grafik oluşturur.
    """
    print(f"\n--- Batarya Akım Grafiği Oluşturuluyor: {grafik_adi} ---")

    plt.figure(figsize=(14, 7))
    plt.bar(saatlik_veri_df['Saat'] - 0.2, saatlik_veri_df['Bataryaya Giden (kWh)'],
            width=0.4, label='Bataryaya Şarj Edilen', color='darkgreen', alpha=0.7)
    plt.bar(saatlik_veri_df['Saat'] + 0.2, -saatlik_veri_df['Bataryadan Çekilen (kWh)'],
            width=0.4, label='Bataryadan Çekilen', color='darkred', alpha=0.7)

    plt.xlabel('Saat')
    plt.ylabel('Enerji Akışı (kWh)')
    plt.title(grafik_adi)
    plt.xticks(saatlik_veri_df['Saat'])
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.axhline(0, color='black', linewidth=0.8)
    plt.legend()
    plt.tight_layout()
    # plt.show(block=False) # BU SATIR SİLİNDİ!

def saatlik_maliyet_grafigi_olustur(saatlik_veri_df, grafik_adi="Saatlik Enerji Maliyeti/Geliri"):
    """
    Saatlik enerji maliyeti/gelirini gösteren çizgi grafik oluşturur.
    """
    print(f"\n--- Maliyet Grafiği Oluşturuluyor: {grafik_adi} ---")

    plt.figure(figsize=(14, 7))
    plt.plot(saatlik_veri_df['Saat'], saatlik_veri_df['Saatlik Maliyet (TL)'],
             label='Saatlik Net Maliyet (TL)', color='darkmagenta', marker='s', linestyle='-')

    plt.xlabel('Saat')
    plt.ylabel('Maliyet (TL)')
    plt.title(grafik_adi)
    plt.xticks(saatlik_veri_df['Saat'])
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.axhline(0, color='black', linewidth=0.8)
    plt.legend()
    plt.tight_layout()
    # plt.show() # BU SATIR SİLİNDİ!