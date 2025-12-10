"""
Flashcard Component
Word card display with flip animation
"""

import streamlit as st
from typing import Dict, Any, Optional, List


def get_flashcard_styles() -> str:
    """Flashcard için CSS stilleri"""
    return """
    <style>
    .flashcard-container {
        perspective: 1000px;
        margin: 20px 0;
    }
    
    .flashcard {
        position: relative;
        width: 100%;
        min-height: 280px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 30px;
        color: white;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        transition: transform 0.4s ease, box-shadow 0.4s ease;
    }
    
    .flashcard:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 45px rgba(102, 126, 234, 0.4);
    }
    
    .flashcard-english {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 8px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .flashcard-pronunciation {
        font-size: 16px;
        opacity: 0.85;
        font-style: italic;
        margin-bottom: 16px;
    }
    
    .flashcard-turkish {
        font-size: 24px;
        font-weight: 500;
        margin-bottom: 20px;
        padding: 12px 20px;
        background: rgba(255,255,255,0.15);
        border-radius: 12px;
        display: inline-block;
    }
    
    .flashcard-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 20px;
    }
    
    .flashcard-badge {
        background: rgba(255,255,255,0.2);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        backdrop-filter: blur(5px);
    }
    
    .flashcard-type {
        background: rgba(255,255,255,0.25);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }
    
    .flashcard-synonyms {
        margin-top: 16px;
        padding-top: 16px;
        border-top: 1px solid rgba(255,255,255,0.2);
    }
    
    .flashcard-example {
        margin-top: 16px;
        padding: 16px;
        background: rgba(0,0,0,0.15);
        border-radius: 12px;
        font-style: italic;
        line-height: 1.5;
    }
    
    .difficulty-stars {
        color: #ffd700;
        font-size: 16px;
        letter-spacing: 2px;
    }
    
    /* Mini card stili */
    .mini-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
        border: 1px solid #667eea;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        transition: all 0.3s ease;
    }
    
    .mini-card:hover {
        border-color: #764ba2;
        transform: scale(1.02);
    }
    
    .mini-card-english {
        font-size: 18px;
        font-weight: 600;
        color: #667eea;
    }
    
    .mini-card-turkish {
        font-size: 14px;
        color: #a0aec0;
        margin-top: 4px;
    }
    </style>
    """


