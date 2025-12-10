"""
📚 Kelime Kartları Sayfası
Onaylanmış kelimeleri görüntüleme ve öğrenme
"""

import streamlit as st
import random

# Page config
st.set_page_config(
    page_title="Kelime Kartları - Lingua-AI",
    page_icon="📚",
    layout="wide"
)

# Auth check - Login Gate
import components.auth as auth
auth.check_auth()

# Imports (sadece giriş yapılmışsa)
from components.flashcard import render_flashcard, render_word_grid, get_flashcard_styles, render_word_of_the_day
from services.firebase_service import get_words
from utils.constants import EXAM_TYPES, DIFFICULTY_LEVELS
from utils.helpers import init_session_state

# Session state başlat
init_session_state()

# Ana içerik
st.title("📚 Kelime Kartları")
st.markdown("YDS, YÖKDİL, TOEFL ve IELTS sınavlarına hazırlık için kelime kartları")

# CSS
st.markdown(get_flashcard_styles(), unsafe_allow_html=True)

# Filtreler
st.markdown("---")

col1, col2, col3 = st.columns([2, 2, 3])

with col1:
    exam_filter = st.selectbox(
        "📋 Sınav Türü",
        options=["all"] + list(EXAM_TYPES.keys()),
        format_func=lambda x: "Tümü" if x == "all" else f"{EXAM_TYPES[x]['icon']} {EXAM_TYPES[x]['name']}"
    )

with col2:
    difficulty_filter = st.selectbox(
        "📊 Zorluk",
        options=["all"] + list(DIFFICULTY_LEVELS.keys()),
        format_func=lambda x: "Tümü" if x == "all" else f"{DIFFICULTY_LEVELS[x]['icon']} {DIFFICULTY_LEVELS[x]['name']}"
    )

with col3:
    search_query = st.text_input("🔍 Kelime Ara", placeholder="İngilizce veya Türkçe...")

# Kelimeleri getir
words = get_words(
    status="approved",
    exam_type=exam_filter if exam_filter != "all" else None,
    difficulty=difficulty_filter if difficulty_filter != "all" else None,
    search_query=search_query if search_query else None,
    limit=100
)

st.markdown("---")

if not words:
    st.info("📭 Henüz kelime bulunmuyor. Kelime ekleyerek katkıda bulunabilirsiniz!")
else:
    # İstatistikler
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Toplam Kelime", len(words))
    
    with col2:
        easy = len([w for w in words if w.get("difficulty", 3) <= 2])
        st.metric("🌱 Kolay", easy)
    
    with col3:
        medium = len([w for w in words if w.get("difficulty", 3) == 3])
        st.metric("🌳 Orta", medium)
    
    with col4:
        hard = len([w for w in words if w.get("difficulty", 3) >= 4])
        st.metric("🔥 Zor", hard)
    
    st.markdown("---")
    
    # Görünüm seçimi
    view_mode = st.radio(
        "Görünüm",
        options=["card", "grid", "list"],
        format_func=lambda x: {"card": "🃏 Kart", "grid": "📊 Grid", "list": "📋 Liste"}[x],
        horizontal=True
    )
    
    # Günün kelimesi
    if words:
        with st.expander("📅 Günün Kelimesi", expanded=True):
            # Rastgele bir kelime seç (her gün aynı olması için seed kullan)
            import datetime
            today_seed = int(datetime.date.today().strftime("%Y%m%d"))
            random.seed(today_seed)
            word_of_day = random.choice(words)
            random.seed()  # Seed'i sıfırla
            
            render_word_of_the_day(word_of_day)
    
    st.markdown("---")
    
    if view_mode == "card":
        # Kart görünümü
        if "current_word_index" not in st.session_state:
            st.session_state.current_word_index = 0
        
        current_idx = st.session_state.current_word_index
        
        # Navigasyon
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        
        with col1:
            if st.button("⏮️ İlk", use_container_width=True):
                st.session_state.current_word_index = 0
                st.rerun()
        
        with col2:
            if st.button("◀️ Önceki", use_container_width=True):
                if current_idx > 0:
                    st.session_state.current_word_index -= 1
                    st.rerun()
        
        with col3:
            st.markdown(f"<h3 style='text-align: center;'>{current_idx + 1} / {len(words)}</h3>", unsafe_allow_html=True)
        
        with col4:
            if st.button("Sonraki ▶️", use_container_width=True):
                if current_idx < len(words) - 1:
                    st.session_state.current_word_index += 1
                    st.rerun()
        
        with col5:
            if st.button("Son ⏭️", use_container_width=True):
                st.session_state.current_word_index = len(words) - 1
                st.rerun()
        
        # Kelime kartı
        if current_idx < len(words):
            render_flashcard(words[current_idx], show_example=True, show_ai_button=True)
        
        # Rastgele kelime butonu
        st.markdown("---")
        if st.button("🎲 Rastgele Kelime", use_container_width=True):
            st.session_state.current_word_index = random.randint(0, len(words) - 1)
            st.rerun()
    
    elif view_mode == "grid":
        # Grid görünümü
        render_word_grid(words, columns=3)
    
    else:
        # Liste görünümü
        for i, word in enumerate(words):
            with st.expander(f"**{word.get('english', '')}** - {word.get('turkish', '')}", expanded=False):
                render_flashcard(word, show_example=True, show_ai_button=True)

# Footer
st.markdown("---")
st.caption("💡 İpucu: 'AI ile Örnek Cümle' butonunu kullanarak kelimeler için YDS formatında cümleler oluşturabilirsiniz.")
