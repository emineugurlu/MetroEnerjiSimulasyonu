# gorsellestirme.py
import matplotlib.pyplot as plt
import pandas as pd # Pandas'ı burada da içe aktarıyoruz

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

    plt.figure(figsize=(10, 6))
    plt.bar(etiketler, degerler, color=renkler)

    plt.ylabel('Enerji Miktarı (kWh)')
    plt.title(grafik_adi)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.axhline(0, color='black', linewidth=0.8)

    for i, v in enumerate(degerler):
        plt.text(i, v + 100, f'{v:.0f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show(block=False) # Grafiği göstermesi ve devam etmesi için block=False

def enerji_dengesi_cizgi_grafigi_olustur(saatlik_veri_df, grafik_adi="Saatlik Metro Enerji Akışı"):
    """
    Saatlik simülasyon sonuçlarını çizgi grafik olarak görselleştirir.
    """
    print(f"\n--- Çizgi Grafik Oluşturuluyor: {grafik_adi} ---")

    plt.figure(figsize=(12, 7))

    plt.plot(saatlik_veri_df['Saat'], saatlik_veri_df['Toplam Sistem Net Tüketimi (kWh)'],
             label='Toplam Sistem Net Tüketimi', color='red', marker='o', linestyle='-')
    plt.plot(saatlik_veri_df['Saat'], saatlik_veri_df['Toplam Yenilenebilir Üretim (kWh)'],
             label='Toplam Yenilenebilir Üretim', color='green', marker='o', linestyle='-')
    plt.plot(saatlik_veri_df['Saat'], saatlik_veri_df['Net Enerji Dengesi (kWh)'],
             label='Net Enerji Dengesi', color='blue', linestyle='--', marker='x')

    plt.xlabel('Saat')
    plt.ylabel('Enerji Miktarı (kWh)')
    plt.title(grafik_adi)
    plt.xticks(saatlik_veri_df['Saat']) # Saatleri tam sayı olarak göster
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.axhline(0, color='black', linewidth=0.8, linestyle='-') # Sıfır çizgisi
    plt.legend()
    plt.tight_layout()
    plt.show() # Son grafiği göstermesi ve bekletmesi için block=True (varsayılan)