def render_flashcard(word: Dict[str, Any], show_example: bool = True, show_ai_button: bool = True):
    """
    Kelime kartını render et
    
    Args:
        word: Kelime verisi
        show_example: Örnek cümle gösterilsin mi
        show_ai_button: AI cümle butonu gösterilsin mi
    """
    from utils.constants import WORD_TYPES, DIFFICULTY_LEVELS, EXAM_TYPES
    
    # Kelime türü bilgisi
    word_type = word.get("type", "noun")
    type_info = WORD_TYPES.get(word_type, WORD_TYPES["noun"])
    
    # Zorluk bilgisi
    difficulty = word.get("difficulty", 3)
    stars = "⭐" * difficulty + "☆" * (5 - difficulty)
    
    # Ana kart HTML - sadece temel bilgiler, iç içe HTML yok
    st.markdown(f'''
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; padding: 30px; color: white; box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3); margin: 20px 0;">
        <div style="font-size: 32px; font-weight: 700; margin-bottom: 8px;">{word.get('english', '')}</div>
        <div style="font-size: 24px; font-weight: 500; margin-bottom: 20px; padding: 12px 20px; background: rgba(255,255,255,0.15); border-radius: 12px; display: inline-block;">{word.get('turkish', '')}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Bilgi etiketleri - Streamlit columns ile
    exam_types = word.get("examTypes", [])
    synonyms = word.get("synonyms", [])
    
    # Etiketler satırı
    tags = []
    tags.append(f"{type_info['abbr']} {type_info['name']}")
    tags.append(stars)
    for et in exam_types:
        if et in EXAM_TYPES:
            tags.append(f"{EXAM_TYPES[et]['icon']} {EXAM_TYPES[et]['name']}")
    
    # Etiketleri göster
    cols = st.columns(len(tags))
    for i, tag in enumerate(tags):
        with cols[i]:
            st.markdown(f"**{tag}**")
    
    # Eş anlamlılar
    if synonyms:
        st.markdown(f"📎 **Eş anlamlılar:** {', '.join(synonyms)}")
    
    # Örnek cümle
    example = word.get("exampleSentence", "")
    if show_example and example:
        st.info(f"💡 **Örnek:** {example}")
    
    # AI Cümle butonu
    if show_ai_button:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🤖 AI ile Örnek Cümle", key=f"ai_btn_{word.get('id', '')}"):
                generate_ai_sentence(word)
        
        with col2:
            if st.button("💡 Hatırlama İpucu", key=f"hint_btn_{word.get('id', '')}"):
                generate_memory_hint(word)


def generate_ai_sentence(word: Dict[str, Any]):
    """AI ile örnek cümle oluştur"""
    from services.groq_service import generate_example_sentence, check_groq_availability
    
    if not check_groq_availability():
        st.warning("⚠️ AI servisi şu anda kullanılamıyor.")
        return
    
    with st.spinner("🤖 AI cümle oluşturuyor..."):
        result = generate_example_sentence(
            word.get("english", ""),
            word.get("type", "noun"),
            word.get("turkish", "")
        )
        
        if result:
            st.success("✨ **AI Örnek Cümle:**")
            
            # İngilizce cümle
            english_sentence = result.get("english", "")
            if english_sentence:
                st.markdown(f"""
                <div style="background: rgba(102, 126, 234, 0.1); border-left: 4px solid #667eea; padding: 15px; border-radius: 8px; margin: 10px 0;">
                    <div style="font-size: 16px; color: #fff; margin-bottom: 8px;">🇬🇧 <strong>English:</strong></div>
                    <div style="font-size: 15px; color: #e0e0e0; font-style: italic;">{english_sentence}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Türkçe çeviri
            turkish_sentence = result.get("turkish", "")
            if turkish_sentence:
                st.markdown(f"""
                <div style="background: rgba(231, 76, 60, 0.1); border-left: 4px solid #e74c3c; padding: 15px; border-radius: 8px; margin: 10px 0;">
                    <div style="font-size: 16px; color: #fff; margin-bottom: 8px;">🇹🇷 <strong>Türkçe:</strong></div>
                    <div style="font-size: 15px; color: #e0e0e0;">{turkish_sentence}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Cümle oluşturulamadı. Lütfen tekrar deneyin.")


def generate_memory_hint(word: Dict[str, Any]):
    """Hafıza ipucu oluştur"""
    from services.groq_service import get_ai_hint, check_groq_availability
    
    if not check_groq_availability():
        st.warning("⚠️ AI servisi şu anda kullanılamıyor.")
        return
    
    with st.spinner("💡 İpucu oluşturuluyor..."):
        hint = get_ai_hint(
            word.get("english", ""),
            f"Türkçe anlamı: {word.get('turkish', '')}"
        )
        
        if hint:
            st.success("💡 **Hatırlama İpucu:**")
            st.info(hint)
        else:
            st.error("İpucu oluşturulamadı. Lütfen tekrar deneyin.")


def render_mini_card(word: Dict[str, Any], on_click_key: str = None):
    """
    Mini kelime kartı (liste görünümü için)
    """
    from utils.constants import WORD_TYPES, DIFFICULTY_LEVELS
    
    word_type = word.get("type", "noun")
    type_info = WORD_TYPES.get(word_type, WORD_TYPES["noun"])
    difficulty = word.get("difficulty", 3)
    stars = "⭐" * difficulty
    
    with st.container():
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.markdown(f"**{word.get('english', '')}**")
            st.caption(word.get('turkish', ''))
        
        with col2:
            st.markdown(f"`{type_info['abbr']}`")
            st.caption(stars)
        
        with col3:
            if on_click_key:
                st.button("👁️", key=on_click_key)


def render_word_grid(words: List[Dict[str, Any]], columns: int = 3):
    """
    Kelime grid'i render et
    
    Args:
        words: Kelime listesi
        columns: Sütun sayısı
    """
    from utils.constants import WORD_TYPES
    
    st.markdown(get_flashcard_styles(), unsafe_allow_html=True)
    
    # Grid oluştur
    for i in range(0, len(words), columns):
        cols = st.columns(columns)
        
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(words):
                word = words[idx]
                word_type = word.get("type", "noun")
                type_info = WORD_TYPES.get(word_type, WORD_TYPES["noun"])
                difficulty = word.get("difficulty", 3)
                stars = "⭐" * difficulty
                
                with col:
                    st.markdown(f"""
                    <div class="mini-card">
                        <div class="mini-card-english">{word.get('english', '')}</div>
                        <div class="mini-card-turkish">{word.get('turkish', '')}</div>
                        <div style="margin-top: 8px;">
                            <span style="color: {type_info['color']}; font-size: 12px;">{type_info['abbr']}</span>
                            <span style="font-size: 12px;">{stars}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


def render_word_of_the_day(word: Dict[str, Any]):
    """Günün kelimesi kartı"""
    st.markdown("""
    <style>
    .wotd-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 20px;
        padding: 30px;
        color: white;
        text-align: center;
        margin: 20px 0;
    }
    .wotd-title {
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 2px;
        opacity: 0.9;
        margin-bottom: 10px;
    }
    .wotd-word {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .wotd-meaning {
        font-size: 20px;
        opacity: 0.95;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="wotd-container">
        <div class="wotd-title">📅 Günün Kelimesi</div>
        <div class="wotd-word">{word.get('english', '')}</div>
        <div class="wotd-meaning">{word.get('turkish', '')}</div>
    </div>
    """, unsafe_allow_html=True)
