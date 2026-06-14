"""
app.py - Streamlit Web App untuk Chatbot Konsultan Pemasaran Digital
Recreate Chat UI (seperti index.html) menggunakan Streamlit Native
"""

import streamlit as st
from FSM import STATES, OPTIONS, INITIAL_STATE, FINAL_STATE, transition
from engine import generate_recommendations

# ─── QUESTION PROMPTS ─────────────────────────────────────────────────────────
PROMPTS = {
    "q0":  "Selamat datang! 👋 Saya adalah <strong>MarketBot</strong> — konsultan pemasaran digital Anda. Saya akan membantu menemukan strategi terbaik untuk bisnis Anda melalui beberapa pertanyaan singkat.",
    "q1":  "Pertama, <strong>apa jenis usaha Anda?</strong> Pilih kategori yang paling sesuai:",
    "q2":  "Siapa <strong>target usia</strong> pelanggan utama bisnis Anda?",
    "q3":  "Apa <strong>profesi</strong> target pelanggan Anda?",
    "q4":  "Bagaimana <strong>gaya hidup</strong> target pelanggan Anda?",
    "q5":  "Berapa <strong>anggaran promosi</strong> yang Anda siapkan per bulan?",
    "q6":  "Apa <strong>tujuan utama pemasaran</strong> Anda saat ini?",
    "q7":  "Di mana <strong>lokasi target pasar</strong> Anda?",
    "q8":  "Sudah berapa lama bisnis Anda berjalan? (<strong>tahap perkembangan</strong>)",
    "q9":  "Media promosi apa yang <strong>sudah pernah Anda gunakan</strong>?",
    "q10": "Seberapa sering Anda melakukan <strong>promosi</strong>?",
    "q11": "Bagaimana <strong>tingkat persaingan</strong> di industri Anda?",
    "q12": "Siapa <strong>jenis pelanggan utama</strong> bisnis Anda?",
    "q13": "⚙️ Menganalisis strategi promosi terbaik...",
    "q14": "📱 Menentukan platform media sosial optimal...",
    "q15": "🎨 Merancang jenis konten yang tepat...",
    "q16": "🌟 Menganalisis strategi influencer marketing...",
    "q17": "🎁 Menyusun program promosi yang efektif...",
    "q18": "🎯 Melakukan segmentasi pasar...",
    "q19": "✅ Analisis selesai!",
    "q20": "Apakah Anda ingin melakukan <strong>konsultasi lagi</strong> untuk bisnis lain?",
    "q21": "Terima kasih telah menggunakan <strong>MarketBot</strong>! 🎉 Semoga strategi ini membantu bisnis Anda berkembang. Sukses selalu!",
}

STEP_LABELS = {
    "q1": "Jenis Usaha", "q2": "Target Usia", "q3": "Profesi",
    "q4": "Gaya Hidup", "q5": "Anggaran", "q6": "Tujuan",
    "q7": "Lokasi", "q8": "Tahap Bisnis", "q9": "Media Sebelumnya",
    "q10": "Frekuensi", "q11": "Kompetisi", "q12": "Jenis Pelanggan",
}

KEY_MAP = {
    "q1": "jenis_usaha", "q2": "target_usia", "q3": "target_profesi", "q4": "gaya_hidup",
    "q5": "anggaran", "q6": "tujuan", "q7": "lokasi", "q8": "tahap_bisnis",
    "q9": "media_sebelumnya", "q10": "frekuensi", "q11": "tingkat_kompetisi", "q12": "jenis_pelanggan",
}

# ─── STREAMLIT CONFIG & CSS ──────────────────────────────────────────────────
st.set_page_config(page_title="MarketBot", page_icon="🤖", layout="wide")

