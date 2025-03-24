from collections import defaultdict, deque
import heapq
import os
from typing import Dict, List, Set, Tuple, Optional

# Tkinter ve PIL kütüphanelerini isteğe bağlı olarak içe aktar
try:
    import tkinter as tk
    from tkinter import Canvas, Label, Button, Frame, Toplevel
    from PIL import Image, ImageTk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print("Not: Tkinter veya PIL kütüphanesi bulunamadı. Görselleştirme devre dışı.")
    print("Metin tabanlı arayüz kullanılacak.")

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str, x: float = 0, y: float = 0):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları
        self.x = x  # x koordinatı (A* algoritması için)
        self.y = y  # y koordinatı (A* algoritması için)

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))
        
    def oklid_mesafe(self, diger_istasyon: 'Istasyon') -> float:
        """İki istasyon arasındaki Öklid mesafesini hesaplar"""
        return ((self.x - diger_istasyon.x) ** 2 + (self.y - diger_istasyon.y) ** 2) ** 0.5

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str, x: float = 0, y: float = 0) -> None:
        if idx not in self.istasyonlar:  # Fixed 'id' to 'idx'
            istasyon = Istasyon(idx, ad, hat, x, y)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """BFS algoritması kullanarak en az aktarmalı rotayı bulur
        
        Bu fonksiyonu tamamlayın:
        1. Başlangıç ve hedef istasyonların varlığını kontrol edin
        2. BFS algoritmasını kullanarak en az aktarmalı rotayı bulun
        3. Rota bulunamazsa None, bulunursa istasyon listesi döndürün
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        # BFS algoritması için kuyruk oluşturma
        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi = {baslangic}
        
        while kuyruk:
            # Kuyruğun başındaki istasyonu ve rotayı al
            guncel_istasyon, rota = kuyruk.popleft()
            
            # Hedef istasyona ulaşıldıysa rotayı döndür
            if guncel_istasyon == hedef:
                return rota
            
            # Komşu istasyonları keşfet
            for komsu, _ in guncel_istasyon.komsular:
                if komsu not in ziyaret_edildi:
                    # Yeni rotayı oluştur ve kuyruğa ekle
                    yeni_rota = rota + [komsu]
                    kuyruk.append((komsu, yeni_rota))
                    ziyaret_edildi.add(komsu)
        
        # Rota bulunamadıysa None döndür
        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritması kullanarak en hızlı rotayı bulur
        
        Bu fonksiyonu tamamlayın:
        1. Başlangıç ve hedef istasyonların varlığını kontrol edin
        2. A* algoritmasını kullanarak en hızlı rotayı bulun
        3. Rota bulunamazsa None, bulunursa (istasyon_listesi, toplam_sure) tuple'ı döndürün
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        # A* algoritması için öncelik kuyruğu oluşturma
        # (f_score, istasyon_id, istasyon, rota, g_score)
        # f_score = g_score (gerçek maliyet) + h_score (tahmini maliyet)
        # g_score = başlangıçtan şimdiye kadar geçen süre
        # h_score = şimdiden hedefe tahmini süre (Öklid mesafesi)
        
        # Başlangıç düğümü için f_score = 0 + h_score
        h_score = baslangic.oklid_mesafe(hedef)
        pq = [(h_score, id(baslangic), baslangic, [baslangic], 0)]
        ziyaret_edildi = set()
        
        while pq:
            # En düşük f_score'a sahip rotayı al
            _, _, guncel_istasyon, rota, g_score = heapq.heappop(pq)
            
            # Hedef istasyona ulaşıldıysa rotayı ve toplam süreyi döndür
            if guncel_istasyon == hedef:
                return (rota, g_score)
            
            # İstasyon daha önce ziyaret edildiyse atla
            istasyon_id = id(guncel_istasyon)
            if istasyon_id in ziyaret_edildi:
                continue
            
            ziyaret_edildi.add(istasyon_id)
            
            # Komşu istasyonları keşfet
            for komsu, sure in guncel_istasyon.komsular:
                if id(komsu) not in ziyaret_edildi:
                    # Yeni rotayı ve g_score'u hesapla
                    yeni_rota = rota + [komsu]
                    yeni_g_score = g_score + sure
                    
                    # Hat değişimi varsa ek süre ekle (aktarma süresi)
                    if len(rota) > 0 and rota[-1].hat != komsu.hat:
                        # Aktarma süresi olarak 2 dakika ekleyelim
                        yeni_g_score += 2
                    
                    # Heuristik (h_score) hesapla - Öklid mesafesi
                    h_score = komsu.oklid_mesafe(hedef)
                    
                    # f_score = g_score + h_score
                    f_score = yeni_g_score + h_score
                    
                    # Öncelik kuyruğuna ekle
                    heapq.heappush(pq, (f_score, id(komsu), komsu, yeni_rota, yeni_g_score))
        
        # Rota bulunamadıysa None döndür
        return None

# Rota formatını iyileştiren yardımcı fonksiyon
def rota_formatla(rota):
    formatted_rota = []
    prev_hat = None
    
    for istasyon in rota:
        if prev_hat and istasyon.hat != prev_hat:
            formatted_rota.append(f"{istasyon.ad} ({istasyon.hat})")
        else:
            formatted_rota.append(istasyon.ad)
        prev_hat = istasyon.hat
        
    return " -> ".join(formatted_rota)

    # Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme (x, y koordinatları ile)
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat", 50, 50)
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat", 40, 60)
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat", 30, 70)
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat", 20, 80)
    metro.istasyon_ekle("K5", "Sincan", "Kırmızı Hat", 10, 90)
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat", 60, 40)
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat", 50, 50)  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat", 60, 60)
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat", 70, 70)
    metro.istasyon_ekle("M5", "Dikimevi", "Mavi Hat", 80, 60)
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat", 10, 60)
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat", 30, 70)  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat", 70, 70)  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat", 80, 80)
    metro.istasyon_ekle("T5", "Etlik", "Turuncu Hat", 90, 90)
    
    # Yeşil Hat (Yeni hat)
    metro.istasyon_ekle("Y1", "Çayyolu", "Yeşil Hat", 40, 20)
    metro.istasyon_ekle("Y2", "Bilkent", "Yeşil Hat", 50, 30)
    metro.istasyon_ekle("Y3", "AŞTİ", "Yeşil Hat", 60, 40)  # Aktarma noktası
    metro.istasyon_ekle("Y4", "Bahçelievler", "Yeşil Hat", 70, 50)
    metro.istasyon_ekle("Y5", "Emek", "Yeşil Hat", 80, 40)
    
    # Ray Hattı (ray.jpg'den)
    metro.istasyon_ekle("R1", "Merkez", "Ray Hat", 45, 45)
    metro.istasyon_ekle("R2", "Doğu", "Ray Hat", 65, 45)
    metro.istasyon_ekle("R3", "Kuzey", "Ray Hat", 45, 25)
    metro.istasyon_ekle("R4", "Batı", "Ray Hat", 25, 45)
    metro.istasyon_ekle("R5", "Güney", "Ray Hat", 45, 65)
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    metro.baglanti_ekle("K4", "K5", 7)  # OSB -> Sincan
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    metro.baglanti_ekle("M4", "M5", 6)  # Gar -> Dikimevi
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    metro.baglanti_ekle("T4", "T5", 4)  # Keçiören -> Etlik
    
    # Yeşil Hat bağlantıları
    metro.baglanti_ekle("Y1", "Y2", 6)  # Çayyolu -> Bilkent
    metro.baglanti_ekle("Y2", "Y3", 5)  # Bilkent -> AŞTİ
    metro.baglanti_ekle("Y3", "Y4", 4)  # AŞTİ -> Bahçelievler
    metro.baglanti_ekle("Y4", "Y5", 5)  # Bahçelievler -> Emek
    
    # Ray Hat bağlantıları
    metro.baglanti_ekle("R1", "R2", 3)  # Merkez -> Doğu
    metro.baglanti_ekle("R1", "R3", 4)  # Merkez -> Kuzey
    metro.baglanti_ekle("R1", "R4", 3)  # Merkez -> Batı
    metro.baglanti_ekle("R1", "R5", 4)  # Merkez -> Güney
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    metro.baglanti_ekle("M1", "Y3", 2)  # AŞTİ aktarma
    metro.baglanti_ekle("K1", "R1", 3)  # Kızılay -> Ray Merkez aktarma
    
    def metro_haritasi_goster():
        """Metro haritasını görselleştiren fonksiyon"""
        if not TKINTER_AVAILABLE:
            print("\nGörselleştirme kullanılamıyor. Tkinter veya PIL kütüphanesi yüklü değil.")
            print("Metin tabanlı harita gösteriliyor:\n")
            
            # Basit bir metin tabanlı harita göster
            for hat_adi in sorted(metro.hatlar.keys()):
                print(f"\n{hat_adi} İstasyonları:")
                for istasyon in sorted(metro.hatlar[hat_adi], key=lambda x: x.ad):
                    print(f"  {istasyon.ad} ({istasyon.idx}): Koordinatlar ({istasyon.x}, {istasyon.y})")
            
            # Algoritma açıklamaları
            print("\nKullanılan Algoritmalar:")
            print("- BFS Algoritması: En az aktarmalı rotayı bulmak için kullanılır.")
            print("- A* Algoritması: En hızlı rotayı bulmak için kullanılır. Öklid mesafesi heuristiği kullanır.")
            return
            
        try:
            # Tkinter penceresi oluştur
            root = tk.Tk()
            root.title("Ankara Metro Haritası")
            root.geometry("1000x800")
            
            # Ana frame
            main_frame = Frame(root)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Harita frame'i
            map_frame = Frame(main_frame)
            map_frame.pack(fill=tk.BOTH, expand=True)
            
            # Canvas oluştur
            canvas = Canvas(map_frame, bg="white")
            canvas.pack(fill=tk.BOTH, expand=True)
            
            # ray.jpg dosyasını yükle
            try:
                img = Image.open("ray.jpg")
                # Resmi canvas boyutuna uygun şekilde yeniden boyutlandır
                img = img.resize((900, 600), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Resmi canvas'a yerleştir
                canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                canvas.image = photo  # Referansı tut
                
                # Hat renklerini tanımla
                hat_renkleri = {
                    "Kırmızı Hat": "red",
                    "Mavi Hat": "blue",
                    "Turuncu Hat": "orange",
                    "Yeşil Hat": "green",
                    "Ray Hat": "purple"
                }
                
                # İstasyonları çiz
                istasyon_boyutu = 10
                for hat_adi, renk in hat_renkleri.items():
                    if hat_adi in metro.hatlar:
                        istasyonlar = metro.hatlar[hat_adi]
                        
                        # Önceki istasyonu takip et (hat çizgisi çizmek için)
                        onceki_istasyon = None
                        
                        for istasyon in istasyonlar:
                            # İstasyon koordinatlarını ölçekle
                            x = istasyon.x * 9  # Canvas'a uygun ölçekleme
                            y = istasyon.y * 6  # Canvas'a uygun ölçekleme
                            
                            # İstasyonu çiz
                            canvas.create_oval(x-istasyon_boyutu, y-istasyon_boyutu, 
                                              x+istasyon_boyutu, y+istasyon_boyutu, 
                                              fill=renk, outline="black")
                            
                            # İstasyon adını yaz
                            canvas.create_text(x, y+15, text=istasyon.ad, fill="black", 
                                              font=("Arial", 8, "bold"))
                            
                            # Hat çizgisini çiz
                            if onceki_istasyon:
                                onceki_x = onceki_istasyon.x * 9
                                onceki_y = onceki_istasyon.y * 6
                                canvas.create_line(onceki_x, onceki_y, x, y, 
                                                 fill=renk, width=3)
                            
                            onceki_istasyon = istasyon
                
                # Aktarma noktalarını belirt
                for istasyon_id1, istasyon_id2 in [("K1", "M2"), ("K3", "T2"), 
                                                  ("M4", "T3"), ("M1", "Y3"),
                                                  ("K1", "R1")]:
                    istasyon1 = metro.istasyonlar[istasyon_id1]
                    istasyon2 = metro.istasyonlar[istasyon_id2]
                    
                    x1, y1 = istasyon1.x * 9, istasyon1.y * 6
                    x2, y2 = istasyon2.x * 9, istasyon2.y * 6
                    
                    # Aktarma çizgisini çiz (kesikli çizgi)
                    canvas.create_line(x1, y1, x2, y2, dash=(4, 2), fill="black", width=1)
                
                # Açıklama bölümü
                legend_frame = Frame(main_frame)
                legend_frame.pack(fill=tk.X, pady=10)
                
                # Hat açıklamaları
                for i, (hat_adi, renk) in enumerate(hat_renkleri.items()):
                    legend_label = Label(legend_frame, text=hat_adi, fg=renk, 
                                        font=("Arial", 10, "bold"))
                    legend_label.grid(row=0, column=i, padx=10)
                
                # Algoritma açıklamaları
                algo_frame = Frame(main_frame)
                algo_frame.pack(fill=tk.X, pady=5)
                
                bfs_label = Label(algo_frame, 
                                 text="BFS Algoritması: En az aktarmalı rotayı bulmak için kullanılır.",
                                 font=("Arial", 10))
                bfs_label.pack(anchor=tk.W)
                
                astar_label = Label(algo_frame, 
                                   text="A* Algoritması: En hızlı rotayı bulmak için kullanılır. Öklid mesafesi heuristiği kullanır.",
                                   font=("Arial", 10))
                astar_label.pack(anchor=tk.W)
                
                # Kapatma butonu
                close_button = Button(main_frame, text="Kapat", command=root.destroy)
                close_button.pack(pady=10)
                
                root.mainloop()
                
            except Exception as e:
                print(f"Resim yüklenirken hata oluştu: {e}")
                print("ray.jpg dosyası mevcut değil veya okunamıyor.")
                print("Harita görselleştirme olmadan devam ediliyor...")
                
                # Basit bir metin tabanlı harita göster
                for hat_adi in sorted(metro.hatlar.keys()):
                    print(f"\n{hat_adi} İstasyonları:")
                    for istasyon in sorted(metro.hatlar[hat_adi], key=lambda x: x.ad):
                        print(f"  {istasyon.ad} ({istasyon.idx}): Koordinatlar ({istasyon.x}, {istasyon.y})")
                
        except Exception as e:
            print(f"Görselleştirme sırasında hata oluştu: {e}")
            print("Tkinter veya PIL kütüphanesi yüklü olmayabilir.")
    
    def kullanici_arayuzu():
        while True:
            print("\n=== Ankara Metro Rota Planlayıcısı ===")
            print("1. Hazır senaryoları göster")
            print("2. Kendi rotanı planla")
            print("3. Tüm istasyonları listele")
            print("4. Metro haritasını göster")
            print("5. Çıkış")
            
            secim = input("\nSeçiminiz (1-5): ")
            
            if secim == "1":
                hazir_senaryolar()
            elif secim == "2":
                kendi_rotani_planla()
            elif secim == "3":
                tum_istasyonlari_listele()
            elif secim == "4":
                metro_haritasi_goster()
            elif secim == "5":
                print("Programdan çıkılıyor...")
                break
            else:
                print("Geçersiz seçim! Lütfen 1-5 arasında bir sayı girin.")
    
    def hazir_senaryolar():
        print("\n=== Hazır Senaryolar ===")
        
        # Senaryo 1: AŞTİ'den OSB'ye
        print("\n1. AŞTİ'den OSB'ye:")
        rota = metro.en_az_aktarma_bul("M1", "K4")
        if rota:
            print("En az aktarmalı rota:", rota_formatla(rota))
        
        sonuc = metro.en_hizli_rota_bul("M1", "K4")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika):", rota_formatla(rota))
        
        # Senaryo 2: Batıkent'ten Keçiören'e
        print("\n2. Batıkent'ten Keçiören'e:")
        rota = metro.en_az_aktarma_bul("T1", "T4")
        if rota:
            print("En az aktarmalı rota:", rota_formatla(rota))
        
        sonuc = metro.en_hizli_rota_bul("T1", "T4")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika):", rota_formatla(rota))
        
        # Senaryo 3: Keçiören'den AŞTİ'ye
        print("\n3. Keçiören'den AŞTİ'ye:")
        rota = metro.en_az_aktarma_bul("T4", "M1")
        if rota:
            print("En az aktarmalı rota:", rota_formatla(rota))
        
        sonuc = metro.en_hizli_rota_bul("T4", "M1")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika):", rota_formatla(rota))
        
        # Senaryo 4: Çayyolu'ndan Sincan'a
        print("\n4. Çayyolu'ndan Sincan'a:")
        rota = metro.en_az_aktarma_bul("Y1", "K5")
        if rota:
            print("En az aktarmalı rota:", rota_formatla(rota))
        
        sonuc = metro.en_hizli_rota_bul("Y1", "K5")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika):", rota_formatla(rota))
        
        # Senaryo 5: Etlik'ten Dikimevi'ne
        print("\n5. Etlik'ten Dikimevi'ne:")
        rota = metro.en_az_aktarma_bul("T5", "M5")
        if rota:
            print("En az aktarmalı rota:", rota_formatla(rota))
        
        sonuc = metro.en_hizli_rota_bul("T5", "M5")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika):", rota_formatla(rota))
            
        # Senaryo 6: Ray Hattı - Kuzey'den Güney'e
        print("\n6. Ray Hattı - Kuzey'den Güney'e:")
        rota = metro.en_az_aktarma_bul("R3", "R5")
        if rota:
            print("En az aktarmalı rota:", rota_formatla(rota))
        
        sonuc = metro.en_hizli_rota_bul("R3", "R5")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika):", rota_formatla(rota))
            
        # Senaryo 7: Kızılay'dan Ray Doğu'ya
        print("\n7. Kızılay'dan Ray Doğu'ya:")
        rota = metro.en_az_aktarma_bul("K1", "R2")
        if rota:
            print("En az aktarmalı rota:", rota_formatla(rota))
        
        sonuc = metro.en_hizli_rota_bul("K1", "R2")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika):", rota_formatla(rota))
    
    def tum_istasyonlari_listele():
        print("\n=== Tüm İstasyonlar ===")
        
        # Hatları alfabetik sırala
        hatlar = sorted(metro.hatlar.keys())
        
        for hat in hatlar:
            print(f"\n{hat}:")
            # İstasyonları alfabetik sırala
            istasyonlar = sorted(metro.hatlar[hat], key=lambda x: x.ad)
            for istasyon in istasyonlar:
                print(f"  {istasyon.idx}: {istasyon.ad}")
    
    def kendi_rotani_planla():
        print("\n=== Kendi Rotanı Planla ===")
        
        # Tüm istasyonları listele
        tum_istasyonlari_listele()
        
        # Başlangıç istasyonu seçimi
        baslangic_id = input("\nBaşlangıç istasyonu ID'si (örn. K1, M2): ")
        if baslangic_id not in metro.istasyonlar:
            print("Geçersiz istasyon ID'si!")
            return
        
        # Hedef istasyonu seçimi
        hedef_id = input("Hedef istasyon ID'si (örn. K1, M2): ")
        if hedef_id not in metro.istasyonlar:
            print("Geçersiz istasyon ID'si!")
            return
        
        if baslangic_id == hedef_id:
            print("Başlangıç ve hedef istasyonları aynı olamaz!")
            return
        
        # En az aktarmalı rotayı bul
        print(f"\n{metro.istasyonlar[baslangic_id].ad}'dan {metro.istasyonlar[hedef_id].ad}'a:")
        rota = metro.en_az_aktarma_bul(baslangic_id, hedef_id)
        if rota:
            print("En az aktarmalı rota:", rota_formatla(rota))
        else:
            print("En az aktarmalı rota bulunamadı!")
        
        # En hızlı rotayı bul
        sonuc = metro.en_hizli_rota_bul(baslangic_id, hedef_id)
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika):", rota_formatla(rota))
        else:
            print("En hızlı rota bulunamadı!")
    
    # Kullanıcı arayüzünü başlat
    kullanici_arayuzu()
