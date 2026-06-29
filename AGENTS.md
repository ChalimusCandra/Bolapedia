# AGENTS.md — BolaPedia: RAG Chatbot Sepak Bola

> **Dokumen ini adalah konteks proyek untuk AI assistant.**
> Gunakan file ini sebagai referensi saat membantu pengembangan proyek BolaPedia.
> Kompatibel dengan: Claude, ChatGPT, Gemini, GitHub Copilot, Cursor, dan AI lainnya.

---

## 🎯 Ringkasan Proyek

| Item | Detail |
|------|--------|
| **Nama Proyek** | BolaPedia |
| **Deskripsi** | RAG (Retrieval-Augmented Generation) chatbot tentang sepak bola yang menjawab pertanyaan pengguna berdasarkan dokumen dan dataset |
| **Keperluan** | Tugas Mata Kuliah |
| **Bahasa Chatbot** | Bahasa Indonesia |
| **Scope Saat Ini** | Chatbot RAG berbasis dokumen (fase awal), dengan rencana ekspansi ke tampilan data dan visualisasi |

## 📋 Deskripsi Proyek

BolaPedia adalah aplikasi chatbot cerdas berbasis **Retrieval-Augmented Generation (RAG)** yang mampu menjawab pertanyaan seputar sepak bola (pemain, klub, transfer, kompetisi, aturan permainan, sejarah) dalam **Bahasa Indonesia**. Sistem mengambil informasi dari knowledge base yang dibangun dari dataset Kaggle dan dokumen teks, lalu menggunakan LLM untuk menghasilkan jawaban yang akurat dan bersumber.

### Tujuan
1. Membangun RAG pipeline lengkap: data ingestion → chunking → embedding → retrieval → generation
2. Menerapkan **model Transformer** untuk embedding dokumen (persyaratan tugas)
3. Menghasilkan chatbot yang menjawab pertanyaan bola dengan akurat berdasarkan data, bukan halusinasi
4. Setiap jawaban harus bisa menunjukkan sumber/dokumen asal informasi

### Mengapa RAG (bukan LLM biasa)?
- LLM biasa tidak memiliki data statistik pemain/klub terkini
- LLM biasa sering berhalusinasi (mengarang data statistik)
- RAG memastikan jawaban di-*ground* pada data nyata dari dataset
- Knowledge base bisa di-update tanpa re-training model

---

## 🛠️ Tech Stack

```
┌────────────────────────────────────────────────────────────┐
│                      TECH STACK                            │
├────────────────────────────────────────────────────────────┤
│  Bahasa       : Python 3.10+                              │
│  RAG Framework: LangChain                                 │
│  Embedding    : sentence-transformers (Transformer-based) │
│                 Model: paraphrase-multilingual-MiniLM-L12-v2│
│  Vector DB   : ChromaDB                                   │
│  LLM         : OpenRouter API (openai/gpt-4o-mini)        │
│  Frontend    : Streamlit                                  │
│  Data Processing: Pandas                                  │
│  PDF Parsing : PyMuPDF (fitz)                             │
└────────────────────────────────────────────────────────────┘
```

### Detail Komponen

| Komponen | Teknologi | Versi/Model | Catatan |
|----------|-----------|-------------|---------|
| **Bahasa Pemrograman** | Python | 3.10+ | Gunakan type hints |
| **RAG Framework** | LangChain | latest | `langchain`, `langchain-community`, `langchain-openai` |
| **Embedding Model** | Sentence Transformers (Transformer-based) | `paraphrase-multilingual-MiniLM-L12-v2` | Wajib Transformer — support Bahasa Indonesia, 384 dimensi, basis arsitektur BERT |
| **Vector Database** | ChromaDB | latest | Persist ke folder `vectorstore/` |
| **LLM** | OpenRouter (GPT-4o-Mini) | `openai/gpt-4o-mini` | API key via openrouter.ai |
| **Frontend** | Streamlit | latest | UI chatbot sederhana |
| **Data Processing** | Pandas | latest | Konversi CSV → dokumen teks |
| **PDF Parsing** | PyMuPDF | latest | Untuk Laws of the Game PDF |

