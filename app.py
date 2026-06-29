import streamlit as st

# === KONFIGURASI HALAMAN ===
st.set_page_config(
    page_title="⚽ BolaPedia AI",
    page_icon="⚽",
    layout="centered"
)

# === JUDUL ===
st.title("⚽ BolaPedia AI")
st.caption("Chatbot cerdas tentang sepak bola — Tanya apa saja!")

# === SIDEBAR ===
with st.sidebar:
    st.header("ℹ️ Tentang")
    st.write("BolaPedia AI menjawab pertanyaan sepak bola berdasarkan data dari Transfermarkt.")
    st.divider()

    st.subheader("📌 Contoh Pertanyaan")
    example_questions = [
        "Siapa Erling Haaland?",
        "Ceritakan tentang Real Madrid",
        "Transfer termahal sepanjang sejarah?",
        "siapa pemain terbaik di Piala Dunia 2022?",
    ]
    for q in example_questions:
        if st.button(q, use_container_width=True):
            st.session_state["user_input"] = q

# === CHAT HISTORY ===
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan semua pesan yang sudah ada
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# === INPUT USER ===
user_input = st.chat_input("Tanya tentang sepak bola...")

# Ambil dari tombol sidebar jika ada
if "user_input" in st.session_state and st.session_state["user_input"]:
    user_input = st.session_state["user_input"]
    st.session_state["user_input"] = ""

# === PROSES PESAN ===
if user_input:
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Jawaban sementara (ganti nanti dengan RAG chain dari Person B)
    # answer = rag_chain.invoke(user_input)  ← ini nanti di Minggu 2
    answer = "🔧 RAG chain belum terhubung. Tunggu Person B selesai!"

    # Tampilkan jawaban bot
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)