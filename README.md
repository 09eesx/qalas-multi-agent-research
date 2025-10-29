
# 🧠 QALAS Research Workflow

### Automated Multi-Agent Workflow for Quantitative MRI Literature Analysis  
**Author:** Esma  
**Tech Stack:** Python · Agno · Azure OpenAI (GPT-5-mini) · PubMed API · Arxiv API  

---

## 🚀 Overview

**QALAS Research Workflow**, **kantitatif MRI (qMRI)** ve **QALAS** (Quantitative Assessment of relaxation times) üzerine bilimsel makaleleri araştıran, sentezleyen ve analiz eden otomatik bir **çoklu ajanlı akıl yürütme sistemidir**.

**PubMed** ve **Arxiv**'e bağlanır, en alakalı teknik ve klinik çalışmaları alır ve metodolojik ve klinik içgörülerle tamamlanmış, **uzman düzeyinde, Türkçe sentezler** üretir.

---

## 🧩 System Architecture

```mermaid
flowchart LR
A[User Query] --> B{Source Selector}
B -->|PubMed| C[PubMed Agent]
B -->|Arxiv| D[Arxiv Agent]
C --> E[QALAS Analysis Agent]
D --> E
E --> F[Expert Turkish Summary]
````

### Components

| Module                   | Description                                                                                                                                          |
| :----------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`PubMedQALASAgent`**   | PubMed API aracılığıyla QALAS / qMRI ile ilgili yayınları getirir ve yapılandırılmış sentez (klinik, tekrarlanabilirlik, validasyon) gerçekleştirir. |
| **`ArxivQALASAgent`**    | Arxiv'den ön baskıları (preprints) ve derin öğrenme tabanlı MRI yöntemlerini (SSL, Wave-CAIPI, Zero-DeepSub, vb.) alır.                              |
| **`QALASAnalysisAgent`** | Her iki kaynağı birleştirir, sorgu niyetini yorumlar ve soruya uyarlanmış **akademik Türkçe bir analiz** oluşturur.                                  |
| **`Source Selector`**    | Sorguya göre hangi ajanların etkinleştirileceğini belirler (örneğin, “validasyon” → PubMed, “zero-shot” → Arxiv).                                    |
| **`Workflow Engine`**    | Agno’nun `Workflow`, `Condition` ve `Step` mantığını kullanarak ajanları orkestre eder ve çıktıları birleştirir.                                     |

---

## 🧠 Reasoning Logic

Her ajan, yapılandırılmış yansıtma ve adaptif sentez sağlamak için **`reasoning=True`** ile çalışır.

| Reasoning Flag                    | Function                                                       |
| :-------------------------------- | :------------------------------------------------------------- |
| `reasoning=True`                  | Sığ özetleme yerine derin bağlamsal çıkarım sağlar.            |
| `markdown=True`                   | Yayınlamaya hazır **Markdown çıktısı** döndürür.               |
| `tools=[PubmedTools, ArxivTools]` | Her ajana API'leri özerk bir şekilde sorgulama yeteneği verir. |

---

## 🧬 Prompt Design

Her ajanın kendi **alan optimize edilmiş komut istemi (prompt)** vardır:

### 🧩 `qalas_pub_prompt`

* **Odak:** Klinik, validasyon ve tekrarlanabilirlik çalışmaları
* **Bölümler:**

  1. Araştırma Bağlamı ve Amacı
  2. Kullanılan Yöntem
  3. Bulgular ve Çıkarımlar
  4. Klinik Etkiler
  5. Gelecek Yönelimler

### 🧩 `arxiv_agent_prompt`

* **Odak:** Teknik, derin öğrenme ve rekonstrüksiyon modelleri
* **Bölümler:**

  1. Problem Tanımı
  2. Önerilen Yöntem
  3. Deneysel Kurulum
  4. Bulgular
  5. Analiz ve Gelecek Yönelimler

### 🧩 `qalas_analysis_prompt`

* **Odak:** Sorgu türüne (karşılaştırma, mekanizma, validasyon, yapay zeka yöntemi veya klinik etki) uyarlanabilen **Türkçe nihai sentez**.

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<yourusername>/qalas-multi-agent-research.git
cd qalas-multi-agent-research
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set up environment variables

Proje kök dizininde bir `.env` dosyası oluşturun:

```bash
OPENAI_API_KEY=your_azure_openai_key_here
```

---

## 🧪 Usage

İş akışını etkileşimli olarak çalıştırın:

```bash
python main.py
```

İstendiğinde:

```
Araştırma konusu: 3D-QALAS reproducibility in neuroimaging
```

### Example Output:

```
=== QALAS RESEARCH RESULT ===

