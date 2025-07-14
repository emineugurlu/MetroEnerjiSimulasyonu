# gorsellestirme.py
import matplotlib.pyplot as plt

def enerji_dengesi_grafigi_olustur(sonuclar):
    """
    Simülasyon sonuçlarını görselleştiren bir çubuk grafik oluşturur.

    Parametreler:
    - sonuclar (dict): Simulasyon motorundan dönen enerji hesaplama sonuçları sözlüğü.
    """
    print("\n--- Grafik Oluşturuluyor... ---")

    etiketler = ['Toplam Net Tüketim', 'Güneş Üretimi', 'Rüzgar Üretimi']
    degerler = [
        sonuclar["Toplam Sistem Net Tüketimi (kWh)"],
        sonuclar["Güneş Paneli Üretimi (kWh)"],
        sonuclar["Rüzgar Türbini Üretimi (kWh)"]
    ]

    renkler = ['red', 'green', 'green']

    plt.figure(figsize=(10, 6))
    plt.bar(etiketler, degerler, color=renkler)

    plt.ylabel('Enerji Miktarı (kWh)')
    plt.title('Günlük Metro Enerji Dengesi')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.axhline(0, color='black', linewidth=0.8)

    for i, v in enumerate(degerler):
        plt.text(i, v + 100, f'{v:.0f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()