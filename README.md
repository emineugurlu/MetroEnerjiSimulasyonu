# ⚡ Enerji Pozitif Metro Projesi: Akıllı EMS Entegreli Dinamik Simülasyon 🚇🔋☀️

## Proje Özeti

Bu proje, metro sistemlerinin enerji tüketimini sadece karşılamakla kalmayıp, kendi enerjisini üreten ve hatta ürettiği fazlayı ulusal elektrik şebekesine geri veren, yani "Enerji Pozitif" hale gelen sürdürülebilir bir model oluşturmayı hedefleyen yenilikçi bir **konsept kanıtlama (Proof of Concept)** simülasyonudur. ✨ Akıllı bir Enerji Yönetim Sistemi (EMS) entegrasyonuyla yenilenebilir enerji kaynaklarını (güneş ve rüzgar) metro altyapısına entegre ederek, enerji verimliliğini ve çevresel sürdürülebilirliği maksimize etmeyi amaçlamaktadır.

## 🌟 Projenin Amacı

* Metro sistemlerinin enerji bağımsızlığını artırmak.
* Fosil yakıt tüketimini ve karbon ayak izini azaltmak. 🌱
* Yenilenebilir enerji kaynaklarının büyük ölçekli altyapılarda entegrasyon potansiyelini göstermek.
* Akıllı enerji yönetimi ve batarya depolama sistemlerinin rolünü modellemek.
* Projenin ekonomik ve çevresel fizibilitesini simülasyon yoluyla ortaya koymak. 💰

## ⚙️ Temel Bileşenler ve Yaklaşım

Proje, aşağıdaki ana bileşenleri içeren dinamik bir simülasyon modeli üzerine kurulmuştur:

1.  **Dinamik Veri Profilleri:** Metro tren sefer yoğunluğu, istasyon enerji tüketimi, güneş radyasyonu ve rüzgar hızı gibi saatlik dinamik veriler, gerçekçi bir senaryo modellemesi için `dinamik_veriler.xlsx` dosyasından okunur.
2.  **Yenilenebilir Enerji Kaynakları:** Güneş panelleri ☀️ ve rüzgar türbinleri 🌬️, metro sistemine entegre edilmiş olup, dinamik verilere göre enerji üretimi simüle edilir.
3.  **Akıllı Enerji Yönetim Sistemi (EMS):** Projenin kalbi olan EMS, enerji üretimini (yenilenebilir), tüketimi (tren ve istasyon), batarya şarj/deşarjını ve şebeke etkileşimini (alım/satım) en uygun maliyet ve verimlilikle yönetmek için tasarlanmıştır. Bu sistem, enerji akışını optimize etmek için bir optimizasyon modeli (Pulp kütüphanesi kullanılarak) kullanır.
4.  **Batarya Enerji Depolama Sistemi:** Bataryalar 🔋, enerji fazlasını depolayarak yenilenebilir enerjinin dalgalanmalarını dengelemekte ve sistemin anlık ihtiyaçlarını karşılamada kritik bir rol oynamaktadır. Şarj ve deşarj verimlilikleri, minimum/maksimum doluluk eşikleri gibi parametreler dikkate alınmıştır.
5.  **Finansal ve Çevresel Analiz:** Simülasyon, enerji maliyetleri/gelirleri, toplam yatırım (CAPEX), işletme-bakım (OPEX) maliyetleri ve karbon emisyonları gibi metrikleri hesaplayarak projenin ekonomik ve çevresel etkilerini nicel olarak değerlendirir.

## 📈 Elde Edilen Başarılar ve Sonuçlar

Yapılan simülasyonlar sonucunda projenin temel hedeflerine ulaşıldığı gözlemlenmiştir:

* **Enerji Pozitiflik:** Simülasyon, metro sisteminin kendi tüketimini (tren ve istasyon) karşılamanın ötesinde, yenilenebilir enerji kaynaklarıyla önemli miktarda enerji fazlası ürettiğini ve bu fazlalığı ulusal şebekeye geri verdiğini göstermiştir.
* **Düşük Şebeke Bağımlılığı:** Akıllı EMS ve batarya depolama sayesinde, metro sisteminin şebekeden enerji alımının neredeyse sıfıra indiği kanıtlanmıştır.
* **Ekonomik Potansiyel:** Enerji satışlarından elde edilen gelirler ve optimize edilmiş enerji yönetimi sayesinde, projenin simülasyon dönemi için net kâr potansiyeli taşıdığı belirlenmiştir.
* **Çevresel Fayda:** Şebekeden alımın minimize edilmesiyle, metro sisteminin karbon ayak izi önemli ölçüde azaltılmıştır.

## 📊 Örnek Simülasyon Çıktıları (Ekran Görüntüleri)

Simülasyon çalıştırıldıktan sonra üretilen bazı grafik örnekleri:


_Grafik 1: Günlük Metro Enerji Dengesi_
<img width="1915" height="1002" alt="image" src="https://github.com/user-attachments/assets/3256f02a-4b9d-4399-92e5-3d44b2f8367e" />

_Grafik 2: Saatlik Metro Enerji Akışı_
<img width="1919" height="1014" alt="image" src="https://github.com/user-attachments/assets/786c9e7a-6d54-4137-a309-29a50a6f5167" />

_Grafik 3: Saatlik Batarya Doluluk Seviyesi_
<img width="1919" height="1011" alt="image" src="https://github.com/user-attachments/assets/03d8d99e-78c4-4af2-b4ae-056bc263bb80" />

_Grafik 4: Saatlik Batarya Şarj/Deşarj Akışı_
<img width="1919" height="1018" alt="image" src="https://github.com/user-attachments/assets/12de54b7-d3c5-4043-adc9-307fbe4c4cb9" />

_Grafik 5: Saatlik Enerji Maliyeti/Geliri_
<img width="1917" height="1014" alt="image" src="https://github.com/user-attachments/assets/7692516f-f507-4bd1-a968-cda6a69a287e" />

## 📂 Proje Yapısı
Kodlama desteği
Şefim, kesinlikle! README dosyasını daha çekici, bilgilendirici ve kullanıcı dostu hale getirelim. Ekran görüntüleri, kurulum talimatları ve biraz emoji, projenizi çok daha cazip kılacaktır.

İşte güncellenmiş ve zenginleştirilmiş README taslağımız:

Markdown

# ⚡ Enerji Pozitif Metro Projesi: Akıllı EMS Entegreli Dinamik Simülasyon 🚇🔋☀️

## Proje Özeti

Bu proje, metro sistemlerinin enerji tüketimini sadece karşılamakla kalmayıp, kendi enerjisini üreten ve hatta ürettiği fazlayı ulusal elektrik şebekesine geri veren, yani "Enerji Pozitif" hale gelen sürdürülebilir bir model oluşturmayı hedefleyen yenilikçi bir **konsept kanıtlama (Proof of Concept)** simülasyonudur. ✨ Akıllı bir Enerji Yönetim Sistemi (EMS) entegrasyonuyla yenilenebilir enerji kaynaklarını (güneş ve rüzgar) metro altyapısına entegre ederek, enerji verimliliğini ve çevresel sürdürülebilirliği maksimize etmeyi amaçlamaktadır.

## 🌟 Projenin Amacı

* Metro sistemlerinin enerji bağımsızlığını artırmak.
* Fosil yakıt tüketimini ve karbon ayak izini azaltmak. 🌱
* Yenilenebilir enerji kaynaklarının büyük ölçekli altyapılarda entegrasyon potansiyelini göstermek.
* Akıllı enerji yönetimi ve batarya depolama sistemlerinin rolünü modellemek.
* Projenin ekonomik ve çevresel fizibilitesini simülasyon yoluyla ortaya koymak. 💰

## ⚙️ Temel Bileşenler ve Yaklaşım

Proje, aşağıdaki ana bileşenleri içeren dinamik bir simülasyon modeli üzerine kurulmuştur:

1.  **Dinamik Veri Profilleri:** Metro tren sefer yoğunluğu, istasyon enerji tüketimi, güneş radyasyonu ve rüzgar hızı gibi saatlik dinamik veriler, gerçekçi bir senaryo modellemesi için `dinamik_veriler.xlsx` dosyasından okunur.
2.  **Yenilenebilir Enerji Kaynakları:** Güneş panelleri ☀️ ve rüzgar türbinleri 🌬️, metro sistemine entegre edilmiş olup, dinamik verilere göre enerji üretimi simüle edilir.
3.  **Akıllı Enerji Yönetim Sistemi (EMS):** Projenin kalbi olan EMS, enerji üretimini (yenilenebilir), tüketimi (tren ve istasyon), batarya şarj/deşarjını ve şebeke etkileşimini (alım/satım) en uygun maliyet ve verimlilikle yönetmek için tasarlanmıştır. Bu sistem, enerji akışını optimize etmek için bir optimizasyon modeli (Pulp kütüphanesi kullanılarak) kullanır.
4.  **Batarya Enerji Depolama Sistemi:** Bataryalar 🔋, enerji fazlasını depolayarak yenilenebilir enerjinin dalgalanmalarını dengelemekte ve sistemin anlık ihtiyaçlarını karşılamada kritik bir rol oynamaktadır. Şarj ve deşarj verimlilikleri, minimum/maksimum doluluk eşikleri gibi parametreler dikkate alınmıştır.
5.  **Finansal ve Çevresel Analiz:** Simülasyon, enerji maliyetleri/gelirleri, toplam yatırım (CAPEX), işletme-bakım (OPEX) maliyetleri ve karbon emisyonları gibi metrikleri hesaplayarak projenin ekonomik ve çevresel etkilerini nicel olarak değerlendirir.

## 📈 Elde Edilen Başarılar ve Sonuçlar

Yapılan simülasyonlar sonucunda projenin temel hedeflerine ulaşıldığı gözlemlenmiştir:

* **Enerji Pozitiflik:** Simülasyon, metro sisteminin kendi tüketimini (tren ve istasyon) karşılamanın ötesinde, yenilenebilir enerji kaynaklarıyla önemli miktarda enerji fazlası ürettiğini ve bu fazlalığı ulusal şebekeye geri verdiğini göstermiştir.
* **Düşük Şebeke Bağımlılığı:** Akıllı EMS ve batarya depolama sayesinde, metro sisteminin şebekeden enerji alımının neredeyse sıfıra indiği kanıtlanmıştır.
* **Ekonomik Potansiyel:** Enerji satışlarından elde edilen gelirler ve optimize edilmiş enerji yönetimi sayesinde, projenin simülasyon dönemi için net kâr potansiyeli taşıdığı belirlenmiştir.
* **Çevresel Fayda:** Şebekeden alımın minimize edilmesiyle, metro sisteminin karbon ayak izi önemli ölçüde azaltılmıştır.

## 📊 Örnek Simülasyon Çıktıları (Ekran Görüntüleri)

Simülasyon çalıştırıldıktan sonra üretilen bazı grafik örnekleri:

**(Buraya Çubuk Grafik Görseli Gelecek - örn. `enerji_dengesi_cubuk.png`)**
_Grafik 1: Günlük Metro Enerji Dengesi_

**(Buraya Çizgi Grafik Görseli Gelecek - örn. `enerji_dengesi_cizgi.png`)**
_Grafik 2: Saatlik Metro Enerji Akışı_

**(Buraya Batarya Doluluk Grafiği Görseli Gelecek - örn. `batarya_doluluk.png`)**
_Grafik 3: Saatlik Batarya Doluluk Seviyesi_

**(Buraya Batarya Akım Grafiği Görseli Gelecek - örn. `batarya_akim.png`)**
_Grafik 4: Saatlik Batarya Şarj/Deşarj Akışı_