### QALAS Sekanslarının Tekrarlanabilirliği Üzerine Bir Değerlendirme

**Teknik Arka Plan:**  
QALAS, T1–T2 relaksasyon haritalarını tek bir taramada ölçerek zaman etkinliği sağlar...

**Deneysel Bulgular:**  
Literatürde test–retest ICC değerleri 0.91–0.98 arasında değişmektedir...

**Sonuç:**  
QALAS, yüksek tekrarlanabilirlik ve kısa tarama süresiyle çok-merkezli çalışmalarda güçlü bir adaydır.
```

Tüm çıktılar otomatik olarak `/outputs` dizinine kaydedilir:
`outputs/qalas_summary_20251029_143255.txt`

---

## 🧠 Example Queries

| Query                           | Description                                                                       |
| :------------------------------ | :-------------------------------------------------------------------------------- |
| **SSL with QALAS**              | Self-supervised mimariler ve sözlük bağımsızlığı.                                 |
| **3D-QALAS in cardiac imaging** | B1 homojenlik düzeltmesi ve hareket yönetimi.                                     |
| **Zero-DeepSub**                | Alt uzay ayrıştırma (subspace decomposition) ve zero-shot öğrenmenin avantajları. |
| **QALAS reproducibility**       | Test-retest metrikleri, ICC ve Bland–Altman analizi.                              |

---

## 🔍 Key Features

✅ Agno **`Workflow`** kullanarak çoklu ajan orkestrasyonu
✅ Otomatik kaynak seçimi (**PubMed / Arxiv**)
✅ Akademik Türkçe tonda, akıl yürütme odaklı özetleme
✅ Modüler komut istemi sistemi (**kolayca özelleştirilebilir**)
✅ Atıf takibi için kalıcı çıktı (output persistence)

---

## 📁 Project Structure

```
📂 qalas-multi-agent-research
│
├── agents/
│   ├── agents.py              # Ajan tanımları
│   └── prompts.py             # Alana özel komut istemleri
│
├── workflow/
│   └── qalas_workflow.py      # İş akışı ve mantığı
│
├── outputs/                   # Otomatik kaydedilen metin raporları
├── main.py                    # CLI giriş noktası
├── .env                       # Ortam değişkenleri
└── README.md
```

---

## 🌍 Future Extensions

🧠 Vektör veri tabanları ile anlamsal geri çağırma (Chroma / PgVector)
🧩 Google Scholar veya Semantic Scholar ile entegrasyon
🧮 Kantitatif makale trend analizi (yıllık / sekans bazında)
🌐 Web gösterge paneli (Streamlit / FastAPI UI)

---

## 💡 Citation

Bu iş akışına araştırmanızda veya projenizde atıfta bulunursanız:

```
Esma. (2025). QALAS Research Workflow: Multi-Agent Reasoning Framework for Quantitative MRI Analysis.
GitHub Repository. https://github.com/<yourusername>/qalas-multi-agent-research
```

---

## 🧠 Acknowledgments

Bu proje, kantitatif MRI araştırmaları için akıllı ajanlar inşa etmeye yönelik devam eden bir girişimin parçasıdır.
Modüler akıl yürütme ardışık düzenlerini sağladığı için **Agno framework**’e ve açık tıbbi görüntüleme araştırma topluluğuna teşekkür ederim.

---

## 🧭 Keywords

`#QALAS` · `#MRI` · `#qMRI` · `#Relaxometry` · `#AIinHealthcare` · `#AgnoAgents` · `#Reasoning` · `#PubMed` · `#Arxiv` · `#MultiAgentSystems` 
---

📌 **Developed by Esma** — tıbbi görüntüleme, yapay zeka ve akıl yürütme sistemlerini tek bir otomatik araştırma motorunda birleştiriyor.

```