### Kenapa Teknologi Ini Dipilih?
- **LangChain**: Framework RAG paling populer, dokumentasi lengkap, mudah di-debug
- **paraphrase-multilingual-MiniLM-L12-v2**: Model Transformer yang mendukung Bahasa Indonesia, cukup ringan (470 MB), akurasi baik untuk multilingual retrieval
- **ChromaDB**: Paling mudah setup (1 baris install), cocok untuk prototyping, persist ke disk
- **GPT-4o-Mini (OpenRouter)**: Sangat hemat biaya, cepat, pintar, mendukung Bahasa Indonesia dengan baik
- **Streamlit**: Cukup 1 file Python untuk membuat web app chatbot

---

## 📦 Dataset

### Sumber Data Utama
**Football Data from Transfermarkt** oleh David Cariboo (Kaggle)
- URL: https://www.kaggle.com/datasets/davidcariboo/player-scores
- Format: Multiple CSV files
- Update: Otomatis per minggu
- Lisensi: CC BY-SA 4.0

### File CSV dalam Dataset

| File | Isi | Kolom Utama | Prioritas |
|------|-----|-------------|:---------:|
| `players.csv` | Profil pemain | player_id, name, position, date_of_birth, country_of_citizenship, current_club_id, market_value_in_eur, height_in_cm, foot | ⭐ P1 |
| `clubs.csv` | Profil klub | club_id, name, domestic_competition_id, squad_size, stadium_name, stadium_seats, coach_name | ⭐ P1 |
| `competitions.csv` | Daftar liga & kompetisi | competition_id, name, type, country_name, confederation | ⭐ P1 |
| `transfers.csv` | Data transfer pemain | player_id, from_club_id, to_club_id, transfer_date, transfer_fee, market_value_in_eur | ⭐ P1 |
| `games.csv` | Data pertandingan | game_id, competition_id, home_club_id, away_club_id, date, home_club_goals, away_club_goals, attendance, referee | ⭐ P1 |
| `appearances.csv` | Penampilan pemain per match | appearance_id, game_id, player_id, goals, assists, yellow_cards, red_cards, minutes_played | 🟡 P2 |
| `player_valuations.csv` | Riwayat market value | player_id, date, market_value_in_eur, current_club_id | 🟡 P2 |
| `game_events.csv` | Event dalam pertandingan | game_id, type (goal/card/sub), player_id, minute | 🟡 P2 |
| `game_lineups.csv` | Lineup per pertandingan | game_id, player_id, club_id, position, type (starting/bench) | 🟢 P3 |
| `club_games.csv` | Stats match per klub | club_id, game_id, goals, opponent_goals, is_win | 🟢 P3 |
| `countries.csv` | Data negara | country_id, name, confederation | 🟢 P3 |

### Dokumen Teks Tambahan (non-CSV)

| Dokumen | Sumber | Keterangan |
|---------|--------|------------|
| Laws of the Game 2024/25 | theifab.com (PDF resmi FIFA/IFAB) | Aturan sepak bola resmi, 17 Laws |
| Glosarium istilah sepak bola | Dibuat manual (Markdown) | ~200 istilah bola dalam Bahasa Indonesia |
| Sejarah klub top dunia | Wikipedia (Creative Commons) | ~20 klub top |
| Sejarah Piala Dunia | Wikipedia (Creative Commons) | Per edisi (1930-2022) |

### Strategi Data untuk RAG
Data CSV **tidak langsung dimasukkan** ke RAG. CSV harus **dikonversi menjadi dokumen teks** terlebih dahulu menggunakan script Python (`convert_data.py`). Setiap baris CSV diubah menjadi paragraf deskriptif yang bisa di-embed.