**(Buraya Maliyet Grafiği Görseli Gelecek - örn. `saatlik_maliyet.png`)**
_Grafik 5: Saatlik Enerji Maliyeti/Geliri_

## 📂 Proje Yapısı

MetroEnerjiSimulasyonu
├── main.py                 # 🚀 Ana simülasyonu başlatan ve sonuçları görselleştiren dosya
├── simulasyon_motoru.py    # 🧠 Enerji dengesi hesaplamalarını ve EMS optimizasyonunu içeren ana mantık
├── gorsellestirme.py       # 📊 Simülasyon sonuçlarını grafiklere döken fonksiyonlar
├── parametreler.py         # ⚙️ Simülasyon için tüm sabit parametrelerin tanımlandığı dosya
├── dinamik_veriler.xlsx    # 📈 Saatlik enerji tüketim ve üretim profillerini içeren Excel dosyası
└── README.md               # 📄 Bu dosya

## 🚀 Nasıl Çalıştırılır?

Projenin kendi sisteminizde çalışması için aşağıdaki adımları takip edin:

1.  **Ön Gereksinimler:**
    * Python 3.x sürümünün kurulu olduğundan emin olun.
    * Gerekli Python kütüphanelerini yükleyin. Terminalinizde şu komutu çalıştırın:
        ```bash
        pip install pandas matplotlib pulp openpyxl
        ```
        (Not: `openpyxl`, `pandas`'ın Excel dosyalarını okuması için gerekli olabilir.)

2.  **Depoyu Klonlama veya İndirme:**
    * Git yüklüyse, terminalde istediğiniz dizine giderek depoyu klonlayın:
        ```bash
        git clone [https://github.com/KULLANICI_ADINIZ/EnerjiPozitifMetro.git](https://github.com/KULLANICI_ADINIZ/EnerjiPozitifMetro.git)
        ```

3.  **Proje Dizine Gitme:**
    * Terminalinizde projenin ana dizinine (yani `main.py` dosyasının bulunduğu klasöre) geçin:
        ```bash
        cd MetroEnerjiSimulasyonu
        ``

4.  **Simülasyonu Başlatma:**
    * Aşağıdaki komutu çalıştırarak simülasyonu başlatın:
        ```bash
        python main.py
        ```

5.  **Sonuçlar:**
    * Simülasyonun ilerlemesini ve özet sonuçlarını terminalde anlık olarak göreceksiniz.
    * Simülasyon tamamlandığında, `matplotlib` tarafından oluşturulan çeşitli grafik pencereleri otomatik olarak açılacaktır. 📊

## 💡 Gelecek Geliştirme Fırsatları (Vizyonumuz)

Bu proje, gelecekteki daha kapsamlı ve gerçek dünya uygulamalarına yönelik çalışmalar için güçlü bir temel sunmaktadır. Potansiyel geliştirme alanlarımız şunlardır:

* **Makine Öğrenmesi Tabanlı Tahmin:** Enerji talebi ve yenilenebilir enerji üretiminin daha isabetli tahmin edilmesi için gelişmiş makine öğrenmesi modellerinin entegrasyonu. Bu, EMS'in proaktif kararlar almasını sağlayacaktır.
* **Dijital İkiz (Digital Twin) Entegrasyonu:** Metro sisteminin ve enerji altyapısının sanal bir kopyasını oluşturarak, "ne olur?" senaryoları üzerinde detaylı analizler yapmak, bakım süreçlerini optimize etmek ve sistemi otomatik olarak iyileştirmek.
* **Enerji Ticareti Modülleri:** Fazla enerjinin spot piyasada dinamik fiyatlandırma algoritmalarıyla değerlendirilerek, projenin finansal gelirlerini maksimize etmek.
* **Sosyal ve Çevresel Etki Analizi:** Karbon azaltımının hava kalitesine, halk sağlığına ve şehir halkının genel refahına olan somut katkılarının bilimsel olarak sayısallaştırılması ve proje paydaşlarına ek değer önerisi olarak sunulması.

---
