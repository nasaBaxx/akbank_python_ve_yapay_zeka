# 🚇 Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu)

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.6+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

> Gelişmiş algoritma tabanlı metro ağı simülasyonu ve rota optimizasyonu

Bu proje, bir metro ağında iki istasyon arasındaki en hızlı ve en az aktarmalı rotaları bulan gelişmiş bir simülasyon uygulamasıdır. Graf veri yapısını kullanarak metro ağını modellemekte ve BFS ile A* algoritmalarını uygulayarak optimum rotaları hesaplamaktadır.

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Başlangıç](#-başlangıç)
- [Kullanılan Teknolojiler](#-kullanılan-teknolojiler-ve-kütüphaneler)
- [Metro Ağı Yapısı](#-metro-ağı-yapısı)
- [Algoritmaların Çalışma Mantığı](#-algoritmaların-çalışma-mantığı)
- [Görselleştirme](#-görselleştirme)
- [Örnek Kullanım ve Test Sonuçları](#-örnek-kullanım-ve-test-sonuçları)
- [Projeyi Geliştirme Fikirleri](#-projeyi-geliştirme-fikirleri)

## 🚀 Özellikler

- **Çoklu Hat Desteği**: Kırmızı, Mavi, Turuncu, Yeşil ve Ray hatları ile gerçekçi metro ağı
- **İki Farklı Rota Optimizasyonu**:
  - 🔄 **En Az Aktarmalı Rota**: BFS algoritması ile hesaplanır
  - ⚡ **En Hızlı Rota**: A* algoritması ve Öklid mesafesi heuristiği ile hesaplanır
- **Görselleştirme**: Tkinter ve PIL kütüphaneleri ile metro ağı görselleştirme
- **Kullanıcı Dostu Arayüz**: Hem grafiksel hem de metin tabanlı arayüz seçenekleri
- **Esnek Yapı**: Yeni hatlar ve istasyonlar kolayca eklenebilir

## 🏁 Başlangıç

### Gereksinimler

- Python 3.6 veya üzeri
- (İsteğe bağlı) Tkinter ve PIL kütüphaneleri (görselleştirme için)

### Kurulum

1. Projeyi klonlayın veya indirin
2. Gerekli kütüphaneleri yükleyin (görselleştirme için):
   ```bash
   pip install pillow
   ```
   
### Kullanım

Programı çalıştırmak için:

```bash
python ErtugrulSaritekin_MetroSimulation.py
```

Ana menüden aşağıdaki seçeneklere erişebilirsiniz:
1. Hazır senaryoları göster
2. Kendi rotanı planla
3. Tüm istasyonları listele
4. Metro haritasını göster
5. Çıkış

## 🛠 Kullanılan Teknolojiler ve Kütüphaneler

- **Python**: Projenin ana programlama dili
- **collections.defaultdict**: Varsayılan değerli sözlük yapısı. Hat bilgilerini saklamak için kullanılmıştır.
- **collections.deque**: BFS algoritması için çift uçlu kuyruk yapısı. FIFO (First In First Out) prensibiyle çalışır.
- **heapq**: A* algoritması için öncelik kuyruğu (priority queue). En düşük maliyetli elemanı öncelikli olarak çıkarmak için kullanılır.
- **typing**: Tip belirteçleri (type hints). Kodun okunabilirliğini ve hata ayıklamayı kolaylaştırır.
- **tkinter**: Grafiksel kullanıcı arayüzü (GUI) oluşturmak için kullanılır.
- **PIL (Python Imaging Library)**: Görüntü işleme ve görselleştirme için kullanılır.

## 🗺 Metro Ağı Yapısı

Simülasyon, aşağıdaki metro hatlarını içermektedir:

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  Sincan │─────│   OSB   │─────│Demetevler│─────│  Ulus   │─────│ Kızılay │  Kırmızı Hat
└─────────┘     └─────────┘     └────┬────┘     └─────────┘     └────┬────┘
                                     │                                │
┌─────────┐     ┌─────────┐     ┌────┴────┐     ┌─────────┐     ┌────┴────┐
│ Batıkent│─────│Demetevler│─────│   Gar   │─────│ Keçiören│─────│  Etlik  │  Turuncu Hat
└─────────┘     └─────────┘     └────┬────┘     └─────────┘     └─────────┘
                                     │
┌─────────┐     ┌─────────┐     ┌────┴────┐     ┌─────────┐     ┌─────────┐
│  AŞTİ   │─────│ Kızılay │─────│ Sıhhiye │─────│   Gar   │─────│Dikimevi │  Mavi Hat
└────┬────┘     └─────────┘     └─────────┘     └─────────┘     └─────────┘
     │
┌────┴────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Çayyolu │─────│ Bilkent │─────│Bahçelievl│─────│  Emek   │                Yeşil Hat
└─────────┘     └─────────┘     └─────────┘     └─────────┘

                    ┌─────────┐
                    │  Kuzey  │
                    └────┬────┘
                         │
┌─────────┐        ┌────┴────┐        ┌─────────┐
│  Batı   │────────│  Merkez │────────│  Doğu   │                          Ray Hat
└─────────┘        └────┬────┘        └─────────┘
                         │
                    ┌────┴────┐
                    │  Güney  │
                    └─────────┘
```

### Ray Hat Entegrasyonu

Projeye eklenen Ray Hattı, merkez istasyondan dört yöne (Kuzey, Güney, Doğu, Batı) uzanan bir hat yapısına sahiptir. Bu hat, Kızılay istasyonu üzerinden ana metro ağına bağlanmaktadır. Ray Hattı'nın koordinatları, ray.jpg görüntüsünden alınmıştır ve görselleştirme bileşeni tarafından kullanılmaktadır.

## 🧮 Algoritmaların Çalışma Mantığı

### BFS (Breadth-First Search) Algoritması

BFS algoritması, grafikte bir başlangıç noktasından başlayarak, tüm komşu düğümleri ziyaret eden ve ardından bu komşuların komşularını ziyaret eden bir arama algoritmasıdır. Bu projede, en az aktarmalı rotayı bulmak için kullanılmıştır.

**Çalışma Adımları:**
1. Başlangıç istasyonunu kuyruğa ekle ve ziyaret edildi olarak işaretle
2. Kuyruk boş olana kadar:
   - Kuyruğun başındaki istasyonu ve rotayı al
   - Eğer bu istasyon hedef istasyonsa, rotayı döndür
   - Tüm komşu istasyonları kontrol et:
     - Eğer komşu daha önce ziyaret edilmediyse, yeni rotayı oluştur ve kuyruğa ekle
     - Komşuyu ziyaret edildi olarak işaretle

BFS algoritması, en kısa yolu (düğüm sayısı açısından) garanti eder. Bu nedenle, en az aktarmalı rotayı bulmak için idealdir, çünkü her istasyon bir düğüm olarak temsil edilir ve en az düğüm sayısına sahip yol, en az aktarmalı rotayı verir.

### A* Algoritması

A* algoritması, en kısa yolu bulmak için kullanılan bir arama algoritmasıdır. Dijkstra algoritmasının bir uzantısıdır ve hedef düğüme olan tahmini mesafeyi (sezgisel) kullanarak daha verimli çalışır. Bu projede, en hızlı rotayı bulmak için kullanılmıştır.

**Çalışma Adımları:**
1. Başlangıç istasyonunu öncelik kuyruğuna ekle (f_score = g_score + h_score)
   - g_score: Başlangıçtan şimdiye kadar geçen süre (başlangıçta 0)
   - h_score: Şimdiden hedefe tahmini süre (Öklid mesafesi)
2. Öncelik kuyruğu boş olana kadar:
   - En düşük f_score'a sahip istasyonu ve rotayı al
   - Eğer bu istasyon hedef istasyonsa, rotayı ve toplam süreyi döndür
   - İstasyon daha önce ziyaret edildiyse, atla
   - İstasyonu ziyaret edildi olarak işaretle
   - Tüm komşu istasyonları kontrol et:
     - Yeni rotayı ve g_score'u hesapla (geçen süre)
     - Hat değişimi varsa ek süre ekle (aktarma süresi)
     - h_score'u hesapla (Öklid mesafesi)
     - f_score = g_score + h_score
     - Komşuyu öncelik kuyruğuna ekle (öncelik = f_score)

A* algoritması, en düşük maliyetli yolu garanti eder. Bu projede, maliyet seyahat süresidir ve hat değişimleri için ek süre eklenir. Öklid mesafesi heuristiği, algoritmanın hedef istasyona doğru daha verimli bir şekilde ilerlemesini sağlar. Bu nedenle, en hızlı rotayı bulmak için idealdir.

### Öklid Mesafesi Heuristiği

A* algoritmasında kullanılan Öklid mesafesi heuristiği, iki istasyon arasındaki düz çizgi mesafesini hesaplar:

```python
def oklid_mesafe(self, diger_istasyon: 'Istasyon') -> float:
    """İki istasyon arasındaki Öklid mesafesini hesaplar"""
    return ((self.x - diger_istasyon.x) ** 2 + (self.y - diger_istasyon.y) ** 2) ** 0.5
```

Bu heuristik, algoritmanın hedef istasyona doğru daha verimli bir şekilde ilerlemesini sağlar ve gereksiz yolları araştırmasını önler.

## 🖼 Görselleştirme

Proje, metro ağını görselleştirmek için iki farklı seçenek sunar:

### Grafiksel Görselleştirme

Tkinter ve PIL kütüphaneleri kullanılarak oluşturulan grafiksel arayüz, metro ağını ray.jpg görüntüsü üzerine çizer. Her hat farklı bir renkle gösterilir ve istasyonlar arasındaki bağlantılar çizgilerle belirtilir. Aktarma noktaları kesikli çizgilerle gösterilir.

### Metin Tabanlı Görselleştirme

Tkinter veya PIL kütüphaneleri mevcut değilse, program otomatik olarak metin tabanlı bir görselleştirme sunar. Bu görselleştirme, her hattın istasyonlarını ve koordinatlarını listeler.

## 📊 Örnek Kullanım ve Test Sonuçları

Proje, yedi farklı senaryo için test edilmiştir:

### Senaryo 1: AŞTİ'den OSB'ye

```
En az aktarmalı rota: AŞTİ -> Kızılay -> Kızılay (Kırmızı Hat) -> Ulus -> Demetevler -> OSB
En hızlı rota (27 dakika): AŞTİ -> Kızılay -> Kızılay (Kırmızı Hat) -> Ulus -> Demetevler -> OSB
```

### Senaryo 2: Batıkent'ten Keçiören'e

```
En az aktarmalı rota: Batıkent -> Demetevler -> Gar -> Keçiören
En hızlı rota (21 dakika): Batıkent -> Demetevler -> Gar -> Keçiören
```

### Senaryo 3: Keçiören'den AŞTİ'ye

```
En az aktarmalı rota: Keçiören -> Gar -> Gar (Mavi Hat) -> Sıhhiye -> Kızılay -> AŞTİ
En hızlı rota (21 dakika): Keçiören -> Gar -> Gar (Mavi Hat) -> Sıhhiye -> Kızılay -> AŞTİ
```

### Senaryo 4: Çayyolu'ndan Sincan'a

```
En az aktarmalı rota: Çayyolu -> Bilkent -> AŞTİ -> AŞTİ (Mavi Hat) -> Kızılay -> Kızılay (Kırmızı Hat) -> Ulus -> Demetevler -> OSB -> Sincan
En hızlı rota (49 dakika): Çayyolu -> Bilkent -> AŞTİ -> AŞTİ (Mavi Hat) -> Kızılay -> Kızılay (Kırmızı Hat) -> Ulus -> Demetevler -> OSB -> Sincan
```

### Senaryo 5: Etlik'ten Dikimevi'ne

```
En az aktarmalı rota: Etlik -> Keçiören -> Gar -> Gar (Mavi Hat) -> Dikimevi
En hızlı rota (19 dakika): Etlik -> Keçiören -> Gar -> Gar (Mavi Hat) -> Dikimevi
```

### Senaryo 6: Ray Hattı - Kuzey'den Güney'e

```
En az aktarmalı rota: Kuzey -> Merkez -> Güney
En hızlı rota (8 dakika): Kuzey -> Merkez -> Güney
```

### Senaryo 7: Kızılay'dan Ray Doğu'ya

```
En az aktarmalı rota: Kızılay -> Merkez (Ray Hat) -> Doğu
En hızlı rota (6 dakika): Kızılay -> Merkez (Ray Hat) -> Doğu
```

## 💡 Projeyi Geliştirme Fikirleri

1. **Gerçek Zamanlı Veri Entegrasyonu**: Gerçek metro sistemlerinden alınan verilerle (örneğin, tren gecikmeleri, istasyon yoğunluğu) simülasyonu güncelleyerek daha gerçekçi sonuçlar elde edilebilir.

2. **Çoklu Kriter Optimizasyonu**: Kullanıcıların farklı kriterlere göre rota seçebilmesi sağlanabilir. Örneğin, en hızlı, en az aktarmalı, en az yürüme mesafeli veya bunların bir kombinasyonu.

3. **Mobil Uygulama**: Simülasyonu bir mobil uygulamaya dönüştürerek, kullanıcıların gerçek zamanlı olarak en iyi rotaları bulmasına yardımcı olunabilir.

4. **Daha Büyük ve Karmaşık Metro Ağları**: Daha fazla hat ve istasyon içeren büyük metro ağları eklenerek, algoritmaların performansı test edilebilir ve iyileştirilebilir.

5. **Yolcu Simülasyonu**: Metro ağındaki yolcu hareketlerini simüle ederek, istasyon ve hat yoğunluklarını tahmin etmek ve buna göre rota önerileri sunmak mümkün olabilir.

6. **3D Görselleştirme**: Metro ağını üç boyutlu olarak görselleştirerek, kullanıcıların rotaları daha iyi anlamasına yardımcı olunabilir.

7. **Web Arayüzü**: Projeyi bir web uygulamasına dönüştürerek, kullanıcıların tarayıcı üzerinden erişmesini sağlamak mümkün olabilir.

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasına bakın.

---

**Geliştirici:** Ertuğrul Sarıtekin  
**Versiyon:** 1.0.0  
**Son Güncelleme:** Mart 2025