Contoh konversi `players.csv`:
```
# Input CSV row:
name=Erling Haaland, position=Centre-Forward, club=Manchester City, market_value=180000000, ...

# Output dokumen teks:
"Profil Pemain: Erling Haaland
 Nama: Erling Haaland
 Posisi: Centre-Forward
 Klub: Manchester City
 Market Value: €180.000.000
 ..."
```

---

## 🏗️ Arsitektur RAG Pipeline

```
┌──────────────────────────── DATA PREPARATION (offline, 1x) ──────────────────────────┐
│                                                                                       │
│  📁 CSV (Kaggle)  ──▶  🔄 convert_data.py  ──▶  📄 Dokumen Teks (.txt)              │
│  📄 PDF (Laws)    ──▶  🔄 parse_pdf.py      ──▶  📄 Dokumen Teks (.txt)              │
│  📝 Markdown      ──────────────────────────────▶ 📄 Dokumen Teks (.txt)              │
│                                                        │                              │
│                                                        ▼                              │
│                                                 ✂️ Text Splitter                      │
│                                                 (RecursiveCharacterTextSplitter)       │
│                                                 chunk_size=500, overlap=50             │
│                                                        │                              │
│                                                        ▼                              │
│                                                 🧮 Transformer Embedding              │
│                                                 (paraphrase-multilingual-MiniLM-L12-v2)│
│                                                        │                              │
│                                                        ▼                              │
│                                                 💾 ChromaDB (persist to disk)          │
└───────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────── QUERY TIME (real-time) ──────────────────────────────────┐
│                                                                                      │
│  👤 User: "Siapa top skor Premier League?"                                          │
│                    │                                                                 │
│                    ▼                                                                 │
│  ┌──────────────────────────┐                                                        │
│  │  🧮 Embed pertanyaan     │ ← Transformer embedding yang sama                     │
│  └────────────┬─────────────┘                                                        │
│               ▼                                                                      │
│  ┌──────────────────────────┐                                                        │
│  │  🔍 Similarity Search    │ ← Cari top-k (k=5) dokumen terdekat di ChromaDB       │
│  └────────────┬─────────────┘                                                        │
│               ▼                                                                      │
│  ┌──────────────────────────┐                                                        │
│  │  📄 Retrieved Documents  │ ← 5 dokumen paling relevan                            │
│  └────────────┬─────────────┘                                                        │
│               ▼                                                                      │
│  ┌──────────────────────────┐                                                        │
│  │  🤖 LLM (GPT-4o-Mini)   │ ← Prompt: "Berdasarkan dokumen berikut, jawab         │
│  │     + System Prompt      │    pertanyaan user dalam Bahasa Indonesia.             │
│  │     + Retrieved Docs     │    Sertakan sumber data."                              │
│  │     + User Question      │                                                        │
│  └────────────┬─────────────┘                                                        │
│               ▼                                                                      │
│  ┌──────────────────────────┐                                                        │
│  │  💬 Jawaban + Sumber     │ ← Tampilkan di Streamlit                              │
│  └──────────────────────────┘                                                        │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📂 Struktur Folder Proyek

```
bolapedia-rag/
│
├── 📁 data/
│   ├── 📁 raw/                        # Dataset mentah dari Kaggle
│   │   ├── players.csv
│   │   ├── clubs.csv
│   │   ├── competitions.csv
│   │   ├── games.csv
│   │   ├── transfers.csv
│   │   ├── appearances.csv
│   │   ├── player_valuations.csv
│   │   ├── game_events.csv
│   │   ├── game_lineups.csv
│   │   ├── club_games.csv
│   │   └── countries.csv
│   │
│   ├── 📁 documents/                  # Dokumen teks tambahan
│   │   ├── laws_of_the_game.pdf
│   │   ├── glossary.md
│   │   └── 📁 history/               # Sejarah klub & kompetisi
│   │       ├── real_madrid.md
│   │       ├── barcelona.md
│   │       └── ...
│   │
│   └── 📁 processed/                 # Hasil konversi (auto-generated)
│       ├── 📁 players/
│       ├── 📁 clubs/
│       ├── 📁 competitions/
│       ├── 📁 transfers/
│       ├── 📁 matches/
│       └── 📁 rules/
│
├── 📁 vectorstore/                    # ChromaDB persistence (auto-generated)
│
├── 📁 scripts/
│   ├── convert_data.py                # Konversi CSV → dokumen teks
│   └── build_vectorstore.py           # Embed dokumen → simpan ke ChromaDB
│
├── app.py                             # Streamlit chatbot (entry point)
├── requirements.txt                   # Python dependencies
├── .env                               # API keys (JANGAN commit ke git)
├── .gitignore
├── README.md                          # Dokumentasi proyek
└── AGENTS.md                          # File ini
```

---

## 📜 Aturan & Konvensi

### Coding Style
- **Bahasa kode**: Variabel, fungsi, komentar dalam Bahasa Inggris
- **Bahasa output**: Chatbot menjawab dalam **Bahasa Indonesia**
- **Python style**: Ikuti PEP 8, gunakan type hints
- **Docstrings**: Wajib untuk setiap fungsi utama
- **Error handling**: Gunakan try-except untuk operasi file dan API calls

### Konvensi Penamaan
```python
# File: snake_case
convert_data.py
build_vectorstore.py

