# SMS Spam Tespiti Uygulaması

Flask tabanlı bir web uygulaması. Bu uygulama, iPhone arayüzünü simüle ederek SMS mesajlarını spam veya ham (spam olmayan) olarak sınıflandırmak için bir makine öğrenmesi modeli kullanır. Projede veri ön işleme, özellik çıkarımı ve PyCaret kullanılarak model geliştirme adımları da yer almaktadır.

---

## Özellikler

- **Modern iPhone Benzeri Arayüz:**  
  Gerçekçi bir iOS görünümü; durum çubuğu, mesaj listesi ve etkileşimli ögeler.

- **Gerçek Zamanlı SMS Sınıflandırması:**  
  Eğitilmiş makine öğrenmesi modeli (PyCaret kullanılarak geliştirilen) ve TF-IDF vektörleyici ile gelen SMS mesajları anında sınıflandırılır.

- **İnteraktif Mesaj Kontrolü:**  
  Kullanıcı arayüzündeki "New" butonu ile yeni mesajlar alınabilir ve her mesaj anında spam analizi yapılarak gösterilir.

- **Duyarlı Tasarım:**  
  Tüm cihazlarda uyumlu, mobil cihazlara optimize edilmiş ve retina ekranlar için optimize edilmiş tasarım.

  ![image](https://github.com/user-attachments/assets/9cb0f181-f574-47b4-96d8-7246cdbd0025)


---

## Önkoşullar

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

---

## Kurulum

1. **Repoyu Klonlayın:**
   ```bash
   git clone https://github.com/haakanergun/teknasyon_spamguard.git
   cd teknasyon_spamguard
   ```

2. **Sanal Ortam Oluşturun (Önerilir):**
   ```bash
   python -m venv venv
   ```

3. **Sanal Ortamı Aktif Hale Getirin:**
   - Windows:
   ```bash
   venv\Scripts\activate
   ```
   - macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Gerekli Paketleri Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

## Uygulamayı Çalıştırma

1. Sanal ortamın aktif olduğundan emin olun.

2. Flask Uygulamasını Başlatın:
   ```bash
   python run.py
   ```

3. Web Tarayıcınızda Aşağıdaki Adrese Gidin:
   ```
   http://127.0.0.1:5000
   ```
Alternatif Uygulamaya Ulaşım:
  ```
   http://37.148.208.129:5001/
  ```

## Proje Yapısı

```
.
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│       └── index.html
├── models/
│   ├── final_pycaret_model.pkl
│   └── tfidf_vectorizer.pkl
├── datasets/
│   └── sms_spam_train.csv
├── notebooks/
│   └── tfidf_classification.ipynb
│   └── gpt.ipynb
├── outputs/
│   └── tfidf_classification.html
├── assets/
│   └── screenshots/
├── logs.log
├── requirements.txt
├── README.md
└── run.py
```

### Klasör Yapısı Açıklamaları

- **`app/`**: Flask uygulamasının ana dizini
  - `routes/`: API endpoint'leri ve route tanımlamaları
  - `static/`: CSS, JavaScript ve diğer statik dosyalar
  - `templates/`: HTML şablonları

- **`models/`**: Eğitilmiş model ve vektörleyici dosyaları
  - `final_pycaret_model.pkl`: PyCaret ile eğitilmiş sınıflandırma modeli
  - `tfidf_vectorizer.pkl`: Eğitilmiş TF-IDF vektörleyici

- **`datasets/`**: Ham ve işlenmiş veri setleri
  - `sms_spam_train.csv`: SMS spam veri seti

- **`notebooks/`**: Jupyter notebook'ları
  - `tfidf_classification.ipynb`: TF-IDF ve sınıflandırma model geliştirme notebook'u

- **`outputs/`**: Model çıktıları ve raporlar
  - `tfidf_classification.html`: Model geliştirme ve analiz raporu

- **Kök Dizindeki Dosyalar**:
  - `run.py`: Uygulamayı başlatan ana script
  - `requirements.txt`: Proje bağımlılıkları
  - `logs.log`: Uygulama log dosyası
  - `README.md`: Proje dökümantasyonu

## Uygulama Nasıl Çalışır?

### Model ve Vektörleyici Yükleme:
- Uygulama başlatıldığında, önceden eğitilmiş PyCaret sınıflandırma modeli ve TF-IDF vektörleyici yüklenir.

### SMS Mesaj İşleme:
- Kullanıcı "New" butonuna tıkladığında, uygulama rastgele bir SMS mesajı seçer.
- Seçilen mesaj, ön işleme tabi tutulur, TF-IDF ile özelliklere dönüştürülür ve model tarafından anında spam veya ham olarak sınıflandırılır.
- Sınıflandırma sonucu hemen kullanıcıya gösterilir.

### Gösterim:
- Sınıflandırma sonucu, iPhone benzeri arayüzde gösterilir:
  - Normal mesajlar standart görünümde
  - Spam mesajlar kırmızı arka plan ve uyarı simgesi (⚠️) ile vurgulanır
  - Her mesajın üstünde gönderici bilgisi ve zaman gösterilir

## Model Geliştirme & Veri Ön İşleme

### Veri Ön İşleme ve Keşifsel Veri Analizi (EDA)

#### Keşifsel Veri Analizi (EDA):
- sms_spam_train.csv veri seti yüklendi; veri boyutu, eksik değerler ve temel istatistikler incelendi.
- Spam ve ham etiket dağılımı bar grafikleri ile görselleştirildi.
- Mesaj uzunluğu ve kelime sayısı histogramları ve KDE kullanılarak analiz edildi.
- Spam ve ham mesajlar için WordCloud'lar oluşturuldu; böylece yaygın kelimeler tespit edildi.
- Her iki sınıfta da en sık geçen kelimeler analiz edilerek, özellik mühendisliği için yönlendirici bilgiler elde edildi.

#### Metin Ön İşleme:
- Metinler küçük harfe çevrildi.
- Özel karakterler ve gereksiz boşluklar temizlendi; Türkçe karakterler korunarak düzenlendi.
- Tokenizasyon gerçekleştirildi ve hem İngilizce hem Türkçe stop-word'ler kaldırıldı.
- (Opsiyonel) Stemming veya lemmatization adımları uygulandı.

### Özellik Çıkarımı

#### TF-IDF Vektörleştirme:
- Ön işlenmiş metin verisi, TF-IDF yöntemi kullanılarak sayısal özelliklere dönüştürüldü.
- Özellik alanı gürültüyü azaltmak amacıyla sınırlandırıldı (örneğin, max_features=5000).
- TF-IDF vektörleyici tfidf_vectorizer.pkl dosyası olarak kaydedildi.

### Model Eğitimi ve Tuning

#### PyCaret ile Model Geliştirme:
- setup fonksiyonu kullanılarak deney ortamı oluşturuldu ve veri seti üzerinde farklı modeller karşılaştırıldı (compare_models).
- En iyi performans gösteren model seçildi ve create_model, tune_model kullanılarak hiperparametre optimizasyonu yapıldı.
- Son model oluşturuldu ve final_pycaret_model.pkl olarak kaydedildi.

### GPT Fine-Tuning ile Model Geliştirme
- OpenAI’nin GPT fine-tuning yöntemi kullanılarak, SMS spam tespiti görevine özel bir model eğitildi.
- Eğitim verisi, chat formatında (system, user, assistant mesajları) JSONL formatına dönüştürüldü.
- JSONL dosyası OpenAI API kullanılarak yüklendi; fine-tuning işine başlandı.
- Fine-tuning işinde, hiperparametreler (örn. n_epochs=1, batch_size=2) ayarlanarak yaklaşık 50 adımda eğitim gerçekleştirildi.
- Elde edilen GPT fine-tuned model, SMS mesajlarının sınıflandırılmasında kullanılmaktadır.

## Backend Geliştirme Detayları

### Flask Uygulama Yapısı:
- Uygulama, modülerlik için application factory pattern kullanılarak geliştirildi.
- Blueprint'ler aracılığıyla farklı rotalar organize edildi.
- Hata yönetimi ve loglama mekanizmaları eklendi.

### API Endpoint'leri:
- `/`: Ana sayfa render edilir.
- `/get_message`: Rastgele SMS mesajı seçip, model ile spam/ham sınıflandırması yaparak JSON formatında sonuç döndürür.

### Model Entegrasyonu:
- Uygulama başlatıldığında, PyCaret modeli ve TF-IDF vektörleyici yüklenir.
- Gelen SMS mesajları ön işleme tabi tutulur ve vektörleştirilerek model tarafından sınıflandırılır.

## Frontend Geliştirme Detayları

### iPhone Benzeri Arayüz:
- iOS tasarım prensiplerine uygun, gerçekçi bir arayüz oluşturuldu.
- SF Pro Text fontu kullanılarak modern bir görünüm sağlandı.
- Durum çubuğunda saat, sinyal göstergesi, operatör adı (TeknasyonCell) ve pil seviyesi bulunur.
- Üst kısımda "New" butonu ile yeni mesaj alma kontrolü sağlanır.

### Mesaj Listesi:
- iOS Messages uygulaması tarzında, kaydırılabilir mesaj listesi oluşturuldu.
- Her mesaj; renkli avatar, gönderici ismi, mesaj önizlemesi, gönderim zamanı ve detay için sağ ok simgesi içerir.

### Spam Mesaj Gösterimi:
- Spam mesajlar, kırmızı arka plan, uyarı simgesi (⚠️) ve "Olası spam mesajı" etiketi ile görsel olarak vurgulanır.

### Etkileşimler ve Animasyonlar:
- Yeni gelen mesajlar yumuşak geçiş animasyonları ile ekranda belirir.
- Dokunma geri bildirimleri ve yumuşak geçiş efektleri sağlanır.
- Responsive ve retina ekranlara uyumlu tasarım ile tüm cihazlarda modern iOS görünümü elde edilir.

## Geliştirme

### Modüler Kod Organizasyonu:
Uygulama, temiz kod prensiplerine uygun, modüler yapı ve açıklayıcı kod yorumlarıyla geliştirildi.

### Performans İyileştirmeleri:
Önbellekleme, lazy loading ve optimize edilmiş animasyonlar kullanılarak uygulamanın performansı artırıldı.
