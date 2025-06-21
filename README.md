 🎭 Tiyatro Asistanı Chatbotu

Bu proje, tiyatro kursları sırasında öğrencilerin ya da eğitmenlerin ellerindeki oyuncu yapısına, mekana, türe ve yazara göre uygun tiyatro oyunlarını bulmalarına yardımcı olan bir yapay zekâ destekli asistandır.

 🚀 Amaç

Tiyatro eğitimi sırasında öğrencilerin sahneleyeceği oyunları seçmek, çoğu zaman mevcut oyuncu kadrosuna, sahne ortamına veya tür tercihlerine göre yapılır. Bu noktada, elimizdeki veri setine dayalı olarak sorulara yanıt verebilen bir **RAG tabanlı (Retrieval-Augmented Generation)** tiyatro asistanı oluşturulmuştur.

 Projenin temel amacı:

* Oyuncu sayısı ve cinsiyete göre uygun oyun önermek
* Belirli bir yazarın yazdığı oyunları listelemek
* Belirli bir yıl ya da mekanla ilgili oyunları sorgulamak
* Selamlaşma ve vedalaşma gibi küçük etkileşimleri tanıyabilmek

🧠 Kullanılan Teknolojiler

* **Python**
* **Streamlit** – Web arayüzü için
* **LangChain** – LLM entegrasyonu ve RAG zinciri
* **Gemini 1.5 Pro (Google GenAI)** – LLM altyapısı
* **Chroma** – Vektör veritabanı olarak
* **.env + dotenv** – API anahtar yönetimi
* **GoogleGenerativeAIEmbeddings** – Embed işlemleri

📁 Dosya Yapısı

```
.
├── app.py                       # Ana uygulama kodu
├── Tiyatro_Oyunlari_Dataset.xlsx  # Oyun bilgilerini içeren veri seti
├── .env                         # GOOGLE_API_KEY içeren dosya
├── chroma_db/                  # Embedlenmiş veri kümesinin kayıtlı olduğu dizin
```

🔧 Kod Yapısına Genel Bakış

`app.py` dosyası Streamlit uygulamasını başlatır. Ana adımlar:

1. **Veri Yükleme**: Excel dosyasındaki tiyatro oyunları okunur ve her satır bir LangChain `Document` nesnesine dönüştürülür.
2. **Vektörleştirme**: Oyun bilgilerinden oluşan belgeler Google GenAI Embed modeliyle embedlenir ve Chroma veritabanına kaydedilir.
3. **Retriever Tanımı**: Benzer belgeleri bulabilmek için Chroma retriever ayarlanır.
4. **LLM Bağlantısı**: Gemini 1.5 Pro modeli kullanılır.
5. **Intent Sınıflandırma**: Kullanıcının sorduğu cümleye uygun intent belirlenir.
6. **RAG Zinciri**: Eğer intent anlamlıysa (yazar sorgusu, oyun önerisi vs.) özet bilgileriyle birlikte cevap üretilir.
7. **UI**: Kullanıcı sorusunu girer, intent tanınır ve cevap görüntülenir.

📊 Veri Seti Formatı

| Oyun Adı | Yazar | Yıl | Mekan | Tür | Özet | Kaç Kişilik | Roller Özeti | Roller Detayı |
| -------- | ----- | --- | ----- | --- | ---- | ----------- | ------------ | ------------- |

Örnek Satır:

```
Kürk Mantolu Madonna | Sabahattin Ali (Uyarlayan: Engin Alkan) | 2013 - Uyarlama | 1930’lar Berlin ve Ankara | Dram / Romantik | Maria Puder ve Raif Efendi’nin içsel yalnızlıkları... | 5 | 2 kadın + 3 erkek | Raif Efendi, Maria Puder, Anlatıcı, Babası, Büro Müdürü
```

🔍 Örnek Sorgular

* `Dram türünde iki kişilik bir oyun önerir misin?`
* `1980 yılında yazılmış oyunlar hangileri?`
* `Ormanda geçen bir oyun var mı?`
* `Raif Efendi karakterinin yer aldığı oyun hangisidir?`
* `Merhaba` → Selamlaşma cevabı verir

⚙️ Kurulum

1. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

2. `.env` dosyası oluşturun ve şu satırı ekleyin:

```
GOOGLE_API_KEY=your_api_key_here
```

3. Uygulamayı başlatın:

```bash
streamlit run app.py
```

👩‍🏫 Neden Bu Proje?

Tiyatro kursu alırken elimizdeki oyunculara uygun oyun bulmakta zorlandık. Bu ihtiyacı çözmek için, sorulara doğal dille cevap verebilecek bir tiyatro danışmanı bot geliştirdik. Bu bot sayesinde:

* Oyuncu sayısı ve türü dikkate alınarak öneriler yapılabilir.
* Özelleştirilmiş filtrelemelerle arama deneyimi sağlanır.
* Öğrenciler, sahneleyecekleri oyunu daha kolay seçebilir.

![Ekran görüntüsü 2025-06-21 143245](https://github.com/user-attachments/assets/32d5fee3-422e-49a4-9cfb-e1861482cf6c)


