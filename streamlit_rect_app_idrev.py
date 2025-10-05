# ==============================================================================
# 1. IMPOR PUSTAKA (LIBRARY)
# ==============================================================================

import streamlit as st
# LangChain/LangGraph: Pustaka untuk membangun 'otak' agen AI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Any

# ==============================================================================
# 1.5. INISIALISASI KONSTANTA & INJEKSI CSS/HTML UNTUK WHATSAPP
# ==============================================================================

# GANTI DENGAN NOMOR WHATSAPP ANDA YANG BENAR (cth: 628123456789)
WHATSAPP_NUMBER = "6289637031266" 
WHATSAPP_LINK = f"https://wa.me/{WHATSAPP_NUMBER}"

# Injeksi CSS dan HTML untuk Floating WhatsApp Button
st.markdown(
    f"""
    <style>
    /* CSS untuk Tombol WhatsApp Melayang */
    .whatsapp-float {{
        position: fixed;
        width: 60px;
        height: 60px;
        bottom: 30px;
        right: 30px;
        background-color: #25d366;
        color: #FFF;
        border-radius: 50px;
        text-align: center;
        /* Ikon Sederhana (SVG WhatsApp Icon) */
        line-height: 65px; 
        font-size: 30px;
        box-shadow: 2px 2px 3px #999;
        z-index: 1000; /* Pastikan berada di atas konten lain */
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none; /* Hilangkan garis bawah pada tautan */
    }}

    .whatsapp-float:hover {{
        background-color: #128c7e;
    }}
    </style>

    <a href="{WHATSAPP_LINK}" class="whatsapp-float" target="_blank" title="Hubungi kami via WhatsApp">
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-whatsapp" viewBox="0 0 16 16">
          <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.927c0 1.399.366 2.76 1.057 3.965L.053 15.94a.5.5 0 0 0 .604.604l4.137-1.378a7.926 7.926 0 0 0 3.965 1.057c4.366 0 7.92-3.558 7.923-7.926.002-2.182-1.04-4.253-2.943-5.352Zm-2.72 8.412c-.59.358-1.077.34-1.385.205-.386-.176-.84-.368-1.381-.54-.486-.153-1.037-.308-1.57-.457-.655-.183-1.282-.373-1.854-.539-.374-.11-.53-.153-.78-.153-.306 0-.52.12-.66.36-.14.24-.2.53-.2.83 0 .34.1.66.33.95.23.3.56.63.95.89.39.26.83.47 1.3.66.47.19.97.35 1.5.48.53.13 1.06.22 1.57.27.53.05 1.04.05 1.5-.02.66-.08 1.25-.33 1.63-.67.38-.34.62-.75.62-1.2.0-.45-.24-.86-.62-1.2-.38-.34-.97-.59-1.63-.67Z"/>
        </svg>
    </a>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# 2. KONFIGURASI DAN TAMPILAN AWAL (CENTERED LAYOUT)
# ==============================================================================

st.set_page_config(
    page_title="Chatbot Ahli TPM", 
    page_icon="🤖", 
    layout="wide", 
    initial_sidebar_state="collapsed" 
    )

# --- FUNGSI CALLBACK UNTUK MENGISI INPUT CHAT DENGAN SARAN ---
def set_input_value(prompt_text):
    """Menyetel nilai kotak input chat saat tombol diklik."""
    st.session_state["chat_input_key"] = prompt_text


# --- PENAMBAHAN: TENGANGAN VERTIKAL DAN HORIZONTAL ---

# Padding vertikal (mendorong konten ke tengah layar saat baru dibuka)
for _ in range(5): 
    st.write('\n')

# Menggunakan 3 kolom: 1 (padding kiri), 3 (konten utama), 1 (padding kanan) untuk centering horizontal
col_left_padding, col_center_content, col_right_padding = st.columns([1, 3, 1])

with col_center_content:
    # 2.1. Kolom untuk Logo dan Judul
    col_logo, col_title = st.columns([1, 4]) 

    with col_logo:
        # Menggunakan ikon pabrik besar sebagai logo visual utama
        st.markdown("# 🏭", unsafe_allow_html=True) 

    with col_title:
        # Menampilkan judul dan deskripsi
        st.title("💬 Chatbot Edukasi tentang TPM System") 
        st.caption("Sebuah chatbot edukasi TPM yang ramah, berpengetahuan, dan siap berdiskusi bersama Anda.")
    
    # 2.2. Pesan Sambutan Besar (Mirip tampilan referensi)
    st.markdown("---") 
    st.markdown("## Bagaimana saya bisa membantu Anda hari ini?")

    # 2.3. Suggested Prompts (Tombol Saran Pertanyaan)
    
    # DAFTAR PERTANYAAN SARAN
    SARAN_PERTANYAAN = [
        "Jelaskan 8 Pilar TPM secara ringkas.",
        "Apa itu metrik OEE? Berikan contoh di mesin mixing.",
        "Mengapa Autonomous Maintenance penting di mesin jahit?",
        "Berikan contoh langkah-langkah Planned Maintenance untuk mesin chiller."
    ]

    # Mengatur tombol dalam dua kolom
    col1, col2 = st.columns(2)
    
    # Menampilkan tombol saran (MENGGUNAKAN on_click CALLBACK)
    with col1:
        st.button(
            SARAN_PERTANYAAN[0], 
            use_container_width=True, 
            help="Klik untuk menanyakan 8 Pilar TPM.",
            on_click=set_input_value, 
            args=[SARAN_PERTANYAAN[0]]
        )
        st.button(
            SARAN_PERTANYAAN[2], 
            use_container_width=True, 
            help="Klik untuk menanyakan Autonomous Maintenance.",
            on_click=set_input_value, 
            args=[SARAN_PERTANYAAN[2]]
        )
    
    with col2:
        st.button(
            SARAN_PERTANYAAN[1], 
            use_container_width=True, 
            help="Klik untuk menanyakan OEE.",
            on_click=set_input_value, 
            args=[SARAN_PERTANYAAN[1]]
        )
        st.button(
            SARAN_PERTANYAAN[3], 
            use_container_width=True, 
            help="Klik untuk menanyakan Planned Maintenance.",
            on_click=set_input_value, 
            args=[SARAN_PERTANYAAN[3]]
        )
    
    st.markdown("---") 


# ==============================================================================
# 3. BILAH SAMPING (SIDEBAR) UNTUK PENGATURAN
# ==============================================================================

with st.sidebar:
    st.subheader("Pengaturan Model AI")
    
    # Input Kunci API
    google_api_key = st.text_input("🔑 Google AI API Key", type="password")
    
    # --- Penjelasan API ---
    st.markdown("---")
    st.markdown("**Mengapa Perlu API Key?**")
    st.caption("Chatbot ini menggunakan model bahasa besar (LLM) dari Google (**Gemini**) yang dihosting secara *cloud*. Kunci API adalah kredensial yang memungkinkan aplikasi ini terhubung ke layanan Gemini untuk menghasilkan jawaban.")
    
    st.markdown("---")
    st.markdown("**Cara Mendapatkan API Key:**")
    st.markdown("""
        Anda bisa mendapatkan Kunci API Google AI secara gratis di Google AI Studio.
        
        [**➡️ Dapatkan Kunci API (Versi Indonesia)**](https://ai.google.dev/gemini-api/docs/api-key?hl=id) 
        
        *(Pastikan Anda login ke Akun Google Anda)*
    """)
    st.markdown("---")

    # Tombol Reset
    st.subheader("Kontrol Percakapan")
    reset_button = st.button("🔄 Mulai Ulang Percakapan", help="Hapus semua pesan dan mulai dari awal")
    st.markdown("---")
    
    # --- INFORMASI TEMA ---
    st.subheader("Tampilan Aplikasi")
    st.info("💡 Untuk mengganti tema (Dark/Light Mode), klik ikon tiga titik (**⋮**) di pojok kanan atas aplikasi Anda, lalu pilih **Settings**.", icon="🎨")


# ==============================================================================
# 4. CEK KUNCI API DAN INISIALISASI AGEN (OTAK CHATBOT)
# ==============================================================================

# 4.1. Cek Kunci API Awal
if not google_api_key:
    st.info(
        "Mohon tambahkan kunci API Google AI Anda di sidebar untuk memulai.",
        icon="🗝️"
    )
    st.info(
        "Anda juga dapat mendapatkan bantuan melalaui Whatsapp dengan klik tombol di pojok kanan bawah",
        icon="💡"
    )
    st.stop()

# 4.2. Inisialisasi Agen 
if ("agent" not in st.session_state) or (getattr(st.session_state, "_last_key", None) != google_api_key):
    try:
        # ----------------------------------------------------------------------
        # --- A. SISTEM PROMPT (Konteks Pabrik Sepatu Diperkuat & Bertahap) ---
        # ----------------------------------------------------------------------
        
        # DAFTAR MESIN UNTUK ANALOGI KUAT
        mesin_spesifik = [
            "mesin jahit", "lini lasting", "mesin chiller", "mesin cutting kulit", 
            "mesin hot press", "mesin mixing", "mesin laminating"
        ]
        mesin_list_str = ", ".join(mesin_spesifik)
        
        system_prompt = (
            "Anda adalah **Chatbot Ahli TPM** yang berfokus pada industri **Manufaktur Sepatu**, namun tampil umum di UI. "
            "Tujuan Anda adalah memberikan jawaban yang **cepat, ringkas, dan bertahap** kepada pengguna. "
            
            "**Instruksi Utama (WAJIB Konteks Sepatu & Format Bertahap):** "
            "1. **Format Respons Awal:** Jawab setiap pertanyaan dengan ringkas, maksimal **3-4 poin utama saja**."
            "2. **Konteks Jawaban Wajib:** Semua poin yang Anda jelaskan **WAJIB** menggunakan contoh dari salah satu mesin atau proses berikut: **{mesin_list_str}**. "
            "   Jangan pernah menggunakan contoh dari industri non-sepatu lainnya."
            "3. **Pendorong Detail:** **Selalu akhiri** respons awal Anda dengan menawarkan detail lebih lanjut. Gunakan frasa seperti: "
            "   'Apakah Anda ingin penjelasan yang lebih rinci tentang hal ini, atau contoh lain di proses *hot press*?' atau 'Silakan ketik 'detail' jika Anda ingin saya jelaskan setiap poin di atas secara mendalam.'"
            "4. **Respons Detail (Jika diminta):** Jika pengguna meminta 'detail' atau 'lebih lanjut', berikan jawaban yang lebih panjang dan terstruktur (menggunakan Markdown *heading* dan *sub-bullet*) sambil tetap menggunakan konteks mesin sepatu."
            "5. **Gaya Komunikasi:** Profesional, ramah, dan ringkas. Gunakan **bold** untuk kata kunci."
            "6. **Penolakan Topik:** Tolak semua pertanyaan non-TPM dengan sopan dan kembalikan fokus ke TPM."
        )
        # ----------------------------------------------------------------------

        # --- B. Inisialisasi Model Gemini ---
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=google_api_key,
            temperature=0.7, 
            system_instruction=system_prompt 
        )
        
        # --- C. Membuat Agen ReAct ---
        st.session_state.agent = create_react_agent(
            model=llm,
            tools=[],  
            prompt="Jalankan tugas Anda sebagai Chatbot Ahli TPM berdasarkan system prompt yang telah diberikan. Prioritaskan jawaban ringkas. Respon segera berdasarkan riwayat percakapan."
        )
        
        # --- D. Manajemen State ---
        st.session_state._last_key = google_api_key
        st.session_state.pop("messages", None) 
        
    except Exception as e:
        # Menambahkan pesan error yang lebih jelas di body utama
        st.error(f"❌ Kunci API tidak valid atau ada kesalahan koneksi: {e}")
        st.stop() 
        
# ==============================================================================
# 5. MENGELOLA RIWAYAT PERCAKAPAN (MEMORY) DAN RESET
# ==============================================================================

# 5.1. Inisialisasi Riwayat Pesan
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5.2. Mengelola Tombol Reset
if reset_button:
    # Hapus semua state yang terkait dengan agent dan percakapan
    keys_to_delete = ["agent", "messages", "_last_key", "chat_input_key"] 
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun() 

# ==============================================================================
# 6. MENAMPILKAN PESAN SEBELUMNYA (Hanya Tampil Setelah Interaksi Dimulai)
# ==============================================================================

if st.session_state.messages:
    for msg in st.session_state.messages:
        avatar = msg.get("avatar")
        if avatar is None:
            # Tetapkan avatar default
            avatar = "🧑‍💻" if msg["role"] == "user" else "⚙️"
            
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# ==============================================================================
# 7. MENGELOLA INPUT PENGGUNA DAN KOMUNIKASI DENGAN AGEN 
# ==============================================================================

# st.chat_input akan otomatis membaca nilai dari st.session_state["chat_input_key"] 
prompt = st.chat_input(
    "Tanyakan tentang TPM...", 
    key="chat_input_key"
)


if prompt:
    # 7.1. Tambahkan Pesan Sambutan ke Riwayat (Jika ini interaksi pertama)
    if not st.session_state.messages:
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Halo! Selamat datang di **Chatbot Edukasi TPM** 🤖. Saya akan berikan ringkasan cepat. Silakan lanjutkan pertanyaan Anda!",
            "avatar": "⚙️" 
        })
    
    # Tambahkan dan Tampilkan Pesan Pengguna
    st.session_state.messages.append({"role": "user", "content": prompt}) 
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # 7.2. Panggil Agen untuk Mendapatkan Respons
    try:
        # Konversi riwayat pesan ke format LangChain
        messages: List[Any] = []
        
        # Konversi riwayat ke HumanMessage/AIMessage untuk LangChain/LangGraph
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                # Mengabaikan pesan sambutan awal saat mengirim ke agen
                if msg["content"].startswith("Halo!"): 
                    continue
                messages.append(AIMessage(content=msg["content"]))
        
        # Panggil agen menggunakan invoke()
        with st.spinner("TPM_Miner sedang menggali informasi..."): 
            response = st.session_state.agent.invoke({"messages": messages})
        
        # Ekstrak jawaban (teks) dari respons LangGraph/ReAct
        if isinstance(response, dict) and "output" in response:
            answer = response["output"]
        elif "messages" in response and len(response["messages"]) > 0:
            answer = response["messages"][-1].content
        else:
            answer = "Maaf, TPM_Miner gagal menghasilkan respons yang jelas. Coba ulangi pertanyaan Anda."

        # 7.3. Tampilkan dan Simpan Jawaban Asisten
        with st.chat_message("assistant", avatar="⚙️"): 
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    except Exception as e:
        error_message = f"Terjadi kesalahan saat pemrosesan: **{e}**. Pastikan Kunci API Anda masih valid dan coba Muat Ulang Percakapan."
        with st.chat_message("assistant", avatar="⚠️"):
            st.markdown(error_message)