# CSS agar tampilan mirip seperti Web Chat (Hide default Streamlit elements)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
        max-width: 800px; /* Lebar chat seperti WhatsApp/Web */
    }
    </style>
    """, unsafe_allow_html=True)

# ─── SESSION STATE INIT ──────────────────────────────────────────────────────
if "state" not in st.session_state:
    st.session_state.state = INITIAL_STATE
    st.session_state.data = {}
    st.session_state.recs = None
    st.session_state.messages = [{"role": "assistant", "content": PROMPTS["q0"]}]

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def _get_flat_options(state: str):
    opts = OPTIONS.get(state)
    if isinstance(opts, dict):
        display_list = []
        value_map = {}
        for group, items in opts.items():
            for item in items:
                display = f"[{group}] {item}"
                display_list.append(display)
                value_map[display] = item
        return display_list, value_map
    elif isinstance(opts, list):
        return opts, {x: x for x in opts}
    return [], {}

# ─── UI RENDERING ─────────────────────────────────────────────────────────────
st.title("🤖 MarketBot")
st.caption("Konsultan Pemasaran Digital")

current_state = st.session_state.state

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)
        
        # Jika pesan mengandung rekomendasi (Result), tampilkan di dalam chat bubble
        if "recs" in msg and msg["recs"]:
            recs = msg["recs"]
            with st.expander("📊 Lihat Hasil Rekomendasi Anda", expanded=True):
                st.subheader("🎯 Segmentasi Pasar")
                for k, v in recs.get("segmentasi", {}).items():
                    st.markdown(f"**{k}:** {v}")
                
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("🚀 Strategi Promosi")
                    for s in recs.get("strategi_promosi", []): st.markdown(f"- {s}")
                    st.subheader("📱 Platform Media Sosial")
                    for p in recs.get("platform_medsos", []): st.markdown(f"- {p}")
                    st.subheader("🌟 Influencer Marketing")
                    st.info(recs.get("influencer", "-"))
                with col2:
                    st.subheader("🎨 Jenis Konten")
                    for k in recs.get("jenis_konten", []): st.markdown(f"- {k}")
                    st.subheader("🎁 Program Promo")
                    for pr in recs.get("program_promo", []): st.markdown(f"- {pr}")

# ─── INTERACTIVE AREA (Chat Input Area) ──────────────────────────────────────

# STATE q0: Welcome
if current_state == "q0":
    if st.button("🚀 Mulai Konsultasi", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Mulai Konsultasi"})
        st.session_state.state = transition(current_state, "start")
        st.session_state.messages.append({"role": "assistant", "content": PROMPTS[st.session_state.state]})
        st.rerun()

# STATE q1 - q12: Questions (Menggunakan Form agar rapi seperti chat quick reply)
elif current_state in KEY_MAP:
    with st.form(key=f"form_{current_state}"):
        display_opts, val_map = _get_flat_options(current_state)
        selected_display = st.selectbox("Pilih jawaban Anda:", display_opts)
        submitted = st.form_submit_button("Lanjut ➡️", use_container_width=True)
        
        if submitted:
            user_input = val_map[selected_display]
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            if current_state in KEY_MAP:
                st.session_state.data[KEY_MAP[current_state]] = user_input
            
            next_state = transition(current_state, user_input)
            
            if next_state in ["q13", "q14", "q15", "q16", "q17", "q18"]:
                recs = generate_recommendations(st.session_state.data)
                st.session_state.recs = recs
                next_state = "q19"
            
            st.session_state.state = next_state
            
            if next_state == "q19":
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": PROMPTS["q19"], 
                    "recs": st.session_state.recs
                })
            else:
                st.session_state.messages.append({"role": "assistant", "content": PROMPTS[next_state]})
            st.rerun()

# STATE q19 & q20: Result & Repeat
elif current_state == "q19":
    st.markdown(PROMPTS["q20"], unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("✅ Ya, konsultasi lagi"):
            st.session_state.messages.append({"role": "user", "content": "Ya, konsultasi lagi"})
            st.session_state.state = transition("q20", "Ya, konsultasi lagi")
            st.session_state.data = {}
            st.session_state.recs = None
            st.session_state.messages.append({"role": "assistant", "content": PROMPTS["q1"]})
            st.rerun()
    with col2:
        if st.button("❌ Tidak, selesai"):
            st.session_state.messages.append({"role": "user", "content": "Tidak, selesai"})
            st.session_state.state = transition("q20", "Tidak, selesai")
            st.session_state.messages.append({"role": "assistant", "content": PROMPTS["q21"]})
            st.rerun()

# STATE q21: End
elif current_state == "q21":
    st.balloons()
    if st.button("🔄 Mulai Sesi Baru"):
        st.session_state.state = INITIAL_STATE
        st.session_state.data = {}
        st.session_state.recs = None
        st.session_state.messages = [{"role": "assistant", "content": PROMPTS["q0"]}]
        st.rerun()