# Fungsi: snake_case
def convert_players_to_documents():
def build_vector_store():

# Variabel: snake_case
player_documents = []
vector_store = None

# Konstanta: UPPER_SNAKE_CASE
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
TOP_K_RESULTS = 5
```

### Konfigurasi Penting
```python
# Embedding
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# Alasan: Transformer-based (BERT), support Bahasa Indonesia, ringan (470MB)

# Chunking
CHUNK_SIZE = 500          # karakter per chunk
CHUNK_OVERLAP = 50        # overlap antar chunk

# Retrieval
TOP_K_RESULTS = 5         # jumlah dokumen yang di-retrieve per query

# LLM
LLM_MODEL = "openai/gpt-4o-mini"
LLM_TEMPERATURE = 0.3     # rendah agar jawaban faktual, tidak kreatif

# Vector Store
VECTORSTORE_DIR = "vectorstore/"
COLLECTION_NAME = "bolapedia"
```

### System Prompt untuk LLM
```
Kamu adalah BolaPedia AI, asisten cerdas yang ahli tentang sepak bola.

Aturan:
1. Jawab HANYA dalam Bahasa Indonesia.
2. Jawab HANYA berdasarkan dokumen konteks yang diberikan.
3. Jika informasi tidak ada di dokumen, katakan: "Maaf, saya tidak menemukan 
   informasi tersebut dalam database saya."
4. JANGAN mengarang atau menambahkan informasi di luar dokumen.
5. Sertakan sumber data di akhir jawaban.
6. Gunakan format yang rapi (bullet points, tabel jika perlu).
7. Jika ditanya perbandingan, sajikan dalam bentuk tabel.
```

### Environment Variables (.env)
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### .gitignore
```
.env
vectorstore/
data/raw/
__pycache__/
*.pyc
venv/
.venv/
```

---

## 🚀 Fase Pengembangan

### Fase 1 — MVP (Chatbot RAG Dasar) ← FOKUS SAAT INI
- [x] Pilih dataset (Transfermarkt dari Kaggle)
- [ ] Setup proyek (folder, dependencies, API key)
- [ ] Konversi CSV → dokumen teks (players, clubs, competitions, transfers, games)
- [ ] Bangun RAG pipeline (load → chunk → embed → store ke ChromaDB)
- [ ] Buat chatbot Streamlit sederhana
- [ ] Testing dengan 10+ pertanyaan berbeda
- [ ] Chatbot bisa menjawab pertanyaan tentang pemain, klub, transfer, pertandingan

### Fase 2 — Enhanced (Tampilan Data Sederhana)
- [ ] Tambahkan dokumen Laws of the Game + glosarium + sejarah
- [ ] Tampilkan sumber dokumen di bawah jawaban
- [ ] Tampilkan data tabel sederhana (statistik pemain, klasemen)
- [ ] Chat history (conversation memory)
- [ ] Contoh pertanyaan yang bisa diklik
- [ ] Perbaikan prompt engineering

### Fase 3 — Advanced (Visualisasi Lengkap)
- [ ] Dashboard visualisasi (grafik, chart)
- [ ] Perbandingan pemain visual (radar chart)
- [ ] Metadata filtering (filter berdasarkan liga, musim, posisi)
- [ ] Evaluasi RAG (precision, recall, faithfulness)
- [ ] Optimasi performa

---

## 💬 Contoh Pertanyaan yang Harus Bisa Dijawab

### Fase 1 (MVP):
```
"Siapa Erling Haaland?"
"Berapa market value Kylian Mbappé?"
"Di klub mana Lionel Messi bermain?"
"Ceritakan tentang Real Madrid"
"Stadion Manchester United namanya apa?"
"Siapa pelatih Liverpool?"
"Berapa fee transfer Neymar ke PSG?"
"Transfer termahal sepanjang sejarah?"
"Hasil pertandingan Barcelona vs Real Madrid terakhir?"
"Liga apa saja yang ada di kompetisi Eropa?"
```

### Fase 2 (Enhanced):
```
"Apa itu offside?"
"Jelaskan aturan handball"
"Bandingkan statistik Salah dan Vinicius Jr"
"Sejarah Piala Dunia 2022"
"Apa arti istilah 'hat-trick'?"
```

---

## 📖 Panduan untuk AI Assistant

Saat membantu proyek ini, perhatikan hal-hal berikut:

### DO ✅
- Gunakan **Python** untuk semua kode
- Gunakan **LangChain** sebagai RAG framework
- Gunakan **ChromaDB** sebagai vector database
- Gunakan **`paraphrase-multilingual-MiniLM-L12-v2`** sebagai embedding model (Transformer-based, support Bahasa Indonesia)
- Gunakan **OpenRouter API** (`openai/gpt-4o-mini`) via library `langchain-openai` sebagai LLM
- Gunakan **Streamlit** untuk UI chatbot
- Jawaban chatbot harus dalam **Bahasa Indonesia**
- Setiap jawaban harus menampilkan **sumber dokumen**
- Ikuti struktur folder yang sudah ditentukan
- Tulis kode yang bersih, dengan docstring dan type hints

### DON'T ❌
- Gunakan base URL OpenRouter saat menginisialisasi ChatOpenAI
- Jangan gunakan framework selain LangChain (kecuali diminta)
- Jangan gunakan embedding model non-Transformer
- Jangan buat arsitektur yang terlalu kompleks — ini proyek tugas kuliah, bukan production system
- Jangan hardcode API key di source code (gunakan .env)
- Jangan commit data raw (CSV) ke git

### Cara Membantu yang Efektif
1. Jika diminta membuat kode, buat **lengkap dan bisa langsung dijalankan**
2. Jika ada error, analisis berdasarkan konteks proyek ini
3. Jika diminta menambah fitur, pastikan konsisten dengan tech stack di atas
4. Jika ada pilihan arsitektur, pilih yang **paling sederhana** yang memenuhi kebutuhan
5. Selalu rujuk ke struktur folder dan konvensi penamaan di atas

---

## 📚 Referensi & Link Penting

| Resource | URL |
|----------|-----|
| Dataset Kaggle | https://www.kaggle.com/datasets/davidcariboo/player-scores |
| LangChain Docs | https://python.langchain.com/docs/ |
| ChromaDB Docs | https://docs.trychroma.com/ |
| Sentence Transformers | https://www.sbert.net/ |
| Streamlit Docs | https://docs.streamlit.io/ |
| OpenRouter API | https://openrouter.ai/ |
| Laws of the Game | https://www.theifab.com/log-documents |
| Hugging Face Model | https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 |
